---
name: slides-search
description: Google Slides を検索する。「Slides 検索」「スライド検索」「Google Slides 検索」「プレゼンを探して」「スライドを検索」「Slides を見つけたい」「Google スライド検索」などで起動。
allowed-tools: [Read, Bash]
---

# Slides Search

Google Slides を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.presentation' and name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --profile <profile-name> --query "mimeType='application/vnd.google-apps.presentation' and name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "mimeType='application/vnd.google-apps.presentation' and name contains 'spec'"

# 名前に "発表" を含む
--query "mimeType='application/vnd.google-apps.presentation' and name contains '発表'"

# 最近更新された
--query "mimeType='application/vnd.google-apps.presentation' and modifiedTime > '2024-01-01'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
