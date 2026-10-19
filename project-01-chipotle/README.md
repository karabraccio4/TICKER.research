# Chipotle Project 1 — Corporate Finance Application

## What this project evaluates

This locally runnable application evaluates whether a buy-side investment fund
should initiate a position in Chipotle Mexican Grill, Inc. (NYSE: CMG). It
contains a five-year Chipotle pro forma, an FCFF DCF derived from that pro
forma, and a developing comparable-company analysis.

## Current recommendation and valuation date

- **Recommendation:** Watch / defer.
- **Valuation date:** February 5, 2026, the first full trading day after
  Chipotle's FY2025 Form 10-K became public after market close on February 4.

The preserved Edition A baseline and working Edition B are in the reports
folder. The application remains incomplete; open gaps are identified in the
validation records and should not be represented as completed evidence.

## Project layout

- models/ — locally runnable financial-model scripts.
- research/ — filing notes, source-based history, and assumptions.
- reports/ — preserved Edition A and developing Edition B reports.
- outputs/ — saved visible output from final model runs.
- validation/ — validation evidence, cold-run log, and AI-use/normalization record.

## Install requirements

From the project root, install the declared dependencies:

    python -m pip install -r requirements.txt

The current valuation application uses only the Python standard library, so
this command does not install any third-party packages at present.

## Run the full application

From the project root, run:

    python run_all.py

This command runs the five-year pro forma, the integrated FCFF DCF, and the
current P/E comparable analysis. It prints results to the terminal and saves a
combined visible-output file at outputs/latest-model-output.txt. The integrated
DCF imports the Chipotle pro forma and derives FCFF from the forecast operating
statements. Its WACC remains provisional until the WACC workpaper is completed.

## Outputs and validation records

- **Visible output:** outputs/latest-model-output.txt after running
  python run_all.py.
- **Validation record:** validation/validation-record.md.
- **Cold-run log:** validation/cold-run-log.md.
- **AI-use and normalization record:** validation/ai-use-and-normalization-record.md.

## Before submission

Complete the open validation records, save final visible outputs, add the
required comparable-company enterprise-value multiple, document WACC support,
perform the cold run, and add recordings and corrected transcripts.
