"""
Inference Module for Predictive Telecom Customer Churn.
ConnectTel / Persevex AI Internship Project.

Provides a standalone, robust interface for loading the trained champion pipeline
and running real-time or batch inference in downstream applications (e.g. IntelliJ IDEA,
Streamlit dashboard, or REST APIs).
"""

import sys
from pathlib import Path
from typing import Dict, Any, Union, List, Optional
import numpy as np
import pandas as pd
import joblib

# Ensure src directory is in path for pickle deserialization of custom transformers
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from feature_engineering import TelecomFeatureEngineer

DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "best_model_pipeline.joblib"
REQUIRED_FEATURES = [
    "tenure_months",
    "contract",
    "internet_service",
    "monthly_charges_usd",
    "total_charges_usd",
    "security_service",
    "streaming_service",
    "failed_payments_90d"
]

_CACHED_MODEL = None


def load_champion_model(model_path: Optional[Union[str, Path]] = None):
    """
    Load the serialized champion model pipeline with cached reuse.
    Ensures TelecomFeatureEngineer is registered in namespace for unpickling.
    """
    global _CACHED_MODEL
    path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found at {path}")
    if _CACHED_MODEL is None or model_path is not None:
        _CACHED_MODEL = joblib.load(path)
    return _CACHED_MODEL


def validate_customer_input(customer_data: Union[Dict[str, Any], pd.DataFrame]) -> pd.DataFrame:
    """
    Validate and format raw customer input into a clean DataFrame ready for pipeline inference.
    Handles None, empty strings, and missing total_charges for zero-tenure accounts.
    """
    if isinstance(customer_data, dict):
        df = pd.DataFrame([customer_data])
    elif isinstance(customer_data, list):
        df = pd.DataFrame(customer_data)
    elif isinstance(customer_data, pd.DataFrame):
        df = customer_data.copy()
    else:
        raise TypeError(f"Unsupported input type: {type(customer_data)}")

    # Check missing required columns
    missing_cols = [c for c in REQUIRED_FEATURES if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required input features: {missing_cols}")

    # Ensure correct data types
    df["tenure_months"] = pd.to_numeric(df["tenure_months"], errors="coerce").fillna(0).astype(int)
    df["monthly_charges_usd"] = pd.to_numeric(df["monthly_charges_usd"], errors="coerce").fillna(0.0).astype(float)
    df["total_charges_usd"] = pd.to_numeric(df["total_charges_usd"], errors="coerce") # NaNs allowed for zero-tenure
    df["security_service"] = pd.to_numeric(df["security_service"], errors="coerce").fillna(0).astype(int)
    df["streaming_service"] = pd.to_numeric(df["streaming_service"], errors="coerce").fillna(0).astype(int)
    df["failed_payments_90d"] = pd.to_numeric(df["failed_payments_90d"], errors="coerce").fillna(0).astype(int)
    
    # Normalize string categories
    df["contract"] = df["contract"].astype(str).str.strip().str.lower()
    df["internet_service"] = df["internet_service"].astype(str).str.strip().str.lower()

    return df[REQUIRED_FEATURES]


DEFAULT_DECISION_THRESHOLD = 0.55  # Optimal F1 threshold tuned on validation partition (F1=0.4667 vs 0.4516 at 0.50)


def predict_churn(
    customer_data: Union[Dict[str, Any], pd.DataFrame],
    threshold: float = DEFAULT_DECISION_THRESHOLD,
    model: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Execute end-to-end inference on one or more customer records.
    
    Decision Threshold:
    -------------------
    Default threshold is 0.55, established via validation optimization (Phase 2).
    At threshold 0.55, the champion model maintains peak recall (77.8% on validation,
    75.0% on test) while reducing false positives, achieving the highest F1 score.
    
    Returns:
        Dictionary with churn prediction (0 or 1), probability, risk tier,
        and primary rule-based risk triggers.
    """
    pipeline = model if model is not None else load_champion_model()
    df = validate_customer_input(customer_data)
    
    probabilities = pipeline.predict_proba(df)[:, 1]
    
    results = []
    for i, prob in enumerate(probabilities):
        row = df.iloc[i]
        is_churn = int(prob >= threshold)
        
        # Risk tiering
        if prob >= 0.70:
            tier = "Critical"
        elif prob >= 0.45:
            tier = "High"
        elif prob >= 0.25:
            tier = "Medium"
        else:
            tier = "Low"
            
        # Identify top qualitative risk triggers
        triggers = []
        if row["contract"] == "monthly":
            triggers.append("Month-to-Month Contract (high switching flexibility)")
        if row["failed_payments_90d"] >= 1:
            triggers.append(f"{row['failed_payments_90d']} Failed Payment(s) in past 90 days")
        if row["tenure_months"] <= 12:
            triggers.append("Early Tenure Subscriber (onboarding vulnerability)")
        if row["internet_service"] == "fiber" and row["monthly_charges_usd"] > 70:
            triggers.append("Premium Fiber Tier (> $70/mo) without bundled add-ons")
            
        results.append({
            "churn_prediction": is_churn,
            "churn_probability": round(float(prob), 4),
            "retention_probability": round(1.0 - float(prob), 4),
            "decision_threshold": threshold,
            "risk_tier": tier,
            "risk_triggers": triggers
        })
        
    return results[0] if isinstance(customer_data, dict) else {"predictions": results}


if __name__ == "__main__":
    test_record = {
        "tenure_months": 0,
        "contract": "monthly",
        "internet_service": "fiber",
        "monthly_charges_usd": 85.0,
        "total_charges_usd": None,
        "security_service": 0,
        "streaming_service": 1,
        "failed_payments_90d": 2
    }
    output = predict_churn(test_record)
    print("Inference Test Output:")
    for k, v in output.items():
        print(f"  {k}: {v}")
