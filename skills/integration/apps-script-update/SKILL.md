---
name: apps-script-update
description: Google Apps Script のコードを更新する。「GAS 更新」「Apps Script 更新」「スクリプト編集」「コードを更新」などで起動。
allowed-tools: [Read, Bash]
---

# Apps Script Update

Google Apps Script プロジェクトのコードを更新します。

## 実行方法

### コード更新

```bash
python plugins/shiiman-google/skills/apps-script-update/scripts/google_apps_script.py update --script-id "ID" --filename "Code.gs" --code "function myFunc() { Logger.log('Hello'); }"
```

### 新しいファイル追加

```bash
python plugins/shiiman-google/skills/apps-script-update/scripts/google_apps_script.py update --script-id "ID" --filename "Utils.gs" --code "function helper() {}"
```

## ファイルタイプ

- `.gs`: サーバーサイド JavaScript
- `.html`: HTML ファイル
- `.json`: JSON ファイル（appsscript.json など）

## ユーザー入力の解釈

- スクリプトIDを聞き出すか、事前に apps-script-list で検索
- 更新するファイル名を確認
- コード内容を確認

## 出力項目

- id: スクリプトID
- status: 更新ステータス
- filename: 更新したファイル名
- url: 編集URL
