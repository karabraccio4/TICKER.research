"""Streamlit front end for the Lab 19 SEC EDGAR legend-investor panel."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

from buffett_10k_skill.edgar_buffett import analysis_for_ticker, display, display_percent, display_ratio, panel_verdict

MEMO_NUMBER = re.compile(r"(?<![A-Za-z])[-+]?\d[\d,]*(?:\.\d+)?%?")
INVESTORS = ("Buffett", "Graham", "Burry")


@st.cache_data(ttl=3600, show_spinner=False)
def get_analysis(ticker: str, email: str) -> dict:
    """Cache keyless SEC results briefly while retaining shared source facts."""
    return analysis_for_ticker(ticker, email)


def table_frame(analysis: dict) -> pd.DataFrame:
    """Show all source facts and their XBRL tags in the five-year table."""
    records = []
    fields = [
        ("revenue", "Revenue"), ("net_income", "Net income"),
        ("operating_cash_flow", "Operating cash flow"), ("capital_spending", "Capital spending"),
        ("equity", "Equity"), ("liabilities", "Liabilities"),
        ("assets_current", "Current assets"), ("liabilities_current", "Current liabilities"),
    ]
    for row in analysis["rows"]:
        record = {"Fiscal year end": row["fiscal_year_end"]}
        for key, label in fields:
            record[label], record[f"{label} XBRL tag"] = display(row[key]), row["tags"][key]
        record["ROE"] = display_percent(row["roe"])
        record["Current ratio"] = display_ratio(row["current_ratio"])
        record["Liabilities / equity"] = display_ratio(row["liabilities_to_equity"])
        record["Owner earnings"] = display(row["owner_earnings"])
        records.append(record)
    return pd.DataFrame(records)


def panel_frame(analysis: dict) -> pd.DataFrame:
    """Make the investor-by-check table from code rather than model judgment."""
    return pd.DataFrame(
        {"Investor": investor, "Check": check, "Result": result}
        for investor, checks in analysis["panel_checks"].items()
        for check, result in checks.items()
    )


def allowed_memo_numbers(analysis: dict) -> set[str]:
    """Build the numeric vocabulary printed by the report and panel checks."""
    allowed = {"15", "15%", "2"}
    source_fields = ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "owner_earnings"]
    for row in analysis["rows"]:
        allowed.update(re.findall(r"\d+(?:\.\d+)?", row["fiscal_year_end"]))
        for field in source_fields:
            if row[field] is not None:
                shown = display(row[field])
                allowed.update({shown, shown.replace(",", "")})
        for field in ("roe",):
            if row[field] is not None:
                shown = display_percent(row[field])
                allowed.update({shown, shown.rstrip("%")})
        for field in ("current_ratio", "liabilities_to_equity"):
            if row[field] is not None:
                allowed.add(display_ratio(row[field]))
    return allowed


def unprinted_memo_numbers(memos: dict[str, str], analysis: dict) -> dict[str, list[str]]:
    """Flag every number each memo uses that is absent from the script output."""
    allowed, flagged = allowed_memo_numbers(analysis), {}
    for investor, memo in memos.items():
        unknown = []
        for token in MEMO_NUMBER.findall(memo):
            plain = token.lstrip("+")
            variants = {plain, plain.replace(",", ""), plain.rstrip("%"), plain.replace(",", "").rstrip("%")}
            if not variants.intersection(allowed) and token not in unknown:
                unknown.append(token)
        if unknown:
            flagged[investor] = unknown
    return flagged


def default_memo(investor: str, ticker: str) -> str:
    path = Path(f"{investor.lower()}_memo_{ticker}.md")
    return path.read_text(encoding="utf-8") if path.exists() else f"Paste the {investor} skill-generated memo here."


st.set_page_config(page_title="Lab 19 — Legend Panel", page_icon="📊", layout="wide")
st.title("Lab 19 — Legend Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
with st.sidebar:
    st.header("SEC EDGAR request")
    ticker = st.text_input("Ticker", value="COST").strip().upper()
    email = st.text_input("Your email for EDGAR User-Agent", help="Required by SEC EDGAR; used only for this request.").strip()
if not ticker:
    st.info("Enter a ticker.")
    st.stop()
if not email or "@" not in email:
    st.warning("Enter your email in the sidebar. SEC EDGAR requires an identifying User-Agent.")
    st.stop()
try:
    with st.spinner(f"Downloading {ticker}'s SEC company facts…"):
        analysis = get_analysis(ticker, email)
except (RuntimeError, ValueError) as error:
    st.error(str(error))
    st.stop()

chart = pd.DataFrame({"Fiscal year end": [r["fiscal_year_end"] for r in analysis["rows"]], "Owner earnings": [r["owner_earnings"] for r in analysis["rows"]], "Net income": [r["net_income"] for r in analysis["rows"]]}).set_index("Fiscal year end")
st.subheader(f"{analysis['company']} ({analysis['ticker']})")
st.caption("USD millions. A gap is not plotted because the underlying value is not found.")
st.line_chart(chart, use_container_width=True)
st.subheader("Five fiscal years from annual 10-K facts")
st.dataframe(table_frame(analysis), hide_index=True, use_container_width=True)
st.subheader("Legend panel: checks computed in code")
st.dataframe(panel_frame(analysis), hide_index=True, use_container_width=True)
st.dataframe(pd.DataFrame([{"Investor": investor, "Verdict": panel_verdict(analysis["panel_checks"][investor])} for investor in INVESTORS]), hide_index=True, use_container_width=True)
st.subheader("Three investor memos")
memos = {}
for column, investor in zip(st.columns(3), INVESTORS):
    with column:
        st.markdown(f"#### {investor}")
        memos[investor] = st.text_area(f"{investor} memo", value=default_memo(investor, ticker), height=380, key=f"{investor}_{ticker}")
flagged = unprinted_memo_numbers(memos, analysis)
if flagged:
    details = "; ".join(f"{investor}: " + ", ".join(f"`{number}`" for number in numbers) for investor, numbers in flagged.items())
    st.error("Numbers in the memo(s) that the script did not print: " + details)
else:
    st.success("Every number in all three memos appears in the script's printed output.")
