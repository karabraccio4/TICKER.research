# Video manifest — add working links after recording

The videos are not present in this repository yet. Add each working share link below after recording; do not replace the distinct prompts with one combined video unless the assignment permits it.

| Video | Required question | Link |
|---|---|---|
| 1 — How it changed | What changed from the baseline, which input moved, and what did that do to the numbers and decision? | **[add link]** |
| 2 — Technical walkthrough | How does `find_lowest_risk_mix` produce the decision number, including feasibility tests and volatility comparison? | **[add link]** |
| 3 — Committee decision | What should the committee do, what evidence supports it, and what condition would reverse it? | **[add link]** |

## Speaking notes

**Video 1:** The all-history baseline is 75% BIL and 25% VT, with 5.51% expected return, 3.84% volatility, and 75% reserve eligible. Last-36-month input changes it to 90% BIL and 10% VT, a 15-point movement. Reducing VT's expected annual return by one point produces 70% BIL and 30% VT, raises volatility to 4.58%, and leaves the mandate feasible.

**Video 2:** `estimates_from_prices` first converts adjacent adjusted-close prices into monthly returns, then annualizes the sample mean and sample volatility and derives correlations. `find_lowest_risk_mix` creates every long-only 5-point mix that sums to 100%, rejects a mix below 5.5% expected return or 20% BIL plus IEF, calculates full covariance-based volatility for every survivor, and retains the one with the smallest volatility.

**Video 3:** Pilot, not adopt. The model gives a feasible low-risk starting allocation, but it is sensitive to the history window and to the VT return estimate. Reverse the decision only when the client has approved a forward-looking return-estimate method and a history window; then reassess implementation costs, taxes, liquidity, and grid precision.
