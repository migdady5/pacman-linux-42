#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/python3 -m pip install pygame-ce vendor/mazegenerator-2.1.0-py3-none-any.whl

printf '%s\n' 'Installed. Run: source .venv/bin/activate && python3 pac-man.py config.json'
