---
name: cron-scheduler
description: 解析、验证和解释cron表达式，计算下次运行时间。
metadata:
  short-description: Cron表达式助手
source:
  repository: https://github.com/kiorber/croniter
  license: MIT
---

# Cron Scheduler Tool

## Description
Parse, validate, and explain cron expressions. Calculate next run times and generate cron syntax.

## Trigger
- `/cron` command
- User needs cron expression help
- User wants to schedule tasks

## Usage

```bash
# Explain cron expression
python scripts/cron_scheduler.py "0 9 * * 1-5"

# Get next N run times
python scripts/cron_scheduler.py "*/15 * * * *" --next 5

# Generate cron from description
python scripts/cron_scheduler.py --generate "every day at 9am"

# Validate expression
python scripts/cron_scheduler.py "0 0 * * *" --validate
```

## Tags
`cron`, `scheduler`, `automation`, `time`, `jobs`

## Compatibility
- Codex: ✅
- Claude Code: ✅
