import json
import pandas as pd
import numpy as np

# Ground Truth Validation Table
df_val = pd.read_csv(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\outputs\tables\model_comparison_validation.csv")
print("=== GROUND TRUTH VALIDATION METRICS ===")
for _, r in df_val.iterrows():
    print(f"Model: {r['Model']}")
    print(f"  CV Mean ROC-AUC: {r['CV Mean ROC-AUC']}")
    print(f"  Val ROC-AUC:     {r['Val ROC-AUC']:.4f}")
    print(f"  Val PR-AUC:      {r['Val PR-AUC']:.4f}")
    print(f"  Val Recall(0.5): {r['Val Recall (0.5)']:.4f}")
    print(f"  Val Prec(0.5):   {r['Val Precision (0.5)']:.4f}")
    print(f"  Val F1(0.5):     {r['Val F1 (0.5)']:.4f}")
    print(f"  Val Brier:       {r['Val Brier Score']:.6f}")

# Ground Truth Threshold Table for Logistic Regression
df_thresh = pd.read_csv(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\outputs\tables\threshold_analysis.csv")
print("\n=== GROUND TRUTH LOGISTIC REGRESSION THRESHOLDS ===")
lr_t = df_thresh[df_thresh['Model'] == 'Logistic Regression'].sort_values(by='Threshold')
for _, r in lr_t.iterrows():
    if r['Threshold'] in [0.45, 0.50, 0.55, 0.60]:
        print(f"Thresh {r['Threshold']:.2f}: Prec={r['Precision']:.4f}, Rec={r['Recall']:.4f}, F1={r['F1_Score']:.4f}, TP={int(r['TP'])}, FP={int(r['FP'])}, FN={int(r['FN'])}, TN={int(r['TN'])}")

# Ground Truth Test Evaluation (from Phase 5 report)
print("\n=== GROUND TRUTH TEST EVALUATION (Phase 5) ===")
# Let's inspect phase_5_final_evaluation_and_intellij_integration.md
with open(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom\reports\phase_5_final_evaluation_and_intellij_integration.md", "r", encoding="utf-8") as f:
    p5_txt = f.read()

for l in p5_txt.split("\n"):
    if any(k in l for k in ["ROC-AUC", "PR-AUC", "Recall", "Precision", "F1", "Brier", "Confusion Matrix", "TP"]):
        print(l)
