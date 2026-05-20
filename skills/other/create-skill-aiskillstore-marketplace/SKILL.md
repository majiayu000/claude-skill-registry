---
name: create-skill
description: Guide for creating new Agent Skills. Use this skill when you need to create a new skill.
---

# Create Skill

## Skill Structure
```
skill-name/
├── SKILL.md          # instructions + metadata
├── scripts/          # executable code (optional)
├── references/       # documentation (optional)
└── assets/           # templates/resources (optional)
```

## Requirements
- **Frontmatter**: Must include `name` (lowercase-alphanumeric) and `description`.
- **Description**: Must include **what** it does and **when** to use it.
- **Body**: Keep under 500 lines. Use imperative language. 
- **Resources**: Move detailed docs to `references/` and code to `scripts/`.

## Process
1. **Directory**: `mkdir <name>`. Create `scripts/`, `references/`, or `assets/` only if you actually have content for them.
2. **Metadata**: Write the `SKILL.md` frontmatter first.
3. **Resources**: Implement scripts and test them.
4. **Instructions**: Write concise steps in `SKILL.md` body.
5. **Verify**: Ensure frontmatter name matches directory name.

## References
- [Full Specification](references/specification.md)
- [Design Patterns](references/what-are-skills.md)