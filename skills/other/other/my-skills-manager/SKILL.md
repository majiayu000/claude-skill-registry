---
name: my-skills-manager
description: USE WHEN managing skills in ~/.my-skills-collection: adding, removing, syncing, or installing skills to AI agents (OpenCode, VSCode Copilot). Triggers on 'add a skill', 'remove skill', 'sync skills', 'install skills', 'list my skills'.
---

## Overview

Manage skills in your local repository (`~/.my-skills-collection`):

- **Add** skills (as git submodules or copied directories)
- **Remove** skills (handles both submodules and regular dirs)
- **Sync** repository and update all submodules
- **List** installed skills
- **Install** skills to AI agents (OpenCode, VSCode Copilot)

## Quick Commands

Use scripts from `scripts/` for safe, interactive operations:

### Add a skill

```bash
# As git submodule (recommended for external repos)
python scripts/add_skill.py --submodule <git-url> --name <skill-name>

# Copy from local directory
python scripts/add_skill.py --copy /path/to/skill --name <skill-name>
```

### Remove a skill

```bash
python scripts/remove_skill.py --name <skill-name>
```

### Sync repository

```bash
python scripts/sync_repo.py
```

### List installed skills

```bash
python scripts/list_skills.py
```

## Reference Files

Read these for detailed workflows:
- `reference/operations.md` — Detailed add/remove/sync procedures
- `reference/installation.md` — Installing skills to AI agents

## When to Use This Skill

- User mentions managing their skills collection
- User wants to add a skill from GitHub or local path
- User needs to sync or update their skills
- User wants to install skills to OpenCode, VSCode Copilot, or other agents
- User asks about their local skills repository

## Important Notes

- Always confirm destructive operations before executing
- Skills must contain a `SKILL.md` file to be recognized
- Use submodules for external repos to easily update later
- Check `~/.my-skills-collection/skills/` for installed skills