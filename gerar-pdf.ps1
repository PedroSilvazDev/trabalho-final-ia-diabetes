$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = if (Test-Path ".\.venv\Scripts\python.exe") {
    ".\.venv\Scripts\python.exe"
} else {
    "python"
}

Write-Host "=== Gerando relatorio PDF ===" -ForegroundColor Cyan

& $python -m pip install -q reportlab scikit-learn pandas matplotlib seaborn joblib numpy

Write-Host "Treinando modelos e gerando graficos..."
& $python main.py

Write-Host "Gerando PDF..."
& $python scripts\gerar_relatorio.py

Write-Host ""
if (Test-Path "docs\relatorio.pdf") {
    $size = (Get-Item "docs\relatorio.pdf").Length
    Write-Host "PDF salvo em: docs\relatorio.pdf ($size bytes)" -ForegroundColor Green
} else {
    Write-Host "PDF automatico falhou. Alternativa:" -ForegroundColor Yellow
    Write-Host "1. Rode: python main.py"
    Write-Host "2. Abra docs\relatorio.html no navegador"
    Write-Host "3. Ctrl+P -> Salvar como PDF -> docs\relatorio.pdf"
}
