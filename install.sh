#!/bin/bash

# CmdChronicle Installation Script

echo "🚀 Installing CmdChronicle..."

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make the main script executable
echo "🔧 Making script executable..."
chmod +x cmdchronicle.py

# Create symlink for easy access
echo "🔗 Creating symlink..."
if [ ! -L /usr/local/bin/cmdchronicle ]; then
    sudo ln -sf "$(pwd)/cmdchronicle.py" /usr/local/bin/cmdchronicle
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To use CmdChronicle:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the tool: python cmdchronicle.py --help"
echo "3. Or use the symlink: cmdchronicle --help"
echo ""
echo "Make sure you have Ollama installed and running for AI insights!"
echo "Visit https://ollama.ai for installation instructions." 