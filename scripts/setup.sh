#!/usr/bin/env bash
# passgen-cli Cross-platform Automatic Setup
# Supported: macOS, Linux, Windows (Git Bash / WSL / PowerShell)

set -e

# Color definitions (works on all systems)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Detect OS
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
  Darwin)
    OS="macOS"
    ;;
  Linux)
    OS="Linux"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    OS="Windows"
    ;;
  *)
    OS="Unknown"
    ;;
esac

# Display banner
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔐 passgen-cli Installation Starting${NC}"
echo -e "${GREEN}System: ${OS}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
  echo -e "${RED}❌ Error: Node.js is not installed${NC}"
  echo ""
  echo "Please visit https://nodejs.org/ to download and install Node.js (v18 or higher)"
  echo ""
  exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo -e "${RED}❌ Error: Node.js 18 or higher is required (current: v$NODE_VERSION)${NC}"
  exit 1
fi

echo -e "${GREEN}✓${NC} Node.js verified"
echo ""

# Check/Install pnpm
if ! command -v pnpm &> /dev/null; then
  echo -e "${YELLOW}📦 Installing pnpm...${NC}"
  npm install -g pnpm
  echo ""
fi

echo -e "${GREEN}✓${NC} pnpm verified"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pnpm install --frozen-lockfile 2>/dev/null || pnpm install

echo ""
echo "🔨 Building TypeScript..."
pnpm build

echo ""
echo "🌍 Registering global command..."
pnpm install -g .

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${CYAN}✅ Installation Successful!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Usage:"
echo ""
echo "  💻 Interactive mode (recommended):"
echo "     $ passgen"
echo ""
echo "  🔐 Generate 16-character password:"
echo "     $ passgen -l 16"
echo ""
echo "  📋 Generate multiple passwords (5x 32 chars, all character types):"
echo "     $ passgen -l 32 -n -a -A -s -c 5"
echo ""
echo "  🎲 Generate with random character types:"
echo "     $ passgen -l 24 -r"
echo ""
echo "  ❓ Show help:"
echo "     $ passgen --help"
echo ""
echo "✨ Enjoy using passgen!${NC}"
echo ""
