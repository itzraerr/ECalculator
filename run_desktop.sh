#!/bin/bash
set -euo pipefail

# Activate venv if present
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

python3 main.py
