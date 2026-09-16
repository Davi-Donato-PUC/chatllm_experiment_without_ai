@echo off
setlocal enabledelayedexpansion

:: ── Check for uncommitted changes ───────────────────────────────────────────
for /f "delims=" %%i in ('git status --porcelain 2^>nul') do set HAS_CHANGES=1
if defined HAS_CHANGES (
    echo You have uncommitted or untracked changes in your working tree.
    echo Please commit or stash them before starting Task 2.
    exit /b 1
)

:: ── Confirmation prompt (default: No) ────────────────────────────────────────
set /p REPLY="This will set up Task 2. Proceed? [y/N] "
if /i not "%REPLY%"=="y" if /i not "%REPLY%"=="yes" (
    echo Aborted by user.
    exit /b 0
)

:: ── Remove existing .github folder ──────────────────────────────────────────
if exist ".github" (
    echo Removing existing .github\ directory...
    rmdir /s /q ".github"
)

:: ── Copy Task 2 artifacts ───────────────────────────────────────────────────
if exist "__tools__\task2" (
    echo Copying __tools__\task2\ artifacts to project root...
    xcopy /E /I /Q /Y "__tools__\task2\." .
) else (
    echo ERROR: __tools__\task2\ directory not found!
    exit /b 1
)

:: ── Commit all changes as chore ─────────────────────────────────────────────
git add -A
git commit -m "chore: setup Task 2 artifacts"

:: ── Done ────────────────────────────────────────────────────────────────────
echo.
echo Task 2 is ready!
echo You can now start working on Task 2.

endlocal
