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
- Creating new skills in `.claude/skills/`
- Reviewing PRs that modify skills
- Validating skill structure before publishing

## Scripts

### validate-skill.ts

Validate one or more skill directories.

```bash
bunx @plaited/development-skills validate-skill [paths...]
```

**Arguments:**
- `paths`: Optional paths to validate (default: `.claude/skills/`)

**Options:**
- `--json`: Output results as JSON

**Examples:**

```bash
# Validate all skills in .claude/skills/
bunx @plaited/development-skills validate-skill

# Validate a specific skill
bunx @plaited/development-skills validate-skill .claude/skills/typescript-lsp

# Validate multiple paths with JSON output
bunx @plaited/development-skills validate-skill .claude/skills/typescript-lsp .claude/skills/code-documentation --json
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
✓ .claude/skills/code-documentation
✗ .claude/skills/invalid-skill
  ERROR: Missing required field in frontmatter: 'description'

2/3 skills valid
```

### JSON (--json)

```json
[
  {
    "valid": true,
    "path": ".claude/skills/typescript-lsp",
    "errors": [],
    "warnings": [],
    "properties": {
      "name": "typescript-lsp",
      "description": "..."
    }
  }
]
```

## Related Skills

- **typescript-lsp** - Example of a well-structured skill with scripts
- **code-documentation** - TSDoc standards for TypeScript/JavaScript code
