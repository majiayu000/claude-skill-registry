---
name: forms-search
description: Google Forms を検索する。「Forms 検索」「フォーム検索」「Google Forms 検索」「フォームを探して」「Forms を見つけたい」「アンケート検索」「Google フォーム検索」などで起動。
allowed-tools: [Read, Bash]
---

# Forms Search

Google Forms を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.form' and name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --profile <profile-name> --query "mimeType='application/vnd.google-apps.form' and name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "mimeType='application/vnd.google-apps.form' and name contains 'spec'"

# 名前に "アンケート" を含む
--query "mimeType='application/vnd.google-apps.form' and name contains 'アンケート'"

# 最近更新された
--query "mimeType='application/vnd.google-apps.form' and modifiedTime > '2024-01-01'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
