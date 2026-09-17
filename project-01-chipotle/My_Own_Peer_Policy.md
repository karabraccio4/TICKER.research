# My Own Peer Policy

## Company and valuation date

> Company: Chipotle Mexican Grill (CMG)  
> Week 3 valuation date: December 31, 2025

## Peer policy

I will compare Chipotle with publicly traded restaurant companies that have meaningful company-operated restaurant sales, similar fast-casual or limited-service restaurant economics, and unit-growth potential. I will use the same valuation date and the latest annual earnings that were public by that date. A company with negative earnings may remain an operating peer, but it cannot be used to calculate a P/E valuation.

## Rejection criteria

- Exclude negative or immaterial EPS from the P/E calculation, because P/E is not meaningful; retain the company as an operating peer when its restaurant model is relevant.
- Exclude franchise-heavy businesses when franchise, royalty, or rent income dominates the business model.
- Reject businesses with substantially different customer, menu, or operating models if those differences drive margins or growth.
- Reject a company if reliable price and annual EPS data are unavailable for December 31, 2025.
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
| CAVA Group (CAVA) | Use with qualification | CAVA owned and operated 367 fast-casual restaurants as of December 29, 2024. | Its company-operated fast-casual model fits the policy. FY2024 diluted EPS of $1.10 includes release of an $83.7 million valuation allowance, so its P/E must be presented with that limitation. CAVA's December 31, 2025 closing price was $58.69. | [CAVA FY2024 Form 10-K, Item 1—Business; Note 7—Income Taxes; Note 12—Earnings Per Share](https://www.sec.gov/Archives/edgar/data/1639438/000162828025007882/cava-20241229.htm); [Nasdaq historical data](https://www.nasdaq.com/market-activity/stocks/cava/historical) |
| Shake Shack (SHAK) | Exclude | As of December 25, 2024, Shake Shack operated 329 company-operated Shacks and had 250 licensed Shacks. | The licensed Shack base is material (250 of 579 system-wide locations). This differs from Chipotle's primarily company-operated restaurant model and meets my franchise-heavy rejection criterion. | [Shake Shack FY2024 Form 10-K, Item 1—Business and Note 1](https://www.sec.gov/Archives/edgar/data/1620533/000162053325000016/shak-20241225.htm) |

## P/E valuation result

Only CAVA is currently usable for a P/E calculation. Its December 31, 2025 price of $58.69 divided by FY2024 diluted EPS of $1.10 produces a **53.35x P/E**. Applying that single-peer reference to Chipotle FY2025 diluted EPS of $1.14 produces an implied Chipotle value of **$60.82 per share**. This is a reference estimate, not a peer range, and is qualified because CAVA's reported EPS includes the valuation-allowance release. Sweetgreen remains an operating peer but is not usable for P/E because it reported a net loss.

**Model run:** `pe_comparables.py` was run with Python 3.12.14. It calculated CAVA at 53.35x P/E and a $60.82 CMG single-peer reference; it reported Sweetgreen's negative EPS as not meaningful for P/E.

**Unresolved:** No second peer currently supports a meaningful P/E, so the result is a single-peer reference rather than a range. The EPS period also differs: Chipotle uses FY2025 EPS from the course project, while CAVA uses the latest annual EPS public by the December 31, 2025 comparison date (FY2024).

## Valuation comparison and provisional call

| Valuation method | Value per CMG share | Basis | Key limitation |
| --- | ---: | --- | --- |
| DCF | $21.69 | FY2025 FCFF; 8.5% WACC; 2.5% terminal growth; $350.545 million cash; no funded debt; 1,342.616 million diluted shares. | The terminal value represents 76.49% of enterprise value, so the result is highly sensitive to long-run growth and the discount rate. |
| Peer P/E | $60.82 | CAVA's 53.35x P/E ($58.69 December 31, 2025 closing price ÷ $1.10 FY2024 diluted EPS) × Chipotle FY2025 diluted EPS of $1.14. | This is a single-peer reference, not a range. CAVA's FY2024 EPS includes a material valuation-allowance release, and the earnings periods do not match. Sweetgreen cannot contribute a P/E because its EPS is negative. |

**Provisional call: Watch / defer.** The DCF and peer reference differ materially, and the peer result is not sufficiently supported to override the DCF because it relies on one qualified peer and mixed-period reported EPS. Before revising the call, obtain a second P/E-usable peer or determine whether a normalized CAVA EPS supports using CAVA as the single reference.
