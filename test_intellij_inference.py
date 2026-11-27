"""
IntelliJ IDEA Inference Verification Script.
ConnectTel / Persevex AI Internship Project.

Tests the exact import mandated by project instructions:
from src.inference import load_champion_model, predict_churn
Executed from the project root directory.
"""

from src.inference import load_champion_model, predict_churn

def main():
    print("=" * 60)
    print("INTELLIJ IDEA INFERENCE VERIFICATION")
    print("=" * 60)
    
    # 1. Test model loading
    print("\n1. Loading champion model pipeline...")
    model = load_champion_model()
    print("   Success! Loaded model type:", type(model))
    
    # 2. Test Customer Record (ConnectTel Monthly Subscriber with payment failure)
    test_customer = {
        "tenure_months": 8,
        "contract": "monthly",
        "internet_service": "fiber",
        "monthly_charges_usd": 85.0,
        "total_charges_usd": 680.0,
        "security_service": 0,
        "streaming_service": 1,
        "failed_payments_90d": 2
    }
    
    print("\n2. Input Customer Profile:")
    for k, v in test_customer.items():
        print(f"   - {k:22s}: {v}")
        
    # 3. Execute inference using optimal decision threshold (0.55)
    print("\n3. Executing inference via predict_churn() with optimal threshold 0.55...")
    result = predict_churn(test_customer, threshold=0.55, model=model)
    
    # 4. Display outputs
    print("\n4. Inference Results:")
    print(f"   - Churn Prediction:       {result['churn_prediction']} ({'High Risk of Leaving' if result['churn_prediction'] == 1 else 'Retained'})")
    print(f"   - Churn Probability:      {result['churn_probability']:.2%}")
    print(f"   - Retention Probability:  {result['retention_probability']:.2%}")
    print(f"   - Risk Classification:    {result['risk_tier']}")
    print(f"   - Decision Threshold:     {result['decision_threshold']}")
    print(f"   - Identified Triggers:    {result['risk_triggers']}")
    
    # 5. Assertions
    assert "churn_prediction" in result, "Missing prediction"
    assert "churn_probability" in result, "Missing probability"
    assert "risk_tier" in result, "Missing risk tier"
    assert 0.0 <= result["churn_probability"] <= 1.0, "Probability out of bounds"
    assert result["churn_prediction"] in [0, 1], "Invalid binary prediction"
    
    print("\n" + "=" * 60)
    print("ALL INTELLIJ INFERENCE CHECKS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
