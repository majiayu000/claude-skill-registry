---
name: text-translator
description: 使用免费翻译API在语言之间翻译文本，支持批量处理和文件翻译。
metadata:
  short-description: 翻译文本
source:
  repository: https://github.com/ssut/py-googletrans
  license: MIT
---

# Text Translator Tool

## Description
Translate text between languages using free translation services with support for auto-detection, batch processing, and file translation.

## Trigger
- `/translate` command
- User needs text translation
- User wants to localize content

## Usage

```bash
# Translate text
python scripts/text_translator.py "Hello world" --to zh

# Auto-detect source language
python scripts/text_translator.py "Bonjour" --to en

# Translate file
python scripts/text_translator.py --file document.txt --to es --output document_es.txt

# Batch translate
python scripts/text_translator.py --file strings.json --to ja --format json
```

## Tags
`translate`, `language`, `i18n`, `localization`, `text`

## Compatibility
- Codex: ✅
- Claude Code: ✅
