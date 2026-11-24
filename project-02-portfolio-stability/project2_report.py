"""Reproducible Project 2 decision report.

Run: python project2_report.py

Uses the checked-in monthly adjusted-close history and the transparent 5-point
grid search in portfolio.py.  This is the command a reviewer can use to
reproduce the numbers in docs/decision-memo.md without opening Streamlit.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from portfolio import (
    covariance_matrix,
    equal_weight_portfolio,
    estimates_from_prices,
    find_lowest_risk_mix,
    inverse_volatility_portfolio,
    portfolio_return,
    portfolio_volatility,
)


OBJECTIVE = 0.055
MINIMUM_RESERVE = 0.20
RESERVE_ELIGIBLE = {"BIL", "IEF"}
PRICE_FILE = Path(__file__).with_name("prices.csv")


def calculate(last_36_months: bool = False, vt_return_change: float = 0.0) -> tuple[dict[str, float], float, float, float]:
    """Return the lowest-risk feasible mix and its three mandate measures."""
    sleeves, correlations = estimates_from_prices(PRICE_FILE, last_36_months=last_36_months)
    sleeves = deepcopy(sleeves)
    sleeves["VT"]["expected_return"] += vt_return_change
    mix = find_lowest_risk_mix(sleeves, correlations, OBJECTIVE, RESERVE_ELIGIBLE, MINIMUM_RESERVE)
    if mix is None:
        raise RuntimeError("No 5-point mix met the Project 2 mandate.")
    expected_return = portfolio_return(mix, sleeves)
    volatility = portfolio_volatility(mix, covariance_matrix(sleeves, correlations))
    reserve_weight = sum(mix[name] for name in RESERVE_ELIGIBLE)
    return mix, expected_return, volatility, reserve_weight


def print_result(label: str, last_36_months: bool = False, vt_return_change: float = 0.0) -> None:
    """Print one result in a compact, GitHub-readable form."""
    mix, expected_return, volatility, reserve_weight = calculate(last_36_months, vt_return_change)
    weights = " / ".join(f"{name} {mix[name] * 100:.0f}%" for name in ("BIL", "IEF", "LQD", "VT"))
    print(f"{label}\n  Mix: {weights}\n  Expected return: {expected_return * 100:.2f}%\n  Volatility: {volatility * 100:.2f}%\n  Reserve eligible: {reserve_weight * 100:.1f}%")


def print_baselines() -> None:
    """Print the two transparent baselines under the same Project 2 mandate."""
    sleeves, correlations = estimates_from_prices(PRICE_FILE)
    for label, mix in (
        ("Equal-weight baseline", equal_weight_portfolio(sleeves)),
        ("Inverse-volatility baseline", inverse_volatility_portfolio(sleeves)),
    ):
        expected_return = portfolio_return(mix, sleeves)
        volatility = portfolio_volatility(mix, covariance_matrix(sleeves, correlations))
        reserve_weight = sum(mix[name] for name in RESERVE_ELIGIBLE)
        return_verdict = "PASS" if expected_return >= OBJECTIVE else f"FAIL (below {OBJECTIVE * 100:.1f}% return objective)"
        reserve_verdict = "PASS" if reserve_weight >= MINIMUM_RESERVE else f"FAIL (below {MINIMUM_RESERVE * 100:.1f}% reserve minimum)"
        overall = "PASS" if expected_return >= OBJECTIVE and reserve_weight >= MINIMUM_RESERVE else "FAIL"
        print(f"{label}\n  Expected return: {expected_return * 100:.2f}% ({return_verdict})\n  Volatility: {volatility * 100:.2f}%\n  Reserve eligible: {reserve_weight * 100:.1f}% ({reserve_verdict})\n  Mandate verdict: {overall}")


def main() -> None:
    print("Project 2: Portfolio stability decision")
    print("Mandate: expected return >= 5.5%; BIL + IEF >= 20.0%; long-only 5-point grid.\n")
    print_baselines()
    print()
    print_result("Baseline - all 59 monthly returns")
    print()
    print_result("Window check - last 36 monthly returns", last_36_months=True)
    print()
    print_result("Stress - VT expected return decreased by 1.0 percentage point", vt_return_change=-0.01)
    print("\nDecision: PILOT a 70–75% BIL / 25–30% VT range, not adopt. Pause or reverse until approving a forward-looking return-estimate method and history window.")


if __name__ == "__main__":
    main()
