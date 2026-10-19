# Chipotle Project 1 — Corporate Finance Application

This repository contains a developing buy-side equity-research application for
Chipotle Mexican Grill, Inc. (NYSE: CMG).

## Current status

The preserved Edition A baseline and a working Edition B are available in the
reports folder. The application is still incomplete. Open gaps are tracked in
the validation records and should not be represented as completed evidence.

## Project layout

- models/ — locally runnable financial-model scripts.
- research/ — filing notes, source-based history, and assumptions.
- reports/ — preserved Edition A and developing Edition B reports.
- outputs/ — saved visible output from final model runs.
- validation/ — validation evidence, cold-run log, and AI-use/normalization record.

## Current model commands

Run these commands from the project root:

    python models\cmg_proforma.py
    python models\cmg_integrated_dcf.py
    python models\pe_comparables.py

The integrated DCF imports the Chipotle pro forma and derives FCFF from the
forecast operating statements. Its WACC remains provisional until the WACC
workpaper is completed.

## Valuation-date convention

The developed valuation uses February 5, 2026, the first full trading day after
the FY2025 Form 10-K was accepted after market close on February 4, 2026.

## Before submission

Complete the open validation records, save final visible outputs, add the
required comparable-company enterprise-value multiple, document WACC support,
perform the cold run, and add recordings and corrected transcripts.
