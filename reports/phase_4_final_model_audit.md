# Phase 4: Final Model Verification & Project Audit Report

**Project:** Predictive Customer Churn Model for a Telecom Company – ConnectTel  
**Domain:** Artificial Intelligence / Customer Retention Machine Learning  
**Workspace:** `C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom`  
**Audit Date:** 2026-11-23  
**Auditor:** Antigravity AI  
**Overall Project Status:** **VERIFIED (Ready for Phase 5 Final Delivery upon Approval)**

---

## 1. Project Structure & Artifact Verification

An exhaustive automated file inventory was conducted across the workspace. All 53 project files are intact, non-empty, and consistent across phases:

| Component / Artifact | Path | Size | Status | Verification Detail |
| :--- | :--- | :---: | :---: | :--- |
| **Primary Dataset** | `data/customers.csv` | 18,781 B | **VERIFIED** | 320 records, 12 columns, pre-split into Train (192), Val (64), Test (64). Untouched. |
| **Original Baseline Backup** | `baseline_original.py` | 1,098 B | **VERIFIED** | Pristine copy of the original 16-line starter baseline script. |
| **Enhanced Baseline Script** | `baseline.py` | 5,247 B | **VERIFIED** | Backward-compatible `ContractGroupBaseline` with Brier Skill Score calculation. |
| **Data Dictionaries & Docs** | `DATA_DICTIONARY.md`, `README.md` | 690 B / 2,539 B | **VERIFIED** | Original project brief guidelines and scope definitions preserved. |
| **Phase 1 EDA Notebook** | `notebooks/01_eda_and_feature_engineering.ipynb` | 14,267 B | **VERIFIED** | 19 cells, complete data audit, statistical hypothesis tests, zero-tenure rationale. |
| **Phase 1 EDA Visualizations** | `outputs/eda_figures/` (7 plots) | ~520 KB total | **VERIFIED** | Figures 01–07: Class balance, contract types, failed payments, numerical distributions. |
| **Phase 2 Modeling Notebook**| `notebooks/02_model_training_and_tuning.ipynb` | 9,088 B | **VERIFIED** | 14 cells, GridSearchCV results, cross-validation, threshold curves, champion selection. |
| **Phase 2 Diagnostic Plots** | `outputs/model_eval_figures/` (5 plots) | ~475 KB total | **VERIFIED** | Figures 01–05: ROC curves, PR curves, confusion matrices, threshold trade-offs, summary. |
| **Serialized Models** | `models/` (4 `.joblib` files) | ~362 KB total | **VERIFIED** | `best_model_pipeline`, `logistic_regression`, `random_forest`, `xgboost`. |
| **Phase 3 SHAP Notebook** | `notebooks/03_model_interpretation_and_business_recommendations.ipynb` | 10,911 B | **VERIFIED** | 16 cells, global SHAP, odds ratios, local waterfall decompositions, playbook. |
| **Phase 3 SHAP Visualizations**| `outputs/shap/` (7 plots) | ~688 KB total | **VERIFIED** | Figures 01–07: Mean |SHAP| bar, beeswarm, odds ratios, 3 waterfalls, cross-model comparison. |
| **Structured Tables** | `outputs/tables/` (7 CSV/JSON files) | ~11 KB total | **VERIFIED** | Hypothesis tests, model validation metrics, threshold grid, feature rankings, playbook. |
| **Executive Business Report** | `reports/business_recommendations_and_interpretation.md` | 5,614 B | **VERIFIED** | Comprehensive narrative report with retention workflows and ROI modeling. |
| **Inference Interface** | `src/inference.py` | 4,500 B | **VERIFIED** | Standalone inference API with error handling, type conversion, and risk tiering. |

---

## 2. Model Loading & Inference Test Results

The saved champion model (`models/best_model_pipeline.joblib`) was loaded into an isolated test harness without retraining. The pipeline consists of:
1. `feature_engineer`: Custom `TelecomFeatureEngineer` transformer.
2. `preprocessor`: Scikit-Learn `ColumnTransformer` (StandardScaler for numerics, OneHotEncoder for categoricals).
3. `classifier`: `LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000, random_state=42)`.

### Test Suite Execution Summary:

```
+------------------------------------------------------------------------------------------------------------------+
| Test Case                 | Input Profile Description           | Output Churn Prob | Prediction | Test Status   |
+------------------------------------------------------------------------------------------------------------------+
| 1. Standard Customer      | Tenure=24m, Annual, Fiber, $75/mo   | 6.18% (Retain=93.8%)| 0 (Retain) | VERIFIED      |
|                           | Total=$1800, 0 failed payments      |                   |            |               |
+------------------------------------------------------------------------------------------------------------------+
| 2. Zero-Tenure Customer   | Tenure=0m, Monthly, DSL, $55/mo     | 54.14% (Risk=Med) | 1 (Churn)  | VERIFIED      |
|    (Missing TotalCharges) | TotalCharges=NaN (unbilled)         |                   |            |               |
+------------------------------------------------------------------------------------------------------------------+
| 3. Unknown Categories     | Contract="unknown_plan",            | 31.60% (Valid)    | 0 (Retain) | VERIFIED      |
|                           | InternetService="satellite"         |                   |            | (No crash)    |
+------------------------------------------------------------------------------------------------------------------+
| 4. Extreme High-Risk      | Tenure=2m, Monthly, DSL, $95/mo     | 97.47% (Critical) | 1 (Churn)  | VERIFIED      |
|                           | 2 Failed Payments in 90d            |                   |            |               |
+------------------------------------------------------------------------------------------------------------------+
| 5. Extreme Low-Risk       | Tenure=48m, Two-Year, Fiber, $45/mo | 1.42% (Low Risk)  | 0 (Retain) | VERIFIED      |
|                           | 0 Failed Payments, Security Add-on  |                   |            |               |
+------------------------------------------------------------------------------------------------------------------+
```

### Key Technical Observations:
- **Feature Consistency:** Inference uses the identical `TelecomFeatureEngineer` transformation logic as training. `total_charges_per_tenure` is safely set to `monthly_charges_usd` for zero-tenure records without division-by-zero errors.
- **Robustness to Unseen Categories:** The one-hot encoder was trained with `handle_unknown='ignore'`, enabling the model to gracefully map unrecognized contract or internet tiers to neutral all-zero dummy vectors without raising exceptions.
- **Risk Ordering:** The pipeline exhibits monotonic risk discrimination ($P_{\text{high}} = 0.9747 \gg P_{\text{low}} = 0.0142$).

---

## 3. Dataset Audit & Methodological Fact-Checking

### A. Synthetic Dataset Scope (Truth in Reporting)
- **Official Primary Data:** The supplied dataset `customers.csv` contains exactly **320 synthetic customer snapshots**.
- **Kaggle Telco Discrepancy:** The initial project brief PDF mentions the standard Kaggle Telco Churn dataset. However, the official Persevex starter `README.md` explicitly overrides this with an educational synthetic substitution:
  > *"Dataset substitution: This pack uses original synthetic teaching data instead of the named external dataset in the project brief. 320 synthetic telecom snapshots with service/contract/charge features... No real Kaggle customer records are bundled."*
- **Audit Conclusion:** The project documentation must continue to clearly state that the 320-record synthetic teaching dataset was utilized. We do not claim to have trained on real Kaggle records.

### B. Test-Set Evaluation History & Quarantining
- **Historical Fact:** The starter `baseline.py` script provided by Persevex automatically evaluated the test set once upon initial unpacking, recording a test Brier score of **`0.095473`**.
- **Discipline Maintained in Phases 1–3:** Throughout Phase 1 (EDA & feature engineering), Phase 2 (cross-validation, grid search, model selection, threshold tuning), and Phase 3 (SHAP analysis), the 64-record test partition was **strictly quarantined and never evaluated or accessed**.
- **Safest Path for Final Evaluation:**
  - One final evaluation of the selected champion model on the test partition ($N=64$) is technically appropriate to establish out-of-sample generalization.
  - **Audit Recommendation:** This single test evaluation should be executed strictly in Phase 5 as an immutable post-hoc validation, comparing test ROC-AUC, PR-AUC, and Brier score against the historical baseline Brier score (`0.095473`).
  - **Status:** **QUARANTINED (Awaiting explicit user authorization before running in Phase 5)**.

---

## 4. Phase 3 SHAP & Business Findings Audit

A rigorous review of the Phase 3 outputs revealed complete internal consistency with one necessary refinement in financial phrasing:

### A. Mathematical Attribution & Rankings
- **Supported by Artifacts:** The reported feature importance rankings in `reports/business_recommendations_and_interpretation.md` exactly match `outputs/tables/feature_importance_champion.csv`:
  1. `contract_monthly`: Coef $+1.9512$, Odds Ratio $7.037\times$, Mean $|SHAP| = 0.8778$ (Rank 1).
  2. `internet_service_fiber`: Coef $-1.7357$, Odds Ratio $0.176\times$, Mean $|SHAP| = 0.7967$ (Rank 2).
  3. `tenure_months`: Coef $-0.8108$, Odds Ratio $0.444\times$, Mean $|SHAP| = 0.7356$ (Rank 3).
  4. `failed_payments_90d`: Coef $+0.5615$, Odds Ratio $1.753\times$, Mean $|SHAP| = 0.5200$ (Rank 4).
  5. `has_failed_payments`: Coef $+0.7585$, Odds Ratio $2.135\times$, Mean $|SHAP| = 0.3558$ (Rank 5).
- **Association vs. Causation:** The report contains clear disclaimers that statistical associations do not prove causation.

### B. Case Study Customer #C210 Audit
- In `customers.csv`, Customer #C210 (row index 209) has `split = validation`, `churn_30d = 0`.
- The champion model predicted a churn probability of **95.13%** (classified as positive at threshold 0.50).
- **Audit Clarification:** Customer #C210 is technically a **False Positive** for the binary 30-day snapshot label. In the business report, this case is correctly positioned as a "Proactive Preventive Intervention Case" (a customer displaying critical warning signs—month-to-month plan + 2 failed payments—who represents an ideal candidate for retention outreach before they churn in days 31–60).

### C. Hypothetical ROI Calculation Time-Horizon Audit
- In the business report simulation, 22 saved customers per month generate $\$16,764$ in annual lifetime revenue ($\$63.50 \times 12 \text{ months} = \$762$ per customer).
- Comparing $\$16,764$ directly against a single month's operational campaign cost of $\$7,250$ conflates a **12-month customer lifetime revenue** with a **1-month campaign cost**.
- **Audit Correction:** The report has been updated to explicitly label this as **Cohort 12-Month LTV ROI**:
  $$\text{Cohort Lifetime Net Gain} = \$16,764 \text{ (12-Month LTV)} - \$7,250 \text{ (Month 1 Campaign Cost)} = +\$9,514 \text{ (131\% Cohort ROI)}$$
  In pure 1-month cash flow terms, saving 22 customers in Month 1 preserves $22 \times \$63.50 = \$1,397$ in immediate monthly billing. The full $\$16,764$ benefit accrues over the entire 12-month contracted horizon.

---

## 5. Technical Readiness for Application Integration

The project is fully prepared for frontend integration into an IntelliJ IDEA Python project, Streamlit dashboard, or API backend:

| Integration Requirement | Technical Specification | Readiness Status |
| :--- | :--- | :--- |
| **Model Loader** | `from inference import load_champion_model; model = load_champion_model()` | **READY** |
| **Prediction Function** | `from inference import predict_churn; result = predict_churn(customer_dict)` | **READY** |
| **Input Schema** | 8 standard customer features (`tenure_months`, `contract`, `internet_service`, `monthly_charges_usd`, `total_charges_usd`, `security_service`, `streaming_service`, `failed_payments_90d`) | **READY** |
| **Zero-Tenure Handling** | Automatic safe assignment of `charges_per_tenure = monthly_charges_usd` and imputation of missing `total_charges_usd` to 0.0 | **READY** |
| **Custom Transformer Path** | Handled transparently by `src/inference.py` ensuring `TelecomFeatureEngineer` is in namespace during unpickling | **READY** |
| **Runtime Dependencies** | Standard libraries only (`python >= 3.10`, `scikit-learn`, `pandas`, `numpy`, `joblib`) | **READY** |

---

## 6. Action Items & Next Steps for Final Delivery

The audit confirms that the model, data pipelines, visual artifacts, and report documentation are technically sound and fully verified.

### Next Steps Requiring User Authorization:
1. **Authorize Final Test Set Evaluation:** Execute a single, un-tuned evaluation of the champion model on the quarantined 64-record test set, comparing final ROC-AUC, PR-AUC, F1, and Brier score against the historical baseline (`0.095473`).
2. **Authorize Application Development:** Build the interactive demonstration web application (Streamlit) using `src/inference.py`.
3. **Authorize Documentation & Presentation Generation:** Compile the final comprehensive project report in PDF format and generate the presentation slide deck in PowerPoint format (`.pptx`).
