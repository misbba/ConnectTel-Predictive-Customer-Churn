"""
Verification Script for ConnectTel Churn Risk Simulator Logic.
Tests inference for all presets and manual input modifications.
"""

import sys
from pathlib import Path

ROOT = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom")
sys.path.append(str(ROOT / "src"))

from inference import load_champion_model, predict_churn, DEFAULT_DECISION_THRESHOLD

def test_simulator_logic():
    print("=" * 65)
    print("CONNECTTEL SIMULATOR INFERENCE & STATE LOGIC VERIFICATION")
    print("=" * 65)
    
    # Check decision threshold
    print(f"\n1. Operational Decision Threshold: {DEFAULT_DECISION_THRESHOLD}")
    assert DEFAULT_DECISION_THRESHOLD == 0.55, f"Expected 0.55, got {DEFAULT_DECISION_THRESHOLD}"
    
    # 2. Check all 4 Presets
    presets = {
        "Preset 1 (High-Risk Delinquent)": {
            "tenure_months": 8, "contract": "monthly", "internet_service": "fiber",
            "monthly_charges_usd": 85.0, "total_charges_usd": 680.0,
            "security_service": 0, "streaming_service": 1, "failed_payments_90d": 2
        },
        "Preset 2 (Loyal Subscriber)": {
            "tenure_months": 48, "contract": "two_year", "internet_service": "fiber",
            "monthly_charges_usd": 45.0, "total_charges_usd": 2160.0,
            "security_service": 1, "streaming_service": 1, "failed_payments_90d": 0
        },
        "Preset 3 (Brand New Signup - Tenure 0)": {
            "tenure_months": 0, "contract": "monthly", "internet_service": "dsl",
            "monthly_charges_usd": 55.0, "total_charges_usd": None,
            "security_service": 0, "streaming_service": 0, "failed_payments_90d": 0
        },
        "Preset 4 (Annual Issue)": {
            "tenure_months": 24, "contract": "annual", "internet_service": "fiber",
            "monthly_charges_usd": 95.0, "total_charges_usd": 2280.0,
            "security_service": 0, "streaming_service": 1, "failed_payments_90d": 1
        }
    }
    
    print("\n2. Testing 4 Presets via predict_churn():")
    for name, payload in presets.items():
        res = predict_churn(payload, threshold=DEFAULT_DECISION_THRESHOLD)
        print(f"   [{name}]")
        print(f"      - Churn Pred:      {res['churn_prediction']} ({'CHURN' if res['churn_prediction'] == 1 else 'RETAIN'})")
        print(f"      - Risk Score:      {res['churn_probability']:.2%}")
        print(f"      - Retain Score:    {res['retention_probability']:.2%}")
        print(f"      - Classification:  {res['risk_tier']}")
        print(f"      - Triggers ({len(res['risk_triggers'])}):  {res['risk_triggers']}")
        
        # Invariants
        assert res['churn_prediction'] in [0, 1]
        assert round(res['churn_probability'] + res['retention_probability'], 4) == 1.0000
        assert res['risk_tier'] in ['Critical', 'High', 'Medium', 'Low']
    
    # 3. Test Manual Input Adjustments (Simulating user moving slider & typing in form)
    print("\n3. Testing Manual Input Modifications (Simulating Calculate Button Click):")
    
    # Case A: User changes Loyal Subscriber (Preset 2) to Month-to-Month with 1 failed payment
    manual_case_a = {
        "tenure_months": 18,
        "contract": "monthly",
        "internet_service": "fiber",
        "monthly_charges_usd": 80.0,
        "total_charges_usd": 1440.0,
        "security_service": 0,
        "streaming_service": 1,
        "failed_payments_90d": 1
    }
    res_a = predict_churn(manual_case_a, threshold=DEFAULT_DECISION_THRESHOLD)
    print("   [Manual Case A: Month-to-Month Fiber, 18m, 1 Fail]")
    print(f"      - Churn Pred:     {res_a['churn_prediction']} (Risk: {res_a['churn_probability']:.2%}) | Tier: {res_a['risk_tier']}")
    print(f"      - Triggers:       {res_a['risk_triggers']}")
    assert res_a['churn_prediction'] == 1, "Expected churn prediction = 1 for month-to-month with failed payment"
    
    # Case B: User converts High-Risk Delinquent (Preset 1) by adding 2-Year Contract and resolving payments
    manual_case_b = {
        "tenure_months": 8,
        "contract": "two_year",
        "internet_service": "fiber",
        "monthly_charges_usd": 85.0,
        "total_charges_usd": 680.0,
        "security_service": 1,
        "streaming_service": 1,
        "failed_payments_90d": 0
    }
    res_b = predict_churn(manual_case_b, threshold=DEFAULT_DECISION_THRESHOLD)
    print("   [Manual Case B: Upgraded to Two-Year & Security, 0 Fails]")
    print(f"      - Churn Pred:     {res_b['churn_prediction']} (Risk: {res_b['churn_probability']:.2%}) | Tier: {res_b['risk_tier']}")
    print(f"      - Triggers:       {res_b['risk_triggers']}")
    assert res_b['churn_prediction'] == 0, "Expected retain prediction = 0 after contract commitment"
    
    print("\n" + "=" * 65)
    print("ALL SIMULATOR INFERENCE & PRESET CHECKS PASSED PERFECTLY!")
    print("=" * 65)

if __name__ == "__main__":
    test_simulator_logic()
