# Lab 20 — Project 2 readiness checkout

## Submit these three GitHub links

1. **README and reproducible tool:** [README.md](../README.md)
2. **Decision, numbers, and validation:** [decision-memo.md](decision-memo.md)
3. **Lab 20 evidence and honest status:** this file, `docs/lab-20-checkout.md`

## Committee decision

**Pilot, not adopt.** Reverse this decision only after the client approves a forward-looking return-estimate method and the history window.

## Reproducibility evidence

- One command: `python project2_report.py`
- Baseline: 75% BIL / 0% IEF / 0% LQD / 25% VT; 5.51% expected return; 3.84% volatility; 75.0% reserve eligible.
- Window test: last 36 monthly returns produces 90% BIL / 10% VT; the largest allocation move is 15 percentage points.
- VT stress reference: a 1.0-percentage-point reduction in VT's expected annual return produces 70% BIL / 30% VT; 5.58% expected return; 4.58% volatility; 70.0% reserve eligible.
- GitHub-readable output: [output/project2-result.txt](../output/project2-result.txt)
- Full validation: [validation.md](validation.md)

## Lab 20 status

| Requirement | Location | Status |
|---|---|---|
| Interactive tool | [app.py](../app.py) | Ready; uploaded-CSV handling tested. |
| README command | [README.md](../README.md) | Ready. |
| Visible output | [project2-result.txt](../output/project2-result.txt) | Ready. |
| Decision memo | [decision-memo.md](decision-memo.md) | Ready. |
| Validation and AI use | [validation-and-ai-use.md](validation-and-ai-use.md) | Validation, AI disclosure, and completed Locked Changed-Input Record. |
| Cold run | [cold-run-note.md](cold-run-note.md) | AI-assisted dry run documented; not a human-partner result. |
| Changed-input record | [locked-changed-input-record.md](locked-changed-input-record.md) | Completed: prediction commit and separate results commit are linked. |
| Videos 1–3 | [video-manifest.md](video-manifest.md) | Links pending recording/upload. |

## Exact supporting-file titles

- `README.md` — Project 2 — Portfolio stability decision
- `docs/decision-memo.md` — Decision memo — Project 2 portfolio stability
- `docs/lab-20-checkout.md` — Lab 20 — Project 2 readiness checkout
- `docs/validation.md` — Validation evidence
- `docs/cold-run-note.md` — Lab 20 cold-run note
- `docs/locked-changed-input-record.md` — Locked changed-input record — Lab 20
- `docs/video-manifest.md` — Video manifest — add working links after recording
- `output/project2-result.txt` — Project 2: Portfolio stability decision
- `project2_report.py` — Reproducible Project 2 decision report
- `app.py` — Lab 15 Streamlit portfolio-stability app
