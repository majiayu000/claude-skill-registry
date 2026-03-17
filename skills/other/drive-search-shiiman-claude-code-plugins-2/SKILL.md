---
name: drive-search
description: Google Drive を検索する。「Drive を検索」「ドライブ検索」「ファイルを探して」「Drive で検索」「Google Drive 検索」「ファイル名で検索」「条件で検索」などで起動。
allowed-tools: [Read, Bash]
---

# Drive Search

Google Drive を検索します。

## 引数

- 検索クエリ (必須): 名前の部分一致など（例: `spec`）

## 実行方法

### アクティブプロファイルで検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --query "name contains '<検索キーワード>'"
```

### プロファイル指定で検索

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py search --profile <profile-name> --query "name contains '<検索キーワード>'"
```

## 検索クエリ例

```bash
# 名前に "spec" を含む
--query "name contains 'spec'"

# 名前に "レポート" を含む
--query "name contains 'レポート'"

# 特定の種類のファイル
--query "mimeType='application/pdf' and name contains 'spec'"

# 最近更新された
--query "modifiedTime > '2024-01-01'"

# フォルダ内を検索
--query "'<folder-id>' in parents and name contains 'spec'"
```

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
