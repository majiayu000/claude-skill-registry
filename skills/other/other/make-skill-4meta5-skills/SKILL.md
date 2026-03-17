---
name: make-skill
description: Create, update, or edit skills in this repository using the canonical taxonomy.
Use when: (1) adding a new skill, (2) renaming or recategorizing a skill,
(3) updating skill metadata/docs to match hooks validation contracts,
(4) editing any existing skill's SKILL.md content.

category: meta
user-invocable: true
---

# Make Skill

Create, update, or edit skills with strict consistency across `../skills` and `../hooks`.

## Flat Path Convention (Hard Rule)

Skills live flat at the repo root: `<skill-name>/SKILL.md`. The `.claude/skills` directory is a symlink to `..` (the repo root). Always edit via the flat canonical path:

- Correct: `wip/SKILL.md`, `make-skill/SKILL.md`
- Wrong: `.claude/skills/wip/SKILL.md`, `.claude/skills/make-skill/SKILL.md`

Both resolve to the same file, but the flat path is the source of truth. Never use the symlink path in edits or references.

## Canonical Taxonomy (Hard-Cut)

Only these categories are valid and supported:
- `meta`
- `audit`
- `principles`
- `habits`
- `hot`

Do not introduce any additional categories.

## Naming Rules

- Skill folder name must match frontmatter `name`.
- Use lowercase kebab-case.
- Renames are hard-cut (no aliases unless explicitly requested).

## Minimal Workflow

1. Create/update `<skill-name>/SKILL.md`.
2. Set frontmatter fields: `name`, `description`, optional `category`, optional `user-invocable`.
3. Add/update `agents/openai.yaml` so `default_prompt` references `$<skill-name>`.
4. **Update `CLAUDE.md`** (mandatory, do not skip):
   - Add the skill name under the correct category in the `## Skills` section.
   - Add `- @.claude/skills/<skill-name>/SKILL.md` to the `## Installed Skills` section.
   - Maintain alphabetical order within each section.
5. **Update `README.md`** (mandatory, do not skip):
   - Add the skill to the `## All Skills` table in the correct category group, alphabetical within group.
   - Update the count on line 1 (e.g., "24 curated" to "25 curated").
6. **Run count check** (mandatory, do not skip):
```bash
./scripts/check-skill-count.sh
```
   All counts must pass. If any fail, fix before proceeding.
7. **Verify `AGENTS.md`** mirrors `CLAUDE.md`. If `AGENTS.md` is a symlink to `CLAUDE.md`, this is automatic. If not, update it manually to match.
8. Validate with local hooks CLI:
```bash
cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js validate <skill-name>
```

## Cross-Repo Contract (Required)

If you change naming/category rules, update all of:
1. `../hooks/packages/skill-loader/src/types.ts`
2. `../hooks/packages/skills/src/types.ts`
3. `../hooks/packages/cli/src/detector/types.ts`
4. Related docs in `../hooks/packages/*/README.md`

## Mandatory Post-Change Local Sync

After any skill creation/rename/category change, run this exact flow before handoff:

```bash
cd ../hooks
npm run build -w @4meta5/skill-loader
npm run build -w @4meta5/skills
npm run build -w @4meta5/skills-cli

cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js validate <skill-name>
node ../skillex/packages/skills-cli/bin/skills.js sync <skill-name> --push
```

If target projects need immediate refresh without publish, run:
```bash
cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js add <skill-name> --cwd /absolute/path/to/project
node ../skillex/packages/skills-cli/bin/skills.js claudemd sync --cwd /absolute/path/to/project
```

## Handoff to Install Skill

After creation, use `$install-skill` flow to install into target projects via local paths, not npm publish.

## Auto-Maintenance

Whenever an install/validation incident happens, update this skill with:
1. Symptom
2. Root cause
3. Detection command
4. Minimal fix

### Incident: Editing via symlink path instead of flat path (2026-02-15)

1. **Symptom**: Agent edited `.claude/skills/wip/SKILL.md` instead of `wip/SKILL.md`.
2. **Root cause**: Agent was unaware that `.claude/skills` is a symlink to `..` and that the flat path is canonical.
3. **Detection**: `ls -la .claude/skills` shows the symlink. Check edit paths in agent output.
4. **Fix**: Added "Flat Path Convention" section to this skill and "Repo Layout" section to `CLAUDE.md`. Always use `<skill-name>/SKILL.md`, never `.claude/skills/<skill-name>/SKILL.md`.

### Incident: README count and table out of sync after adding skills (2026-02-16)

1. **Symptom**: README said "23 curated" but 24 skills existed on disk. `script-agents` was missing from the README table.
2. **Root cause**: make-skill workflow did not include README update or count validation as mandatory steps.
3. **Detection**: `./scripts/check-skill-count.sh`
4. **Fix**: Added steps 5 (update README) and 6 (run count check) to Minimal Workflow. Created `scripts/check-skill-count.sh` to validate disk, README, and CLAUDE.md stay in sync.