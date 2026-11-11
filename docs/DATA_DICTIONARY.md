
# SecureFinance Africa – Synthetic Dataset Dictionary

## Dataset Information

- File: securefinance_synthetic_data.csv
- Records: 1,200
- Columns: 13
- Format: CSV
- Random seed: 42
- Data classification: Synthetic / Fictional

## Field Definitions

| Field | Description |
|---|---|
| customer_id | Fictional applicant identifier |
| age | Applicant age |
| gender | Synthetic gender group |
| region_type | Urban or rural classification |
| monthly_income_ngn | Monthly income in NGN |
| debt_to_income_ratio | Debt burden ratio |
| credit_history_months | Credit history duration |
| missed_payments_12m | Missed payments over 12 months |
| employment_years | Employment duration |
| neutral_score | Score based on financial indicators |
| ai_score | Simulated AI score with controlled group penalties |
| neutral_approved | Neutral baseline decision |
| ai_approved | Simulated AI decision |

## Ethical Considerations

Gender and region are retained for fairness auditing.

The simulated AI score deliberately incorporates group-based
penalties to create a controlled discrimination scenario.

These penalties are artificial and are not evidence of
real-world discrimination.

## Limitations

The dataset is synthetic and does not represent actual
customers, real financial behaviour or a validated lending model.

The experiment demonstrates fairness auditing methods only.
