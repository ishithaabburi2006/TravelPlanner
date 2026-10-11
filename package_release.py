#!/usr/bin/env python3
"""Create a source release ZIP without local secrets or generated files."""

from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "TravelPlanner-release-clean.zip"
EXCLUDED_DIRS = {
    ".git", ".idea", ".vscode", "__MACOSX", "node_modules", "target", "dist",
    ".pytest_cache", "__pycache__",
}
EXCLUDED_SUFFIXES = {".log", ".tmp", ".iml", ".pyc"}


def include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name == ".DS_Store" or path.suffix in EXCLUDED_SUFFIXES or path.suffix == ".zip":
        return False
    # Keep the safe templates; never package an actual environment file.
    if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
        return False
    return path.is_file()


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
count = 0
with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(ROOT.rglob("*")):
        if include(path) and path.resolve() != OUTPUT and path.resolve() != temporary:
            archive.write(path, path.relative_to(ROOT).as_posix())
            count += 1
temporary.replace(OUTPUT)
print(f"Created {OUTPUT} with {count} files")
