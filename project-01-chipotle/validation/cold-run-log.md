# Cold-Run Log

**Status:** Complete — final refresh after the integrated sensitivity-grid addition

| Field | Record |
| --- | --- |
| Date and time | October 19, 2026, 3:49 PM ET |
| Fresh environment used | New Python 3.13.15 virtual environment created outside the repository at `C:\Users\KARABR~1\AppData\Local\Temp\cmg-project-coldrun-20261019-final`. It contained only the virtual-environment defaults before installation. |
| Requirements installed | `requirements.txt` contains no third-party packages because the application uses only the Python standard library. `python -m pip install --disable-pip-version-check -r requirements.txt` completed successfully. |
| First application command | `C:\Users\KARABR~1\AppData\Local\Temp\cmg-project-coldrun-20261019-final\Scripts\python.exe run_all.py` |
| First failure or result | No application failure. Exit code 0. The pro forma, integrated FCFF DCF, comparable analyses, and official training-case reconciliation all ran and saved visible output. |
| Time to visible output | 1.256 seconds, measured from the start of `run_all.py` to exit code 0. |
| Fixes made | Before this final run, the normalization review identified and corrected the missing noncash-impairment add-back in integrated FCFF. The finalization pass then added the integrated WACC/terminal-growth sensitivity grid. The DCF, scenario, reverse-DCF, report, validation, and output figures were regenerated. No dependency fix was required. |
| Final successful command | `C:\Users\KARABR~1\AppData\Local\Temp\cmg-project-coldrun-20261019-final\Scripts\python.exe run_all.py` |
| Output location | `outputs/latest-model-output.txt` |

## Result preserved

The final cold run includes the normal three-statement checks, the integrated
DCF directionality and enterprise-to-equity bridge checks, comparable-company
outputs, and the official training-case reconciliation. The combined result is
saved in `outputs/latest-model-output.txt`.
