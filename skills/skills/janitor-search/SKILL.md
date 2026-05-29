---
name: janitor-search
description: "Search GitHub for new skills to install. Deprecated alias — use /janitor-discover (combines search + pre-install check)."
metadata:
  version: 1.3.0
  deprecated: true
  replaced_by: janitor-discover
---

# Skill Discovery (Deprecated Alias)

**Renamed in v1.3.** Search and pre-install check are now merged into one entry point: `/janitor-discover`. The new command dispatches to the right mode based on whether you pass a keyword (search) or a URL (pre-install check). This alias will be removed in v1.4.

When invoked, run `/janitor-discover` with the same arguments and mention the rename in one short line at the top.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/discover.sh <keyword-or-url> [options]
```

All flags from the v1.2 search command (`--limit`, `--compare`, `--json`) work unchanged.

## Migration

- Keyword search → `/janitor-discover <keyword>`
- Compare mode → `/janitor-discover --compare <skill-name>`
- Pre-install check → `/janitor-discover <github-url>` (replaces `/janitor-precheck`)

## Related Skills

- `/janitor-discover` — the new combined entry point
- `/janitor-value` — check which existing skills you actually use before adding more
