# Validation and AI use — Project 2

**Status:** Completed working validation record. The locked changed-input prediction was committed before the rerun; the observed result was committed separately afterward.

## Decision, source boundary, and intended use

**Decision:** Pilot, not adopt the portfolio process. Reverse this decision only after the client approves a forward-looking return-estimate method and history window.

**Intended user:** Community arts nonprofit reserve fund with a five-year horizon.

**Portfolio source boundary:** `prices.csv` holds 60 completed monthly Yahoo Finance Adjusted Close observations for BIL, IEF, LQD, and VT, October 2021 through September 2026. The file was downloaded October 22, 2026; prices are USD. The model converts these observations into 59 monthly returns and annualized historical arithmetic-mean return estimates. They are descriptive estimates, not forecasts.

**Point-in-time source boundary:** The Federal Funds Effective Rate signal uses the ALFRED vintage knowable on the decision date. At September 30, 2026, August 2026 at 3.63% was the latest known monthly observation; September's 3.75% value, published October 1, is excluded. See [point-in-time-signal.md](point-in-time-signal.md).

## Validation record

| Test | Result | Evidence |
|---|---|---|
| Clean command-line reproduction | Pass | `python project2_report.py` prints the decision with no network, account, or API key. Checked output: [../output/project2-result.txt](../output/project2-result.txt). |
| Uploaded-CSV handling | Pass | `portfolio.estimates_from_prices` decodes the Streamlit uploaded-file byte stream and successfully reads BIL, IEF, LQD, and VT. |
| Baseline mandate comparison | Pass | Equal weight (3.01% return) and inverse volatility (3.37% return) both fail the 5.5% return objective; the constrained mix passes return and reserve. See [validation.md](validation.md). |
| Point-in-time known answer | Pass | The September 30, 2026 decision view retains August FEDFUNDS 3.63% and excludes September 3.75%, published October 1. |
| Historical-window sensitivity | Sensitive | Limiting the input to the last 36 monthly returns moves BIL from 75% to 90% and VT from 25% to 10%. |
| Locked VT return-estimate stress run | Sensitive but feasible | The completed record changes VT from 11.05% to 10.05% per year. The allocation moves from 75% BIL / 25% VT to 70% BIL / 30% VT; expected return rises from 5.51% to 5.58%, volatility rises from 3.84% to 4.58%, and reserve eligible weight falls from 75.0% to 70.0%. |

## Limitations and monitoring

- Historical arithmetic means, covariance, and the 5-point allocation grid are not forecasts and can produce estimate-sensitive allocations.
- The point-in-time rate signal is a monitor for the cash-and-rate environment, not an optimizer input or automatic allocation override.
- Before a future recommendation or rebalance, use the appropriate ALFRED vintage; do not substitute today's revised FRED history.
- Review the allocation if the approved estimation method, history window, client reserve requirement, liquidity terms, implementation costs, or tax assumptions change.

## Material AI use and disposition

| Interaction date | Tool and version | Material use | Human check / disposition |
|---|---|---|---|
| November 17, 2026 | OpenAI Codex coding agent; model/version not displayed in the student interface | Drafted repository documentation, a reproducible report, and an uploaded-CSV decoding repair. | The report was run from a fresh folder; the uploaded-CSV behavior was tested; the AI-assisted cold run is clearly labeled as not a human-partner result. |
| November 23, 2026 | OpenAI Codex coding agent; model/version not displayed in the student interface | Added the app's baseline comparison and FEDFUNDS point-in-time monitor; organized the data card and validation record. | The Streamlit app was tested headlessly with zero exceptions; the report snapshot matches the checked-in output; FRED and ALFRED documentation were checked for source, units, and vintage behavior. |

The AI assisted with implementation and documentation. The financial decision, any final changed-input prediction, and all video explanations remain the student's responsibility. This is an educational demonstration, not investment advice.

## Locked Changed-Input Record — completed

The complete record is [locked-changed-input-record.md](locked-changed-input-record.md).

- **Prediction checkpoint:** [commit `6fb9b67`](https://github.com/karabraccio4/TICKER.research/commit/6fb9b67), before the changed-input run.
- **Input:** VT annual expected-return estimate, 11.05% to 10.05% per year (−1.00 percentage point).
- **Result checkpoint:** [commit `0239609`](https://github.com/karabraccio4/TICKER.research/commit/0239609), after the result was recorded.
- **Decision effect:** The numeric mandate remained feasible, but the allocation's sensitivity supports the unchanged pilot-not-adopt recommendation.
