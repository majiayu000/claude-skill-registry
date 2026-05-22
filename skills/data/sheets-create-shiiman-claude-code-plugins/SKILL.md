---
name: sheets-create
description: Google Sheets スプレッドシートを新規作成する。「スプレッドシート作成」「Sheets 作成」「新しいシート」「スプレッドシートを作って」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets Create

Google Sheets スプレッドシートを新規作成します。

## 実行方法

### 基本的な作成

```bash
python plugins/shiiman-google/skills/sheets-create/scripts/google_sheets.py create --name "スプレッドシート名"
```

### フォルダを指定

```bash
python plugins/shiiman-google/skills/sheets-create/scripts/google_sheets.py create --name "スプレッドシート名" --folder-id "フォルダID"
```

## ユーザー入力の解釈

- スプレッドシート名を聞き出す
- フォルダを指定したい場合は事前に drive-search で検索

## 出力項目

- id: スプレッドシートID
- name: スプレッドシート名
- url: 編集URL
