---
name: regex-tester
description: 测试和调试正则表达式，支持匹配高亮、捕获组和常用模式库。
metadata:
  short-description: 测试正则表达式
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# Regex Tester Tool

## Description
Test and debug regular expressions with match highlighting, capture group extraction, and a library of common patterns.

## Trigger
- `/regex` command
- User needs to test regex
- User wants pattern matching help

## Usage

```bash
# Test pattern
python scripts/regex_tester.py "\\d+" "abc123def456"

# Show capture groups
python scripts/regex_tester.py "(\\w+)@(\\w+)" "user@domain" --groups

# Find all matches
python scripts/regex_tester.py "\\b\\w{4}\\b" "The quick brown fox" --all

# Use common pattern
python scripts/regex_tester.py --pattern email "Contact: test@example.com"
```

## Tags
`regex`, `pattern`, `match`, `test`, `text`

## Compatibility
- Codex: ✅
- Claude Code: ✅
