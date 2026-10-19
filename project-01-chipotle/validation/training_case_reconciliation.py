"""Reconcile the course's official five-year DCF training case.

Run from the project root:
    python validation/training_case_reconciliation.py

The inputs and rounded expected results are from “The Training-Case DCF,
Worked End to End,” supplied in the Week 6 student materials. The test calls
the project's actual value_dcf function rather than duplicating its DCF math.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from cmg_integrated_dcf import value_dcf  # noqa: E402


FCFF = {
    2026: 108.0,
    2027: 114.48,
    2028: 120.204,
    2029: 125.01216,
    2030: 128.7625248,
}
WACC = 0.10
TERMINAL_GROWTH = 0.03
CASH = 50.0
DEBT = 300.0
SHARES = 50.0
TOLERANCE = 0.01  # The teaching case publishes dollar figures rounded to cents.

# Official, displayed training-case answers. Values are compared at the
# published precision; internal calculations retain the unrounded FCFF path.
EXPECTED = {
    "pv_explicit": 448.44,
    "terminal_value_2030": 1894.65,
    "pv_terminal": 1176.43,
    "enterprise_value": 1624.87,
    "equity_value": 1374.87,
    "value_per_share": 27.50,
    "terminal_value_share": 0.724,
}
GRID_EXPECTED = {
    (0.09, 0.02): 28.60,
    (0.09, 0.03): 32.94,
    (0.09, 0.04): 39.02,
    (0.10, 0.02): 24.36,
    (0.10, 0.03): 27.50,
    (0.10, 0.04): 31.69,
    (0.11, 0.02): 21.06,
    (0.11, 0.03): 23.41,
    (0.11, 0.04): 26.44,
}


def value_case(wacc=WACC, terminal_growth=TERMINAL_GROWTH):
    return value_dcf(
        FCFF,
        wacc=wacc,
        terminal_growth=terminal_growth,
        non_operating_cash=CASH,
        funded_debt=DEBT,
        diluted_shares=SHARES,
    )


def assert_close(label, actual, expected, tolerance=TOLERANCE):
    difference = actual - expected
    print(
        f"{label:<28} actual {actual:>10.4f} | expected {expected:>10.4f} "
        f"| difference {difference:>+9.4f}"
    )
    if abs(difference) > tolerance:
        raise AssertionError(f"{label} differs from the training answer by more than {tolerance}.")


def main():
    print("Official training-case DCF reconciliation (USD millions except per-share values)")
    result = value_case()
    for key in (
        "pv_explicit",
        "terminal_value_2030",
        "pv_terminal",
        "enterprise_value",
        "equity_value",
        "value_per_share",
    ):
        assert_close(key, result[key], EXPECTED[key])
    assert_close(
        "terminal_value_share",
        result["terminal_value_share"],
        EXPECTED["terminal_value_share"],
        tolerance=0.001,
    )

    print("\nOfficial WACC / terminal-growth grid (value per diluted share)")
    for (wacc, growth), expected in GRID_EXPECTED.items():
        actual = value_case(wacc, growth)["value_per_share"]
        assert_close(f"WACC {wacc:.0%}, g {growth:.0%}", actual, expected)

    print("\nReverse-DCF zero-shift check")
    base_value = value_case()["value_per_share"]
    assert_close("Base value equals target", base_value, 27.50)
    print("PASS: official training case reconciles to the published rounded outputs.")


if __name__ == "__main__":
    main()
