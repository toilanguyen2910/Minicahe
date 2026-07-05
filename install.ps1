<#
.SYNOPSIS
    Minicahe Installer for Windows
.DESCRIPTION
    Installs Minicahe Mini Token Optimizer
#>

Write-Host ""
Write-Host "Minicahe Installer" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "Error: Python 3.9+ is required." -ForegroundColor Red
    Write-Host "Download from: https://python.org"
    exit 1
}

$ver = & $python.Source --version
Write-Host "Found: $ver" -ForegroundColor Green
Write-Host ""
Write-Host "Installing Minicahe..." -ForegroundColor Yellow

& $python.Source -m pip install --upgrade pip -q
& $python.Source -m pip install minicahe -q 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing from source..."
    & $python.Source -m pip install -e .
}

Write-Host ""
Write-Host "Minicahe installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Try: minicahe compress --help" -ForegroundColor Cyan
