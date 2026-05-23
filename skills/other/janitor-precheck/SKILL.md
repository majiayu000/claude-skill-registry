---
name: janitor-precheck
description: "Check if a new skill overlaps with existing ones before installing. Deprecated alias — use /janitor-discover with a URL or path."
metadata:
  version: 1.3.0
  deprecated: true
  replaced_by: janitor-discover
---

# Pre-Install Overlap Check (Deprecated Alias)

**Renamed in v1.3.** Pre-install check is now part of `/janitor-discover`. Passing a GitHub URL or local path to `/janitor-discover` runs the same overlap analysis. This alias will be removed in v1.4.

When invoked, run `/janitor-discover` with the same argument and mention the rename in one short line at the top.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/discover.sh <github-url-or-path> [--json]
```

Examples:
- `discover.sh https://github.com/user/my-skill`
- `discover.sh user/my-skill`
- `discover.sh ~/Downloads/some-skill/`

## Migration

- Pre-install check by URL → `/janitor-discover <url>`
- Pre-install check by path → `/janitor-discover <path>`

The v1.3 check is more accurate than v1.2 because the installed-skills baseline now includes plugin-namespaced skills (`marketing-skills:image`, `figma:figma-use`, etc.) that v1.2 was blind to.

## Related Skills

- `/janitor-discover` — the new combined entry point
- `/janitor-report` — full health check, including existing duplicates
