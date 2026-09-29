"""Create a Linux source release containing the assigned maze wheel."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WHEEL_NAME = "mazegenerator-2.1.0-py3-none-any.whl"


def main() -> int:
    """Bundle runnable source, assets, and the unmodified assigned wheel."""
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel_zip", type=Path, nargs="?")
    arguments = parser.parse_args()
    if arguments.wheel_zip is None:
        wheel = (ROOT / "vendor" / WHEEL_NAME).read_bytes()
    else:
        try:
            with zipfile.ZipFile(arguments.wheel_zip) as source:
                wheel = source.read(WHEEL_NAME)
        except (OSError, KeyError, zipfile.BadZipFile) as error:
            parser.error(f"Cannot read assigned maze wheel: {error}")

    output = ROOT / "dist" / "pacman-linux-source.zip"
    output.parent.mkdir(exist_ok=True)
    files = [ROOT / name for name in (
        "pac-man.py", "config.json", "README.md", "install-linux.sh",
    )]
    files.extend((ROOT / "src").glob("*.py"))
    files.extend(path for path in (ROOT / "assets").rglob("*")
                 if path.is_file())
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, Path("pacman") / path.relative_to(ROOT))
        archive.writestr(f"pacman/vendor/{WHEEL_NAME}", wheel)
    print(f"Linux source package ready: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
