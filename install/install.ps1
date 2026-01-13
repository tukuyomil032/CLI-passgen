<#
Simple installer for Windows (PowerShell).
Usage (install latest main):
  iex (iwr -useb https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.ps1)
Install a specific release tag (example v1.0.0):
  $env:VERSION = 'v1.0.0'; iex (iwr -useb https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.ps1)
#>

Set-StrictMode -Version Latest

Write-Host "passgen-cli installer"
$py = Get-Command python3 -ErrorAction SilentlyContinue; if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py) {
  Write-Error "Python is not installed. Install Python 3 and re-run this script."
  exit 1
}

Write-Host "Using Python:" (& $py.Path --version)

# Determine source tarball: use $env:VERSION (tag) or fallback to main
if ($env:VERSION) {
  $tarUrl = "https://github.com/tukuyomil032/CLI-passgen/archive/refs/tags/$($env:VERSION).tar.gz"
} else {
  $tarUrl = "https://github.com/tukuyomil032/CLI-passgen/archive/refs/heads/main.tar.gz"
}

Write-Host "Installing or upgrading passgen-cli from: $tarUrl"
& $py.Path -m pip install --upgrade --user $tarUrl

if ($LASTEXITCODE -ne 0) {
  Write-Error "pip install failed. Ensure pip is available or run with administrative privileges if necessary."
  exit $LASTEXITCODE
}

Write-Host "passgen-cli installed successfully."

Write-Host "If the 'passgen' command is not found, ensure your Python user base Scripts folder is on PATH."
Write-Host "Typical locations:"
Write-Host "  $([System.Environment]::GetFolderPath('UserProfile'))\AppData\Roaming\Python\PythonXX\Scripts"

Write-Host "You can now run: passgen -h"
