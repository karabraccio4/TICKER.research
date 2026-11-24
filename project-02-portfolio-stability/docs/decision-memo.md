# Decision memo — Project 2 portfolio stability

**Decision date:** November 17, 2026
**Client:** Community arts nonprofit reserve fund
**Horizon:** Five years
**Decision:** **Pilot, not adopt.** Use the baseline allocation only as a starting allocation. Reverse this decision only after the client approves a forward-looking return-estimate method and the history window.

## Mandate and method

The portfolio must be long only, have an expected annual return of at least **5.5%**, and maintain at least **20.0%** in reserve-eligible BIL and IEF. The model searches all long-only allocations in 5-percentage-point increments and selects the feasible mix with the lowest volatility, calculated as `sqrt(w' covariance w)`.

The source file is `prices.csv`: 60 monthly Yahoo Finance Adjusted Close observations for BIL, IEF, LQD, and VT, from October 2021 through September 2026. That gives 59 monthly returns. Historical arithmetic-average returns and covariances are descriptive estimates, not forecasts. The data were downloaded October 22, 2026; prices are USD and all reported returns, volatility, and weights below are annual percentages.

## Baseline result

Using all 59 monthly returns, the lowest-volatility feasible mix is **75% BIL, 0% IEF, 0% LQD, and 25% VT**. Its expected return is **5.51%**, volatility is **3.84%**, and reserve-eligible weight is **75.0%**. It meets both numeric mandate constraints.

## Validation and changed inputs

Using only the last 36 monthly returns changes the mix to **90% BIL, 0% IEF, 0% LQD, and 10% VT**; expected return is **5.95%**, volatility is **1.21%**, and reserve-eligible weight is **90.0%**. The largest allocation move is **15 percentage points**.

For the return-estimate stress case, VT's annual expected return falls by **1.0 percentage point**. The result becomes **70% BIL, 0% IEF, 0% LQD, and 30% VT**; expected return is **5.58%**, volatility is **4.58%**, and reserve-eligible weight is **70.0%**. The numeric mandate remains feasible, but the allocation and risk move materially.

## Point-in-time reserve-yield monitor

The rate monitor uses the latest **knowable** Federal Funds Effective Rate (`FEDFUNDS`) rather than today's revised history. On the September 30, 2026 decision date, the latest available monthly observation was **August 2026 at 3.63%**. September's 3.75% value was published October 1 and was excluded. The signal monitors the cash-and-rate environment relevant to BIL; it is not a forecast, optimizer input, or automatic allocation override. Future decisions require the applicable ALFRED vintage. See [point-in-time-signal.md](point-in-time-signal.md).

## Committee rationale and limits

The model supplies a feasible, low-volatility starting point, but not enough evidence for adoption. The history-window test changes the BIL/VT allocation by 15 points, and the VT estimate stress case changes the allocation by 5 points while increasing volatility. Before adoption, the client must approve the forward-looking return-estimate method and the appropriate history window. The committee should also review implementation costs, tax considerations, liquidity assumptions, and whether the model's 5-point allocation grid is sufficiently precise.

Reproduction: run `python project2_report.py` from the repository root. See [validation-and-ai-use.md](validation-and-ai-use.md) for the source boundary, validation record, AI-use disclosure, and Locked Changed-Input Record status.
