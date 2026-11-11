
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_synthetic_dataset_exists_and_is_readable():
    path = ROOT / "data/synthetic/securefinance_synthetic_data.csv"
    assert path.exists()
    data = pd.read_csv(path)
    assert not data.empty

    required_columns = {
        "gender",
        "region_type",
        "ai_approved",
        "neutral_approved",
    }
    assert required_columns.issubset(data.columns)


def test_synthetic_dataset_has_expected_groups():
    path = ROOT / "data/synthetic/securefinance_synthetic_data.csv"
    data = pd.read_csv(path)

    assert set(data["gender"].dropna().unique()) == {"Female", "Male"}
    assert set(data["region_type"].dropna().unique()) == {"Rural", "Urban"}


def test_fairness_outputs_exist_and_are_readable():
    files = [
        "outputs/reports/fairness_metrics_by_group.csv",
        "outputs/reports/fairness_summary.csv",
        "outputs/reports/bias_mitigation_comparison.csv",
        "outputs/reports/intersectional_fairness_metrics.csv",
    ]

    for filename in files:
        path = ROOT / filename
        assert path.exists(), f"Missing: {filename}"
        result = pd.read_csv(path)
        assert not result.empty, f"Empty output: {filename}"


def test_intersectional_audit_covers_four_groups():
    path = ROOT / "outputs/reports/intersectional_fairness_metrics.csv"
    data = pd.read_csv(path)

    expected_groups = {
        "Female_Rural",
        "Female_Urban",
        "Male_Rural",
        "Male_Urban",
    }

    assert expected_groups.issubset(set(data["intersection"]))
    assert data["sample_count"].gt(0).all()
    assert data["selection_rate"].between(0, 1).all()
    assert data["accuracy"].between(0, 1).all()


def test_governance_and_compliance_documents_exist():
    required_files = [
        "risk_assessment/ai_risk_register.csv",
        "legal_compliance/compliance_matrix.csv",
        "docs/AI_GOVERNANCE_FRAMEWORK.md",
        "legal_compliance/legal_compliance_assessment.md",
    ]

    for filename in required_files:
        path = ROOT / filename
        assert path.exists(), f"Missing: {filename}"
        assert path.stat().st_size > 0, f"Empty: {filename}"


def test_key_figures_exist():
    figures = [
        "outputs/figures/approval_rates_by_gender.png",
        "outputs/figures/approval_rates_by_region_type.png",
        "outputs/figures/shap_summary_plot.png",
        "outputs/figures/shap_feature_importance.png",
        "outputs/figures/bias_mitigation_comparison.png",
    ]

    for filename in figures:
        path = ROOT / filename
        assert path.exists(), f"Missing figure: {filename}"
        assert path.stat().st_size > 0, f"Empty figure: {filename}"
