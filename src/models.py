"""
Model Training, Hyperparameter Tuning & Evaluation Module.
ConnectTel / Persevex AI Internship Project (Phase 2).

Includes:
1. Logistic Regression, Random Forest, and XGBoost Classifiers.
2. Stratified 5-Fold Cross Validation within Training partition only (N=192).
3. GridSearchCV hyperparameter optimization with ROC-AUC scoring.
4. Comprehensive validation evaluation (ROC-AUC, PR-AUC, Precision, Recall, F1, Brier Score).
5. Threshold analysis and precision-recall trade-off examination.
6. Baseline comparison against ContractGroupBaseline.
7. Model artifact serialization (joblib) and publication-quality visual diagnostics.
"""

import os
import sys
from pathlib import Path
import json
from typing import Dict, Tuple, Any, List, Optional

import numpy as np
import pandas as pd
import joblib

# Headless matplotlib configuration
os.environ["MPLCONFIGDIR"] = str(Path(__file__).resolve().parent.parent / ".mplconfig")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
    brier_score_loss,
    roc_curve,
    precision_recall_curve,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "src"))

FIGURES_DIR = PROJECT_ROOT / "outputs" / "model_eval_figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
MODELS_DIR = PROJECT_ROOT / "models"

for d in [FIGURES_DIR, TABLES_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150


def get_model_definitions(random_state: int = 42) -> Dict[str, Tuple[Any, Dict[str, List[Any]]]]:
    """
    Define models and their respective compact hyperparameter grids.
    Designed for small, imbalanced datasets (N=192, 37 churners).
    """
    # Positive class weighting factor: 155 non-churn / 37 churn = ~4.19
    pos_scale = 155.0 / 37.0
    
    models = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000, random_state=random_state),
            {
                "classifier__C": [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0],
                "classifier__class_weight": [None, "balanced"]
            }
        ),
        "Random Forest": (
            RandomForestClassifier(random_state=random_state),
            {
                "classifier__n_estimators": [50, 100],
                "classifier__max_depth": [3, 5, 8],
                "classifier__min_samples_split": [2, 5],
                "classifier__min_samples_leaf": [1, 2],
                "classifier__class_weight": [None, "balanced"]
            }
        ),
        "XGBoost": (
            xgb.XGBClassifier(
                random_state=random_state,
                eval_metric="logloss"
            ),
            {
                "classifier__n_estimators": [30, 60, 100],
                "classifier__max_depth": [2, 3],
                "classifier__learning_rate": [0.03, 0.08, 0.15],
                "classifier__scale_pos_weight": [1.0, pos_scale],
                "classifier__subsample": [0.8, 1.0],
                "classifier__colsample_bytree": [0.8, 1.0]
            }
        )
    }
    return models


def train_and_tune_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    random_state: int = 42
) -> Dict[str, GridSearchCV]:
    """
    Train and tune all candidate models using Stratified K-Fold CV inside the training partition only.
    Independent feature engineering pipeline is enclosed in every candidate Pipeline.
    """
    from feature_engineering import get_full_feature_pipeline
    
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    model_defs = get_model_definitions(random_state=random_state)
    fitted_grids = {}
    
    print(f"--- Starting Stratified {n_splits}-Fold Cross-Validation on Training Data (N={len(X_train)}) ---")
    
    for name, (base_clf, param_grid) in model_defs.items():
        print(f"\n[Training] Optimizing {name} with GridSearchCV...")
        preprocessor, _, _ = get_full_feature_pipeline()
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", base_clf)
        ])
        
        grid = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=cv,
            scoring="roc_auc",
            n_jobs=1,
            refit=True,
            return_train_score=True
        )
        grid.fit(X_train, y_train)
        
        cv_auc = grid.best_score_
        print(f"  -> Best CV ROC-AUC: {cv_auc:.4f}")
        print(f"  -> Best Hyperparameters: {grid.best_params_}")
        fitted_grids[name] = grid
        
    return fitted_grids


def evaluate_on_validation(
    fitted_grids: Dict[str, GridSearchCV],
    X_val: pd.DataFrame,
    y_val: pd.Series,
    baseline_brier: float = 0.119013,
    default_threshold: float = 0.5
) -> pd.DataFrame:
    """
    Evaluate all tuned models on the validation set (N=64).
    Computes ROC-AUC, PR-AUC, Precision, Recall, F1, and Brier Score.
    """
    records = []
    
    # 1. Baseline Benchmark Record
    records.append({
        "Model": "ContractGroupBaseline (Prior)",
        "Tuned Params": "Empirical Bayes Laplace-smoothed contract rate",
        "CV Mean ROC-AUC": np.nan,
        "Val ROC-AUC": 0.6121, # Empirical ranking on validation
        "Val PR-AUC": 0.2289,
        "Val Precision (0.5)": 0.0, # Baseline max prob is 0.3148, so at 0.5 it predicts 0 positives
        "Val Recall (0.5)": 0.0,
        "Val F1 (0.5)": 0.0,
        "Val Brier Score": baseline_brier,
        "Brier Skill Score vs Baseline": 0.0000
    })
    
    for name, grid in fitted_grids.items():
        best_pipe = grid.best_estimator_
        y_val_prob = best_pipe.predict_proba(X_val)[:, 1]
        y_val_pred = (y_val_prob >= default_threshold).astype(int)
        
        val_auc = roc_auc_score(y_val, y_val_prob)
        val_pr_auc = average_precision_score(y_val, y_val_prob)
        val_prec = precision_score(y_val, y_val_pred, zero_division=0)
        val_rec = recall_score(y_val, y_val_pred, zero_division=0)
        val_f1 = f1_score(y_val, y_val_pred, zero_division=0)
        val_brier = brier_score_loss(y_val, y_val_prob)
        brier_skill = 1.0 - (val_brier / baseline_brier)
        
        records.append({
            "Model": name,
            "Tuned Params": str(grid.best_params_),
            "CV Mean ROC-AUC": grid.best_score_,
            "Val ROC-AUC": val_auc,
            "Val PR-AUC": val_pr_auc,
            "Val Precision (0.5)": val_prec,
            "Val Recall (0.5)": val_rec,
            "Val F1 (0.5)": val_f1,
            "Val Brier Score": val_brier,
            "Brier Skill Score vs Baseline": brier_skill
        })
        
    df_results = pd.DataFrame(records)
    df_results.to_csv(TABLES_DIR / "model_comparison_validation.csv", index=False)
    print(f"\nSaved validation comparison table to {TABLES_DIR / 'model_comparison_validation.csv'}")
    return df_results


def analyze_thresholds(
    fitted_grids: Dict[str, GridSearchCV],
    X_val: pd.DataFrame,
    y_val: pd.Series,
    threshold_range: Optional[np.ndarray] = None
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Examine precision, recall, and F1 across decision thresholds in [0.10, 0.90].
    Identifies the optimal F1 threshold for each model strictly on Validation data.
    """
    if threshold_range is None:
        threshold_range = np.linspace(0.10, 0.85, 16)
        
    rows = []
    best_thresholds = {}
    
    for name, grid in fitted_grids.items():
        best_pipe = grid.best_estimator_
        y_val_prob = best_pipe.predict_proba(X_val)[:, 1]
        
        best_f1 = -1.0
        best_th = 0.5
        
        for th in threshold_range:
            preds = (y_val_prob >= th).astype(int)
            prec = precision_score(y_val, preds, zero_division=0)
            rec = recall_score(y_val, preds, zero_division=0)
            f1 = f1_score(y_val, preds, zero_division=0)
            
            # Confusion matrix counts
            tn, fp, fn, tp = confusion_matrix(y_val, preds, labels=[0, 1]).ravel()
            
            rows.append({
                "Model": name,
                "Threshold": round(th, 2),
                "Precision": round(prec, 4),
                "Recall": round(rec, 4),
                "F1_Score": round(f1, 4),
                "TP": tp, "FP": fp, "FN": fn, "TN": tn
            })
            
            if f1 > best_f1:
                best_f1 = f1
                best_th = round(th, 2)
                
        best_thresholds[name] = best_th
        
    df_thresholds = pd.DataFrame(rows)
    df_thresholds.to_csv(TABLES_DIR / "threshold_analysis.csv", index=False)
    
    print("\nOptimal Validation Thresholds (Maximizing F1):")
    for m_name, opt_th in best_thresholds.items():
        opt_row = df_thresholds[(df_thresholds["Model"] == m_name) & (df_thresholds["Threshold"] == opt_th)].iloc[0]
        print(f"  {m_name:20s}: Optimal Threshold = {opt_th:.2f} | Precision = {opt_row['Precision']:.2f} | Recall = {opt_row['Recall']:.2f} | F1 = {opt_row['F1_Score']:.2f} (TP={opt_row['TP']}, FP={opt_row['FP']})")
        
    return df_thresholds, best_thresholds


def generate_evaluation_plots(
    fitted_grids: Dict[str, GridSearchCV],
    X_val: pd.DataFrame,
    y_val: pd.Series,
    baseline_probs: Optional[np.ndarray] = None
):
    """
    Generate complete set of diagnostic evaluation charts on Validation data.
    """
    print("\n--- Generating Model Diagnostic Plots ---")
    
    colors = {
        "Logistic Regression": "#2b5c8f",
        "Random Forest": "#2ca02c",
        "XGBoost": "#d95f02"
    }
    
    # -------------------------------------------------------------
    # 1. ROC Curves Comparison
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    
    for name, grid in fitted_grids.items():
        best_pipe = grid.best_estimator_
        y_val_prob = best_pipe.predict_proba(X_val)[:, 1]
        fpr, tpr, _ = roc_curve(y_val, y_val_prob)
        auc_val = roc_auc_score(y_val, y_val_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", color=colors[name], lw=2.2)
        
    if baseline_probs is not None:
        fpr_b, tpr_b, _ = roc_curve(y_val, baseline_probs)
        auc_b = roc_auc_score(y_val, baseline_probs)
        plt.plot(fpr_b, tpr_b, label=f"Contract Baseline (AUC = {auc_b:.3f})", color="gray", linestyle="--", lw=1.8)
        
    plt.plot([0, 1], [0, 1], color="black", linestyle=":", label="Random Chance (AUC = 0.500)")
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    plt.ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    plt.title("Figure 1: ROC Curves on Validation Set (N=64)", fontsize=13, fontweight="bold")
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    p1 = FIGURES_DIR / "01_roc_curves_validation.png"
    plt.savefig(p1)
    plt.close()
    print(f"Saved: {p1.name}")
    
    # -------------------------------------------------------------
    # 2. Precision-Recall Curves Comparison
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    base_rate = y_val.mean()
    
    for name, grid in fitted_grids.items():
        best_pipe = grid.best_estimator_
        y_val_prob = best_pipe.predict_proba(X_val)[:, 1]
        prec, rec, _ = precision_recall_curve(y_val, y_val_prob)
        ap = average_precision_score(y_val, y_val_prob)
        plt.plot(rec, prec, label=f"{name} (PR-AUC = {ap:.3f})", color=colors[name], lw=2.2)
        
    plt.axhline(base_rate, color="gray", linestyle=":", label=f"Prevalence Baseline ({base_rate:.3f})")
    plt.xlabel("Recall", fontsize=11)
    plt.ylabel("Precision", fontsize=11)
    plt.title("Figure 2: Precision-Recall Curves on Validation Set (N=64)", fontsize=13, fontweight="bold")
    plt.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    p2 = FIGURES_DIR / "02_pr_curves_validation.png"
    plt.savefig(p2)
    plt.close()
    print(f"Saved: {p2.name}")
    
    # -------------------------------------------------------------
    # 3. Confusion Matrices Heatmaps
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    for i, (name, grid) in enumerate(fitted_grids.items()):
        best_pipe = grid.best_estimator_
        y_val_pred = (best_pipe.predict_proba(X_val)[:, 1] >= 0.5).astype(int)
        cm = confusion_matrix(y_val, y_val_pred)
        
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Retained (0)", "Churned (1)"])
        disp.plot(ax=axes[i], cmap="Blues", colorbar=False, values_format="d")
        
        # Calculate accuracy, prec, recall for title
        rec = recall_score(y_val, y_val_pred, zero_division=0)
        prec = precision_score(y_val, y_val_pred, zero_division=0)
        axes[i].set_title(f"{name}\n(Prec={prec:.2f}, Rec={rec:.2f})", fontsize=11, fontweight="bold")
        axes[i].grid(False)
        
    plt.suptitle("Figure 3: Validation Confusion Matrices at Threshold = 0.50 (N=64)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    p3 = FIGURES_DIR / "03_confusion_matrices_validation.png"
    plt.savefig(p3)
    plt.close()
    print(f"Saved: {p3.name}")
    
    # -------------------------------------------------------------
    # 4. Precision-Recall-F1 vs Threshold Curves
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    thresholds = np.linspace(0.1, 0.85, 30)
    
    for i, (name, grid) in enumerate(fitted_grids.items()):
        best_pipe = grid.best_estimator_
        probs = best_pipe.predict_proba(X_val)[:, 1]
        
        precs, recs, f1s = [], [], []
        for th in thresholds:
            p = (probs >= th).astype(int)
            precs.append(precision_score(y_val, p, zero_division=0))
            recs.append(recall_score(y_val, p, zero_division=0))
            f1s.append(f1_score(y_val, p, zero_division=0))
            
        axes[i].plot(thresholds, precs, label="Precision", color="#2b5c8f", lw=2)
        axes[i].plot(thresholds, recs, label="Recall", color="#d95f02", lw=2)
        axes[i].plot(thresholds, f1s, label="F1-Score", color="#2ca02c", lw=2, linestyle="--")
        axes[i].axvline(0.5, color="gray", linestyle=":", label="Default (0.50)")
        
        opt_idx = np.argmax(f1s)
        axes[i].scatter([thresholds[opt_idx]], [f1s[opt_idx]], color="red", s=60, zorder=5, label=f"Max F1 ({thresholds[opt_idx]:.2f})")
        
        axes[i].set_title(name, fontsize=12, fontweight="bold")
        axes[i].set_xlabel("Decision Threshold")
        if i == 0:
            axes[i].set_ylabel("Metric Score")
        axes[i].legend(loc="best", fontsize=9)
        axes[i].set_ylim(-0.05, 1.05)
        
    plt.suptitle("Figure 4: Threshold Analysis & Precision-Recall Trade-off (Validation Set)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    p4 = FIGURES_DIR / "04_threshold_tradeoff_curves.png"
    plt.savefig(p4)
    plt.close()
    print(f"Saved: {p4.name}")
    
    # -------------------------------------------------------------
    # 5. Model Metrics Summary Bar Chart
    # -------------------------------------------------------------
    df_metrics = pd.read_csv(TABLES_DIR / "model_comparison_validation.csv")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    plot_df = df_metrics.melt(
        id_vars=["Model"],
        value_vars=["Val ROC-AUC", "Val PR-AUC", "Val Brier Score"],
        var_name="Metric",
        value_name="Score"
    )
    
    sns.barplot(data=plot_df, x="Model", y="Score", hue="Metric", palette="Set2", ax=ax, edgecolor="black")
    ax.set_title("Figure 5: Model Metric Comparison on Validation Set (Lower Brier is Better)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Score")
    ax.set_xticks(range(4))
    ax.set_xticklabels(["Contract Prior", "Logistic Reg", "Random Forest", "XGBoost"], rotation=0)
    ax.legend(title="Metric", loc="upper right")
    ax.set_ylim(0, 0.95)
    
    for p in ax.patches:
        h = p.get_height()
        if h > 0.03:
            ax.annotate(f"{h:.3f}", (p.get_x() + p.get_width() / 2., h + 0.015),
                        ha="center", va="bottom", fontsize=8, fontweight="bold")
            
    plt.tight_layout()
    p5 = FIGURES_DIR / "05_model_metrics_summary.png"
    plt.savefig(p5)
    plt.close()
    print(f"Saved: {p5.name}")


def save_best_artifacts(
    fitted_grids: Dict[str, GridSearchCV],
    val_results: pd.DataFrame,
    best_model_name: str
):
    """
    Serialize models to disk and export full evaluation records.
    """
    for name, grid in fitted_grids.items():
        fname = name.lower().replace(" ", "_")
        joblib.dump(grid.best_estimator_, MODELS_DIR / f"{fname}_pipeline.joblib")
        
    best_pipe = fitted_grids[best_model_name].best_estimator_
    joblib.dump(best_pipe, MODELS_DIR / "best_model_pipeline.joblib")
    print(f"\nSaved best model ({best_model_name}) pipeline to {MODELS_DIR / 'best_model_pipeline.joblib'}")


def run_phase_2(random_state: int = 42):
    """
    Execute full Phase 2 workflow: training, tuning, validation evaluation,
    threshold analysis, and artifact generation.
    """
    from data_loader import load_raw_data, get_splits
    from baseline import ContractGroupBaseline, load as load_baseline_data
    
    raw_df = load_raw_data()
    X_train, y_train, X_val, y_val, X_test, y_test = get_splits(raw_df)
    
    print("=" * 70)
    print("PHASE 2: MODEL TRAINING, HYPERPARAMETER TUNING & VALIDATION")
    print("=" * 70)
    print(f"Training Data:   X={X_train.shape}, Churners={y_train.sum()} ({y_train.mean()*100:.1f}%)")
    print(f"Validation Data: X={X_val.shape}, Churners={y_val.sum()} ({y_val.mean()*100:.1f}%)")
    print(f"Test Data:       X={X_test.shape} [LOCKED & QUARANTINED]")
    
    # 1. Train and tune models with 5-fold CV
    fitted_grids = train_and_tune_models(X_train, y_train, n_splits=5, random_state=random_state)
    
    # 2. Get baseline validation probabilities for fair comparison
    baseline_rows = load_baseline_data("customers.csv")
    train_rows = [r for r in baseline_rows if r["split"] == "train"]
    val_rows = [r for r in baseline_rows if r["split"] == "validation"]
    
    base_model = ContractGroupBaseline()
    base_model.fit(train_rows)
    val_base_probs = np.array([base_model.predict_proba(r["contract"]) for r in val_rows])
    val_base_brier = sum((p - int(r["churn_30d"])) ** 2 for p, r in zip(val_base_probs, val_rows)) / len(val_rows)
    
    # 3. Evaluate on validation
    val_results = evaluate_on_validation(fitted_grids, X_val, y_val, baseline_brier=val_base_brier)
    
    # 4. Threshold analysis
    threshold_results, best_thresholds = analyze_thresholds(fitted_grids, X_val, y_val)
    
    # 5. Diagnostic plots
    generate_evaluation_plots(fitted_grids, X_val, y_val, baseline_probs=val_base_probs)
    
    # 6. Determine best model based on ROC-AUC and PR-AUC on Validation
    # Filter ML models
    ml_results = val_results[val_results["Model"] != "ContractGroupBaseline (Prior)"]
    best_row = ml_results.sort_values(by=["Val ROC-AUC", "Val PR-AUC"], ascending=False).iloc[0]
    best_name = best_row["Model"]
    
    print("\n" + "=" * 70)
    print(f"BEST PERFORMING MODEL ON VALIDATION: {best_name}")
    print(f"  Val ROC-AUC:     {best_row['Val ROC-AUC']:.4f}")
    print(f"  Val PR-AUC:      {best_row['Val PR-AUC']:.4f}")
    print(f"  Val Brier Score: {best_row['Val Brier Score']:.6f} (Skill: {best_row['Brier Skill Score vs Baseline']:.4f})")
    print(f"  Optimal Threshold (Max F1): {best_thresholds[best_name]}")
    print("=" * 70)
    
    # 7. Save serialized model artifacts
    save_best_artifacts(fitted_grids, val_results, best_name)
    
    return fitted_grids, val_results, threshold_results, best_name


if __name__ == "__main__":
    run_phase_2()
