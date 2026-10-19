# Integrated Low, Base, and High Scenario Assumptions

These are named analyst cases, not forecasts of probability. Each case changes
revenue growth, gross margin, and capital spending in `models/cmg_proforma.py`.
Those changes flow through all five forecast years of the income statement,
balance sheet, cash flow statement, FCFF calculation, and DCF bridge.

| Scenario | Revenue growth, FY2026E-FY2030E | Gross margin | Capital spending, FY2026E-FY2030E | Operating interpretation |
| --- | --- | ---: | --- | --- |
| Low / downside | 4.0%, 4.5%, 5.0%, 5.0%, 5.0% | 24.5% | $700m, $725m, $750m, $750m, $750m | Weaker transactions and comparable sales, fewer openings, and food/labor pressure. Lower capital spending reflects a slower opening pace. |
| Base | 9.0%, 7.0%, 6.5%, 6.0%, 5.5% | 25.5% | $834.1m, then $850m annually | Openings support sales despite flat FY2026 comparable sales; the model uses the latest historical gross-margin ratio and management's FY2026 capex guidance. |
| High / upside | 11.0%, 9.0%, 8.0%, 7.0%, 6.0% | 26.2% | $925m, then $950m annually | Transaction recovery and successful openings support revenue and margin. Higher capital spending funds the greater expansion. |

## Evidence and challenge

The FY2025 Form 10-K reports FY2025 comparable-restaurant-sales growth of
negative 1.7%, driven by a 2.9% transaction decline, while 334 company-owned
restaurants opened during the year. Management's FY2026 outlook called for
approximately flat comparable restaurant sales, 350-370 openings, and capital
expenditures of approximately $834.1 million. These facts support using a
growth case that depends on unit expansion, as well as a downside case if
transactions or openings disappoint. The low and high numeric paths are the
student's stress cases rather than management guidance.

Source: [Chipotle FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm), MD&A and Outlook, pp. 24-25 and 29.

Evidence that would change the cases: subsequent quarterly filings or earnings
releases showing sustained positive/negative transaction growth, openings above
or below the plan, material food or labor-cost movement, or revised capital
expenditure guidance. The scenarios do not assign probabilities and should not
be interpreted as price targets.
