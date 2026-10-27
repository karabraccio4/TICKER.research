# Lab 16 — Provenance Gate

## Goal

Build a point-in-time filter for a fictional card-spend index and show what
could actually have been known on the 31 March 2026 decision date.

## Key idea

The month measured is not necessarily the date investors could see a value.
For every observation, I need to distinguish:

- **Measurement time:** the month the index describes.
- **Publication time:** the date that value was released.
- **Revision time:** the date a later version of an already measured month was released.

Using data that was published after a decision date is look-ahead bias. It
makes a backtest appear to use information that would not have existed in
real time.

## Filter process

The script in `asof.py` applies these rules in order:

1. Quarantine rows without a ticker.
2. Remove exact duplicates.
3. Remove values published after the decision date.
4. For each ticker and measured month, keep the latest publication that was
   knowable by the decision date.

## Verified row funnel

| Funnel step | Rows removed |
| --- | --- |
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

## Results on 31 March 2026

The signal is the percent change from the prior month to the latest available
month for each ticker.

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

For AAA, the naive result uses March's 109 reading, which was published on 10
April. It was not available on the 31 March decision date. The knowable
signal used January's 101 and the latest available February revision of 103:
`(103 / 101 - 1) * 100 = +1.98%`.

## Later-date check

Changing `DECISION_DATE` to `2026-04-15` made every as-of signal equal its
naive signal. This confirms that the difference at 31 March came from
information published later. The script has been returned to `2026-03-31`.

## Reflection

Rule 3, the publication-date cutoff, removed the AAA March row that created
the largest difference between the as-of and naive results. A backtest built
on the naive column would falsely claim that it could trade on March momentum
before the March data was released.
