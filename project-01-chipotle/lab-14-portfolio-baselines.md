# Lab 14 — Meridian Portfolio Baselines

**Student:** Kara Braccio  
**Date:** October 20, 2026  
**Files:** [portfolio.py](portfolio.py) and [mandate.py](mandate.py)  
**Run commands:** `python portfolio.py` and `python mandate.py`

## Question

The portfolio engine calculates each simple Meridian baseline's expected return, volatility, and reserve-eligible share from the supplied course-authored inputs. On return alone, the benchmark meets the 6.5% objective; however, it does not meet the Meridian mandate because it holds no reserve-eligible assets. The other two baselines meet more of the mandate's liquidity needs but do not meet the stated expected-return objective.

## Inputs and calculation method

The expected return is the weighted average of the four sleeve returns. The covariance matrix is calculated from the supplied data:

`covariance(i, j) = correlation(i, j) × volatility(i) × volatility(j)`

Portfolio volatility is the square root of the full variance calculation, `sqrt(w' × covariance matrix × w)`. This includes the correlation/covariance terms between sleeves; it does not simply add or square individual volatilities.

The 6.5% objective is CPI + 4%, using CPI of 2.5% as the labelled course estimate. Reserve-eligible sleeves are Treasury bills and the Treasury 10-year note, as defined in Lab 13.

## Known-answer verification

| Portfolio | Weights: bills / 10-year / IG / equity (%) | Expected return | Volatility | Reserve-eligible | Meets 6.5% objective? |
|---|---:|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | no |

All figures above are computed from the editable input tables in `portfolio.py`.

## Meridian mandate check

I added the benchmark portfolio as Candidate E in `mandate.py`: 40% investment-grade bond fund and 60% global equity index fund. It has a 0.0% reserve-eligible share, so it fails Meridian's S3 reserve requirement of at least 3.0%. The benchmark also passes the other checkable rules, but that does not cure the S3 failure.

This shows that the client’s own benchmark is a performance reference (S4), not automatically a compliant portfolio under the full mandate.

## Correlation validation and changed-input test

The engine refuses to run if a correlation falls outside -1 to 1 or if the table is not symmetric.

Required correlation test:

- Change the investment-grade-bond-fund / global-equity-index-fund correlation from 0.25 to 0.50 in **both** cells.
- The benchmark volatility rises from 10.46% to **11.00%**.
- Restore both cells to 0.25 after the test.

**Run result:** I tested both changed correlation cells together and the benchmark volatility was 11.00%. The saved correlation table remains at 0.25 in both cells.

Required refusal test:

- Change either IG–equity correlation cell to 1.3.
- `portfolio.py` stops with an input-validation error rather than calculating a result.
- Restore the input to 0.25 after the test.

**Run result:** The validator refused the 1.3 correlation with: `Correlation for Investment-grade bond fund / Global equity index fund is outside -1 to 1: 1.3`.

## Explain the code — complete in your own words

Portfolio volatility measures how much a portfolio's returns fluctuate over time. It is commonly used as a measure of investment risk because it shows how much portfolio returns move up and down. The `portfolio_volatility` function loops through every pair of holdings, multiplies each pair's weights by its covariance, adds those terms into variance, and then takes the square root.

**Owen's question:** If minimizing portfolio volatility reduces risk, why would we not invest everything in cash or government bonds?  
**My answer:** While cash and government bonds may reduce volatility, they may not generate enough return to meet the foundation's CPI + 4% objective under S2. We need to balance minimizing risk with earning sufficient returns to meet the foundation's long-term goals.

## Diversification

Two risky assets can have lower combined risk when their correlation is below +1 because they do not move perfectly together. When one investment performs poorly, the other may perform better, reducing overall portfolio fluctuations. This is the benefit of diversification. The benchmark's calculated portfolio volatility of 10.46% reflects the combined risk of its 60% equity and 40% bond allocation, accounting for the correlation between the two assets.

**My hand calculation:**

`Portfolio volatility = sqrt((0.60 × 0.16)^2 + (0.40 × 0.06)^2 + 2 × 0.60 × 0.40 × 0.16 × 0.06 × 0.25) = 0.1046, or 10.46%.`

## Reflection

Inverse volatility assigns higher weights to assets with lower volatility, which is why Treasury bills receive the largest allocation. Since Treasury bills have very little price fluctuation, the strategy heavily favors them over riskier investments such as stocks.

I would show the CIO the 60/40 benchmark first because it is the foundation's stated benchmark under S4. It provides a useful starting point for evaluating risk and return, whereas the inverse-volatility portfolio may be too conservative to achieve the CPI + 4% objective.
