# PHASE 7.3.1 – FINAL PPT AND PDF DOCUMENT ACCURACY AUDIT

**Project:** Predictive Customer Churn Model for a Telecom Company – ConnectTel  
**Internship Program:** Persevex AI Internship  
**Primary IDE:** JetBrains IntelliJ IDEA Ultimate 2024.3  
**Execution Environment:** Python 3.13.5 (64-bit)  
**Workspace:** `C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom`  
**Audit Date:** November 25, 2026  
**Audited Artifacts:**
1. `deliverables/ConnectTel_Executive_Presentation.pptx` (16 Slides, 1,330,859 bytes)
2. `deliverables/ConnectTel_Technical_Project_Report.pdf` (13 Pages, 1,209,372 bytes)
3. `reports/phase_7_3_submission_documentation_report.md` (18,075 bytes)

---

## 1. Executive Summary & Audit Mandate

In strict adherence to Persevex AI Internship standards for academic integrity and production engineering rigor, Phase 7.3.1 conducted a comprehensive, line-by-line factual and numerical verification of the generated executive presentation and technical project report. Every claim, parameter, metric, odds ratio, customer identifier, financial figure, and screenshot was audited against primary ground truth sources:
- Serialized Scikit-Learn pipelines (`models/best_model_pipeline.joblib`, `xgboost_pipeline.joblib`, `random_forest_pipeline.joblib`).
- Official executed notebooks (`notebooks/01_eda_and_feature_engineering.ipynb`, `02_model_training_and_tuning.ipynb`, `03_model_interpretation_and_business_recommendations.ipynb`).
- Pre-computed ground truth tables (`outputs/tables/model_comparison_validation.csv`, `feature_importance_champion.csv`, `threshold_analysis.csv`).
- Historical Phase 1–6 reports, specifically `reports/business_recommendations_and_interpretation.md` and `reports/phase_5_final_evaluation_and_intellij_integration.md`.

### Summary of Audit Verdict
The audit verified that the primary project narrative, dataset partitions (192 train / 64 val / 64 test), test evaluation metrics (0.7679 ROC-AUC, 75.0% recall, 6/8 detected), and live application screenshots are **100% genuine and methodologically sound**.

However, the audit identified **seven critical discrepancies** across candidate hyperparameters, validation benchmark tables, odds ratio feature attributions, financial claims, calibration terminology, and local SHAP case probabilities that require precise corrections before final submission.

---

## 2. Item-by-Item Verification Findings (Specific Discrepancy Audit)

### Discrepancy 1: XGBoost Hyperparameters
* **Audited Locations:**
  * Presentation: Slide 6 (`MODEL ARCHITECTURE`)
  * PDF Report: Section 6 / Page 5 (Table 3: `Model Specifications & Hyperparameters`)
* **Current Claim in Documents:**
  * Slide 6: *"Optimized Params: n_estimators=100, max_depth=3, lr=0.05"*.
  * PDF Table 3: *"n_estimators = 100, max_depth = 3, lr = 0.05, colsample_bytree = 0.8, scale_pos_weight = 4.19"*.
* **Verified Ground Truth Source:**
  * `models/xgboost_pipeline.joblib` (Classifier Parameters)
  * `outputs/tables/model_comparison_validation.csv` (Row 3: XGBoost)
  * Notebook 2 (`notebooks/02_model_training_and_tuning.ipynb` Cell 6)
  * Actual verified hyperparameters:
    * `n_estimators`: **30** (NOT 100)
    * `max_depth`: **3**
    * `learning_rate`: **0.15** (NOT 0.05)
    * `colsample_bytree`: **0.8**
    * `scale_pos_weight`: **4.189189** (~4.19)
    * `subsample`: **1.0**
* **Nature of Error:** Severe parameter discrepancy. The number of trees is overstated by >3x (100 vs. 30), and the learning rate is understated by 3x (0.05 vs. 0.15).
* **Recommended Correction:**
  * **PPTX Slide 6:** Change `n_estimators=100, max_depth=3, lr=0.05` to `n_estimators=30, max_depth=3, lr=0.15, colsample_bytree=0.8, scale_pos_weight=4.19`.
  * **PDF Table 3:** Update `Selected Parameters` column to `n_estimators = 30, max_depth = 3, lr = 0.15, colsample_bytree = 0.8, scale_pos_weight = 4.19`.

---

### Discrepancy 2: Random Forest and XGBoost Validation Metrics (PR-AUC, ROC-AUC, Brier)
* **Audited Locations:**
  * Presentation: Slide 7 (`MODEL EVALUATION`)
  * PDF Report: Section 7 / Page 6 (Table 4: `Validation Performance Comparison`)
  * Phase 7.3 Report: `reports/phase_7_3_submission_documentation_report.md` Sections 4 & 5
* **Current Claim in Documents:**
  * Slide 7:
    * Baseline: ROC-AUC = 0.6556 | PR-AUC = 0.2312 | Brier = 0.119048
    * Champion: Brier Score = 0.170669
    * Random Forest: ROC-AUC = 0.7677 | PR-AUC = 0.4497 | Recall = 44.44% | Brier = 0.117769
    * XGBoost: ROC = 0.7293 | PR = 0.3621 | Recall = 33.33% | Brier = 0.128452
  * PDF Table 4:
    * Baseline: ROC = 0.6556, PR = 0.2312, Recall = 0.0%, Prec = 0.0%, F1 = 0.0000, Brier = 0.119048
    * Random Forest: ROC = 0.7677, PR = 0.4497, Recall = 44.4%, Prec = 33.3%, F1 = 0.3810, Brier = 0.117769
    * XGBoost: ROC = 0.7293, PR = 0.3621, Recall = 33.3%, Prec = 27.3%, F1 = 0.3000, Brier = 0.128452
  * Phase 7.3 Report claimed: RF PR-AUC = 0.3800, XGB PR-AUC = 0.3831.
* **Verified Ground Truth Source:**
  * `outputs/tables/model_comparison_validation.csv`
  * Notebook 2 (`notebooks/02_model_training_and_tuning.ipynb` Cell 6)
  * Exact verified validation metrics (evaluated at default 0.50 cutoff on 64 validation records):

| Model | CV Mean ROC-AUC | Val ROC-AUC | Val PR-AUC | Val Recall (0.5) | Val Precision (0.5) | Val F1 (0.5) | Val Brier Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline (Contract Prior)** | — | **0.6121** | **0.2289** | **0.00%** | **0.00%** | **0.0000** | **0.119013** |
| **Logistic Regression (Champ)**| **0.7141** | **0.7697** | **0.4923** | **77.78% (7/9)** | **31.82%** | **0.4516** | **0.204877** |
| **Random Forest** | **0.6570** | **0.7576** | **0.3191** | **66.67% (6/9)** | **28.57%** | **0.4000** | **0.173479** |
| **XGBoost** | **0.7001** | **0.7020** | **0.3413** | **55.56% (5/9)** | **25.00%** | **0.3448** | **0.175568** |

* **Nature of Error:** Multiple desynchronized numbers. In the presentation and PDF, RF PR-AUC was inflated to 0.4497 (and in Phase 7.3 report to 0.3800) when ground truth is **0.3191**. XGBoost PR-AUC was reported as 0.3621 (and 0.3831) when ground truth is **0.3413**. Random Forest recall at 0.5 was understated as 44.4% (actual is 66.67%), and XGBoost recall was understated as 33.3% (actual is 55.56%). Champion Brier score was reported as 0.170669 instead of **0.204877**.
* **Recommended Correction:**
  * Replace the entire validation comparison table in PPT Slide 7 and PDF Table 4 with the exact ground truth values from `model_comparison_validation.csv` displayed above.

---

### Discrepancy 3: Fiber Optic Odds Ratio and Direction
* **Audited Locations:**
  * Presentation: Slide 10 (`Top Feature Attribution Insights`), Slide 12 (`Tier 4: Premium Bundling`)
  * PDF Report: Section 10 / Page 7 (Table 7: `Champion Model Feature Importance`), Section 11 / Page 8 (Table 8: `Tier 4 Playbook`)
  * Phase 7.3 Report: `reports/phase_7_3_submission_documentation_report.md` Sections 4 & 5
* **Current Claim in Documents:**
  * Slide 10: *"Fiber optic internet (OR = 1.56x)"* claimed as an elevated risk factor.
  * Slide 12: *"Fiber Optic > $70/mo without add-on (OR = 1.56x)"*.
  * PDF Table 7: `internet_service_fiber`: `Raw Coef = +0.4444`, `Odds Ratio = 1.559x`, `Direction = Increases Churn`.
  * PDF Table 8: `Fiber tier without add-ons (OR = 1.56x, Churn = 26.2%)`.
  * Phase 7.3 Report: *"Fiber optic internet (1.56x)"*.
* **Verified Ground Truth Source:**
  * `models/best_model_pipeline.joblib` (Serialized Preprocessor & LogisticRegression weights)
  * `outputs/tables/feature_importance_champion.csv`
  * `reports/business_recommendations_and_interpretation.md` (Phase 3 Report, Section 2)
  * Exact verified feature coefficients and odds ratios:

| Feature Name | Transform Type | Coefficient ($\beta$) | Odds Ratio | Direction | Domain Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`cat__internet_service_fiber`** | OneHotEncoder | **-1.7357** | **0.1763 (0.18x)** | **Protective (Decreases Churn)** | Standalone fiber subscription acts as a loyalty anchor (13.3% churn vs 27.1% for DSL). |
| **`remainder__fiber_high_charge`**| Domain Interaction| **+0.4564** | **1.5783 (1.58x)** | **Risk Factor (Increases Churn)** | High monthly charges (> $70) among fiber customers drive price sensitivity and churn. |

* **Nature of Error:** Severe statistical inversion and feature conflation. Standalone fiber service (`internet_service_fiber`) has a negative coefficient (**-1.7357**) and an odds ratio of **0.1763 (0.18x)**, meaning it significantly *decreases* churn odds. The positive odds ratio of ~1.58x belongs exclusively to the interaction feature `fiber_high_charge`. Claiming that `internet_service_fiber` has `coef = +0.4444` and `OR = 1.559x` directly contradicts the champion model.
* **Recommended Correction:**
  * In PDF Table 7: Correct `internet_service_fiber` to `Raw Coef = -1.7357`, `Odds Ratio = 0.176x`, `Direction = Decreases Churn (Protective)`. Add `fiber_high_charge` as a separate row: `Raw Coef = +0.4564`, `Odds Ratio = 1.578x`, `Direction = Increases Churn`.
  * In PPT Slide 10 & 12, and PDF Table 8: Explicitly attribute the 1.58x odds ratio to `fiber_high_charge` (Fiber customers paying >$70/mo without bundled security), while citing standalone fiber as a protective retention anchor (0.18x).

---

### Discrepancy 4: Projected Net Retention Value of $18,480 per 1,000 Subscribers
* **Audited Locations:**
  * Phase 7.3 Report: `reports/phase_7_3_submission_documentation_report.md` Section 4 & 5
* **Current Claim in Documents:**
  * *"Financial ROI: Projected net annual retention savings of $18,480 per 1,000 subscriber base."*
* **Verified Ground Truth Source:**
  * Comprehensive repository grep across all files (`.py`, `.ipynb`, `.md`, `.json`, `.csv`).
  * `outputs/tables/business_action_playbook.csv`
  * `reports/business_recommendations_and_interpretation.md` (Phase 3 Report, Section 4)
* **Nature of Error:** Fabricated / Unsupported Metric. The figure "$18,480" does not exist in any notebook, script, or model artifact. In `reports/business_recommendations_and_interpretation.md` Section 4, the only documented simulation is a **hypothetical illustrative model on a 10,000 subscriber base**:
  * 10,000 subscribers with 16.9% base churn rate = 1,690 churners/year.
  * Targeted top decile (1,000 subscribers) containing 145 expected churners.
  * 15% intervention save rate = 22 preserved subscribers.
  * 12-Month LTV saved = 22 * $762 = $16,764.
  * Campaign intervention cost = 1,000 * $7.25 = $7,250.
  * Net Cohort ROI = **+$9,514 net gain per cohort** (~131% ROI).
* **Recommended Correction:**
  * Completely excise "$18,480 per 1,000 subscribers" from all documentation.
  * Replace with the Phase 3 approved simulation of **+$9,514 net gain per 10,000-subscriber cohort**, and explicitly label it as a *"Hypothetical Illustrative Business Simulation (Not empirical ConnectTel accounting data)"*.

---

### Discrepancy 5: Customer Acquisition Cost (CAC) of $300–$450
* **Audited Locations:**
  * Presentation: Slide 2 (`The Telecom Churn Imperative`)
  * PDF Report: Section 1 / Page 1 & Section 2 / Page 2
  * Phase 7.3 Report: `reports/phase_7_3_submission_documentation_report.md` Section 4
* **Current Claim in Documents:**
  * Phase 7.3 Report: *"customer acquisition costs ($300–$450)"*.
  * PPT Slide 2 & PDF Page 2: *"costs 5x to 7x more than preserving an existing account"*.
* **Verified Ground Truth Source:**
  * Persevex AI Project Guidelines and dataset documentation.
* **Nature of Error:** Contextual misattribution. Neither the 320-record synthetic teaching dataset nor the internship guidelines contain measured financial accounting or CAC records for ConnectTel. The "$300–$450" figure is a recognized external telecommunications industry benchmark for postpaid broadband/wireless, but must not be represented as an internal ConnectTel metric.
* **Recommended Correction:**
  * In all documents, explicitly qualify: *"According to general telecommunications industry benchmarks, subscriber acquisition typically costs 5x to 7x more than retention ($300–$450 in external industry literature), establishing the economic rationale for churn prevention."*

---

### Discrepancy 6: Operational Threshold (0.55) Calibration Wording
* **Audited Locations:**
  * Presentation: Slide 2, Slide 8, Slide 13
  * PDF Report: Cover/Metadata, Section 1 / Page 1, Section 8 / Page 6
* **Current Claim in Documents:**
  * PPT Slide 2: *"through disciplined operational cutoff calibration"*
  * PPT Slide 13: *"Visual gauge calibrated to threshold 0.55 cutoff."*
  * PDF Cover/Metadata: *"Operational Decision Threshold: 0.55 (Calibrated on Validation Partition for Peak F1 = 0.4667)"*
  * PDF Line 289: *"threshold-calibrated decisioning"*
  * PDF Line 328: *"decision threshold calibration at 0.55"*
* **Verified Ground Truth Source:**
  * User instruction from Phase 6: *"1. Replace 'Calibrated Operational Decision Cutoff' with 'Operational Decision Threshold'."*
  * Scikit-Learn pipeline and Brier score documentation.
* **Nature of Error:** Terminology ambiguity. The model produces uncalibrated discriminative ranking scores (Brier score 0.209454 vs baseline 0.095473 due to `class_weight='balanced'`). Describing the decision threshold as "calibrated" conflates decision-rule threshold tuning (maximizing F1) with probability calibration (Platt scaling / isotonic regression).
* **Recommended Correction:**
  * Replace all occurrences of "calibrated threshold" or "threshold calibration" with **"Operational Decision Threshold (Tuned for Peak F1 = 0.4667)"** or **"Decision Threshold Optimization"**.
  * Update PPT Slide 13 to: *"Visual gauge configured to operational decision threshold 0.55."*

---

### Discrepancy 7: Local SHAP Customer Case Identifiers and Probabilities
* **Audited Locations:**
  * Presentation: Slide 11 (`Local Customer Diagnostics: SHAP Waterfall Case Studies`)
  * PDF Report: Section 10 / Page 8 (Local Case Studies)
  * Phase 7.3 Report: `reports/phase_7_3_submission_documentation_report.md` Sections 4 & 5
* **Current Claim in Documents:**
  * PPT Slide 11:
    * Customer #C225: *"P = 90.96%"*
    * Customer #C193: *"P = 1.42%"*
  * PDF Section 10:
    * Customer #C225: *"Prob = 90.96%"*
    * Customer #C193: *"Prob = 1.42%"*
    * Customer #C210: *"Prob = 59.3%"*
  * Phase 7.3 Report claimed: *"Customer #38 (88.3% risk)"*.
* **Verified Ground Truth Source:**
  * Notebook 3 (`notebooks/03_model_interpretation_and_business_recommendations.ipynb` Cell 10)
  * Saved waterfall plots in `outputs/shap/`:
    * `04_local_explanation_high_risk.png`: **Customer #C225, Prob = 85.8%**
    * `05_local_explanation_low_risk.png`: **Customer #C193, Prob = 8.7%**
    * `06_local_explanation_proactive_case.png`: **Customer #C210, Prob = 95.1%**
* **Nature of Error:** Numerical desynchronization and customer ID hallucination. The author of the presentation and PDF scripts copied the Streamlit UI preset risk scores (High-Risk Delinquent preset = 91.0% / 90.96%, Loyal Subscriber preset = 1.4% / 1.42%) and mistakenly applied them to Notebook 3 customers #C225 and #C193. Additionally, "Customer #38" in the Phase 7.3 report was completely fabricated.
* **Recommended Correction:**
  * In PPT Slide 11: Update Customer #C225 to **Prob = 85.8%** and Customer #C193 to **Prob = 8.7%** (matching the embedded waterfall plots).
  * In PDF Section 10: Update Customer #C225 to **Prob = 85.8%**, Customer #C193 to **Prob = 8.7%**, and Customer #C210 to **Prob = 95.1%**.
  * Remove all references to "Customer #38".

---

### Discrepancy 8: Validation Threshold 0.50 False Positive Confusion Matrix
* **Audited Locations:**
  * Presentation: Slide 8 (`MODEL DECISIONING`)
  * PDF Report: Section 8 / Page 6 (Operational Threshold Tuning)
* **Current Claim in Documents:**
  * Slide 8 & PDF Section 8: *"At 0.50 cutoff, the model caught 77.8% of churners but triggered 17 false alarms (Precision = 29.17%, F1 = 0.4516). Adjusting the decision threshold to 0.55 eliminated 3 false alarms..."*
* **Verified Ground Truth Source:**
  * `outputs/tables/threshold_analysis.csv` (Logistic Regression Rows for 0.45, 0.50, 0.55):
    * Threshold 0.45: TP = 7, **FP = 17**, FN = 2, TN = 38, Precision = 0.2917, Recall = 0.7778, F1 = 0.4242
    * Threshold 0.50: TP = 7, **FP = 15**, FN = 2, TN = 40, Precision = 0.3182, Recall = 0.7778, F1 = 0.4516
    * Threshold 0.55: TP = 7, **FP = 14**, FN = 2, TN = 41, Precision = 0.3333, Recall = 0.7778, F1 = 0.4667
* **Nature of Error:** Conflation of threshold 0.45 with threshold 0.50. At 0.50, the model produced 15 false alarms (precision 31.82%). The 17 false alarms occurred at threshold 0.45. Raising the threshold from 0.50 to 0.55 eliminated **1 false alarm** (from 15 down to 14), not 3.
* **Recommended Correction:**
  * Correct the narrative in Slide 8 and PDF Section 8: *"At the default 0.50 cutoff, the model caught 77.78% of churners with 15 false alarms (Precision = 31.82%, F1 = 0.4516). Increasing the threshold to 0.55 eliminated an additional false alarm (reducing FP from 15 to 14, increasing precision to 33.33%), achieving the peak validation F1-score of 0.4667 without losing sensitivity."*

---

## 3. Comprehensive Verification Matrix for Metrics & Splits

| Metric Category | Specific Parameter | Status in Documents | Verified Source Ground Truth | Audit Result |
| :--- | :--- | :--- | :--- | :--- |
| **Dataset Splits** | Total Dataset Rows | 320 Records | `customers.csv` (320 rows) | **PASS / VERIFIED** |
| | Training Split | 192 Records (60.0%, 37 Churners) | `customers.csv` (192 rows, 19.27% churn) | **PASS / VERIFIED** |
| | Validation Split | 64 Records (20.0%, 9 Churners) | `customers.csv` (64 rows, 14.06% churn) | **PASS / VERIFIED** |
| | Test Split | 64 Records (20.0%, 8 Churners) | `customers.csv` (64 rows, 12.50% churn) | **PASS / VERIFIED** |
| **Validation Benchmark** | Logistic Regression ROC | 0.7697 | `model_comparison_validation.csv` (0.7697) | **PASS / VERIFIED** |
| | Logistic Regression PR | 0.4923 | `model_comparison_validation.csv` (0.4923) | **PASS / VERIFIED** |
| | Baseline ROC-AUC | Claimed 0.6556 | `model_comparison_validation.csv` (**0.6121**) | **FAIL (Fix to 0.6121)** |
| | Baseline PR-AUC | Claimed 0.2312 | `model_comparison_validation.csv` (**0.2289**) | **FAIL (Fix to 0.2289)** |
| | Random Forest ROC | Claimed 0.7677 | `model_comparison_validation.csv` (**0.7576**) | **FAIL (Fix to 0.7576)** |
| | Random Forest PR-AUC | Claimed 0.4497 / 0.3800 | `model_comparison_validation.csv` (**0.3191**) | **FAIL (Fix to 0.3191)** |
| | Random Forest Recall (0.5)| Claimed 44.44% | `model_comparison_validation.csv` (**66.67%**) | **FAIL (Fix to 66.67%)** |
| | XGBoost ROC-AUC | Claimed 0.7293 | `model_comparison_validation.csv` (**0.7020**) | **FAIL (Fix to 0.7020)** |
| | XGBoost PR-AUC | Claimed 0.3621 / 0.3831 | `model_comparison_validation.csv` (**0.3413**) | **FAIL (Fix to 0.3413)** |
| | XGBoost Recall (0.5) | Claimed 33.33% | `model_comparison_validation.csv` (**55.56%**) | **FAIL (Fix to 55.56%)** |
| **Test Evaluation** | Test ROC-AUC | 0.7679 | Phase 5 Audit Report (0.7679) | **PASS / VERIFIED** |
| | Test PR-AUC | 0.4708 | Phase 5 Audit Report (0.4708) | **PASS / VERIFIED** |
| | Test Recall (0.55 Cutoff)| 75.00% (6 of 8 caught) | Phase 5 Audit Report (6/8 detected) | **PASS / VERIFIED** |
| | Test Precision | 25.00% (6 of 24 flagged) | Phase 5 Audit Report (25.00%) | **PASS / VERIFIED** |
| | Test F1-Score | 0.3750 | Phase 5 Audit Report (0.3750) | **PASS / VERIFIED** |
| | Test Brier Score (Champ)| 0.209454 | Phase 5 Audit Report (0.209454) | **PASS / VERIFIED** |
| | Test Brier Score (Base) | 0.095473 | Phase 5 Audit Report (0.095473) | **PASS / VERIFIED** |
| | Test Confusion Matrix | TP=6, FP=18, FN=2, TN=38 | Phase 5 Audit Report (`TP=6, FP=18, FN=2, TN=38`)| **PASS / VERIFIED** |

---

## 4. Application Screenshot Authentication Audit

* **Screenshot 1:** `outputs/app_screenshots/01_connecttel_app_overview.png` (213,235 bytes, 1422×948 PNG)
  * Visual Element: ConnectTel Churn Risk Simulator with High-Risk Delinquent profile loaded.
  * Model Output: Model-Estimated Risk Score = **91.0%**, Verdict = **PROACTIVE INTERVENTION REQUIRED: HIGH CHURN RISK** (Electric Orange banner), Active Risk Triggers = 4.
  * Capture Method: Captured directly via Chrome DevTools Protocol (CDP) WebSocket connection to live Streamlit instance (`http://localhost:8504`).
  * Authentication: **AUTHENTIC & VERIFIED (Zero Mock Data)**.
* **Screenshot 2:** `outputs/app_screenshots/02_connecttel_app_loyal_profile.png` (230,121 bytes, 1422×948 PNG)
  * Visual Element: ConnectTel Churn Risk Simulator with Loyal Subscriber profile loaded.
  * Model Output: Model-Estimated Risk Score = **1.4%**, Verdict = **RETAINED SUBSCRIBER: LOW CHURN RISK** (Emerald Green banner), Active Risk Triggers = 0.
  * Capture Method: Captured directly via Chrome DevTools Protocol (CDP) WebSocket connection to live Streamlit instance (`http://localhost:8504`).
  * Authentication: **AUTHENTIC & VERIFIED (Zero Mock Data)**.

---

## 5. Master Remediation Plan (Pending User Authorization)

In compliance with strict rules, **no files have been modified yet**. The following exact code and text updates are ready to be applied across `scripts/build_presentation.py` and `scripts/build_pdf_report.py` upon user approval:

1. **XGBoost Hyperparameters:** Correct `n_estimators=30, max_depth=3, learning_rate=0.15` across Slide 6 and PDF Table 3.
2. **Validation Table Synchronization:** Update Slide 7 and PDF Table 4 to reflect exact CSV values (RF PR-AUC: 0.3191, XGB PR-AUC: 0.3413, Baseline ROC: 0.6121, etc.).
3. **Fiber Optic Distinction:** Correct PDF Table 7 and Slide 10 to document `cat__internet_service_fiber` as protective (0.18x, $\beta=-1.7357$) and `remainder__fiber_high_charge` as the high-charge risk driver (1.58x, $\beta=+0.4564$).
4. **Excise $18,480:** Remove the unsupported "$18,480 per 1,000 subscribers" claim from all reports; replace with the Phase 3 hypothetical simulation of +$9,514 per 10,000 subscribers (explicitly labeled illustrative).
5. **CAC Clarification:** Qualify the $300–$450 figure as an external telecommunications industry benchmark rather than ConnectTel internal accounting data.
6. **Calibration Terminology:** Replace "calibrated threshold" with "operational decision threshold (tuned for peak F1 = 0.4667)".
7. **Local SHAP Probabilities:** Correct Slide 11 and PDF Section 10 to match notebook waterfall plots: Customer #C225 (85.8%), Customer #C193 (8.7%), Customer #C210 (95.1%).
8. **Threshold 0.50 FP Count:** Correct Slide 8 and PDF Section 8 to state that threshold 0.50 had 15 false alarms (not 17), and threshold 0.55 eliminated 1 false alarm to reach peak F1.

---

```
======================================================================
PHASE 7.3.1 AUDIT COMPLETE: 8 DISCREPANCIES IDENTIFIED FOR CORRECTION
======================================================================
```
