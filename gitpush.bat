@echo off
cd /d "%~dp0"

REM ========= CONFIG ==========
set REMOTE_URL=https://github.com/atm-2025/gitpush
set BRANCH=main

REM ========= INIT REPO ==========
if not exist ".git" (
    echo [INFO] Git not initialized. Initializing...
    git init
    git remote add origin %REMOTE_URL%
    git branch -M %BRANCH%
)

REM ========= ALWAYS TRY ADD & COMMIT ==========
echo [INFO] Adding all files...
git add .

for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%i

echo [INFO] Committing...
git commit -m "Auto commit %timestamp%" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Nothing to commit.
    pause
    exit /b
)

echo [INFO] Pushing to GitHub...
git push -u origin %BRANCH%

echo [SUCCESS] Changes pushed.
pause
