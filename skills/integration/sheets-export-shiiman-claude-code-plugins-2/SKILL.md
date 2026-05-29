---
name: sheets-export
description: Google Sheets をエクスポートする。「Sheets を CSV で」「スプレッドシートをエクスポート」「Sheets をダウンロード」「Excel で保存」「CSV に変換」などで起動。
allowed-tools: [Read, Bash]
---

# Sheets Export

Google Sheets をファイルにエクスポートします。

## 引数

- スプレッドシートID (必須): エクスポートするスプレッドシートのID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（csv, xlsx, pdf, ods, tsv）デフォルト: csv

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py export --sheet-id <sheet-id> --output ~/Downloads/data.csv
```

### Excel形式でエクスポート

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_sheets.py export --sheet-id <sheet-id> --output ~/Downloads/data.xlsx --type xlsx
```
