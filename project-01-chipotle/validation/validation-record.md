# Project 1 Validation Record — Chipotle

**Status:** Partially complete. This record distinguishes completed, saved
evidence from the one test that cannot be completed without the class-provided
training case. All values are USD millions unless stated otherwise.

## 1. Known-answer/training-case reconciliation — OPEN

- **Required input/result:** the course's synthetic or known-answer training
  case and its published expected result.
- **Current evidence:** none is present in this repository. The preserved
  Edition A identifies this as future work; it does not supply the case.
- **What is needed to close it:** enter the class-supplied inputs in a
  dedicated test, run it, and save actual-versus-expected outputs with the
  difference and pass/fail criterion.

No result has been invented or represented as passing.

## 2. Independent source and definition check — COMPLETE

- **Input checked:** FY2025 cash capital expenditures of **$666.336m**.
- **Definition:** purchases of leasehold improvements, property, and equipment
  in the FY2025 cash-flow statement; this is cash capex, not a data-provider
  field with an unspecified definition.
- **Source/result:** `research/cmg-history-and-assumptions.md` traces the
  amount to Chipotle's FY2025 Form 10-K and shows the source agrees to the
  alternative data-provider field after rounding.
- **Why it matters:** capex directly reduces FCFF in
  `models/cmg_integrated_dcf.py`.

The separately documented WACC source/definition check is in
`research/wacc-support.md`: dated Treasury yield, Restaurant/Dining beta,
implied ERP, zero funded debt, tax rate, and the operating-lease convention.

## 3. Directional changed-input prediction written before the run — COMPLETE, LAB 11 SCOPE

`research/lab-11-input-notes.md` records the following prediction under the
timestamp **September 29, 2026** and base-model commit **`e1fde4e`**. The date
is preserved exactly as recorded; this repository does not claim an earlier
prediction.

- A 1.0-percentage-point reduction in every FY2026E-FY2030E revenue-growth
  input should lower FY2030E operating income, FCFE, and value per share by
  about 4%-6% for operating income and value per share.
- A 1.0-percentage-point reduction in gross margin should lower those outputs;
  FY2030E operating income was predicted to fall by about $130m.

The pre-run record applies to the Lab 11 FCFE pro-forma sensitivity, not to a
claim that the later integrated FCFF model existed on September 29.

## 4. Locked Changed-Input Record — COMPLETE, LAB 11 SCOPE

**Source:** `research/lab-11-input-notes.md`, “Locked Changed-Input Record.”

| Item | Revenue-growth lower case | Gross-margin lower case |
| --- | --- | --- |
| Old input | 9.0%, 7.0%, 6.5%, 6.0%, 5.5% for FY2026E-FY2030E | 25.5% in every forecast year |
| New input | Each year lower by 1.0 percentage point: 8.0%, 6.0%, 5.5%, 5.0%, 4.5% | 24.5% in every forecast year |
| Units | Percentage points; all other independent inputs held at base | Percentage points; all other independent inputs held at base |
| Prediction recorded before run | Operating income, FCFE, and value/share decline | Operating income, FCFE, and value/share decline; EBIT effect about $130m |
| Actual FY2030E result | Operating income: $2,591.9m → $2,444.4m; FCFE: $1,897.6m → $1,772.4m; value/share: $19.65 → $18.47 | Operating income: $2,591.9m → $2,461.8m; FCFE: $1,897.6m → $1,798.3m; value/share: $19.65 → $18.61 |
| Prediction check | Broadly matched: operating income fell 5.7%; value/share fell 6.1% | Matched: operating income fell $130.0m |
| Decision effect | Did not change Watch / defer; revenue growth became the first research priority | Did not change Watch / defer; margin remains a material uncertainty |

This is preserved as the dated Lab 11 record. The current FCFF DCF has a
separate, automated driver-linkage check showing that a lower pro-forma
revenue-growth path lowers FY2030E FCFF and DCF value per share.

## 5. Three-statement articulation checks — COMPLETE

- **Base-year reconciliation:** `models/cmg_proforma.py` asserts FY2025
  revenue of $11,925.601m, cash of $350.545m, inventory of $49.508m, PP&E of
  $2,679.361m, and equity of $2,830.607m against the FY2025 Form 10-K base
  values.
- **Balance sheet:** the normal October 19, 2026 run of `python run_all.py`
  reports assets minus liabilities and equity of $0.0 for every FY2026E-FY2030E
  year.
- **Cash reconciliation:** the same run reports cash-flow ending cash minus
  balance-sheet cash of $0.0 in every forecast year.
- **Saved evidence:** `outputs/latest-model-output.txt`.

## 6. DCF monotonicity checks — COMPLETE

`models/cmg_integrated_dcf.py` runs `assert_dcf_directionality()` during the
normal application run. It fails loudly if either a 1.0-percentage-point higher
WACC or a 1.0-percentage-point lower terminal growth rate raises value per
share. The October 19, 2026 normal run reports **“DCF directionality checks:
PASS.”**

The same code also checks the operating link: the lower pro-forma
revenue-growth path must reduce both FY2030E FCFF and DCF value per share.

## 7. Enterprise-to-equity bridge check — COMPLETE

`assert_enterprise_to_equity_bridge()` in `models/cmg_integrated_dcf.py`
checks both formulas during the normal run:

`Equity value = enterprise value + non-operating cash - funded debt`

`Value per diluted share = equity value / diluted shares`

For the base case: $27,973.2m enterprise value + $350.545m cash - $0 funded
debt = $28,323.8m equity value; divided by 1,342.616m diluted shares equals
$21.10 per share. The October 19, 2026 normal run reports
**“Enterprise-to-equity bridge check: PASS.”**

## 8. Peer-policy/multiple-definition check — COMPLETE

`My_Own_Peer_Policy.md` sets the comparison date as February 5, 2026 and
defines enterprise value as market capitalization plus funded debt less cash.
It excludes operating lease liabilities from debt and defines EBITDA as
reported operating income plus depreciation and amortization, matching the DCF
lease convention. `models/ev_ebitda_comparables.py` applies that definition to
CMG, CAVA, and Sweetgreen and rejects Sweetgreen's nonpositive EBITDA as not
meaningful. The P/E model likewise excludes peers with nonpositive EPS.

## 9. Highest-risk failure test — COMPLETE

**Risk tested:** a pro-forma can appear usable if a calculated ending cash
balance no longer agrees with the balance sheet.

**Test:** `python models/cmg_proforma.py --break-cash` deliberately replaces
FY2026E calculated cash with opening cash.

**Observed result:** the model stops with
`AssertionError: FY2026E: balance sheet gap is -1348.549015 million`.

**Conclusion:** this error is expected and demonstrates that the balance-sheet
assertion fails loudly. The ordinary command, `python run_all.py`, passes;
do not use the break-cash command as a normal production run.

## 10. Fresh-eyes partner challenge and response — PARTIALLY COMPLETE

The partner feedback is preserved in `feedback-from-my-partner.md`.

- **Challenge:** Why do the DCF and FCFE pro-forma values differ, and what is
  the largest limitation? The partner also recommended a CAPM-supported cost
  of equity and a second usable peer or normalization of CAVA's EPS.
- **Response/action:** the final valuation now uses an integrated FCFF DCF and
  CAPM-supported 8.10% WACC documented in `research/wacc-support.md`; it also
  adds EV/EBITDA under the same lease convention. The analysis continues to
  qualify CAVA as a single-peer reference rather than averaging it with the
  DCF. Terminal-value dependence and the limited peer set remain limitations.
- **Effect on decision:** Watch / defer remains unchanged because the
  February 5, 2026 market price of $38.45 is above the integrated DCF range of
  $18.43-$22.77 per share.
- **Open credit item:** the partner's name is not recorded in the existing
  notes. Add the challenger's name before final submission if the instructor
  requires named attribution.

## Remaining validation work

1. Obtain and run the class-provided known-answer/training-case reconciliation.
2. Complete the separate fresh-environment cold-run log.
3. Add the partner's name to the fresh-eyes record if required by the course.
