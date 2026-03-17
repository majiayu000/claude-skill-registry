---
name: apps-script-search
description: Google Apps Script を検索する。「Apps Script 検索」「GAS 検索」「スクリプト検索」「Apps Script を探して」「GAS を見つけたい」「Google スクリプト検索」「Apps Script の検索」などで起動。
allowed-tools: [Read, Bash]
---

# Apps Script Search

Google Apps Script を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.script' and name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --profile <profile-name> --query "mimeType='application/vnd.google-apps.script' and name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "mimeType='application/vnd.google-apps.script' and name contains 'spec'"

# 名前に "自動化" を含む
--query "mimeType='application/vnd.google-apps.script' and name contains '自動化'"

# 最近更新された
--query "mimeType='application/vnd.google-apps.script' and modifiedTime > '2024-01-01'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
