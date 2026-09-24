# Lab 9 — Pro Forma and Floor-Plan Financing

## Model verification

- Ran `python proforma.py` successfully.
- The three statements balance: assets minus liabilities and equity is `$0.0 million` in FY2026E and FY2030E.
- FY2026E revenue is `$18,323.0 million`; FY2030E revenue is `$19,678.3 million`.
- FY2026E operating income is `$844.2 million`; FY2030E operating income is `$971.4 million`.
- FY2026E net income is `$413.6 million`; FY2030E net income is `$527.5 million`.
- FY2026E FCFE is `$211.4 million`; FY2030E FCFE is `$342.3 million`.
- FY2026E cash is `$101.8 million`; FY2030E cash is `$719.8 million`.
- The equity value per share is `$291.75`, and 79.8% of value is after FY2030E.

## Floor-plan financing

1. Floor-plan financing is short-term, inventory-secured borrowing that auto dealers use to buy vehicle inventory. It may be provided by manufacturer-affiliated finance companies or banks.
2. As inventory grows, the floor-plan balance generally grows because it finances the vehicles. The model calculates interest using the opening floor-plan balance. The change in floor-plan debt is included in FCFE as an operating source of cash because it offsets the cash investment in inventory.
3. Removing floor-plan financing makes the company fund its vehicle inventory with its own cash. Losing roughly $2.0–$2.2 billion of inventory financing is much larger than the associated interest savings, which explains why cash falls to about negative $1.1 billion in the video scenario.

Source: [AutoNation 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/350698/000162828026007800/an-20251231.htm).
