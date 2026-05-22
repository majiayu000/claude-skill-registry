---
name: janitor-report
description: "Full health check of all your skills in one report. Use when the user wants to check for errors, find duplicates, detect broken skills, or get a complete overview of skill health."
metadata:
  version: 1.2.0
---

# Health Report

Generate a comprehensive health report combining inventory, quality checks, duplicate detection, and broken skill findings.

## How to Run

Run all analysis scripts and combine results:

```bash
bash ~/.claude/skills/skills-janitor/scripts/scan.sh
bash ~/.claude/skills/skills-janitor/scripts/lint.sh
bash ~/.claude/skills/skills-janitor/scripts/detect_dupes.sh
```

## What It Covers

### Inventory (scan.sh)
- All skills across user, project, plugin, and account scopes
- Symlink status, frontmatter fields, line counts

### Quality Checks (lint.sh)
- **Critical**: Broken symlinks, missing SKILL.md, missing frontmatter
- **Warning**: Missing/empty name or description, description too short/long, missing version
- **Info**: No body content, no Gotchas section, large files

### Duplicate Detection (detect_dupes.sh)
- Keyword overlap analysis using Jaccard similarity
- Flags pairs with >30% overlap
- Shows shared keywords and scopes

### Broken & Orphaned Skills
- Broken symlinks (target deleted)
- Empty directories (no SKILL.md)
- Orphaned user-scope copies of plugin skills

## Report Format

Present a unified report with severity levels:

```
| Skill              | Scope   | Status      | Issues                          |
|--------------------|---------|-------------|---------------------------------|
| marketing-copy     | user    | OK          | -                               |
| seo-audit          | user    | WARNING     | Description too short (28 chars) |
| old-deploy-helper  | user    | CRITICAL    | Broken symlink                  |
| marketing-copy-v2  | user    | DUPLICATE?  | 72% overlap with marketing-copy |
```

### Recommended Actions
For each issue found, suggest:
- Broken symlinks: `/janitor-fix --prune`
- Quality issues: `/janitor-fix`
- Duplicates: manual review, consider removing one
- Token waste: `/janitor-tokens`

## Related Skills

- For inventory only: `/janitor-audit`
- For auto-fixing: `/janitor-fix`
- For usage analytics: `/janitor-usage`
- For token cost: `/janitor-tokens`
