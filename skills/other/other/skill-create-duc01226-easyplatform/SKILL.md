---
name: skill-create
version: 2.0.0
description: '[Skill Management] Create new Claude Code skills or scan/fix invalid skill headers. Triggers on: create skill, new skill, skill schema, scan skills, fix skills, invalid skill, validate skills, skill header.'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Create new Claude Code skills with proper structure or scan/fix invalid skill headers across the catalog.

**Workflow:**

1. **Clarify** — Gather purpose, trigger keywords, tools needed via AskUserQuestion
2. **Check Existing** — Glob for similar skills, avoid duplication
3. **Scaffold** — Create directory + SKILL.md with frontmatter + Quick Summary
4. **Validate** — Run frontmatter + header validation

**Key Rules:**

- Every SKILL.md MUST include `## Quick Summary` (Goal/Workflow/Key Rules) within first 30 lines
- Single-line `description` with `[Category]` prefix and trigger keywords
- SKILL.md under 500 lines; use `references/` for detail
- Always break work into small todo tasks; always add final self-review task

## Modes

| Mode | Trigger | Action |
|------|---------|--------|
| **Create** | `$ARGUMENTS` describes a new skill | Create skill following workflow below |
| **Scan & Fix** | `$ARGUMENTS` mentions scan, fix, validate, invalid | Run validation across all skills |

## Prerequisites

- **MUST READ** `references/claude-skill-schema.md` — Official Claude Code SKILL.md schema

## Mode 1: Create Skill

### Workflow

1. **Clarify** — If requirements unclear, use `AskUserQuestion` for: purpose, auto vs user-invoked, trigger keywords, tools needed
2. **Check Existing** — Glob `.claude/skills/*/SKILL.md` for similar skills. Avoid duplication.
3. **Create Directory** — `.claude/skills/{skill-name}/SKILL.md`
4. **Write Frontmatter** — Follow schema from `references/claude-skill-schema.md`
5. **Write Instructions** — Concise, actionable, progressive disclosure
6. **Add References** — Move detailed docs to `references/` directory if content >200 lines
7. **Add Scripts** — Create `scripts/` for executable helpers if needed
8. **Validate** — Run frontmatter validation (see Mode 2 single-file check)

### Frontmatter Template

```yaml
---
name: {kebab-case-name}
description: '[Category] What it does. Triggers on: keyword1, keyword2.'
---
```

**Official fields:** `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`

**Project conventions (non-official but used here):** `activation: user-invoked`, `version: X.Y.Z`

### Rules

- SKILL.md is instructions, not documentation. Teach Claude HOW to do the task.
- Single-line `description` (multi-line YAML breaks catalog parsing)
- Description must include trigger keywords for auto-activation
- Use `[Category]` prefix in description (e.g., `[Frontend]`, `[Planning]`, `[AI & Tools]`)
- Keep SKILL.md under 500 lines; use `references/` for detail
- Progressive disclosure: frontmatter → SKILL.md summary → reference files
- Token efficiency: every line must earn its place
- No URLs without context — explain what the link provides
- Use `researcher` subagent if topic needs research
- Use `Explore` subagent for URLs/repos (parallel for multiple sources)
- Use `repomix` for GitHub repos

## Mode 2: Scan & Fix Invalid Skills

### What It Validates

| Check | Rule | Severity |
|-------|------|----------|
| Frontmatter exists | Must have `---` delimiters | Error |
| Description single-line | No literal newlines in description value | Error |
| Description not empty | Must have description for discoverability | Warning |
| Name format | Lowercase, hyphens, max 64 chars | Error |
| No unknown official fields | Flag fields not in official schema | Info |
| Description has category | Should start with `[Category]` | Warning |
| File size | SKILL.md should be <500 lines | Warning |
| Quick Summary exists | Must have `## Quick Summary` in first 30 lines | Warning |

### Scan Workflow

1. **Discover** — Glob `.claude/skills/*/SKILL.md` for all skills
2. **Parse** — Read first 20 lines of each file, extract frontmatter
3. **Validate** — Check each rule above
4. **Report** — List issues grouped by severity (Error > Warning > Info)
5. **Fix** — If user confirms, fix Error-level issues automatically:
   - Missing frontmatter → add minimal `---\nname: {dir-name}\ndescription: ''\n---`
   - Multi-line description → collapse to single line
   - Invalid name → suggest kebab-case fix

### Validate Script

```bash
# Report only
node .claude/skills/skill-create/scripts/validate-skills.cjs

# Report + auto-fix (removes invalid fields, renames typos)
node .claude/skills/skill-create/scripts/validate-skills.cjs --fix

# Scan specific directory
node .claude/skills/skill-create/scripts/validate-skills.cjs --path .claude/skills/my-skill
```

## Requirements

<user-prompt>$ARGUMENTS</user-prompt>

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
