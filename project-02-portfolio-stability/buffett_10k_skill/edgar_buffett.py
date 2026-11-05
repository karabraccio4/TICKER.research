"""Download 10-K facts from SEC EDGAR and compute a legend-investor panel.

Run:
    $env:SEC_EDGAR_EMAIL = "your.email@example.edu"
    python buffett_10k_skill/edgar_buffett.py COST --panel-memos .

The SEC asks automated users to identify themselves.  This program never
estimates: a missing fact stays ``not found`` and a check without every input
stays ``not known``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
REQUIRED_EMAIL_MESSAGE = (
    "Set SEC_EDGAR_EMAIL to your email address so EDGAR receives the required "
    "identifying User-Agent (example: $env:SEC_EDGAR_EMAIL = 'name@school.edu')."
)
TAG_OPTIONS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
    "equity": ["StockholdersEquity"],
    "liabilities": ["Liabilities"],
    "assets_current": ["AssetsCurrent"],
    "liabilities_current": ["LiabilitiesCurrent"],
}
FLOW_FIELDS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}
GRAHAM_CURRENT_RATIO_THRESHOLD = 2.0
DISPLAY_NAMES = {
    "revenue": "Revenue",
    "net_income": "Net income",
    "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending",
    "equity": "Equity",
    "liabilities": "Liabilities",
    "assets_current": "Current assets",
    "liabilities_current": "Current liabilities",
}


def sec_get(url: str, email: str) -> dict[str, Any]:
    """Get a JSON EDGAR endpoint with an identifying, keyless User-Agent."""
    request = Request(
        url,
        headers={
            "User-Agent": f"FIN 43900 Lab 18 {email}",
            "Host": "www.sec.gov" if "www.sec.gov" in url else "data.sec.gov",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"SEC EDGAR returned HTTP {error.code} for {url}.") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach SEC EDGAR: {error.reason}") from error


def ticker_to_cik(ticker: str, email: str) -> int:
    """Look up an SEC CIK using the SEC's published ticker file."""
    entries = sec_get(TICKERS_URL, email)
    ticker = ticker.upper()
    for entry in entries.values():
        if entry["ticker"].upper() == ticker:
            return int(entry["cik_str"])
    raise ValueError(f"Ticker {ticker!r} was not found in SEC company_tickers.json.")


def monetary_units(fact: dict[str, Any]) -> list[dict[str, Any]]:
    """Return USD facts.  EDGAR facts may also carry per-share or share units."""
    return fact.get("units", {}).get("USD", [])


def is_annual_10k(item: dict[str, Any], field: str) -> bool:
    """Keep annual 10-K observations, and require a one-year duration for flows."""
    if item.get("form") != "10-K" or item.get("fp") != "FY":
        return False
    if field not in FLOW_FIELDS:
        return True
    start, end = item.get("start"), item.get("end")
    if not start or not end:
        return False
    days = (date.fromisoformat(end) - date.fromisoformat(start)).days
    return 300 <= days <= 380


def pick_fact_for_year(
    facts: dict[str, Any], field: str, fiscal_year_end: str
) -> tuple[dict[str, Any] | None, str | None]:
    """Select a field for one FY: tag preference first, newest filing wins next.

    This is the core row-building rule.  Companyfacts can contain the same
    annual period in successive 10-K filings.  Matching the actual fiscal-year
    end (rather than EDGAR's ``fy`` filing label) and sorting by ``filed``
    descending deliberately makes the newer filing control.
    """
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in TAG_OPTIONS[field]:
        candidates = [
            item
            for item in monetary_units(gaap.get(tag, {}))
            if item.get("end") == fiscal_year_end and is_annual_10k(item, field)
        ]
        if candidates:
            return max(candidates, key=lambda item: item.get("filed", "")), tag
    return None, None


def fiscal_year_ends(facts: dict[str, Any]) -> list[tuple[int, str]]:
    """Find fiscal-year-end dates from annual 10-K revenue facts.

    Companyfacts also includes annual-looking contexts for benefit plans and
    other disclosures that do not represent the company's fiscal year. Revenue
    is a required operating flow and therefore anchors the five company years.
    """
    discovered: set[str] = set()
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in TAG_OPTIONS["revenue"]:
        for item in monetary_units(gaap.get(tag, {})):
            if is_annual_10k(item, "revenue") and item.get("end"):
                discovered.add(item["end"])
    return [(int(end[:4]), end) for end in sorted(discovered)[-5:]]


def display(value: float | None) -> str:
    """Format millions for people while preserving the no-estimates rule."""
    return "not found" if value is None else f"{value:,.0f}"


def display_percent(value: float | None) -> str:
    return "not known" if value is None else f"{value * 100:.1f}%"


def display_ratio(value: float | None) -> str:
    """Format ratios as ratios, never as percentages."""
    return "not known" if value is None else f"{value:.2f}"


def value_in_millions(item: dict[str, Any] | None) -> float | None:
    return None if item is None else float(item["val"]) / 1_000_000


def check_every(values: list[float | None], predicate) -> str:
    if any(value is None for value in values):
        return "not known"
    return "pass" if all(predicate(value) for value in values) else "fail"


def build_rows(facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn EDGAR facts into five annual rows, including tags and derived values."""
    rows: list[dict[str, Any]] = []
    for fiscal_year, fiscal_year_end in fiscal_year_ends(facts):
        row: dict[str, Any] = {"fiscal_year": fiscal_year, "fiscal_year_end": fiscal_year_end, "tags": {}}
        for field in TAG_OPTIONS:
            item, tag = pick_fact_for_year(facts, field, fiscal_year_end)
            row[field] = value_in_millions(item)
            row["tags"][field] = tag or "not found"
        equity = row["equity"]
        net_income = row["net_income"]
        row["roe"] = None if equity is None or equity <= 0 or net_income is None else net_income / equity
        ocf, capex = row["operating_cash_flow"], row["capital_spending"]
        row["owner_earnings"] = None if ocf is None or capex is None else ocf - capex
        current_assets, current_liabilities = row["assets_current"], row["liabilities_current"]
        row["current_ratio"] = (
            None
            if current_assets is None or current_liabilities is None or current_liabilities <= 0
            else current_assets / current_liabilities
        )
        liabilities = row["liabilities"]
        row["liabilities_to_equity"] = (
            None if liabilities is None or equity is None or equity <= 0 else liabilities / equity
        )
        rows.append(row)
    return rows


def growth_check(values: list[float | None]) -> str:
    """Return a first-to-last growth result without assuming intermediate values."""
    if len(values) != 5 or values[0] is None or values[-1] is None:
        return "not known"
    return "pass" if values[-1] > values[0] else "fail"


def make_buffett_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Compute all three Buffett checks strictly from the five output rows."""
    roe = [row["roe"] for row in rows]
    owner_earnings = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": check_every(roe, lambda value: value >= 0.15),
        "Owner earnings positive every year": check_every(owner_earnings, lambda value: value > 0),
        "Owner earnings grew, first year to last": growth_check(owner_earnings),
    }


def make_graham_checks(
    rows: list[dict[str, Any]], current_ratio_threshold: float = GRAHAM_CURRENT_RATIO_THRESHOLD
) -> dict[str, str]:
    """Compute Lab 19's stated Graham screens from the shared five-year rows."""
    current_ratio = rows[-1]["current_ratio"] if rows else None
    net_income = [row["net_income"] for row in rows]
    latest_ratio = "not known" if current_ratio is None else ("pass" if current_ratio >= current_ratio_threshold else "fail")
    return {
        f"Current ratio of {current_ratio_threshold:g} or more, latest year": latest_ratio,
        "Net income positive every year": check_every(net_income, lambda value: value > 0),
        "Net income grew, first year to last": growth_check(net_income),
    }


def make_burry_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Compute Lab 19's stated Burry screens from the shared five-year rows."""
    cash_covers_income: list[float | None] = []
    for row in rows:
        ocf, income = row["operating_cash_flow"], row["net_income"]
        cash_covers_income.append(None if ocf is None or income is None else ocf - income)
    leverage = rows[-1]["liabilities_to_equity"] if rows else None
    leverage_result = "not known" if leverage is None else ("pass" if leverage <= 2 else "fail")
    return {
        "Operating cash flow at least net income every year": check_every(cash_covers_income, lambda difference: difference >= 0),
        "Liabilities no more than twice equity, latest year": leverage_result,
    }


def make_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Compatibility alias for Lab 18 callers that only need Buffett's checks."""
    return make_buffett_checks(rows)


def make_panel_checks(
    rows: list[dict[str, Any]], current_ratio_threshold: float = GRAHAM_CURRENT_RATIO_THRESHOLD
) -> dict[str, dict[str, str]]:
    return {
        "Buffett": make_buffett_checks(rows),
        "Graham": make_graham_checks(rows, current_ratio_threshold),
        "Burry": make_burry_checks(rows),
    }


def analysis_for_ticker(
    ticker: str, email: str, current_ratio_threshold: float = GRAHAM_CURRENT_RATIO_THRESHOLD
) -> dict[str, Any]:
    cik = ticker_to_cik(ticker, email)
    facts = sec_get(FACTS_URL.format(cik=cik), email)
    rows = build_rows(facts)
    if len(rows) != 5:
        raise RuntimeError(f"EDGAR supplied only {len(rows)} fiscal years of annual 10-K facts; need five.")
    return {
        "ticker": ticker.upper(),
        "company": facts.get("entityName", ticker.upper()),
        "cik": f"{cik:010d}",
        "units": "USD millions (except ratios)",
        "rows": rows,
        "checks": make_buffett_checks(rows),
        "panel_checks": make_panel_checks(rows, current_ratio_threshold),
    }


def print_report(analysis: dict[str, Any]) -> None:
    """Print every permitted memo number and its source XBRL tag."""
    print(f"{analysis['company']} ({analysis['ticker']}) | CIK {analysis['cik']}")
    print("All dollars are USD millions. Source: SEC EDGAR companyfacts, annual 10-K only.")
    print("\nFiscal year end | Revenue [tag] | Net income [tag] | Operating cash flow [tag] | Capital spending [tag] | Equity [tag] | Liabilities [tag] | Current assets [tag] | Current liabilities [tag] | ROE | Current ratio | Liabilities/equity | Owner earnings")
    for row in analysis["rows"]:
        tags = row["tags"]
        print(
            f"{row['fiscal_year_end']} | {display(row['revenue'])} [{tags['revenue']}] | "
            f"{display(row['net_income'])} [{tags['net_income']}] | "
            f"{display(row['operating_cash_flow'])} [{tags['operating_cash_flow']}] | "
            f"{display(row['capital_spending'])} [{tags['capital_spending']}] | "
            f"{display(row['equity'])} [{tags['equity']}] | "
            f"{display(row['liabilities'])} [{tags['liabilities']}] | "
            f"{display(row['assets_current'])} [{tags['assets_current']}] | "
            f"{display(row['liabilities_current'])} [{tags['liabilities_current']}] | "
            f"{display_percent(row['roe'])} | {display_ratio(row['current_ratio'])} | "
            f"{display_ratio(row['liabilities_to_equity'])} | "
            f"{display(row['owner_earnings'])}"
        )
    print("\nPanel checks")
    for investor, checks in analysis["panel_checks"].items():
        for check, outcome in checks.items():
            print(f"- {investor} | {check}: {outcome}")


def panel_verdict(checks: dict[str, str]) -> str:
    """Turn deterministic checks into a conservative memo starting verdict."""
    if any(result == "not known" for result in checks.values()):
        return "watch it"
    return "own the business" if all(result == "pass" for result in checks.values()) else "watch it"


def memo_template(analysis: dict[str, Any], investor: str = "Buffett") -> str:
    """Return an investor-specific memo shell restricted to printed script values."""
    checks = analysis["panel_checks"][investor]
    verdict = panel_verdict(checks)
    lenses = {
        "Buffett": "I judge the business, not its price.",
        "Graham": "I emphasize conservative financial condition and earnings stability, not price in this lab.",
        "Burry": "I test whether earnings are supported by cash and whether leverage is contained.",
    }
    checks_text = "; ".join(f"{check} — {outcome}" for check, outcome in checks.items())
    return f"""# {investor}-style memo: {analysis['ticker']}

## Verdict: {verdict}

{lenses[investor]} This memo uses only the SEC EDGAR annual-filing facts printed by `edgar_buffett.py`, in USD millions.

The code checks are: {checks_text}.

Write the final {investor}-style reasoning here using only numbers shown in the script output. If a check is not known because an input is not found, say that the business cannot be judged on that check. Do not discuss stock price or add a number not printed by the script.

## My decision

I trust the verdict only to the extent that the EDGAR facts and the stated checks capture the business; it is a disciplined operating-quality screen, not an investment recommendation.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="US ticker, e.g. COST")
    parser.add_argument("--json", action="store_true", help="print the analysis as JSON")
    parser.add_argument("--memo", type=Path, help="write a Buffett memo shell to this Markdown file")
    parser.add_argument("--panel-memos", type=Path, help="write Buffett, Graham, and Burry memo shells into this directory")
    parser.add_argument("--email", help="EDGAR contact email; defaults to SEC_EDGAR_EMAIL")
    parser.add_argument(
        "--graham-current-ratio-threshold", type=float, default=GRAHAM_CURRENT_RATIO_THRESHOLD,
        help="Graham current-ratio threshold; default 2.0, use 1.0 only for the Lab 19 sensitivity probe",
    )
    args = parser.parse_args()
    email = args.email or os.environ.get("SEC_EDGAR_EMAIL")
    if not email or "@" not in email:
        raise SystemExit(REQUIRED_EMAIL_MESSAGE)
    try:
        analysis = analysis_for_ticker(args.ticker, email, args.graham_current_ratio_threshold)
    except (RuntimeError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error
    if args.memo:
        args.memo.write_text(memo_template(analysis), encoding="utf-8")
        print(f"Wrote memo shell: {args.memo}")
    if args.panel_memos:
        args.panel_memos.mkdir(parents=True, exist_ok=True)
        for investor in ("Buffett", "Graham", "Burry"):
            path = args.panel_memos / f"{investor.lower()}_memo_{analysis['ticker']}.md"
            path.write_text(memo_template(analysis, investor), encoding="utf-8")
            print(f"Wrote memo shell: {path}")
    print(json.dumps(analysis, indent=2) if args.json else "")
    if not args.json:
        print_report(analysis)


if __name__ == "__main__":
    main()
