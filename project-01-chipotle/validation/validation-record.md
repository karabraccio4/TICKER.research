# Project 1 Validation Record — Chipotle

**Status:** Substantially complete. This record distinguishes completed, saved
evidence from remaining validation work. All values are USD millions unless
stated otherwise.

## 1. Known-answer/training-case reconciliation — COMPLETE

- **Official source:** “The Training-Case DCF, Worked End to End,” supplied in
  the Week 6 materials. The training case uses FCFF of $100m in the year just
  ended; five annual growth rates of 8%, 6%, 5%, 4%, and 3%; 3% terminal
  growth; 10% WACC; $50m cash; $300m debt; and 50m diluted shares.
- **Test implementation:** `validation/training_case_reconciliation.py` calls
  the project's actual `value_dcf()` function with the official five-year FCFF
  path: $108.0000m, $114.4800m, $120.2040m, $125.0122m, and $128.7625m.
- **Actual vs. published rounded result:** PV of explicit FCFF $448.4408m vs.
  $448.44m; terminal value $1,894.6486m vs. $1,894.65m; PV of terminal value
  $1,176.4277m vs. $1,176.43m; EV $1,624.8685m vs. $1,624.87m; equity value
  $1,374.8685m vs. $1,374.87m; and value per diluted share $27.4974 vs.
  $27.50.
- **Grid check:** all nine official WACC/terminal-growth grid cells reconcile
  within $0.01 per share. The reverse-DCF zero-shift check also reconciles the
  $27.50 rounded base value.
- **Result:** PASS. Small differences are from the handout's displayed
  rounding; the test retains the unrounded FCFF path and accepts differences
  no greater than $0.01 on dollar outputs and $0.001 on the terminal share.

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

## 10. Fresh-eyes partner challenge and response — COMPLETE

**Challenger:** Katie, whose company was Apple. The partner feedback is
preserved in `feedback-from-my-partner.md` and the Lab 11 exchange is in
`research/lab-11-input-notes.md`.

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

## Remaining validation work

No additional validation test is currently open. The completed fresh-environment
run is recorded in `validation/cold-run-log.md`. Validation does not remove the
documented finance limitations, including terminal-value dependence, the
single-peer comparable reference, and the absence of scenario probabilities.
