"""CMG five-year pro forma and FCFE valuation (USD millions except per-share data).

LAB 10 SUPPORTING EVIDENCE
==========================
Sources: FY2023 10-K (0001562762-24-000023):
https://www.sec.gov/Archives/edgar/data/0001058090/000156276224000023/cmg-20231231x10k.htm
FY2024 10-K (0001058090-25-000014):
https://www.sec.gov/Archives/edgar/data/0001058090/000105809025000014/cmg-20241231.htm
FY2025 10-K (0001058090-26-000009):
https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000009/cmg-20251231.htm

History (USD millions; each year is sourced to its respective 10-K)
Line                                  FY2023     FY2024     FY2025
Revenue                            9,871.649 11,313.853 11,925.601
Gross profit (derived*)            2,586.092  3,017.692  3,026.207
G&A                                  633.584    697.483    652.017
Net income                        1,228.737  1,534.110  1,535.761
Inventory                            39.309     48.942     49.508
Net PP&E                          2,170.038  2,390.126  2,679.361
Shareholders' equity              3,062.207  3,655.546  2,830.607
*CMG does not report gross profit. It is calculated as revenue less food,
beverage and packaging, labor, occupancy, and other restaurant operating costs.

Ratio                               FY2023     FY2024     FY2025
Gross margin                         26.2%      26.7%      25.4%
G&A / gross profit                   24.5%      23.1%      21.5%
Inventory days                        4.9        5.3        5.1
D&A / opening PP&E                   16.4%      15.4%      15.1%
Cash capex                         (560.731)  (593.603)  (666.336)
Tax rate                              24.2%      23.7%      23.6%
Reported growth                       14.3%      14.6%       5.4%
Comparable restaurant sales            7.9%       7.4%      (1.7)%

Assumptions: value | label | reason
FY2026 comps flat | Guidance | Management's stated outlook.
FY2026 openings 350-370 | Guidance | Management's stated opening target.
FY2026 revenue growth 9.0% | Judgment | New openings add sales despite flat comps;
I round down because new restaurants contribute for only part of the year.
FY2027-30 growth 7.0%, 6.5%, 6.0%, 5.5% | Judgment | Growth tapers as the store base grows.
Gross margin 25.5%; G&A / GP 21.5%; inventory days 5.1; D&A / opening PP&E 15.1%;
tax rate 23.6% | History | Each uses the latest reported historical ratio.
FY2026 capex $834.1m | Guidance | Management's stated forecast.
FY2027-30 capex $850m | Judgment | Keeps capex near guidance to support stores and equipment.
Floor-plan financing none; revolver $0 drawn, $500m available | History | CMG has no floor-plan debt.
Terminal growth 2.5%; cost of equity 9.0% | Judgment | Conservative long-run growth; provisional rate pending CAPM.

Confirmed by hand: FY2025 total revenue was $11,925.601m; FY2025 purchases of
leasehold improvements, property and equipment (cash capex) were ($666.336m).

Partner review: The partner asked why FY2026 growth is 9.0% if comps are flat.
I chose it because 350-370 openings add sales, but rounded down for partial-year
contributions; I would lower it if openings miss guidance or comps decline and
raise it only if openings are achieved and comps turn positive.
My Apple question: How did you decide your revenue-growth assumption, and what
evidence would make you revise it? My attack: the revenue-growth judgment does
not separate Services from product-cycle and geographic risk; it should show
the mix or a sensitivity. The recorded answer is that it uses FY2025 sales and
Services growth, but would fall if iPhone, China, or Services demand weakens.

CMG calls organic growth comparable restaurant sales. ABG's 1.8% organic growth
excludes acquisition/portfolio effects included in its 4.7% reported growth.
I would defend History longest because it is audited and traceable; CMG's 5.4%
revenue growth alongside (1.7)% comparable sales was the surprising result.

Check proof: normal run prints zero balance-sheet gaps and cash above a $25.0m
floor. `python models/cmg_proforma.py --break-cash` corrupts FY2026E cash and
raises `AssertionError: FY2026E: balance sheet gap is -1348.549015 million`.
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
