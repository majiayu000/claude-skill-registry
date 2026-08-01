---
name: skills-dcramer-ash
description: Create or update Ash skills in ~/.ash/workspace/skills/.
---

# /create-skill

Create or update Ash skills in `~/.ash/workspace/skills/`.

## Usage

```
/create-skill <name>
```

Example: `/create-skill weather-check`

## Skill Structure

```
~/.ash/workspace/skills/<name>/
├── SKILL.md          # Required - frontmatter + instructions
├── *.sh              # Optional - shell scripts
├── *.py              # Optional - Python scripts
└── *.json            # Optional - data files
```

## SKILL.md Format

```markdown
---
description: One-line description of what the skill does
env:                  # Optional - env vars from config.toml
  - API_KEY
packages:             # Optional - apt packages needed
  - jq
tools:        # Optional - restrict to these tools
  - bash
---

Instructions for the agent to follow.
Reference scripts as: bash ~/.ash/workspace/skills/<name>/script.sh
```

## Config for Env Vars

If your skill needs API keys, add to `~/.ash/config.toml`:

```toml
[skills.<name>]
API_KEY = "your-key-here"
```

## Process

1. Create skill directory: `mkdir -p ~/.ash/workspace/skills/<name>`
2. Write SKILL.md with frontmatter and instructions
3. Add any helper scripts/data files
4. Validate: `uv run ash skill validate ~/.ash/workspace/skills/<name>`
5. Report: skill name, description, and any config needed

## Tips

- Keep instructions focused - Claude is smart
- Put complex logic in scripts, not SKILL.md
- Only declare env vars you actually use
- Use `tools: [bash]` for shell-only skills
