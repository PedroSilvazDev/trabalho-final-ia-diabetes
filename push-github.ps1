$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$githubUser = "PedroSilvazDev"
$repoName = "trabalho-final-ia-diabetes"
$remoteUrl = "https://github.com/$githubUser/$repoName.git"
$commitMessage = "Trabalho final IA - predicao de diabetes com KNN e SVM"

Write-Host "=== Upload para GitHub ===" -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git nao encontrado. Instale em https://git-scm.com/download/win"
}

if (-not (Test-Path ".\.git")) {
    Write-Host "Inicializando repositorio git..."
    git init
    git branch -M main
}

Write-Host "Adicionando arquivos do projeto..."
git add .
git reset .venv 2>$null

$status = git status --porcelain
if (-not $status) {
    Write-Host "Nada novo para commitar." -ForegroundColor Yellow
} else {
    git commit -m $commitMessage
    Write-Host "Commit criado com sucesso." -ForegroundColor Green
}

if (-not (git remote get-url origin 2>$null)) {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        Write-Host "Criando repositorio no GitHub com gh..."
        gh repo create $repoName --public --source . --remote origin --push
    } else {
        Write-Host ""
        Write-Host "Remote origin nao configurado e gh CLI nao encontrado." -ForegroundColor Yellow
        Write-Host "1. Crie um repositorio vazio em: https://github.com/new"
        Write-Host "   Nome: $repoName"
        Write-Host "2. Depois rode:"
        Write-Host "   git remote add origin $remoteUrl"
        Write-Host "   git push -u origin main"
        exit 0
    }
} else {
    Write-Host "Enviando para origin/main..."
    git push -u origin main
}

Write-Host ""
Write-Host "Pronto! Repositório:" -ForegroundColor Green
Write-Host "https://github.com/$githubUser/$repoName"
git remote get-url origin
