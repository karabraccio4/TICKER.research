"""Lab 13 — Meridian Foundation Reserve mandate checker.

Run: python mandate.py
Probe: python mandate.py --probe
All dollar figures are USD millions and all portfolio weights are percentages.
"""

from __future__ import annotations

import argparse


# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Candidate D exposes that passing rules is not the same as meeting the objective.
    "D": {
        "Cash": 10, "Treasury bills": 0, "Treasury 10-year note": 90,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def pct(value: float) -> str:
    """Display all measured percentages to one decimal place."""
    return f"{value:.1f}"


def pass_or_fail(passes: bool) -> str:
    return "pass" if passes else "FAIL"


def measure_candidate(weights: dict[str, float], reserve_minimum: float) -> list[tuple[str, float, bool]]:
    """Return the four checkable mandate measures and their pass/fail results."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    eligible_weight = sum(
        weight for holding, weight in weights.items() if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_weights: dict[str, float] = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0.0) + weight
    largest_company = max(company_weights.values(), default=0.0)

    return [
        ("Weights sum to 100", total_weight, total_weight == 100.0),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0.0),
        (f"Reserve >= {pct(reserve_minimum)}%", eligible_weight, eligible_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {pct(MINIMUM_LIQUID_SHARE)}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (
            f"Largest single company <= {pct(ISSUER_LIMIT)}%",
            largest_company,
            largest_company <= ISSUER_LIMIT,
        ),
    ]


def print_candidate(name: str, weights: dict[str, float], reserve_minimum: float) -> None:
    checks = measure_candidate(weights, reserve_minimum)
    print(f"\nCandidate {name}")
    for rule, value, passes in checks:
        print(f"{rule}: {pct(value)} {pass_or_fail(passes)}")
    print("Calendar-year loss: requires CIO clarification")
    failures = sum(not passes for _, _, passes in checks)
    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--probe",
        action="store_true",
        help="Run the required temporary long-only test for candidate A.",
    )
    args = parser.parse_args()

    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {pct(reserve_minimum)}% of the portfolio")

    candidates = {name: weights.copy() for name, weights in CANDIDATES.items()}
    if args.probe:
        candidates["A"]["Cash"] = -2
        candidates["A"]["Global equity index fund"] = 64
        print("Required probe active: Candidate A Cash = -2 and Global equity index fund = 64.")

    for name, weights in candidates.items():
        print_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
