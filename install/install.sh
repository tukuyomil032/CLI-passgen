#!/usr/bin/env sh
set -eu

# Simple installer for POSIX systems (Linux, macOS without Homebrew)
# Usage (install latest main):
#   curl -sSL https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.sh | sh
# Install a specific release tag (example v1.0.0):
#   curl -sSL https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.sh | VERSION=v1.0.0 sh

echo "passgen-cli installer"

# Find a python executable
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Error: Python is not installed. Install Python 3 and re-run this script." >&2
  exit 1
fi

echo "Using Python: $($PY --version 2>&1)"

# Determine source tarball: use VERSION env var (tag) or fallback to main branch
if [ -n "${VERSION:-}" ]; then
  TAR_URL="https://github.com/tukuyomil032/CLI-passgen/archive/refs/tags/${VERSION}.tar.gz"
else
  TAR_URL="https://github.com/tukuyomil032/CLI-passgen/archive/refs/heads/main.tar.gz"
fi

echo "Installing or upgrading passgen-cli from: $TAR_URL"
if $PY -m pip install --upgrade --user "$TAR_URL"; then
  echo "passgen-cli installed successfully."
else
  echo "pip install failed. You may need to run with sudo or ensure pip is available." >&2
  exit 1
fi

# Advise about PATH
USER_BASE=$($PY -c 'import site,sys; print(site.USER_BASE)')
BIN_DIR="$USER_BASE/bin"

if [ -d "$BIN_DIR" ]; then
  echo "Installed to: $BIN_DIR"
  case "$(uname -s)" in
    Linux|Darwin)
      echo "Make sure $BIN_DIR is on your PATH. Example:"
      echo "  export PATH=\"$BIN_DIR:\$PATH\"";
      ;;
    *)
      ;;
  esac
fi

echo "You can now run: passgen -h"

exit 0
