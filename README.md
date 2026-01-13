# CLI-passgen

Lightweight password generation CLI tool

<img width="451" height="147" alt="SCR-20260114-bgrj" src="https://github.com/user-attachments/assets/a9063b58-f964-4733-917d-1bbe6e4d9cff" />




## Features

- 🔐 Password generation using the `secrets` module
- 🎨 Beautifully decorated CLI output
- 🎯 Customizable character types (numbers, lowercase, uppercase, special characters)
- 🎲 Option to select character types randomly
- 📦 Easy to install and use

CLI-passgen can be installed in several ways.

## Technology Stacks
 - Homebrew (Formula distribution)
 - Bash / Shell scripts (installers)
 - PowerShell (Windows installer)

## Languages
- Python 3.11
- Ruby
- Shell

### macOS / Linux (install via curl)

Download the binary for your platform from the latest release and install it to `/usr/local/bin` (or `~/.local/bin` if you do not have write permission).

```bash
curl -sSL https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.sh | sh
# Example to specify a particular release:
VERSION=${version} curl -sSL https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.sh | sh
```

### Windows (PowerShell)

Running the installer in PowerShell places `passgen.exe` into `%USERPROFILE%\bin`.

```powershell
iex (iwr -useb https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.ps1)
# Example to specify a particular release:
$env:VERSION = 'v1.0.0'; iex (iwr -useb https://raw.githubusercontent.com/tukuyomil032/CLI-passgen/main/install/install.ps1)
```

### macOS (Homebrew)

In addition to curl, Homebrew can be used.

```bash
brew tap tukuyomil032/passgen
brew install tukuyomil032/passgen/passgen
```

```bash
Alternatively, you can install directly from a raw Formula URL temporarily:
brew install https://raw.githubusercontent.com/tukuyomil032/homebrew-passgen/main/Formula/passgen.rb
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
