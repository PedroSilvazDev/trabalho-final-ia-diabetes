$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$githubUser = "PedroSilvazDev"
$repoName = "trabalho-final-ia-diabetes"
$remoteUrl = "https://github.com/$githubUser/$repoName.git"
$commitMessage = "Trabalho final IA - predicao de diabetes com KNN e SVM"

function Test-GitRemote {
    param([string]$Name)
    $remotes = & git remote 2>$null
    return ($remotes -contains $Name)
}

Write-Host "=== Upload para GitHub ===" -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git nao encontrado. Instale em https://git-scm.com/download/win"
}

if (-not (Test-Path ".\.git")) {
    Write-Host "Inicializando repositorio git..."
    & git init
    & git branch -M main
}

Write-Host "Adicionando arquivos do projeto..."
& git add .
& git reset .venv 2>$null

$status = & git status --porcelain
if (-not $status) {
    Write-Host "Nada novo para commitar." -ForegroundColor Yellow
} else {
    & git commit -m $commitMessage
    Write-Host "Commit criado com sucesso." -ForegroundColor Green
}

if (-not (Test-GitRemote "origin")) {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        Write-Host "Criando repositorio no GitHub com gh..."
        & gh repo create $repoName --public --source . --remote origin --push
    } else {
        Write-Host "Configurando remote origin..."
        & git remote add origin $remoteUrl
        Write-Host "Enviando para origin/main..."
        & git push -u origin main
    }
} else {
    Write-Host "Enviando para origin/main..."
    & git push -u origin main
}

Write-Host ""
Write-Host "Pronto! Repositorio:" -ForegroundColor Green
Write-Host "https://github.com/$githubUser/$repoName"

if (Test-GitRemote "origin") {
    & git remote get-url origin
}
