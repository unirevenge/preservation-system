#!/bin/bash
# CADE System Initialization Script for Unix-like systems

echo "[*] Starting CADE System Initialization..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

# Make sure we have the right Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=${PYTHON_VERSION%%.*}
PYTHON_MINOR=${PYTHON_VERSION#*.}

if [ $PYTHON_MAJOR -lt 3 ] || { [ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -lt 8 ]; }; then
    echo "[ERROR] Python 3.8+ is required, but found $PYTHON_VERSION"
    exit 1
fi

# Run the initialization script
echo "[*] Running initialization script..."
python3 init_cade.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Initialization failed. Check the output above for details."
    exit 1
fi

echo "[*] Initialization completed successfully!"
echo

echo "To activate the virtual environment, run:"
echo "   source venv/bin/activate"
echo
echo "To start the CADE system, run:"
echo "   python -m cade_production"
