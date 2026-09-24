"""ABG five-year pro forma and FCFE valuation (USD millions except per-share data)."""

YEARS = range(2026, 2031)

# Assumptions: history, guidance, and stated base-case judgments.
GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = {2026: 0.665, 2027: 0.655, 2028: 0.645, 2029: 0.645, 2030: 0.645}
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# FY2025 opening balance sheet, USD millions.
opening = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def total_assets(statement):
    return statement["cash"] + statement["inventory"] + statement["ppe"] + statement["other_assets"]


def total_liabilities_and_equity(statement):
    return (statement["floor_plan"] + statement["term_debt"] + statement["revolver"]
            + statement["other_liabilities"] + statement["equity"])


def assert_balanced(year, statement):
    """Stop the model when a projected balance sheet or cash floor check fails."""
    balance_gap = total_assets(statement) - total_liabilities_and_equity(statement)
    if abs(balance_gap) > 1e-6:
        raise AssertionError(f"{year}: balance sheet gap is {balance_gap:.6f} million")
    cash_gap = statement["cash"] - MINIMUM_CASH
    if cash_gap < -1e-6:
        raise AssertionError(f"{year}: cash is below the minimum by {-cash_gap:.6f} million")


def print_table(title, rows, projections):
    print(f"\n{title} (USD millions)")
    print(f"{'':30}" + "".join(f"{year:>12}" for year in YEARS))
    for label, key in rows:
        print(f"{label:30}" + "".join(f"{projections[year][key]:>12,.1f}" for year in YEARS))


def main():
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be less than the cost of equity.")

    projections = {}
    prior = opening.copy()

    for year in YEARS:
        revenue = prior["revenue"] * (1 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        impairment = IMPAIRMENT
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (prior["floor_plan"] * FLOOR_PLAN_RATE
                    + prior["term_debt"] * TERM_DEBT_RATE
                    + prior["revolver"] * REVOLVER_RATE)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = prior["ppe"] + CAPEX - depreciation
        revenue_change = revenue - prior["revenue"]
        other_working_capital_change = OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
        other_assets = prior["other_assets"] + other_working_capital_change - impairment
        term_debt = prior["term_debt"] - DEBT_REPAYMENT
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - SHARE_BUYBACK

        change_inventory = inventory - prior["inventory"]
        change_floor_plan = floor_plan - prior["floor_plan"]
        fcfe = (net_income + depreciation + impairment - CAPEX - change_inventory
                - other_working_capital_change + change_floor_plan - DEBT_REPAYMENT)

        # Cash is residual after FCFE and buybacks. Draw only to meet the cash floor;
        # otherwise use excess cash to repay any outstanding revolver first.
        cash_before_revolver = prior["cash"] + fcfe - SHARE_BUYBACK
        revolver = prior["revolver"]
        if cash_before_revolver < MINIMUM_CASH:
            draw = MINIMUM_CASH - cash_before_revolver
            revolver += draw
            if revolver > REVOLVER_LIMIT + 1e-6:
                raise AssertionError(f"{year}: revolver exceeds its limit by {revolver - REVOLVER_LIMIT:.6f} million")
            cash = MINIMUM_CASH
        else:
            revolver_repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
            revolver -= revolver_repayment
            cash = cash_before_revolver - revolver_repayment

        statement = {
            "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "cash": cash, "inventory": inventory, "ppe": ppe,
            "other_assets": other_assets, "floor_plan": floor_plan,
            "term_debt": term_debt, "revolver": revolver,
            "other_liabilities": other_liabilities, "equity": equity,
            "other_working_capital_change": other_working_capital_change,
            "change_inventory": change_inventory, "change_floor_plan": change_floor_plan,
            "fcfe": fcfe,
        }
        assert_balanced(year, statement)
        projections[year] = statement
        prior = statement

    print_table("Income statement", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], projections)
    print_table("Balance sheet", [
        ("Cash", "cash"), ("Inventory", "inventory"), ("Property & equipment", "ppe"),
        ("Other assets", "other_assets"), ("Total assets", "total_assets"),
        ("Floor-plan debt", "floor_plan"), ("Term debt", "term_debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"),
        ("Shareholders' equity", "equity"), ("Total liabilities & equity", "total_liabilities_and_equity"),
    ], {year: {**statement, "total_assets": total_assets(statement),
               "total_liabilities_and_equity": total_liabilities_and_equity(statement)}
        for year, statement in projections.items()})
    print_table("Cash flow / free cash flow to equity", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in inventory", "change_inventory"),
        ("Change in other working capital", "other_working_capital_change"),
        ("Change in floor plan", "change_floor_plan"),
        ("Debt repayment", "debt_repayment"), ("FCFE", "fcfe"),
    ], {year: {**statement, "capex": -CAPEX, "debt_repayment": -DEBT_REPAYMENT}
        for year, statement in projections.items()})

    print("\nChecks (USD millions)")
    print(f"{'':30}" + "".join(f"{year:>12}" for year in YEARS))
    print(f"{'Assets - liabilities - equity':30}" + "".join(
        f"{total_assets(projections[year]) - total_liabilities_and_equity(projections[year]):>12,.1f}"
        for year in YEARS))
    print(f"{'Cash above minimum':30}" + "".join(
        f"{projections[year]['cash'] - MINIMUM_CASH:>12,.1f}" for year in YEARS))

    pv_explicit = sum(projections[year]["fcfe"] / (1 + COST_OF_EQUITY) ** (year - 2025) for year in YEARS)
    terminal_fcfe = (projections[2030]["fcfe"] + DEBT_REPAYMENT) * (1 + TERMINAL_GROWTH)
    terminal_value_2030 = terminal_fcfe / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value_2030 / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_explicit + pv_terminal

    print("\nValuation (USD millions except per-share value)")
    print(f"Equity value:                 {equity_value:,.2f}")
    print(f"Share of value after 2030:    {pv_terminal / equity_value:.1%}")
    print(f"Value per share:              ${equity_value / SHARES_OUTSTANDING:,.2f}")


if __name__ == "__main__":
    main()
