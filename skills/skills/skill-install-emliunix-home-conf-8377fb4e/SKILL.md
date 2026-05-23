---
name: skill-install
description: Install Claude skills from .skill files. Use when installing a new skill provided by the user as a .skill file (which is a zip archive containing the skill directory structure).
---

# Skill Installation

## Installation

Extract the .skill file to `~/.claude/skills/`:

```bash
unzip skill-name.skill -d ~/.claude/skills/
```

The .skill file is a zip archive containing a directory with the skill name (e.g., `skill-name/`), which includes `SKILL.md` and optional bundled resources.

## Post-Installation Behavior

After installation:

1. **Read frontmatter only**: Load and read the YAML frontmatter from the skill's `SKILL.md` to understand its name, description, and when to use it. This is essential metadata for knowing the skill's capabilities.

2. **Lazy-load body**: Do NOT read the full body of `SKILL.md` or any bundled resources at this time. Only load these when the skill actually triggers for a relevant task.

This progressive loading approach minimizes context usage while ensuring new skills are available when needed.
