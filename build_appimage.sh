#!/bin/bash
set -euo pipefail

# This script prepares a simple AppDir and uses appimagetool if available.
# It assumes you have a working Python venv and mpv installed locally.

APP=ECalculator
OUT=${APP}.AppImage

if ! command -v appimagetool >/dev/null 2>&1; then
  echo "appimagetool not found. Install it from https://appimage.org/ or your distro." >&2
  exit 1
fi

mkdir -p AppDir/usr/bin
cp -r . AppDir/usr/bin/${APP}
cp run_desktop.sh AppDir/usr/bin/${APP}/run_desktop.sh

cat > AppDir/${APP}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=${APP}
Exec=/usr/bin/env bash -c "cd \"$(pwd)\" && ./run_desktop.sh"
Icon=calculator
Categories=Utility;
EOF

appimagetool AppDir ${OUT}
echo "Built ${OUT}"
