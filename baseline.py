"""
Baseline Model for Predictive Telecom Customer Churn.
ConnectTel / Persevex AI Internship Project.

This module improves upon the original starter baseline.py while strictly preserving
the original model's empirical Bayes smoothed contract prior logic and evaluation results.

Algorithm:
- Base churn rate on training set: base = (churn_train + 1) / (N_train + 2)
- Empirical Bayes contract smoothed probability:
    P(churn | contract = c) = (churn_c + 5 * base) / (N_c + 5)
- Constant base rate baseline:
    P(churn) = base (for all customers)
"""

from pathlib import Path
import csv
import json
import math
from typing import Dict, List, Any

BASE = Path(__file__).resolve().parent


def load(name: str) -> List[Dict[str, Any]]:
    """Load CSV dataset into a list of row dictionaries."""
    with (BASE / "data" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(name: str, rows: List[Dict[str, Any]]) -> None:
    """Save row dictionaries to CSV."""
    with (BASE / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


class ContractGroupBaseline:
    """
    Contract-Group Empirical Bayes Smoothed Probability Baseline.
    Preserves exact formula from starter baseline.py.
    """
    def __init__(self, m_weight: float = 5.0):
        self.m_weight = m_weight
        self.base_rate: float = 0.0
        self.contract_probs: Dict[str, float] = {}

    def fit(self, train_rows: List[Dict[str, Any]]) -> "ContractGroupBaseline":
        n_train = len(train_rows)
        churn_train = sum(int(r["churn_30d"]) for r in train_rows)
        # Laplace-smoothed global prior
        self.base_rate = (churn_train + 1) / (n_train + 2)
        
        contracts = {r["contract"] for r in train_rows}
        self.contract_probs = {}
        for c in contracts:
            group = [r for r in train_rows if r["contract"] == c]
            g_churn = sum(int(r["churn_30d"]) for r in group)
            # Empirical Bayes smoothing towards base_rate with weight m_weight
            prob = (g_churn + self.m_weight * self.base_rate) / (len(group) + self.m_weight)
            self.contract_probs[c] = prob
        return self

    def predict_proba(self, contract: str) -> float:
        return self.contract_probs.get(contract, self.base_rate)


def evaluate_split(
    rows: List[Dict[str, Any]],
    baseline_model: ContractGroupBaseline
) -> Dict[str, Any]:
    """Calculate Brier score and comparison with constant base rate."""
    n = len(rows)
    if n == 0:
        return {}
    actuals = [int(r["churn_30d"]) for r in rows]
    churn_count = sum(actuals)
    
    # Contract group predictions
    preds = [baseline_model.predict_proba(r["contract"]) for r in rows]
    brier_score = sum((p - y) ** 2 for p, y in zip(preds, actuals)) / n
    
    # Constant base rate predictions (as requested in README Task 3)
    const_preds = [baseline_model.base_rate] * n
    const_brier = sum((p - y) ** 2 for p, y in zip(const_preds, actuals)) / n
    
    # Brier skill score relative to constant base rate
    brier_skill_score = 1.0 - (brier_score / (const_brier + 1e-12))
    
    return {
        "n": n,
        "churn_count": churn_count,
        "churn_rate": churn_count / n,
        "brier_score": brier_score,
        "constant_base_brier_score": const_brier,
        "brier_skill_score": brier_skill_score
    }


def main():
    rows = load("customers.csv")
    train = [r for r in rows if r["split"] == "train"]
    
    # Fit baseline model
    model = ContractGroupBaseline()
    model.fit(train)
    
    print("Baseline Model Fitted:")
    print(f"  Global Base Rate: {model.base_rate:.4f}")
    for c, p in sorted(model.contract_probs.items()):
        print(f"  P(Churn | contract={c}): {p:.4f}")
        
    # Generate predictions for all rows (backward compatible)
    pred_rows = [
        {"customer_id": r["customer_id"], "churn_probability": model.predict_proba(r["contract"])}
        for r in rows
    ]
    save("predictions.csv", pred_rows)
    
    # Evaluate validation and test splits
    metrics = {}
    for split in ["validation", "test"]:
        g = [r for r in rows if r["split"] == split]
        metrics[split] = evaluate_split(g, model)
        
    # Save standard metrics.json (backward compatible format)
    compat_metrics = {
        s: {
            "n": metrics[s]["n"],
            "churn_count": metrics[s]["churn_count"],
            "brier_score": metrics[s]["brier_score"]
        }
        for s in ["validation", "test"]
    }
    (BASE / "metrics.json").write_text(json.dumps(compat_metrics, indent=2))
    
    # Save full metrics including skill score
    (BASE / "outputs" / "baseline_evaluation_full.json").write_text(
        json.dumps(metrics, indent=2)
    )
    
    print("\nEvaluation Results:")
    for split, m in metrics.items():
        print(f"  {split.upper()}: N={m['n']}, Churn={m['churn_count']}, Brier={m['brier_score']:.6f}, Skill Score={m['brier_skill_score']:.4f}")
    print("\nSaved predictions.csv and metrics.json (preserved baseline compatibility).")


if __name__ == "__main__":
    main()
