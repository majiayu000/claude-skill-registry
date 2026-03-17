---
name: rustfeed-feed-ops
description: rustfeed のフィード管理（追加、削除、更新）と記事操作（取得、既読管理、お気に入り）のCLI/TUIコマンド実行をサポートします。フィード操作、記事取得、データベース操作時に使用します。
allowed-tools: Bash(cargo:*), Read
---

# Rustfeed フィード操作ガイド

このスキルは rustfeed の CLI/TUI を使ったフィード管理と記事操作の方法を提供します。

## クイックスタート

### CLI実行

```bash
# CLI実行
cargo run --bin rustfeed-cli -- <command>

# TUI実行
cargo run --bin rustfeed-tui
```

## フィード管理

### フィード追加

```bash
cargo run --bin rustfeed-cli -- add <FEED_URL>
```

**例**:
```bash
# 技術ブログのフィード追加
cargo run --bin rustfeed-cli -- add https://blog.rust-lang.org/feed.xml

# 複数のフィードを順次追加
cargo run --bin rustfeed-cli -- add https://example.com/rss
cargo run --bin rustfeed-cli -- add https://another.com/atom.xml
```

**対応形式**: RSS 1.0, RSS 2.0, Atom

### フィード一覧表示

```bash
cargo run --bin rustfeed-cli -- list
```

**出力内容**:
- フィードID
- タイトル
- URL
- 購読開始日

### フィード削除

```bash
cargo run --bin rustfeed-cli -- delete <FEED_ID>
```

**例**:
```bash
# ID 3 のフィードを削除
cargo run --bin rustfeed-cli -- delete 3
```

**注意**: 削除すると関連する記事も全て削除されます

### フィード情報更新

```bash
cargo run --bin rustfeed-cli -- update <FEED_ID>
```

**目的**: フィードのメタデータ（タイトル、説明）を再取得して更新

## 記事操作

### 記事取得（フェッチ）

```bash
# 全フィードから新着記事を取得
cargo run --bin rustfeed-cli -- fetch

# 特定フィードのみ取得
cargo run --bin rustfeed-cli -- fetch --feed-id <ID>
```

**動作**:
1. 登録済みの全フィードにアクセス
2. 新着記事を取得してデータベースに保存
3. 既存記事は重複チェックでスキップ

**エラーハンドリング**:
- タイムアウト: 30秒でリトライ
- 404エラー: スキップして次のフィードへ
- パースエラー: エラーログ出力してスキップ

### 記事一覧表示

```bash
# 全記事表示
cargo run --bin rustfeed-cli -- articles

# 未読のみ表示
cargo run --bin rustfeed-cli -- articles --unread

# お気に入りのみ表示
cargo run --bin rustfeed-cli -- articles --favorite

# 特定フィードの記事のみ
cargo run --bin rustfeed-cli -- articles --feed-id 2
```

**表示内容**:
- 記事ID
- タイトル
- URL
- 公開日時
- 既読/未読ステータス
- お気に入りステータス

### 記事を既読にする

```bash
cargo run --bin rustfeed-cli -- mark-read <ARTICLE_ID>

# 複数記事を一括で既読に
cargo run --bin rustfeed-cli -- mark-read 1 2 3
```

### 記事をお気に入りに追加

```bash
cargo run --bin rustfeed-cli -- favorite <ARTICLE_ID>

# お気に入り解除
cargo run --bin rustfeed-cli -- unfavorite <ARTICLE_ID>
```

## データベース操作

### データベースパス

デフォルト: `~/.rustfeed/rustfeed.db`

カスタムパス指定:
```bash
RUSTFEED_DB_PATH=/path/to/custom.db cargo run --bin rustfeed-cli -- list
```

### データベースのバックアップ

```bash
# バックアップ作成
cp ~/.rustfeed/rustfeed.db ~/.rustfeed/rustfeed.db.backup

# バックアップから復元
cp ~/.rustfeed/rustfeed.db.backup ~/.rustfeed/rustfeed.db
```

### データベースのリセット

```bash
# データベース削除（全データ消去）
rm ~/.rustfeed/rustfeed.db

# 次回実行時に自動的に新しいデータベースが作成される
cargo run --bin rustfeed-cli -- list
```

## TUI操作

### TUI起動

```bash
cargo run --bin rustfeed-tui
```

### TUI キーバインド

| キー | 動作 |
|------|------|
| `j` / `↓` | 下に移動 |
| `k` / `↑` | 上に移動 |
| `Enter` | 記事を開く |
| `r` | フィードをリフレッシュ |
| `m` | 既読/未読トグル |
| `f` | お気に入りトグル |
| `q` | 終了 |

**注意**: TUI は開発中の機能です。最新の実装は `rustfeed-tui/src/` を参照してください。

## よくあるタスク

### 日次の記事取得ルーチン

```bash
# 新着記事を取得して未読のみ表示
cargo run --bin rustfeed-cli -- fetch && \
cargo run --bin rustfeed-cli -- articles --unread
```

### 新しいフィードソースを追加して即座に取得

```bash
cargo run --bin rustfeed-cli -- add https://example.com/feed.xml && \
cargo run --bin rustfeed-cli -- fetch
```

### 記事の検索（データベース直接クエリ）

```bash
# sqlite3を使用
sqlite3 ~/.rustfeed/rustfeed.db "SELECT title, url FROM articles WHERE title LIKE '%Rust%';"
```

## トラブルシューティング

### フィード取得が失敗する

**症状**: "Failed to fetch feed" エラー

**原因と対処**:

1. **ネットワークエラー**
   ```bash
   # ネットワーク接続確認
   curl -I https://example.com/feed.xml
   ```

2. **無効なフィードURL**
   ```bash
   # フィード形式を検証
   curl https://example.com/feed.xml | head -20
   ```

3. **タイムアウト**
   - デフォルトタイムアウト: 30秒
   - カスタムタイムアウト設定は `rustfeed-core/src/feed/` を確認

### データベースがロックされている

**症状**: "database is locked" エラー

**対処**:
```bash
# 他のrustfeedプロセスを確認
ps aux | grep rustfeed

# プロセスを終了
kill <PID>
```

### 文字化けが発生する

**症状**: 記事タイトルやコンテンツが正しく表示されない

**原因**: エンコーディング問題

**対処**:
- `feed-rs` が自動でエンコーディングを処理
- 問題が続く場合は Issue を報告

## 開発者向け情報

### コマンド実装の追加

新しいCLIコマンドを追加する場合：

1. `rustfeed-cli/src/commands/` に新しいモジュールを作成
2. `rustfeed-cli/src/main.rs` の `Commands` enum に追加
3. コマンドロジックを実装
4. `CLAUDE.md` を更新

### データベーススキーマ確認

```bash
sqlite3 ~/.rustfeed/rustfeed.db ".schema"
```

### ログ出力の有効化

```bash
# DEBUGレベルのログ出力
RUST_LOG=debug cargo run --bin rustfeed-cli -- fetch

# 特定モジュールのみ
RUST_LOG=rustfeed_core::feed=trace cargo run --bin rustfeed-cli -- fetch
```

## 参考リソース

- フィード形式仕様: [RSS 2.0](https://www.rssboard.org/rss-specification), [Atom](https://datatracker.ietf.org/doc/html/rfc4287)
- SQLiteドキュメント: https://www.sqlite.org/docs.html
- Clap（CLIパーサー）: https://docs.rs/clap/latest/clap/
- Ratatui（TUI）: https://ratatui.rs/
