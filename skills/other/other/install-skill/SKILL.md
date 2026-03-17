---
name: install-skill
description: Install skills from ../skills into a target project via local ../hooks CLI,
including pre-publish local-path workflows after make-skill changes.
Use when: (1) a new or renamed skill was added in ../skills, (2) hooks packages
changed locally and are not published yet, (3) you need deterministic installation
for both Claude Code and Codex with no stale npm dependency assumptions.

category: meta
user-invocable: true
---

# Install Skill

Install skills using local repos (`../skills` + `../hooks`) first. Do not require npm publish.

## Primary Flow

1. Ensure target skill exists under `../skills/<skill-name>/SKILL.md`.
2. If hooks contracts changed, rebuild local packages:
```bash
cd ../hooks
npm run build -w @4meta5/skill-loader
npm run build -w @4meta5/skills
npm run build -w @4meta5/skills-cli
```
3. Install into target project from local source:
```bash
cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js add <skill-name> --cwd /absolute/path/to/project
```
4. Sync project skill references:
```bash
cd /absolute/path/to/project
node ../skillex/packages/skills-cli/bin/skills.js claudemd sync
```

## Dual Runtime Requirement (Claude + Codex)

The install is not complete until both runtimes are covered:

1. Claude Code path:
- `.claude/skills/<skill-name>/SKILL.md` exists
- `CLAUDE.md` contains `- @.claude/skills/<skill-name>/SKILL.md`
- `.claude/hooks/skill-forced-eval.sh` exists and points to local CLI fallback when available

2. Codex path:
- `AGENTS.md` must expose the same installed skill references.
- Preferred pattern: `AGENTS.md` symlink to `CLAUDE.md`.
- If symlink is not used, keep `AGENTS.md` skill refs in lockstep with `CLAUDE.md`.

Verification commands:
```bash
cd /absolute/path/to/project
ls -l AGENTS.md
rg -n "@.claude/skills/.*/SKILL.md" CLAUDE.md AGENTS.md
```

## Hard-Cut Rename Install

If skill names were renamed, do not keep aliases.
1. Install new name.
2. Remove old name from project:
```bash
cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js remove <old-skill-name> --cwd /absolute/path/to/project
```
3. Run `node ../skillex/packages/skills-cli/bin/skills.js claudemd sync --cwd /absolute/path/to/project`.
4. Re-check `AGENTS.md` mirrors updated references.

## Replace Set Workflow

When user requests a strict target set (replace stale installs completely):

```bash
# 1) remove everything not in target set
cd /absolute/path/to/project
ls .claude/skills
# remove non-target skills explicitly via skills.js remove

# 2) install target set from local skills repo
cd ../skills
node ../skillex/packages/skills-cli/bin/skills.js add <skill-a> <skill-b> ... --cwd /absolute/path/to/project

# 3) sync docs and verify both runtimes
node ../skillex/packages/skills-cli/bin/skills.js claudemd sync --cwd /absolute/path/to/project
cd /absolute/path/to/project
rg -n "@.claude/skills/.*/SKILL.md" CLAUDE.md AGENTS.md
```

## Safety Guardrails For Bulk Cleanup

Before removing skills from `.claude/skills`:
1. Never treat dot-prefixed entries as skills (`.git`, `.claude`, `.scout`, etc.).
2. If `.claude/skills` is a symlink, resolve it and verify it points to a dedicated skills directory.
3. Only remove names that:
- are in a known stale-name list, or
- are installed skill directories with a valid `SKILL.md`.
4. After cleanup, verify repository metadata still exists (`.git` present) and rerun `skills list`.

## Auto-Maintenance

After any incident, update this skill and `../make-skill` with:
1. Symptom
2. Root cause
3. Detection command
4. Minimal fix command

When invoked, always prefer local-path installation before recommending npm-published binaries.
