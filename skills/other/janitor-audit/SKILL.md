---
name: janitor-audit
description: "Show all your installed skills. Deprecated alias — use /janitor-report --brief."
metadata:
  version: 1.3.0
  deprecated: true
  replaced_by: janitor-report
---

# Skill Audit (Deprecated Alias)

**Renamed in v1.3.** This command is kept as a working alias for one release; please switch to `/janitor-report --brief` (inventory-only) or `/janitor-report` (full health check). It will be removed in v1.4.

When invoked, run the inventory scan and tell the user about the rename in one short line at the top of the output.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/scan.sh
```

Output is the JSON inventory `/janitor-report --brief` would produce. Present it as a summary table the same way you would for `/janitor-report --brief`.

## Migration

- Inventory only → `/janitor-report --brief`
- Inventory + health checks → `/janitor-report`
