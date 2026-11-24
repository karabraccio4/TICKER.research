# Project 2 — Portfolio stability decision

This repository supports a proposed reserve-fund allocation for a community arts nonprofit with a five-year horizon. It is a classroom model, not investment advice.

## Decision

**Pilot, not adopt:** use the baseline mix only as a starting allocation. Reverse that decision only after the client approves a forward-looking return-estimate method and the history window; the historical-window check moves 15 percentage points between BIL and VT.

The decision memo, data dates, conditions, and the exact numbers are in [docs/decision-memo.md](docs/decision-memo.md). A GitHub-readable copy of the result is in [output/project2-result.txt](output/project2-result.txt).

## Cold-run command

From the repository root, run exactly:

```powershell
python project2_report.py
```

It uses only the Python standard library and the checked-in `prices.csv`; no download, account, or API key is required. The command prints the baseline, changed-window validation, VT stress run, mandate measures, and decision line.

To use the interactive tool after installing its optional interface dependency, run `python -m pip install -r requirements.txt`, then:

```powershell
python -m streamlit run app.py
```

In the sidebar, upload the checked-in `prices.csv`, leave **Use only the last 36 monthly returns** off for the baseline, set the objective to **5.5%**, set the reserve minimum to **20.0%**, and retain **BIL** and **IEF** as reserve eligible. A teammate can move the 36-month toggle or change VT's expected-return estimate and immediately read the mandate result.

## How the model works

`portfolio.py` turns monthly adjusted-close prices into annualized arithmetic-mean return estimates, sample volatility, and correlations. It enumerates every long-only allocation on a 5-percentage-point grid and retains the feasible mix with the lowest `sqrt(w' covariance w)`. A mix must have expected return at least 5.5% and BIL + IEF at least 20.0%.

The interactive app also compares the constrained portfolio with two transparent baselines under the same mandate: equal weight and inverse volatility (weights proportional to `1 / volatility`). It states whether each portfolio passes the return and reserve rules, including the rule that fails.

| File | Purpose |
|---|---|
| `project2_report.py` | Reproducible command-line decision report |
| `app.py` | Interactive Streamlit tool |
| `portfolio.py` | Inputs, validation, historical-estimate calculation, and transparent grid search |
| `prices.csv` | 60 completed monthly adjusted-close observations, October 2021–September 2026 |
| `docs/decision-memo.md` | Committee decision, conditions, and limitations |
| `docs/validation.md` | Baseline, mandate, window, and stress evidence |
| `docs/point-in-time-signal.md` | FEDFUNDS point-in-time signal, data card, and as-of rule |
| `docs/locked-changed-input-record.md` | Lab 20 record to complete before rerunning the stress case |
| `docs/cold-run-note.md` | Partner-only cold-run note template |
| `docs/video-manifest.md` | Three required video prompts and links to add after recording |

## Source and units

`prices.csv` contains Yahoo Finance Adjusted Close prices for BIL, IEF, LQD, and VT, downloaded October 22, 2026. Dates are completed calendar months, oldest first; the file covers October 2021 through September 2026, producing 59 monthly returns. Returns, volatility, correlations, and weights are decimals in code and percentages in output. Currency is USD.

## Honest Lab 20 status

The reproducible package and the pre-run materials are ready. The partner cold run, its elapsed time/first failure, the prediction-before-rerun record, the required commit/push, and the actual video URLs must be completed by the student and partner during Lab 20; they must not be backfilled or represented as completed.
