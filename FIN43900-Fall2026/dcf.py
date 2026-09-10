"""Five-year FCFF discounted cash flow model (all monetary inputs in USD millions)."""

# ----------------------------
# Inputs you can edit by hand
# ----------------------------
# FY2025 actuals, in USD millions, from Chipotle's FY2025 Form 10-K:
# starting FCFF = cash from operations ($2,113.926m) - capex ($666.336m).
starting_fcff = 1447.590
# Analyst base-case assumptions: growth reflects planned restaurant openings,
# tempered by the FY2025 comparable-sales decline and elevated FY2026 capex.
growth_rates = [0.05, 0.07, 0.07, 0.06, 0.05]
# Analyst base-case discount-rate and steady-state growth assumptions.
# Confirm with course guidance if your professor specifies a required WACC.
wacc = 0.085
terminal_growth = 0.025
# FY2025 balance-sheet cash, funded debt, and diluted weighted-average shares.
non_operating_cash = 350.545
debt = 0.0
diluted_shares = 1342.616

# Sensitivity-grid inputs (edit these lists as needed).
sensitivity_waccs = [0.09, 0.10, 0.11]
sensitivity_terminal_growths = [0.02, 0.03, 0.04]

# Reverse-DCF inputs (edit these values as needed).
reverse_target_share_price = 36.03
reverse_lower_shift = -0.05
reverse_upper_shift = 0.10
reverse_tolerance = 0.000001
reverse_max_iterations = 200


if terminal_growth >= wacc:
    raise SystemExit(
        "Error: terminal growth must be less than WACC for the Gordon-growth formula."
    )

if len(growth_rates) != 5:
    raise SystemExit("Error: provide exactly five yearly growth rates.")

if diluted_shares <= 0:
    raise SystemExit("Error: diluted shares must be greater than zero.")


fcff_by_year = []
fcff = starting_fcff
for growth_rate in growth_rates:
    fcff *= 1 + growth_rate
    fcff_by_year.append(fcff)

pv_explicit_fcff = sum(
    fcff / (1 + wacc) ** year
    for year, fcff in enumerate(fcff_by_year, start=1)
)
terminal_value_year_5 = (
    fcff_by_year[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
)
pv_terminal_value = terminal_value_year_5 / (1 + wacc) ** 5
enterprise_value = pv_explicit_fcff + pv_terminal_value
equity_value = enterprise_value + non_operating_cash - debt
value_per_diluted_share = equity_value / diluted_shares
pv_terminal_value_share_of_ev = pv_terminal_value / enterprise_value


for year, fcff in enumerate(fcff_by_year, start=1):
    print(f"FCFF Year {year}: {fcff:.4f}")
print(f"PV of five explicit FCFF: {pv_explicit_fcff:.4f}")
print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
print(f"PV of terminal value: {pv_terminal_value:.4f}")
print(f"Enterprise value: {enterprise_value:.4f}")
print(f"Equity value: {equity_value:.4f}")
print(f"Value per diluted share: {value_per_diluted_share:.4f}")
print(f"PV terminal value as share of enterprise value: {pv_terminal_value_share_of_ev:.4f}")


def calculate_value_per_share(test_growth_rates, test_wacc, test_terminal_growth):
    """Return DCF value per diluted share for a supplied assumption set."""
    test_fcff = starting_fcff
    test_fcff_by_year = []
    for test_growth_rate in test_growth_rates:
        test_fcff *= 1 + test_growth_rate
        test_fcff_by_year.append(test_fcff)

    test_pv_explicit_fcff = sum(
        test_fcff / (1 + test_wacc) ** year
        for year, test_fcff in enumerate(test_fcff_by_year, start=1)
    )
    test_terminal_value_year_5 = (
        test_fcff_by_year[-1] * (1 + test_terminal_growth)
        / (test_wacc - test_terminal_growth)
    )
    test_pv_terminal_value = test_terminal_value_year_5 / (1 + test_wacc) ** 5
    test_enterprise_value = test_pv_explicit_fcff + test_pv_terminal_value
    test_equity_value = test_enterprise_value + non_operating_cash - debt
    return test_equity_value / diluted_shares


print("\nSensitivity grid: value per diluted share")
header = "WACC \\ terminal growth |" + "".join(
    f" {growth:.0%}".rjust(10) for growth in sensitivity_terminal_growths
)
print(header)
print("-" * len(header))
for sensitivity_wacc in sensitivity_waccs:
    cells = []
    for sensitivity_terminal_growth in sensitivity_terminal_growths:
        if sensitivity_terminal_growth >= sensitivity_wacc:
            cells.append("invalid".rjust(10))
        else:
            sensitivity_value = calculate_value_per_share(
                growth_rates, sensitivity_wacc, sensitivity_terminal_growth
            )
            cells.append(f"${sensitivity_value:,.2f}".rjust(10))
    print(f"{sensitivity_wacc:.0%}".ljust(24) + "|" + "".join(cells))


def reverse_dcf_value_for_shift(shift):
    """Return value per share after applying one shift to all explicit growth rates."""
    shifted_growth_rates = [growth_rate + shift for growth_rate in growth_rates]
    if any(growth_rate <= -1 for growth_rate in shifted_growth_rates):
        return None
    return calculate_value_per_share(shifted_growth_rates, wacc, terminal_growth)


print("\nReverse DCF: uniform shift to all five explicit FCFF growth rates")
print(f"Target share price: ${reverse_target_share_price:,.2f}")
print(
    "Inputs held fixed: "
    f"starting FCFF=${starting_fcff:,.3f}m; WACC={wacc:.1%}; "
    f"terminal growth={terminal_growth:.1%}; cash=${non_operating_cash:,.3f}m; "
    f"debt=${debt:,.3f}m; diluted shares={diluted_shares:,.3f}m."
)
print("Base explicit growth rates: " + ", ".join(f"{rate:.1%}" for rate in growth_rates))
print(
    "Search bracket: "
    f"{reverse_lower_shift:+.1%} to {reverse_upper_shift:+.1%} applied to each growth rate."
)

lower_value = reverse_dcf_value_for_shift(reverse_lower_shift)
upper_value = reverse_dcf_value_for_shift(reverse_upper_shift)

if lower_value is None or upper_value is None:
    print("No solution: the search bracket pushes an annual growth rate to -100% or below.")
elif not min(lower_value, upper_value) <= reverse_target_share_price <= max(
    lower_value, upper_value
):
    print("No solution in this bracket: the target share price is not reachable.")
else:
    lower_shift = reverse_lower_shift
    upper_shift = reverse_upper_shift
    for _ in range(reverse_max_iterations):
        midpoint_shift = (lower_shift + upper_shift) / 2
        midpoint_value = reverse_dcf_value_for_shift(midpoint_shift)
        if abs(midpoint_value - reverse_target_share_price) <= reverse_tolerance:
            break
        if midpoint_value < reverse_target_share_price:
            lower_shift = midpoint_shift
        else:
            upper_shift = midpoint_shift
    shifted_growth_rates = [growth_rate + midpoint_shift for growth_rate in growth_rates]
    print(f"Solved uniform growth-rate shift: {midpoint_shift:+.4%}")
    print(f"Value per diluted share at solved shift: ${midpoint_value:,.4f}")
    print("Shifted explicit growth rates: " + ", ".join(f"{rate:.4%}" for rate in shifted_growth_rates))
