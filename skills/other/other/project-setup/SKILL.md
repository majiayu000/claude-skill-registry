---
name: Project Setup and Miyabi Integration
description: Complete project initialization including Cargo workspace setup, GitHub integration, and Miyabi framework integration. Use when creating new projects or integrating Miyabi.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 🚀 Project Setup and Miyabi Integration

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐ (P2 Level)
**Purpose**: プロジェクト初期化、Cargo Workspace設定、Miyabi統合

---

## 📋 概要

新規プロジェクト作成からMiyabiフレームワーク統合まで、
完全なプロジェクトセットアップを提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 新規プロジェクト | "create a new project" |
| Miyabi統合 | "integrate Miyabi into this project" |
| Rust Workspace | "set up a new Rust workspace" |
| マイクロサービス | "starting new microservices" |

---

## 🔧 P1: セットアップモード

### 3つのモード

| モード | 用途 | 所要時間 |
|--------|------|---------|
| **New Project** | ゼロから新規 | 10-15分 |
| **Add Miyabi** | 既存に追加 | 5-10分 |
| **Microservice** | 新規crate追加 | 3-5分 |

---

## 🚀 P2: セットアップパターン

### Pattern 1: 新規プロジェクト

```bash
# Step 1: ディレクトリ作成
mkdir my-project && cd my-project

# Step 2: Cargo Workspace初期化
cat > Cargo.toml << 'EOF'
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.package]
version = "0.1.0"
edition = "2021"
authors = ["Your Name <email@example.com>"]
license = "MIT"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "1"
anyhow = "1"
tracing = "0.1"
EOF

# Step 3: 基本crate作成
mkdir -p crates/my-core
cargo init crates/my-core --lib

# Step 4: Git初期化
git init
```

### Pattern 2: Miyabi統合

```bash
# Step 1: .claudeディレクトリ作成
mkdir -p .claude/{agents,context,commands,Skills}

# Step 2: CLAUDE.md作成
cat > CLAUDE.md << 'EOF'
# Project Name

## MCP First Approach
...
EOF

# Step 3: GitHub統合
# - Labels設定
# - Workflow追加
# - Issue templates

# Step 4: 環境変数設定
cat > .env.example << 'EOF'
GITHUB_TOKEN=
ANTHROPIC_API_KEY=
EOF
```

### Pattern 3: 新規Microservice

```bash
# Step 1: crate作成
cargo init crates/my-service --lib

# Step 2: Cargo.toml設定
cat > crates/my-service/Cargo.toml << 'EOF'
[package]
name = "my-service"
version.workspace = true
edition.workspace = true

[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
EOF

# Step 3: 基本構造
mkdir -p crates/my-service/src
```

---

## ⚡ P3: ディレクトリ構造

### 推奨構造

```
my-project/
├── Cargo.toml           # Workspace root
├── CLAUDE.md            # AI指示書
├── README.md            # プロジェクト説明
├── .env.example         # 環境変数例
├── .gitignore
├── crates/
│   ├── my-core/         # コアライブラリ
│   ├── my-cli/          # CLIバイナリ
│   └── my-api/          # APIサーバー
├── .claude/
│   ├── agents/          # Agent定義
│   ├── context/         # コンテキスト
│   ├── commands/        # カスタムコマンド
│   └── Skills/          # スキル定義
├── .github/
│   ├── workflows/       # CI/CD
│   ├── ISSUE_TEMPLATE/  # Issueテンプレート
│   └── labels.yml       # ラベル定義
└── docs/
    └── README.md        # ドキュメント
```

---

## 📊 チェックリスト

### 新規プロジェクト

- [ ] Cargo.toml (workspace)
- [ ] 基本crate作成
- [ ] Git初期化
- [ ] .gitignore
- [ ] README.md
- [ ] CLAUDE.md

### Miyabi統合

- [ ] .claudeディレクトリ
- [ ] Agent定義
- [ ] コンテキスト
- [ ] カスタムコマンド
- [ ] GitHub Labels
- [ ] CI/CD Workflow

### 環境設定

- [ ] .env.example
- [ ] 環境変数ドキュメント
- [ ] 開発環境手順

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| `cargo build` | 成功 |
| `cargo test` | 成功 |
| Git | 初期コミット完了 |
| ドキュメント | README存在 |

---

## 🔗 関連Skills

- **Rust Development**: ビルド確認
- **Git Workflow**: 初期コミット
- **Documentation**: README作成
