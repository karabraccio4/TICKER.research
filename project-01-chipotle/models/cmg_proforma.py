"""CMG five-year pro forma and FCFE valuation (USD millions except per-share data).

Opening data: CMG FY2025 Form 10-K, accession 0001058090-26-000009.
Forecast assumptions and evidence: research/cmg-history-and-assumptions.md.
"""

import sys

YEARS = range(2026, 2031)

# Assumptions: guidance, history, and documented judgments.
REVENUE_GROWTH = {2026: 0.090, 2027: 0.070, 2028: 0.065, 2029: 0.060, 2030: 0.055}
GROSS_MARGIN = 0.255
FOOD_BEVERAGE_PACKAGING_TO_REVENUE = 0.296
SGA_TO_GROSS_PROFIT = 0.215
DEPRECIATION_TO_OPENING_PPE = 0.151
CAPEX = {2026: 834.1, 2027: 850.0, 2028: 850.0, 2029: 850.0, 2030: 850.0}
TAX_RATE = 0.236
INVENTORY_DAYS = 5.1
PREOPENING_TO_REVENUE = 49.507 / 11925.601
IMPAIRMENT_TO_REVENUE = 27.503 / 11925.601
INTEREST_INCOME_TO_REVENUE = 73.721 / 11925.601
COST_OF_EQUITY = 0.090
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 1302.423  # millions; January 30, 2026 shares outstanding
MINIMUM_CASH = 25.0
BREAK_CASH_TEST = "--break-cash" in sys.argv

# FY2025 opening balance sheet, USD millions.
opening = {
    "revenue": 11925.601,
    "cash": 350.545,
    "accounts_receivable": 156.466,
    "inventory": 49.508,
    "prepaids": 120.450,
    "income_tax_receivable": 91.393,
    "investments": 895.714,
    "restricted_cash": 35.364,
    "ppe": 2679.361,
    "operating_lease_assets": 4463.010,
    "other_assets": 152.720,
    "accounts_payable": 212.813,
    "accrued_payroll": 250.126,
    "accrued_liabilities": 182.448,
    "unearned_revenue": 240.375,
    "operating_lease_liabilities": 5075.814,
    "deferred_tax_liabilities": 125.674,
    "other_liabilities": 76.674,
    "equity": 2830.607,
}


def total_assets(s):
    return sum(s[k] for k in (
        "cash", "accounts_receivable", "inventory", "prepaids", "income_tax_receivable",
        "investments", "restricted_cash", "ppe", "operating_lease_assets", "other_assets",
    ))


def total_liabilities_and_equity(s):
    return sum(s[k] for k in (
        "accounts_payable", "accrued_payroll", "accrued_liabilities", "unearned_revenue",
        "operating_lease_liabilities", "deferred_tax_liabilities", "other_liabilities", "equity",
    ))


def assert_balanced(year, s):
    gap = total_assets(s) - total_liabilities_and_equity(s)
    if abs(gap) > 1e-6:
        raise AssertionError(f"FY{year}E: balance sheet gap is {gap:.6f} million")
    cash_gap = s["cash"] - MINIMUM_CASH
    if cash_gap < -1e-6:
        raise AssertionError(f"FY{year}E: cash is below the minimum by {-cash_gap:.6f} million")


def print_table(title, rows, projections):
    print(f"\n{title} (USD millions)")
    print(f"{'':34}" + "".join(f"{year:>12}" for year in YEARS))
    for label, key in rows:
        print(f"{label:34}" + "".join(f"{projections[y][key]:>12,.1f}" for y in YEARS))


def main():
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be less than the cost of equity.")

    projections = {}
    prior = opening.copy()
    for year in YEARS:
        revenue = prior["revenue"] * (1 + REVENUE_GROWTH[year])
        gross_profit = revenue * GROSS_MARGIN
        food_labor_occupancy_other = revenue - gross_profit
        food_beverage_packaging = revenue * FOOD_BEVERAGE_PACKAGING_TO_REVENUE
        sga = gross_profit * SGA_TO_GROSS_PROFIT
        depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        preopening = revenue * PREOPENING_TO_REVENUE
        impairment = revenue * IMPAIRMENT_TO_REVENUE
        operating_income = gross_profit - sga - depreciation - preopening - impairment
        interest_income = revenue * INTEREST_INCOME_TO_REVENUE
        pretax_income = operating_income + interest_income
        tax = pretax_income * TAX_RATE
        net_income = pretax_income - tax

        accounts_receivable = revenue * opening["accounts_receivable"] / opening["revenue"]
        inventory = food_beverage_packaging * INVENTORY_DAYS / 365
        prepaids = revenue * opening["prepaids"] / opening["revenue"]
        income_tax_receivable = revenue * opening["income_tax_receivable"] / opening["revenue"]
        investments = opening["investments"]
        restricted_cash = opening["restricted_cash"]
        ppe = prior["ppe"] + CAPEX[year] - depreciation
        operating_lease_assets = revenue * opening["operating_lease_assets"] / opening["revenue"]
        other_assets = revenue * opening["other_assets"] / opening["revenue"]
        accounts_payable = revenue * opening["accounts_payable"] / opening["revenue"]
        accrued_payroll = revenue * opening["accrued_payroll"] / opening["revenue"]
        accrued_liabilities = revenue * opening["accrued_liabilities"] / opening["revenue"]
        unearned_revenue = revenue * opening["unearned_revenue"] / opening["revenue"]
        operating_lease_liabilities = revenue * opening["operating_lease_liabilities"] / opening["revenue"]
        deferred_tax_liabilities = revenue * opening["deferred_tax_liabilities"] / opening["revenue"]
        other_liabilities = revenue * opening["other_liabilities"] / opening["revenue"]
        equity = prior["equity"] + net_income

        change_nwc = ((accounts_receivable + inventory + prepaids + income_tax_receivable)
                      - (accounts_payable + accrued_payroll + accrued_liabilities + unearned_revenue)
                      - ((prior["accounts_receivable"] + prior["inventory"] + prior["prepaids"] + prior["income_tax_receivable"])
                         - (prior["accounts_payable"] + prior["accrued_payroll"] + prior["accrued_liabilities"] + prior["unearned_revenue"])))
        fcfe = net_income + depreciation + impairment - CAPEX[year] - change_nwc

        # Cash is the balancing account after the operational forecast. CMG has no floor-plan debt.
        noncash_assets = (accounts_receivable + inventory + prepaids + income_tax_receivable + investments
                          + restricted_cash + ppe + operating_lease_assets + other_assets)
        liabilities_and_equity = (accounts_payable + accrued_payroll + accrued_liabilities + unearned_revenue
                                  + operating_lease_liabilities + deferred_tax_liabilities + other_liabilities + equity)
        cash = liabilities_and_equity - noncash_assets
        if BREAK_CASH_TEST and year == 2026:
            cash = prior["cash"]  # Deliberately corrupt FY2026E cash to test the balance-sheet assertion.

        s = locals().copy()
        s["cash"] = cash
        assert_balanced(year, s)
        projections[year] = s
        prior = s

    print_table("Income statement", [
        ("Revenue", "revenue"), ("Food, beverage & packaging", "food_beverage_packaging"),
        ("Restaurant operating costs", "food_labor_occupancy_other"),
        ("Gross profit (derived)", "gross_profit"), ("G&A", "sga"),
        ("Depreciation & amortization", "depreciation"), ("Pre-opening", "preopening"),
        ("Impairment", "impairment"), ("Operating income", "operating_income"),
        ("Interest and other income", "interest_income"), ("Pretax income", "pretax_income"),
        ("Tax", "tax"), ("Net income", "net_income"),
    ], projections)
    print_table("Balance sheet", [
        ("Cash", "cash"), ("Accounts receivable", "accounts_receivable"), ("Inventory", "inventory"),
        ("Investments", "investments"), ("PP&E, net", "ppe"), ("Operating lease assets", "operating_lease_assets"),
        ("Total assets", "total_assets"), ("Accounts payable", "accounts_payable"),
        ("Operating lease liabilities", "operating_lease_liabilities"), ("Shareholders' equity", "equity"),
        ("Total liabilities & equity", "total_liabilities_and_equity"),
    ], {y: {**s, "total_assets": total_assets(s), "total_liabilities_and_equity": total_liabilities_and_equity(s)} for y, s in projections.items()})
    print_table("Cash flow / FCFE", [
        ("Net income", "net_income"), ("Depreciation & amortization", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in working capital", "change_nwc"), ("FCFE", "fcfe"),
    ], {y: {**s, "capex": -CAPEX[y], "change_nwc": -s["change_nwc"]} for y, s in projections.items()})
    print("\nChecks (USD millions)")
    print(f"{'':34}" + "".join(f"{year:>12}" for year in YEARS))
    print(f"{'Assets - liabilities - equity':34}" + "".join(f"{total_assets(projections[y]) - total_liabilities_and_equity(projections[y]):>12,.1f}" for y in YEARS))
    print(f"{'Cash above minimum':34}" + "".join(f"{projections[y]['cash'] - MINIMUM_CASH:>12,.1f}" for y in YEARS))

    pv_explicit = sum(projections[y]["fcfe"] / (1 + COST_OF_EQUITY) ** (y - 2025) for y in YEARS)
    terminal_fcfe = projections[2030]["fcfe"] * (1 + TERMINAL_GROWTH)
    pv_terminal = terminal_fcfe / (COST_OF_EQUITY - TERMINAL_GROWTH) / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_explicit + pv_terminal
    print("\nValuation (USD millions except per-share value)")
    print(f"Equity value:                 {equity_value:,.2f}")
    print(f"Share of value after 2030:    {pv_terminal / equity_value:.1%}")
    print(f"Value per share:              ${equity_value / SHARES_OUTSTANDING:,.2f}")


if __name__ == "__main__":
    main()
