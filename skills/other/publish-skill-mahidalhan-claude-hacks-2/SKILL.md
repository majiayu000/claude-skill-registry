---
name: publish-skill
description: |
  USE WHEN: user wants to publish, port, or share a skill to a marketplace repo.
  DO NOT USE WHEN: creating new skills, installing skills, or general questions.
license: MIT
---

# Publish Skill to Marketplace

Port skills from any project to the claude-hacks marketplace.

## Usage

```bash
publish-skill <skill-name> [--source PATH] [--dry-run] [--no-push]
```

## What It Does

1. Copies skill to `skills/<name>/skills/<name>/`
2. Updates `.claude-plugin/marketplace.json`
3. Bumps version if exists, adds new entry if not
4. Commits and pushes

## Examples

```bash
publish-skill my-skill
publish-skill my-skill --source /path/to/.claude/skills/my-skill
publish-skill my-skill --dry-run
```

## Pre-Publish Check

Verify SKILL.md has:
- `name:` in frontmatter
- `description:` with USE WHEN / DO NOT USE WHEN
