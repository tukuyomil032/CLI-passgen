@echo off
REM passgen-cli Windows Automatic Setup (Batch)
REM Supported: Windows CMD

setlocal enabledelayedexpansion

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🔐 passgen-cli Installation Starting
echo System: Windows (CMD)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Check Node.js
where node >nul 2>nul
if errorlevel 1 (
    echo ❌ Error: Node.js is not installed
    echo.
    echo Please visit https://nodejs.org/ to download and install Node.js (v18 or higher)
    echo.
    exit /b 1
)

echo ✓ Node.js verified
echo.

REM Check/Install pnpm
where pnpm >nul 2>nul
if errorlevel 1 (
    echo 📦 Installing pnpm...
    call npm install -g pnpm
    echo.
)

echo ✓ pnpm verified
echo.

REM Install dependencies
echo 📦 Installing dependencies...
call pnpm install

echo ✓ Dependencies installed
echo.

REM Build TypeScript
echo 🔨 Building TypeScript...
call pnpm build

echo ✓ Build complete
echo.

REM Register global command
echo 🌍 Registering global command...
call pnpm install -g .

echo ✓ Global registration complete
echo.

REM Success message
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ Installation Successful!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 📝 Usage:
echo.
echo   💻 Interactive mode (recommended):
echo      ^> passgen
echo.
echo   🔐 Generate 16-character password:
echo      ^> passgen -l 16
echo.
echo   📋 Generate multiple passwords (5x 32 chars, all character types):
echo      ^> passgen -l 32 -n -a -A -s -c 5
echo.
echo   🎲 Generate with random character types:
echo      ^> passgen -l 24 -r
echo.
echo   ❓ Show help:
echo      ^> passgen --help
echo.
echo ✨ Enjoy using passgen!
echo.

endlocal
