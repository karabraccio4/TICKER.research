# WACC Support — Chipotle Mexican Grill (CMG)

**Valuation date:** February 5, 2026  
**Currency:** U.S. dollars  
**All dollar amounts:** USD millions unless stated otherwise

## Method

Cost of equity is estimated with CAPM:

`Cost of equity = risk-free rate + beta × equity risk premium`

WACC is calculated as:

`WACC = E / (D + E) × cost of equity + D / (D + E) × after-tax cost of debt`

## Dated inputs and sources

| Input | Value | Treatment and source |
| --- | ---: | --- |
| Risk-free rate | 4.21% | U.S. Treasury daily **10-year nominal Treasury par yield** on February 5, 2026. [U.S. Treasury daily yield-curve data](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value=2026). |
| Beta | 0.92 | January 2026 levered beta for the 64-firm **Restaurant/Dining** industry. This is an industry proxy, not a CMG-specific regression beta. [Damodaran Cost of Capital data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/wacc.html). |
| U.S. implied equity risk premium | 4.23% | Damodaran's historical implied U.S. ERP for 2025, published in the January 2026 update. [Historical Implied Equity Risk Premiums](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histimpl.html). |
| CMG share price | $38.45 | CMG closing price on February 5, 2026. [CMG historical prices](https://finance.yahoo.com/quote/CMG/history/). |
| Diluted share basis | 1,342.616 | FY2025 diluted weighted-average shares. Used for both the DCF per-share bridge and the equity-weight calculation, while recognizing that it is not a point-in-time share count. [CMG FY2025 Form 10-K, Statements of Income](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm). |
| Funded debt | $0.000 | Chipotle had no outstanding revolver borrowings at December 31, 2025. The facility would bear SOFR + 1.125% if drawn, but that is not a cost of debt applied to zero funded debt. [CMG FY2025 Form 10-K, Note 12](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm). |
| Tax rate | 23.6% | FY2025 effective income tax rate. [CMG FY2025 Form 10-K, Income Taxes](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm). |
| Operating lease liabilities | $5,075.814 | Excluded from funded debt. CMG records operating lease cost primarily in occupancy, other operating costs, G&A, and pre-opening expense; the FCFF forecast begins with EBIT after those operating costs. [CMG FY2025 Form 10-K, Leases](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm). |

## Calculation

`Market equity value = $38.45 × 1,342.616 = $51,623.585`

`Cost of equity = 4.21% + (0.92 × 4.23%) = 8.1016%`

Because funded debt is $0.000 under the selected convention:

`E / (D + E) = 100.0%` and `D / (D + E) = 0.0%`

`WACC = 100.0% × 8.1016% + 0.0% × after-tax cost of debt = 8.1016%`

The model uses **8.10%** (the unrounded code value is 8.1016%).

## Lease and valuation-definition convention

The model treats the $5.076 billion operating lease liability as an operating obligation, rather than funded financial debt. This is consistent with the FCFF DCF: projected EBIT includes operating lease cost, so adding the lease liability as debt without a matching adjustment to EBIT/FCFF would mix conventions. The enterprise-to-equity bridge therefore subtracts only funded debt ($0.000) and adds the modeled cash balance.

The same convention must be used for the future EV/EBITDA peer comparison: exclude operating lease liabilities from enterprise value and use EBITDA before lease-adjustment. A lease-adjusted EV/EBITDA comparison would require both adding lease liabilities to EV and using a lease-adjusted earnings measure; this project does not do that.

## Limitation and evidence that would change the input

The 0.92 beta is an industry proxy. A CMG-specific beta calculated from a stated return window and market index, or a defensible comparable-company unlever/relever analysis, could change the cost of equity. The point-in-time share count may also differ from FY2025 weighted-average diluted shares. These are research limitations, not adjustments made in the model.
