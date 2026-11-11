
"""
AICS-201: SecureFinance Africa
SHAP Explainability Assessment

This is an educational surrogate model.
It approximates the deliberately biased simulated AI decisions.
It is not a production credit-risk model.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import shap

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# 1. Paths and data loading
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data/synthetic/securefinance_synthetic_data.csv"
OUTPUT_DIR = ROOT / "outputs/reports"
FIGURE_DIR = ROOT / "outputs/figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

print("=" * 65)
print("SECUREFINANCE AFRICA - SHAP EXPLAINABILITY ASSESSMENT")
print("=" * 65)

# --------------------------------------------------
# 2. Prepare model features
# --------------------------------------------------

features = [
    "age",
    "gender",
    "region_type",
    "monthly_income_ngn",
    "debt_to_income_ratio",
    "credit_history_months",
    "missed_payments_12m",
    "employment_years",
]

X = df[features].copy()
y = df["ai_approved"]

# Encode categorical variables.
X = pd.get_dummies(
    X,
    columns=["gender", "region_type"],
    dtype=int
)

# --------------------------------------------------
# 3. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# 4. Train surrogate Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=6,
    min_samples_leaf=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== SURROGATE MODEL PERFORMANCE =====")
print(f"Test accuracy: {accuracy:.4f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# --------------------------------------------------
# 5. Calculate SHAP values
# --------------------------------------------------

print("\nCalculating SHAP values...")

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X_test)

# Handle different SHAP output formats.
if isinstance(shap_values, list):
    values = shap_values[1]
else:
    values = np.asarray(shap_values)

    if values.ndim == 3:
        values = values[:, :, 1]

# --------------------------------------------------
# 6. Calculate global feature importance
# --------------------------------------------------

importance = pd.DataFrame({
    "feature": X_test.columns,
    "mean_absolute_shap": np.abs(values).mean(axis=0)
})

importance = importance.sort_values(
    "mean_absolute_shap",
    ascending=False
)

importance.to_csv(
    OUTPUT_DIR / "shap_feature_importance.csv",
    index=False
)

print("\n===== SHAP FEATURE IMPORTANCE =====")
print(importance.to_string(index=False))

# --------------------------------------------------
# 7. Generate SHAP summary plot
# --------------------------------------------------

plt.figure()

shap.summary_plot(
    values,
    X_test,
    show=False,
    plot_size=(10, 7)
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "shap_summary_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 8. Generate SHAP feature importance chart
# --------------------------------------------------

plt.figure(figsize=(10, 6))

top_features = importance.head(10).sort_values(
    "mean_absolute_shap"
)

plt.barh(
    top_features["feature"],
    top_features["mean_absolute_shap"]
)

plt.xlabel("Mean Absolute SHAP Value")
plt.ylabel("Feature")
plt.title("Top 10 Features Influencing AI Approval")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "shap_feature_importance.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 9. Save model evaluation
# --------------------------------------------------

with open(
    OUTPUT_DIR / "shap_model_evaluation.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("AICS-201 SHAP MODEL EVALUATION\n")
    file.write("=" * 45 + "\n")
    file.write(f"Surrogate test accuracy: {accuracy:.4f}\n\n")
    file.write(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

print("\n===== GENERATED FILES =====")
print(OUTPUT_DIR / "shap_feature_importance.csv")
print(OUTPUT_DIR / "shap_model_evaluation.txt")
print(FIGURE_DIR / "shap_summary_plot.png")
print(FIGURE_DIR / "shap_feature_importance.png")

print("\nSHAP EXPLAINABILITY ANALYSIS COMPLETED.")
print("=" * 65)
