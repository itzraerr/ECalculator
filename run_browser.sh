#!/bin/bash
set -euo pipefail

# Activate venv if present
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

python3 -c "import flet; flet.app(target=__import__('simplewebcal').main, view=flet.WEB_BROWSER)"
