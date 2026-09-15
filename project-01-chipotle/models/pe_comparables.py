"""Comparable-company P/E valuation using only manually entered inputs.

Enter a positive diluted EPS for the target and positive price/EPS values for
each peer. All prices are per share. This script never uses cash or debt.
"""

from statistics import median


# ---------------------------------------------------------------------------
# Editable inputs
# ---------------------------------------------------------------------------
TARGET = {
    "ticker": "ABG",  # Asbury Automotive Group, Inc.
    # FY2024 GAAP diluted EPS from Asbury's FY2024 Form 10-K / earnings release.
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "diluted_eps": 36.81},
]


def normalized_ticker(value):
    """Normalize a ticker/name for target exclusion and peer deduplication."""
    return str(value).strip().upper()


def positive_number(value):
    """Return True only for usable positive numeric inputs."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def format_price(value):
    return f"${value:,.2f}"


def format_change(value):
    return f"${value:+,.2f}"


target_ticker = normalized_ticker(TARGET["ticker"])
target_eps = TARGET["diluted_eps"]

unique_peers = []
seen_tickers = set()
for peer in PEERS:
    ticker = normalized_ticker(peer.get("ticker", ""))
    if not ticker:
        print("Excluded peer with a missing ticker.")
        continue
    if ticker == target_ticker:
        print(f"Excluded {ticker}: it is the target company.")
        continue
    if ticker in seen_tickers:
        print(f"Excluded duplicate peer: {ticker}.")
        continue
    seen_tickers.add(ticker)
    unique_peers.append({**peer, "ticker": ticker})

print(f"Target: {target_ticker}")
if not positive_number(target_eps):
    print("Target diluted EPS: not meaningful (missing or nonpositive).")
else:
    print(f"Target diluted EPS: {target_eps:.6f}")

print("\nPeer P/E multiples")
usable_peers = []
for peer in unique_peers:
    price = peer.get("price")
    diluted_eps = peer.get("diluted_eps")
    if not positive_number(price) or not positive_number(diluted_eps):
        peer["pe"] = None
        print(f"{peer['ticker']}: not meaningful (missing or nonpositive price or diluted EPS)")
        continue
    peer["pe"] = price / diluted_eps
    usable_peers.append(peer)
    print(f"{peer['ticker']}: {peer['pe']:.6f}x")


def implied_price(pe_multiple):
    """Return the target implied price, or None if target EPS is unusable."""
    if not positive_number(target_eps):
        return None
    return pe_multiple * target_eps


def print_estimate(label, pe_multiple):
    price = implied_price(pe_multiple)
    if price is None:
        print(f"{label}: not meaningful (target diluted EPS is missing or nonpositive).")
    else:
        print(f"{label}: {pe_multiple:.6f}x -> {format_price(price)}")


if not usable_peers:
    print("\nPeer valuation: no usable peers.")
    full_median_pe = None
    full_median_price = None
elif len(usable_peers) == 1:
    full_median_pe = usable_peers[0]["pe"]
    full_median_price = implied_price(full_median_pe)
    print("\nPeer valuation: reference estimate only (one usable peer; no range).")
    print_estimate("Reference P/E and implied price", full_median_pe)
else:
    peer_multiples = [peer["pe"] for peer in usable_peers]
    minimum_pe = min(peer_multiples)
    full_median_pe = median(peer_multiples)
    maximum_pe = max(peer_multiples)
    full_median_price = implied_price(full_median_pe)
    print("\nPeer valuation")
    print_estimate("Minimum P/E and implied price", minimum_pe)
    print_estimate("Median P/E and implied price", full_median_pe)
    print_estimate("Maximum P/E and implied price", maximum_pe)


print("\nPeer-removal check")
if not unique_peers:
    print("No peers to remove.")
elif full_median_price is None:
    print("No estimate: no usable full-peer median or target diluted EPS.")
else:
    for removed_peer in unique_peers:
        remaining_multiples = [
            peer["pe"]
            for peer in usable_peers
            if peer["ticker"] != removed_peer["ticker"]
        ]
        if not remaining_multiples:
            print(f"Remove {removed_peer['ticker']}: no estimate (no usable peers remain).")
            continue
        remaining_median_pe = median(remaining_multiples)
        remaining_price = implied_price(remaining_median_pe)
        dollar_change = remaining_price - full_median_price
        estimate_label = "median implied price"
        if len(remaining_multiples) == 1:
            estimate_label = "reference implied price (one usable peer remains; no range)"
        print(
            f"Remove {removed_peer['ticker']}: "
            f"{estimate_label} {format_price(remaining_price)}; "
            f"change from full-peer estimate {format_change(dollar_change)}"
        )
