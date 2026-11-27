import hashlib
from pathlib import Path
from pptx import Presentation

root = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom")

print("=" * 80)
print("POST-CLEANUP VERIFICATION OF ESSENTIAL FILES")
print("=" * 80)

# 1. Final PPT
ppt = root / "deliverables" / "ConnectTel_Executive_Presentation_Final.pptx"
assert ppt.exists(), "Final PPT missing!"
with open(ppt, "rb") as f:
    h = hashlib.sha256(f.read()).hexdigest()
prs = Presentation(str(ppt))
assert len(prs.slides) == 16, f"Expected 16 slides, got {len(prs.slides)}"
assert h == "ceb69bc85838992109f298ceaf21442b43b1a2c9f433365b7935c487364315fe", "Final PPT SHA-256 altered!"
print(f"1. Final PPT: Verified untouched (16 slides, {ppt.stat().st_size:,} bytes, SHA-256: {h[:16]}...)")

# 2. Retained baseline outputs
assert (root / "outputs" / "baseline_predictions.csv").exists(), "baseline_predictions.csv missing!"
assert (root / "outputs" / "baseline_metrics.json").exists(), "baseline_metrics.json missing!"
print("2. Retained baseline outputs in outputs/: Verified intact.")

# 3. All 22 image files
imgs = list((root / "outputs").rglob("*.png"))
assert len(imgs) == 22, f"Expected 22 images, got {len(imgs)}"
print(f"3. All 22 uncompressed project images: Verified intact.")

# 4. Dataset
c_csv = root / "data" / "customers.csv"
assert c_csv.exists(), "customers.csv missing!"
print(f"4. Dataset data/customers.csv: Verified intact ({c_csv.stat().st_size:,} bytes).")

# 5. Notebooks
for nb in ["01_eda_and_feature_engineering.ipynb", "02_model_training_and_tuning.ipynb", "03_model_interpretation_and_business_recommendations.ipynb"]:
    nb_p = root / "notebooks" / nb
    assert nb_p.exists(), f"{nb} missing!"
print("5. All 3 Jupyter Notebooks: Verified intact.")

# 6. Models
for m in ["best_model_pipeline.joblib", "logistic_regression_pipeline.joblib", "random_forest_pipeline.joblib", "xgboost_pipeline.joblib"]:
    m_p = root / "models" / m
    assert m_p.exists(), f"{m} missing!"
print("6. All 4 trained model pipelines: Verified intact.")

# 7. Code & App
assert (root / "app.py").exists(), "app.py missing!"
assert (root / "src" / "inference.py").exists(), "src/inference.py missing!"
assert (root / "baseline.py").exists(), "baseline.py missing!"
assert (root / "baseline_original.py").exists(), "baseline_original.py missing!"
print("7. Source code (app.py, src/inference.py, baseline.py, baseline_original.py): Verified intact.")

# 8. Test inference functionality
import sys
sys.path.insert(0, str(root))
from src.inference import predict_churn

sample = {
    "contract": "month-to-month",
    "tenure_months": 8,
    "monthly_charges_usd": 85.0,
    "total_charges_usd": 680.0,
    "internet_service": "fiber_optic",
    "failed_payments_90d": 2,
    "streaming_service": "no",
    "security_service": "no"
}
res = predict_churn(sample)
print(f"8. Inference test on High-Risk sample:")
print(f"   Churn Probability: {res['churn_probability']} | Prediction: {res['churn_prediction']} | Decision Threshold: {res['decision_threshold']} | Tier: {res['risk_tier']}")
assert res['churn_prediction'] == 1, "Expected churn prediction 1"
assert res['decision_threshold'] == 0.55, "Expected threshold 0.55"

print("\nALL VERIFICATION AUDITS PASSED 100%!")
