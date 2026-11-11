
"""
AICS-201: SecureFinance Africa
AI Bias Mitigation Experiment

Uses Fairlearn ExponentiatedGradient with Demographic Parity.

Two separate mitigation experiments are performed:
1. Gender-constrained mitigation.
2. Region-constrained mitigation.

The target is neutral_approved, a synthetic reference label.
Sensitive attributes are used for fairness constraints and auditing,
not as financial decision features.
"""

from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, accuracy_score


# --------------------------------------------------
# 1. Load dataset and configure output directories
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data/synthetic/securefinance_synthetic_data.csv"
OUTPUT_DIR = ROOT / "outputs/reports"
FIGURE_DIR = ROOT / "outputs/figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("SECUREFINANCE AFRICA - AI BIAS MITIGATION")
print("=" * 70)


# --------------------------------------------------
# 2. Prepare legitimate financial features
# --------------------------------------------------

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

# Sensitive attributes are kept separate.
sensitive = df[["gender", "region_type"]]


# --------------------------------------------------
# 3. Create reproducible training and testing sets
# --------------------------------------------------

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

# Original simulated AI decisions on the same test records.
original_predictions = df.loc[idx_test, "ai_approved"].to_numpy()


# --------------------------------------------------
# 4. Define fairness evaluation function
# --------------------------------------------------

def evaluate_predictions(
    model_name,
    predictions,
    audit_attribute,
    sensitive_values,
):

    frame = MetricFrame(
        metrics={
            "selection_rate": selection_rate,
            "true_positive_rate": recall_score,
        },
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=sensitive_values,
    )

    dp_difference = demographic_parity_difference(
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=sensitive_values,
    )

    dp_ratio = demographic_parity_ratio(
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=sensitive_values,
    )

    tpr_difference = (
        frame.by_group["true_positive_rate"].max()
        - frame.by_group["true_positive_rate"].min()
    )

    result = {
        "model": model_name,
        "audit_attribute": audit_attribute,
        "accuracy_vs_neutral_baseline": accuracy_score(
            y_test, predictions
        ),
        "demographic_parity_difference": dp_difference,
        "demographic_parity_ratio": dp_ratio,
        "equal_opportunity_difference": tpr_difference,
    }

    print(f"\n===== {model_name.upper()} / {audit_attribute.upper()} =====")
    print(frame.by_group.to_string())
    print(f"Demographic parity difference: {dp_difference:.4f}")
    print(f"Demographic parity ratio: {dp_ratio:.4f}")
    print(f"Equal opportunity difference: {tpr_difference:.4f}")
    print(f"Accuracy versus reference: {result['accuracy_vs_neutral_baseline']:.4f}")

    return result


# --------------------------------------------------
# 5. Evaluate original simulated AI decisions
# --------------------------------------------------

results = []

for attribute in ["gender", "region_type"]:

    results.append(
        evaluate_predictions(
            "Original AI",
            original_predictions,
            attribute,
            A_test[attribute],
        )
    )


# --------------------------------------------------
# 6. Train separate constrained models
# --------------------------------------------------

mitigated_predictions = {}

for constraint_attribute in ["gender", "region_type"]:

    print(
        f"\n===== MITIGATION CONSTRAINT: "
        f"{constraint_attribute.upper()} ====="
    )

    mitigation_model = ExponentiatedGradient(
        estimator=LogisticRegression(max_iter=1000),
        constraints=DemographicParity(),
        eps=0.02,
        max_iter=50,
    )

    mitigation_model.fit(
        X_train,
        y_train,
        sensitive_features=A_train[constraint_attribute],
    )

    predictions = mitigation_model.predict(
        X_test,
        random_state=42,
    )

    mitigated_predictions[constraint_attribute] = predictions

    print("Mitigation model training completed.")

    # Evaluate against BOTH protected attributes.
    for audit_attribute in ["gender", "region_type"]:

        results.append(
            evaluate_predictions(
                f"Mitigated ({constraint_attribute})",
                predictions,
                audit_attribute,
                A_test[audit_attribute],
            )
        )


# --------------------------------------------------
# 7. Export results
# --------------------------------------------------

results_df = pd.DataFrame(results)

output_file = OUTPUT_DIR / "bias_mitigation_comparison.csv"

results_df.to_csv(output_file, index=False)

print("\n===== BEFORE AND AFTER COMPARISON =====")
print(results_df.to_string(index=False))


# --------------------------------------------------
# 8. Generate demographic parity ratio chart
# --------------------------------------------------

plot_data = results_df.pivot(
    index="model",
    columns="audit_attribute",
    values="demographic_parity_ratio",
)

ax = plot_data.plot(
    kind="bar",
    figsize=(11, 6),
)

ax.axhline(
    y=0.80,
    linestyle="--",
    label="0.80 screening reference",
)

ax.set_title("Demographic Parity Ratio: Before and After Mitigation")
ax.set_ylabel("Demographic Parity Ratio")
ax.set_xlabel("Decision model")
ax.set_ylim(0, 1.1)
ax.legend()

plt.xticks(rotation=15, ha="right")
plt.tight_layout()

chart_file = FIGURE_DIR / "bias_mitigation_comparison.png"

plt.savefig(chart_file, dpi=300)
plt.close()


# --------------------------------------------------
# 9. Save experiment methodology
# --------------------------------------------------

methodology_file = OUTPUT_DIR / "bias_mitigation_methodology.txt"

with open(methodology_file, "w", encoding="utf-8") as file:

    file.write("AICS-201 BIAS MITIGATION EXPERIMENT\n")
    file.write("=" * 50 + "\n")
    file.write("Algorithm: Fairlearn ExponentiatedGradient\n")
    file.write("Constraint: DemographicParity\n")
    file.write("Reference: Synthetic neutral_approved labels\n")
    file.write("Financial features only: Yes\n")
    file.write("Gender-constrained model: Yes\n")
    file.write("Region-constrained model: Yes\n")
    file.write("Evaluation: Held-out test dataset\n")
    file.write("Test size: 25 percent\n")
    file.write("Random state: 42\n")
    file.write(
        "Note: This is an educational simulation, not a "
        "production lending model.\n"
    )


# --------------------------------------------------
# 10. Final output
# --------------------------------------------------

print("\n===== GENERATED FILES =====")
print(output_file)
print(chart_file)
print(methodology_file)

print("\nBIAS MITIGATION EXPERIMENT COMPLETED.")
print("=" * 70)
