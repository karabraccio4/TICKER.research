# Project 1 Video Recording Scripts — Chipotle

Use these as speaking guides rather than reading every word. Show the listed
files on screen while explaining the work in your own words.

## Video 1 — Research Evolution

Open: `reports/Project_1_Edition_A_Chipotle_Original_Submitted.md`,
`reports/Project_1_Edition_B_Chipotle.md`,
`research/cmg-history-and-assumptions.md`, and the FY2025 Form 10-K.

### Screen sequence

1. **Introduction / investment question:** GitHub repository home page or
   `reports/Project_1_Edition_B_Chipotle.md` title and recommendation.
2. **Original Edition A and company selection:**
   `reports/Project_1_Edition_A_Chipotle_Original_Submitted.md`, showing its
   Decision and Filing Evidence sections.
3. **Fiscal year, filing date, and valuation date explanation:** browser tab
   with the FY2025 10-K cover page showing “fiscal year ended December 31,
   2025”; then Edition B's Company, filing, and reporting basis section,
   which explains the February 4 filing and February 5 valuation date.
4. **Filing evidence:** 10-K MD&A in the browser or Edition B's Filing evidence
   table. Point to comparable sales, transactions, cash, debt, and openings.
5. **Research evolution and forecast assumptions:**
   `research/cmg-history-and-assumptions.md`, especially Assumption set for the
   CMG forecast; then `models/cmg_proforma.py` only briefly if helpful.
6. **AI use and independent verification:**
   `validation/ai-use-and-normalization-record.md`, then
   `research/wacc-support.md` for the 8.10% WACC and beta limitation.
7. **Closing conclusion:** Edition B's Decision or Conditional call section.

“Hi, this is my Chipotle Project 1 research-evolution video. My investment
question is whether a fund with no current Chipotle position should initiate,
watch/defer, or avoid the stock.

My original Edition A conclusion was Watch/Defer. I selected Chipotle because
it is a company-operated restaurant business where I could connect restaurant
openings, comparable sales, margins, capex, and cash flow. My main concern was
that FY2025 comparable restaurant sales declined 1.7%, driven by a 2.9%
transaction decline, even though Chipotle opened 334 company-owned restaurants.

The 10-K says it is for the fiscal year ended December 31, 2025. That is
correct because those are the financial-statement and base-year dates. The
filing was released after market close on February 4, 2026, so I selected
February 5, 2026 as the valuation date: the first full trading day after the
filing became public. My market price, market capitalization, peer prices, and
market-date WACC inputs use February 5, while the operating history comes from
the FY2025 financial statements.

My starting evidence came from Chipotle’s FY2025 Form 10-K. I used the filing
for revenue, cash of $350.545 million, zero revolver borrowings, diluted shares,
comparable-sales results, and restaurant-opening data.

As the project developed, I moved from a separate DCF path to an integrated
model. My five-year pro forma now drives FCFF directly. My base forecast assumes
revenue growth slows from 9% in 2026 to 5.5% in 2030, with growth supported by
openings but limited by the flat comparable-sales guidance.

Codex helped organize sources, connect the pro forma to the DCF, and structure
validation. I independently checked the WACC inputs: the Treasury rate,
Damodaran beta and equity-risk premium, Chipotle’s debt, and the lease treatment.
I accepted the 8.10% WACC calculation but qualified the beta because it is an
industry beta, not a Chipotle-specific beta.

My final conclusion remains Watch/Defer. The main research question is whether
transaction recovery and restaurant economics can support a stronger cash-flow
path.”

## Video 2 — Code and Validation

Open `README.md`, `run_all.py`, `models/cmg_proforma.py`, and
`models/cmg_integrated_dcf.py` in VS Code. Run `python run_all.py`, then show
`outputs/latest-model-output.txt` and the validation files.

### Screen sequence

1. **Introduction and how to run the project:** `README.md` in VS Code, showing
   the `python run_all.py` command and output location.
2. **Operating-model architecture:** `models/cmg_proforma.py`; scroll to
   `BASE_INPUTS`, `SCENARIO_CASES`, and the three-statement checks. Do not try
   to read all code aloud.
3. **DCF architecture:** `models/cmg_integrated_dcf.py`; show
   `fcff_from_projections`, `value_dcf`, the WACC constants, and the bridge
   check.
4. **Live normal run:** VS Code terminal running `python run_all.py`; pause on
   the balance-sheet/cash checks, integrated DCF result, sensitivity grid,
   low/base/high cases, and training-case PASS output.
5. **Saved validation evidence:** `outputs/latest-model-output.txt`,
   `validation/validation-record.md`, and
   `validation/training_case_reconciliation.py`.
6. **Highest-risk failure test and cold run:**
   `validation/validation-record.md` section 9 or
   `validation/cold-run-log.md`. You may show the break-cash command/error from
   the saved record instead of deliberately interrupting your live recording.

“This is my code-and-validation demonstration for Chipotle. The README gives
the exact command to run the application. The core operating model is
`cmg_proforma.py`, which forecasts the income statement, balance sheet, and
cash flow statement from FY2026 through FY2030.

The integrated valuation model is `cmg_integrated_dcf.py`. It takes pro-forma
outputs and calculates FCFF from after-tax EBIT, depreciation, noncash
impairment, capex, and working-capital changes. It discounts FCFF at an 8.10%
WACC and completes the enterprise-value-to-equity-value bridge.

The normal run shows that the balance sheet balances in every forecast year and
that ending cash from the cash-flow statement equals balance-sheet cash. The
DCF directionality and enterprise-to-equity bridge checks pass.

The base integrated DCF produces $21.55 per diluted share. The low/base/high
operating cases produce $18.85, $21.55, and $23.25 per share. The official
training-case reconciliation also passes, including the WACC-terminal-growth
grid.

My highest-risk failure test is the deliberate break-cash test. When I run
`python models/cmg_proforma.py --break-cash`, the model intentionally stops
with a balance-sheet assertion error. That is expected and proves the check can
catch a broken model. The cold-run log records a successful run in a new Python
environment.”

## Video 3 — Committee Defense

Open `reports/Project_1_Edition_B_Chipotle.md`,
`outputs/latest-model-output.txt`, and `My_Own_Peer_Policy.md`.

### Screen sequence

1. **Recommendation and date basis:** Edition B's heading and Decision section.
   Keep the February 5, 2026 valuation-date language visible.
2. **DCF range versus market price:** Edition B's Integrated low, base, and
   high scenarios table and the same-date comparison table.
3. **Operating thesis and evidence:** Edition B's Filing evidence table or the
   FY2025 10-K MD&A browser tab for comparable-sales, transaction, and opening
   evidence.
4. **Downside and high case:** Edition B's scenario table, with
   `research/scenario-assumptions.md` ready if you want to explain the drivers.
5. **Sensitivity and reverse DCF:** Edition B's Sensitivity grid and reverse
   DCF section.
6. **Comparable-method disagreement:** `My_Own_Peer_Policy.md` and Edition B's
   Comparable-company valuation section. Point out why you do not average the
   peer result with the DCF.
7. **Monitor and reversal triggers:** Edition B's Conditional call, monitoring,
   and reversal triggers section.

“My recommendation is Watch/Defer. I used FY2025 financial statements ending
December 31, 2025 and a February 5, 2026 valuation date, which was the first
full trading day after the FY2025 10-K was filed after market close. On that
valuation date, Chipotle closed at $38.45 per share.

My integrated DCF operating range is $18.85 to $23.25 per diluted share, with
a $21.55 base case. The market price is above even my high operating case.

Chipotle has expansion potential, liquidity, and no funded revolver debt.
However, FY2025 comparable restaurant sales declined 1.7% and transactions
declined 2.9%. My valuation depends on whether transaction growth recovers
while Chipotle continues opening restaurants without damaging margins or
requiring materially higher reinvestment.

My downside case assumes weaker transactions and comparable sales, fewer
openings, and food and labor pressure. My high case assumes stronger
transaction recovery, successful openings, and better margins, but also higher
capex to fund growth.

The comparable-company results are higher references, but I do not average them
with my DCF. CAVA is the only usable peer reference, and its P/E has a
tax-related limitation. The DCF remains my primary method because it models
Chipotle’s forecast cash flow and reinvestment directly.

My reverse DCF shows that, with base margins, capex, WACC, and terminal growth
held constant, the $38.45 market price requires revenue growth of roughly 19.4%
in FY2026 and 15.9% by FY2030. That is an operating hurdle, not a prediction.

I would reconsider the recommendation if the price fell into my valuation range
or if sourced evidence showed sustained transaction recovery, successful
openings, stable margins, and stronger FCFF. I would become more negative if
transaction declines continue, openings miss plan, margins weaken, or
reinvestment needs rise.”
