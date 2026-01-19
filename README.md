# passgen-cli

🔐 軽量でシンプルなパスワード生成CLIツール（TypeScript版）

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Node.js](https://img.shields.io/badge/node.js-18%2B-brightgreen)

## 🚀 クイックスタート

### 前提条件
- **Node.js 18+** 
- **pnpm** （なければ自動インストール）

### インストール

#### macOS / Linux
```bash
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
bash scripts/setup.sh
```

#### Windows (PowerShell)
```powershell
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
.\scripts\setup.ps1
```

#### Windows (CMD)
```cmd
git clone https://github.com/tukuyomil032/CLI-passgen.git
cd CLI-passgen
scripts\setup.bat
```

## 📖 使い方

### 対話型モード（推奨）
```bash
passgen
```
文字タイプ、長さ、コピー先を対話的に選択できます。

### コマンドラインオプション
```bash
# 16文字生成
passgen -l 16

# 複数生成（5個×32文字、全文字種）
passgen -l 32 -n -a -A -s -c 5

# ランダム文字種
passgen -l 24 -r

# ヘルプ
passgen --help
```

### オプション一覧
- `-l, --length` - パスワード長（デフォルト: 16）
- `-c, --count` - 生成数（デフォルト: 1）
- `-n` - 数字を含める
- `-a` - 小文字を含める
- `-A` - 大文字を含める
- `-s` - 記号を含める
- `-r` - ランダム文字種
- `-q, --quiet` - 出力を最小化
- `--copy / --no-copy` - クリップボードコピー制御

## 🔐 セキュリティ

- `crypto.randomInt()` による暗号学的に安全なランダム生成
- すべての入力を検証
- TypeScript による型安全

## ✨ 機能

- 🔐 暗号学的に安全なパスワード生成
- 🎨 ANSIカラー対応の美しいUI
- 💬 対話型モード
- 📋 自動クリップボードコピー
- ⚡ クロスプラットフォーム対応 (macOS/Linux/Windows)
- 🎯 複数のCLIオプション

## 🛠️ 技術スタック

| 技術 | バージョン | 用途 |
|-----|----------|------|
| TypeScript | 5.3+ | 言語 |
| Node.js | 18+ | ランタイム |
| pnpm | 最新 | パッケージ管理 |
| yargs | 17.7.2 | CLI引数解析 |
| inquirer | 9.2.11 | 対話入力 |
| ora | 8.0.1 | スピナー表示 |
| clipboardy | 4.0.0 | クリップボード操作 |

## 📦 開発

### ローカル開発
```bash
pnpm install
pnpm dev          # ts-nodeで直実行
pnpm build        # TypeScriptをコンパイル
pnpm link --global # グローバルにリンク
```


## 📁 プロジェクト構成

```
CLI-passgen/
├── src/                    # TypeScript ソースコード
│   ├── main.ts             # CLI エントリーポイント
│   ├── core/               # コア機能
│   │   ├── generator.ts    # パスワード生成
│   │   ├── clipboard.ts    # クリップボード操作
│   │   └── constants.ts    # 定数定義
│   └── ui/                 # UI 表示
│       ├── display.ts      # 画面描画
│       └── interactive.ts  # 対話型入力
├── scripts/                # セットアップスクリプト
│   ├── setup.sh            # macOS/Linux 用
│   ├── setup.ps1           # Windows PowerShell 用
│   └── setup.bat           # Windows CMD 用
├── package.json            # NPM 設定
├── tsconfig.json           # TypeScript 設定
└── README.md               # このファイル
```

## 📄 ライセンス

MIT

---
