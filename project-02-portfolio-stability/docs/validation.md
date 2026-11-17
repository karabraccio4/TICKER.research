# Validation evidence

Run `python project2_report.py` from the repository root. The checked-in expected output is [../output/project2-result.txt](../output/project2-result.txt).

| Check | Result | Evidence |
|---|---|---|
| Baseline reproducibility | Pass | 75% BIL / 0% IEF / 0% LQD / 25% VT; 5.51% expected return; 3.84% volatility; 75.0% reserve eligible. |
| Expected-return mandate | Pass | 5.51% is at least the 5.5% objective. |
| Reserve mandate | Pass | 75.0% BIL + IEF is at least the 20.0% minimum. |
| Long-only/grid rule | Pass | All weights are nonnegative and sum to 100.0%; `find_lowest_risk_mix` enumerates the 5-point grid. |
| Changed history window | Sensitive | Last 36 returns: 90% BIL / 10% VT, 5.95%, 1.21%, 90.0% reserve. The largest weight changes by 15 points. |
| VT return stress | Sensitive but feasible | Decreasing VT's annual expected return by 1.0 point produces 70% BIL / 30% VT, 5.58%, 4.58%, 70.0% reserve. |

The unchanged source price window has 60 observations (59 monthly returns), October 2021 through September 2026. The changed-window test uses the final 36 monthly returns. Both results are descriptive calculations based on historical adjusted-close prices; neither is a forecast validation.
