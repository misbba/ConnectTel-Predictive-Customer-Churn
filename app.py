"""
ConnectTel – Customer Churn Risk Simulator
Persevex AI Internship Project | Phase 6 Working Application

Theme: Deep black background, dark chocolate-brown cards, warm orange accent,
rounded containers, and clean executive typography.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# Setup paths for custom transformers and model loading
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.inference import load_champion_model, predict_churn, DEFAULT_DECISION_THRESHOLD

# Page Configuration
st.set_page_config(
    page_title="ConnectTel | Customer Churn Risk Simulator",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Deep black, dark chocolate brown cards, warm orange accent)
CUSTOM_CSS = """
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e0e11 !important;
        color: #e5e5e8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1c1512 0%, #261c16 100%);
        border: 1px solid #3d2a20;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .main-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .title-orange {
        color: #ff7a00;
    }
    .main-subtitle {
        color: #9e9ea7;
        font-size: 14px;
        margin-top: 6px;
    }
    .threshold-badge {
        display: inline-block;
        background-color: #2e1d13;
        border: 1px solid #f26419;
        color: #ff8c32;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Cards */
    .connecttel-card {
        background-color: #1a1411;
        border: 1px solid #33231a;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .card-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #2e1e16;
        padding-bottom: 10px;
    }
    .card-title-icon {
        color: #ff7a00;
    }
    
    /* Metrics Row */
    .metric-pill {
        background-color: #15110f;
        border: 1px solid #2e1d15;
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-value-orange {
        font-size: 20px;
        font-weight: 700;
        color: #ff7a00;
    }
    .metric-label {
        font-size: 11px;
        color: #9e9ea7;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Result Banners */
    .result-banner-churn {
        background: linear-gradient(135deg, #38120d 0%, #4a1912 100%);
        border: 1px solid #ff4d4f;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 18px;
    }
    .result-banner-retain {
        background: linear-gradient(135deg, #0d2e1c 0%, #133d26 100%);
        border: 1px solid #52c41a;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 18px;
    }
    .result-status {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .status-churn { color: #ff7875; }
    .status-retain { color: #73d13d; }
    
    /* Risk Tiers */
    .tier-critical {
        background-color: #431414;
        color: #ff7875;
        border: 1px solid #a8071a;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .tier-high {
        background-color: #3b2210;
        color: #ffa940;
        border: 1px solid #d46b08;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .tier-medium {
        background-color: #362f11;
        color: #ffec3d;
        border: 1px solid #d4b106;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .tier-low {
        background-color: #112a19;
        color: #73d13d;
        border: 1px solid #237804;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    
    /* Status Feedback Banners */
    .status-alert-update {
        background: linear-gradient(135deg, #1c2b1a 0%, #253a23 100%);
        border: 1px solid #52c41a;
        color: #95de64;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        font-weight: 600;
    }
    .status-alert-warning {
        background: linear-gradient(135deg, #2e2413 0%, #3d2f16 100%);
        border: 1px solid #faad14;
        color: #ffd666;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        font-weight: 600;
    }
    .status-alert-info {
        background: linear-gradient(135deg, #15202b 0%, #1c2c3d 100%);
        border: 1px solid #1890ff;
        color: #91d5ff;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Risk Trigger Bullet */
    .trigger-item {
        background-color: #211914;
        border-left: 3px solid #ff7a00;
        border-radius: 4px;
        padding: 8px 12px;
        margin-bottom: 8px;
        font-size: 13px;
        color: #dedee3;
    }
    .action-item {
        background-color: #1e1915;
        border-left: 3px solid #f26419;
        border-radius: 4px;
        padding: 10px 14px;
        margin-bottom: 10px;
        font-size: 13px;
    }
    .action-title {
        color: #ff944d;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .action-desc {
        color: #b5b5be;
        font-size: 12px;
    }
    
    /* Streamlit Widget Overrides */
    div[data-baseweb="select"] > div {
        background-color: #120e0c !important;
        border-color: #3d2b21 !important;
        color: #ffffff !important;
    }
    div[data-baseweb="input"] > div {
        background-color: #120e0c !important;
        border-color: #3d2b21 !important;
        color: #ffffff !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #f26419 0%, #ff7a00 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        width: 100% !important;
        font-size: 15px !important;
        box-shadow: 0 4px 12px rgba(242, 100, 25, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff7a00 0%, #ff944d 100%) !important;
        box-shadow: 0 6px 16px rgba(242, 100, 25, 0.5) !important;
        transform: translateY(-1px) !important;
    }
    .disclaimer-box {
        background-color: #13100f;
        border: 1px dashed #3a281e;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 12px;
        color: #8c8c94;
        margin-top: 16px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="main-header">
    <div class="main-title">
        <span>📶 Connect<span class="title-orange">Tel</span></span>
        <span style="font-weight: 300; color: #55443c;">|</span>
        <span style="font-size: 22px; font-weight: 500;">Customer Churn Risk Simulator</span>
    </div>
    <div class="main-subtitle">
        Persevex AI Internship Project · Machine Learning Production Retention Engine
    </div>
    <div class="threshold-badge">
        🎯 Operational Decision Threshold: 0.55 (Max Validation F1 = 0.4667 | Test Recall = 75.0%)
    </div>
</div>
""", unsafe_allow_html=True)

# Performance Highlights Bar
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""
    <div class="metric-pill">
        <div class="metric-value">Logistic Reg</div>
        <div class="metric-label">Champion Model</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-pill">
        <div class="metric-value-orange">0.7679</div>
        <div class="metric-label">Final Test ROC-AUC</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-pill">
        <div class="metric-value">75.0%</div>
        <div class="metric-label">Test Recall (6/8)</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-pill">
        <div class="metric-value-orange">0.4708</div>
        <div class="metric-label">Test PR-AUC</div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div class="metric-pill">
        <div class="metric-value">0.095473</div>
        <div class="metric-label">Baseline Test Brier</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Feature Mappings
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
    """Build standardized feature dictionary for inference pipeline."""
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

def apply_preset(tenure, contract, internet, monthly, total, security, streaming, fails, preset_name):
    """Callback triggered on preset button click: updates session state and calculates prediction."""
    st.session_state["widget_tenure"] = int(tenure)
    st.session_state["widget_contract"] = str(contract)
    st.session_state["widget_internet"] = str(internet)
    st.session_state["widget_monthly"] = float(monthly)
    st.session_state["widget_total"] = float(total)
    st.session_state["widget_security"] = bool(security)
    st.session_state["widget_streaming"] = bool(streaming)
    st.session_state["widget_fails"] = int(fails)
    
    payload = build_customer_payload(tenure, contract, internet, monthly, total, security, streaming, fails)
    st.session_state["evaluated_payload"] = payload
    st.session_state["prediction_result"] = predict_churn(payload, threshold=DEFAULT_DECISION_THRESHOLD)
    st.session_state["status_type"] = "preset"
    st.session_state["status_message"] = (
        f"⚡ <strong>Preset Loaded: {preset_name}</strong> — "
        f"Model estimated risk score is <strong>{st.session_state['prediction_result']['churn_probability']:.1%}</strong> "
        f"(Tier: {st.session_state['prediction_result']['risk_tier'].upper()})."
    )

# Session State Initialization on First Load
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    st.session_state["widget_tenure"] = 8
    st.session_state["widget_contract"] = "Month-to-Month"
    st.session_state["widget_internet"] = "Fiber Optic"
    st.session_state["widget_monthly"] = 85.0
    st.session_state["widget_total"] = 680.0
    st.session_state["widget_security"] = False
    st.session_state["widget_streaming"] = True
    st.session_state["widget_fails"] = 2
    
    init_payload = build_customer_payload(8, "Month-to-Month", "Fiber Optic", 85.0, 680.0, False, True, 2)
    st.session_state["evaluated_payload"] = init_payload
    st.session_state["prediction_result"] = predict_churn(init_payload, threshold=DEFAULT_DECISION_THRESHOLD)
    st.session_state["status_type"] = "initial"
    st.session_state["status_message"] = "Initial benchmark profile loaded: High-Risk Delinquent Account."

# Preset Profiles Bar
st.markdown("##### ⚡ Quick Customer Presets")
p_col1, p_col2, p_col3, p_col4 = st.columns([1, 1, 1, 1])
with p_col1:
    st.button(
        "🔥 High-Risk Delinquent Profile",
        key="btn_preset_1",
        on_click=apply_preset,
        args=(8, "Month-to-Month", "Fiber Optic", 85.0, 680.0, False, True, 2, "High-Risk Delinquent Profile"),
        use_container_width=True
    )
with p_col2:
    st.button(
        "🛡️ Loyal Long-Term Subscriber",
        key="btn_preset_2",
        on_click=apply_preset,
        args=(48, "Two-Year", "Fiber Optic", 45.0, 2160.0, True, True, 0, "Loyal Long-Term Subscriber"),
        use_container_width=True
    )
with p_col3:
    st.button(
        "🆕 Brand New Signup (Tenure 0)",
        key="btn_preset_3",
        on_click=apply_preset,
        args=(0, "Month-to-Month", "DSL", 55.0, 0.0, False, False, 0, "Brand New Signup (Tenure 0)"),
        use_container_width=True
    )
with p_col4:
    st.button(
        "⚠️ Annual Contract with Payment Issue",
        key="btn_preset_4",
        on_click=apply_preset,
        args=(24, "Annual", "Fiber Optic", 95.0, 2280.0, False, True, 1, "Annual Contract with Payment Issue"),
        use_container_width=True
    )

st.write("")

# Main Interface: Left = Input Form, Right = Prediction & Prescriptions
left_col, right_col = st.columns([1.1, 1.2], gap="large")

with left_col:
    st.markdown("""
    <div class="connecttel-card">
        <div class="card-title">
            <span class="card-title-icon">📋</span> Customer Account Parameters
        </div>
    """, unsafe_allow_html=True)
    
    # Contract & Internet Rows
    c1, c2 = st.columns(2)
    with c1:
        contract_options = ["Month-to-Month", "Annual", "Two-Year"]
        contract_choice = st.selectbox(
            "Contract Type",
            contract_options,
            key="widget_contract"
        )
    with c2:
        internet_options = ["Fiber Optic", "DSL", "None (No Internet)"]
        internet_choice = st.selectbox(
            "Internet Service",
            internet_options,
            key="widget_internet"
        )
        
    # Tenure & Failed Payments Rows
    c3, c4 = st.columns(2)
    with c3:
        tenure_val = st.slider(
            "Tenure (Months)",
            min_value=0,
            max_value=60,
            key="widget_tenure"
        )
    with c4:
        fails_val = st.selectbox(
            "Failed Payments (Last 90 Days)",
            [0, 1, 2],
            key="widget_fails"
        )
        
    # Billing Parameters
    c5, c6 = st.columns(2)
    with c5:
        monthly_val = st.number_input(
            "Monthly Charges ($ USD)",
            min_value=20.0,
            max_value=110.0,
            step=1.0,
            key="widget_monthly"
        )
    with c6:
        is_zero_tenure = (tenure_val == 0)
        if is_zero_tenure:
            total_val = None
            st.info("ℹ️ Tenure = 0: Zero historical cycles accrued. Handled safely via explicit domain rule.")
        else:
            # If widget_total is <= 0 or missing, initialize to reasonable estimate
            if st.session_state.get("widget_total", 0.0) <= 0.0:
                st.session_state["widget_total"] = float(round(tenure_val * monthly_val, 2))
            total_val = st.number_input(
                "Total Charges ($ USD)",
                min_value=0.0,
                max_value=10000.0,
                step=50.0,
                key="widget_total"
            )
            
    # Add-on Services
    st.markdown("<p style='font-size: 13px; font-weight: 600; color: #ffffff; margin-top: 8px;'>Subscribed Add-On Services</p>", unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        sec_val = st.checkbox("🛡️ Online Security Service", key="widget_security")
    with c8:
        stream_val = st.checkbox("🎬 Streaming TV / Media", key="widget_streaming")
        
    st.write("")
    calculate_clicked = st.button("🚀 Calculate Churn Risk", key="btn_calculate_churn", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Build current payload from latest customer input values
current_payload = build_customer_payload(
    tenure=tenure_val,
    contract=contract_choice,
    internet=internet_choice,
    monthly=monthly_val,
    total=0.0 if is_zero_tenure else total_val,
    security=sec_val,
    streaming=stream_val,
    fails=fails_val
)

# Detect if current input parameters differ from the last evaluated payload
eval_p = st.session_state.get("evaluated_payload", {})
inputs_differ_from_last_eval = False
if eval_p:
    if (eval_p["tenure_months"] != current_payload["tenure_months"] or
        eval_p["contract"] != current_payload["contract"] or
        eval_p["internet_service"] != current_payload["internet_service"] or
        eval_p["monthly_charges_usd"] != current_payload["monthly_charges_usd"] or
        eval_p["total_charges_usd"] != current_payload["total_charges_usd"] or
        eval_p["security_service"] != current_payload["security_service"] or
        eval_p["streaming_service"] != current_payload["streaming_service"] or
        eval_p["failed_payments_90d"] != current_payload["failed_payments_90d"]):
        inputs_differ_from_last_eval = True

# When the user clicks "🚀 Calculate Churn Risk"
if calculate_clicked:
    # 1. Read latest customer input values (current_payload)
    # 2. Call the actual predict_churn() function from src/inference.py
    new_result = predict_churn(current_payload, threshold=DEFAULT_DECISION_THRESHOLD)
    
    # 3. Update churn prediction
    # 4. Update model-estimated risk score and complementary score
    # 5. Update risk classification
    st.session_state["prediction_result"] = new_result
    st.session_state["evaluated_payload"] = current_payload
    
    calc_time = pd.Timestamp.now().strftime("%H:%M:%S")
    st.session_state["status_type"] = "updated"
    st.session_state["status_message"] = (
        f"✅ <strong>Churn Risk Recalculated at {calc_time}:</strong> "
        f"Model estimated risk score is <strong>{new_result['churn_probability']:.1%}</strong> "
        f"(Tier: {new_result['risk_tier'].upper()})."
    )
    inputs_differ_from_last_eval = False

# Right Column: Prediction Engine Outputs
with right_col:
    result = st.session_state["prediction_result"]
    eval_profile = st.session_state["evaluated_payload"]
    
    churn_prob = result["churn_probability"]
    retain_prob = result["retention_probability"]
    is_churn = result["churn_prediction"]
    tier = result["risk_tier"]
    triggers = result["risk_triggers"]
    
    eval_contract = eval_profile["contract"]
    eval_internet = eval_profile["internet_service"]
    eval_tenure = eval_profile["tenure_months"]
    eval_fails = eval_profile["failed_payments_90d"]
    eval_monthly = eval_profile["monthly_charges_usd"]
    eval_sec = bool(eval_profile["security_service"])
    eval_stream = bool(eval_profile["streaming_service"])
    
    # Feedback Notification Banners
    if inputs_differ_from_last_eval and not calculate_clicked:
        st.markdown("""
        <div class="status-alert-warning">
            <span>⚠️ <strong>Parameters Modified:</strong> You have changed account settings. Click <strong>'🚀 Calculate Churn Risk'</strong> to evaluate the updated profile.</span>
        </div>
        """, unsafe_allow_html=True)
    elif "status_message" in st.session_state and st.session_state.get("status_type") == "updated":
        st.markdown(f"""
        <div class="status-alert-update">
            <span>{st.session_state["status_message"]}</span>
        </div>
        """, unsafe_allow_html=True)
    elif "status_message" in st.session_state and st.session_state.get("status_type") == "preset":
        st.markdown(f"""
        <div class="status-alert-info">
            <span>{st.session_state["status_message"]}</span>
        </div>
        """, unsafe_allow_html=True)
        
    # 1. Primary Verdict Card
    if is_churn == 1:
        st.markdown(f"""
        <div class="result-banner-churn">
            <div class="result-status status-churn">⚠️ HIGH RISK OF CHURN</div>
            <div style="font-size: 14px; color: #ffccc7;">Model flags this customer as high risk of churn within 30 days.</div>
            <div style="margin-top: 12px;">
                <span class="tier-{tier.lower()}">Risk Classification: {tier.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-banner-retain">
            <div class="result-status status-retain">✅ RETAINED SUBSCRIBER</div>
            <div style="font-size: 14px; color: #d9f7be;">Customer predicted to remain active under current terms.</div>
            <div style="margin-top: 12px;">
                <span class="tier-{tier.lower()}">Risk Classification: {tier.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # 2. Risk Score & Model Calibration Transparency
    st.markdown("""
    <div class="connecttel-card">
        <div class="card-title">
            <span class="card-title-icon">📊</span> Risk Score Metrics
        </div>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(f"""
        <div style="background-color: #15110f; border: 1px solid #3d2319; border-radius: 10px; padding: 14px; text-align: center;">
            <div style="font-size: 28px; font-weight: 800; color: #ff7a00;">{churn_prob:.1%}</div>
            <div style="font-size: 11px; color: #9e9ea7; text-transform: uppercase; margin-top: 4px;">Model-Estimated Risk Score</div>
            <div style="font-size: 10px; color: #6e6e76; margin-top: 2px;">(Uncalibrated discriminative score)</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div style="background-color: #15110f; border: 1px solid #1f3627; border-radius: 10px; padding: 14px; text-align: center;">
            <div style="font-size: 28px; font-weight: 800; color: #52c41a;">{retain_prob:.1%}</div>
            <div style="font-size: 11px; color: #9e9ea7; text-transform: uppercase; margin-top: 4px;">Complementary Score</div>
            <div style="font-size: 10px; color: #6e6e76; margin-top: 2px;">(1.0 - Estimated Risk Score)</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Visual Progress Bar
    st.progress(float(churn_prob))
    st.caption(f"Decision Boundary: Risk Score $\\ge$ {DEFAULT_DECISION_THRESHOLD:.2f} triggers retention intervention.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 3. Model Explainability & Active Triggers
    st.markdown("""
    <div class="connecttel-card">
        <div class="card-title">
            <span class="card-title-icon">🔍</span> Identified Risk Drivers & Protective Factors
        </div>
    """, unsafe_allow_html=True)
    
    if triggers:
        for t in triggers:
            st.markdown(f'<div class="trigger-item">⚠️ {t}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="trigger-item" style="border-left-color: #52c41a;">✅ Zero acute risk triggers identified. Stable subscriber profile.</div>', unsafe_allow_html=True)
        
    # Additional Contextual Factors
    if eval_sec:
        st.markdown('<div class="trigger-item" style="border-left-color: #4575b4;">🛡️ Active Online Security subscription acts as a retention stickiness anchor (OR = 0.79x).</div>', unsafe_allow_html=True)
    if eval_contract in ["annual", "two_year"]:
        st.markdown('<div class="trigger-item" style="border-left-color: #4575b4;">🔒 Long-Term Commitment Plan substantially mitigates switching velocity (OR = 0.14x vs monthly).</div>', unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 4. Actionable Retention Recommendations
    st.markdown("""
    <div class="connecttel-card">
        <div class="card-title">
            <span class="card-title-icon">🎯</span> Prescribed Retention Interventions (Playbook)
        </div>
    """, unsafe_allow_html=True)
    
    if eval_contract == "monthly":
        st.markdown("""
        <div class="action-item">
            <div class="action-title">1. Proactive Contract Migration Offer (High Priority)</div>
            <div class="action-desc">Dispatch a personalized 1-Year commitment offer featuring a 15% rate lock discount plus 3 months of complimentary cybersecurity protection. Month-to-month contracts multiply churn odds by 7.04x.</div>
        </div>
        """, unsafe_allow_html=True)
        
    if eval_fails >= 1:
        st.markdown("""
        <div class="action-item">
            <div class="action-title">2. Smart Billing Recovery Sequence (Urgent)</div>
            <div class="action-desc">Trigger automated 'Card Update Concierge' via SMS with frictionless payment retry link and optional flexible due-date selection. Avoid punitive disconnection notices which accelerate churn.</div>
        </div>
        """, unsafe_allow_html=True)
        
    if eval_tenure <= 12:
        st.markdown("""
        <div class="action-item">
            <div class="action-title">3. VIP Onboarding Check-In</div>
            <div class="action-desc">Schedule a customer care welcome touchpoint to verify WiFi coverage and hardware satisfaction. Subscribers in months 0-12 are at peak vulnerability.</div>
        </div>
        """, unsafe_allow_html=True)
        
    if eval_internet == "fiber" and eval_monthly > 70.0 and not eval_sec:
        st.markdown("""
        <div class="action-item">
            <div class="action-title">4. Premium Value-Add Bundling</div>
            <div class="action-desc">Attach ConnectTel Security at zero charge for 6 months to reinforce perceived value without discounting core fiber speed tier pricing.</div>
        </div>
        """, unsafe_allow_html=True)
        
    if not triggers:
        st.markdown("""
        <div class="action-item">
            <div class="action-title">Standard Account Maintenance</div>
            <div class="action-desc">Account is performing healthily. No special discount or retention outreach needed. Maintain regular service notifications.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Methodological Disclaimer Footer
st.markdown("""
<div class="disclaimer-box">
    <strong>Methodological Notice & Synthetic Dataset Limitations:</strong><br>
    This simulation engine utilizes the ConnectTel champion Regularized Logistic Regression pipeline trained strictly on the official Persevex 320-record synthetic teaching dataset.
    Predictions reflect statistical associations within this synthetic teaching distribution and must not be interpreted as guaranteed outcomes or empirical real-world telecom industry benchmarks.
    Model probability outputs are uncalibrated discriminative ranking scores tuned for maximum recall sensitivity (75.0% on test partition).
</div>
""", unsafe_allow_html=True)
