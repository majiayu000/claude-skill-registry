---
name: sheets-list
description: Google Sheets の一覧を取得する。「スプレッドシート一覧」「Sheets 一覧」「Google Sheets 一覧」「Sheets を見たい」「スプレッドシート」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets List

Google Sheets の一覧を取得します。

## 実行方法

### 基本的な一覧取得

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.spreadsheet'"
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.spreadsheet'" --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py --format json search --query "mimeType='application/vnd.google-apps.spreadsheet'"
```

## 出力項目

- id: スプレッドシートID
- name: スプレッドシート名
- modifiedTime: 更新日時
- webViewLink: 閲覧URL

## 関連操作

- 検索: `drive-search` コマンドでキーワード検索
- 作成: `sheets-create` スキルで新規スプレッドシート作成
