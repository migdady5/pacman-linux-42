#!/usr/bin/env sh
set -e

apt-get update -qq
apt-get install -y --no-install-recommends binutils
python -m pip install --no-cache-dir \
    vendor/mazegenerator-2.1.0-py3-none-any.whl \
    pygame-ce pyinstaller
python package.py
python - <<'PY'
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path("dist/linux/pacman")
output = Path("dist/pacman-linux-x86_64.zip")
with ZipFile(output, "w", ZIP_DEFLATED) as archive:
    for path in root.rglob("*"):
        if path.is_file():
            archive.write(path, Path("pacman") / path.relative_to(root))
print(f"Linux release ready: {output}")
PY
