---
name: Dependency Management for Cargo and npm
description: Manage Rust and Node.js dependencies including adding, updating, auditing, and resolving conflicts. Use when updating dependencies or resolving version conflicts.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# 📦 Dependency Management

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐ (P2 Level)
**Purpose**: Cargo/npm依存関係の追加・更新・監査

---

## 📋 概要

Rust (Cargo) と Node.js (npm) の依存関係管理、
バージョン競合解決、セキュリティ監査を提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 依存更新 | "update dependencies" |
| バージョン競合 | "why is there a version conflict?" |
| 依存追加 | "add a new dependency" |
| 定期更新 | "weekly/monthly dependency updates" |

---

## 🔧 P1: コマンド一覧

### Cargo（Rust）

| コマンド | 用途 | 頻度 |
|---------|------|------|
| `cargo add <crate>` | 依存追加 | 中 |
| `cargo update` | 全依存更新 | 週次 |
| `cargo update -p <crate>` | 特定更新 | 随時 |
| `cargo tree` | 依存ツリー | 調査時 |
| `cargo audit` | セキュリティ監査 | 週次 |
| `cargo-udeps` | 未使用検出 | 月次 |

### npm（Node.js）

| コマンド | 用途 | 頻度 |
|---------|------|------|
| `npm install <pkg>` | 依存追加 | 中 |
| `npm update` | 全依存更新 | 週次 |
| `npm audit` | セキュリティ監査 | 週次 |
| `npm outdated` | 古い依存確認 | 月次 |

---

## 🚀 P2: 更新戦略

### 更新頻度ガイドライン

| バージョン | 頻度 | リスク | 例 |
|-----------|------|--------|-----|
| Patch (x.x.Y) | 週次 | 低 | 1.0.0 → 1.0.1 |
| Minor (x.Y.0) | 月次 | 中 | 1.0.0 → 1.1.0 |
| Major (Y.0.0) | 四半期 | 高 | 1.0.0 → 2.0.0 |

### Pattern 1: 安全な更新

```bash
# Step 1: 現状確認
cargo outdated

# Step 2: Patch更新（安全）
cargo update

# Step 3: テスト
cargo test --all

# Step 4: 監査
cargo audit
```

### Pattern 2: 特定クレート更新

```bash
# 特定クレートのみ
cargo update -p tokio

# バージョン指定（Cargo.toml）
[dependencies]
tokio = "1.35"  # 1.35.x の最新
```

### Pattern 3: 依存ツリー調査

```bash
# 全体ツリー
cargo tree

# 特定クレートの依存元
cargo tree -i tokio

# 重複検出
cargo tree -d
```

---

## ⚡ P3: バージョン競合解決

### 競合パターン

| パターン | 症状 | 解決策 |
|----------|------|--------|
| 複数バージョン | `cargo tree -d` で検出 | 統一バージョン指定 |
| 非互換feature | コンパイルエラー | feature調整 |
| 循環依存 | リンクエラー | 依存構造見直し |

### 解決例

```toml
# Cargo.toml - バージョン統一
[workspace.dependencies]
tokio = { version = "1.35", features = ["full"] }

[dependencies]
tokio = { workspace = true }
```

```bash
# feature競合確認
cargo tree -f "{p} {f}"
```

---

## 📊 Workspace依存管理

### 推奨構造

```toml
# ルート Cargo.toml
[workspace]
members = ["crates/*"]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

```toml
# crates/miyabi-core/Cargo.toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
```

---

## 🛡️ セキュリティ監査

### 自動監査設定

```bash
# 監査実行
cargo audit

# 修正可能な脆弱性を自動修正
cargo audit fix

# CI用（失敗時に終了）
cargo audit --deny warnings
```

### 未使用依存検出

```bash
# インストール
cargo install cargo-udeps

# 実行（nightly必要）
cargo +nightly udeps
```

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| `cargo audit` | 0 vulnerabilities |
| `cargo tree -d` | 最小限の重複 |
| `cargo-udeps` | 未使用なし |
| ビルド | 成功 |
| テスト | 全パス |

---

## 🔗 関連Skills

- **Rust Development**: ビルド確認
- **Security Audit**: 脆弱性対応
- **Git Workflow**: 更新コミット
