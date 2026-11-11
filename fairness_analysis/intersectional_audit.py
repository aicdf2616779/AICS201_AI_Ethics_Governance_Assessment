
"""
AICS-201: Intersectional Fairness Audit

Evaluates the original simulated decisions and the two
Fairlearn mitigation models across gender-region intersections.

Educational synthetic-data experiment only.
"""

from pathlib import Path

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from fairlearn.metrics import MetricFrame, selection_rate

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/synthetic/securefinance_synthetic_data.csv"
)

output = ROOT / "outputs/reports"
output.mkdir(parents=True, exist_ok=True)

features = [
    "age",
    "monthly_income_ngn",
    "debt_to_income_ratio",
    "credit_history_months",
    "missed_payments_12m",
    "employment_years",
]

X = df[features]
y = df["neutral_approved"]

sensitive = df[["gender", "region_type"]].copy()

sensitive["intersection"] = (
    sensitive["gender"].astype(str)
    + "_"
    + sensitive["region_type"].astype(str)
)

X_train, X_test, y_train, y_test, A_train, A_test, idx_train, idx_test = (
    train_test_split(
        X,
        y,
        sensitive,
        df.index,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
)

original = df.loc[idx_test, "ai_approved"].to_numpy()

results = []

def audit(name, predictions):

    frame = MetricFrame(
        metrics={
            "selection_rate": selection_rate,
            "accuracy": accuracy_score,
        },
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=A_test["intersection"],
    )

    print(f"\n===== {name} =====")
    print(frame.by_group.to_string())

    for group, values in frame.by_group.iterrows():
        results.append({
            "model": name,
            "intersection": group,
            "selection_rate": values["selection_rate"],
            "accuracy": values["accuracy"],
            "sample_count": int(
                (A_test["intersection"] == group).sum()
            ),
        })

audit("Original AI", original)

for attribute in ["gender", "region_type"]:

    model = ExponentiatedGradient(
        estimator=LogisticRegression(max_iter=1000),
        constraints=DemographicParity(),
        eps=0.02,
        max_iter=50,
    )

    model.fit(
        X_train,
        y_train,
        sensitive_features=A_train[attribute],
    )

    predictions = model.predict(
        X_test,
        random_state=42,
    )

    audit(f"Mitigated ({attribute})", predictions)

result_df = pd.DataFrame(results)

result_df.to_csv(
    output / "intersectional_fairness_metrics.csv",
    index=False,
)

print("\n===== INTERSECTIONAL AUDIT SUMMARY =====")
print(result_df.to_string(index=False))

print("\nSaved:")
print(output / "intersectional_fairness_metrics.csv")

print("\nINTERSECTIONAL FAIRNESS AUDIT COMPLETED.")
