$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$remoteUrl = "https://github.com/PedroSilvazDev/trabalho-final-ia-diabetes.git"
$logFile = Join-Path $PSScriptRoot "_push_log.txt"
$commitMessage = "Trabalho final IA - predicao de diabetes com KNN e SVM"

function Log($msg) {
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $msg"
    Add-Content -Path $logFile -Value $line
    Write-Host $line
}

"" | Set-Content -Path $logFile -Encoding UTF8
Log "=== Push para GitHub ==="

if (-not (Test-Path ".\.git")) {
    Log "Inicializando git..."
    git init 2>&1 | ForEach-Object { Log $_ }
    git branch -M main 2>&1 | ForEach-Object { Log $_ }
}

$remotes = git remote 2>$null
if ($remotes -contains "origin") {
    git remote set-url origin $remoteUrl 2>&1 | ForEach-Object { Log $_ }
    Log "Remote origin atualizado."
} else {
    git remote add origin $remoteUrl 2>&1 | ForEach-Object { Log $_ }
    Log "Remote origin adicionado."
}

Log "Adicionando arquivos..."
git add . 2>&1 | ForEach-Object { Log $_ }

$status = git status --porcelain 2>&1
if ($status) {
    Log "Criando commit..."
    git commit -m $commitMessage 2>&1 | ForEach-Object { Log $_ }
} else {
    Log "Nenhuma alteracao nova para commitar."
}

$hash = git rev-parse --short HEAD 2>&1
Log "HASH: $hash"

Log "Arquivos no commit:"
git ls-tree -r HEAD --name-only 2>&1 | ForEach-Object { Log "  $_" }

Log "Enviando para GitHub..."
$pushOutput = git push -u origin main 2>&1
$pushOutput | ForEach-Object { Log $_ }
Log "EXIT_PUSH: $LASTEXITCODE"

if ($LASTEXITCODE -eq 0) {
    Log "SUCESSO: https://github.com/PedroSilvazDev/trabalho-final-ia-diabetes"
} else {
    Log "FALHA no push. Verifique login do GitHub."
}
