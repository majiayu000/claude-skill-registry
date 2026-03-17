---
name: mcaf-skill-curation
description: "Create, update, and validate repository skills under your agent’s skills directory (Codex: `.codex/skills/`, Claude: `.claude/skills/`) so they match the real codebase and `AGENTS.md` rules; tune YAML `description` triggers, apply feedback, and generate `<available_skills>` metadata blocks."
compatibility: "Requires repository write access; uses a shell and Python 3 for validation/scripts."
---

# MCAF: Skill Curation

## Outputs

- New/updated skill folders under your agent’s skills directory with valid `SKILL.md` frontmatter and lean workflows
- Updated YAML `description` triggers for correct matching
- A generated `<available_skills>` block (metadata only) for your agent runtime
- A validation report (script output)

## Workflow

1. Read the repo’s sources of truth:
   - `AGENTS.md` (commands + hard rules)
   - `docs/Architecture/Overview.md` (modules/boundaries) if present
2. Inventory skills and identify drift:
   - list all `*/SKILL.md` under your skills directory (Codex: `.codex/skills/*/SKILL.md`, Claude Code: `.claude/skills/*/SKILL.md`)
   - verify folder name == YAML `name`
   - look for “template cruft” inside skill folders (README/INSTALL/CHANGELOG) and remove it
3. Update skills to match reality (no guessing):
   - ensure each skill references **real** commands (from `AGENTS.md`)
   - ensure each skill’s YAML `description` includes trigger keywords that match how users ask for the task
   - ensure workflows reference real modules/boundaries (from architecture overview)
4. Create new skills for repeated/fragile workflows:
   - keep one workflow per skill (split mega-skills)
   - copy the closest existing skill and adapt (folder/name, triggers, outputs, workflow)
   - use `scripts/` for deterministic or fragile steps
   - use `references/` only for copy/paste templates and structured checklists (avoid “reading lists”)
5. Validate skills (fix errors before shipping):
   - run the bundled validator from the repo root:
     - `python3 <skills-dir>/mcaf-skill-curation/scripts/validate_skills.py <skills-dir>`
     - Codex: `python3 .codex/skills/mcaf-skill-curation/scripts/validate_skills.py .codex/skills`
     - Claude: `python3 .claude/skills/mcaf-skill-curation/scripts/validate_skills.py .claude/skills`
6. Generate a metadata-only skills block for your agent runtime:
   - run the bundled generator from the repo root:
     - `python3 <skills-dir>/mcaf-skill-curation/scripts/generate_available_skills.py <skills-dir> --absolute`
     - Codex: `python3 .codex/skills/mcaf-skill-curation/scripts/generate_available_skills.py .codex/skills --absolute`
     - Claude: `python3 .claude/skills/mcaf-skill-curation/scripts/generate_available_skills.py .claude/skills --absolute`
   - paste the output into your agent configuration (system/developer prompt)
7. When user feedback is about skills:
   - update the relevant `<skills-dir>/<skill-name>/SKILL.md` (especially YAML `description` triggers) so the fix is permanent

## Bundled scripts

- `scripts/validate_skills.py` — validates frontmatter + folder/name rules and flags common spec violations.
- `scripts/generate_available_skills.py` — prints an `<available_skills>` XML block from your skills directory `*/SKILL.md` metadata.

## Guardrails

- Don’t turn a skill into a wiki: keep `SKILL.md` procedural and short.
- Don’t add extra docs inside skill folders (`README.md`, `INSTALLATION_GUIDE.md`, `CHANGELOG.md`, etc.).
- Prefer updating triggers (`description`) over adding more and more body text.
- YAML is strict: if a value contains `:` or other YAML-significant characters, wrap it in quotes.

## Examples (trigger phrases)

- "update our skills to match the repo"
- "this skill triggers wrong, fix the description"
- "generate available_skills block"
- "validate skills frontmatter"
