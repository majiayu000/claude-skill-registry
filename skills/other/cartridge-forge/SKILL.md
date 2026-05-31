---
name: cartridge-forge
description: Use when the user asks to forge, scaffold, or author a new cartridge — content cartridge, department cartridge, or chipset bundle. Drives the cartridge-forge loop (scaffold → fill → gate checks → commit) via the skill-creator cartridge CLI.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "the user asks to forge, scaffold, or author a new cartridge — content cartridge, department cartridge, or chipset bundle"
updated: 2026-04-25
status: ACTIVE
---

# Cartridge Forge

Forge a new cartridge end-to-end using the `skill-creator cartridge`
CLI. The forge is the toolchain that builds cartridges; this skill
is the playbook that drives it.

## When to invoke

Trigger on any of:

- "create a cartridge for X"
- "forge a new cartridge"
- "scaffold a department" / "generate a department cartridge"
- "build a content cartridge"
- "make a chipset bundle for X"

Do **not** trigger for migrating legacy cartridges (that is
`cartridge migrate`) or for forking an existing one (that is
`cartridge fork`).

## Prerequisites

1. `docs/cartridge/FORGING-GUIDE.md` and
   `docs/cartridge/CARTRIDGE-SPEC.md` are the normative references.
   Read them once per session if the context is not already loaded.
2. Pick the target directory. Convention:
   - `examples/cartridges/<slug>/` for in-repo cartridges
   - `./my-cartridges/<slug>/` for ad-hoc / user-local work
3. Pick the slug. Drop the `-department` suffix **unless** the
   cartridge is directly tied to a college department in
   `.college/`. "systems-administration" — not
   "systems-administration-department".
4. Pick the template: `department` (skills + agents + teams),
   `content` (deepMap + story arc), `coprocessor` (pure functional
   tooling), or `graphics` (GLSL / OpenGL / WebGL / Vulkan shader
   pipeline; grounded in the GFX research series at
   [/Research/GFX/](https://tibsfox.com/Research/GFX/) on tibsfox.com).

## The Forge Loop

```
scaffold → fill → validate → eval → dedup → metrics → commit
```

Every step is idempotent and JSON-capable. `eval` is the gate —
if it exits non-zero, the cartridge is not ready to ship.

### 1. Scaffold

```
skill-creator cartridge scaffold <template> <dir> <slug>
```

Writes an 8-file skeleton: `cartridge.yaml`, `chipsets/*.yaml`,
one placeholder skill, agent, and team, plus a `README.md`.
Round-trips through `load` → `validate` with zero errors before
any edits.

### 2. Fill

Replace placeholder content with real content. A full department
cartridge typically wants:

- **Skills** — one per daily responsibility surface (10–15 is a
  comfortable size; fewer feels thin, more suggests a split)
- **Agents** — an Opus capcom + hands-on Sonnet executors;
  router topology with `is_capcom: true` on the capcom
- **Teams** — one per recurring workflow (author, review,
  incident, drill) — each team names its roster and
  `use_when`
- **Grove record types** — 4–8 record types that capture the
  durable outputs this cartridge produces
- **Evaluation domains** — one per skill domain; keep them
  aligned with the `domain:` field on each skill

Replace the skeleton's `cartridge.yaml` header:

- `id:` slug
- `name:` title case, human-readable
- `author:` real author
- `description:` one-paragraph, no marketing tone
- `provenance.origin`, `provenance.createdAt`
- `metadata.tags`

Delete the three placeholder markdown files
(`skills/placeholder-skill.md`, `agents/placeholder-agent.md`,
`teams/placeholder-team.md`) and replace them with one markdown
file per real skill / agent / team. Each companion file is
informational — the loader does not scan them, but a "full"
cartridge ships them.

### 3. Validate

```
skill-creator cartridge validate <dir>/cartridge.yaml --json
```

`valid: true` is the required outcome. If there are validation-debt
errors (e.g. around `agent_affinity` or `domains_covered`), add
`--allow-validation-debt` and track the debt per
`docs/cartridge/KNOWN-VALIDATION-DEBT.md`.

### 4. Eval

```
skill-creator cartridge eval <dir>/cartridge.yaml
```

Runs the pre-deploy gates declared in
`chipsets/evaluation.yaml`. Default gates:

- `all_skills_have_descriptions`
- `all_agents_have_roles`
- `grove_record_types_defined`
- `has_evaluation_chipset`

Exit code `0` is required before commit.

### 5. Dedup

```
skill-creator cartridge dedup <dir>/cartridge.yaml
```

`no collisions` is required. Collisions mean a skill or agent is
defined twice across chipsets — either intentional merge
(refactor) or typo (fix).

### 6. Metrics

```
skill-creator cartridge metrics <dir>/cartridge.yaml
```

Informational, not a gate. Captures shape (skill / agent / team /
record-type counts) for the commit message.

### 7. Commit

Conventional Commits, scope `cartridge`:

```
feat(cartridge): forge <slug> cartridge

N skills / M agents / K teams / J grove record types.
Forged via cartridge-forge from the <template> template.
All forge gates green: validate, eval, dedup.
```

## Rules

1. **Never hand-author a `cartridge.yaml` from scratch.** Always
   scaffold first — the template encodes the current schema.
2. **Never skip `eval`.** It is the ship gate.
3. **`kind: department` is a schema discriminator, not a college
   tie.** The chipset kind stays `department` even when the
   cartridge is not tied to a college department.
4. **Drop `-department` from the slug** unless the cartridge is
   tied to an entry under `.college/`.
5. **The companion markdown files are not validated.** Write
   them anyway — a cartridge without them is scaffold-quality.
6. **Backup and DR content belongs in a dedicated team**
   (`<slug>-dr-drill-team` or equivalent) if the cartridge has
   data-durability responsibilities.

## Reference walkthrough

A complete worked example:
`examples/cartridges/systems-administration/` — 12 skills,
5 agents, 4 teams, 6 grove record types, all forge gates green.

## Output contract

After the loop completes, report to the user:

- Final `id`, `name`, and path
- Chipset list
- Counts: skills / agents / teams / grove record types
- `validate / eval / dedup` verdicts
- Any validation debt accepted and the follow-up note

Do not report "done" before all four forge gates (validate, eval,
dedup, metrics) have been run and shown green.
