---
name: apps-script-list
description: Google Apps Script の一覧を取得する。「Apps Script 一覧」「スクリプト一覧」「GAS 一覧」「Apps Script を見たい」「GAS リスト」「Google スクリプト」などで起動。
allowed-tools: [Read, Bash]
---

# Apps Script List

Google Apps Script の一覧を取得します。

## 実行方法

### 基本的な一覧取得

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.script'"
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.script'" --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py --format json search --query "mimeType='application/vnd.google-apps.script'"
```

## 出力項目

- id: スクリプトID
- name: スクリプト名
- modifiedTime: 更新日時
- webViewLink: 閲覧URL

## 関連操作

- 検索: `drive-search` コマンドでキーワード検索
- 作成: `apps-script-create` スキルで新規スクリプト作成
