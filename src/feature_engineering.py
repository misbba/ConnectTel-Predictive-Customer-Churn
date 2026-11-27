"""
Feature Engineering Module for Predictive Telecom Customer Churn.
ConnectTel / Persevex AI Internship Project.

Includes:
1. Explicit zero-tenure rule transformer (handling missing total_charges_usd and charges-per-tenure).
2. ServiceCount engineer.
3. Domain features: charges_ratio, has_failed_payments, zero_tenure_flag.
4. Scikit-learn compatible Transformer & ColumnTransformer preprocessing pipeline.
5. Strict training-only fitting to prevent data leakage.
"""

from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


class TelecomFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom Scikit-Learn Transformer for Telecom Churn Feature Engineering.
    
    Zero-Tenure and Missing Value Rationale:
    ----------------------------------------
    - Customers with tenure_months == 0 have just signed up on the snapshot date (2025-01-01).
    - They have completed zero billing cycles, so their historical accumulated total_charges_usd
      is logically $0.00 billed to date (or blank in the raw transactional dump).
    - Dividing by zero (total_charges / 0) is undefined and setting the ratio to 0 falsely implies
      a free plan. Thus, our explicit zero-tenure rule assigns:
         charges_per_tenure = monthly_charges_usd (for tenure == 0)
         charges_per_tenure = total_charges_usd / tenure_months (for tenure > 0)
      This represents their true expected monthly billing velocity.
    - Missing total_charges_usd for zero tenure is filled with 0.0 with this explicit domain explanation.
    """
    
    def __init__(self, create_interaction_features: bool = True):
        self.create_interaction_features = create_interaction_features
        self.median_total_charges_ = None
        self.feature_names_out_ = None
        
    def fit(self, X: pd.DataFrame, y=None):
        X_df = X.copy()
        # Learn median total_charges from training data for any unexpected non-zero tenure NaNs
        non_zero_tenure = X_df[X_df["tenure_months"] > 0]
        self.median_total_charges_ = non_zero_tenure["total_charges_usd"].median()
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        
        # 1. Audit and impute total_charges_usd with explicit domain rule
        # Zero-tenure accounts have 0 cumulative historical billing
        is_zero_tenure = X_out["tenure_months"] == 0
        X_out["is_zero_tenure"] = is_zero_tenure.astype(int)
        
        # Impute total_charges: 0.0 for zero tenure, median for any other unexpected NaN
        X_out.loc[is_zero_tenure & X_out["total_charges_usd"].isnull(), "total_charges_usd"] = 0.0
        if X_out["total_charges_usd"].isnull().any():
            X_out["total_charges_usd"] = X_out["total_charges_usd"].fillna(self.median_total_charges_)
            
        # 2. TotalChargesPerTenure (Safe computation with explicit zero-tenure rule)
        # For tenure == 0, billing rate is monthly_charges_usd; for tenure > 0, ratio of total to tenure
        charges_per_tenure = np.where(
            X_out["tenure_months"] == 0,
            X_out["monthly_charges_usd"].astype(float),
            X_out["total_charges_usd"] / np.maximum(X_out["tenure_months"], 1)
        )
        X_out["total_charges_per_tenure"] = charges_per_tenure
        
        # 3. ServiceCount (security_service + streaming_service)
        X_out["service_count"] = X_out["security_service"] + X_out["streaming_service"]
        
        # 4. Domain & behavioral features
        if self.create_interaction_features:
            # Payment distress flag
            X_out["has_failed_payments"] = (X_out["failed_payments_90d"] > 0).astype(int)
            # Velocity ratio: actual monthly rate relative to stated monthly charges
            # Detects fee escalation or expired promotions
            eps = 1e-5
            X_out["charges_velocity_ratio"] = (
                X_out["total_charges_per_tenure"] / (X_out["monthly_charges_usd"] + eps)
            )
            # Fiber high charge indicator
            is_fiber = (X_out["internet_service"] == "fiber").astype(int)
            X_out["fiber_high_charge"] = (
                is_fiber * (X_out["monthly_charges_usd"] > 70).astype(int)
            )
            
        self.feature_names_out_ = list(X_out.columns)
        return X_out

    def get_feature_names_out(self, input_features=None):
        if self.feature_names_out_ is not None:
            return np.array(self.feature_names_out_, dtype=object)
        if input_features is not None:
            return np.array(input_features, dtype=object)
        return np.array([], dtype=object)


def build_preprocessor_pipeline(categorical_cols: List[str], numerical_cols: List[str]) -> ColumnTransformer:
    """
    Build Scikit-Learn ColumnTransformer for scaling numerical features
    and one-hot encoding categorical variables.
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols)
        ],
        remainder="passthrough"
    )
    return preprocessor


def get_full_feature_pipeline() -> Tuple[Pipeline, List[str], List[str]]:
    """
    Returns full preprocessing pipeline combining feature engineering
    and ColumnTransformer scaling/encoding.
    """
    num_cols = [
        "tenure_months", "monthly_charges_usd", "total_charges_usd",
        "total_charges_per_tenure", "service_count", "failed_payments_90d",
        "charges_velocity_ratio"
    ]
    cat_cols = ["contract", "internet_service"]
    # Binary columns passed through
    
    col_preprocessor = build_preprocessor_pipeline(cat_cols, num_cols)
    
    pipeline = Pipeline([
        ("feature_engineer", TelecomFeatureEngineer()),
        ("preprocessor", col_preprocessor)
    ])
    
    return pipeline, num_cols, cat_cols


def engineer_features_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function that transforms a raw DataFrame into an enriched DataFrame
    with all engineered columns.
    """
    fe = TelecomFeatureEngineer()
    fe.fit(df)
    return fe.transform(df)


if __name__ == "__main__":
    from data_loader import load_raw_data, get_splits
    
    df = load_raw_data()
    X_train, y_train, X_val, y_val, X_test, y_test = get_splits(df)
    
    fe = TelecomFeatureEngineer()
    fe.fit(X_train)
    X_train_fe = fe.transform(X_train)
    X_val_fe = fe.transform(X_val)
    
    print("Feature Engineering Verification:")
    print("Original feature count:", X_train.shape[1])
    print("Engineered feature count:", X_train_fe.shape[1])
    print("\nNew engineered columns:")
    for col in X_train_fe.columns:
        if col not in X_train.columns:
            print(f"  + {col} (dtype: {X_train_fe[col].dtype})")
            
    print("\nZero-tenure row check in X_train_fe:")
    zero_rows = X_train_fe[X_train_fe["tenure_months"] == 0]
    print(zero_rows[[
        "tenure_months", "monthly_charges_usd", "total_charges_usd",
        "total_charges_per_tenure", "service_count", "is_zero_tenure"
    ]])
    
    # Test full sklearn pipeline fit on train only
    pipe, num_c, cat_c = get_full_feature_pipeline()
    pipe.fit(X_train)
    X_train_proc = pipe.transform(X_train)
    X_val_proc = pipe.transform(X_val)
    print(f"\nPipeline Transformed Shapes:")
    print(f"  Train transformed matrix shape: {X_train_proc.shape}")
    print(f"  Validation transformed matrix shape: {X_val_proc.shape}")
    print("Pipeline fitted strictly on training data: VERIFIED.")
