"""
Script to generate notebooks/03_model_interpretation_and_business_recommendations.ipynb
ConnectTel / Persevex AI Internship Project.
"""

import json
from pathlib import Path

NOTEBOOK_PATH = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\notebooks\03_model_interpretation_and_business_recommendations.ipynb")

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Predictive Customer Churn Model for ConnectTel\n",
            "## Phase 3: Model Interpretation (SHAP / Explainable AI) & Business Retention Recommendations\n",
            "\n",
            "**Author:** Persevex AI Intern  \n",
            "**Domain:** Artificial Intelligence / Customer Retention Machine Learning  \n",
            "**Champion Model:** Regularized Logistic Regression (`C=10.0`, `class_weight='balanced'`)  \n",
            "**Partitions Analyzed:** Training Set ($N=192$, Background Reference), Validation Set ($N=64$, Explanation Cohort)  \n",
            "**Test Set ($N=64$):** Strictly locked and quarantined for final evaluation only.  \n",
            "\n",
            "---"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. Phase 3 Objectives\n",
            "\n",
            "A high-performing model is useless in a customer retention setting if the retention team cannot explain **why** an individual is flagged for churn.\n",
            "\n",
            "In this phase, we apply **SHAP (SHapley Additive exPlanations)** grounded in cooperative game theory to unpack our champion Logistic Regression pipeline:\n",
            "1. **Global Explainability:** Quantify the global importance and directional impact of each feature across the customer base.\n",
            "2. **Odds Ratio Quantification:** Compute odds ratios with exact multiplicative risk interpretations.\n",
            "3. **Local Customer Case Studies:** Generate granular waterfall plots for individual customer accounts (True Positive, True Negative, Proactive Risk Candidate).\n",
            "4. **Cross-Model Consensus:** Compare SHAP feature rankings with Random Forest and XGBoost `TreeExplainer`.\n",
            "5. **Operational Retention Playbook:** Translate statistical risk drivers into targeted, high-ROI business interventions for ConnectTel's retention team."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Environment & Module Setup\n",
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
            "import shap\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "from data_loader import load_raw_data, get_splits\n",
            "from interpretability import clean_feature_names\n",
            "\n",
            "print('Phase 3 modules and libraries loaded successfully.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2. Loading Champion Pipeline & Data Partitions\n",
            "\n",
            "We load the champion model pipeline (`models/best_model_pipeline.joblib`) fitted in Phase 2.\n",
            "The training partition serves as the background dataset ($N=192$), and the validation partition ($N=64$) serves as the explanation cohort."
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
            "best_pipe = joblib.load(PROJECT_ROOT / 'models' / 'best_model_pipeline.joblib')\n",
            "prep = best_pipe.named_steps['preprocessor']\n",
            "clf = best_pipe.named_steps['classifier']\n",
            "\n",
            "X_tr_trans = prep.transform(X_train)\n",
            "X_val_trans = prep.transform(X_val)\n",
            "feature_names = clean_feature_names(list(prep.get_feature_names_out()))\n",
            "\n",
            "print(f'Transformed Features ({len(feature_names)}): {feature_names}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3. Global Feature Importance & Odds Ratios\n",
            "\n",
            "We inspect the exact Logistic Regression coefficients, Odds Ratios ($\\text{OR} = \\exp(\\beta)$), and Mean Absolute SHAP values."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "importance_df = pd.read_csv(PROJECT_ROOT / 'outputs' / 'tables' / 'feature_importance_champion.csv')\n",
            "importance_df[['Feature', 'Coefficient', 'Odds_Ratio', 'Mean_Abs_SHAP', 'Effect_Direction']]"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "#### Global Feature Interpretation:\n",
            "1. **`contract_monthly` (Odds Ratio = 7.04x):** Month-to-month contracts multiply the odds of churn by over **$7\\times$** compared to long-term commitments. Subscribers have zero contractual friction to leave when encountering billing or competitor promotions.\n",
            "2. **`internet_service_fiber` (Odds Ratio = 0.18x):** In this cohort, Fiber Optic connection serves as a strong retention anchor (churn rate: 13.3% vs 27.1% for DSL).\n",
            "3. **`tenure_months` (Odds Ratio = 0.44x):** Longer tenure strongly reduces churn risk. The early onboarding window represents the peak vulnerability zone.\n",
            "4. **`failed_payments_90d` (Odds Ratio = 1.75x):** Each failed payment in the prior 90 days escalates churn odds by **75%**.\n",
            "5. **`has_failed_payments` (Odds Ratio = 2.14x):** Any history of payment failure more than doubles churn risk."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Display Global SHAP Plots\n",
            "from IPython.display import Image, display\n",
            "\n",
            "global_figs = [\n",
            "    ('Figure 1: Champion Model Global SHAP Feature Importance', PROJECT_ROOT / 'outputs' / 'shap' / '01_champion_shap_summary_bar.png'),\n",
            "    ('Figure 2: SHAP Beeswarm Distribution Plot', PROJECT_ROOT / 'outputs' / 'shap' / '02_champion_shap_beeswarm.png'),\n",
            "    ('Figure 3: Logistic Regression Odds Ratios', PROJECT_ROOT / 'outputs' / 'shap' / '03_champion_odds_ratios.png')\n",
            "]\n",
            "\n",
            "for title, p in global_figs:\n",
            "    if p.exists():\n",
            "        print(f'=== {title} ===')\n",
            "        display(Image(filename=str(p)))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 4. Local Customer Case Studies (Waterfall Explanations)\n",
            "\n",
            "We examine individual customer predictions to understand how individual attributes combine to push probability up or down."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "local_figs = [\n",
            "    ('Figure 4: High-Risk Churner (Customer #C225, Prob=85.8%)', PROJECT_ROOT / 'outputs' / 'shap' / '04_local_explanation_high_risk.png'),\n",
            "    ('Figure 5: Low-Risk Loyal Customer (Customer #C193, Prob=8.7%)', PROJECT_ROOT / 'outputs' / 'shap' / '05_local_explanation_low_risk.png'),\n",
            "    ('Figure 6: High-Risk Preventive Intervention Case (Customer #C210, Prob=95.1%)', PROJECT_ROOT / 'outputs' / 'shap' / '06_local_explanation_proactive_case.png')\n",
            "]\n",
            "\n",
            "for title, p in local_figs:\n",
            "    if p.exists():\n",
            "        print(f'=== {title} ===')\n",
            "        display(Image(filename=str(p)))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5. Cross-Model Consensus (Supporting Models Comparison)\n",
            "\n",
            "We compare top SHAP feature importances across Logistic Regression, Random Forest, and XGBoost."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "comp_df = pd.read_csv(PROJECT_ROOT / 'outputs' / 'tables' / 'feature_importance_comparison.csv')\n",
            "display(comp_df.head(8))\n",
            "\n",
            "p7 = PROJECT_ROOT / 'outputs' / 'shap' / '07_supporting_models_shap_comparison.png'\n",
            "if p7.exists():\n",
            "    display(Image(filename=str(p7)))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 6. Actionable Business Retention Playbook\n",
            "\n",
            "We translate the model findings into an operational retention strategy for ConnectTel's retention team."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "playbook_df = pd.read_csv(PROJECT_ROOT / 'outputs' / 'tables' / 'business_action_playbook.csv')\n",
            "for i, row in playbook_df.iterrows():\n",
            "    print(f\"Risk Driver {i+1}: {row['Risk_Driver']}\")\n",
            "    print(f\"  Target Segment: {row['Target_Customer_Segment']}\")\n",
            "    print(f\"  Evidence:       {row['Empirical_Evidence']}\")\n",
            "    print(f\"  Intervention:   {row['Actionable_Retention_Intervention']}\")\n",
            "    print(f\"  Channel:        {row['Primary_Channel']}\")\n",
            "    print(f\"  Success Metric: {row['Success_Metric']}\\n\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 7. Phase 3 Conclusion\n",
            "\n",
            "- **Explainability Verified:** SHAP and odds ratios demonstrate complete alignment on `contract_monthly`, `failed_payments_90d`, and `tenure_months` as the dominant churn predictors.\n",
            "- **Granular Transparency:** Individual customer predictions can now be diagnosed on demand using waterfall decompositions.\n",
            "- **Actionable Strategy:** ConnectTel's retention team has concrete, prioritized playbooks to intervene before high-risk customers cancel.\n",
            "\n",
            "**Ready for Next Stages:** Live interactive demonstration app, final locked test set evaluation, and presentation deliverables."
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
print(f"Phase 3 notebook written to: {NOTEBOOK_PATH}")
