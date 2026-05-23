---
name: k-create-skill
description: >
  Meta knowledge for creating Claude skills. Provides templates, best practices,
  and patterns for building effective skills with routing tables and reference
  files. Load this when creating new skills or understanding the skill system.
  Triggers: create skill, new skill, skill template, skill architecture, SKILL.md.
---

# Creating Claude Skills

Knowledge for creating and maintaining Claude commands and skills.

## Mechanic Skill System

This project uses a three-prefix taxonomy:

| Prefix | Type | Purpose |
|--------|------|---------|
| `c-` | Commands | Action workflows with explicit steps |
| `s-` | Skills | How-to knowledge (paired with commands) |
| `k-` | Knowledge | Context/background (no command needed) |

See [../../AGENTS.md](../../AGENTS.md) for full system documentation.

## Creating a New Action

To add a new action (e.g., "deploy"):

1. Create `commands/c-deploy.md` with explicit steps
2. Create `skills/s-deploy/SKILL.md` with detailed guidance
3. Add bidirectional links between them

## Creating New Knowledge

To add new context (e.g., "blizzard-api"):

1. Create `skills/k-blizzard-api/SKILL.md`
2. No command needed - the skill IS the context loader

## Skill Structure

```
skills/[skill-name]/
├── SKILL.md              # Required: Main skill file
└── references/           # Optional: Supporting documents
    ├── topic1.md
    └── topic2.md
```

## SKILL.md Format

```markdown
---
name: [prefix]-[name]
description: >
  [What this skill does]. [What content it covers].
  Use when [scenarios]. Triggers: [keyword1], [keyword2], [keyword3].
---

# [Title]

[One-line description]

## Related Commands (for s-* skills only)

- [c-X](../../commands/c-X.md) - [description]

## Capabilities / Key Concepts

1. **[Item 1]** — [Brief description]
2. **[Item 2]** — [Brief description]

## Routing Logic (optional)

| Request type | Load reference |
|--------------|----------------|
| [Topic] | [references/file.md](references/file.md) |
```

## Core Principles

### 1. Progressive Loading

Skills load in stages:
- **Stage 1:** Name + description (always loaded)
- **Stage 2:** SKILL.md body (when skill is relevant)
- **Stage 3:** References (only when explicitly needed)

Design for minimal initial context, deep references.

### 2. Clear Triggers

Description should include trigger words that help Claude know when to use this skill.

### 3. Self-Contained References

Each reference file should be independently useful without requiring other files.

### 4. Actionable Content

Focus on rules, patterns, and examples—not background explanation.

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Skill file format | [references/format.md](references/format.md) |
| Routing tables | [references/routing.md](references/routing.md) |
| Description writing | [references/descriptions.md](references/descriptions.md) |
| Reference file design | [references/reference-files.md](references/reference-files.md) |
| Skill architecture | [references/architecture.md](references/architecture.md) |
