"""
Script to generate notebooks/02_model_training_and_tuning.ipynb
ConnectTel / Persevex AI Internship Project.
"""

import json
from pathlib import Path

NOTEBOOK_PATH = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\notebooks\02_model_training_and_tuning.ipynb")

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Predictive Customer Churn Model for ConnectTel\n",
            "## Phase 2: Model Training, Stratified K-Fold CV & Hyperparameter Tuning\n",
            "\n",
            "**Author:** Persevex AI Intern  \n",
            "**Domain:** Artificial Intelligence / Customer Retention Machine Learning  \n",
            "**Dataset:** 320 Synthetic Telecom Records (`customers.csv`)  \n",
            "**Splits in Use:** Training ($N=192$, Churners=37), Validation ($N=64$, Churners=9)  \n",
            "**Test Partition ($N=64$):** Strictly locked and quarantined for final evaluation only.  \n",
            "\n",
            "---"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. Phase 2 Objectives & Methodology\n",
            "\n",
            "In this phase, we develop, optimize, and rigorously evaluate three distinct classes of classification algorithms:\n",
            "1. **Logistic Regression:** Linear baseline providing interpretable odds ratios and calibrated probabilities.\n",
            "2. **Random Forest:** Non-linear ensemble model capturing complex interactions among features.\n",
            "3. **XGBoost:** State-of-the-art gradient boosted decision trees optimized for tabular classification.\n",
            "\n",
            "#### Rigorous Data Science Guardrails:\n",
            "- **Leakage Prevention:** Feature engineering, imputers, and standard scalers are fitted **strictly inside each fold** via Scikit-Learn `Pipeline`.\n",
            "- **Stratified 5-Fold Cross-Validation:** Preserves the 19.3% positive class ratio across all 5 training folds (~7-8 churners per fold).\n",
            "- **GridSearchCV Hyperparameter Optimization:** Tuned using `roc_auc` scoring over focused, compact search spaces.\n",
            "- **Zero-Test-Data Rule:** The test set ($N=64$) is never used for hyperparameter tuning, model selection, or threshold calibration."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Environment & Module Imports\n",
            "import os, sys\n",
            "from pathlib import Path\n",
            "\n",
            "PROJECT_ROOT = Path('.').resolve().parent\n",
            "for p in [str(PROJECT_ROOT), str(PROJECT_ROOT / 'src')]:\n",
            "    if p not in sys.path:\n",
            "        sys.path.append(p)\n",
            "\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import joblib\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "from data_loader import load_raw_data, get_splits\n",
            "from feature_engineering import get_full_feature_pipeline\n",
            "from models import train_and_tune_models, evaluate_on_validation, analyze_thresholds\n",
            "\n",
            "print('Phase 2 modules loaded successfully.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2. Data Loading & Partition Verification\n",
            "\n",
            "We load the primary dataset and extract feature matrices, ensuring metadata (`customer_id`, `snapshot_date`, `split`) and target (`churn_30d`) are separated."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "raw_df = load_raw_data()\n",
            "X_train, y_train, X_val, y_val, X_test, y_test = get_splits(raw_df)\n",
            "\n",
            "print(f'Training Set:   X={X_train.shape}, Churners={y_train.sum()} ({y_train.mean()*100:.2f}%)')\n",
            "print(f'Validation Set: X={X_val.shape}, Churners={y_val.sum()} ({y_val.mean()*100:.2f}%)')\n",
            "print(f'Test Set:       X={X_test.shape} [QUARANTINED]')\n",
            "print('Features:', list(X_train.columns))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3. Model Training & Hyperparameter Tuning (GridSearchCV)\n",
            "\n",
            "We tune Logistic Regression, Random Forest, and XGBoost using Stratified 5-Fold Cross Validation."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load serialized models from models/ or inspect validation comparison table\n",
            "comparison_df = pd.read_csv(PROJECT_ROOT / 'outputs' / 'tables' / 'model_comparison_validation.csv')\n",
            "comparison_df"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 4. Diagnostic Performance Visualizations\n",
            "\n",
            "We review the validation diagnostic charts generated in `outputs/model_eval_figures/`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Image, display\n",
            "\n",
            "figs = [\n",
            "    ('Figure 1: Validation ROC Curves', PROJECT_ROOT / 'outputs' / 'model_eval_figures' / '01_roc_curves_validation.png'),\n",
            "    ('Figure 2: Validation Precision-Recall Curves', PROJECT_ROOT / 'outputs' / 'model_eval_figures' / '02_pr_curves_validation.png'),\n",
            "    ('Figure 3: Confusion Matrices at Threshold = 0.50', PROJECT_ROOT / 'outputs' / 'model_eval_figures' / '03_confusion_matrices_validation.png'),\n",
            "    ('Figure 4: Threshold Analysis & Precision-Recall Trade-off', PROJECT_ROOT / 'outputs' / 'model_eval_figures' / '04_threshold_tradeoff_curves.png'),\n",
            "    ('Figure 5: Model Metric Summary (ROC-AUC, PR-AUC, Brier Score)', PROJECT_ROOT / 'outputs' / 'model_eval_figures' / '05_model_metrics_summary.png')\n",
            "]\n",
            "\n",
            "for title, p in figs:\n",
            "    if p.exists():\n",
            "        print(f'=== {title} ===')\n",
            "        display(Image(filename=str(p)))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5. Classification Threshold Analysis\n",
            "\n",
            "In telecom churn prevention, false negatives (failing to identify a churning customer) often carry higher business cost than false positives (offering a retention discount to a retained customer).\n",
            "We examine precision, recall, and F1 across decision thresholds."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "thresh_df = pd.read_csv(PROJECT_ROOT / 'outputs' / 'tables' / 'threshold_analysis.csv')\n",
            "print('--- Top F1 Thresholds for Logistic Regression ---')\n",
            "display(thresh_df[thresh_df['Model'] == 'Logistic Regression'].sort_values(by='F1_Score', ascending=False).head(5))\n",
            "\n",
            "print('--- Top F1 Thresholds for Random Forest ---')\n",
            "display(thresh_df[thresh_df['Model'] == 'Random Forest'].sort_values(by='F1_Score', ascending=False).head(5))\n",
            "\n",
            "print('--- Top F1 Thresholds for XGBoost ---')\n",
            "display(thresh_df[thresh_df['Model'] == 'XGBoost'].sort_values(by='F1_Score', ascending=False).head(5))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 6. Baseline Benchmark Comparison\n",
            "\n",
            "- **ContractGroupBaseline:** Achieves Validation ROC-AUC of **0.6121** and PR-AUC of **0.2289** with Brier score **0.1190**.\n",
            "- **Logistic Regression:** Achieves Validation ROC-AUC of **0.7737** (+0.1616 over baseline) and PR-AUC of **0.5039** (+0.2750 over baseline).\n",
            "- **Why Brier Score Differs:** The baseline assigns conservative probabilities (all between 0.12 and 0.31) with zero recall at threshold 0.50. Logistic Regression applies class-weight balancing to identify true churners, achieving **77.8% Recall**."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 7. Phase 2 Conclusion & Selection of Champion Model\n",
            "\n",
            "- **Champion Model Selected:** **Logistic Regression** (`C=5.0`, `class_weight='balanced'`).\n",
            "- **Rationale:** Highest validation ROC-AUC ($0.7737$), highest PR-AUC ($0.5039$), highest F1 ($0.4516$ at 0.50, $0.4667$ at 0.55), catching **7 out of 9 churners** (Recall = $77.8%$).\n",
            "- **Next Step (Phase 3):** Explainability via **SHAP (SHapley Additive exPlanations)** to answer key business retention questions."
        ]
    }
]

notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.13.5"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

NOTEBOOK_PATH.write_text(json.dumps(notebook_json, indent=2), encoding="utf-8")
print(f"Phase 2 notebook written to: {NOTEBOOK_PATH}")
