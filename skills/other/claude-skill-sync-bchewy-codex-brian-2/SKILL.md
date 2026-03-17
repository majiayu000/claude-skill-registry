---
name: claude-skill-sync
description: Copy or sync Claude skills from ~/.claude/skills into ~/.codex/skills so they are available in Codex. Use when asked to import, migrate, copy, or sync Claude skills, or when moving skills between Claude and Codex with optional repeatable sync.
---

# Claude Skill Sync

## Overview

Copy Claude skills into Codex using the bundled script. Default behavior is a safe
one-off copy; sync mode supports repeatable runs with optional pruning. You can
also include official Claude plugin skills.

## Quick Start (One-Off Copy)

- Dry run to preview actions:
  `python3 ~/.codex/skills/claude-skill-sync/scripts/claude_skill_sync.py --dry-run`
- Run the copy (prompts on conflicts):
  `python3 ~/.codex/skills/claude-skill-sync/scripts/claude_skill_sync.py`
- Include official plugin skills:
  `python3 ~/.codex/skills/claude-skill-sync/scripts/claude_skill_sync.py --include-official-plugins`

If running from this repo, use:
`python3 skills/claude-skill-sync/scripts/claude_skill_sync.py`

## Conflict Handling

- Default `--conflict ask` prompts per skill: overwrite, skip, or abort.
- For non-interactive runs, set a policy explicitly:
  - `--conflict overwrite`
  - `--conflict skip`
  - `--conflict abort`
- In `--dry-run`, conflicts default to skip with a warning.

## Repeatable Sync

Use `--mode sync` for repeatable updates:
- `python3 ~/.codex/skills/claude-skill-sync/scripts/claude_skill_sync.py --mode sync --conflict ask`
- Optional mirror cleanup (destructive): add `--prune` to remove Codex skills not
  present in Claude.

## Paths and Filters

- Defaults:
  - Source: `~/.claude/skills`
  - Destination: `~/.codex/skills`
- Override with `--source` and `--dest`, add extra roots with `--extra-source`.
- Use `--recursive` to scan nested trees for `SKILL.md`.
- Official plugin skills: add `--include-official-plugins`.
- The script copies directories that contain `SKILL.md`.

### scripts/
Executable code that performs the copy/sync operation.

- `claude_skill_sync.py`: Copy/sync Claude skills into Codex with conflict prompts.
