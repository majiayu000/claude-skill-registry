---
name: openskills-skill-authoring
description: Create and refine OpenSkills-compatible skills (SKILL.md + optional resources) with strong metadata, clear activation triggers, and reliable execution guidance.
---

# OpenSkills Skill Authoring

Use this skill when creating or updating skills under `examples/skills` or any OpenSkills-compatible skill directory.

## Authoring Standard

Each skill directory should include:

- `SKILL.md` (required)
- optional `scripts/`, `references/`, `assets/`

## SKILL.md Requirements

- YAML frontmatter with:
  - `name`
  - `description`
- Body with concise instructions and practical execution flow.
- Description must include both:
  - what the skill does
  - when to activate it

## Writing Guidance

1. Keep core instructions short; move details to `references/`.
2. Prefer deterministic scripts for fragile or repetitive steps.
3. Include explicit input/output expectations.
4. Avoid vague names and ambiguous activation phrases.

## Validation Flow

1. Ensure directory name matches skill `name` semantics.
2. Verify skill discovery and activation behavior in runtime or example agent.
3. If scripts are present, verify paths and execution assumptions.

## Output Format

- Skill metadata quality review
- Instruction clarity review
- Activation trigger quality review
- Suggested revisions
