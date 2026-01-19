# passgen-cli

🔐 A lightweight and simple password generator CLI tool

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Node.js](https://img.shields.io/badge/node.js-18%2B-brightgreen)

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+**
- **npm**, **pnpm**, **yarn**, or **bun**

### Installation

#### For End Users

##### Using npm
```bash
npm install -g @tukuyomil032/passgen
passgen
```

##### Using pnpm
```bash
pnpm add -g @tukuyomil032/passgen
passgen
```

##### Using yarn
```bash
yarn global add @tukuyomil032/passgen
passgen
```

##### Using bun
```bash
bun add -g @tukuyomil032/passgen
passgen
```

#### For Developers (Local Development)

##### macOS / Linux
```bash
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
bash scripts/setup.sh
```

##### Windows (PowerShell)
```powershell
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
.\scripts\setup.ps1
```

##### Windows (CMD)
```cmd
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
scripts\setup.bat
```

## 📖 Usage

### Interactive Mode (Recommended)
```bash
passgen
```
Select character types, password length, and copy destination interactively.

### Command-line Options
```bash
# Generate a 16-character password
passgen -l 16

# Generate 5 passwords, 32 characters each, with all character types
passgen -l 32 -n -a -A -s -c 5

# Generate with random character types
passgen -l 24 -r

# Display help
passgen --help
```

### Available Options
- `-l, --length` - Password length (default: 16)
- `-c, --count` - Number of passwords to generate (default: 1)
- `-n` - Include numbers (0-9)
- `-a` - Include lowercase letters (a-z)
- `-A` - Include uppercase letters (A-Z)
- `-s` - Include special characters
- `-r` - Randomly select character types
- `-q, --quiet` - Minimize output
- `--copy / --no-copy` - Control clipboard copy behavior

## 🔐 Security

- Cryptographically secure random generation using `crypto.randomInt()`
- All inputs are validated
- Full type safety with TypeScript

## ✨ Features

- 🔐 Cryptographically secure password generation
- 🎨 Beautiful ANSI color support
- 💬 Interactive mode
- 📋 Automatic clipboard copy
- ⚡ Cross-platform support (macOS/Linux/Windows)
- 🎯 Multiple CLI options

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| TypeScript | 5.3+ | Language |
| Node.js | 18+ | Runtime |
| pnpm | Latest | Package manager |
| yargs | 17.7.2 | CLI argument parsing |
| inquirer | 9.2.11 | Interactive prompts |
| ora | 8.0.1 | Spinner display |
| clipboardy | 4.0.0 | Clipboard operations |

## 📦 Development

### Local Development Setup
```bash
pnpm install
pnpm dev          # Run with ts-node
pnpm build        # Compile TypeScript
pnpm link --global # Link globally for development
```

## 📁 Project Structure

```
CLI-passgen/
├── src/                    # TypeScript source code
│   ├── main.ts             # CLI entry point
│   ├── core/               # Core functionality
│   │   ├── generator.ts    # Password generation logic
│   │   ├── clipboard.ts    # Clipboard operations
│   │   └── constants.ts    # Constants and character sets
│   └── ui/                 # UI components
│       ├── display.ts      # Display rendering
│       └── interactive.ts  # Interactive mode
├── scripts/                # Setup scripts (for developers)
│   ├── setup.sh            # macOS/Linux setup
│   ├── setup.ps1           # Windows PowerShell setup
│   └── setup.bat           # Windows CMD setup
├── dist/                   # Compiled JavaScript (generated)
├── package.json            # NPM configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

## 📄 License

MIT

---
