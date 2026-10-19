"""Integrated FCFF DCF driven by the Chipotle five-year pro forma.

All amounts are USD millions except per-share values. This module imports the
operating forecast from cmg_proforma.py; it does not enter a separate FCFF
growth path. CAPM/WACC support is documented in research/wacc-support.md.
"""

from __future__ import annotations

import copy

from cmg_proforma import (
    BASE_INPUTS,
    SCENARIO_CASES,
    SENSITIVITY_CASES,
    TAX_RATE,
    TERMINAL_GROWTH,
    YEARS,
    run_model,
)


# February 5, 2026 CAPM inputs: 4.21% risk-free rate + 0.92 beta x 4.23% ERP.
# CMG has no funded debt under the project's operating-lease convention, so
# WACC equals the cost of equity. See research/wacc-support.md for sources.
RISK_FREE_RATE = 0.0421
BETA = 0.92
EQUITY_RISK_PREMIUM = 0.0423
COST_OF_EQUITY = RISK_FREE_RATE + BETA * EQUITY_RISK_PREMIUM
WACC = COST_OF_EQUITY
# FY2025 diluted weighted-average shares, in millions. This is kept consistent
# with the original DCF until an as-of-date diluted share-count bridge is added.
DILUTED_SHARES = 1342.616
FUNDED_DEBT = 0.0
NON_OPERATING_CASH = 350.545
MARKET_PRICE_AS_OF_DATE = 38.45  # CMG close on February 5, 2026.
MARKET_CAPITALIZATION_AS_OF_DATE = MARKET_PRICE_AS_OF_DATE * DILUTED_SHARES
# Reverse DCF: apply one additive shift to each annual pro-forma revenue-growth
# assumption while holding base margin, capex, WACC, terminal growth, cash, and
# funded debt constant. The bracket is deliberately wide enough to test whether
# the same-date market price can be reached under that one-variable framing.
REVERSE_REVENUE_GROWTH_SHIFT_BRACKET = (-0.10, 0.30)
REVERSE_TOLERANCE = 0.000001
REVERSE_MAX_ITERATIONS = 200


def fcff_from_projections(projections):
    """Calculate FCFF directly from each pro-forma year."""
    fcff = {}
    for year in YEARS:
        statement = projections[year]
        nopat = statement["operating_income"] * (1 - TAX_RATE)
        fcff[year] = (
            nopat
            + statement["depreciation"]
            - statement["capital_spending"]
            - statement["change_nwc"]
        )
    return fcff


def value_dcf(fcff, wacc=WACC, terminal_growth=TERMINAL_GROWTH):
    """Value supplied FCFF using a Gordon-growth terminal value."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")

    pv_explicit = sum(
        fcff[year] / (1 + wacc) ** (year - 2025)
        for year in YEARS
    )
    terminal_fcff = fcff[2030] * (1 + terminal_growth)
    terminal_value_2030 = terminal_fcff / (wacc - terminal_growth)
    pv_terminal = terminal_value_2030 / (1 + wacc) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + NON_OPERATING_CASH - FUNDED_DEBT
    return {
        "pv_explicit": pv_explicit,
        "terminal_value_2030": terminal_value_2030,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": equity_value / DILUTED_SHARES,
        "terminal_value_share": pv_terminal / enterprise_value,
    }


def run_integrated_dcf(inputs=None, wacc=WACC, terminal_growth=TERMINAL_GROWTH):
    """Run the pro forma, derive FCFF, and value it in one traceable path."""
    if inputs is None:
        inputs = copy.deepcopy(BASE_INPUTS)
    projections, proforma_results = run_model(inputs, print_output=False)
    fcff = fcff_from_projections(projections)
    valuation = value_dcf(fcff, wacc=wacc, terminal_growth=terminal_growth)
    return projections, proforma_results, fcff, valuation


def assert_dcf_directionality(fcff):
    """Fail loudly if a higher WACC or lower terminal growth raises value."""
    base = value_dcf(fcff, wacc=WACC, terminal_growth=TERMINAL_GROWTH)
    higher_wacc = value_dcf(fcff, wacc=WACC + 0.01, terminal_growth=TERMINAL_GROWTH)
    lower_growth = value_dcf(fcff, wacc=WACC, terminal_growth=TERMINAL_GROWTH - 0.01)
    if higher_wacc["value_per_share"] >= base["value_per_share"]:
        raise AssertionError("Higher WACC did not reduce value per share.")
    if lower_growth["value_per_share"] >= base["value_per_share"]:
        raise AssertionError("Lower terminal growth did not reduce value per share.")


def assert_enterprise_to_equity_bridge(valuation):
    """Confirm the DCF enterprise-value bridge and per-share division reconcile."""
    expected_equity_value = valuation["enterprise_value"] + NON_OPERATING_CASH - FUNDED_DEBT
    if abs(valuation["equity_value"] - expected_equity_value) > 1e-6:
        raise AssertionError("Enterprise-to-equity bridge does not reconcile.")
    expected_per_share = valuation["equity_value"] / DILUTED_SHARES
    if abs(valuation["value_per_share"] - expected_per_share) > 1e-6:
        raise AssertionError("Equity-value-to-per-share bridge does not reconcile.")


def assert_proforma_driver_linkage():
    """Confirm a lower pro-forma revenue path reduces FCFF and DCF value."""
    base_inputs = copy.deepcopy(BASE_INPUTS)
    lower_inputs = copy.deepcopy(BASE_INPUTS)
    lower_inputs["revenue_growth"] = copy.deepcopy(
        SENSITIVITY_CASES["Revenue growth"]["lower"]
    )
    _, _, base_fcff, base_value = run_integrated_dcf(base_inputs)
    _, _, lower_fcff, lower_value = run_integrated_dcf(lower_inputs)
    if lower_fcff[2030] >= base_fcff[2030]:
        raise AssertionError("Lower revenue growth did not reduce FY2030E FCFF.")
    if lower_value["value_per_share"] >= base_value["value_per_share"]:
        raise AssertionError("Lower revenue growth did not reduce DCF value per share.")


def run_scenario_valuations():
    """Run named operating cases through the pro forma, FCFF, and DCF bridge."""
    scenario_results = {}
    for name, case in SCENARIO_CASES.items():
        projections, _, fcff, valuation = run_integrated_dcf(
            copy.deepcopy(case["inputs"])
        )
        scenario_results[name] = {
            "description": case["description"],
            "fy2030_revenue": projections[2030]["revenue"],
            "fy2030_ebit": projections[2030]["operating_income"],
            "fy2030_fcff": fcff[2030],
            **valuation,
        }

    low = scenario_results["Low / downside"]["value_per_share"]
    base = scenario_results["Base"]["value_per_share"]
    high = scenario_results["High / upside"]["value_per_share"]
    if not low < base < high:
        raise AssertionError("Named scenario values must be ordered low < base < high.")
    return scenario_results


def value_for_revenue_growth_shift(shift):
    """Return integrated DCF results after a uniform revenue-growth shift."""
    inputs = copy.deepcopy(BASE_INPUTS)
    inputs["revenue_growth"] = {
        year: BASE_INPUTS["revenue_growth"][year] + shift for year in YEARS
    }
    if any(rate <= -1 for rate in inputs["revenue_growth"].values()):
        raise ValueError("Reverse-DCF growth shift makes revenue nonpositive.")
    return run_integrated_dcf(inputs)


def solve_reverse_dcf():
    """Solve for the revenue-growth shift that matches the same-date market price."""
    lower_shift, upper_shift = REVERSE_REVENUE_GROWTH_SHIFT_BRACKET
    _, _, _, lower_value = value_for_revenue_growth_shift(lower_shift)
    _, _, _, upper_value = value_for_revenue_growth_shift(upper_shift)

    if not (
        lower_value["value_per_share"]
        <= MARKET_PRICE_AS_OF_DATE
        <= upper_value["value_per_share"]
    ):
        return None

    midpoint_shift = None
    midpoint_value = None
    for _ in range(REVERSE_MAX_ITERATIONS):
        midpoint_shift = (lower_shift + upper_shift) / 2
        _, _, _, midpoint_value = value_for_revenue_growth_shift(midpoint_shift)
        if abs(midpoint_value["value_per_share"] - MARKET_PRICE_AS_OF_DATE) <= REVERSE_TOLERANCE:
            break
        if midpoint_value["value_per_share"] < MARKET_PRICE_AS_OF_DATE:
            lower_shift = midpoint_shift
        else:
            upper_shift = midpoint_shift

    inputs = copy.deepcopy(BASE_INPUTS)
    implied_growth = {
        year: BASE_INPUTS["revenue_growth"][year] + midpoint_shift for year in YEARS
    }
    inputs["revenue_growth"] = implied_growth
    projections, _, fcff, valuation = run_integrated_dcf(inputs)
    return {
        "growth_shift": midpoint_shift,
        "implied_growth": implied_growth,
        "fy2030_revenue": projections[2030]["revenue"],
        "fy2030_ebit": projections[2030]["operating_income"],
        "fy2030_fcff": fcff[2030],
        **valuation,
    }


def print_scenario_valuations():
    """Print the final-year operating and valuation outputs for each named case."""
    scenarios = run_scenario_valuations()
    print("\nIntegrated low / base / high scenarios")
    print("Each named operating case runs through all five pro-forma years and the FCFF DCF.")
    print(
        f"{'Scenario':<18}{'FY2030E revenue':>18}{'FY2030E EBIT':>16}"
        f"{'FY2030E FCFF':>16}{'EV':>14}{'Equity value':>16}{'Value/share':>15}"
    )
    for name in ("Low / downside", "Base", "High / upside"):
        result = scenarios[name]
        print(
            f"{name:<18}{result['fy2030_revenue']:>17,.1f}"
            f"{result['fy2030_ebit']:>16,.1f}"
            f"{result['fy2030_fcff']:>16,.1f}"
            f"{result['enterprise_value']:>14,.1f}"
            f"{result['equity_value']:>16,.1f}"
            f"{result['value_per_share']:>15,.2f}"
        )
    print(
        "DCF valuation range (low to high): "
        f"${scenarios['Low / downside']['value_per_share']:.2f} to "
        f"${scenarios['High / upside']['value_per_share']:.2f} per diluted share; "
        f"base: ${scenarios['Base']['value_per_share']:.2f}."
    )


def print_reverse_dcf():
    """Explain the one-variable operating hurdle implied by the market price."""
    result = solve_reverse_dcf()
    print("\nIntegrated reverse DCF: market-implied revenue-growth hurdle")
    print(f"Valuation date and target market price: February 5, 2026 / ${MARKET_PRICE_AS_OF_DATE:.2f}")
    print(f"Same-date market capitalization: ${MARKET_CAPITALIZATION_AS_OF_DATE:,.1f} million")
    print(
        "Held at base case: gross margin, capital spending, WACC, terminal growth, "
        "cash, funded debt, and diluted shares."
    )
    if result is None:
        lower, upper = REVERSE_REVENUE_GROWTH_SHIFT_BRACKET
        print(
            "No solution in the tested revenue-growth-shift bracket "
            f"({lower:+.1%} to {upper:+.1%})."
        )
        return

    growth_text = ", ".join(
        f"FY{year}E {result['implied_growth'][year]:.1%}" for year in YEARS
    )
    print(f"Solved uniform revenue-growth shift: {result['growth_shift']:+.2%} each year")
    print(f"Market-implied revenue-growth path: {growth_text}")
    print(
        f"At that path: FY2030E revenue ${result['fy2030_revenue']:,.1f}m; "
        f"EBIT ${result['fy2030_ebit']:,.1f}m; FCFF ${result['fy2030_fcff']:,.1f}m; "
        f"value/share ${result['value_per_share']:.2f}."
    )
    print(
        "Interpretation: this is a one-variable hurdle under the model's base "
        "margin and reinvestment assumptions, not a forecast or a probability."
    )


def print_dcf():
    _, _, fcff, valuation = run_integrated_dcf()
    assert_dcf_directionality(fcff)
    assert_proforma_driver_linkage()
    assert_enterprise_to_equity_bridge(valuation)
    print("Integrated FCFF DCF (USD millions except per-share values)")
    print("FCFF is calculated from the Chipotle pro forma, not a separate growth path.")
    for year in YEARS:
        print(f"FY{year}E FCFF: ${fcff[year]:,.1f}")
    print(f"PV of explicit FCFF: ${valuation['pv_explicit']:,.1f}")
    print(f"PV of terminal value: ${valuation['pv_terminal']:,.1f}")
    print(f"Enterprise value: ${valuation['enterprise_value']:,.1f}")
    print(f"Equity value: ${valuation['equity_value']:,.1f}")
    print(f"Value per diluted share: ${valuation['value_per_share']:,.2f}")
    print(f"Terminal-value share of enterprise value: ${valuation['terminal_value_share']:.1%}")
    print("DCF directionality checks: PASS")
    print("Pro-forma revenue-driver-to-FCFF-to-DCF check: PASS")
    print("Enterprise-to-equity bridge check: PASS")
    print(f"Market price on February 5, 2026: ${MARKET_PRICE_AS_OF_DATE:,.2f}")
    print(f"Market capitalization on February 5, 2026: ${MARKET_CAPITALIZATION_AS_OF_DATE:,.1f} million")
    print(f"Base value / market price: ${valuation['value_per_share'] / MARKET_PRICE_AS_OF_DATE:.2f}x")
    print_scenario_valuations()
    print_reverse_dcf()


if __name__ == "__main__":
    print_dcf()
