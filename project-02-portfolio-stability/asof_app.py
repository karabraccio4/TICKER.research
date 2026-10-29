"""Lab 17: FRED and ALFRED point-in-time interest-rate audit.

Run with: python -m streamlit run asof_app.py
"""

from __future__ import annotations

from datetime import date
from io import StringIO

import pandas as pd
import requests
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_CSV = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id: str) -> pd.DataFrame:
    """Download the currently published vintage of one FRED series."""
    response = requests.get(FRED_CSV.format(series_id=series_id), timeout=30)
    response.raise_for_status()
    return parse_csv(response.text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_on(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download the vintage of one series that ALFRED showed on a given date."""
    response = requests.get(
        ALFRED_CSV.format(series_id=series_id, vintage_date=vintage_date), timeout=30
    )
    response.raise_for_status()
    return parse_csv(response.text, series_id)


def parse_csv(csv_text: str, series_id: str) -> pd.DataFrame:
    """Turn a FRED-style CSV into dated numeric observations; '.' becomes missing."""
    frame = pd.read_csv(StringIO(csv_text), na_values=".")
    if "observation_date" not in frame.columns or len(frame.columns) < 2:
        raise ValueError(f"FRED did not return usable data for {series_id}.")
    value_column = frame.columns[-1]
    frame = frame.rename(columns={"observation_date": "date", value_column: "value"})
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    return frame[["date", "value"]].dropna(subset=["date"])


def last_observation(frame: pd.DataFrame) -> pd.Series | None:
    """Return the final non-missing observation, or None when there is none."""
    available = frame.dropna(subset=["value"])
    return None if available.empty else available.iloc[-1]


def display_observation(observation: pd.Series | None) -> str:
    if observation is None:
        return "No available value"
    return f"{observation['date'].date():%Y-%m-%d}: {observation['value']:.3f}"


st.set_page_config(page_title="Point-in-Time Rate Audit", page_icon="📈", layout="wide")
st.title("Point-in-Time Rate Audit")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Series and dates")
    selected_ids = st.multiselect(
        "Rate series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    extra_id = st.text_input("Add another FRED series ID", placeholder="Example: T10Y2Y").strip().upper()
    if extra_id and extra_id not in selected_ids:
        selected_ids.append(extra_id)
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today())

if not selected_ids:
    st.info("Choose at least one series in the sidebar.")
    st.stop()

records = []
for series_id in selected_ids:
    name = SERIES.get(series_id, "Added FRED series")
    try:
        today_data = download_today(series_id)
        vintage_data = download_as_known_on(series_id, as_known_on.isoformat())
    except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
        st.error(f"{series_id}: could not load this series. {error}")
        continue

    chart_today = today_data[today_data["date"].dt.date >= start_date].dropna(subset=["value"])
    chart_vintage = vintage_data[vintage_data["date"].dt.date >= start_date]
    known_last = last_observation(chart_vintage)
    today_last = last_observation(chart_today)

    st.subheader(f"{series_id} — {name}")
    if chart_today.empty:
        st.warning(f"No current {series_id} observations are available from {start_date:%Y-%m-%d}.")
    else:
        st.line_chart(chart_today.set_index("date")["value"], use_container_width=True)
    st.caption(
        f"Last date known on {as_known_on:%Y-%m-%d}: {display_observation(known_last)}"
    )

    if known_last is None:
        later_values = 0
        revised_values = 0
    else:
        known_dates = set(chart_vintage.dropna(subset=["value"])["date"])
        today_by_date = today_data.set_index("date")["value"]
        vintage_by_date = vintage_data.set_index("date")["value"]
        later_values = int(
            ((today_data["date"] > known_last["date"]) & today_data["value"].notna()).sum()
        )
        common_dates = known_dates.intersection(set(today_by_date.dropna().index))
        revised_values = sum(
            pd.notna(vintage_by_date[observation_date])
            and today_by_date[observation_date] != vintage_by_date[observation_date]
            for observation_date in common_dates
        )

    records.append(
        {
            "Series ID": f"https://fred.stlouisfed.org/series/{series_id}",
            "Last measured, as known then": display_observation(known_last),
            "Last measured, today": display_observation(today_last),
            "Today's values after known date": later_values,
            "Revised values on shared dates": revised_values,
        }
    )

st.subheader("Point-in-time audit table")
if records:
    st.dataframe(
        pd.DataFrame(records),
        column_config={
            "Series ID": st.column_config.LinkColumn(
                "Series ID", display_text=r".*/series/(.*)$", help="Open the FRED series page"
            )
        },
        hide_index=True,
        use_container_width=True,
    )
else:
    st.warning("No selected series could be loaded. Check the IDs or your network connection.")
