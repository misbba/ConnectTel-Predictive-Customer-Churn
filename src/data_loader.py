"""
Data Loader Module for Predictive Telecom Customer Churn.
ConnectTel / Persevex AI Internship Project.

Handles:
- Loading raw customers.csv
- Schema validation & zero-tenure audit
- Predefined split separation (Train: 192, Validation: 64, Test: 64)
- Strict Data Leakage Prevention (excluding metadata & target from X)
"""

from pathlib import Path
from typing import Dict, Tuple, List, Optional
import pandas as pd
import numpy as np

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.csv"
LEAKAGE_COLUMNS = ["customer_id", "snapshot_date", "split"]
TARGET_COLUMN = "churn_30d"


def load_raw_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """
    Load raw customers.csv and validate essential schema.
    """
    path = Path(filepath) if filepath else DEFAULT_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    df = pd.read_csv(path)
    
    # Expected columns check
    expected_cols = [
        "customer_id", "snapshot_date", "tenure_months", "contract",
        "internet_service", "monthly_charges_usd", "total_charges_usd",
        "security_service", "streaming_service", "failed_payments_90d",
        "churn_30d", "split"
    ]
    missing_cols = [c for c in expected_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")
        
    return df


def audit_dataset(df: pd.DataFrame) -> Dict:
    """
    Audit data characteristics, missing values, zero-tenure rows, and class balance.
    """
    total_rows = len(df)
    missing_by_col = df.isnull().sum().to_dict()
    
    zero_tenure = df[df["tenure_months"] == 0]
    zero_tenure_missing_charges = zero_tenure["total_charges_usd"].isnull().sum()
    
    split_counts = df["split"].value_counts().to_dict()
    
    churn_rates = {}
    for s in ["train", "validation", "test"]:
        sub = df[df["split"] == s]
        if len(sub) > 0:
            churn_rates[s] = {
                "n": len(sub),
                "churn_count": int(sub[TARGET_COLUMN].sum()),
                "churn_rate": float(sub[TARGET_COLUMN].mean())
            }
            
    return {
        "total_records": total_rows,
        "missing_values": missing_by_col,
        "zero_tenure_count": len(zero_tenure),
        "zero_tenure_missing_charges": int(zero_tenure_missing_charges),
        "splits": split_counts,
        "churn_rates_by_split": churn_rates
    }


def get_splits(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    leakage_cols: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Extract Train, Validation, and Test feature matrices and target vectors.
    Strictly removes leakage columns (customer_id, snapshot_date, split, and target).
    
    Returns:
        (X_train, y_train, X_val, y_val, X_test, y_test)
    """
    if leakage_cols is None:
        leakage_cols = LEAKAGE_COLUMNS
        
    # Validation of split integrity
    required_splits = {"train", "validation", "test"}
    present_splits = set(df["split"].unique())
    if not required_splits.issubset(present_splits):
        raise ValueError(f"Dataset missing required splits. Present: {present_splits}")
        
    train_mask = df["split"] == "train"
    val_mask = df["split"] == "validation"
    test_mask = df["split"] == "test"
    
    features_to_drop = list(set(leakage_cols + [target_col]))
    
    X_train = df.loc[train_mask].drop(columns=features_to_drop).copy()
    y_train = df.loc[train_mask, target_col].copy()
    
    X_val = df.loc[val_mask].drop(columns=features_to_drop).copy()
    y_val = df.loc[val_mask, target_col].copy()
    
    X_test = df.loc[test_mask].drop(columns=features_to_drop).copy()
    y_test = df.loc[test_mask, target_col].copy()
    
    return X_train, y_train, X_val, y_val, X_test, y_test


if __name__ == "__main__":
    raw_df = load_raw_data()
    audit = audit_dataset(raw_df)
    print("Dataset Audit Summary:")
    for k, v in audit.items():
        print(f"  {k}: {v}")
        
    X_tr, y_tr, X_v, y_v, X_te, y_te = get_splits(raw_df)
    print(f"\nSplits extracted successfully:")
    print(f"  Train:      X={X_tr.shape}, y={y_tr.shape}")
    print(f"  Validation: X={X_v.shape}, y={y_v.shape}")
    print(f"  Test:       X={X_te.shape}, y={y_te.shape}")
    print(f"  Features:   {list(X_tr.columns)}")
