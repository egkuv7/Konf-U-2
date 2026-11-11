@echo off
echo === Running tests ===
python -m unittest discover -s tests
echo === Running application ===
python -m src.main
