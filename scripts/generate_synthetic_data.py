
"""
AICS-201: SecureFinance Africa
Synthetic Financial Dataset Generator

Purpose:
Generate fictional financial applicant records for AI fairness,
ethics, governance and explainability assessment.

No real customer information is used.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# Reproducibility
RANDOM_SEED = 42
NUMBER_OF_RECORDS = 1200

rng = np.random.default_rng(RANDOM_SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 1. Generate fictional customer characteristics
# --------------------------------------------------

customer_id = [
    f"SFA-{i:05d}"
    for i in range(1, NUMBER_OF_RECORDS + 1)
]

age = rng.integers(21, 66, NUMBER_OF_RECORDS)

gender = rng.choice(
    ["Female", "Male"],
    NUMBER_OF_RECORDS
)

region_type = rng.choice(
    ["Urban", "Rural"],
    NUMBER_OF_RECORDS,
    p=[0.60, 0.40]
)

monthly_income = rng.normal(
    250000, 85000, NUMBER_OF_RECORDS
)

monthly_income = np.clip(
    monthly_income, 60000, 800000
).round(2)

debt_ratio = rng.beta(
    2, 5, NUMBER_OF_RECORDS
)

debt_ratio = np.clip(
    debt_ratio, 0.02, 0.95
).round(3)

credit_history = rng.integers(
    3, 181, NUMBER_OF_RECORDS
)

missed_payments = rng.poisson(
    0.8, NUMBER_OF_RECORDS
)

missed_payments = np.clip(
    missed_payments, 0, 8
)

employment_years = np.minimum(
    rng.gamma(2.5, 2.5, NUMBER_OF_RECORDS),
    np.maximum(age - 18, 0)
)

employment_years = employment_years.round(1)

# --------------------------------------------------
# 2. Calculate standardised financial indicators
# --------------------------------------------------

def standardise(values):
    return (
        values - np.mean(values)
    ) / np.std(values)


income_z = standardise(monthly_income)
debt_z = standardise(debt_ratio)
history_z = standardise(credit_history)
missed_z = standardise(missed_payments)
employment_z = standardise(employment_years)

# --------------------------------------------------
# 3. Calculate neutral financial assessment score
# --------------------------------------------------

neutral_score = (
    0.80 * income_z
    - 0.90 * debt_z
    + 0.60 * history_z
    - 0.80 * missed_z
    + 0.30 * employment_z
)

# Neutral decision uses financial indicators only.
neutral_approved = (
    neutral_score >= 0.0
).astype(int)

# --------------------------------------------------
# 4. Simulate controlled discriminatory effects
# --------------------------------------------------

gender_penalty = np.where(
    gender == "Female", 0.55, 0.0
)

region_penalty = np.where(
    region_type == "Rural", 0.25, 0.0
)

ai_score = (
    neutral_score
    - gender_penalty
    - region_penalty
)

ai_approved = (
    ai_score >= 0.0
).astype(int)

# --------------------------------------------------
# 5. Construct the dataset
# --------------------------------------------------

df = pd.DataFrame({
    "customer_id": customer_id,
    "age": age,
    "gender": gender,
    "region_type": region_type,
    "monthly_income_ngn": monthly_income,
    "debt_to_income_ratio": debt_ratio,
    "credit_history_months": credit_history,
    "missed_payments_12m": missed_payments,
    "employment_years": employment_years,
    "neutral_score": neutral_score.round(4),
    "ai_score": ai_score.round(4),
    "neutral_approved": neutral_approved,
    "ai_approved": ai_approved
})

# --------------------------------------------------
# 6. Export synthetic dataset
# --------------------------------------------------

output_file = OUTPUT_DIR / "securefinance_synthetic_data.csv"

df.to_csv(output_file, index=False)

# --------------------------------------------------
# 7. Generate dataset summary
# --------------------------------------------------

print("=" * 60)
print("SECUREFINANCE AFRICA - SYNTHETIC DATA GENERATION")
print("=" * 60)

print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print("\nGender distribution:")
print(df["gender"].value_counts())

print("\nRegion distribution:")
print(df["region_type"].value_counts())

print("\nNeutral approval rate:")
print(f"{df['neutral_approved'].mean():.2%}")

print("\nSimulated AI approval rate:")
print(f"{df['ai_approved'].mean():.2%}")

print("\nAI approval rate by gender:")
print(df.groupby("gender")["ai_approved"].mean().round(4))

print("\nAI approval rate by region:")
print(df.groupby("region_type")["ai_approved"].mean().round(4))

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nDataset saved successfully:")
print(output_file)

print("=" * 60)
