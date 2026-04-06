@echo off
echo.
echo === HANGARIN Repository Push Helper ===
echo.
echo [1/3] Adding all files to git...
git add .

echo [2/3] Committing changes...
git commit -m "Update HANGARIN project with latest changes"

echo [3/3] Pushing to GitHub...
echo Note: If this fails, you may need to log in to your account.
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [!] PUSH FAILED (Error 403: Forbidden). 
    echo This means your current account (baterricho) does NOT have permission.
    echo.
    echo [FORCE LOGIN] Attempting to clear cached credentials for github.com...
    cmdkey /delete:LegacyGeneric:target=git:https://github.com
    
    echo.
    echo Retrying push... A login prompt should appear now.
    git push origin main
)

echo.
echo === Push process complete ===
pause
