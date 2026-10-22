"""Lab 15 Streamlit portfolio-stability app.

Run: python -m streamlit run app.py
"""

from __future__ import annotations

import math

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    covariance_matrix,
    estimates_from_prices,
    find_lowest_risk_mix,
    portfolio_return,
    portfolio_volatility,
)


def copy_sleeves(sleeves: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """Copy inputs so the app never changes the imported Meridian constants."""
    return {name: details.copy() for name, details in sleeves.items()}


def mix_measures(
    mix: dict[str, float], sleeves: dict[str, dict[str, float]], correlations: dict[str, dict[str, float]], reserve: set[str]
) -> tuple[float, float, float]:
    """Calculate the requested decision measures using the engine functions."""
    return (
        portfolio_return(mix, sleeves),
        portfolio_volatility(mix, covariance_matrix(sleeves, correlations)),
        sum(mix[name] for name in reserve),
    )


def show_answer(
    heading: str,
    mix: dict[str, float] | None,
    sleeves: dict[str, dict[str, float]],
    correlations: dict[str, dict[str, float]],
    reserve: set[str],
) -> None:
    """Render one candidate result or the required no-feasible-mix message."""
    st.subheader(heading)
    if mix is None:
        st.error("No mix meets the objective and reserve rule on the 5-point grid.")
        return
    expected, volatility, reserve_weight = mix_measures(mix, sleeves, correlations, reserve)
    st.dataframe(
        {"Asset": list(mix), "Weight": [f"{weight * 100:.0f}%" for weight in mix.values()]},
        hide_index=True,
        width="stretch",
    )
    one, two, three = st.columns(3)
    one.metric("Expected return", f"{expected * 100:.2f}%")
    two.metric("Volatility", f"{volatility * 100:.2f}%")
    three.metric("Reserve eligible", f"{reserve_weight * 100:.2f}%")


st.set_page_config(page_title="Portfolio Stability Decision", page_icon="Portfolio", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate and data")
    objective = st.number_input("Expected-return objective (%)", value=OBJECTIVE_RETURN * 100, step=0.1) / 100
    reserve_minimum = st.number_input("Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0, step=1.0) / 100
    uploaded_prices = st.file_uploader("Upload monthly prices.csv", type="csv")
    last_36_months = st.toggle("Use only the last 36 monthly returns", value=False)

try:
    if uploaded_prices is None:
        loaded_sleeves = copy_sleeves(SLEEVES)
        loaded_correlations = CORRELATIONS
        data_label = "Meridian course inputs"
    else:
        loaded_sleeves, loaded_correlations = estimates_from_prices(uploaded_prices, last_36_months=False)
        data_label = "CSV historical estimates (all available monthly returns)"
        if last_36_months:
            current_sleeves, current_correlations = estimates_from_prices(uploaded_prices, last_36_months=True)
        else:
            current_sleeves, current_correlations = copy_sleeves(loaded_sleeves), loaded_correlations
    if uploaded_prices is None:
        current_sleeves, current_correlations = copy_sleeves(loaded_sleeves), loaded_correlations
except (ValueError, KeyError) as error:
    st.error(f"Could not estimate inputs from the CSV: {error}")
    st.stop()

st.info(f"Loaded inputs: {data_label}. Returns are historical estimates, not forecasts.")
st.subheader("Editable expected-return estimates")
for name in current_sleeves:
    current_sleeves[name]["expected_return"] = st.number_input(
        f"{name} expected return (%)",
        value=float(current_sleeves[name]["expected_return"] * 100),
        step=0.1,
        key=f"return_{name}",
    ) / 100

st.subheader("Reserve-eligible assets")
current_reserve = {
    name
    for name in current_sleeves
    if st.checkbox(name, value=name in RESERVE_ELIGIBLE, key=f"reserve_{name}")
}
loaded_reserve = {name for name in loaded_sleeves if name in RESERVE_ELIGIBLE}

current_mix = find_lowest_risk_mix(
    current_sleeves, current_correlations, objective, current_reserve, reserve_minimum
)
loaded_mix = find_lowest_risk_mix(
    loaded_sleeves, loaded_correlations, objective, loaded_reserve, reserve_minimum
)

left, right = st.columns(2)
with left:
    show_answer("Lowest-risk mix: current inputs", current_mix, current_sleeves, current_correlations, current_reserve)
with right:
    show_answer("Answer for inputs as loaded", loaded_mix, loaded_sleeves, loaded_correlations, loaded_reserve)

if current_mix is not None and loaded_mix is not None:
    largest_change = max(abs(current_mix[name] - loaded_mix[name]) for name in current_mix) * 100
    st.metric("Largest weight change from inputs as loaded", f"{largest_change:.1f} points")
else:
    st.info("A largest weight change is unavailable because one comparison mix is infeasible.")
