"""Lab 16: point-in-time (as-of) filtering for the fictional card-spend table."""

from datetime import date

# Editable inputs
DECISION_DATE = "2026-03-31"
ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "index": 111.0},
]


def show_removed(rule, removed):
    """Print one funnel stage, including original row identifiers."""
    print(f"{rule}: removed {len(removed)} row(s): {[row['row'] for row in removed]}")


def keep_latest_publication(rows):
    """For each ticker/month, retain the row with the newest publication date."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published"] > latest[key]["published"]:
            latest[key] = row
    return list(latest.values())


def print_signals(rows, label):
    """Print percent change from the prior available month to each ticker's latest month."""
    print(f"\n{label}")
    by_ticker = {}
    for row in rows:
        by_ticker.setdefault(row["ticker"], []).append(row)

    for ticker in sorted(by_ticker):
        series = sorted(by_ticker[ticker], key=lambda row: row["month"])
        if len(series) < 2:
            print(f"{ticker}: not enough months for a signal")
            continue
        previous, latest = series[-2], series[-1]
        percent_change = (latest["index"] / previous["index"] - 1) * 100
        print(
            f"{ticker}: {percent_change:+.2f}% "
            f"({previous['month']} to {latest['month']})"
        )


def main():
    decision_date = date.fromisoformat(DECISION_DATE)

    # Rule 1: quarantine missing tickers.
    valid_tickers = [row for row in ROWS if row["ticker"]]
    show_removed("1. Missing ticker (quarantined)", [row for row in ROWS if not row["ticker"]])

    # Rule 2: remove exact duplicates; row number is not part of the data identity.
    seen = set()
    deduplicated = []
    duplicates = []
    for row in valid_tickers:
        identity = (row["ticker"], row["month"], row["published"], row["index"])
        if identity in seen:
            duplicates.append(row)
        else:
            seen.add(identity)
            deduplicated.append(row)
    show_removed("2. Exact duplicates", duplicates)

    # Rule 3: exclude releases that had not happened by the decision date.
    knowable = [
        row for row in deduplicated
        if date.fromisoformat(row["published"]) <= decision_date
    ]
    after_decision = [row for row in deduplicated if row not in knowable]
    show_removed("3. Published after decision date", after_decision)

    # Rule 4: use the latest revision that was knowable on the decision date.
    panel = keep_latest_publication(knowable)
    revised_away = [row for row in knowable if row not in panel]
    show_removed("4. Superseded by a later knowable revision", revised_away)

    print("\nAs-of panel")
    for row in sorted(panel, key=lambda row: (row["ticker"], row["month"])):
        print(
            f"row {row['row']:>2} | {row['ticker']} | {row['month']} | "
            f"published {row['published']} | {row['index']:.1f}"
        )
    print_signals(panel, "As-of signals (decision date: " + DECISION_DATE + ")")

    # Comparison only: apply rules 1 and 2, then select latest publications
    # without considering the decision date.
    naive_panel = keep_latest_publication(deduplicated)
    print_signals(naive_panel, "Naive signals (publication date ignored)")


if __name__ == "__main__":
    main()
