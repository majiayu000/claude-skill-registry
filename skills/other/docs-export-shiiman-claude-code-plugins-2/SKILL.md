---
name: docs-export
description: Google Docs をエクスポートする。「Docs を PDF で」「ドキュメントをエクスポート」「Docs をダウンロード」「ドキュメントを PDF に」「Word で保存」などで起動。
allowed-tools: [Read, Bash]
---

# Docs Export

Google Docs をファイルにエクスポートします。

## 引数

- ドキュメントID (必須): エクスポートするドキュメントのID

## オプション

- `--output <path>` (必須): 出力ファイルパス
- `--type <format>`: 出力形式（pdf, docx, txt, html, rtf, epub）デフォルト: pdf

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_docs.py export --doc-id <doc-id> --output ~/Downloads/document.pdf
```

### Word形式でエクスポート

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_docs.py export --doc-id <doc-id> --output ~/Downloads/document.docx --type docx
```
