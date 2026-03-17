---
name: sheets-search
description: Google Sheets を検索する。「Sheets 検索」「スプレッドシート検索」「Google Sheets 検索」「シートを探して」「スプレッドシートを検索」「Sheets を見つけたい」「Google スプレッドシート検索」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets Search

Google Sheets を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.spreadsheet' and name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --profile <profile-name> --query "mimeType='application/vnd.google-apps.spreadsheet' and name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "mimeType='application/vnd.google-apps.spreadsheet' and name contains 'spec'"

# 名前に "予算" を含む
--query "mimeType='application/vnd.google-apps.spreadsheet' and name contains '予算'"

# 最近更新された
--query "mimeType='application/vnd.google-apps.spreadsheet' and modifiedTime > '2024-01-01'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
