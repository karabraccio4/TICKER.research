# My Own Peer Policy

## Company and valuation date

> Company: Chipotle Mexican Grill (CMG)  
> Valuation date: February 5, 2026 (the first full trading day after the FY2025 Form 10-K was publicly accepted after market close on February 4, 2026)

## Peer policy

I will compare Chipotle with publicly traded restaurant companies that have meaningful company-operated restaurant sales, similar fast-casual or limited-service restaurant economics, and unit-growth potential. I will use the same valuation date and the latest annual earnings that were public by that date. A company with negative earnings may remain an operating peer, but it cannot be used to calculate a P/E valuation.

## Rejection criteria

- Exclude negative or immaterial EPS from the P/E calculation, because P/E is not meaningful; retain the company as an operating peer when its restaurant model is relevant.
- Exclude franchise-heavy businesses when franchise, royalty, or rent income dominates the business model.
- Reject businesses with substantially different customer, menu, or operating models if those differences drive margins or growth.
- Reject a company if reliable price and annual EPS data are unavailable for February 5, 2026.
- Qualify, rather than automatically reject, companies with a major one-time gain or loss; disclose the item and the resulting limitation when using reported GAAP EPS.

## Candidate research request

Research CAVA and Shake Shack for:

- FY2025 diluted EPS
- December 31, 2025 closing price
- Calculated P/E
- Ownership/franchise mix
- Any unusual earnings items

## Candidate source table

| Candidate | Decision | Business-model evidence | Reason for decision | Source locator |
| --- | --- | --- | --- | --- |
| Sweetgreen (SG) | Qualify as an operating peer; exclude from P/E | Sweetgreen reports one revenue stream: retail food-and-beverage sales from company-owned U.S. restaurants. | Its company-operated restaurant model is relevant. FY2024 annual diluted EPS was **$(0.79)** (a net loss), so P/E is not meaningful and it cannot produce an implied share value. Its Form 10-K was filed February 27, 2025, before the December 31, 2025 comparison date. | [Sweetgreen FY2024 Form 10-K, Note 12—Net Loss Per Share and Note 15—Reportable Segment](https://www.sec.gov/Archives/edgar/data/1477815/000162828025008367/sg-20241229.htm) |
| Wingstop (WING) | Exclude | Wingstop reported 2,513 franchised locations and 50 company-owned restaurants as of December 28, 2024; 98% of its restaurant base was franchised. | Although FY2024 diluted EPS was positive at **$3.70**, its 98%-franchised, royalty- and franchise-fee-based model differs materially from Chipotle's primarily company-operated restaurant model and meets my franchise-heavy rejection criterion. Its Form 10-K was filed February 19, 2025, before the December 31, 2025 comparison date. | [Wingstop FY2024 Form 10-K, Item 7—Overview and Note 2—Earnings Per Share](https://www.sec.gov/Archives/edgar/data/1636222/000163622225000008/wing-20241228.htm) |
| CAVA Group (CAVA) | Use with qualification | CAVA owned and operated 367 fast-casual restaurants as of December 29, 2024. | Its company-operated fast-casual model fits the policy. FY2024 diluted EPS of $1.10 includes release of an $83.7 million valuation allowance, so its P/E must be presented with that limitation. CAVA's February 5, 2026 closing price was $64.55. | [CAVA FY2024 Form 10-K, Item 1—Business; Note 7—Income Taxes; Note 12—Earnings Per Share](https://www.sec.gov/Archives/edgar/data/1639438/000162828025007882/cava-20241229.htm); [CAVA historical price data](https://finance.yahoo.com/quote/CAVA/history/) |
| Shake Shack (SHAK) | Exclude | As of December 25, 2024, Shake Shack operated 329 company-operated Shacks and had 250 licensed Shacks. | The licensed Shack base is material (250 of 579 system-wide locations). This differs from Chipotle's primarily company-operated restaurant model and meets my franchise-heavy rejection criterion. | [Shake Shack FY2024 Form 10-K, Item 1—Business and Note 1](https://www.sec.gov/Archives/edgar/data/1620533/000162053325000016/shak-20241225.htm) |

## Comparable-input convention

All equity prices and market capitalizations use **February 5, 2026**. Annual accounting data use the latest annual reports public by that date: CMG FY2025 and CAVA/Sweetgreen FY2024. Enterprise value is `market capitalization + funded debt - cash`. Under the lease convention in [wacc-support.md](research/wacc-support.md), operating lease liabilities are excluded from debt for every company, and EBITDA is consistently defined as **reported operating income + depreciation and amortization**, not company-defined adjusted EBITDA.

| Company | Market-capitalization input | Cash | Funded debt | Reported EBITDA | Diluted EPS | P/E | EV / EBITDA | Use and source |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CMG (target) | $38.45 × 1,342.616m diluted shares = $51,623.585m | $350.545m | $0.000m | $2,297.180m | $1.14 | 33.73x | 22.32x | [CMG FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm); [February 5 price](https://finance.yahoo.com/quote/CMG/history/) |
| CAVA | $7,487.000m same-date market capitalization | $366.120m | $0.000m | $103.473m | $1.10 | 58.68x | 68.82x | Qualified, but only as a one-peer reference. [Same-date market cap](https://www.financecharts.com/stocks/CAVA/summary/market-cap); [CAVA FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1639438/000162828025007882/cava-20241229.htm). |
| Sweetgreen (SG) | $697.661m same-date market capitalization | $214.789m | $0.000m | $(28.358)m | $(0.79) | NM | NM | Operating peer only; negative EPS and EBITDA prevent both valuations. [Same-date market cap](https://www.financecharts.com/stocks/SG/summary/market-cap); [Sweetgreen FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1477815/000162828025008367/sg-20241229.htm). |

The market-cap provider estimates same-date market capitalization. CAVA's share count reported in its FY2024 10-K is dated February 18, 2025, not February 5, 2026; this analysis therefore uses the same-date market capitalization directly rather than mixing an older share count with the February 2026 price.

## P/E valuation result

Only CAVA is currently usable for a P/E calculation. Its February 5, 2026 price of $64.55 divided by FY2024 diluted EPS of $1.10 produces a **58.68x P/E**. Applying that single-peer reference to Chipotle FY2025 diluted EPS of $1.14 produces an implied Chipotle value of **$66.90 per share**. This is a reference estimate, not a peer range, and is qualified because CAVA's reported EPS includes the valuation-allowance release. Sweetgreen remains an operating peer but is not usable for P/E because it reported a net loss.

**Model run:** `pe_comparables.py` was run with Python 3.12.14. It calculated CAVA at 58.68x P/E and a $66.90 CMG single-peer reference; it reported Sweetgreen's negative EPS as not meaningful for P/E.

## EV/EBITDA valuation result

CAVA's February 5 enterprise value is `$7,487.000m + $0.000m - $366.120m = $7,120.880m`. Its reported EBITDA is `$43.118m operating income + $60.355m D&A = $103.473m`, producing a **68.82x EV/EBITDA** reference. Applying it to CMG's FY2025 reported EBITDA of `$1,935.798m + $361.382m = $2,297.180m` implies a CMG enterprise value of $158,089.000m and an equity value of $158,439.545m, or **$118.01 per CMG share**.

Sweetgreen's reported EBITDA is negative ($28.358m), so its EV/EBITDA is not meaningful. The CAVA result is therefore a single-peer reference, not a peer range.

**Model run:** `ev_ebitda_comparables.py` calculates CAVA's 68.82x EV/EBITDA and $118.01 CMG reference; it rejects Sweetgreen's negative EBITDA as not meaningful.

**Unresolved:** No second peer currently supports a meaningful P/E or EV/EBITDA, so both results are single-peer references rather than ranges. The annual periods also differ: Chipotle uses FY2025 results, while CAVA and Sweetgreen use the latest annual reports public by February 5, 2026 (FY2024).

## Method differences and valuation conclusion

P/E and EV/EBITDA need not give the same answer. P/E uses after-tax income to common shareholders and is affected by CAVA's valuation-allowance release. EV/EBITDA compares pre-interest, pre-tax operating performance and is not affected by that tax benefit, but it ignores capital expenditures, working capital, and the substantial reinvestment requirements of restaurant expansion. The two peer references also use CAVA FY2024 operating data against CMG FY2025 operating data.

I do **not** mechanically average the $21.10 DCF, $66.90 P/E reference, and $118.01 EV/EBITDA reference. The DCF is the intrinsic-value method because it models Chipotle's own FCFF, capital expenditures, working capital, and cost of capital. The comparable results show that the market assigned CAVA a much higher growth multiple, but one qualified peer cannot establish that Chipotle deserves the same multiple.

## Valuation comparison and provisional call

| Valuation method | Value per CMG share | Basis | Key limitation |
| --- | ---: | --- | --- |
| DCF | $21.10 | FY2026E-FY2030E FCFF derived from the Chipotle pro forma; 8.10% CAPM WACC; 2.5% terminal growth; $350.545 million cash; no funded debt; 1,342.616 million diluted shares. See [WACC support](research/wacc-support.md). | The terminal value represents 78.9% of enterprise value, so the result is highly sensitive to long-run growth and the discount rate. |
| Peer P/E | $66.90 | CAVA's 58.68x P/E ($64.55 February 5, 2026 closing price ÷ $1.10 FY2024 diluted EPS) × Chipotle FY2025 diluted EPS of $1.14. | This is a single-peer reference, not a range. CAVA's FY2024 EPS includes a material valuation-allowance release, and the earnings periods do not match. Sweetgreen cannot contribute a P/E because its EPS is negative. |

| Valuation method | Value per CMG share | Basis | Key limitation |
| --- | ---: | --- | --- |
| Peer EV/EBITDA | $118.01 | CAVA's 68.82x EV/EBITDA applied to CMG FY2025 reported EBITDA, then converted through CMG's cash/debt bridge. | One peer; CAVA's smaller high-growth base and different annual period make the reference weak. Sweetgreen's negative EBITDA is unusable. |

**Provisional call: Watch / defer.** The DCF and peer references differ materially, and the peer results are not sufficiently supported to override the DCF because they rely on one qualified, high-growth peer and mixed annual periods. Before revising the call, obtain a second EV/EBITDA-usable company-operated peer and determine whether CAVA's growth, margins, and reinvestment needs justify applying its multiple to Chipotle.
