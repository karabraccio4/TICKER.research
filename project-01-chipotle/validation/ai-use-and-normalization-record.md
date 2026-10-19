# AI-Use and Base-Year Normalization Record

**Project:** Chipotle Mexican Grill, Inc. (CMG)

**Valuation date:** February 5, 2026
**Status:** Completed record of assistance actually used and independently
checked. This record does not claim that AI made the investment judgment.

## AI-use record

| AI-assisted task | What Codex helped do | Student's independent check and disposition | Evidence/location |
| --- | --- | --- | --- |
| Project organization and documentation | Organized the source map, project folders, README, Edition B, validation record, and saved-output workflow. | The student reviewed the created files and retains responsibility for the sources, assumptions, and recommendation. | `README.md`, `reports/Project_1_Edition_B_Chipotle.md`, and `validation/` |
| Model integration and testing | Helped revise the Python model so the DCF derives FCFF from the Chipotle pro forma, added scenarios, bridge checks, reverse DCF, and the training-case test. | The student reviewed the visible outputs and the normal and intentional-failure runs. The code output is evidence to inspect, not an unreviewed AI conclusion. | `models/cmg_proforma.py`, `models/cmg_integrated_dcf.py`, `validation/training_case_reconciliation.py`, and `outputs/latest-model-output.txt` |
| WACC calculation and convention | Helped organize the CAPM calculation: risk-free rate + beta × ERP; $0 funded debt under the selected lease convention; resulting WACC 8.1016%. | **Accepted with qualification.** The student independently checked the Treasury rate, Damodaran beta and ERP, Chipotle debt, and lease treatment. The student accepts the calculation but qualifies the 0.92 beta as a Restaurant/Dining industry proxy, not a CMG-specific beta. | `research/wacc-support.md`; U.S. Treasury, Damodaran, and CMG FY2025 Form 10-K links within that file |
| Research synthesis | Helped locate and organize filing facts and comparable-company inputs. | The student checked the cited source/definition for FY2025 cash capex and the dated WACC inputs; unsupported conclusions are kept as limitations rather than accepted facts. | `research/cmg-history-and-assumptions.md`, `My_Own_Peer_Policy.md`, and `validation/validation-record.md` |

## Independently checked AI output

**Output reviewed:** The proposed **8.1016% WACC** for the February 5, 2026
valuation date.

**Calculation:**

`Cost of equity = 4.21% risk-free rate + (0.92 beta × 4.23% ERP) = 8.1016%`

With $0 funded debt, the selected capital-structure convention makes WACC equal
to cost of equity.

**Independent evidence checked by the student:**

- U.S. Treasury February 5, 2026 10-year nominal yield: 4.21%.
- Damodaran January 2026 Restaurant/Dining levered beta: 0.92.
- Damodaran historical implied U.S. ERP: 4.23%.
- CMG FY2025 Form 10-K, Note 12: $0 revolver borrowings at year-end.
- CMG FY2025 Form 10-K lease disclosure: operating lease costs are included in
  operating expenses before EBIT.

**Disposition:** Accepted for the model, but qualified. The industry beta is
not a CMG-specific regression beta; a documented company-specific beta or
comparable unlever/relever analysis could change WACC and the valuation.

## Base-year normalization / contamination catalog

The base year is FY2025. “Normalized” means a documented adjustment to remove
or replace a reported base-year item. No adjustment is made merely because an
item could vary in the future.

| Item reviewed | FY2025 evidence reviewed | Treatment | Why |
| --- | --- | --- | --- |
| Impairment charges ($27.503m in the model's FY2025 history) | The FY2025 10-K and the model's historical inputs; the 10-K identifies impairment charges as a possible driver of quarterly results. | **Separately disclosed; no earnings normalization.** The model subtracts impairment in operating income and adds it back in FCFE/FCFF cash-flow logic because it is noncash. It is forecast at the historical revenue ratio, which remains a limitation to revisit. | The available evidence does not establish that the FY2025 amount was a one-time item that should be removed from the normalized base. |
| FY2025 marketing/promotion, utility inflation, food-cost inflation, and tariff effects | FY2025 MD&A attributes changes in restaurant costs to lower sales volumes, marketing/promotion, food and utility inflation, tariffs, and menu-price effects. | **Left unchanged and separately disclosed.** These effects remain within the FY2025 historical margin rather than being removed. | They are operating factors, and the reviewed filing evidence does not isolate a supported, nonrecurring dollar amount to normalize. Their persistence is addressed through scenarios and sensitivity, not a fabricated adjustment. |
| Stock-based compensation/tax impacts, litigation/settlement costs, restaurant openings/closures, and other non-operating costs | FY2025 MD&A says quarterly results can be affected by these items. | **No adjustment made.** | The reviewed disclosure identifies possible variability but does not, in the source map used here, quantify a specific FY2025 one-time amount suitable for removal. |
| Operating lease liabilities ($5,075.814m) | FY2025 Form 10-K lease note and operating-expense disclosure. | **Not a normalization; separately disclosed accounting convention.** Excluded from funded debt in the DCF bridge and EV/EBITDA because EBIT already includes operating lease cost. | Adding the operating lease liability as debt without a matching lease adjustment to EBIT/EBITDA would mix conventions. See `research/wacc-support.md`. |
| Cash and cash equivalents ($350.545m) | FY2025 balance sheet. | **No normalization; disclosed bridge assumption.** Added as non-operating cash in the DCF bridge. | The model has not established what portion is operational cash. This is a stated limitation, not an unsupported adjustment. |

## Conclusion and remaining limitations

No base-year normalization adjustment is claimed without filing support. The
model keeps the FY2025 reported base, labels the impairment and lease treatment,
and identifies operating-cost and cash-treatment uncertainties for future
research. The Watch / defer recommendation remains the student's judgment:
AI assistance organized and tested the evidence-and-model stack but did not
replace the student's source checks, assumptions, or decision.
