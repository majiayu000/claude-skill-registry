---
name: janitor-usage
description: "Show which skills you use. Deprecated alias — use /janitor-value (which now combines usage + token cost)."
metadata:
  version: 1.3.0
  deprecated: true
  replaced_by: janitor-value
---

# Usage Tracking (Deprecated Alias)

**Renamed in v1.3.** Usage and token-cost are now merged into one view: `/janitor-value`. The combined report sorts skills by waste (heavy + unused first), which is more useful than seeing usage alone. This alias will be removed in v1.4.

When invoked, run `/janitor-value` and mention the rename in one short line at the top.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/value.sh [--weeks N] [--json]
```

## Migration

- Just usage data → still available via `value.sh` (usage is shown in the combined table)
- Raw JSON usage history → `~/.claude/skills/skills-janitor/data/usage-history.json` (unchanged)

## Related Skills

- `/janitor-value` — the new combined view
- `/janitor-report` — full health check
