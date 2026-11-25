@echo off
title Agenda Oficial PC - Crônica Eclesiástica & Patrimônio (Desktop)
chcp 65001 > nul
echo.
echo ========================================================
echo    AGENDA OFICIAL PC - CRÔNICA ECLESIÁSTICA & PATRIMÔNIO
echo    Versão 1.1.5 • Desktop Widescreen Edition
echo ========================================================
echo.
echo Iniciando servidor local na porta 8181...
echo Acessando: http://localhost:8181/agenda_pc/index.html
echo.
start http://localhost:8181/agenda_pc/index.html
cd /d "%~dp0\.."
python -m http.server 8181
pause
