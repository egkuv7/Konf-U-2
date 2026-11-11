@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Running tests ===
py -u -m unittest discover -s tests
echo === Running application ===
py -u -m src.main
pause
