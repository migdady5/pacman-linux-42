"""Build a distributable Pac-Man folder for the current operating system."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST_ROOT = ROOT / "dist" / sys.platform
OUTPUT = DIST_ROOT / "pacman"


def main() -> int:
    """Build the executable and copy its editable resources."""
    if importlib.util.find_spec("mazegenerator") is None:
        print("Install the assigned mazegenerator wheel before packaging.")
        return 1
    if importlib.util.find_spec("PyInstaller") is None:
        print("Install PyInstaller before packaging.")
        return 1

    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--onedir", "--name", "pacman", "--distpath", str(DIST_ROOT),
        "--hidden-import", "mazegenerator",
        str(ROOT / "pac-man.py"),
    ]
    try:
        subprocess.run(command, cwd=ROOT, check=True)
        shutil.copytree(ROOT / "assets", OUTPUT / "assets",
                        dirs_exist_ok=True)
        shutil.copy2(ROOT / "config.json", OUTPUT / "config.json")
        shutil.copy2(ROOT / "README.md", OUTPUT / "README.md")
        if sys.platform == "win32":
            launcher = OUTPUT / "run-pacman.bat"
            launcher.write_text(
                '@echo off\r\ncd /d "%~dp0"\r\npacman.exe config.json\r\n',
                encoding="utf-8",
            )
        else:
            launcher = OUTPUT / "run-pacman.sh"
            launcher.write_text(
                '#!/usr/bin/env bash\nset -e\n'
                'cd "$(dirname "$0")"\nexec ./pacman config.json\n',
                encoding="utf-8",
            )
            launcher.chmod(0o755)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Packaging failed: {error}")
        return 1

    print(f"Package ready: {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
