---
name: asset-validation
description: Validate Codex AI assets such as AGENTS.md files, Codex skills, templates, checklists, and support scripts. Use after creating or modifying the repository's Codex component package.
user-invocable: false
---

# Asset Validation

Validate Codex-native AI assets before considering the package complete.

## Scope

Validate:

- Root or scoped `AGENTS.md`
- `.agents/skills/*/SKILL.md`
- Companion markdown resources for skills
- `.codex/templates/*`
- `.codex/checklists/*`
- explicit support scripts used by the Codex package

Do not use this skill for application linting, unit tests, or runtime deployment checks.

## Validation Layers

### 1. Structure

Confirm:

- The asset is stored in the correct directory
- `SKILL.md` lives under `.agents/skills/<skill-name>/`
- Companion resources are colocated with their skill or under `.codex/`
- The package does not introduce unsupported runtime assumptions

### 2. Content Rules

Confirm:

- English only
- No secrets or credentials
- No broken references
- No Claude-only runtime instructions
- Instructions are concrete and scoped

### 3. Frontmatter

For `SKILL.md`:

- `name` present
- `description` present and specific
- Any optional fields are valid and necessary

For `AGENTS.md`, templates, and checklists:

- No YAML frontmatter unless there is a clear reason

### 4. Dependency Integrity

Check:

- References to `AGENTS.md`
- References to `.agents/skills/<name>/`
- References to `.codex/templates/` and `.codex/checklists/`
- References to local scripts

Flag missing targets and orphaned assets that no workflow will discover.

### 5. Token Discipline

Check:

- `SKILL.md` files are concise enough for progressive disclosure
- `AGENTS.md` files do not bury critical policy in long prose
- Reference material is moved out of hot-path assets when appropriate

## Report Format

Return:

- Summary
- Passed checks
- Findings
- Required follow-up

Use `validation-checklist.md` for the detailed checklist and script patterns.
