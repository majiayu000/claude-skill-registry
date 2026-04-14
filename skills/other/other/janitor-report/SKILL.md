---
name: janitor-report
description: "Full health check of all your skills in one report"
metadata:
  version: 1.0.0
---

# Health Report

Generate a comprehensive health report combining audit, lint, and duplicate detection results.

## How to Run

Run all three analysis scripts and combine results:

```bash
bash ~/.claude/skills/skills-janitor/scripts/scan.sh
bash ~/.claude/skills/skills-janitor/scripts/lint.sh
bash ~/.claude/skills/skills-janitor/scripts/detect_dupes.sh
```

## Report Format

Present a unified report with:

### Summary Table
```
| Skill              | Scope   | Status      | Issues                          |
|--------------------|---------|-------------|---------------------------------|
| marketing-copy     | user    | OK          | -                               |
| seo-audit          | user    | WARNING     | Description too short (28 chars) |
| old-deploy-helper  | user    | CRITICAL    | Broken symlink                  |
| marketing-copy-v2  | user    | DUPLICATE?  | 72% overlap with marketing-copy |
```

### Severity Levels
- `CRITICAL` - broken skills, missing files (fix immediately)
- `WARNING` - suboptimal configuration (should fix)
- `INFO` - suggestions for improvement (nice to have)

### Recommended Actions
For each issue found, suggest a specific fix with the relevant janitor- command.

## Related Skills

- For inventory only: `/janitor-audit`
- For error check only: `/janitor-check`
- For duplicates only: `/janitor-duplicates`
- For usage analytics: `/janitor-usage`
