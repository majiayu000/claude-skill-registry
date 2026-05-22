---
name: docs-create
description: Google Docs ドキュメントを新規作成する。「ドキュメント作成」「Docs 作成」「新しいドキュメント」「ドキュメントを作って」などで起動。
allowed-tools: [Read, Bash]
---

# Docs Create

Google Docs ドキュメントを新規作成します。

## 実行方法

### 基本的な作成

```bash
python plugins/shiiman-google/skills/docs-create/scripts/google_docs.py create --name "ドキュメント名"
```

### フォルダを指定

```bash
python plugins/shiiman-google/skills/docs-create/scripts/google_docs.py create --name "ドキュメント名" --folder-id "フォルダID"
```

### 初期内容を指定

```bash
python plugins/shiiman-google/skills/docs-create/scripts/google_docs.py create --name "ドキュメント名" --content "初期テキスト"
```

## ユーザー入力の解釈

- ドキュメント名を聞き出す
- フォルダを指定したい場合は事前に drive-search で検索
- 初期内容があれば --content で指定

## 出力項目

- id: ドキュメントID
- name: ドキュメント名
- url: 編集URL
