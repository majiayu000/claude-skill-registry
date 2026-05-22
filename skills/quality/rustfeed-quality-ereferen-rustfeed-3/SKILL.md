---
name: rustfeed-quality
description: rustfeed プロジェクトのコード品質チェック（cargo fmt、clippy、test、doc）を実行します。コード品質確認、コミット前チェック、CI/CD検証時に使用します。
allowed-tools: Bash(cargo:*)
---

# Rustfeed コード品質チェック

このスキルは rustfeed プロジェクトのコード品質を確保するためのチェック手順を提供します。

## コミット前の必須チェック

コードをコミットする前に、必ず以下のチェックを実行してください：

### 1. フォーマットチェック

```bash
cargo fmt --check
```

**目的**: コードが Rust 標準のフォーマットに従っているか確認

**修正方法**（エラーが出た場合）:
```bash
cargo fmt
```

### 2. Lintチェック（Clippy）

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

**目的**: Rust のベストプラクティスに従っているか、潜在的なバグがないか確認

**Clippyの警告レベル**:
- `-D warnings`: 警告をエラーとして扱う（CIと同等の厳密さ）
- `--all-targets`: テストコードも含めてチェック
- `--all-features`: 全てのfeatureフラグでチェック

**よくある警告と修正方法**:

| 警告 | 説明 | 修正 |
|------|------|------|
| `unused_imports` | 使われていないインポート | 削除する |
| `dead_code` | 使われていない関数/変数 | 削除または `#[allow(dead_code)]` |
| `needless_return` | 不要な `return` | 削除する |
| `clone_on_copy` | Copyトレイトで `.clone()` | `.clone()` を削除 |

### 3. テスト実行

```bash
# 全テスト実行
cargo test

# 特定のテストのみ
cargo test test_fetch_feed

# 詳細表示
cargo test -- --nocapture
```

**目的**: 既存機能が壊れていないか、新機能が正しく動作するか確認

### 4. ドキュメント生成チェック

```bash
cargo doc --no-deps --document-private-items
```

**目的**: rustdoc コメントが正しくパースされるか確認

**オプション**:
- `--no-deps`: 依存クレートのドキュメントは生成しない（高速化）
- `--document-private-items`: privateアイテムも含める

## クイック品質チェック（一括実行）

全てのチェックを一度に実行する場合：

```bash
cargo fmt --check && \
cargo clippy --all-targets --all-features -- -D warnings && \
cargo test && \
cargo doc --no-deps --document-private-items
```

**成功条件**: 全てのコマンドがエラーなく完了する

## ビルドチェック

### リリースビルド

```bash
cargo build --release
```

**目的**: 最適化ビルドが成功するか確認

### 全ターゲットビルド

```bash
cargo build --all-targets
```

**目的**: CLI、TUI、テスト、ベンチマークが全てビルドできるか確認

## パフォーマンス測定

### ベンチマーク実行（未実装の場合はスキップ）

```bash
cargo bench
```

### ビルド時間測定

```bash
cargo clean
cargo build --timings
# target/cargo-timings/ にレポートが生成される
```

## 依存関係チェック

### 未使用の依存確認（cargo-udeps使用）

```bash
# cargo-udepsのインストール（初回のみ）
cargo install cargo-udeps

# 未使用依存のチェック
cargo +nightly udeps
```

### セキュリティ監査（cargo-audit使用）

```bash
# cargo-auditのインストール（初回のみ）
cargo install cargo-audit

# 脆弱性チェック
cargo audit
```

## トラブルシューティング

### ビルドエラーが出る場合

```bash
# 1. クリーンビルド
cargo clean
cargo build

# 2. Cargo.lockを再生成
rm Cargo.lock
cargo build

# 3. rustupを最新に
rustup update
```

### テストが失敗する場合

```bash
# 詳細なエラー出力
cargo test -- --nocapture --test-threads=1

# 特定のテストのみデバッグ
RUST_LOG=debug cargo test test_name -- --nocapture
```

### Clippyの警告を一時的に無効化

```rust
// 関数レベル
#[allow(clippy::similar_names)]
fn my_function() { /* ... */ }

// ファイルレベル
#![allow(clippy::module_inception)]
```

**注意**: 本当に必要な場合のみ使用し、理由をコメントで説明する

## CI/CD環境での実行

GitHub Actionsなどで実行する場合：

```yaml
- name: Run quality checks
  run: |
    cargo fmt --check
    cargo clippy --all-targets --all-features -- -D warnings
    cargo test
    cargo doc --no-deps
```

## ベストプラクティス

1. **コミット前に必ずチェック**: fmt → clippy → test の順で実行
2. **Clippyの警告はゼロにする**: 警告を放置しない
3. **テストカバレッジを意識**: 主要なパスには必ずテストを書く
4. **ドキュメントを書く**: 公開API には必ず rustdoc を追加

## 参考コマンド

```bash
# コンパイル時間の詳細表示
cargo build -Z timings

# 依存関係ツリー表示
cargo tree

# 重複依存の確認
cargo tree --duplicates
```
