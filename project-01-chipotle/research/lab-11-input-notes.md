# Lab 11 — Input Notes

## CMG: cost of equity

Value per share comes from the five-year FCFE amounts plus the terminal value, discounted back using the 9.0% cost of equity. I think changing the cost-of-equity input will affect value per share because it changes the present value of both the five-year cash flows and the terminal value.

I think revenue growth would drive Chipotle's forecast because, if Chipotle performs well, higher revenue should lead to higher operating income and FCFE. Higher forecast cash flows increase the equity value and therefore the value per share, assuming margins and the other inputs remain the same.

## Partner notes — Apple

My partner wonders whether Apple’s tax rate could affect its valuation. Yes: a higher tax rate lowers after-tax income and free cash flow, which lowers the present value of Apple’s forecast cash flows and terminal value; a lower tax rate has the opposite effect.

My partner changed Apple revenue growth from 5.0% to 3.0% in every forecast year while keeping every other assumption the same. This is a 2.0-percentage-point decrease to one independent input across the forecast path.

For Apple's sensitivity analysis, the base revenue-growth input is 5.0% in every forecast year, with lower and higher cases of 3.0% and 7.0%; the base gross-margin input is 46.5%, with lower and higher cases of 45.5% and 47.5%. Revenue growth therefore has a plus-or-minus 2.0-percentage-point range, while gross margin has a plus-or-minus 1.0-percentage-point range.

## Sensitivity setup — CMG

I will use the same outputs for every scenario: FY2030E operating income, FY2030E FCFE, and value per share. The model uses FCFE, not FCFF, and all dollar amounts are USD millions except value per share.

| Independent operating driver | Base case | Lower case | Higher case | Units and forecast years | Reason for range |
|---|---|---|---|---|---|
| Revenue growth | FY2026E–FY2030E: 9.0%, 7.0%, 6.5%, 6.0%, 5.5% | 8.0%, 6.0%, 5.5%, 5.0%, 4.5% | 10.0%, 8.0%, 7.5%, 7.0%, 6.5% | Percentage of revenue; each lower/higher path shifts every forecast year by 1.0 percentage point | FY2026 is based on flat comparable-sales guidance plus planned openings, while later years taper as the store base grows; a 1.0-point range is a reproducible judgment around that base path. |
| Gross margin | 25.5% in FY2026E–FY2030E | 24.5% in every forecast year | 26.5% in every forecast year | Percentage of revenue; a 1.0 percentage-point shift in every forecast year | Derived gross margin was 26.2% in FY2023, 26.7% in FY2024, and 25.4% in FY2025, so the range spans recent history around the 25.5% base case. |

## Locked Changed-Input Record — not yet run

**Timestamp:** September 29, 2026. **Base-model Git commit:** `e1fde4e`.

| Input change | Prediction before running | Why |
|---|---|---|
| Revenue-growth path: base → lower, a decrease of 1.0 percentage point in every FY2026E–FY2030E year | FY2030E operating income, FY2030E FCFE, and value per share should all decline; I expect FY2030E operating income and value per share to fall by roughly 4%–6%. | Lower revenue produces lower gross profit and operating income in every forecast year, and also reduces the terminal FCFE. |
| Gross margin: 25.5% → 24.5%, a decrease of 1.0 percentage point in every FY2026E–FY2030E year | FY2030E operating income, FY2030E FCFE, and value per share should all decline; I expect the FY2030E operating-income reduction to be roughly $130 million. | A one-point lower margin reduces gross profit by about 1% of FY2030E revenue, partly offset by lower G&A because G&A is modeled as a percentage of gross profit. |

Before running either change, I showed these ranges and predictions to my partner. My partner confirmed that the units are percentage points, not percent changes, and that only one independent input changes in each scenario.

## What I changed — CMG

For CMG, I changed one independent input at a time. For revenue growth, I used the base path of 9.0%, 7.0%, 6.5%, 6.0%, and 5.5% for FY2026E–FY2030E, with lower and higher paths that move every year by minus or plus 1.0 percentage point; for gross margin, I tested 24.5%, 25.5%, and 26.5% in every forecast year while leaving all other assumptions at base.

## V — check the result

### CMG base check

The base run before the analysis and the restored base run after the analysis matched: FY2030E operating income was $2,591.9 million, FY2030E FCFE was $1,897.6 million, and value per share was $19.65. The balance-sheet check was $0.0 in every forecast year and cash remained above the $25.0 million minimum in every usable run.

### CMG actual one-at-a-time results

| Driver and case | FY2030E operating income ($m) | Change from base ($m) | FY2030E FCFE ($m) | Change from base ($m) | Value per share | Change from base | Accounting check |
|---|---:|---:|---:|---:|---:|---:|---|
| Revenue growth — lower | 2,444.4 | (147.5) | 1,772.4 | (125.2) | $18.47 | ($1.19) | Pass |
| Revenue growth — base | 2,591.9 | 0.0 | 1,897.6 | 0.0 | $19.65 | $0.00 | Pass |
| Revenue growth — higher | 2,745.0 | 153.1 | 2,027.8 | 130.2 | $20.89 | $1.23 | Pass |
| Gross margin — lower | 2,461.8 | (130.0) | 1,798.3 | (99.3) | $18.61 | ($1.04) | Pass |
| Gross margin — base | 2,591.9 | 0.0 | 1,897.6 | 0.0 | $19.65 | $0.00 | Pass |
| Gross margin — higher | 2,721.9 | 130.0 | 1,997.0 | 99.3 | $20.70 | $1.04 | Pass |

The revenue-growth spans were $300.56 million for FY2030E operating income, $255.40 million for FY2030E FCFE, and $2.42 per share; the gross-margin spans were $260.07 million, $198.70 million, and $2.09 per share, respectively. Each change from base was recomputed as the changed output minus the base output.

### Locked Changed-Input Record — actual result and prediction check

The lower revenue-growth path produced FY2030E operating income of $2,444.4 million and value per share of $18.47, versus base values of $2,591.9 million and $19.65. My prediction of roughly a 4%–6% decline was broadly accurate: operating income declined about 5.7% and value per share declined about 6.1%; the small difference from the rough range is explained by compounding lower growth across all five forecast years and by the lower terminal FCFE.

The lower gross-margin case produced FY2030E operating income of $2,461.8 million, a $130.0 million decline from base, which matched my rough prediction of about $130 million. The prediction was accurate because the 1.0-percentage-point margin reduction applies directly to FY2030E revenue, partly offset by G&A falling with gross profit.

### Partner exchange 2

I will show my partner the CMG lower revenue-growth result and its base result: FY2030E operating income changed from $2,591.9 million to $2,444.4 million, a difference of ($147.5 million), and value per share changed from $19.65 to $18.47, a difference of ($1.19). I will ask her to recompute those differences, confirm that the other independent inputs stayed at base, and trace the result from lower revenue through lower gross profit, operating income, FCFE, terminal FCFE, and value per share.

For Apple, I recorded that my partner changed revenue growth from 5.0% to 3.0% in every forecast year while holding other assumptions at base. The Apple base and changed output values are still needed to recompute her differences and complete my check of her evidence.

### Conclusion and research priority

The sensitivity results do not change my base-model valuation result because the base inputs and outputs were restored exactly after the analysis. They make revenue growth my first research priority because its tested value-per-share span of $2.42 is larger than the gross-margin span of $2.09, so evidence on comparable restaurant sales and new restaurant openings would be most useful.

## E — find the driver

Over these tested ranges, revenue growth is the larger CMG driver for all three outputs. Its FY2030E operating-income span is $300.56 million compared with $260.07 million for gross margin, its FCFE span is $255.40 million compared with $198.70 million, and its value-per-share span is $2.42 compared with $2.09.

This ranking is only **over these ranges**: both inputs were tested with 1.0-percentage-point changes, but a larger or smaller range could change the measured span. It does not prove that revenue growth is always more important than gross margin in every possible Chipotle forecast.

### Causal link I will explain to my partner

When the revenue-growth path is lower, Chipotle has less revenue in every forecast year; with the gross-margin assumption held constant, that creates less gross profit, lower operating income, lower FCFE, and lower terminal FCFE. The lower terminal FCFE and explicit-period FCFE reduce value per share from $19.65 in the base case to $18.47 in the lower revenue-growth case.

### Partner exchange 3 — pending live discussion

**Question I expect to receive:** Could revenue growth rank first only because of the ranges you chose?

**My answer:** Yes, the ranking is limited to the ranges I tested; a wider gross-margin range or a narrower revenue-growth range could change the spans. With the same 1.0-percentage-point tests used here, revenue growth had the larger span, so I would research comparable restaurant sales and new restaurant openings first.

**Question I will ask about Apple:** Is Apple’s main driver ranking caused by the size of the range tested, or by the company’s underlying business economics?

**Partner's response about Apple:** Apple's revenue-growth result may look larger partly because it was tested over a wider plus-or-minus 2.0-percentage-point range than the plus-or-minus 1.0-percentage-point gross-margin range. The result is still useful for the stated ranges, but it does not prove revenue growth is always Apple's main driver; the product-versus-Services mix and its effect on gross margin also matter.

**My summary of the comparison:** CMG and Apple should not be ranked against each other using raw dollar changes because their sizes and stated sensitivity ranges differ. For CMG, both drivers used 1.0-percentage-point shifts and revenue growth had the larger span; for Apple, the wider revenue-growth range could contribute to a larger revenue-growth span.

I checked that Apple's stated ranges use percentage points and that revenue growth and gross margin are separate independent inputs. Apple output values are still needed to recompute the actual base-versus-changed differences.

## Sensitivity — learn on my own

One-at-a-time sensitivity changes one independent input while holding every other independent assumption at base, then lets all linked statement quantities recalculate. The chosen range affects the ranking because a wider range can create a larger output span even when the underlying driver is not inherently more important.

A sensitivity table is not a forecast probability because it shows what the model produces under selected assumptions, not the likelihood that each assumption or result will occur. It does not assign probabilities to the lower, base, or higher cases.

## Reflection — partner explanation

Over my CMG ranges, revenue growth mattered most because it produced the largest spans for FY2030E operating income, FY2030E FCFE, and value per share. I was surprised that lowering gross margin by 1.0 percentage point still reduced FY2030E operating income by $130.0 million, which was nearly as large as the lower revenue-growth case even though revenue growth had the larger overall span.
