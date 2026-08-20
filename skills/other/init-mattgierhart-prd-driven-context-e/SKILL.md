---
name: init
description: >
  Seed a fresh (greenfield) repository with the PRD-Driven Context Engineering scaffold —
  PRD.md, SoT/ knowledge files, EPIC templates, domain-profile config, and agent MEMORY
  starters. Invoked as /prd-ce:init when the plugin is installed. The framework itself
  (skills, agents, hooks, scripts) ships LIVE in the plugin; this skill only plants the
  consumer-owned files the plugin cannot carry as behavior. Triggers on "/prd-ce:init",
  "set up PRD lifecycle here", "scaffold a new PRD-CE project", "initialize the methodology".
  Outputs a seeded scaffold + a verification report.
disable-model-invocation: true
execution_modes:
  default: standard
  supports: [quick, standard, deep]
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /prd-ce:init — Greenfield Scaffold Seeder

Plant the consumer-owned scaffold for a fresh PRD-CE project. The methodology engine
(lifecycle skills, the agent squad, governance hooks, `readiness.py`) is delivered **live**
by the installed `prd-ce` plugin — it never gets copied into your repo. This skill seeds only
what is yours to own and edit: `PRD.md`, the `SoT/` graph, `epics/` templates, your
`.claude/domain-profile.yaml`, and per-agent `MEMORY.md` starters.

> **One manifest, no drift.** The seed list comes from `install-manifest.yaml`'s
> `template_seed` section — the same list `install.sh` (fork path) and `ghm-template-sync`
> (update path) read. This skill drives the deterministic `prd-ce-init.sh` so behavior is
> identical no matter who invokes it.

> **Scope (v1): greenfield only.** This seeds an *empty* structure into a fresh repo.
> Mid-build and live-codebase on-ramps (entry-mode branching, graph extraction) are
> backlogged — see `temp/plugin-conversion-plan.md`. If the target already has `PRD.md` or
> `SoT/` content, the seeder keeps it (non-destructive) rather than adapting to it.

## Consumes

- `${CLAUDE_PLUGIN_ROOT}/templates/` — the bundled seed sources (mirrors `template_seed`
  paths) the packager ships with the plugin.
- `install-manifest.yaml` `template_seed` + `never_touch` — authoritative seed/skip lists.
- `scripts/prd-ce-init.sh` — the deterministic seeder this skill drives.

## Produces

- A seeded scaffold in the target repo (no new SoT IDs — this skill *places* templates, it
  does not author specs).
- A freshly reset `PRD.md` (frontmatter at v0.1, today's date, no stale `template_version`).
- A verification report (hooks emit valid JSON; `readiness.py` runs).

## Workflow

### Phase 1 — Preflight
1. Confirm `git`, `python3`, `bash` are present. Warn (don't block) if the target isn't a git repo.
2. Confirm **greenfield**: if `PRD.md` or non-empty `SoT/` already exist, say so and stop —
   the seeder will keep them untouched, so there is nothing for init to do. (Point the user at
   the lifecycle skills to keep building, not at re-seeding.)

### Phase 2 — Wizard questions
Ask only what changes the outcome (honor the execution mode's budget):
- **Target directory** (default: current repo).
- **Domain profile**: `product` (default) · `library` · `infrastructure` · `research`.
  Quick mode skips this and takes the default.

### Phase 3 — Seed (drive `prd-ce-init.sh`)
Run the deterministic seeder so behavior matches every other path:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/prd-ce-init.sh" --target <DIR> --dry-run   # preview
bash "${CLAUDE_PLUGIN_ROOT}/scripts/prd-ce-init.sh" --target <DIR>             # seed
```
- Show the `--dry-run` plan first `[standard+]`, then execute.
- The seeder skips any file that already exists (`never_touch` honored) and resets a freshly
  seeded `PRD.md` frontmatter to v0.1.
- After seeding, if the chosen domain profile differs from the default, update the
  `profile:` key in the seeded `.claude/domain-profile.yaml` `[standard+]`.

### Phase 4 — Verify (trust-but-verify)
1. Run each plugin hook against the target; assert valid JSON on stdout.
2. Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/readiness.py" run` — a BLOCK on an empty
   scaffold is the **gate working** (no content yet), not a failure. Report the score.
3. Print next steps: customize `README.md` + `PRD.md`, then "Let's frame the problem" (v0.1).

## Anti-patterns

| Pattern | Fix |
|---------|-----|
| Hardcoding the seed file list in the skill | Drive `prd-ce-init.sh`; it reads `template_seed` |
| Copying the framework (skills/hooks) into the consumer repo | The plugin provides those live — seed only consumer-owned files |
| Overwriting an existing `PRD.md`/`SoT/` | Greenfield-only; the seeder skips what exists |
| Leaving `PRD.md` at the example's version header | Frontmatter reset to v0.1 happens automatically on a fresh seed |
| Treating a readiness BLOCK on a fresh scaffold as a bug | It's the gate working — report the score |
