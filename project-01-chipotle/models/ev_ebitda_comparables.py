"""Comparable-company EV/EBITDA analysis using a consistent lease convention.

All values are USD millions except prices and per-share values. Operating lease
liabilities are excluded from debt and EBITDA is calculated as reported
operating income plus depreciation and amortization for every company.
Source detail and qualifications are in My_Own_Peer_Policy.md.
"""


TARGET = {
    "ticker": "CMG",
    "price": 38.45,
    "diluted_shares": 1342.616,
    "cash": 350.545,
    "funded_debt": 0.0,
    "operating_income": 1935.798,
    "depreciation_and_amortization": 361.382,
}

PEERS = [
    {
        "ticker": "CAVA",
        # February 5, 2026 historical market capitalization.
        "market_cap": 7487.000,
        "cash": 366.120,
        "funded_debt": 0.0,
        "operating_income": 43.118,
        "depreciation_and_amortization": 60.355,
    },
    {
        "ticker": "SG",
        # February 5, 2026 historical market capitalization.
        "market_cap": 697.661,
        "cash": 214.789,
        "funded_debt": 0.0,
        "operating_income": -95.704,
        "depreciation_and_amortization": 67.346,
    },
]


def enterprise_value(market_cap, funded_debt, cash):
    """Return EV under the project's funded-debt-only lease convention."""
    return market_cap + funded_debt - cash


def ebitda(operating_income, depreciation_and_amortization):
    """Return consistently defined reported EBITDA."""
    return operating_income + depreciation_and_amortization


def main():
    target_market_cap = TARGET["price"] * TARGET["diluted_shares"]
    target_ev = enterprise_value(
        target_market_cap, TARGET["funded_debt"], TARGET["cash"]
    )
    target_ebitda = ebitda(
        TARGET["operating_income"], TARGET["depreciation_and_amortization"]
    )

    print("Comparable-company EV/EBITDA (USD millions except prices and per-share values)")
    print("Convention: exclude operating lease liabilities from debt and use reported EBITDA.")
    print(
        f"CMG: market cap ${target_market_cap:,.1f}; EV ${target_ev:,.1f}; "
        f"EBITDA ${target_ebitda:,.1f}; EV/EBITDA {target_ev / target_ebitda:.2f}x"
    )

    usable = []
    for peer in PEERS:
        peer_ev = enterprise_value(peer["market_cap"], peer["funded_debt"], peer["cash"])
        peer_ebitda = ebitda(peer["operating_income"], peer["depreciation_and_amortization"])
        if peer_ebitda <= 0:
            print(
                f"{peer['ticker']}: market cap ${peer['market_cap']:,.1f}; EV ${peer_ev:,.1f}; "
                f"EBITDA ${peer_ebitda:,.1f}; EV/EBITDA not meaningful (nonpositive EBITDA)."
            )
            continue
        multiple = peer_ev / peer_ebitda
        usable.append((peer["ticker"], multiple))
        print(
            f"{peer['ticker']}: market cap ${peer['market_cap']:,.1f}; EV ${peer_ev:,.1f}; "
            f"EBITDA ${peer_ebitda:,.1f}; EV/EBITDA {multiple:.2f}x"
        )

    if len(usable) != 1:
        print("No single-peer EV/EBITDA reference is available.")
        return

    ticker, multiple = usable[0]
    implied_ev = multiple * target_ebitda
    implied_equity_value = implied_ev + TARGET["cash"] - TARGET["funded_debt"]
    implied_price = implied_equity_value / TARGET["diluted_shares"]
    print(
        f"\n{ticker} reference only: {multiple:.2f}x applied to CMG EBITDA ${target_ebitda:,.1f} "
        f"= implied CMG EV ${implied_ev:,.1f}; implied equity value ${implied_equity_value:,.1f}; "
        f"implied value per share ${implied_price:,.2f}."
    )


if __name__ == "__main__":
    main()
