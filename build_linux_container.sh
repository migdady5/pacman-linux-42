#!/bin/sh
set -eu
apt-get update
apt-get install -y --no-install-recommends binutils
python3 -m pip install -r requirements.txt
python3 -m pip install vendor/mazegenerator-2.1.0-py3-none-any.whl
python3 package.py
python3 -c 'import shutil; shutil.make_archive("dist/pacman-linux_x86_64", "zip", "dist/linux")'
