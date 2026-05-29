---
name: meatycapture-capture
description: Capture bugs/enhancements/ideas to request-logs. For quick operations use /mc command instead.
---

# MeatyCapture Skill

Request-log markdown files for development tracking.

## Capture Method Selection

| Scenario | Method | Tokens/Effort |
|----------|--------|---------------|
| Single capture during development | `mc-quick.sh` | ~50 tokens |
| AI agent capturing findings | `mc-quick.sh` | ~50 tokens |
| Batch capture (3+ items) | Direct CLI | ~200+ tokens |
| Complex notes or custom fields | Direct CLI | ~200+ tokens |
| Appending to existing docs | Direct CLI | ~150 tokens |
| Post-commit: update docs + close item | `update-bug-docs.py` | ~20 tokens |
| Batch file bugs (3+) from JSON/CSV | `batch-file-bugs.sh` | ~30 tokens |

**Scripts spec**: `.claude/specs/script-usage/bug-automation-scripts.md`

## Quick Capture Script

Ultra-simple wrapper - reduces ~20 lines JSON to single command:

```bash
mc-quick.sh TYPE DOMAIN SUBDOMAIN "Title" "Problem" "Goal" [notes...]

# Examples:
mc-quick.sh enhancement web deployments "Add remove button" "Button not implemented" "Full removal workflow"
mc-quick.sh bug api validation "Fix timeout" "Sessions expire early" "Extend TTL to 24h"

# With environment variables:
MC_PROJECT=other-project MC_PRIORITY=high mc-quick.sh bug cli commands "Title" "Problem" "Goal"
```

**Environment Variables**: `MC_PROJECT` (default: skillmeat), `MC_PRIORITY` (default: medium), `MC_STATUS` (default: triage)

**Full documentation**: [./usage-specs/mc-quick-script.md](./usage-specs/mc-quick-script.md)

## Quick Commands (use `/mc` for simple operations)

| Command | Example |
|---------|---------|
| List | `meatycapture log list PROJECT --json` |
| View | `meatycapture log view PATH --json` |
| Search | `meatycapture log search "query" PROJECT --json` |
| Capture | `meatycapture log create --json < input.json` |
| Note Add | `meatycapture log note add DOC ITEM -c "text"` |
| Update | `meatycapture log item update DOC ITEM --status done` |

## Workflows (load only when needed)

| Action | When to Load |
|--------|--------------|
| [Capture](./workflows/capturing.md) | Batch capture, validation, templates |
| [View/Search](./workflows/viewing.md) | Advanced filters, output formats |
| [Status Update](./workflows/updating.md) | Change item status, add notes |
| [Projects](./workflows/managing.md) | Configure projects, defaults |

## Field Reference

See [./references/field-options.md](./references/field-options.md) for valid values.
