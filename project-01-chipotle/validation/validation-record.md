# Validation Record

Status: **Incomplete — working record**

Do not mark an item complete until the corresponding test has actually been run
and its evidence is preserved.

## Required evidence

- [ ] Known-answer or synthetic training-case reconciliation
- [ ] Independent source and definition check on a load-bearing input
- [ ] Directional changed-input prediction written before execution
- [ ] Locked Changed-Input Record with timestamp/commit, units, prediction, actual result, and decision effect
- [ ] Base-year reconciliation to the filing
- [ ] Balance-sheet and cash-flow articulation checks
- [x] DCF directionality check: the integrated DCF fails if higher WACC or lower terminal growth raises value
- [ ] Enterprise-to-equity bridge check
- [ ] Peer-policy and multiple-definition consistency check
- [ ] Highest-risk failure test
- [ ] Fresh-environment cold-run evidence

## Existing evidence to reconcile

- research/lab-11-input-notes.md contains a September 29, 2026 changed-input record for the FCFE pro-forma sensitivity analysis.
- models/cmg_proforma.py with the --break-cash argument deliberately produces a balance-sheet assertion failure.
- models/cmg_integrated_dcf.py includes DCF directionality assertions.

These records still need to be organized against the final integrated model and
the project’s exact validation requirements.
