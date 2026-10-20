# Lab 13 — Meridian Foundation Reserve Mandate

**Student:** Kara Braccio  
**Date:** October 20, 2026  
**Checker:** [mandate.py](mandate.py)  
**Run command:** `python mandate.py`  
**Required probe command:** `python mandate.py --probe`

## D — Decision question

The client permits a candidate portfolio only when it satisfies every **checkable** mandate rule. Before anyone optimizes, the CIO must clarify the undefined calendar-year-loss rule (S9) and state what the pilot should optimize (S10). The numeric checks alone cannot choose an appropriate portfolio.

## Investment policy statement: S1–S10 classification

| Statement | Type | Reason |
|---|---|---|
| S1 — Seven-year horizon; annual rebalancing | Hard constraint | It specifies the investment horizon and an implementation/rebalancing schedule. |
| S2 — CPI + 4% annual net return over rolling five-year periods | Objective | This is the desired investment outcome, rather than a portfolio restriction. |
| S3 — $0.75M quarterly payout; 12 months in cash or daily-liquid government securities | Hard constraint | It sets a specific liquidity reserve amount and eligible assets. |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | It provides a performance reference, but the CIO did not say that holdings must track or replicate it. |
| S5 — Long-only; no borrowing, short sales, or derivatives | Hard constraint | These are explicit prohibited portfolio practices. |
| S6 — No single issuer above 8% | Hard constraint | It is a measurable diversification limit, with stated exemptions. |
| S7 — Annual turnover at most 25% without committee approval | Hard constraint | It is a measurable trading limit, subject to a stated approval exception. |
| S8 — At least 90% redeemable within five business days | Hard constraint | It is a measurable liquidity threshold. |
| S9 — No calendar-year loss greater than 10% | Unverifiable promise | The CIO supplied neither a measurement method nor a breach rule, so it cannot be coded or tested honestly. |
| S10 — No sector/ESG/tax/home-bias preference; no stated pilot optimization | Missing | The absence of preferences is clear, but the objective function or trade-off for a portfolio optimizer is not specified. |

### How the statements map to an IPS

An investment policy statement turns the client’s return objective (S2), horizon and implementation requirements (S1), liquidity needs (S3 and S8), benchmark reference (S4), and investment restrictions (S5–S7) into a documented mandate. S9 remains an unresolved risk-limit instruction rather than a computer rule. S10 identifies the missing optimization objective that the CIO must supply.

## I and V — Checker evidence

`mandate.py` uses only the standard library. It calculates the reserve minimum from the editable inputs rather than typing the result: `4 × $0.75M ÷ $100M = 3.0%`.

The normal run produced the required known-answer results:

| Rule | A | B | C |
|---|---:|---:|---:|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

The issuer check aggregates Acme Corp bonds and Acme Corp stock: Candidate B is 5.0% + 4.0% = 9.0%, so it fails the 8.0% limit.

### Required deliberate-break probe

I ran `python mandate.py --probe`. The probe temporarily changes Candidate A Cash to -2% and the Global equity index fund to 64%, keeping the total at 100%.

- Candidate A’s lowest weight was -2.0 and **failed** long-only.
- Candidate A’s reserve-eligible weight was still 10.0%, so the reserve check passed.
- All other checkable rules still passed.

The probe is implemented as a temporary command-line test, so it does not alter the normal Candidate A inputs.

## Understanding check — complete before submitting

The line I want to be able to explain is the **largest single company** calculation. My answer is:

> Acme bonds and stock are added together because they are issued by the same company. Candidate B has 5% in Acme bonds and 4% in Acme stock, totaling 9%. This exceeds the 8% single-issuer limit under S6, so Candidate B fails that requirement.

Self-check after writing: both securities belong to Acme Corp, so the checker aggregates them into one 9.0% company exposure. Cash, Treasury securities, and diversified funds are exempt under the client’s stated issuer rule.

## E — Attack on the checker: Candidate D

I added Candidate D to `mandate.py`:

| Holding | D weight (%) |
|---|---:|
| Cash | 10 |
| Treasury bills | 0 |
| Treasury 10-year note | 90 |
| All other permitted holdings | 0 |

Candidate D passes every checkable rule: weights total 100.0%, its lowest weight is 0.0%, 100.0% is reserve-eligible, 100.0% is redeemable within five business days, and it has 0.0% single-company exposure because U.S. Treasury securities are exempt.

**Judgment:** Yes, the objection to Candidate D is reasonable because, although it passes the coded rules, its conservative allocation may not generate sufficient returns to meet the foundation's CPI + 4% objective. S2 is the main concern because it establishes the return objective, while S10 highlights that the CIO has not specified what the portfolio should optimize.

### Skeptical-colleague exchange (complete in your own words)

**My challenge to Candidate D:**

> My concern with Candidate D is that it may not generate enough return to meet the foundation's CPI + 4% objective under S2. Even though it meets the coded requirements, this does not necessarily make it a suitable portfolio for the foundation.

**Skeptical colleague’s challenge to my reasoning:**

> **Skeptical colleague:** S2 only states that the foundation wants to earn CPI + 4%. It does not specifically require investing in equities, so we cannot automatically say Candidate D is unsuitable just because it has a conservative allocation.
>
> **My response:** I agree that S2 does not require a specific amount of equity exposure. However, I would still question whether Candidate D's conservative investments could realistically achieve the CPI + 4% return objective. Even though it passes all the coded rules, we need to evaluate its expected returns before deciding if it is suitable for the foundation.

## One question for the CIO — AI closed

I would ask the CIO whether the portfolio should prioritize maximizing returns or minimizing risk while trying to meet the CPI + 4% objective. If the CIO prioritizes returns, I would consider a higher allocation to equities. If the CIO prioritizes minimizing risk, I would consider a larger allocation to government bonds and cash.

## Reflection — AI closed

1. **Why can a portfolio pass every checkable rule and still be wrong for this client?**

   > A portfolio can pass every coded rule but still be unsuitable because the code only checks measurable restrictions, not whether the investments will achieve the client's financial objectives.

2. **The S1–S10 type I was least sure of was:**

   > I was least sure about S9 because the 10% maximum annual loss sounds like a hard constraint, but it cannot be guaranteed or properly tested without more information.

## Project 2 starting point — your client mandate

> **AI-open setup, but this must describe a client you choose.** Before Project 2, replace this block with your client, investment objective, hard constraints, and the one question that must be answered before optimization. Do not present Candidate D as your own client mandate.
