#!/usr/bin/env bash
# passgen-cli クロスプラットフォーム自動セットアップ
# 対応: macOS, Linux, Windows (Git Bash / WSL / PowerShell)

set -e

# カラー定義（すべてのシステムで動作）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# OS判定
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

# バナー表示
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}                                                                ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}           🔐 passgen-cli インストール開始                    ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}              システム: ${GREEN}${OS}${CYAN}                                      ║${NC}"
echo -e "${CYAN}║${NC}                                                                ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Node.js チェック
if ! command -v node &> /dev/null; then
  echo -e "${RED}❌ エラー: Node.js がインストールされていません${NC}"
  echo ""
  echo "インストール手順:"
  case "$OS" in
    macOS)
      echo "  brew install node"
      ;;
    Linux)
      echo "  sudo apt-get install nodejs"
      ;;
    Windows)
      echo "  1. https://nodejs.org/ja/ からダウンロード"
      echo "  2. インストーラーを実行"
      ;;
  esac
  exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo -e "${RED}❌ エラー: Node.js 18 以上が必要です（現在: v$NODE_VERSION）${NC}"
  exit 1
fi

echo -e "${GREEN}✓${NC} Node.js チェック完了"
echo ""

# pnpm チェック・インストール
if ! command -v pnpm &> /dev/null; then
  echo -e "${YELLOW}📦 pnpm をインストール中...${NC}"
  npm install -g pnpm
  echo ""
fi

echo -e "${GREEN}✓${NC} pnpm チェック完了"
echo ""

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ エラー: pnpm がインストールされていません"
    echo "詳細: https://pnpm.io/installation"
    exit 1
fi

echo "📦 依存パッケージをインストール中..."
pnpm install --frozen-lockfile 2>/dev/null || pnpm install

echo ""
echo "🔨 TypeScript をコンパイル中..."
pnpm build

echo ""
echo "🌍 グローバルコマンドを登録中..."
pnpm install -g .

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ インストール完了！                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 使用方法："
echo ""
echo "  💻 対話型モード（推奨）:"
echo "     $ passgen"
echo ""
echo "  🔐 16文字のパスワード生成:"
echo "     $ passgen -l 16"
echo ""
echo "  📋 複数生成（5個×32文字、全文字種）:"
echo "     $ passgen -l 32 -n -a -A -s -c 5"
echo ""
echo "  🎲 ランダム文字種で生成:"
echo "     $ passgen -l 24 -r"
echo ""
echo "  ❓ ヘルプを表示:"
echo "     $ passgen --help"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✨ これであなたも passgen ユーザーです！楽しんでください🎉"
echo ""
