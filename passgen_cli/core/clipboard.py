"""Clipboard utilities for copying passwords."""

import subprocess
import sys
import platform


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard. Returns True on success."""
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            subprocess.run(
                ["pbcopy"],
                input=text.encode("utf-8"),
                check=True
            )
            return True
        elif system == "Linux":
            # Try xclip first, then xsel
            try:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"),
                    check=True
                )
                return True
            except FileNotFoundError:
                try:
                    subprocess.run(
                        ["xsel", "--clipboard", "--input"],
                        input=text.encode("utf-8"),
                        check=True
                    )
                    return True
                except FileNotFoundError:
                    return False
        elif system == "Windows":
            subprocess.run(
                ["clip"],
                input=text.encode("utf-16"),
                check=True
            )
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False


def is_clipboard_available() -> bool:
    """Check if clipboard functionality is available."""
    system = platform.system()

    try:
        if system == "Darwin":
            subprocess.run(["which", "pbcopy"], capture_output=True, check=True)
            return True
        elif system == "Linux":
            try:
                subprocess.run(["which", "xclip"], capture_output=True, check=True)
                return True
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(["which", "xsel"], capture_output=True, check=True)
                    return True
                except subprocess.CalledProcessError:
                    return False
        elif system == "Windows":
            return True  # clip is always available on Windows
        else:
            return False
    except subprocess.CalledProcessError:
        return False
