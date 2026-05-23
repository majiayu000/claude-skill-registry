---
name: janitor-fix
description: "Automatically fix skill problems (safe preview first). Also use with --prune to find and remove broken symlinks, empty directories, and orphaned skills."
metadata:
  version: 1.2.0
---

# Auto-Fix

Automatically fix common skill issues. Dry-run by default - shows what would change without modifying files.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/fix.sh            # preview fixes
bash ~/.claude/skills/skills-janitor/scripts/fix.sh --apply     # apply fixes
bash ~/.claude/skills/skills-janitor/scripts/fix.sh --prune     # find broken/orphaned skills
bash ~/.claude/skills/skills-janitor/scripts/fix.sh --prune --apply  # remove broken skills
```

## What It Fixes

- Adds missing frontmatter delimiters (`---`)
- Fills empty `description` fields with a template
- Adds missing `version` field (defaults to "1.0.0")
- Generates template descriptions using the skill folder name

## Prune Mode (`--prune`)

Finds and removes broken skills:
- **Broken symlinks** - skill folder points to deleted source
- **Empty directories** - skill folder with no SKILL.md
- **Orphaned skills** - user-scope copies of plugin skills

Dry-run by default. Pass `--apply` to actually remove them.

## Safety

- **Dry-run by default** - must pass `--apply` to write changes
- Skips plugin/marketplace skills (changes get overwritten on update)
- Skips broken symlinks (unless `--prune` mode)
- Logs ALL changes with timestamps to `data/changelog.log`
- Always asks for confirmation before removing

## Related Skills

- For finding issues: `/janitor-report`
- For usage analytics: `/janitor-usage`
- For token cost: `/janitor-tokens`
