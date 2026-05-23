---
name: manage-skills
description: Manages Claude Code skills - creates, updates, and maintains skills following established design principles. Use when the user asks to create a skill, update a skill, refactor a skill, or wants to teach Claude a new capability.
version: 3
---

# Skill Management

## Skill Design Principles

### 1. SKILL.md is Self-Contained
- Contains ALL information needed to use the skill
- Should be as minimal as possible while conveying complete information
- No need for separate README, USAGE, INSTALL, or CHANGELOG files

### 2. Single Script Design
- Optimize for ONE script per skill (not multiple scripts)
- Use command-line parameters for different operations
- Pattern: `./script.sh <command> [arguments]`

### 3. Minimal File Structure
```
skill-name/
├── SKILL.md          # Required - complete documentation
└── script.sh         # Optional - single CLI if needed
```

## SKILL.md Structure

Required frontmatter:
```yaml
---
name: skill-name
description: What it does and when to use it. Use when [triggers].
version: 1
---
```

## Creating a New Skill

1. Create directory in `.claude/skills/skill-name/`
2. Create SKILL.md with frontmatter and documentation
3. Optionally add a shell script for automation
4. Make scripts executable with `chmod +x`

## Rendering Custom UI

For rendering interactive HTML interfaces in chat, use the **create-interface** skill which provides comprehensive documentation on the `mcp__noetect-ui__render_ui` tool.
