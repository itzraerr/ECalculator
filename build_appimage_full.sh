#!/usr/bin/env bash
set -euo pipefail

# build_appimage_full.sh
# Creates a fully self-contained AppImage for ECalculator.
# Steps:
# 1) Creates a temporary venv and installs requirements + pyinstaller
# 2) Builds a onefile binary via pyinstaller
# 3) Copies libmpv and its shared-library dependencies into AppDir/usr/lib
# 4) Creates AppRun wrapper and .desktop file
# 5) Downloads appimagetool if missing and builds the AppImage
#
# IMPORTANT: This script runs on x86_64 Linux and assumes you have build tools
# and network access. The produced AppImage should run on similar Linux systems
# without additional installation.

APPNAME=ECalculator
BUILD_DIR=build_appimage_full
VENV_DIR="$BUILD_DIR/venv"
DIST_DIR=dist
APPDIR=AppDir
PYINSTALLER_NAME=${APPNAME}

echo "Starting full AppImage build for ${APPNAME}"

rm -rf "$BUILD_DIR" "$APPDIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR"

echo "Creating venv and installing build deps..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller pillow

echo "Running PyInstaller (onefile)..."
pyinstaller --noconfirm --clean --onefile --name "$PYINSTALLER_NAME" simplewebcal.py

if [ ! -f "dist/${PYINSTALLER_NAME}" ]; then
  echo "PyInstaller did not produce expected binary at dist/${PYINSTALLER_NAME}" >&2
  exit 1
fi

mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/lib" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

echo "Copying application binary..."
cp "dist/${PYINSTALLER_NAME}" "$APPDIR/usr/bin/${APPNAME}"
chmod +x "$APPDIR/usr/bin/${APPNAME}"

echo "Locating libmpv..."
LIBMPV_PATH=""
if command -v ldconfig >/dev/null 2>&1; then
  LIBMPV_PATH=$(ldconfig -p | awk '/libmpv.so.1/ {print $NF; exit}') || true
fi
if [ -z "$LIBMPV_PATH" ]; then
  # try locate
  LIBMPV_PATH=$(which mpv 2>/dev/null || true)
fi

if [ -n "$LIBMPV_PATH" ] && [ -f "$LIBMPV_PATH" ]; then
  echo "Found libmpv binary at $LIBMPV_PATH"
else
  # maybe ldconfig returned the library path, check libs directly
  LIBMPV_PATH=$(ldconfig -p | awk '/libmpv.so/ {print $NF; exit}' || true)
fi

if [ -n "$LIBMPV_PATH" ]; then
  echo "Copying libmpv and dependencies into AppDir..."
  # if path points to mpv executable, try to find the shared library via ldd
  if file "$LIBMPV_PATH" | grep -q ELF; then
    # if binary is executable mpv, try to get its linked libmpv
    LIBS_TO_COPY=$(ldd "$LIBMPV_PATH" | awk '/libmpv/ {print $(NF-1)}' || true)
  else
    LIBS_TO_COPY="$LIBMPV_PATH"
  fi
  # ensure we include at least the library file
  for lib in $LIBS_TO_COPY; do
    if [ -f "$lib" ]; then
      cp -v "$lib" "$APPDIR/usr/lib/" || true
      # copy dependencies of the lib
      for dep in $(ldd "$lib" | awk '/=>/ {print $(NF-1)}' | sort -u); do
        if [ -f "$dep" ]; then
          cp -v "$dep" "$APPDIR/usr/lib/" || true
        fi
      done
    fi
  done
else
  echo "Warning: libmpv not found on build host; the produced AppImage may fail on systems without libmpv." >&2
fi

echo "Writing AppRun wrapper..."
cat > "$APPDIR/AppRun" <<'APP_RUN'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
exec "$HERE/usr/bin/ECalculator" "$@"
APP_RUN
chmod +x "$APPDIR/AppRun"

echo "Writing .desktop file..."
cat > "$APPDIR/${APPNAME}.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=${APPNAME}
Exec=ECalculator
Icon=ecalc
Categories=Utility;
EOF

echo "Creating a small placeholder icon (PNG)..."
ICON_PNG="$APPDIR/usr/share/icons/hicolor/256x256/apps/ecalc.png"
mkdir -p "$(dirname "$ICON_PNG")"
python3 - "$ICON_PNG" <<'PY'
import sys
from PIL import Image, ImageDraw
path = sys.argv[1]
img = Image.new('RGBA', (256,256), (0,0,0,0))
draw = ImageDraw.Draw(img)
draw.ellipse((10,10,246,246), fill=(13,37,86,255))
# simple centered 'E'
draw.text((96,84), 'E', fill=(233,35,15,255))
img.save(path)
PY

echo "Ensuring appimagetool is available..."
if ! command -v appimagetool >/dev/null 2>&1; then
  echo "Downloading appimagetool.AppImage to build dir..."
  # pick official AppImage release
  TOOL=/tmp/appimagetool-x86_64.AppImage
  wget -q -O "$TOOL" "https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage" || true
  chmod +x "$TOOL" || true
  APPIMAGETOOL="$TOOL"
else
  APPIMAGETOOL=$(command -v appimagetool)
fi

echo "Building AppImage (this may take a while)..."
"$APPIMAGETOOL" "$APPDIR" || {
  echo "appimagetool failed" >&2
  exit 1
}

echo "AppImage build complete. See *.AppImage in current dir."
