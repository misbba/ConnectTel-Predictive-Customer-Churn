# ConnectTel Customer Retention Strategy & Explainable AI Report
**Domain:** Telecommunications Customer Churn Prevention  
**Project:** Persevex AI Internship Project  
**Champion Model:** Regularized Logistic Regression (`C=10.0`, `class_weight='balanced'`)  
**Scope Note:** All analyses are derived strictly from the official 320-record synthetic teaching dataset (`customers.csv`).

---

## 1. Executive Summary

ConnectTel faces revenue loss from subscriber churn. Machine learning modeling in Phase 2 demonstrated that **Regularized Logistic Regression** is the champion model, achieving:
- **Validation ROC-AUC:** `0.7697` (substantially outperforming the baseline of `0.6121`).
- **Validation PR-AUC:** `0.4923` (more than double the baseline of `0.2289`).
- **Validation Recall:** `77.78%` (catching 7 out of 9 churners on validation).

Using **SHAP (SHapley Additive exPlanations)** and model odds ratios, we have decoded the "black-box" decision boundary into transparent, actionable business levers.

---

## 2. Top Churn Risk Drivers (Model Interpretability Findings)

| Rank | Feature | Odds Ratio | Mean |SHAP| | Direction | Key Business Interpretation |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | `contract_monthly` | **7.04x** | **0.878** | Risk Factor | Subscribers on Month-to-Month contracts are **7x more likely to churn** than those on 1- or 2-year contracts. Lack of commitment lowers switching friction. |
| **2** | `internet_service_fiber` | **0.18x** | **0.797** | Protective | Fiber connection acts as an anchor of retention in this cohort (13.3% churn vs 27.1% for DSL). |
| **3** | `tenure_months` | **0.44x** | **0.736** | Protective | Customer risk decreases steadily with tenure. The first 12 months represent the critical danger zone. |
| **4** | `failed_payments_90d` | **1.75x** | **0.520** | Risk Factor | Each failed billing transaction escalates churn odds by **75%**. Delinquency is a strong operational signal of churn. |
| **5** | `has_failed_payments` | **2.14x** | **0.356** | Risk Factor | Having any payment failure in the past 90 days more than doubles overall churn risk. |
| **6** | `fiber_high_charge` | **1.58x** | **0.115** | Risk Factor | Fiber accounts paying premium fees (> $70) without value bundling show increased risk. |
| **7** | `security_service` | **0.79x** | **0.116** | Protective | Having an active cybersecurity subscription improves retention stickiness. |

> [!NOTE]
> **Correlation vs. Causation Caution:**  
> These statistical associations indicate which features the model relies upon to rank customer risk. They do not prove that signing a contract directly prevents dissatisfaction. However, they provide high-precision targeting rules for retention operations.

---

## 3. ConnectTel Retention Team Operational Playbook

### Tier 1: Proactive Contract Migration (High Impact)
- **Target Audience:** Month-to-month subscribers with tenure between 6 and 18 months.
- **Action:** Deliver personalized offers migrating users to a 1-Year agreement with a 10-15% monthly discount or complimentary device insurance.
- **Operational Trigger:** When predicted churn probability exceeds **0.50**.

### Tier 2: Smart Billing Recovery Workflow (Urgent Operational Intervention)
- **Target Audience:** Any customer logging their 1st failed payment in 90 days.
- **Action:** Transition from abrasive collections notices to supportive "Card Update Concierge" communications (frictionless mobile link, flexible billing date).
- **Operational Trigger:** Immediate rule-based trigger upon failed ACH or credit card transaction.

### Tier 3: Value-Add Bundling for Premium Accounts
- **Target Audience:** Fiber accounts billed over $70/month.
- **Action:** Attach ConnectTel Security or Streaming services free for 6 months to reinforce perceived value before customers compare competitor rates.

---

## 4. Hypothetical Business Impact & ROI Simulation

*The following calculation is a transparent simulation based explicitly stated assumptions for ConnectTel:*

### Baseline Parameters:
- Total Customer Base: `10,000` subscribers.
- Annual Churn Rate: `16.9%` (~1,690 churners per year, or ~141 per month).
- Average Monthly Revenue Per User (ARPU): `$63.50` (mean monthly charge in dataset).
- Customer Lifetime Horizon: 12 months ($63.50 * 12 = `$762.00` annual revenue per subscriber).
- Model Recall: `77.8%` (identifies ~110 of the 141 monthly churners).
- Retention Campaign Save Rate: `20%` (conservative industry standard for targeted retention offers).
- Cost of Retention Offer: `$50.00` per targeted subscriber.

### Projected Cohort Economics (12-Month LTV Horizon):
1. **Identified High-Risk Churners:** ~110 customers flagged per monthly campaign cycle.
2. **Customers Saved:** 110 * 20% = **22 customers retained per campaign cohort**.
3. **Immediate Monthly Cash Flow Preserved:** 22 saved customers * $63.50 = **$1,397 per month**.
4. **Preserved 12-Month Customer Lifetime Revenue (LTV):** 22 saved customers * $762.00 = **$16,764 total lifetime value**.
5. **Campaign Operational Cost:** (~110 targets + ~35 false positives) * $50 = **$7,250 one-time cohort campaign cost**.
6. **Net Cohort Lifetime ROI:** $16,764 (12-Month LTV) - $7,250 (Campaign Cost) = **+$9,514 net gain per cohort** (~131% Cohort ROI).

---

## 5. Scope Limitations & Methodological Integrity

1. **Synthetic Data Constraint:** The 320 records provided are educational synthetic instances. The financial modeling above demonstrates the analytical methodology and operational workflow, but should not be interpreted as certified real-world financial guidance.
2. **Quarantined Test Set:** True out-of-sample generalization metrics will be confirmed exclusively in the final evaluation stage.
