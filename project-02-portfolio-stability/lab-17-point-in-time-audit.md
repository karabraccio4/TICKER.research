# Lab 17 — Point-in-Time Audit

## D — The question

Was each number in my series knowable on the day I would have traded on it —
and may Project 2 use it?

## Partner discussion

**Rate:** Federal Reserve federal funds rate.

**Why it matters:** It affects borrowing costs, consumer spending, and company
valuations. When rates rise, borrowing becomes more expensive, which can slow
company growth and reduce stock valuations. When rates fall, companies can
borrow more cheaply, potentially encouraging investment and increasing
valuations.

Owen recorded this explanation for the partner discussion.

## R — Real data sources

Lab 17 uses FRED's current CSV download and ALFRED's historical-vintage CSV
download. The starting rate series are BAA, FEDFUNDS, DGS10, and
MORTGAGE30US. A FRED page shows the series as it reads today; ALFRED can show
the values that were available on an earlier date.

## I — App build

`asof_app.py` downloads the current FRED vintage and the selected ALFRED
vintage separately for each selected series. It treats `.` as a missing value,
displays current-value charts from the chosen start date, and reports the
latest observation known on the selected date. Its audit table compares the
known vintage with today's vintage by counting later observations and changed
values on shared observation dates.

## V — Known-answer validation

With **As known on** set to 5 October 2026, the app's ALFRED vintage returns:

| Series | Last date known | Value |
| --- | --- | --- |
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

The PAYEMS probe with **As known on** set to 15 January 2025 returns December
2024 at 159,536 as known then. Today's December 2024 value is 158,316, and
381 shared observations have revisions. This confirms the app uses ALFRED for
the historical vintage rather than reading today's FRED data twice.

## E — My series data card: FEDFUNDS

| Field | Evidence |
| --- | --- |
| Source and link | Board of Governors of the Federal Reserve System (US), [FRED FEDFUNDS page](https://fred.stlouisfed.org/series/FEDFUNDS); release: H.15 Selected Interest Rates. |
| What it measures | The effective federal funds rate: the weighted-average overnight rate at which depository institutions trade federal funds. |
| Units | Percent, not seasonally adjusted; monthly average of daily figures. |
| Publication lag | The 30 September 2026 ALFRED vintage ended at August 2026 (3.63). September's 3.75 appeared in the current vintage with a FRED update timestamp of 1 October 2026, so that month was not available on 30 September. |
| Revisions | FRED states that all data are subject to revision. In this 30 September versus 29 October app comparison, the shared FEDFUNDS observations had 0 revisions. |
| Download date | 29 October 2026. |

### Three-value page check

I checked the current FRED page against the app: July 2026 = 3.63, August
2026 = 3.63, and September 2026 = 3.75. The values matched.

### Partner attack: publication date

The publication date is the field I trust least because a monthly observation
can describe September but still be unavailable on 30 September. The app's
ALFRED result ended at August on that date, while the FRED page shows the
September value was updated on 1 October; this is evidence for using the
vintage date rather than the month label.

## Project 2 decision

**Admit, with a point-in-time rule:** FEDFUNDS is a monthly average published
after the measured month ends. On 30 September 2026, the latest knowable value
was August's 3.63; September's 3.75 was published on 1 October. The tested
vintages showed no revisions on shared dates, but FRED says the data may be
revised. Project 2 may use FEDFUNDS only from the ALFRED vintage available on
each decision date, never by applying today's values with an assumed fixed
lag. I would quarantine it instead if I could not obtain the appropriate
ALFRED vintage or document the decision date.
