# Validation evidence

Run `python project2_report.py` from the repository root. The checked-in expected output is [../output/project2-result.txt](../output/project2-result.txt).

| Check | Result | Evidence |
|---|---|---|
| Baseline reproducibility | Pass | 75% BIL / 0% IEF / 0% LQD / 25% VT; 5.51% expected return; 3.84% volatility; 75.0% reserve eligible. |
| Expected-return mandate | Pass | 5.51% is at least the 5.5% objective. |
| Reserve mandate | Pass | 75.0% BIL + IEF is at least the 20.0% minimum. |
| Long-only/grid rule | Pass | All weights are nonnegative and sum to 100.0%; `find_lowest_risk_mix` enumerates the 5-point grid. |
| Equal-weight baseline | Fail | 25% in each sleeve produces 3.01% expected return, 7.55% volatility, and 50.0% reserve eligible. It passes the reserve rule but fails the 5.5% return objective. |
| Inverse-volatility baseline | Fail | Weights proportional to 1/volatility produce 3.37% expected return, 1.37% volatility, and 92.8% reserve eligible. It passes the reserve rule but fails the 5.5% return objective. |
| Point-in-time signal | Pass | At the September 30, 2026 decision date, the ALFRED-compatible latest known `FEDFUNDS` observation was August 2026 at 3.63%. September's 3.75% value, published October 1, was excluded. See [point-in-time-signal.md](point-in-time-signal.md). |
| Changed history window | Sensitive | Last 36 returns: 90% BIL / 10% VT, 5.95%, 1.21%, 90.0% reserve. The largest weight changes by 15 points. |
| VT return stress | Sensitive but feasible | Decreasing VT's annual expected return by 1.0 point produces 70% BIL / 30% VT, 5.58%, 4.58%, 70.0% reserve. |

The unchanged source price window has 60 observations (59 monthly returns), October 2021 through September 2026. The changed-window test uses the final 36 monthly returns. Both results are descriptive calculations based on historical adjusted-close prices; neither is a forecast validation.
