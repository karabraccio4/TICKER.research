# Point-in-time signal data card — FEDFUNDS reserve-yield monitor

## Decision use

**Signal:** the latest knowable monthly effective federal funds rate (`FEDFUNDS`) as of the portfolio decision date.

**Project 2 decision date:** September 30, 2026.
**Signal available then:** August 2026 = **3.63%**.
**Not used:** September 2026 = **3.75%**, because it was published on October 1, 2026—after the decision date.

The signal monitors the cash-and-rate environment relevant to the BIL reserve sleeve. It does **not** change the optimizer's historical return estimates, set a forecast, or automatically override the 5.5% return and 20% reserve mandate. If an appropriate ALFRED vintage cannot be obtained for a future decision date, the rate signal is unavailable and must not be substituted with today's FRED value.

## Data card

| Field | Evidence |
|---|---|
| Series | `FEDFUNDS`, Federal Funds Effective Rate |
| Source | Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, distributed by [FRED](https://fred.stlouisfed.org/series/FEDFUNDS) |
| Vintage source | [ALFRED](https://alfred.stlouisfed.org/series?seid=FEDFUNDS), which permits retrieval of values available on a historical vintage date |
| Definition | Weighted-average overnight rate at which depository institutions trade federal funds |
| Units and frequency | Percent, not seasonally adjusted; monthly average of daily figures |
| As-of boundary | Use only the ALFRED vintage available on or before the decision date; retain the latest published observation in that vintage |
| Known-answer check | On September 30, 2026, the latest known observation was August 2026 at 3.63%. The September 2026 3.75% value entered FRED on October 1 and is excluded. |
| Revisions | Economic data may be revised. Historical decisions use the contemporaneous ALFRED vintage rather than today's FRED series. |
| Project role | Risk monitor for the cash-and-rate environment; no automatic allocation rule or return forecast |

## Interpretation and monitoring

The 3.63% reading is descriptive evidence that a positive cash-rate environment existed as of the decision date. It supports monitoring the reserve sleeve, but it does not prove BIL will earn that rate or that the portfolio will meet its return objective.

Before any future rebalance or recommendation, refresh the signal from the correct ALFRED vintage and record the decision date, latest knowable observation, and any revision. Escalate the recommendation for committee review if the signal cannot be reproduced from a vintage, if the cash-rate regime changes materially, or if the client changes the reserve-liquidity requirement.
