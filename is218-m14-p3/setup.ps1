# Setup script for IS218 Module 14 Project (Windows PowerShell)
# This script helps set up the development environment

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "IS218 Module 14 - Setup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.11 or higher." -ForegroundColor Red
    exit 1
}

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker is not installed. Docker is recommended for this project." -ForegroundColor Yellow
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
}

# Create virtual environment
Write-Host ""
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Install Playwright
Write-Host ""
Write-Host "Installing Playwright browsers..." -ForegroundColor Yellow
playwright install --with-deps chromium

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host ""
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please update it with your database credentials." -ForegroundColor Green
} else {
    Write-Host "✅ .env file already exists." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update .env file with your database credentials"
Write-Host "2. Start PostgreSQL database"
Write-Host "3. Run: uvicorn app.main:app --reload"
Write-Host "4. Open browser: http://localhost:8000"
Write-Host ""
Write-Host "Or use Docker Compose:" -ForegroundColor Yellow
Write-Host "  docker-compose up --build"
Write-Host ""
Write-Host "Run tests:" -ForegroundColor Yellow
Write-Host "  pytest -v"
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
