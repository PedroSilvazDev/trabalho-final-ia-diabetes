@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe scripts\gerar_relatorio.py
) else (
    python scripts\gerar_relatorio.py
)
if exist "docs\relatorio.pdf" (
    echo.
    echo PDF atualizado em: docs\relatorio.pdf
    copy /Y "docs\relatorio.pdf" "%USERPROFILE%\Downloads\relatorio_trabalho_ia.pdf"
    echo Copia salva em: %USERPROFILE%\Downloads\relatorio_trabalho_ia.pdf
) else (
    echo ERRO: PDF nao foi gerado.
)
pause
