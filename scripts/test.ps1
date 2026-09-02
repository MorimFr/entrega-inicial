$ErrorActionPreference = "Stop"

$pythonPath = if (Test-Path ".venv\Scripts\python.exe") {
    ".venv\Scripts\python.exe"
} else {
    "python"
}

& $pythonPath -m ruff check .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $pythonPath -m pytest
exit $LASTEXITCODE

