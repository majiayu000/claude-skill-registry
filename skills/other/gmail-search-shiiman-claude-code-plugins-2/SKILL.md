---
name: gmail-search
description: Gmail でメールを検索する。「メール検索」「メールを探して」「Gmail 検索」「メールを検索して」「○○からのメール」「件名で検索」などで起動。
allowed-tools: [Read, Bash]
---

# Gmail Search

Gmail でメールを検索します。Gmail の検索クエリ構文を使用できます。

## 引数

- 検索クエリ (必須): Gmail の検索クエリ

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--include-body`: 本文プレビューを含める

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py search --query "<query>"
```

### 最大件数を指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py search --query "<query>" --max 50
```

### 本文プレビューを含める

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py search --query "<query>" --include-body
```

## クエリ例

| クエリ | 説明 |
|--------|------|
| `from:user@example.com` | 送信者で検索 |
| `to:user@example.com` | 宛先で検索 |
| `subject:会議` | 件名で検索 |
| `has:attachment` | 添付ファイル付き |
| `after:2025/01/01` | 日付以降 |
| `before:2025/01/31` | 日付以前 |
| `is:unread` | 未読 |
| `is:starred` | スター付き |
| `label:important` | ラベルで検索 |
