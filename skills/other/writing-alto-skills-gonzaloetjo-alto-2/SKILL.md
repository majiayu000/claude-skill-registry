---
name: writing-alto-skills
description: Use when creating or editing ALTO skills (skills/*/SKILL.md) or agents (agents/*.md). Guide for skill structure, frontmatter format, and content organization.
---

# Writing ALTO Skills

## Frontmatter (Required)

```yaml
---
name: skill-name
description: Use when [triggering conditions]. [What the skill does].
---
```

| Field | Constraints |
|-------|-------------|
| `name` | Letters, numbers, hyphens. Max 64 chars. |
| `description` | Start with "Use when...". Max 1024 chars. |

## Description Examples

```yaml
# Specific triggering conditions
description: Use when testing ALTO protocol and finding issues. Run protocol tests, analyze artifacts.

# File-based triggers
description: Use when creating or editing ALTO skills (skills/*/SKILL.md) or agents (agents/*.md).
```

## Content Guidelines

1. **Start with key action** - What should agent do first?
2. **Numbered steps** for procedures
3. **Tables** for reference data
4. **Code blocks** for commands/examples
5. **Bullets over paragraphs** - Keep prose minimal

**Word limit:** 500 words (excludes code blocks). Validator warns above this.

## Validate Before Commit

```bash
devenv shell -- alto-validate
```

**Reference:** [superpowers/writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)
