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
    echo [!] PUSH FAILED. This usually means you need to log in.
    echo.
    echo Attempting to trigger a login prompt...
    echo (If you have GitHub CLI installed, running 'gh auth login' may help)
    git remote set-url origin https://github.com/202180176-ship-it/HANGARIN.git
    git push origin main
)

echo.
echo === Push process complete ===
pause
