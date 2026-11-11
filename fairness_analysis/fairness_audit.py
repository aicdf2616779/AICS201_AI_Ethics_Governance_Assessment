
"""
AICS-201: SecureFinance Africa
Algorithmic Fairness Audit

Uses synthetic data only.

The neutral_approved decision is used as a proxy reference
for assessing the effect of the simulated AI decision process.
It is NOT a verified real-world outcome.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
)
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score


# --------------------------------------------------
# 1. Paths and dataset loading
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data/synthetic/securefinance_synthetic_data.csv"
OUTPUT_DIR = ROOT / "outputs/reports"
FIGURE_DIR = ROOT / "outputs/figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

y_true = df["neutral_approved"]
y_pred = df["ai_approved"]


# --------------------------------------------------
# 2. Define fairness metrics
# --------------------------------------------------

def sample_count(y_true, y_pred):
    return len(y_true)


metrics = {
    "selection_rate": selection_rate,
    "true_positive_rate": recall_score,
    "sample_count": sample_count,
}


# --------------------------------------------------
# 3. Audit each protected attribute separately
# --------------------------------------------------

summary_results = []
group_results = []

protected_attributes = ["gender", "region_type"]

print("=" * 65)
print("SECUREFINANCE AFRICA - ALGORITHMIC FAIRNESS AUDIT")
print("=" * 65)

for attribute in protected_attributes:

    groups = df[attribute]

    frame = MetricFrame(
        metrics=metrics,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=groups,
    )

    group_metrics = frame.by_group.copy()

    dp_difference = demographic_parity_difference(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=groups,
    )

    dp_ratio = demographic_parity_ratio(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=groups,
    )

    # Equal opportunity difference:
    # Difference between the highest and lowest group TPR.
    tpr_difference = (
        group_metrics["true_positive_rate"].max()
        - group_metrics["true_positive_rate"].min()
    )

    # Add group identifier
    group_metrics = group_metrics.reset_index()
    group_metrics.insert(0, "protected_attribute", attribute)

    group_results.append(group_metrics)

    summary_results.append({
        "protected_attribute": attribute,
        "demographic_parity_difference": dp_difference,
        "demographic_parity_ratio": dp_ratio,
        "equal_opportunity_difference": tpr_difference,
        "overall_ai_accuracy_vs_baseline": accuracy_score(
            y_true, y_pred
        ),
    })

    print(f"\n===== FAIRNESS AUDIT: {attribute.upper()} =====")

    print("\nGroup metrics:")
    print(group_metrics.to_string(index=False))

    print(f"\nDemographic parity difference: {dp_difference:.4f}")
    print(f"Demographic parity ratio: {dp_ratio:.4f}")
    print(f"Equal opportunity difference: {tpr_difference:.4f}")


# --------------------------------------------------
# 4. Export fairness results
# --------------------------------------------------

group_output = pd.concat(group_results, ignore_index=True)

summary_output = pd.DataFrame(summary_results)

group_output.to_csv(
    OUTPUT_DIR / "fairness_metrics_by_group.csv",
    index=False
)

summary_output.to_csv(
    OUTPUT_DIR / "fairness_summary.csv",
    index=False
)


# --------------------------------------------------
# 5. Generate selection-rate charts
# --------------------------------------------------

for attribute in protected_attributes:

    rates = df.groupby(attribute)["ai_approved"].mean()

    plt.figure(figsize=(8, 5))

    rates.plot(kind="bar")

    plt.title(f"AI Approval Rates by {attribute.replace('_', ' ').title()}")
    plt.xlabel(attribute.replace("_", " ").title())
    plt.ylabel("Approval Rate")

    plt.ylim(0, 1)
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = (
        FIGURE_DIR / f"approval_rates_by_{attribute}.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"\nChart saved: {output_path}")


# --------------------------------------------------
# 6. Confusion matrix
# --------------------------------------------------

cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

print("\n===== CONFUSION MATRIX =====")
print(cm)

print("\n===== OVERALL ACCURACY =====")
print(f"{accuracy_score(y_true, y_pred):.4f}")

print("\n===== FAIRNESS SUMMARY =====")
print(summary_output.to_string(index=False))

print("\n===== OUTPUT FILES =====")
print(OUTPUT_DIR / "fairness_metrics_by_group.csv")
print(OUTPUT_DIR / "fairness_summary.csv")

print("\nFAIRNESS AUDIT COMPLETED.")
print("=" * 65)
