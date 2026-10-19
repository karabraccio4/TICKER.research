# Validation Record

Status: **Incomplete — working record**

Do not mark an item complete until the corresponding test has actually been run
and its evidence is preserved.

## Required evidence

- [ ] Known-answer or synthetic training-case reconciliation
- [x] Independent source and definition check on a load-bearing input: the CAPM WACC inputs, funded-debt treatment, tax rate, and operating-lease convention are documented with dated Treasury, Damodaran, price, and FY2025 10-K sources in `research/wacc-support.md`.
- [ ] Directional changed-input prediction written before execution
- [ ] Locked Changed-Input Record with timestamp/commit, units, prediction, actual result, and decision effect
- [x] Base-year reconciliation to the filing: `models/cmg_proforma.py` checks FY2025 revenue ($11,925.601m), cash ($350.545m), inventory ($49.508m), PP&E ($2,679.361m), and equity ($2,830.607m) against the model's 10-K base year.
- [x] Balance-sheet and cash-flow articulation checks: the October 19, 2026 local run showed zero balance-sheet gap and zero cash-flow-ending-cash-to-balance-sheet-cash gap for FY2026E-FY2030E.
- [x] DCF directionality check: the integrated DCF fails if higher WACC or lower terminal growth raises value
- [ ] Enterprise-to-equity bridge check
- [ ] Peer-policy and multiple-definition consistency check
- [ ] Highest-risk failure test
- [ ] Fresh-environment cold-run evidence

## Existing evidence to reconcile

- research/lab-11-input-notes.md contains a September 29, 2026 changed-input record for the FCFE pro-forma sensitivity analysis.
- models/cmg_proforma.py with the --break-cash argument deliberately produces a FY2026E balance-sheet assertion failure; this was run locally on October 19, 2026.
- models/cmg_integrated_dcf.py includes DCF directionality assertions.
- models/cmg_integrated_dcf.py also verifies that using the lower revenue-growth scenario lowers FY2030E FCFF and the DCF value per share relative to the base case.

These records still need to be organized against the final integrated model and
the project’s exact validation requirements.
