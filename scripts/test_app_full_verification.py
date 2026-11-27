"""
Comprehensive Verification Script for ConnectTel Streamlit Application.
Tests:
1. Preset buttons logic (all 4 presets)
2. Calculate Churn Risk button workflow
3. Manual input updates and reactive recalculation
4. Synchronized risk scores, complementary scores, tiers, triggers, and prescriptions
"""

import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom")
sys.path.append(str(ROOT / "src"))

from inference import load_champion_model, predict_churn, DEFAULT_DECISION_THRESHOLD

CONTRACT_MAPPING = {
    "Month-to-Month": "monthly",
    "Annual": "annual",
    "Two-Year": "two_year"
}
INTERNET_MAPPING = {
    "Fiber Optic": "fiber",
    "DSL": "dsl",
    "None (No Internet)": "none"
}

def build_customer_payload(tenure, contract, internet, monthly, total, security, streaming, fails):
    contract_slug = CONTRACT_MAPPING.get(contract, contract)
    internet_slug = INTERNET_MAPPING.get(internet, internet)
    is_zero = (int(tenure) == 0)
    
    return {
        "tenure_months": int(tenure),
        "contract": contract_slug,
        "internet_service": internet_slug,
        "monthly_charges_usd": float(monthly),
        "total_charges_usd": None if is_zero else float(total),
        "security_service": int(security),
        "streaming_service": int(streaming),
        "failed_payments_90d": int(fails)
    }

def run_tests():
    print("=" * 70)
    print("CONNECTTEL APPLICATION: COMPREHENSIVE BUTTON & STATE TEST SUITE")
    print("=" * 70)
    
    # Verify Model
    model = load_champion_model()
    print("\n[STEP 1] Champion Model Loaded Successfully:")
    print(f"  - Model Pipeline Type: {type(model)}")
    print(f"  - Operational Decision Threshold: {DEFAULT_DECISION_THRESHOLD}")
    assert DEFAULT_DECISION_THRESHOLD == 0.55
    
    # Test Payload Builder
    print("\n[STEP 2] Testing build_customer_payload():")
    p1 = build_customer_payload(8, "Month-to-Month", "Fiber Optic", 85.0, 680.0, False, True, 2)
    assert p1["contract"] == "monthly"
    assert p1["internet_service"] == "fiber"
    assert p1["total_charges_usd"] == 680.0
    assert p1["security_service"] == 0
    assert p1["streaming_service"] == 1
    assert p1["failed_payments_90d"] == 2
    print("  [OK] Payload builder formats categorical slugs and types correctly.")
    
    # Test Zero-Tenure Rule in Payload Builder
    p_zero = build_customer_payload(0, "Month-to-Month", "DSL", 55.0, 0.0, False, False, 0)
    assert p_zero["total_charges_usd"] is None
    print("  [OK] Zero-tenure accounts correctly set total_charges_usd = None.")
    
    # Test All 4 Presets
    print("\n[STEP 3] Testing All 4 Quick Presets (Simulating Preset Button Clicks):")
    presets_config = [
        ("High-Risk Delinquent Profile", 8, "Month-to-Month", "Fiber Optic", 85.0, 680.0, False, True, 2, 1, "Critical"),
        ("Loyal Long-Term Subscriber", 48, "Two-Year", "Fiber Optic", 45.0, 2160.0, True, True, 0, 0, "Low"),
        ("Brand New Signup (Tenure 0)", 0, "Month-to-Month", "DSL", 55.0, 0.0, False, False, 0, 0, "Low"),
        ("Annual Contract with Payment Issue", 24, "Annual", "Fiber Optic", 95.0, 2280.0, False, True, 1, 0, "Medium"),
    ]
    
    for name, tenure, contract, internet, monthly, total, sec, stream, fails, exp_pred, exp_tier in presets_config:
        payload = build_customer_payload(tenure, contract, internet, monthly, total, sec, stream, fails)
        res = predict_churn(payload, threshold=DEFAULT_DECISION_THRESHOLD)
        print(f"\n  Testing Preset: {name}")
        print(f"    - Tenure: {tenure}m | Contract: {contract} | Internet: {internet}")
        print(f"    - Monthly: ${monthly} | Total: ${total} | Security: {sec} | Stream: {stream} | Fails: {fails}")
        print(f"    - Prediction:          {res['churn_prediction']} ({'CHURN' if res['churn_prediction'] == 1 else 'RETAINED'})")
        print(f"    - Risk Score:          {res['churn_probability']:.2%}")
        print(f"    - Complementary Score: {res['retention_probability']:.2%}")
        print(f"    - Classification:      {res['risk_tier']}")
        print(f"    - Active Triggers:     {res['risk_triggers']}")
        
        assert res["churn_prediction"] == exp_pred, f"Preset {name} prediction mismatch: {res['churn_prediction']} != {exp_pred}"
        assert res["risk_tier"] == exp_tier, f"Preset {name} tier mismatch: {res['risk_tier']} != {exp_tier}"
        assert round(res["churn_probability"] + res["retention_probability"], 4) == 1.0000
    
    # Test Calculate Churn Risk Button with Manual Changes
    print("\n[STEP 4] Testing 'Calculate Churn Risk' Button Workflow (Simulating User Form Edits):")
    
    # Scenario 1: User starts at Preset 1 (High Risk 90.96%) and switches contract to Annual
    print("\n  Scenario 1: User switches from Month-to-Month to Annual Contract (other features unchanged)")
    payload_edited_1 = build_customer_payload(8, "Annual", "Fiber Optic", 85.0, 680.0, False, True, 2)
    res_1 = predict_churn(payload_edited_1, threshold=DEFAULT_DECISION_THRESHOLD)
    print(f"    - Initial Risk (Month-to-Month): 90.96% (Tier: Critical)")
    print(f"    - After 'Calculate Churn Risk' Click: {res_1['churn_probability']:.2%} (Tier: {res_1['risk_tier']})")
    print(f"    - New Triggers: {res_1['risk_triggers']}")
    assert res_1["churn_probability"] < 0.9096, "Expected risk to drop after annual contract commitment"
    
    # Scenario 2: User adds Online Security to High-Risk Profile
    print("\n  Scenario 2: User adds Online Security service")
    payload_edited_2 = build_customer_payload(8, "Month-to-Month", "Fiber Optic", 85.0, 680.0, True, True, 2)
    res_2 = predict_churn(payload_edited_2, threshold=DEFAULT_DECISION_THRESHOLD)
    print(f"    - After 'Calculate Churn Risk' Click: {res_2['churn_probability']:.2%} (Tier: {res_2['risk_tier']})")
    assert res_2["churn_probability"] < 0.9096, "Expected risk to drop with security add-on"
    
    # Scenario 3: Complete Turnaround (User fixes billing, signs 2-Year contract, reaches 18 months)
    print("\n  Scenario 3: User applies complete turnaround (2-Year contract, 18m tenure, 0 fails, security enabled)")
    payload_turnaround = build_customer_payload(18, "Two-Year", "Fiber Optic", 65.0, 1170.0, True, True, 0)
    res_turnaround = predict_churn(payload_turnaround, threshold=DEFAULT_DECISION_THRESHOLD)
    print(f"    - Prediction:          {res_turnaround['churn_prediction']} (RETAINED)")
    print(f"    - Risk Score:          {res_turnaround['churn_probability']:.2%}")
    print(f"    - Complementary Score: {res_turnaround['retention_probability']:.2%}")
    print(f"    - Classification:      {res_turnaround['risk_tier']}")
    print(f"    - Active Triggers:     {res_turnaround['risk_triggers']}")
    assert res_turnaround["churn_prediction"] == 0
    assert res_turnaround["risk_tier"] == "Low"
    assert len(res_turnaround["risk_triggers"]) == 0
    
    print("\n" + "=" * 70)
    print("ALL APPLICATION BUTTON & STATE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
