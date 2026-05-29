---
name: sheets-update
description: Google Sheets スプレッドシートのセルを更新する。「スプレッドシート更新」「Sheets 更新」「シートに書き込み」「セルを更新」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets Update

Google Sheets スプレッドシートのセルを更新します。

## 実行方法

### セルを更新

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py update --sheet-id "シートID" --range "A1" --values '["値1", "値2"]'
```

### 複数行を更新

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py update --sheet-id "シートID" --range "A1:B2" --values '[["A1","B1"],["A2","B2"]]'
```

### 行を末尾に追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py append --sheet-id "シートID" --range "Sheet1" --values '["値1", "値2"]'
```

## ユーザー入力の解釈

- シートIDを聞き出すか、事前に sheets-list/drive-search で検索
- 更新範囲と値を確認
- 「追加」「末尾に」などの指定があれば append サブコマンドを使用

## 出力項目

- id: スプレッドシートID
- status: 更新ステータス
- updatedRange: 更新された範囲
- url: 編集URL
