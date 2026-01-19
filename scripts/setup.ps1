# passgen-cli Windows Automatic Setup (PowerShell)
# Supported: Windows 10/11

param(
    [switch]$Help
)

if ($Help) {
    Write-Host "passgen-cli Windows Setup Script"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\setup.ps1"
    Write-Host ""
    exit 0
}

# Color definitions
$Colors = @{
    Red    = "Red"
    Green  = "Green"
    Yellow = "Yellow"
    Cyan   = "Cyan"
    Blue   = "Blue"
}

# Display banner
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔐 passgen-cli Installation Starting" -ForegroundColor Cyan
Write-Host "System: Windows" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
$NodeInstalled = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
if (-not $NodeInstalled) {
    Write-Host "❌ Error: Node.js is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please visit https://nodejs.org/ to download and install Node.js (v18 or higher)"
    Write-Host ""
    exit 1
}

# Check Node.js version
$NodeVersion = [int]((node -v) -replace "v", "" -split "\.")[0]
if ($NodeVersion -lt 18) {
    Write-Host "❌ Error: Node.js 18 or higher is required (current: v$NodeVersion)" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Node.js verified" -ForegroundColor Green
Write-Host ""

# Check/Install pnpm
$PnpmInstalled = $null -ne (Get-Command pnpm -ErrorAction SilentlyContinue)
if (-not $PnpmInstalled) {
    Write-Host "📦 Installing pnpm..." -ForegroundColor Yellow
    npm install -g pnpm
    Write-Host ""
}

Write-Host "✓ pnpm verified" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pnpm install

Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Build TypeScript
Write-Host "🔨 Building TypeScript..." -ForegroundColor Yellow
pnpm build

Write-Host "✓ Build complete" -ForegroundColor Green
Write-Host ""

# Register global command
Write-Host "🌍 Registering global command..." -ForegroundColor Yellow
pnpm install -g .

Write-Host "✓ Global registration complete" -ForegroundColor Green
Write-Host ""

# Success message
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Installation Successful!" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 Usage:" -ForegroundColor Green
Write-Host ""
Write-Host "  💻 Interactive mode (recommended):" -ForegroundColor Cyan
Write-Host "     > passgen"
Write-Host ""
Write-Host "  🔐 Generate 16-character password:" -ForegroundColor Cyan
Write-Host "     > passgen -l 16"
Write-Host ""
Write-Host "  📋 Generate multiple passwords (5x 32 chars, all character types):" -ForegroundColor Cyan
Write-Host "     > passgen -l 32 -n -a -A -s -c 5"
Write-Host ""
Write-Host "  🎲 Generate with random character types:" -ForegroundColor Cyan
Write-Host "     > passgen -l 24 -r"
Write-Host ""
Write-Host "  ❓ Show help:" -ForegroundColor Cyan
Write-Host "     > passgen --help"
Write-Host ""
Write-Host "✨ Enjoy using passgen!" -ForegroundColor Green
Write-Host ""
