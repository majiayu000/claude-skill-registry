---
name: Debugging and Troubleshooting
description: Systematic error diagnosis and debugging workflow for Rust code. Use when code isn't working, tests fail, or runtime errors occur.
allowed-tools: Bash, Read, Grep, Glob
---

# 🐛 Debugging and Troubleshooting

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐⭐ (P1 Level)
**Purpose**: 体系的なエラー診断とRustデバッグワークフロー

---

## 📋 概要

コンパイルエラー、テスト失敗、ランタイムエラーに対する
体系的な診断と解決ワークフローを提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 動作不良 | "this code isn't working" |
| テスト失敗 | "why is this test failing?" |
| エラー解析 | "debug this error" |
| コンパイルエラー | "compilation error" |
| ランタイムエラー | "runtime panic" |

---

## 🔧 P1: エラー分類と対処

### エラー分類表

| 分類 | 症状 | 診断コマンド | 優先度 |
|------|------|-------------|--------|
| コンパイルエラー | `error[E####]` | `cargo check` | 高 |
| テスト失敗 | `test ... FAILED` | `cargo test -- --nocapture` | 高 |
| ランタイムpanic | `thread 'main' panicked` | `RUST_BACKTRACE=1` | 高 |
| ロジックエラー | 期待と異なる出力 | `dbg!()`, ログ | 中 |
| パフォーマンス | 遅い・メモリ大 | `cargo bench`, `valgrind` | 中 |
| 統合エラー | 外部サービス失敗 | ネットワーク診断 | 低 |

---

## 🚀 P2: デバッグパターン

### Pattern 1: コンパイルエラー

```bash
# Step 1: エラー確認
cargo check 2>&1 | head -50

# Step 2: エラーコード解析
# error[E0277] → Trait未実装
# error[E0412] → 型未定義
# error[E0433] → モジュール未解決

# Step 3: 詳細情報
rustc --explain E0277
```

**よくあるエラーと解決**:

| エラーコード | 原因 | 解決策 |
|-------------|------|--------|
| E0277 | Trait未実装 | `#[derive(...)]` または手動実装 |
| E0412 | 型が見つからない | `use`文追加 |
| E0433 | モジュール解決失敗 | パス確認、`mod`宣言 |
| E0502 | 借用競合 | 借用スコープ見直し |
| E0382 | 所有権移動後使用 | `clone()` または参照 |

### Pattern 2: テスト失敗

```bash
# Step 1: 失敗テスト特定
cargo test 2>&1 | grep FAILED

# Step 2: 詳細出力で実行
cargo test test_name -- --nocapture

# Step 3: 順次実行（並列問題回避）
cargo test -- --test-threads=1

# Step 4: アサーション詳細
# pretty_assertions, insta使用推奨
```

### Pattern 3: ランタイムpanic

```bash
# Step 1: バックトレース取得
RUST_BACKTRACE=1 cargo run

# Step 2: 完全バックトレース
RUST_BACKTRACE=full cargo run

# Step 3: panic箇所特定
# at src/lib.rs:42:5 を確認

# Step 4: デバッガ使用
rust-lldb target/debug/miyabi
```

### Pattern 4: ロジックエラー

```rust
// dbg!マクロ使用
let result = dbg!(compute_value());

// tracing使用
tracing::debug!(?value, "computed value");

// 条件付きログ
if cfg!(debug_assertions) {
    println!("Debug: {:?}", state);
}
```

---

## ⚡ P3: 高度なデバッグツール

### デバッグツール一覧

| ツール | 用途 | コマンド |
|--------|------|---------|
| `rust-lldb` | デバッガ | `rust-lldb target/debug/miyabi` |
| `cargo-expand` | マクロ展開 | `cargo expand` |
| `cargo-asm` | アセンブリ確認 | `cargo asm` |
| `valgrind` | メモリ診断 | `valgrind ./target/debug/miyabi` |
| `miri` | UB検出 | `cargo +nightly miri test` |

### VS Codeデバッグ設定

```json
{
  "type": "lldb",
  "request": "launch",
  "name": "Debug Miyabi",
  "cargo": {
    "args": ["build", "--bin=miyabi"]
  },
  "args": [],
  "cwd": "${workspaceFolder}"
}
```

---

## 🛡️ 共通パニック対処

| パニック | 原因 | 対処 |
|----------|------|------|
| `unwrap()` on None | Option未処理 | `if let Some` / `?` |
| `unwrap()` on Err | Result未処理 | `match` / `?` |
| index out of bounds | 配列範囲外 | `.get()` / bounds check |
| overflow | 算術オーバーフロー | `checked_*` / `wrapping_*` |
| stack overflow | 無限再帰 | 再帰ロジック見直し |

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| エラー分類 | 正確な分類 |
| 根本原因特定 | 原因明確化 |
| 解決策提示 | 具体的な修正方法 |
| 再発防止 | テスト追加 |

---

## 🔗 関連Skills

- **Rust Development**: ビルド・テスト
- **Performance Analysis**: パフォーマンス問題
- **Security Audit**: セキュリティ問題
