---
name: skill-forge
description: Use when the user asks to forge, scaffold, author, or ship a new skill or agent — the skill-creator's own namesake artifacts. Drives the skill-forge loop (create → fill → validate → critique → ship → publish) via the skill-creator CLI.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "the user asks to create, scaffold, or author a new skill or agent"
  - "the user wants to ship or publish a skill through its quality gates"
updated: 2026-07-12
status: ACTIVE
---

# Skill Forge

Forge a new skill or agent end-to-end using the `skill-creator`
CLI. The forge is the toolchain that scaffolds, validates, and
ships skills and agents; this skill is the playbook that drives it.

## When to invoke

Trigger on any of:

- "create a skill for X" / "author a new skill"
- "scaffold a skill" / "make me a skill that …"
- "add an agent" / "author a subagent for X"
- "ship this skill" / "run the skill through its gates"

Do **not** trigger for:

- Editing an existing skill's guidance — that is
  `skill-creator refine <name>` (corrections, not a new artifact).
- Retiring a skill — that is `skill-creator skill retire <name>`
  (suggest-first, reversible).
- Forging a **cartridge** (content / department / chipset bundle) —
  that is the `cartridge-forge` skill.

## Prerequisites

1. `docs/SKILL-FORMAT.md` is the normative frontmatter/format
   reference; `docs/skill-authoring/skill-md-quality-checks.md`
   lists the hard defects the gate rejects; `docs/authoring-tools.md`
   maps the CLI surface. Read them once per session if the context
   is not already loaded.
2. Pick the slug (kebab-case, matches the skill `name:`). Keep it
   specific — the description and triggers must not collide with an
   existing skill's activation.
3. Decide **skill vs agent**. A skill is auto-loading guidance
   (a `SKILL.md`); an agent is a delegated subagent with its own
   tool set (an `agents/<name>.md`). Author the one the task needs.

## The Forge Loop

```
create → fill → validate → critique → ship → publish
```

Every step is idempotent. `skill ship` is the gate — if it exits
non-zero, the skill is not ready to publish.

### 1. Create

```
skill-creator create
```

The wizard scaffolds a spec-valid `SKILL.md`: repo-canonical
frontmatter (`version` / `format` / `status: ACTIVE`) plus a body
seeded from a template preset (workflow-guide / reference /
checklist) rather than a blank prompt. It prints a
`Next: validate → critique → ship` footer.

For an agent instead of a skill:

```
skill-creator agents create --name=<slug> --description="…"
```

(or run it interactively). It delegates to the AgentGenerator and
writes a spec-valid agent `.md` with comma-separated `tools`.

### 2. Fill

Replace the template body with real guidance. A well-formed skill
body typically wants:

- A one-line intro naming what the skill drives.
- A **When to invoke** section with concrete trigger phrases and an
  explicit do-**not** list (the highest-signal way to keep two
  on-demand skills from co-activating).
- The working steps — commands, rules, or a decision procedure.
- An **Output contract** if the skill produces a deliverable.

Keep the frontmatter `description` and `triggers` distinct: a
trigger that is a verbatim-truncated copy of the description is a
hard defect (see step 3).

### 3. Validate

```
skill-creator validate <name>
```

Runs the skill-content gate: it **blocks** on structural threats
(unsafe YAML, path traversal, schema violation, secret in
frontmatter) and **sanitizes-and-warns** on in-body issues. A clean
exit is required.

### 4. Critique

```
skill-creator critique <name>
```

Surfaces quality issues (thin triggers, missing sections, vague
description) that validate does not hard-block. Address the
findings before shipping.

### 5. Ship

```
skill-creator skill ship <name>
```

Runs the ship pipeline in order — **validate → critique →
test-triggering** — with a per-gate verdict. Exit code `0` means
`<name>` is ship-ready. This is the equivalent of cartridge-forge's
`eval` gate: do not report "done" before it is green. Use `--mock`
to dry-run the pipeline.

For an agent, the parallel gate is:

```
skill-creator agents validate
```

which now exits non-zero on spec defects.

### 6. Publish

```
skill-creator publish <name>
```

Promotes the ship-ready skill. Only run after `skill ship` is green.

## Rules

1. **Never hand-edit a skill under `.claude/skills/`.** That tree is
   gitignored and self-mod-guarded; the tracked source is
   `project-claude/skills/`. Author there and let
   `node project-claude/install.cjs` deploy it.
2. **Never skip `skill ship`.** It is the publish gate.
3. **A correction is not a new skill.** Route "the skill got X
   wrong" to `skill-creator refine`, not a fresh `create`.
4. **Keep triggers distinct from the description** and from other
   skills' triggers — co-activation is a real cost on every session.
5. **Commit the SOURCE only** (`project-claude/…`), never
   `.claude/…` — the git-add-blocker enforces this.

## Reference walkthrough

A well-formed recent skill to model:
`project-claude/skills/skill-frontmatter-doctor/SKILL.md` — a
single-file, on-demand skill with a tight description, distinct
triggers, and a clear defect-detection procedure.

## Output contract

After the loop completes, report to the user:

- Final `name`, artifact kind (skill / agent), and source path.
- Frontmatter shape: `version` / `format` / `status`.
- `validate / critique / ship` verdicts (each shown green).
- Whether it was deployed (`install.cjs`) and published.

Do not report "done" before `skill ship` (or `agents validate`) has
been run and shown green.
