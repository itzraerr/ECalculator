# ECalculator (Flet + SymPy)

ECalculator is a desktop/web calculator built with Flet and SymPy. It supports basic arithmetic, scientific functions, and complex numbers (use `i` or `j` for the imaginary unit).

Requirements

- Python 3.8+
- See `requirements.txt` for dependencies.

Quick start (development)

1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Run the app (browser mode by default if desktop runtime is unavailable)

```bash
python main.py
```

Desktop runtime (preferred)

For a native desktop window, Flet's desktop runtime uses mpv/libmpv. On Debian/Ubuntu install mpv:

```bash
sudo add-apt-repository universe
sudo apt update
sudo apt install mpv
```

Then run the provided desktop launcher:

```bash
source venv/bin/activate
./run_desktop.sh
```

If `libmpv` is missing the app will automatically fall back to opening in your web browser.

Browser-only run

```bash
source venv/bin/activate
./run_browser.sh
```

Docker (contains mpv)

```bash
docker build -t ecalculator .
docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ecalculator
```

AppImage (minimal)

Build a minimal AppImage (requires `appimagetool` and mpv available on target):

```bash
chmod +x build_appimage.sh
./build_appimage.sh
```

Full self-contained AppImage

Build a fully self-contained AppImage (bundles Python, libs, and mpv). This is heavier but requires no extra runtime on the target machine:

```bash
chmod +x build_appimage_full.sh
./build_appimage_full.sh
```

Notes and caveats

- The full AppImage is produced with PyInstaller and attempts to include `libmpv` and its dependencies. Building on an older, widely-compatible distro (for example Ubuntu LTS) tends to produce more portable AppImages.
- The produced AppImage is large because it includes Python and libraries.
- The AppImage still needs access to X/Wayland on the host (running it on a headless machine requires X forwarding or a virtual framebuffer).

Alternative: Use Flet's pack tooling / environment

Flet offers packaging and environment tools that may simplify distributing a web or desktop app. If you prefer a Flet-provided workflow, consider using `flet pack` or `flet cloud` (check Flet docs for current commands and options). The main alternatives:

- `flet pack` (if available in your Flet version) can package apps for desktop platforms and may bundle the runtime.
- Use Docker to create a controlled runtime and distribute the image.

Troubleshooting

- If you see an error about `libmpv.so.1` when launching, install mpv as shown above or run the browser mode.
- If PyInstaller fails during full AppImage build, ensure development tools (gcc, make) and a working Python dev environment are available on the build host.

Questions or next steps

- Want me to replace the placeholder icon used in the AppImage with a designed icon? I can add SVG/PNG assets.
- Want a CI script to build and upload the AppImage automatically? I can add a GitHub Actions workflow.

Desktop runtime (preferred)

To run the native desktop runtime (gives a native window), install mpv/libmpv on your system first (Ubuntu/Debian):

```bash
sudo add-apt-repository universe
sudo apt update
sudo apt install mpv
```

Then run:

```bash
source venv/bin/activate
./run_desktop.sh
```

If libmpv is missing the app will automatically fall back to opening in your web browser.

Browser-only run

```bash
source venv/bin/activate
./run_browser.sh
```

Docker (contains mpv)

```bash
docker build -t ecalculator .
docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ecalculator
```

AppImage (Linux desktop bundle)

This repository includes `build_appimage.sh` which creates a minimal AppDir and calls `appimagetool` to produce an AppImage. You'll need `appimagetool` installed and mpv available on the target system.

```bash
chmod +x build_appimage.sh
./build_appimage.sh
```

If `appimagetool` is not available, download it from https://appimage.org/ and place it on your PATH.

Full self-contained AppImage

If you want a fully self-contained AppImage (bundles Python binary, dependencies and libmpv), use `build_appimage_full.sh`.

```bash
chmod +x build_appimage_full.sh
./build_appimage_full.sh
```

Notes:
- This script uses PyInstaller to build a one-file binary and attempts to copy libmpv and its dependencies into the AppDir. It downloads `appimagetool` if missing.
- Building on the target distribution (or a compatible one) improves compatibility. The script is intended for x86_64 Linux.
- The produced AppImage will be larger because it includes Python and libraries.