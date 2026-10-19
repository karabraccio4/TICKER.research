"""Run the current Chipotle valuation application and save visible output."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "outputs" / "latest-model-output.txt"
SCRIPTS = (
    ROOT / "models" / "cmg_proforma.py",
    ROOT / "models" / "cmg_integrated_dcf.py",
    ROOT / "models" / "pe_comparables.py",
    ROOT / "models" / "ev_ebitda_comparables.py",
)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    sections = []
    for script in SCRIPTS:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        section = f"\n{'=' * 72}\n{script.name}\n{'=' * 72}\n{result.stdout}"
        if result.stderr:
            section += f"\nSTDERR:\n{result.stderr}"
        sections.append(section)
        if result.returncode != 0:
            OUTPUT_PATH.write_text("".join(sections), encoding="utf-8")
            print("".join(sections))
            raise SystemExit(f"{script.name} failed; partial output saved to {OUTPUT_PATH}.")

    OUTPUT_PATH.write_text("".join(sections), encoding="utf-8")
    print("".join(sections))
    print(f"\nSaved visible output to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
