---
name: accessing-google-workspace
description: >
  gcloud CLI経由でGoogle SheetsとDocsにアクセスする。
  Google Sheets/DocsのURLを共有した時、または
  スプレッドシート, Sheets, Docs, Google ドキュメント に言及した時に使用。
allowed-tools: [Bash, Read]
user-invocable: false
---

# Google Workspaceアクセス

CLI経由でGoogle SheetsとDocsにアクセスする。

## URL検出

| パターン                          | タイプ        |
| --------------------------------- | ------------- |
| `docs.google.com/spreadsheets/d/` | Google Sheets |
| `docs.google.com/document/d/`     | Google Docs   |

## コマンド

### Google Sheets

```bash
# CSV形式
gsheet "URL"

# JSONL形式（構造化データ向け）
gsheet "URL" json
```

### Google Docs

```bash
# テキスト形式
gdoc "URL"

# Markdown形式
gdoc "URL" md
```

## フォーマット選択

| データタイプ      | 推奨フォーマット     |
| ----------------- | -------------------- |
| 表形式データ      | `json` (JSONL)       |
| ドキュメント/仕様 | `md` (Markdown)      |
| シンプルな取得    | デフォルト (CSV/txt) |
