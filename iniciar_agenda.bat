@echo off
title Agenda Oficial - Crônica Eclesiástica (Porta 8181)
echo ========================================================
echo         AGENDA OFICIAL ECLESIASTICA (Porta 8181)
echo ========================================================
echo.
echo Iniciando servidor local na porta 8181...
echo Acessando http://localhost:8181 no navegador...
echo.

start http://localhost:8181
python -m http.server 8181 --directory "%~dp0"

pause
