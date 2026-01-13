#!/usr/bin/env python3
"""Build script for creating standalone executables."""

import subprocess
import sys
import shutil
from pathlib import Path


def build_with_pyinstaller():
    """Build standalone executable using PyInstaller."""
    print("Building standalone executable with PyInstaller...")

    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "passgen",
        "--clean",
        "--add-data", "passgen_cli:passgen_cli",
        "passgen_cli/main.py"
    ], check=True)

    print("\n✓ Build complete!")
    print("  Executable: dist/passgen")


def build_with_shiv():
    """Build zipapp using shiv."""
    print("Building zipapp with shiv...")

    subprocess.run([
        sys.executable, "-m", "shiv",
        "-c", "passgen",
        "-o", "dist/passgen.pyz",
        "."
    ], check=True)

    print("\n✓ Build complete!")
    print("  Executable: dist/passgen.pyz")


if __name__ == "__main__":
    Path("dist").mkdir(exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == "shiv":
        build_with_shiv()
    else:
        build_with_pyinstaller()
