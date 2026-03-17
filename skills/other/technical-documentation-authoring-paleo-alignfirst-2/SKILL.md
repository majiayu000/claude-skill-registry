---
name: technical-documentation-authoring
description: Create or augment technical documentation. Use when writing new skills, updating existing skills. Also use when modifying project documentation like AGENTS.md.
license: CC0 1.0
metadata:
  author: Paleo
  version: "1.0"
  repository: https://github.com/paleo/alignfirst
---

# Technical Documentation Authoring

## References

- [Agent Skills specification](https://agentskills.io/specification.md)
- [Bootstrapping Skills](references/bootstrapping-skills.md) — infer project-specific skills from codebase analysis

## Workflow

### 0. Bootstrapping (Optional)

If the user asks to **bootstrap** skills by analyzing the codebase (rather than requesting a specific skill), then read _Bootstrapping Skills_ first. This applies even if reusable skills already exist; the goal is to create project-specific documentation.

### 1. Understand the Subject

Clarify what needs to be documented. Ask the user if unclear.

### 2. Determine the Target

**For agent skill documentation:**

1. Scan existing skills' `description` fields for keyword matches
2. If a potential match exists, read that skill's content to confirm suitability
3. Decision:
   - User requested a specific skill AND it's suitable → proceed
   - User requested a new skill AND no suitable skill exists → create it
   - Otherwise → discuss with user before proceeding

**For general documentation** (`AGENTS.md`, README, etc.): proceed directly.

### 3. Determine Placement (Skills Only)

- **SKILL.md**: Essential content required to use the skill
- **references/**: Optional detailed content that can be skipped

### 4. Write the Documentation

Follow the guidelines below.

## Creating a New Skill

```
{skills-dir}/skill-name/
└── SKILL.md           # Required
```

Frontmatter:

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

The `name` must match the directory name. Use lowercase with hyphens.

## Writing Guidelines

**Target audience**: An experienced newcomer.

- Be brief and specific
- No obvious information, no generic best practices
- Clear title, specific purpose
- New documents: 40–80 lines typical
- `SKILL.md`: under 500 lines
- Keep code snippets small; reference source files for full examples
