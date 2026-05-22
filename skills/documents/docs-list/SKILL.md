---
name: docs-list
description: Google Docs の一覧を取得する。「ドキュメント一覧」「Docs 一覧」「Google Docs 一覧」「Docs を見たい」「ドキュメント」などで起動。
allowed-tools: [Read, Bash]
---

# Docs List

Google Docs の一覧を取得します。

## 実行方法

### 基本的な一覧取得

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.document'"
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.document'" --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py --format json search --query "mimeType='application/vnd.google-apps.document'"
```

## 出力項目

- id: ドキュメントID
- name: ドキュメント名
- modifiedTime: 更新日時
- webViewLink: 閲覧URL

## 関連操作

- 検索: `drive-search` コマンドでキーワード検索
- 作成: `docs-create` スキルで新規ドキュメント作成
