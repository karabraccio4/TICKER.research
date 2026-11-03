"""Streamlit front end for Lab 18's EDGAR Buffett-investor skill.

Run:
    $env:SEC_EDGAR_EMAIL = "your.email@example.edu"
    python -m streamlit run buffett_10k_app.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

from buffett_10k_skill.edgar_buffett import analysis_for_ticker, display, display_percent


MEMO_NUMBER = re.compile(r"(?<![A-Za-z])[-+]?\d[\d,]*(?:\.\d+)?%?")


@st.cache_data(ttl=3600, show_spinner=False)
def get_analysis(ticker: str, email: str) -> dict:
    """Cache SEC results briefly to respect EDGAR while keeping the app responsive."""
    return analysis_for_ticker(ticker, email)


def table_frame(analysis: dict) -> pd.DataFrame:
    """Make the required five-year display table with XBRL tags visible."""
    records = []
    for row in analysis["rows"]:
        record = {"Fiscal year end": row["fiscal_year_end"]}
        for key, label in [
            ("revenue", "Revenue"),
            ("net_income", "Net income"),
            ("operating_cash_flow", "Operating cash flow"),
            ("capital_spending", "Capital spending"),
            ("equity", "Equity"),
        ]:
            record[label] = display(row[key])
            record[f"{label} XBRL tag"] = row["tags"][key]
        record["ROE"] = display_percent(row["roe"])
        record["Owner earnings"] = display(row["owner_earnings"])
        records.append(record)
    return pd.DataFrame(records)


def allowed_memo_numbers(analysis: dict) -> set[str]:
    """Create the exact numeric vocabulary printed by the script's result."""
    allowed = {"15", "15%"}  # printed in the ROE check label
    for row in analysis["rows"]:
        for token in re.findall(r"\d+(?:\.\d+)?", row["fiscal_year_end"]):
            allowed.add(token)
        for field in ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"]:
            if row[field] is not None:
                # Permit both script formatting (e.g., 5,844) and an ungrouped equivalent.
                shown = display(row[field])
                allowed.add(shown)
                allowed.add(shown.replace(",", ""))
        if row["roe"] is not None:
            pct = display_percent(row["roe"])
            allowed.add(pct)
            allowed.add(pct.rstrip("%"))
    return allowed


def unprinted_memo_numbers(memo: str, analysis: dict) -> list[str]:
    """Return distinct numeric tokens the memo used but EDGAR output did not print."""
    allowed = allowed_memo_numbers(analysis)
    unknown = []
    for token in MEMO_NUMBER.findall(memo):
        plain = token.lstrip("+")
        variants = {plain, plain.replace(",", ""), plain.rstrip("%"), plain.replace(",", "").rstrip("%")}
        if not variants.intersection(allowed) and token not in unknown:
            unknown.append(token)
    return unknown


def default_memo(ticker: str) -> str:
    """Use the saved COST memo when available; otherwise prompt for the skill's memo."""
    path = Path(f"buffett_memo_{ticker}.md")
    return path.read_text(encoding="utf-8") if path.exists() else "Paste the skill-generated Buffett-style memo here."


st.set_page_config(page_title="Lab 18 — Buffett Investor", page_icon="📊", layout="wide")
st.title("Lab 18 — Buffett Investor as a Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("SEC EDGAR request")
    ticker = st.text_input("Ticker", value="COST").strip().upper()
    email = st.text_input("Your email for EDGAR User-Agent", type="default", help="Required by SEC EDGAR; used only for this request.").strip()

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

chart = pd.DataFrame(
    {
        "Fiscal year end": [row["fiscal_year_end"] for row in analysis["rows"]],
        "Owner earnings": [row["owner_earnings"] for row in analysis["rows"]],
        "Net income": [row["net_income"] for row in analysis["rows"]],
    }
).set_index("Fiscal year end")
st.subheader(f"{analysis['company']} ({analysis['ticker']})")
st.caption("USD millions. A gap is not plotted because the underlying value is not found.")
st.line_chart(chart, use_container_width=True)

st.subheader("Five fiscal years from annual 10-K facts")
st.dataframe(table_frame(analysis), hide_index=True, use_container_width=True)

st.subheader("Buffett checks computed in code")
checks = pd.DataFrame(
    [{"Check": check, "Result": result} for check, result in analysis["checks"].items()]
)
st.dataframe(checks, hide_index=True, use_container_width=True)

st.subheader("Buffett-style memo")
memo = st.text_area(
    "Memo text (the app checks it against the script output)",
    value=default_memo(ticker),
    height=310,
    key=f"memo_{ticker}",
)
unknown = unprinted_memo_numbers(memo, analysis)
if unknown:
    st.error("Numbers in the memo that the script did not print: " + ", ".join(f"`{number}`" for number in unknown))
else:
    st.success("Every number in this memo appears in the script's printed output.")
