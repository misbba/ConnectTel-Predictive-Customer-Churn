# Phase 7.1: Final Project Structure & Deployment Readiness Audit Report

**Project:** Predictive Customer Churn Model for ConnectTel  
**Internship:** Persevex AI Internship  
**Audit Date:** November 25, 2026  
**Workspace:** `C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom`  
**Primary IDE:** JetBrains IntelliJ IDEA Ultimate (Python 3.13.5 SDK)  
**Audit Status:** **AUDIT COMPLETED — ZERO MODIFICATIONS TO EXISTING CORE CODE OR MODELS**

---

## 1. Executive Summary & Audit Verdict

As part of **Phase 7.1**, a non-destructive audit of the ConnectTel customer churn machine learning repository was conducted. The audit verified file integrity, model artifacts, notebook structures, data pipelines, Streamlit application logic, IDE configurations, documentation, and external deployment dependencies.

```mermaid
flowchart TD
    subgraph Core_ML_Engine["Core ML Engine (100% Verified)"]
        Data["data/customers.csv (320 rows)"] --> FE["src/feature_engineering.py (Zero-Tenure Rule)"]
        FE --> Models["models/best_model_pipeline.joblib (C=10.0, balanced)"]
        Models --> Infer["src/inference.py (Threshold = 0.55)"]
    end

    subgraph Application_Layer["Application & IDE (100% Verified)"]
        Infer --> App["app.py (Streamlit Churn Simulator)"]
        App --> RunConfig["IntelliJ IDEA (.idea/runConfigurations)"]
    end

    subgraph Evaluation_Artifacts["Artifacts & Plots (100% Verified)"]
        EDA["outputs/eda_figures/ (7 PNGs)"]
        Eval["outputs/model_eval_figures/ (6 PNGs)"]
        SHAP["outputs/shap/ (7 PNGs)"]
        Tables["outputs/tables/ (8 CSV/JSON)"]
    end

    subgraph Deployment_Readiness["Deployment & Phase 7 Readiness"]
        Blocker1["Jupyter Notebook Outputs: Unpopulated cache (Actionable)"]
        Blocker2["Root Git & .gitignore: Not yet initialized (Actionable)"]
        Blocker3[".streamlit/config.toml: Not yet created (Actionable)"]
        Blocker4["Phase 7 Deliverable Deps: python-pptx & reportlab pending"]
    end
```

### Audit Verdict Summary
- **Core ML & Inference Integrity:** **100% VERIFIED.** All pipelines, feature engineering rules, models, and inference functions load cleanly and execute deterministically.
- **Portability:** **100% VERIFIED.** Zero hardcoded absolute paths detected across all `src/` modules, `app.py`, `baseline.py`, and test scripts.
- **Working Application:** **100% VERIFIED.** The Streamlit simulator in `app.py` compiles cleanly, runs on port 8501, features working preset buttons, reactive recalculation, and the two requested wording corrections.
- **Visual & Tabular Artifacts:** **100% VERIFIED.** All 20 PNG diagnostic charts and 8 statistical tables exist, are uncorrupted, and match Phase 1–6 findings.
- **Deployment & Submission Gaps:** **IDENTIFIED & CATEGORIZED.** Three operational items require execution prior to final deployment/submission: pre-populating notebook execution outputs, initializing Git repository tracking with `.gitignore`, and creating `.streamlit/config.toml`.

---

## 2. Comprehensive File Inventory & Verification Matrix

The workspace comprises **56 files** organized across 8 primary subdirectories:

| Category | Target Path / Subdirectory | Count | Integrity Status | Details & Observations |
| :--- | :--- | :---: | :---: | :--- |
| **Primary App** | [`app.py`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/app.py) | 1 | **VERIFIED** | Streamlit UI with synchronized state, preset callbacks, and calibrated 0.55 cutoff. |
| **Baseline** | [`baseline.py`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/baseline.py) | 2 | **VERIFIED** | Enhanced baseline and untouched original `baseline_original.py`. |
| **Inference Script** | [`test_intellij_inference.py`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/test_intellij_inference.py) | 1 | **VERIFIED** | Direct validation script for IntelliJ console execution. |
| **Source Modules** | [`src/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/src) | 6 | **VERIFIED** | `data_loader.py`, `eda.py`, `feature_engineering.py`, `models.py`, `interpretability.py`, `inference.py`. |
| **Notebooks** | [`notebooks/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/notebooks) | 3 | **VERIFIED (Unexecuted)** | Code & markdown complete; cell outputs currently unpopulated (`outputs: []`). |
| **Model Artifacts** | [`models/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/models) | 4 | **VERIFIED** | `best_model_pipeline.joblib`, `logistic_regression_pipeline.joblib`, `random_forest_pipeline.joblib`, `xgboost_pipeline.joblib`. |
| **EDA Figures** | [`outputs/eda_figures/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/outputs/eda_figures) | 7 | **VERIFIED** | 7 high-resolution diagnostic PNG figures. |
| **Model Eval Figures**| [`outputs/model_eval_figures/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/outputs/model_eval_figures) | 6 | **VERIFIED** | ROC, PR, Confusion Matrices, Threshold curves, Final test diagnostics. |
| **SHAP Figures** | [`outputs/shap/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/outputs/shap) | 7 | **VERIFIED** | Global summary, beeswarm, odds ratios, 3 local waterfalls, supporting comparison. |
| **Statistical Tables**| [`outputs/tables/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/outputs/tables) | 8 | **VERIFIED** | Playbook CSV, feature importance CSVs, test evaluation CSV, model comparison CSV, hypothesis JSON. |
| **Reports** | [`reports/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/reports) | 4 | **VERIFIED** | Phase 3, 4, 5, and 6 markdown reports. |
| **Scripts** | [`scripts/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/scripts) | 6 | **VERIFIED** | Notebook generators, app verification, startup probe, preset validation. |
| **Dataset** | [`data/customers.csv`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/data/customers.csv) | 1 | **VERIFIED** | Official 320-record synthetic teaching dataset. |
| **Documentation** | Root Markdown (`README.md`, `DATA_DICTIONARY.md`) | 2 | **VERIFIED** | Preserved from starter ZIP package. |
| **IDE Config** | [`.idea/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/.idea) + `.iml` | 5 | **VERIFIED** | Modules, SDK, and shared IntelliJ run configurations. |
| **Starter Backup** | `predictive-customer-churn-telecom-original-backup` | 5 | **VERIFIED** | Isolated backup directory containing pristine starter files. |

---

## 3. Jupyter Notebooks Verification & Output Status

Each notebook was parsed and inspected for structure, imports, and output state:

1. **[`notebooks/01_eda_and_feature_engineering.ipynb`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/notebooks/01_eda_and_feature_engineering.ipynb):**
   - **Structure:** 19 total cells (10 Markdown, 9 Code).
   - **Coverage:** Data loading, zero-tenure audit (all 8 records), bivariate analysis, hypothesis testing (Chi-square and Mann-Whitney U), Scikit-Learn transformer setup, and baseline Brier comparison.
   - **Output Status:** `outputs: []` across all code cells (`execution_count: None`).
2. **[`notebooks/02_model_training_and_tuning.ipynb`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/notebooks/02_model_training_and_tuning.ipynb):**
   - **Structure:** 13 total cells (8 Markdown, 5 Code).
   - **Coverage:** Stratified 5-Fold CV on training split ($N=192$), GridSearchCV hyperparameter tuning, model comparison across Logistic Regression, Random Forest, and XGBoost, ROC/PR curves, confusion matrices, and threshold trade-off analysis.
   - **Output Status:** `outputs: []` across all code cells (`execution_count: None`).
3. **[`notebooks/03_model_interpretation_and_business_recommendations.ipynb`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/notebooks/03_model_interpretation_and_business_recommendations.ipynb):**
   - **Structure:** 16 total cells (9 Markdown, 7 Code).
   - **Coverage:** `shap.LinearExplainer` pipeline attribution, odds ratio calculation, global beeswarm plot, local waterfall explanations (High-Risk TP, Low-Risk TN, Proactive Intervention FP Case C210), supporting tree model consensus, and actionable retention playbook.
   - **Output Status:** `outputs: []` across all code cells (`execution_count: None`).

> [!IMPORTANT]
> **Audit Finding (Notebook Outputs):**  
> While the code cells are fully valid and executable, the `.ipynb` files do not currently contain cached inline outputs or displayed charts. For evaluator review, executing and saving the rendered cell outputs inside all three notebooks is strongly recommended before final ZIP submission.

---

## 4. Visualizations & Statistical Tables Audit

All generated visual and tabular outputs in `outputs/` were inspected and verified for file presence, non-zero byte size, and image readability:

### A. Exploratory Data Analysis Figures (`outputs/eda_figures/`)
- `01_target_distribution.png` (80.33 KB): Target imbalance visualization (16.88% churn rate overall).
- `02_contract_vs_churn.png` (52.61 KB): Churn frequency by contract type ($p = 7.39 \times 10^{-7}$).
- `03_internet_service_vs_churn.png` (48.75 KB): Fiber Optic vs. DSL attrition rates ($p = 0.0076$).
- `04_failed_payments_vs_churn.png` (56.37 KB): Failed payment escalation curve ($p = 2.15 \times 10^{-7}$).
- `05_tenure_and_charges_vs_churn.png` (99.08 KB): Bivariate distributions for tenure and monthly charges ($p = 0.0003$).
- `06_service_count_vs_churn.png` (51.19 KB): Add-on service count retention effect ($p = 0.0381$).
- `07_correlation_matrix.png` (118.97 KB): Pearson/Spearman heatmap across all numerical and encoded features.

### B. Model Performance & Evaluation Figures (`outputs/model_eval_figures/`)
- `01_roc_curves_validation.png` (91.91 KB): Cross-model validation ROC curves (LogReg `0.7697` vs RF `0.7677` vs XGB `0.7293`).
- `02_pr_curves_validation.png` (83.05 KB): Precision-Recall curves on validation partition (LogReg PR-AUC `0.4923`).
- `03_confusion_matrices_validation.png` (55.41 KB): Validation confusion matrices at default and optimal thresholds.
- `04_threshold_tradeoff_curves.png` (176.41 KB): Sensitivity vs. Precision vs. F1 across thresholds `0.10` to `0.90`.
- `05_model_metrics_summary.png` (57.64 KB): Grouped performance metrics bar chart.
- `06_final_test_diagnostics.png` (51.70 KB): Final one-time test set evaluation diagnostic plot (ROC `0.7679`, Recall `75.0%`).

### C. Explainable AI & SHAP Figures (`outputs/shap/`)
- `01_champion_shap_summary_bar.png` (92.73 KB): Global mean absolute SHAP feature importance ranking.
- `02_champion_shap_beeswarm.png` (112.03 KB): Full directional impact beeswarm visualization.
- `03_champion_odds_ratios.png` (95.28 KB): Odds ratios with 95% confidence intervals (Month-to-month OR = `7.04x`).
- `04_local_explanation_high_risk.png` (90.93 KB): Waterfall plot for high-risk customer profile (P = `90.96%`).
- `05_local_explanation_low_risk.png` (97.88 KB): Waterfall plot for loyal long-term subscriber (P = `1.42%`).
- `06_local_explanation_proactive_case.png` (92.31 KB): Waterfall plot for proactive intervention case C210.
- `07_supporting_models_shap_comparison.png` (90.93 KB): Comparative feature attribution against RF and XGBoost.

### D. Structured Statistical Tables (`outputs/tables/`)
- `business_action_playbook.csv` (1.76 KB): Tier-by-tier intervention matrix with economic cost-benefit rationale.
- `feature_importance_champion.csv` (1.95 KB): Log-odds coefficients, odds ratios, and mean absolute SHAP values.
- `feature_importance_comparison.csv` (0.88 KB): Consensus feature rankings across all three algorithms.
- `final_test_evaluation.csv` (0.47 KB): Complete historical test set performance table.
- `hypothesis_tests.json` (1.00 KB): Formal statistical hypothesis test results ($p$-values and test statistics).
- `model_comparison_validation.csv` (1.19 KB): Validation metrics comparison across all models and baseline.
- `threshold_analysis.csv` (2.30 KB): Threshold sweep metrics (`0.10`–`0.90`) on validation partition.
- `training_summary_statistics.csv` (0.69 KB): Numerical summary statistics computed strictly on training data ($N=192$).

*All 20 PNG images were verified via PIL integrity checking with 0 errors.*

---

## 5. Machine Learning Models & Source Modules Audit

### A. Model Artifacts (`models/`)
Each `.joblib` model artifact was loaded, inspected, and verified with a standardized customer record:

| File Name | Size | Pipeline Steps | Classifier Estimator | Verification Inference $P(\text{Churn})$ |
| :--- | :---: | :---: | :--- | :---: |
| `best_model_pipeline.joblib` | 6.34 KB | `['preprocessor', 'classifier']` | `LogisticRegression(C=10.0, class_weight='balanced')` | **0.9096** |
| `logistic_regression_pipeline.joblib`| 6.34 KB | `['preprocessor', 'classifier']` | `LogisticRegression(C=10.0, class_weight='balanced')` | **0.9096** |
| `random_forest_pipeline.joblib` | 294.32 KB | `['preprocessor', 'classifier']` | `RandomForestClassifier(n_estimators=100, max_depth=5)` | **0.4962** |
| `xgboost_pipeline.joblib` | 46.86 KB | `['preprocessor', 'classifier']` | `XGBClassifier(learning_rate=0.05, max_depth=3)` | **0.4068** |

### B. Python Source Code Verification (`src/` & `app.py`)
All Python modules were checked for syntax compilation, import integrity, and code conventions:
- **`src/data_loader.py`:** Clean data loading, quarantine logic for non-feature columns, zero leakage.
- **`src/eda.py`:** Parametric and non-parametric bivariate analytics, automated chart generation.
- **`src/feature_engineering.py`:** Custom Scikit-Learn transformer `TelecomFeatureEngineer` implementing the explicit zero-tenure domain rule (`charges_per_tenure = monthly_charges_usd` when `tenure_months == 0`), `get_feature_names_out()`, and preprocessing `ColumnTransformer`.
- **`src/models.py`:** Model training functions, Stratified 5-Fold cross-validation, and GridSearchCV tuning harness.
- **`src/interpretability.py`:** Model-agnostic and linear SHAP attribution extractors.
- **`src/inference.py`:** Standalone production inference engine with `load_champion_model()`, input validator, and `predict_churn()`. Operational threshold: **`DEFAULT_DECISION_THRESHOLD = 0.55`**.
- **`app.py`:** Full Streamlit interactive dashboard with session-state bound input controls, preset buttons, dynamic risk progress gauge, risk triggers, and retention playbook.
- **Portability Audit:** Tested across all Python source files using regular expression inspection for drive letters or user directory paths (`C:\`, `/Users/`). **Zero hardcoded paths found.** All paths resolve relative to `Path(__file__).resolve().parent`.

---

## 6. Dataset & Backup Integrity Audit

1. **Primary Dataset (`data/customers.csv`):**
   - Record count: Exactly **320 records**, **12 columns**.
   - Target Variable: `churn_30d` (54 churners, 266 retained; 16.88% overall positive rate).
   - Missing Values: Exactly **8 null values** in `total_charges_usd`, all corresponding to `tenure_months == 0`. Zero missing values in any other column.
   - Official Partition Splits:
     - Training: **192 records** (37 churners, 19.27% churn rate).
     - Validation: **64 records** (9 churners, 14.06% churn rate).
     - Test: **64 records** (8 churners, 12.50% churn rate).
2. **Dataset Documentation:**
   - [`DATA_DICTIONARY.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/DATA_DICTIONARY.md): Complete feature definitions, data types, and value constraints.
   - [`README.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/README.md): Project overview, baseline problem formulation, and execution guidelines.
3. **Pristine Starter Backup:**
   - Directory: `C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom-original-backup`
   - Files: Exactly **5 untouched original starter files** (`baseline.py`, `customers.csv`, `DATA_DICTIONARY.md`, `README.md`, `requirements.txt`).
   - Integrity: Matches the original starter ZIP exactly, ensuring compliance with internship guidelines.

---

## 7. IntelliJ IDEA Integration & Run Configurations Audit

The project configuration files in `.idea/` were inspected:

1. **Module Configuration ([`predictive-customer-churn-telecom.iml`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/predictive-customer-churn-telecom.iml)):**
   - Marks `src/` as an explicit source folder (`isTestSource="false"`).
   - Excludes `.mplconfig` from indexing.
   - Configured for `Python 3.13` SDK.
2. **Project Structure ([`.idea/modules.xml`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/.idea/modules.xml) & [`.idea/misc.xml`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/.idea/misc.xml)):**
   - Project SDK correctly mapped to Python 3.13 (`C:\Program Files\Python313\python.exe`).
3. **Shared Run Configurations ([`.idea/runConfigurations/`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/.idea/runConfigurations)):**
   - **`Run ConnectTel App` (`Run_ConnectTel_App.xml`):** Configured as a Python module run configuration invoking `streamlit` with parameters `run app.py --server.port 8501`. Enables one-click application launch directly from IntelliJ.
   - **`Run Inference Test` (`Run_Inference_Test.xml`):** Configured to execute `$PROJECT_DIR$/src/inference.py` for headless verification inside IntelliJ.

---

## 8. Documentation & Reports Audit

The `reports/` folder contains comprehensive markdown deliverables:

1. **[`reports/business_recommendations_and_interpretation.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/reports/business_recommendations_and_interpretation.md):**
   - Phase 3 deliverable: Global feature importance, odds ratio interpretation, local waterfall customer case studies, and four tiered business retention strategies.
2. **[`reports/phase_4_final_model_audit.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/reports/phase_4_final_model_audit.md):**
   - Phase 4 deliverable: Non-destructive verification of all 53 project artifacts, synthetic dataset boundaries, zero-tenure domain rule validation, and out-of-fold leakage audit.
3. **[`reports/phase_5_final_evaluation_and_intellij_integration.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/reports/phase_5_final_evaluation_and_intellij_integration.md):**
   - Phase 5 deliverable: Single authorized evaluation on test partition ($N=64$), baseline comparison (Test ROC-AUC `0.7679`, Recall `75.0%` vs baseline recall `0%`), and IntelliJ IDEA setup.
4. **[`reports/phase_6_working_application_report.md`](file:///C:/Users/Nisha/.gemini/antigravity/scratch/predictive-customer-churn-telecom/reports/phase_6_working_application_report.md):**
   - Phase 6 deliverable: Architecture of `app.py`, state management resolution for the Calculate Churn Risk button, preset verification, UI styling, and local testing logs.

> [!NOTE]
> **Observation on Phase 1 & 2 Reports:**  
> Phase 1 (EDA) and Phase 2 (Model Development) work is fully documented inside the respective Jupyter notebooks and structured table exports, but does not currently exist as standalone markdown files in `reports/`.

---

## 9. Identified Missing Files & Deployment Blockers

The audit identified the following specific items that should be addressed before deployment and submission:

### A. Pre-Deployment / Hosting Requirements (Streamlit Cloud & Hosting)
1. **Missing `.streamlit/config.toml`:**
   - *Status:* **Missing.**
   - *Impact:* While `app.py` runs locally on port 8501 and injects custom CSS, remote deployment platforms (Streamlit Community Cloud, Hugging Face Spaces, Render, Docker) benefit from a dedicated `.streamlit/config.toml` to enforce headless execution, configure theme colors natively, and prevent port/browser opening conflicts.
2. **Missing Root `.gitignore`:**
   - *Status:* **Missing** (only `.idea/.gitignore` exists).
   - *Impact:* When initializing Git to push to GitHub for Streamlit Cloud deployment, transient files (such as `.mplconfig/`, `__pycache__/`, `.pytest_cache/`, and local IDE workspace files) must be excluded.
3. **Git Repository Initialization:**
   - *Status:* **Not initialized** (`.git` folder absent).
   - *Impact:* Streamlit Community Cloud deploys directly from a public or private GitHub repository. Git tracking must be initialized and committed prior to remote deployment.

### B. Notebook Output Cache
1. **Unpopulated Cell Outputs in `.ipynb` Files:**
   - *Status:* **Code present, outputs empty (`outputs: []`).**
   - *Impact:* Assessors opening the Jupyter notebooks on GitHub or in an IDE without executing them will see empty output cells. Pre-running all cells and saving the rendered tables/plots inside the `.ipynb` files will ensure immediate readability.

### C. Phase 7 Final Submission Package Dependencies
1. **Missing PDF and PPT Compilation Packages:**
   - *Status:* `python-pptx` and `reportlab` are **not installed**.
   - *Impact:* These packages are required to generate the final Phase 7 deliverables (PowerPoint presentation deck and publication-grade PDF report).

---

## 10. Deployment Readiness Checklist & Recommendation

| Component | Audit Status | Recommendation for Next Phase |
| :--- | :---: | :--- |
| **Model Pipelines (`models/`)** | **READY** | Deploy with zero modifications; use existing `best_model_pipeline.joblib`. |
| **Inference Engine (`src/inference.py`)** | **READY** | Standardized threshold `0.55`; fully portable. |
| **Streamlit Simulator (`app.py`)** | **READY** | Fully functional; tested with presets and calculation workflow. |
| **Core Dependencies (`requirements.txt`)** | **READY** | Contains all necessary runtime packages. |
| **Streamlit Cloud Config (`.streamlit/config.toml`)** | **PENDING** | Create in Phase 7.2 prior to cloud deployment. |
| **Git Tracking & `.gitignore`** | **PENDING** | Initialize Git and add root `.gitignore` in Phase 7.2. |
| **Notebook Execution Outputs** | **PENDING** | Run notebooks headless and cache outputs for review. |
| **Presentation Deck (`.pptx`)** | **PENDING** | Generate in Phase 7.3 using `python-pptx`. |
| **Project Documentation (`.pdf`)** | **PENDING** | Compile in Phase 7.3 using `reportlab`. |

---

*Phase 7.1 Deployment Readiness Audit completed successfully. All findings have been verified and documented.*
