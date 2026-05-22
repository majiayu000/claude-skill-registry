---
name: validate-skill
description: Validate skill directories against AgentSkills spec
license: ISC
compatibility: Requires bun
allowed-tools: Bash
---

# Validate Skill

## Purpose

This skill validates skill directories against the [AgentSkills specification](https://agentskills.io/specification). Use it to ensure your skills have proper frontmatter, required fields, and follow naming conventions.

**Use when:**
- Creating new skills in any agent's skills directory (`.claude/skills/`, `.cursor/skills/`, etc.)
- Reviewing PRs that modify skills
- Validating skill structure before publishing

## Scripts

### validate-skill.ts

Validate one or more skill directories.

```bash
bunx @plaited/development-skills validate-skill [paths...]
```

**Arguments:**
- `paths`: Paths to validate (defaults to current agent's skills directory)

**Options:**
- `--json`: Output results as JSON

**Examples:**

```bash
# Validate skills in current directory's .claude/skills/
bunx @plaited/development-skills validate-skill .claude/skills

# Validate Cursor skills
bunx @plaited/development-skills validate-skill .cursor/skills

# Validate a specific skill
bunx @plaited/development-skills validate-skill .claude/skills/typescript-lsp

# Validate multiple paths with JSON output
bunx @plaited/development-skills validate-skill .claude/skills .cursor/skills --json
```

## Validation Rules

### Required Fields

- `name`: Skill name (lowercase, alphanumeric with hyphens)
- `description`: Brief description of the skill

### Naming Conventions

- Name must be lowercase
- Only alphanumeric characters and hyphens allowed
- Cannot start or end with hyphen
- Cannot contain consecutive hyphens
- Maximum 64 characters
- Directory name must match skill name

### Optional Fields

- `license`: License identifier
- `compatibility`: Runtime requirements
- `allowed-tools`: Comma-separated list of allowed tools
- `metadata`: Key-value pairs for additional metadata

## Output Format

### Human-Readable (default)

```
✓ .claude/skills/typescript-lsp
✓ .cursor/skills/my-skill
✗ .claude/skills/invalid-skill
  ERROR: Missing required field in frontmatter: 'description'

2/3 skills valid
```

### JSON (--json)

```json
[
  {
    "valid": true,
    "path": ".cursor/skills/my-skill",
    "errors": [],
    "warnings": [],
    "properties": {
      "name": "my-skill",
      "description": "..."
    }
  }
]
```

## Related Skills

- **typescript-lsp** - Example of a well-structured skill with scripts
- **code-documentation** - TSDoc standards for TypeScript/JavaScript code
