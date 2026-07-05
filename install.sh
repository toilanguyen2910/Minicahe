#!/bin/bash
# Minicahe installer for Linux/macOS

set -e

echo ""
echo "Minicahe Installer"
echo "=================="
echo ""

# Check for Python
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo "Error: Python 3 is required"
    exit 1
fi

echo "Found: $($PYTHON --version)"

echo "Installing Minicahe..."
$PYTHON -m pip install --upgrade pip -q
$PYTHON -m pip install minicahe -q 2>/dev/null || $PYTHON -m pip install -e .

echo ""
echo "Minicahe installed successfully!"
echo ""
echo "Try: minicahe compress --help"
