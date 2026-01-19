# passgen-cli Windows 自動セットアップ (PowerShell)
# 対応: Windows 10/11

param(
    [switch]$Help
)

if ($Help) {
    Write-Host "passgen-cli Windows セットアップスクリプト"
    Write-Host ""
    Write-Host "使用方法:"
    Write-Host "  .\setup.ps1"
    Write-Host ""
    exit 0
}

# 色定義
$Colors = @{
    Red    = "Red"
    Green  = "Green"
    Yellow = "Yellow"
    Cyan   = "Cyan"
    Blue   = "Blue"
}

# バナー
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║           🔐 passgen-cli インストール開始                    ║" -ForegroundColor Cyan
Write-Host "║              システム: Windows                               ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Node.js チェック
$NodeInstalled = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
if (-not $NodeInstalled) {
    Write-Host "❌ エラー: Node.js がインストールされていません" -ForegroundColor Red
    Write-Host ""
    Write-Host "インストール手順:"
    Write-Host "  1. https://nodejs.org/ja/ にアクセス"
    Write-Host "  2. LTS版をダウンロードしてインストール"
    Write-Host "  3. PowerShellを再起動して再度このスクリプトを実行"
    Write-Host ""
    exit 1
}

# Node.js バージョン確認
$NodeVersion = [int]((node -v) -replace "v", "" -split "\.")[0]
if ($NodeVersion -lt 18) {
    Write-Host "❌ エラー: Node.js 18 以上が必要です（現在: v$NodeVersion）" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Node.js チェック完了" -ForegroundColor Green
Write-Host ""

# pnpm チェック・インストール
$PnpmInstalled = $null -ne (Get-Command pnpm -ErrorAction SilentlyContinue)
if (-not $PnpmInstalled) {
    Write-Host "📦 pnpm をインストール中..." -ForegroundColor Yellow
    npm install -g pnpm
    Write-Host ""
}

Write-Host "✓ pnpm チェック完了" -ForegroundColor Green
Write-Host ""

# 依存パッケージ インストール
Write-Host "📦 依存パッケージをインストール中..." -ForegroundColor Yellow
pnpm install

Write-Host "✓ パッケージインストール完了" -ForegroundColor Green
Write-Host ""

# TypeScript コンパイル
Write-Host "🔨 TypeScript をコンパイル中..." -ForegroundColor Yellow
pnpm build

Write-Host "✓ コンパイル完了" -ForegroundColor Green
Write-Host ""

# グローバルコマンド登録
Write-Host "🌍 グローバルコマンドを登録中..." -ForegroundColor Yellow
pnpm install -g .

Write-Host "✓ グローバル登録完了" -ForegroundColor Green
Write-Host ""

# 完成メッセージ
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    ✅ インストール完了！                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 使用方法:" -ForegroundColor Green
Write-Host ""
Write-Host "  💻 対話型モード（推奨）:" -ForegroundColor Cyan
Write-Host "     > passgen"
Write-Host ""
Write-Host "  🔐 16文字のパスワード生成:" -ForegroundColor Cyan
Write-Host "     > passgen -l 16"
Write-Host ""
Write-Host "  📋 複数生成（5個×32文字、全文字種）:" -ForegroundColor Cyan
Write-Host "     > passgen -l 32 -n -a -A -s -c 5"
Write-Host ""
Write-Host "  🎲 ランダム文字種で生成:" -ForegroundColor Cyan
Write-Host "     > passgen -l 24 -r"
Write-Host ""
Write-Host "  ❓ ヘルプを表示:" -ForegroundColor Cyan
Write-Host "     > passgen --help"
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ これであなたも passgen ユーザーです！楽しんでください🎉" -ForegroundColor Green
Write-Host ""
