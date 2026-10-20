"""Lab 14 — Meridian Foundation Reserve portfolio return and risk engine.

Run: python portfolio.py
The inputs below are course-authored training values, not market estimates.
"""

from __future__ import annotations

import math
import sys


# Editable inputs. Rates and volatilities are decimals, not percentages.
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% plus 4.0%; labelled estimate.
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlations(sleeves: dict[str, dict[str, float]], correlations: dict[str, dict[str, float]]) -> None:
    """Stop if the correlation matrix has missing, non-symmetric, or invalid entries."""
    names = list(sleeves)
    for left in names:
        if left not in correlations:
            raise ValueError(f"Correlation table is missing row: {left}")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Correlation table is missing {left} / {right}.")
            value = correlations[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Correlation for {left} / {right} is outside -1 to 1: {value}")
            if correlations.get(right, {}).get(left) != value:
                raise ValueError(f"Correlation table is not symmetric at {left} / {right}.")


def covariance_matrix(sleeves: dict[str, dict[str, float]], correlations: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """Compute covariance = correlation × left volatility × right volatility."""
    return {
        left: {
            right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def portfolio_return(weights: dict[str, float], sleeves: dict[str, dict[str, float]]) -> float:
    """Compute the weighted average expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_volatility(weights: dict[str, float], covariances: dict[str, dict[str, float]]) -> float:
    """Compute sqrt(w' * covariance matrix * w), retaining every covariance term."""
    variance = sum(
        weights[left] * weights[right] * covariances[left][right]
        for left in weights
        for right in weights
    )
    if variance < 0:
        raise ValueError(f"Portfolio variance cannot be negative: {variance}")
    return math.sqrt(variance)


def reserve_eligible_weight(weights: dict[str, float]) -> float:
    """Add the client-designated bills and 10-year Treasury sleeve weights."""
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def equal_weight_portfolio(sleeves: dict[str, dict[str, float]]) -> dict[str, float]:
    """Return equal weights across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves: dict[str, dict[str, float]]) -> dict[str, float]:
    """Scale 1 / volatility weights to sum to 100%."""
    raw_weights = {name: 1 / details["volatility"] for name, details in sleeves.items()}
    total = sum(raw_weights.values())
    return {name: weight / total for name, weight in raw_weights.items()}


def baseline_portfolios(sleeves: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """Define the three required Meridian baseline portfolios."""
    return {
        "Benchmark": {
            "Treasury bills": 0.0,
            "Treasury 10-year note": 0.0,
            "Investment-grade bond fund": 0.40,
            "Global equity index fund": 0.60,
        },
        "Equal weight": equal_weight_portfolio(sleeves),
        "Inverse volatility": inverse_volatility_portfolio(sleeves),
    }


def print_portfolio(name: str, weights: dict[str, float], sleeves: dict[str, dict[str, float]], covariances: dict[str, dict[str, float]]) -> None:
    """Print one portfolio's inputs-derived return, risk, liquidity reserve, and objective test."""
    expected = portfolio_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariances)
    reserve_weight = reserve_eligible_weight(weights)
    weight_line = " / ".join(f"{weights[sleeve] * 100:.1f}" for sleeve in sleeves)

    print(f"\n{name}")
    print(f"Weights (bills / 10-year / IG / equity): {weight_line}%")
    print(f"Expected return: {expected * 100:.2f}%")
    print(f"Volatility: {volatility * 100:.2f}%")
    print(f"Reserve-eligible weight: {reserve_weight * 100:.1f}%")
    print(f"Meets {OBJECTIVE_RETURN * 100:.1f}% objective: {'yes' if expected >= OBJECTIVE_RETURN else 'no'}")


def main() -> None:
    try:
        validate_correlations(SLEEVES, CORRELATIONS)
        covariances = covariance_matrix(SLEEVES, CORRELATIONS)
        for name, weights in baseline_portfolios(SLEEVES).items():
            print_portfolio(name, weights, SLEEVES, covariances)
    except ValueError as error:
        print(f"Input validation error: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
