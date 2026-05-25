---
name: janitor-report
description: "Full health check of all your skills in one report. Use when the user wants to check for errors, find duplicates, detect broken skills, or get a complete overview of skill health. Pass --brief for inventory only."
metadata:
  version: 1.3.0
---

# Health Report

Generate a comprehensive health report combining inventory, quality checks, duplicate detection, and broken skill findings.

As of v1.3, the report covers plugin-namespaced skills (e.g. `marketing-skills:image`, `figma:figma-use`) in addition to user and project scope — these were invisible to the v1.2 report.

## Modes

- **`/janitor-report`** (default) — full health check: inventory + lint + duplicates + broken
- **`/janitor-report --brief`** — inventory only (replaces the old `/janitor-audit`)

## How to Run

Full report:

```bash
bash ~/.claude/skills/skills-janitor/scripts/scan.sh
bash ~/.claude/skills/skills-janitor/scripts/lint.sh
bash ~/.claude/skills/skills-janitor/scripts/detect_dupes.sh
```

Brief mode (inventory only):

```bash
bash ~/.claude/skills/skills-janitor/scripts/scan.sh
```

## What the Full Report Covers

### Inventory (scan.sh)
- All skills across user, project, codex, plugin, and source scopes
- Plugin skills appear with their full invocation name (`<plugin>:<skill>`)
- Symlink status, frontmatter fields, line counts

### Quality Checks (lint.sh)
- **Critical**: Broken symlinks, missing SKILL.md, missing frontmatter
- **Warning**: Missing/empty name or description, description too short/long, missing version
- **Info**: No body content, no Gotchas section, large files

### Duplicate Detection (detect_dupes.sh)
- **Name collisions** — two distinct skills with the same qualified name at different paths
- **Description overlap** — Jaccard similarity >30%, with cross-scope user-vs-plugin pairs explicitly surfaced (e.g. `marketing-seo-audit` (user) ↔ `marketing-skills:seo-audit` (plugin))

## Report Format

Present a unified report with severity levels:

```
| Skill                            | Scope    | Status      | Issues                                   |
|----------------------------------|----------|-------------|------------------------------------------|
| marketing-copywriting            | user     | DUPLICATE?  | 90% overlap with marketing-skills:copywriting |
| seo-audit                        | user     | WARNING     | Description too short                    |
| old-deploy-helper                | user     | CRITICAL    | Broken symlink                           |
| figma:figma-use                  | plugin   | OK          | -                                        |
```

### Recommended Actions

For each issue found, suggest:
- Broken symlinks → `/janitor-fix --prune`
- Quality issues → `/janitor-fix`
- User-vs-plugin duplicates → uninstall the user-scope copy and rely on the plugin (or vice versa)
- Token waste → `/janitor-value`

## Related Skills

- `/janitor-report --brief` — inventory only
- `/janitor-fix` — auto-fix issues
- `/janitor-value` — token cost + usage (combined)
- `/janitor-discover` — find or evaluate new skills
