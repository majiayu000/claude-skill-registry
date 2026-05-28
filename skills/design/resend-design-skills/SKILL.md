---
name: resend-design-skills
description: Use when needing Resend design resources. Routes to brand guidelines, visual identity, and other design sub-skills.
metadata:
    author: resend
    version: "1.0.0"
---

# Design Skills

A collection of design-related skills for Claude Code.

## Available Skills

| Skill | Description | Path |
|-------|-------------|------|
| `resend-brand` | Applies Resend's brand colors, typography, and visual identity to artifacts | [brand-guidelines/SKILL.md](brand-guidelines/SKILL.md) |

## Structure

Each skill lives in its own folder with a `SKILL.md` file that defines:
- Frontmatter with `name` and `description`
- Guidelines, rules, and reference material

```
design-skills/
├── SKILL.md              # This index file
├── brand-guidelines/
│   └── SKILL.md          # Resend brand skill
```
