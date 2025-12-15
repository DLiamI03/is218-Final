#!/bin/bash

# Setup script for IS218 Module 14 Project
# This script helps set up the development environment

echo "========================================="
echo "IS218 Module 14 - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python is installed: $(python3 --version)"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Docker is recommended for this project."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
else
    echo "✅ Docker is installed: $(docker --version)"
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright
echo ""
echo "Installing Playwright browsers..."
playwright install --with-deps chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your database credentials."
else
    echo "✅ .env file already exists."
fi

echo ""
echo "========================================="
echo "Setup Complete! 🎉"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Update .env file with your database credentials"
echo "2. Start PostgreSQL database"
echo "3. Run: uvicorn app.main:app --reload"
echo "4. Open browser: http://localhost:8000"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up --build"
echo ""
echo "Run tests:"
echo "  pytest -v"
echo ""
echo "========================================="
