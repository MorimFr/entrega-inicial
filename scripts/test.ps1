$ErrorActionPreference = "Stop"

$pythonPath = if (Test-Path ".venv\Scripts\python.exe") {
    ".venv\Scripts\python.exe"
} else {
    "python"
}

& $pythonPath scripts/run_harness.py
exit $LASTEXITCODE

