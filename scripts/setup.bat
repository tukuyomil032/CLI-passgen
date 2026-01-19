@echo off
REM passgen-cli Windows セットアップスクリプト (Batch版)
REM 対応: Windows CMD

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║           🔐 passgen-cli インストール開始                    ║
echo ║              システム: Windows (CMD)                          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Node.js チェック
where node >nul 2>nul
if errorlevel 1 (
    echo ❌ エラー: Node.js がインストールされていません
    echo.
    echo インストール手順:
    echo   1. https://nodejs.org/ja/ にアクセス
    echo   2. LTS版をダウンロードしてインストール
    echo   3. CMD/PowerShellを再起動して再度このスクリプトを実行
    echo.
    exit /b 1
)

echo ✓ Node.js チェック完了
echo.

REM pnpm チェック・インストール
where pnpm >nul 2>nul
if errorlevel 1 (
    echo 📦 pnpm をインストール中...
    call npm install -g pnpm
    echo.
)

echo ✓ pnpm チェック完了
echo.

REM 依存パッケージ インストール
echo 📦 依存パッケージをインストール中...
call pnpm install

echo ✓ パッケージインストール完了
echo.

REM TypeScript コンパイル
echo 🔨 TypeScript をコンパイル中...
call pnpm build

echo ✓ コンパイル完了
echo.

REM グローバルコマンド登録
echo 🌍 グローバルコマンドを登録中...
call pnpm install -g .

echo ✓ グローバル登録完了
echo.

REM 完成メッセージ
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ✅ インストール完了！                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📝 使用方法:
echo.
echo   💻 対話型モード（推奨）:
echo      ^> passgen
echo.
echo   🔐 16文字のパスワード生成:
echo      ^> passgen -l 16
echo.
echo   📋 複数生成（5個×32文字、全文字種）:
echo      ^> passgen -l 32 -n -a -A -s -c 5
echo.
echo   🎲 ランダム文字種で生成:
echo      ^> passgen -l 24 -r
echo.
echo   ❓ ヘルプを表示:
echo      ^> passgen --help
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✨ これであなたも passgen ユーザーです！楽しんでください🎉
echo.

endlocal
