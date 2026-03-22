---
name: project-skill-creator
description: Creates project-managed skills in .chalk/skills with safe naming, ownership metadata, and versioned frontmatter.
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write
argument-hint: "[skill name, purpose, optional triggers/examples]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: skills, scaffolding, meta
capabilities: skills.project.create, skills.scaffold
activation-intents: create project skill, add local skill, scaffold skill
activation-events: user-prompt
activation-artifacts: .chalk/skills/**
risk-level: medium
---

# Project Skill Creator

Create project-managed skills in `.chalk/skills` without conflicting with Chalk-managed skills.

## Workflow

1. Ask the user for:
   - skill name
   - purpose/description
   - optional triggers/examples
2. Normalize the provided skill name to kebab-case:
   - lowercase
   - replace spaces/underscores with `-`
   - remove characters outside `a-z`, `0-9`, and `-`
   - collapse repeated `-`
   - trim leading/trailing `-`
3. Reject the normalized name if it starts with `chalk-`.
4. Ensure `.chalk/skills` exists.
5. Check for collisions:
   - If `.chalk/skills/<normalized-name>/` already exists, do not overwrite.
   - Ask for explicit confirmation before any replace behavior.
   - Default behavior is create-only.
6. Create folder `.chalk/skills/<normalized-name>/`.
7. Create `.chalk/skills/<normalized-name>/SKILL.md` with frontmatter:

   ```yaml
   ---
   name: <normalized-name>
   description: <purpose/description>
   owner: project
   version: "1.0.0"
   metadata-version: "2"
   ---
   ```

8. Add these markdown sections to the generated skill file:
   - `# <Skill Name>`
   - `## Purpose`
   - `## Workflow`
   - `## Inputs`
   - `## Output`
   - `## Guardrails`
9. In `## Purpose`, include the user-provided purpose/description.
10. If provided, include user triggers/examples in the generated skill (typically under `## Inputs` or `## Workflow`).
11. Confirm the created path and summarize what was generated.

## Inputs

- Required: skill name, purpose/description
- Optional: triggers/examples

## Output

- New project skill folder at `.chalk/skills/<normalized-name>/`
- New skill definition file at `.chalk/skills/<normalized-name>/SKILL.md`
- Confirmation message including normalized name, created paths, and included sections

## Guardrails

- Never modify existing Chalk-managed skills.
- Never modify skills named with `chalk-*` prefix.
- Never overwrite existing project skill folders unless user explicitly confirms replace.
- Default to create-only behavior.
- If validation fails (invalid or reserved name), stop and request a new name.
