#!/bin/bash
set -euo pipefail

# This script prepares a simple AppDir and uses appimagetool if available.
# It assumes you have a working Python venv and mpv installed locally.

APP=ECalculator
OUT=${APP}.AppImage

APPIMAGETOOL=""
if ! command -v appimagetool >/dev/null 2>&1; then
  echo "appimagetool not found on PATH. Downloading a temporary copy..."
  TOOL="/tmp/appimagetool-x86_64.AppImage"
  if [ ! -f "$TOOL" ]; then
    wget -q -O "$TOOL" "https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage" || true
  fi
  if [ -f "$TOOL" ]; then
    chmod +x "$TOOL"
    APPIMAGETOOL="$TOOL"
  else
    echo "Failed to download appimagetool; please install it manually: https://appimage.org/" >&2
    exit 1
  fi
else
  APPIMAGETOOL=$(command -v appimagetool)
fi

mkdir -p AppDir/usr/bin/${APP}
# Copy only necessary files into the AppDir app folder
cp -r ./* AppDir/usr/bin/${APP}/

# Ensure the bundled run script is executable
if [ -f AppDir/usr/bin/${APP}/run_desktop.sh ]; then
  chmod +x AppDir/usr/bin/${APP}/run_desktop.sh
fi

# AppRun wrapper to launch the bundled run_desktop.sh inside the AppImage
cat > AppDir/AppRun <<'AR'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
exec "$HERE/usr/bin/${APP}/run_desktop.sh" "$@"
AR
chmod +x AppDir/AppRun

cat > AppDir/${APP}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=${APP}
Exec=${APP}
Icon=calculator
Categories=Utility;
EOF

"${APPIMAGETOOL}" AppDir ${OUT}
echo "Built ${OUT}"
