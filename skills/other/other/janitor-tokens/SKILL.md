---
name: janitor-tokens
description: "Show how many context window tokens each skill consumes. Deprecated alias — use /janitor-value (which combines tokens with usage)."
metadata:
  version: 1.3.0
  deprecated: true
  replaced_by: janitor-value
---

# Context Window Token Cost (Deprecated Alias)

**Renamed in v1.3.** Token cost and usage tracking are now merged into one view: `/janitor-value`. The combined report sorts by waste (heavy + unused first), which is more actionable than tokens alone. This alias will be removed in v1.4.

When invoked, run `/janitor-value` and mention the rename in one short line at the top.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/value.sh [--budget N] [--weeks N] [--json]
```

## Migration

- Token cost only → still available; `value.sh` includes the same token table plus usage cross-reference
- JSON output → same `--json` flag works on `value.sh`

## Related Skills

- `/janitor-value` — the new combined view
- `/janitor-report` — full health check
- `/janitor-fix --prune` — remove broken or unused skills
