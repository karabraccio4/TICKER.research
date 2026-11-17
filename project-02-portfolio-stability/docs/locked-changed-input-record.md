# Locked changed-input record — Lab 20

**Status: prepared, not yet locked.** Complete the prediction, commit and push it *before* running the changed case. Do not revise the prediction afterward.

## Prediction before rerun

- Input selected: VT annual expected-return estimate.
- Baseline value and unit: record the printed baseline VT annual estimate from the app, in percent.
- New value and unit: baseline VT annual estimate minus **1.0 percentage point**.
- Expected direction: I expect the model to require a larger VT weight to clear the same 5.5% objective after each percentage point of VT return is reduced; therefore BIL should fall, volatility should rise, and reserve-eligible weight should fall.
- Expected decision effect: The mandate should remain feasible, but the pilot-not-adopt decision should not become stronger because the allocation is estimate-sensitive.
- Prediction commit hash and GitHub URL: **[fill before rerun]**

## Observed after rerun

- Command/tool settings used:
- Output saved at:
- Observed mix, expected return, volatility, and reserve-eligible weight:
- Did the numeric mandate remain feasible?
- Did the decision line change?
- Did the result match the prediction? Why or why not?

### Prior reproducible reference (not a substitute for the locked Lab 20 record)

The existing model run with VT reduced by 1.0 percentage point produced 70% BIL / 0% IEF / 0% LQD / 30% VT, 5.58% expected return, 4.58% volatility, and 70.0% reserve eligible. It is shown so the student can detect a software or settings mismatch, not so this record can be falsely represented as having been committed before a Lab 20 rerun.
