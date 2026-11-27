import json
import os
import joblib
import pandas as pd
import numpy as np

base_dir = r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom"

print("=" * 70)
print("GROUND TRUTH AUDIT SCRIPT")
print("=" * 70)

# 1. Notebook 2: Model Training and Tuning outputs
nb2_path = os.path.join(base_dir, "notebooks", "02_model_training_and_tuning.ipynb")
with open(nb2_path, "r", encoding="utf-8") as f:
    nb2 = json.load(f)

print("\n--- NOTEBOOK 2 OUTPUTS ---")
for idx, cell in enumerate(nb2["cells"]):
    src = "".join(cell.get("source", []))
    if any(k in src.lower() for k in ["comparison", "results", "pr_auc", "xgb", "champion", "grid", "cv_results"]):
        print(f"\n[Cell {idx} - {cell['cell_type']}] Source excerpt:\n{src[:250]}...")
        outputs = cell.get("outputs", [])
        for out in outputs:
            if "text" in out:
                print("Output text:\n" + "".join(out["text"])[:600])
            elif "data" in out:
                for mime, val in out["data"].items():
                    if mime == "text/plain":
                        print("Output plain text:\n" + "".join(val)[:600])
                    elif mime == "text/html":
                        print("Output HTML (first 300 chars):\n" + "".join(val)[:300])

# 2. Notebook 3: SHAP, customer cases, odds ratios, recommendations
nb3_path = os.path.join(base_dir, "notebooks", "03_model_interpretation_and_business_recommendations.ipynb")
with open(nb3_path, "r", encoding="utf-8") as f:
    nb3 = json.load(f)

print("\n--- NOTEBOOK 3 OUTPUTS ---")
for idx, cell in enumerate(nb3["cells"]):
    src = "".join(cell.get("source", []))
    if any(k in src.lower() for k in ["waterfall", "odds_ratio", "customer", "case", "recommendation", "net", "roi", "cac", "18,480", "18480"]):
        print(f"\n[Cell {idx} - {cell['cell_type']}] Source excerpt:\n{src[:250]}...")
        outputs = cell.get("outputs", [])
        for out in outputs:
            if "text" in out:
                print("Output text:\n" + "".join(out["text"])[:600])
            elif "data" in out:
                for mime, val in out["data"].items():
                    if mime == "text/plain":
                        print("Output plain text:\n" + "".join(val)[:600])

# 3. Check reports
print("\n--- CHECKING REPORTS ---")
reports_dir = os.path.join(base_dir, "reports")
for rname in os.listdir(reports_dir):
    rpath = os.path.join(reports_dir, rname)
    with open(rpath, "r", encoding="utf-8") as f:
        txt = f.read()
    matches = []
    for target in ["18,480", "18480", "CAC", "$300", "450", "0.4923", "0.3800", "0.3831", "Fiber optic", "Customer #38", "Customer 38"]:
        if target.lower() in txt.lower():
            matches.append(target)
    if matches:
        print(f"Report '{rname}' matched: {matches}")
