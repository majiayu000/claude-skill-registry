# skill

Manage skills - reusable, parameterized prompts.

## Usage

```bash
codegeass skill [OPTIONS] COMMAND [ARGS]...
```

## Commands

::: mkdocs-click
    :module: codegeass.cli.commands.skill
    :command: skill
    :prog_name: codegeass skill
    :depth: 1

## Examples

### List Skills

```bash
# List all available skills
codegeass skill list

# List with details
codegeass skill list --verbose
```

### Show Skill Details

```bash
codegeass skill show review
```

### Validate a Skill

```bash
# Validate SKILL.md format
codegeass skill validate .claude/skills/review/SKILL.md

# Validate all skills
codegeass skill validate --all
```

### Render a Skill

Preview the rendered prompt with arguments:

```bash
codegeass skill render review "Check authentication code"
```

## Skill Format

Skills use YAML frontmatter in SKILL.md files:

```markdown
---
name: review
description: Review code for issues
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# Code Review

$ARGUMENTS

Focus on:
- Code quality
- Potential bugs
- Security issues
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier |
| `description` | Yes | What the skill does |
| `context` | No | Execution context |
| `agent` | No | Agent type |
| `allowed-tools` | No | Permitted tools |

## Skill Locations

Skills are searched in:

1. `.claude/skills/` in the current project
2. `~/.claude/skills/` for global skills

## Using Skills with Tasks

```bash
# Create a task that uses a skill
codegeass task create \
  --name review-task \
  --schedule "0 9 * * *" \
  --mode skill \
  --skill review \
  --skill-args "Review the API module"
```
