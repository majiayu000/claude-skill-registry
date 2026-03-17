---
name: generating-ceo-briefing
description: |
  Generate weekly CEO briefing reports from activity logs.
  Use when creating executive summaries, analyzing system performance,
  reviewing weekly metrics, or troubleshooting report generation.
  NOT when processing individual tasks (use orchestrator skill).
---

# CEO Briefing Generator Skill

Weekly summary report generation from system logs.

## Quick Start

```bash
# Generate report
python scripts/run.py

# Custom period
python scripts/run.py --days 14

# Dry run
python scripts/run.py --dry-run
```

## Report Sections

1. Executive Summary
2. Activity by Source (Gmail, WhatsApp, Filesystem)
3. Actions Performed
4. Pending Items
5. Errors & Exceptions
6. System Health
7. Recommendations

## Output

Creates `Vault/CEO_Briefing_YYYY-MM-DD.md`

## Verification

Run: `python scripts/verify.py`
