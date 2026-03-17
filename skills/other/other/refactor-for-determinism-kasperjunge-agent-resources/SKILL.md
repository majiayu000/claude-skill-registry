---
name: refactor-for-determinism
description: Design or refactor skills by separating deterministic and non-deterministic steps. Use when creating or improving skills, especially to move repeatable workflows into scripts/ and update SKILL.md to call them.
---

# Refactor for Determinism

Build reliable skills by separating deterministic steps from judgment-based steps.

## Core Principle

**Deterministic steps belong in scripts.** Use SKILL.md to orchestrate the workflow and reserve judgment for the non-deterministic parts.

## Workflow

### 1. Identify Deterministic vs Non-Deterministic Work

For each step in the skill:
- **Deterministic**: repeatable, mechanical, or validation-heavy steps → script candidates
- **Non-deterministic**: judgment, interpretation, creative choices → keep in SKILL.md

Examples of deterministic steps:
- Running quality checks
- Verifying clean git state
- Updating version strings
- Promoting CHANGELOG sections
- Collecting diff context for review

Examples of non-deterministic steps:
- Writing changelog content
- Selecting a solution approach
- Code review judgments
- Deciding release timing

### 2. Design Scripts for Deterministic Steps

For each deterministic step:
- Create a script in `scripts/` within the skill directory
- Make it self-contained with clear error messages
- Validate inputs and exit non-zero on failure
- Prefer small, single-purpose scripts

### 3. Update SKILL.md to Use Scripts

- Replace manual command lists with script calls
- Reference scripts using relative paths: `scripts/...`
- Keep judgment steps explicit in prose

### 4. Document Boundaries

Make the line between scripted and non-scripted steps obvious:
- Use section headers like "Deterministic Steps" and "Judgment Steps"
- Call out where human/agent judgment is required

## Output Format

```
## Determinism Audit

### Deterministic Steps (script candidates)
- [Step] → [script name]

### Non-Deterministic Steps (keep in SKILL.md)
- [Step] → [why it needs judgment]

### Script Plan
- scripts/[name] - [purpose, inputs, outputs]

### SKILL.md Updates
- [Where to call each script]
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Scripting judgment | Keep decision-making in SKILL.md |
| One giant script | Split into small, focused scripts |
| Silent failures | Print clear errors and exit non-zero |
| Hardcoded paths | Use repo-relative paths |
| Forgetting SKILL.md updates | Always wire scripts into instructions |

## What NOT to Do

- Do NOT hide decisions inside scripts
- Do NOT make scripts that require manual editing
- Do NOT mix multiple responsibilities into one script
- Do NOT add extra documentation files beyond SKILL.md
