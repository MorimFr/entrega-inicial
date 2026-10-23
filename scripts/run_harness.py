"""Harness único com lint e relatórios persistentes (local, Docker e CI)."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    commands = [
        [sys.executable, "-m", "ruff", "check", "."],
        [
            sys.executable,
            "-m",
            "pytest",
            "-o",
            "addopts=-ra --strict-markers",
            "--cov=campusflow",
            "--cov-fail-under=90",
            "--cov-report=term-missing",
            f"--cov-report=xml:{args.artifacts / 'coverage.xml'}",
            f"--cov-report=html:{args.artifacts / 'htmlcov'}",
            f"--junitxml={args.artifacts / 'junit.xml'}",
        ],
    ]
    with (args.artifacts / "test-output.log").open("w", encoding="utf-8") as log:
        for command in commands:
            print("RUN: " + " ".join(command), flush=True)
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            ) as process:
                assert process.stdout is not None
                for line in process.stdout:
                    print(line, end="", flush=True)
                    log.write(line)
                code = process.wait()
            log.flush()
            if code:
                return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
