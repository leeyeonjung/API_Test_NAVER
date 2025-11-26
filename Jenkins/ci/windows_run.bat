@echo off

echo === 1. Git Pull ===
cd C:\Automation\API_Test_Naver
git fetch origin main
git reset --hard origin/main

echo === 2. Run Pytest ===
pytest -v --disable-warnings

echo === 3. Copy Latest Report ===
set REPORT_DIR=C:\Automation\API_Test_Naver\Result

for /f "delims=" %%i in ('dir "%REPORT_DIR%\test_report_*.html" /b /o:-d') do (
    set LATEST=%%i
    goto COPY_FILE
)

:COPY_FILE
copy "%REPORT_DIR%\%LATEST%" "windows_%LATEST%"

echo Windows Run Complete
