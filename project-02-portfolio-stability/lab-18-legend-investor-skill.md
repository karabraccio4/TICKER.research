# Lab 18 — Legend Investor as Skill

## D — the question

Can an investor's philosophy become a skill an AI runs the same way every time — every number computed by code from the 10-K, with the judgment left to the model?

My answer is yes, within a clear boundary: code retrieves, selects, labels, calculates, and marks missing data; the memo interprets the resulting evidence.

## Partner discussion

Code can compute owner earnings: operating cash flow minus capital spending. It can also calculate ROE and apply a stated pass/fail rule consistently. Judgment is deciding whether a pattern of profitability, reinvestment, and missing information makes the business one to own, watch, or pass. Judgment also cannot turn an unreported capital-spending value into a fact.

## My build request to the AI

> Build a reusable Codex skill named `buffett-10k-investor`, with a bundled Python script and a Streamlit app. For a ticker, use only keyless SEC EDGAR ticker and companyfacts endpoints with an identifying User-Agent. Use annual 10-K facts only, label the last five years by fiscal-year-end date, prefer the specified XBRL tags, let the latest filing win for a repeated period, and never estimate a missing value. Print every input with its tag; calculate ROE, owner earnings, and the three specified Buffett checks in code. Save a short Markdown memo that uses only printed values and judges the business, not its price. In the app, chart owner earnings and net income, show the table/checks/memo, and flag any memo number absent from the script output.

## Files

| File | Purpose |
| --- | --- |
| `buffett_10k_skill/edgar_buffett.py` | SEC EDGAR retrieval, five-year row construction, calculations, checks, and memo shell. |
| `buffett_10k_app.py` | Streamlit app with chart, fact table, checks, memo, and number-provenance flag. |
| `buffett_memo_COST.md` | Buffett-style COST memo and my decision. |
| `C:\Users\Kara Braccio\.codex\skills\buffett-10k-investor\SKILL.md` | Installed Codex skill instructions. |

## R — data rules implemented

The script uses the SEC ticker-to-CIK JSON and the SEC companyfacts JSON, not FAskills or paid data. It sends an identifying User-Agent in the form `FIN 43900 Lab 18 email-address` and takes the email from `SEC_EDGAR_EMAIL` or the `--email` option.

For each selected annual 10-K observation, flow values must span roughly one year. If the same fiscal-year fact appears in more than one filing, the most recently filed one wins. Revenue tries `RevenueFromContractWithCustomerExcludingAssessedTax` before `Revenues`; capital spending tries `PaymentsToAcquirePropertyPlantAndEquipment` before `PaymentsToAcquireProductiveAssets`. The app shows the tag used beside every source input.

All dollar output is USD millions. ROE is net income divided by year-end equity. Owner earnings are operating cash flow minus capital spending. A source value not present is `not found`; a derivative or check that needs a missing input is `not known`. Equity at or below zero makes ROE `not known`.

## Run instructions

In PowerShell, use an email address belonging to the person running the request:

```powershell
$env:SEC_EDGAR_EMAIL = "your.email@school.edu"
python buffett_10k_skill/edgar_buffett.py COST --memo buffett_memo_COST.md
python -m streamlit run buffett_10k_app.py
```

The Streamlit sidebar also asks for the email before it makes an EDGAR request. The email is not hard-coded into the repository.

## V — COST known-answer check

The expected five rows, in USD millions, are:

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

The expected three checks are pass, pass, pass. A live EDGAR run on 3 November 2026 matched every displayed COST value and all three check results. The saved COST memo uses only values in this table and gives the required one-line personal decision.

## Probes and expected behavior

| Probe | Expected result |
| --- | --- |
| `python buffett_10k_skill/edgar_buffett.py JPM` | Live run: capital spending is `not found`; owner earnings is `not found`; both owner-earnings checks are `not known`; the generated memo shell tells the writer to say it cannot judge owner earnings. |
| Put `40.0%` in the memo box | The app flags `40.0%` because that number was not printed by the script. |
| Fresh browser-AI answer | Compare its undocumented ROE figures with the app’s table, XBRL tags, and SEC source rules. |

### Explain the core code

`build_rows` loops over the five fiscal years. For each required field it calls `pick_fact_for_year`. That function searches tags in the required priority order, filters to 10-K and FY facts, requires a one-year duration for flows, and chooses the candidate with the latest `filed` date. If no candidate exists, it returns `(None, None)`. `build_rows` converts `None` to the displayed `not found`, and leaves ROE or owner earnings as `None` whenever their inputs are unavailable. `make_checks` turns any missing check input into `not known` rather than guessing.

## Agent skills — learn on your own

1. A skill is a folder whose `SKILL.md` begins with front matter containing a name and description, followed by reusable instructions and optional scripts.
2. The name and description let an AI decide whether the skill applies without loading detailed instructions. It reads the rest only when the request matches, which keeps unrelated context out of the conversation.
3. Numbers belong in code because code applies source, tag-preference, period, unit, and missing-data rules identically each time. The model is then limited to interpreting documented results rather than inventing a figure or silently changing a rule.

## Reflection

The skill makes the five-year selection, source-tag preference, unit conversion, missing-value handling, formulas, and checks repeatable. It leaves the business-quality conclusion and its explanation to the model. `Not found` is better than an estimate because it preserves the evidence boundary: the user can see what EDGAR did not report and knows exactly why a conclusion is not known.

## Sources

- SEC ticker-to-CIK: <https://www.sec.gov/files/company_tickers.json>
- SEC companyfacts endpoint: <https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json>
- SEC EDGAR API documentation: <https://www.sec.gov/search-filings/edgar-application-programming-interfaces>
- Streamlit documentation: <https://docs.streamlit.io/>

## Live-run assumption

The live SEC requests used the student's supplied email address only in the required EDGAR User-Agent. The address is not hard-coded in the repository; future runs must set `SEC_EDGAR_EMAIL` or enter an email in the app sidebar.
