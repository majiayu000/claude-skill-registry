---
name: asset-validation
description: Validate Windsurf AI assets such as AGENTS.md files, Windsurf skills, templates, checklists, and support scripts. Use after creating or modifying the repository's Windsurf component package.
---

# Asset Validation

Validate Windsurf-native AI assets before considering the package complete.

## Scope

Validate:

- Root or scoped `AGENTS.md`
- `.windsurf/skills/*/SKILL.md`
- Companion markdown resources for skills
- shared template resources under `.windsurf/skills/ai-assets/templates/*`
- shared checklists under `.windsurf/skills/ai-assets/checklists/*`
- explicit support scripts used by the Windsurf package, including `.windsurf/hooks/scripts/*`

Do not use this skill for application linting, unit tests, or runtime deployment checks.

## Validation Layers

### 1. Structure

Confirm:

- The asset is stored in the correct directory
- `SKILL.md` lives under `.windsurf/skills/<skill-name>/`
- Companion resources are colocated with their skill or stored in a documented shared resource folder
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
- References to `.windsurf/skills/<name>/`
- References to shared templates and checklists under `.windsurf/skills/ai-assets/`
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
