import math


def calculate_investment_metrics(
    purchase_price_lakhs,
    monthly_rent_rupees,
    annual_expenses_rupees=0,
    one_time_costs_rupees=0,
    vacancy_rate_pct=0,
    appreciation_rate_pct=None
):
    """Calculate rental yields, cash flow, and a five-year scenario."""

    inputs = {
        "purchase_price_lakhs": purchase_price_lakhs,
        "monthly_rent_rupees": monthly_rent_rupees,
        "annual_expenses_rupees": annual_expenses_rupees,
        "one_time_costs_rupees": one_time_costs_rupees,
        "vacancy_rate_pct": vacancy_rate_pct
    }

    if appreciation_rate_pct is not None:
        inputs["appreciation_rate_pct"] = appreciation_rate_pct

    for name, value in inputs.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a valid number.")

        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")

    if purchase_price_lakhs <= 0:
        raise ValueError("Purchase price must be greater than zero.")

    if monthly_rent_rupees < 0:
        raise ValueError("Monthly rent cannot be negative.")

    if annual_expenses_rupees < 0 or one_time_costs_rupees < 0:
        raise ValueError("Expenses cannot be negative.")

    if not 0 <= vacancy_rate_pct <= 100:
        raise ValueError("Vacancy rate must be between 0 and 100.")

    if appreciation_rate_pct is not None and appreciation_rate_pct <= -100:
        raise ValueError("Appreciation rate must be greater than -100%.")

    purchase_price_rupees = purchase_price_lakhs * 100000
    total_acquisition_cost = purchase_price_rupees + one_time_costs_rupees

    gross_annual_rent = monthly_rent_rupees * 12
    effective_annual_rent = gross_annual_rent * (1 - vacancy_rate_pct / 100)
    net_annual_rent = effective_annual_rent - annual_expenses_rupees

    gross_rental_yield = (gross_annual_rent / purchase_price_rupees) * 100
    net_rental_yield = (net_annual_rent / total_acquisition_cost) * 100
    monthly_net_cash_flow = net_annual_rent / 12

    five_year_value = None

    if appreciation_rate_pct is not None:
        five_year_value = (
            purchase_price_rupees * (1 + appreciation_rate_pct / 100) ** 5
        )

    return {
        "purchase_price_rupees": round(purchase_price_rupees, 2),
        "total_acquisition_cost": round(total_acquisition_cost, 2),
        "gross_annual_rent": round(gross_annual_rent, 2),
        "effective_annual_rent": round(effective_annual_rent, 2),
        "net_annual_rent": round(net_annual_rent, 2),
        "gross_rental_yield_pct": round(gross_rental_yield, 2),
        "net_rental_yield_pct": round(net_rental_yield, 2),
        "monthly_net_cash_flow": round(monthly_net_cash_flow, 2),
        "five_year_scenario_value": (
            round(five_year_value, 2)
            if five_year_value is not None else None
        )
    }



def compare_appreciation_scenarios(
    purchase_price_lakhs,
    appreciation_rates=None
):
    """Compare hypothetical five-year property appreciation scenarios."""

    if (
        isinstance(purchase_price_lakhs, bool)
        or not isinstance(purchase_price_lakhs, (int, float))
        or not math.isfinite(purchase_price_lakhs)
        or purchase_price_lakhs <= 0
    ):
        raise ValueError("Purchase price must be a finite positive number.")

    if appreciation_rates is None:
        appreciation_rates = {
            "Conservative": 3,
            "Moderate": 5,
            "Optimistic": 8
        }

    if not isinstance(appreciation_rates, dict) or not appreciation_rates:
        raise ValueError("Appreciation rates must be a non-empty dictionary.")

    purchase_price_rupees = purchase_price_lakhs * 100000
    scenarios = []

    for scenario_name, rate in appreciation_rates.items():
        if not isinstance(scenario_name, str) or not scenario_name.strip():
            raise ValueError("Scenario names must be non-empty strings.")

        if (
            isinstance(rate, bool)
            or not isinstance(rate, (int, float))
            or not math.isfinite(rate)
            or rate <= -100
        ):
            raise ValueError("Appreciation rates must be finite numbers greater than -100.")

        future_value = purchase_price_rupees * (1 + rate / 100) ** 5

        scenarios.append({
            "Scenario": scenario_name,
            "Annual Appreciation (%)": rate,
            "Current Value (₹)": round(purchase_price_rupees, 2),
            "Five-Year Scenario Value (₹)": round(future_value, 2),
            "Estimated Change (₹)": round(
                future_value - purchase_price_rupees, 2
            )
        })

    return scenarios
