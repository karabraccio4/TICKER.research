# Lab 19 — Legend Panel

## D — the question

When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would I trust the panel?

## Partner discussion

Graham can differ from Buffett because Graham requires a margin of safety and emphasizes conservative balance-sheet screens. Buffett may admire a durable business without treating it as a bargain. Burry reads the same statements skeptically: he tests whether cash supports earnings and looks for balance-sheet risk or evidence that a strong narrative is hiding a weak downside case.

## Build request to the AI

> Extend my Lab 18 EDGAR skill and Streamlit app into a three-investor panel. Keep the exact same keyless SEC EDGAR data source and Lab 18 10-K selection rules. Add liabilities, current assets, and current liabilities. Compute every check in code, write a separate short memo for Buffett, Graham, and Burry using only printed numbers, and show a panel table, verdicts, side-by-side memos, and a flag for any memo number not printed by the script.

## Shared facts and rules

All investors use exactly the same SEC EDGAR companyfacts output:

| Rule | Implementation |
| --- | --- |
| Filings | 10-K only; five latest fiscal years, labelled by fiscal-year-end date. |
| Flows | Revenue, net income, and operating cash flow must be one-year periods. |
| Duplicate fact | Latest filing wins for an identical fiscal-year-end date. |
| Revenue | `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`. |
| Net income | `NetIncomeLoss`. |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities`. |
| Capital spending | `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`. |
| Equity | `StockholdersEquity`. |
| Liabilities | `Liabilities`. |
| Current assets | `AssetsCurrent`. |
| Current liabilities | `LiabilitiesCurrent`. |
| Missing source fact | `not found`, never an estimate. |
| Missing check input | `not known`. |

## Investor checks to compute in code

| Investor | Check |
| --- | --- |
| Buffett | ROE at least 15% every year; owner earnings positive every year; owner earnings grew from first to last year. |
| Graham | Latest-year current ratio at least 2; net income positive every year; net income grew from first to last year. |
| Burry | Operating cash flow at least net income every year; latest-year liabilities no more than twice equity. |

Current ratio is current assets divided by current liabilities. Liabilities-to-equity is not known when equity is zero or below.

## App requirements

The Streamlit app keeps the Lab 18 chart and five-year fact table. It adds a panel table of investor × check with `pass`, `fail`, or `not known`; each investor's verdict; three memos side by side; and one unprinted-number flag across all three memos. The app must continue to show: “Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.”

## Sources read, but not installed or used as data

- [Ben Graham FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md): conservative quantitative screening, current ratio, earnings stability, and margin of safety.
- [Michael Burry FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md): skeptical forensic analysis, cash-flow support for earnings, liabilities, and bear-case thinking.
- [Streamlit documentation](https://docs.streamlit.io/): app framework reference.

FAskills itself and its paid data sources are not installed or used. The only numerical source is SEC EDGAR.

## COST validation

A live EDGAR run on 5 November 2026 matched the supplied COST ratios exactly:

| FY end | 2022-08-28 | 2023-09-03 | 2024-09-01 | 2025-08-31 | 2026-08-30 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Current ratio | 1.02 | 1.07 | 0.97 | 1.03 | 1.06 |
| Liabilities ÷ equity | 2.11 | 1.75 | 1.96 | 1.64 | 1.49 |

The panel results also matched: Buffett 3 of 3; Graham 2 of 3 because the current-ratio screen fails at 1.06; Burry 2 of 2. The current-ratio probe was considered, and the Graham memo records the decision to retain the 2.00 threshold because it preserves the conservative liquidity screen.

## Files created or changed

| File | Purpose |
| --- | --- |
| `buffett_10k_skill/edgar_buffett.py` | Shared SEC extraction, balance-sheet facts, ratios, all panel checks, and memo shells. |
| `buffett_10k_app.py` | Chart, tagged fact table, panel table/verdicts, side-by-side memos, and one cross-panel numeric-provenance flag. |
| `buffett_memo_COST.md` | Completed Buffett memo. |
| `graham_memo_COST.md` | Completed Graham memo and threshold decision. |
| `burry_memo_COST.md` | Completed Burry memo. |

## My Project 2 company — NVIDIA (NVDA)

I selected NVIDIA because it was the largest disclosed company holding of the Vanguard Total World Stock ETF (`VT`), one of my Project 2 funds. Vanguard’s holdings page reported NVIDIA at 4.52% as of 30 September 2026, above Apple at 4.08%. The panel used NVIDIA’s SEC EDGAR facts, not the fund provider’s data.

| Investor | Result | Verdict |
| --- | --- | --- |
| Buffett | All three checks pass. | Own the business |
| Graham | All three checks pass; latest current ratio is 3.91. | Own the business |
| Burry | Leverage passes at 0.31 liabilities/equity; cash flow does not meet or exceed net income every year. | Watch it |

The three completed NVIDIA memos are `buffett_memo_NVDA.md`, `graham_memo_NVDA.md`, and `burry_memo_NVDA.md`.

## Explain the Graham code to my partner

The `make_graham_checks` function receives the five shared annual rows and a current-ratio threshold, which defaults to 2. First, it takes `rows[-1]["current_ratio"]`, the ratio from the latest fiscal year. Next, it collects each row’s `net_income` into a five-item list. If the latest ratio is missing, the current-ratio result is `not known`; otherwise it is `pass` when the ratio is at least the threshold and `fail` when it is lower. It then calls `check_every` for positive net income: that helper returns `not known` immediately if any value is missing, otherwise it returns `pass` only if every value is positive. Finally, `growth_check` returns `not known` when the first or last income is missing, and otherwise compares the last year with the first. The function returns all three named results for the panel table.

The answer to the partner’s missing-input question is: the code does not estimate. A missing current ratio makes that check `not known`; a missing net-income value makes the all-years check `not known`; and a missing first or last income makes the growth check `not known`.

## Bull and bear — NVIDIA

**Bull case:** Revenue grew from 26,914 to 215,938 and owner earnings grew from 8,132 to 96,676. Buffett’s profitability checks and Graham’s liquidity and earnings checks all pass, including a latest current ratio of 3.91.

**Bear case:** Burry’s cash-versus-earnings check fails because operating cash flow does not meet or exceed net income every year; the latest values are 102,718 and 120,067. A skeptical reviewer would investigate why cash conversion trails reported earnings before relying on the stronger profitability screens.

## My decision

**Only with a condition:** I would let this panel screen Project 2 companies only as a transparent first pass, followed by a manual review of missing facts, cash-conversion gaps, business risks, and valuation.

## A panel of AI agents — learn on my own

1. An AI-agent panel is a set of separate, scoped skills that receive the same source facts and apply different explicit rules and interpretations.
2. The personas can disagree even with identical facts because their code checks, thresholds, and judgment lenses differ: Buffett prioritizes profitability and owner earnings, Graham prioritizes conservative liquidity and earnings stability, and Burry prioritizes cash support for earnings and leverage.
3. The panel agreed that NVIDIA had strong profitability, positive/growing earnings, and acceptable latest leverage. It split because Burry’s cash-versus-earnings test failed while Buffett and Graham passed their full screens.

## Reflection

The threshold probe shows that a screen’s verdict is a design choice, not a fact about the company: lowering Graham’s current-ratio cutoff changed COST from fail to pass. Publishing the threshold, preserving `not known` for gaps, and showing the raw values lets a reviewer see that judgment rather than mistake it for an objective answer.
