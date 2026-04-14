---
name: janitor-fix
description: "Automatically fix skill problems (safe preview first)"
metadata:
  version: 1.0.0
---

# Auto-Fix

Automatically fix common skill issues. Dry-run by default - shows what would change without modifying files.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/fix.sh          # preview changes
bash ~/.claude/skills/skills-janitor/scripts/fix.sh --apply   # apply changes
```

## What It Fixes

- Adds missing frontmatter delimiters (`---`)
- Fills empty `description` fields with a template
- Adds missing `version` field (defaults to "1.0.0")
- Generates template descriptions using the skill folder name

## Safety

- **Dry-run by default** - must pass `--apply` to write changes
- Skips plugin/marketplace skills (changes get overwritten on update)
- Skips broken symlinks
- Logs ALL changes with timestamps to `data/changelog.log`
- Never deletes anything

## Important

- **NEVER modify skill content without showing the diff first**
- **NEVER delete skills without explicit user confirmation**
- Always run lint first to understand what needs fixing

## Related Skills

- For finding issues: `/janitor-check`
- For duplicate detection: `/janitor-duplicates`
- For broken links/orphans: `/janitor-cleanup`
