import math
import pytest

from src.investment_calculator import calculate_investment_metrics


def test_standard_investment_calculation():
    result = calculate_investment_metrics(
        purchase_price_lakhs=50,
        monthly_rent_rupees=25000,
        annual_expenses_rupees=30000,
        one_time_costs_rupees=300000,
        vacancy_rate_pct=5,
        appreciation_rate_pct=5
    )

    assert result["gross_rental_yield_pct"] == 6.00
    assert result["net_rental_yield_pct"] == 4.81
    assert result["monthly_net_cash_flow"] == 21250.0


def test_negative_cash_flow():
    result = calculate_investment_metrics(
        purchase_price_lakhs=50,
        monthly_rent_rupees=10000,
        annual_expenses_rupees=150000
    )

    assert result["net_annual_rent"] < 0
    assert result["monthly_net_cash_flow"] < 0


def test_full_vacancy():
    result = calculate_investment_metrics(
        purchase_price_lakhs=50,
        monthly_rent_rupees=25000,
        vacancy_rate_pct=100
    )

    assert result["effective_annual_rent"] == 0
    assert result["net_annual_rent"] == 0


def test_missing_appreciation_assumption():
    result = calculate_investment_metrics(50, 25000)

    assert result["five_year_scenario_value"] is None


def test_zero_appreciation():
    result = calculate_investment_metrics(
        50, 25000, appreciation_rate_pct=0
    )

    assert result["five_year_scenario_value"] == 5000000


@pytest.mark.parametrize(
    "purchase_price, monthly_rent",
    [
        (0, 25000),
        (-10, 25000),
        (50, -1000),
        (50, math.nan),
        (50, math.inf),
        (50, True),
        ("fifty", 25000)
    ]
)
def test_invalid_inputs(purchase_price, monthly_rent):
    with pytest.raises(ValueError):
        calculate_investment_metrics(
            purchase_price,
            monthly_rent
        )


def test_invalid_vacancy_rate():
    with pytest.raises(ValueError):
        calculate_investment_metrics(
            50, 25000, vacancy_rate_pct=101
        )


def test_invalid_appreciation_rate():
    with pytest.raises(ValueError):
        calculate_investment_metrics(
            50, 25000, appreciation_rate_pct=-100
        )


from src.investment_calculator import compare_appreciation_scenarios


def test_appreciation_scenario_comparison():
    results = compare_appreciation_scenarios(50)

    assert len(results) == 3
    assert results[0]["Scenario"] == "Conservative"
    assert results[1]["Scenario"] == "Moderate"
    assert results[2]["Scenario"] == "Optimistic"

    assert results[0]["Five-Year Scenario Value (₹)"] == 5796370.37
    assert results[1]["Five-Year Scenario Value (₹)"] == 6381407.81
    assert results[2]["Five-Year Scenario Value (₹)"] == 7346640.38


def test_custom_appreciation_scenario():
    results = compare_appreciation_scenarios(
        50,
        {"Custom": 6}
    )

    assert len(results) == 1
    assert results[0]["Scenario"] == "Custom"
    assert results[0]["Annual Appreciation (%)"] == 6


def test_invalid_scenario_purchase_price():
    for price in [0, -10, math.nan, math.inf, True, "fifty"]:
        with pytest.raises(ValueError):
            compare_appreciation_scenarios(price)


def test_invalid_appreciation_scenario_rate():
    for rate in [-100, math.nan, math.inf, True, "five"]:
        with pytest.raises(ValueError):
            compare_appreciation_scenarios(50, {"Invalid": rate})


def test_empty_appreciation_scenarios():
    with pytest.raises(ValueError):
        compare_appreciation_scenarios(50, {})
