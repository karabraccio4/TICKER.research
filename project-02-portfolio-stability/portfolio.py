"""Lab 14 — Meridian Foundation Reserve portfolio return and risk engine.

Run: python portfolio.py
The inputs below are course-authored training values, not market estimates.
"""

from __future__ import annotations

import math
import sys
import csv
from pathlib import Path
from typing import TextIO


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


def find_lowest_risk_mix(
    sleeves: dict[str, dict[str, float]],
    correlations: dict[str, dict[str, float]],
    objective_return: float,
    reserve_eligible: set[str],
    minimum_reserve: float,
    step: float = 0.05,
) -> dict[str, float] | None:
    """Search every long-only ``step`` mix and return the lowest-risk feasible one.

    The default 5-point grid makes the optimizer easy to inspect in class.
    A feasible mix must sum to 100%, meet the return objective, and meet the
    reserve-eligible minimum.  ``None`` means no grid mix passes both tests.
    """
    if not 0 < step <= 1 or not math.isclose(1 / step, round(1 / step)):
        raise ValueError("Search step must divide 100% exactly, such as 0.05.")

    names = list(sleeves)
    units = round(1 / step)
    covariances = covariance_matrix(sleeves, correlations)
    best_mix: dict[str, float] | None = None
    best_volatility = float("inf")

    def search(position: int, units_left: int, chosen: list[int]) -> None:
        nonlocal best_mix, best_volatility
        if position == len(names) - 1:
            weights = {
                name: units_for_name * step
                for name, units_for_name in zip(names, [*chosen, units_left])
            }
            expected = portfolio_return(weights, sleeves)
            reserve_weight = sum(weights[name] for name in reserve_eligible)
            if expected + 1e-12 < objective_return or reserve_weight + 1e-12 < minimum_reserve:
                return
            volatility = portfolio_volatility(weights, covariances)
            if volatility < best_volatility - 1e-12:
                best_mix = weights
                best_volatility = volatility
            return

        for allocation_units in range(units_left + 1):
            search(position + 1, units_left - allocation_units, [*chosen, allocation_units])

    validate_correlations(sleeves, correlations)
    search(0, units, [])
    return best_mix


def estimates_from_prices(
    source: str | Path | TextIO,
    last_36_months: bool = False,
) -> tuple[dict[str, dict[str, float]], dict[str, dict[str, float]]]:
    """Estimate annualized inputs from a monthly adjusted-close CSV.

    The CSV must put ``date`` first, list months oldest first, and contain one
    price column per ticker.  Returns are mean monthly return × 12; volatility
    is sample monthly standard deviation × sqrt(12).  Correlations use the
    same monthly-return sample.  Set ``last_36_months`` to use only the last
    36 monthly returns instead of every available month.
    """
    should_close = False
    if isinstance(source, (str, Path)):
        handle = open(source, newline="")
        should_close = True
    else:
        handle = source
        handle.seek(0)

    try:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or reader.fieldnames[0] != "date":
            raise ValueError("CSV must have date as its first column.")
        names = reader.fieldnames[1:]
        if not names:
            raise ValueError("CSV must include at least one ticker price column.")
        prices = {name: [] for name in names}
        for row in reader:
            for name in names:
                prices[name].append(float(row[name]))
    finally:
        if should_close:
            handle.close()

    if any(len(values) < 3 for values in prices.values()):
        raise ValueError("CSV needs at least three monthly price rows.")
    monthly_returns = {
        name: [later / earlier - 1 for earlier, later in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {name: values[-36:] for name, values in monthly_returns.items()}
    observations = len(next(iter(monthly_returns.values())))
    if observations < 2:
        raise ValueError("At least two monthly returns are required to estimate volatility.")

    means = {name: sum(values) / observations for name, values in monthly_returns.items()}
    monthly_volatilities = {
        name: math.sqrt(sum((value - means[name]) ** 2 for value in values) / (observations - 1))
        for name, values in monthly_returns.items()
    }
    estimated_sleeves = {
        name: {
            "expected_return": means[name] * 12,
            "volatility": monthly_volatilities[name] * math.sqrt(12),
        }
        for name in names
    }
    estimated_correlations: dict[str, dict[str, float]] = {}
    for left in names:
        estimated_correlations[left] = {}
        for right in names:
            if left == right:
                estimated_correlations[left][right] = 1.0
            elif monthly_volatilities[left] == 0 or monthly_volatilities[right] == 0:
                raise ValueError(f"Cannot calculate correlation when {left} or {right} has zero volatility.")
            else:
                covariance = sum(
                    (left_value - means[left]) * (right_value - means[right])
                    for left_value, right_value in zip(monthly_returns[left], monthly_returns[right])
                ) / (observations - 1)
                estimated_correlations[left][right] = covariance / (
                    monthly_volatilities[left] * monthly_volatilities[right]
                )
    validate_correlations(estimated_sleeves, estimated_correlations)
    return estimated_sleeves, estimated_correlations


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
