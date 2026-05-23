---
name: skill-writer
description: "Expert assistant for authoring Claude Code skills. Creates SKILL.md files with proper YAML frontmatter, validates naming conventions, enforces tool minimalism, and applies official best practices. Triggers on keywords: writing skills, creating skills, skill authoring, SKILL.md, new skill, skill template, skill validation, skill structure, create skill, update skill"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Skill Writer

Expert guide for creating Claude Code skills. Reference: https://code.claude.com/docs/en/skills

## Purpose

Generate precise SKILL.md files that comply with Claude Code skill specification:
- Validate naming constraints (64 chars, lowercase/numbers/hyphens only, no reserved words)
- Enforce description requirements (1024 chars max, third person, trigger keywords)
- Apply tool minimalism (only grant necessary tools)
- Ensure project-agnostic field is explicitly set
- Maintain file structure constraints (under 500 lines, one-level references)

## Variables

None - skill-writer has no runtime configuration.

## Instructions

### 1. Understand Request

Parse user request to determine:
- Skill purpose and scope
- Target operations (read-only, write, refactor, workflow)
- Project-specific vs reusable

### 2. Validate Constraints (BLOCKING)

**STOP. Validate BEFORE generating.**

| Field | Constraint |
|-------|------------|
| `name` | Max 64 chars, `/^[a-z0-9-]+$/`, no "anthropic"/"claude" |
| `description` | Max 1024 chars, third person, includes "Triggers on keywords:" |
| `project-agnostic` | REQUIRED - must be explicitly true or false |

See `cookbook/validation.md` for detailed checks.

### 3. Select Pattern

Choose from `templates/`:
- `skill-template.md` - Comprehensive template with all sections

### 4. Generate SKILL.md

Apply template with validated values. Follow structure from `templates/skill-template.md`.

### 5. Verify (BLOCKING)

**STOP. Verify before delivery.**
- Line count under 500
- No bash execution pattern (exclamation-backtick sequence)
- All paths use forward slashes
- References are one-level deep

## Workflow

```
1. Parse request -> scope, tools, agnostic?
2. Validate constraints -> BLOCK if invalid
3. Select pattern based on tool needs
4. Generate SKILL.md from template
5. Verify output -> BLOCK if violations
6. Deliver with checklist confirmation
```

## Report

Output format for generated skills:

```
## Generated Skill: {name}

### Validation
- Name: PASS/FAIL (reason)
- Description: PASS/FAIL (reason)
- Project-agnostic: PASS/FAIL (value)
- Tools: {count} tools granted

### Files Created
- SKILL.md ({line_count} lines)
- {supporting_files if any}

### Checklist
- [ ] Name constraints satisfied
- [ ] Description includes triggers
- [ ] project-agnostic explicitly set
- [ ] Under 500 lines
- [ ] Minimal tools granted
```

## Examples

### DOs

**Focused purpose with minimal tools:**
```yaml
---
name: python-type-annotator
description: Adds type annotations to Python functions. Infers types from usage and docstrings. Triggers on keywords: add types, type hints, annotate python
project-agnostic: true
allowed-tools:
  - Read
  - Edit
  - Glob
---
```

**Clear triggers in description:**
```yaml
description: Formats SQL queries with consistent style. Handles SELECT, INSERT, UPDATE, DELETE. Triggers on keywords: format sql, sql formatter, pretty print sql
```

**Explicit project-agnostic for reusable skills:**
```yaml
project-agnostic: true  # Zero project dependencies
```

### DONTs

**Vague name and description:**
```yaml
# BAD - unfocused
name: code-helper
description: Helps with all coding tasks
```

**Missing trigger keywords:**
```yaml
# BAD - not discoverable
description: Formats SQL queries
```

**Excessive tool permissions:**
```yaml
# BAD - grants more than needed for read-only task
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
```

**Missing project-agnostic:**
```yaml
# BAD - required field missing
name: my-skill
description: Does something
allowed-tools:
  - Read
```

**Reserved word in name:**
```yaml
# BAD - contains reserved word
name: claude-assistant
```

## Quick Reference

### YAML Frontmatter Template
```yaml
---
name: skill-name
description: Third-person description under 1024 chars. Triggers on keywords: keyword1, keyword2
project-agnostic: true
allowed-tools:
  - Read
  - Glob
---
```

### Directory Structure
```
.claude/skills/skill-name/
  SKILL.md           # Required
  supporting.md      # Optional, one level only
```

### Tool Permission Matrix

| Task Type | Required Tools |
|-----------|----------------|
| Read/analyze | Read, Glob |
| Search content | Read, Glob, Grep |
| Write docs | Read, Write, Glob |
| Edit files | Read, Edit, Glob |
| Run commands | Bash, Read |

## Supporting Files

- `templates/skill-template.md` - Comprehensive skill template
- `cookbook/validation.md` - Validation checklist and scripts
- `cookbook/patterns.md` - Common skill patterns with examples
- `cookbook/anti-patterns.md` - What NOT to do
