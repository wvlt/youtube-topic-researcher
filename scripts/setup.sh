#!/bin/bash
# Setup script for YouTube Content Researcher Agent

echo "🚀 Setting up YouTube Content Researcher Agent..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p config

# Setup environment file
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (please configure it)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to .env file"
echo "2. Download OAuth2 credentials from Google Cloud Console"
echo "3. Save credentials as config/client_secrets.json"
echo "4. Run: source venv/bin/activate"
echo "5. Run: python -m src.main"
echo ""

