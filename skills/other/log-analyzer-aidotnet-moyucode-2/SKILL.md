---
name: log-analyzer
description: 解析和分析日志文件，支持模式匹配、过滤、统计和错误检测。
metadata:
  short-description: 分析日志文件
source:
  repository: https://github.com/logpai/logparser
  license: MIT
---

# Log Analyzer Tool

## Description
Parse and analyze log files to extract patterns, filter entries, generate statistics, and detect errors.

## Trigger
- `/logs` command
- User needs to analyze logs
- User wants to find errors in logs

## Usage

```bash
# Analyze log file
python scripts/log_analyzer.py app.log

# Filter by level
python scripts/log_analyzer.py app.log --level ERROR

# Search pattern
python scripts/log_analyzer.py app.log --grep "connection failed"

# Get statistics
python scripts/log_analyzer.py app.log --stats

# Tail mode
python scripts/log_analyzer.py app.log --tail 100
```

## Tags
`logs`, `analysis`, `debugging`, `monitoring`, `errors`

## Compatibility
- Codex: ✅
- Claude Code: ✅
