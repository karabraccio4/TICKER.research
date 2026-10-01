# Feedback From My Partner — Chipotle

## Questions received and my responses

- **Selection and evidence question:** Why did you select Chipotle when FY2025 comparable restaurant sales fell 1.7% and transactions fell 2.9%?
  - **My response:** I selected Chipotle because it is a primarily company-operated fast-casual restaurant company with measurable unit growth, comparable-sales data, and enough financial history to model. The comparable-sales decline is a risk, but it is not proof of a permanent decline. Chipotle opened 334 company-owned restaurants in FY2025, so unit growth still contributed to total revenue growth.
  - **Follow-up question:** Which source supports the comparable-sales decline, transaction decline, and restaurant openings?
  - **My response:** Chipotle's FY2025 Form 10-K, MD&A pages 24–25, reports a 1.7% comparable-sales decline, a 2.9% transaction decline, and 334 company-owned restaurant openings.

- **Model and valuation question:** Your DCF gives $21.69 per share, while your FCFE pro forma gives $19.65. Why are they different?
  - **My response:** The models use different cash-flow definitions and discount rates. The DCF begins with FCFF of $1,447.590 million, calculated as FY2025 operating cash flow of $2,113.926 million less capital expenditures of $666.336 million, and discounts FCFF at an 8.5% WACC. The pro forma forecasts FCFE and discounts it using a 9.0% cost of equity. Therefore, the two values should not be identical.
  - **Follow-up question:** What is the biggest limitation of both models?
  - **My response:** Terminal value is the largest limitation. It represents 76.49% of enterprise value in the DCF and about 76.0% of equity value in the FCFE pro forma, so the results are highly sensitive to long-run growth and discount-rate assumptions.

- **Peer valuation question:** Why should the $60.82 CAVA P/E reference be considered when your intrinsic values are approximately $20–$22 per share?
  - **My response:** I treat it only as a qualified reference, not as a peer range or my primary conclusion. CAVA is the only P/E-usable peer; Sweetgreen had negative EPS, while Wingstop and Shake Shack did not fit my company-operated peer policy. CAVA's FY2024 EPS also included a material valuation-allowance release, and its earnings period does not match Chipotle's FY2025 EPS.

- **Sensitivity and interpretation question:** You identified revenue growth as the largest driver. Does that ranking depend on the ranges you selected?
  - **My response:** Yes. The ranking is limited to the equal plus-or-minus 1 percentage-point ranges I tested. Revenue growth had a $2.42 value-per-share span, compared with $2.09 for gross margin, but a different range could change the ranking. Revenue growth is my first research priority because I need more evidence on comparable restaurant sales, transaction recovery, and new restaurant openings.

## Partner's explanation back and my correction

- **Partner's explanation:** Chipotle remains Watch / defer because the intrinsic valuations are around $20–$22 per share, while the peer P/E reference is much higher but is not reliable enough to override the intrinsic valuations. Revenue growth was the main driver over the tested sensitivity ranges. The largest limitations are terminal-value dependence and the single qualified P/E peer.
- **My correction:** None. This explanation accurately reflected my conclusion, main driver, and limitations.

## Feedback received

- **Strength:** My partner noted that I tied the FY2026 9.0% revenue-growth assumption to management's flat comparable-sales guidance and its planned 350–370 company-owned restaurant openings, rather than assuming same-store sales would immediately recover.
- **Improvement:** My partner recommended documenting a CAPM-based cost of equity and obtaining a second P/E-usable peer or normalizing CAVA's EPS before placing more weight on the peer valuation.

## What I will keep, revise, or investigate

- **Keep:** I will keep the Watch / defer conclusion and the distinction between the DCF, FCFE pro forma, and qualified single-peer P/E reference. Both intrinsic models produce values near $20–$22 per share, while the P/E reference has material limitations.
- **Revise or investigate:** I will investigate a CAPM-supported cost of equity, the amount of cash that is operational rather than excess, transaction recovery and comparable sales, new-unit returns, and a second P/E-usable peer or normalized CAVA EPS.
- **Effect of the review:** The review does not change my Watch / defer conclusion. It reinforces my research priority: determine whether transaction growth and new-unit economics can support the forecast revenue-growth path.
- **Unresolved work:** I have not run a CAPM calculation, normalized CAVA's EPS, obtained a second P/E-usable peer, or tested the portion of cash required for operations. These are open research tasks, not completed model repairs.

## Reflection

- **Question that made me reconsider something:** The question about why the DCF and FCFE pro-forma values differ made me focus on the importance of using the correct cash-flow definition and discount rate for each valuation method.
- **What I understand better now:** I better understand that agreement between two intrinsic valuations is useful, but it does not eliminate uncertainty when terminal value represents about three-quarters of total value. I also understand why the CAVA result should remain a qualified reference rather than determine my conclusion.

## Existing Chipotle analysis and outputs

- [FY2025 10-K notes](research/Chipotle_FY2025_10-K_Notes.md)
- [History and forecast assumptions](research/cmg-history-and-assumptions.md)
- [Peer policy](My_Own_Peer_Policy.md)
- [Lab 11 sensitivity notes](research/lab-11-input-notes.md)
- [DCF model](models/dcf.py)
- [Chipotle FCFE pro-forma model](models/cmg_proforma.py)
- [P/E comparables model](models/pe_comparables.py)
- [Project 1 report](reports/Project_1_Edition_A_Chipotle.md)
