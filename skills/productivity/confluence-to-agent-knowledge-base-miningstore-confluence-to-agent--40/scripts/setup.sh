#!/bin/bash
# Quick setup script for confluence-kb
# Usage: bash setup.sh

set -e

echo "=== confluence-kb Setup ==="
echo ""

# Check Python version
python3 --version 2>/dev/null || { echo "Python 3 is required. Please install it first."; exit 1; }

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -e .

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Activate the environment:"
echo "  source venv/bin/activate"
echo ""
echo "Quick start:"
echo "  1. Copy configs/miningstore.yaml to ckb-config.yaml"
echo "  2. Set environment variables:"
echo "     export CONFLUENCE_EMAIL='your@email.com'"
echo "     export CONFLUENCE_API_TOKEN='your_token'"
echo "     export ANTHROPIC_API_KEY='your_key'"
echo "  3. Run: ckb ingest"
echo "  4. Run: ckb compile"
echo "  5. Run: ckb query 'What are the mining site protocols?'"
echo ""
