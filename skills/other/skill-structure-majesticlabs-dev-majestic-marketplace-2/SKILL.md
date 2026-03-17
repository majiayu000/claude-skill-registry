---
name: skill-structure
description: Skill file structure, naming conventions, directory layout, and frontmatter requirements. Use when creating skill files to ensure correct format and validation.
---

# Skill Structure

## Naming Rules

| Rule | Example |
|------|---------|
| Format | `kebab-case`, lowercase, 1-64 chars |
| Pattern | `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| Must match | Directory name exactly |

**Good/Bad Examples:**

| Good | Bad | Why |
|------|-----|-----|
| `stimulus-coder` | `MySkill` | Uppercase not allowed |
| `tdd-workflow` | `skill_helper` | Underscores not allowed |
| `pdf-processing` | `-invalid` | Can't start with hyphen |
| `seo-content` | `skill--bad` | No consecutive hyphens |

## Directory Structure

### Flat Structure (most skills)

```
plugins/majestic-rails/skills/stimulus-coder/SKILL.md
→ name: stimulus-coder
→ invoked as: /majestic-rails:stimulus-coder
```

### Nested Structure (categorized skills)

```
plugins/majestic-company/skills/ceo/strategic-planning/SKILL.md
→ name: strategic-planning
→ invoked as: /majestic-company:ceo:strategic-planning
```

**Key Points:**
- The `name` field is ONLY the final skill name (not the full path)
- Directory name must match `name` exactly
- Use nesting to group related skills (ceo/, fundraising/, research/)

## Progressive Disclosure

For complex skills, split into multiple files:

```
my-skill/
├── SKILL.md (overview, <500 lines)
├── references/
│   ├── patterns.md (detailed patterns)
│   └── examples.md (extended examples)
└── scripts/
    └── helper.py (utility scripts)
```

**Rules:**
- References one level deep only (SKILL.md to reference.md, not deeper)
- Scripts execute without loading into context
- Keep SKILL.md focused on navigation and core content
- Subdirectories only: `scripts/`, `references/`, `assets/`

## Frontmatter

```yaml
---
name: skill-name              # Required, matches directory
description: What it does...  # Required, max 1024 chars
allowed-tools: Read, Bash     # Optional, space-delimited
---
```

### Description Template

```
[What it does]. Use when [trigger contexts]. Triggers on [specific keywords].
```

**Example:**
```yaml
description: Best practices for writing Stimulus controllers in Rails applications. Use when creating JavaScript controllers, handling DOM events, or adding interactivity. Triggers on Stimulus, controllers, data-action, data-target.
```

**Rules:**
- Max 1024 characters
- Third person ("Processes..." not "I process...")
- Include trigger keywords users would naturally say

## Tool Access

| Tools Needed | Example Use Case |
|--------------|------------------|
| `Read, Grep, Glob` | Search codebase for patterns |
| `Bash(python:*)` | Execute Python scripts |
| `WebFetch` | Fetch external documentation |
| None | Pure knowledge/guidance |

## Limits

- **SKILL.md:** Max 500 lines
- **Name:** Max 64 characters
- **Description:** Max 1024 characters

## Validation Checklist

- [ ] Name matches directory name exactly
- [ ] Name follows pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`
- [ ] Description under 1024 chars with trigger keywords
- [ ] SKILL.md under 500 lines
- [ ] No persona statements or attribution
- [ ] Subdirectories only: `scripts/`, `references/`, `assets/`
