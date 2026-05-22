---
name: apps-script-create
description: Google Apps Script プロジェクトを新規作成する。「GAS 作成」「Apps Script 作成」「スクリプト作成」「GAS を作って」などで起動。
allowed-tools: [Read, Bash]
---

# Apps Script Create

Google Apps Script プロジェクトを新規作成します。

## 実行方法

### スタンドアロンスクリプト作成

```bash
python plugins/shiiman-google/skills/apps-script-list/scripts/google_apps_script.py create --name "スクリプト名"
```

### スプレッドシートに紐付けて作成

```bash
python plugins/shiiman-google/skills/apps-script-list/scripts/google_apps_script.py create --name "マクロ" --parent-id "スプレッドシートID"
```

## ユーザー入力の解釈

- スクリプト名を聞き出す
- スプレッドシートなどに紐付けるか確認
- 紐付ける場合は --parent-id で指定

## 出力項目

- id: スクリプトID
- name: スクリプト名
- parentId: 親ドキュメントID（紐付けた場合）
- url: 編集URL
