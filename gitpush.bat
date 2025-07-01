@echo off
cd /d "%~dp0"

REM ======== CONFIG ========
set REMOTE_URL=https://github.com/atm-2025/gitpush.git
set BRANCH=main

REM ======== INIT IF NEEDED ========
if not exist ".git" (
    echo [INFO] Git not initialized. Initializing...
    git init
    git remote add origin %REMOTE_URL%
    git branch -M %BRANCH%
)

REM ======== CHECK FOR ANY CHANGE ========
git status --porcelain | findstr /r /v "^$" >nul
IF %ERRORLEVEL% NEQ 0 (
    REM ======== STAGE, COMMIT, PUSH ========
    echo [INFO] Adding files...
    git add .

    for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%i

    echo [INFO] Committing...
    git commit -m "Auto commit %timestamp%"

    echo [INFO] Pushing...
    git push -u origin %BRANCH%

    echo [SUCCESS] Upload complete.
    pause
    exit /b
)

echo [INFO] No changes to commit.
pause
