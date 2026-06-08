$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".\.venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" main.py

Write-Host ""
Write-Host "Pronto! Graficos em outputs\figures e modelos em models\" -ForegroundColor Green
