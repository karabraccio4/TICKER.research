# Locked changed-input record — Lab 20

**Status: completed.** Prediction committed before the rerun in [commit `6fb9b67`](https://github.com/karabraccio4/TICKER.research/commit/6fb9b67); observed results recorded afterward in [commit `0239609`](https://github.com/karabraccio4/TICKER.research/commit/0239609).

## Prediction before rerun

- Input selected: VT annual expected-return estimate.
- Baseline value and unit: 11.05% per year.
- New value and unit: 10.05% per year.
- Change: -1.00 percentage point.
- Expected direction: I expect the model to adjust the portfolio allocation after VT's expected return decreases from 11.05% to 10.05%. I expect the portfolio's expected return to decrease unless the model compensates by changing the allocation. Volatility may increase if the model shifts more weight toward VT, while reserve-eligible weight may decrease.
- Expected decision effect: I expect lowering VT's expected return to make it harder for the portfolio to meet the 5.50% return objective. Since the baseline portfolio only slightly exceeds the objective, the mandate may become infeasible. This would support my recommendation to pilot the strategy rather than fully adopt it.
- Prediction commit hash and GitHub URL: [`6fb9b67`](https://github.com/karabraccio4/TICKER.research/commit/6fb9b67)
- Prediction timestamp: November 23, 2026, 7:50 PM EST.

## Observed after rerun
- Command/tool settings used: Opened the Streamlit app at http://localhost:8501 and uploaded `prices.csv`. The expected-return objective was set to 5.50%, and the minimum reserve-eligible weight was 20.00%. BIL and IEF were selected as reserve-eligible assets, while LQD and VT were not. The "Use only the last 36 monthly returns" option was turned off. I changed only VT's annual expected return from 11.05% to 10.05%.

Output saved at: Streamlit screenshots of the baseline and changed-input results.

Observed portfolio mix: Before the change, the portfolio consisted of 75% BIL, 0% IEF, 0% LQD, and 25% VT. After reducing VT's expected return, the portfolio changed to 70% BIL, 0% IEF, 0% LQD, and 30% VT.

Observed expected return: Increased from 5.51% to 5.58%.

Observed volatility: Increased from 3.84% to 4.58%.

Observed reserve-eligible weight: Decreased from 75.00% to 70.00%.

Did the numeric mandate remain feasible? Yes. The new portfolio had an expected return of 5.58%, which exceeded the 5.50% objective, and a reserve-eligible weight of 70%, which exceeded the required 20%. Both requirements passed.

Did the decision line change? No. The constrained portfolio passed both mandate requirements before and after the change. I would still recommend piloting the strategy rather than fully adopting it because the allocation is sensitive to changes in expected-return estimates.

Did the result match the prediction? Why or why not? The results partially matched my prediction. I expected lowering VT's expected return to make it harder to meet the objective and potentially increase volatility while decreasing reserve-eligible weight. The model responded by increasing VT's portfolio weight from 25% to 30%, causing volatility to rise and reserve eligibility to fall. However, the portfolio's expected return actually increased slightly because the optimizer increased its allocation to VT enough to offset the lower return estimate. Overall, the mandate remained feasible.
