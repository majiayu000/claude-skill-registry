---
name: skill-builder
description: |
  Build correct, consistent Agent Skills (create/update/delete/add content) using validated templates,
  safe defaults, and cross-skill consistency checks.
  Works across common agent CLIs that load skills from Markdown folders.
  Triggers: "new skill", "create skill", "build skill", "update skill", "delete skill",
  "add to skill", "skill template", "skill validation", "skill builder".
license: MIT
compatibility: Agent Skills spec (agentskills.io). Works with any agent product that supports SKILL.md frontmatter + Markdown.
metadata:
  version: "1.0"
---

# Skill Builder

Unified, security-first skill builder.

This skill is intentionally opinionated:
- Prefer no new skill if a simpler change works (project docs, a script, or a small snippet).
- When you do create a skill, make it boring, testable, and hard to misuse.
- Keep one clear router and avoid overlapping triggers across skills.

## Operation Router

| User intent | Operation | Output |
|---|---|---|
| create/build/make/new skill | CREATE | new skill folder + `SKILL.md` + `README.md` |
| update/modify/improve skill | UPDATE | minimal diff, keep triggers stable |
| delete/remove skill | DELETE | remove skill + update repo index |
| add content/route/workflow to skill | ADD | new router row + new section file (when needed) |
| validate skill | VALIDATE | checklist results + fixes |
| rename skill | RENAME | safe rename + reference updates |

## What "Correct" Means

This skill treats "correct" as:

- Conforms to the Agent Skills spec (directory + `SKILL.md` frontmatter constraints).
- Uses progressive disclosure: small `SKILL.md`, deeper docs in `references/`.
- Has unambiguous activation: specific description + non-overlapping triggers.
- Is safe: no secrets, no default-destructive commands, tool usage is scoped.

## Phase 0: First-Principles Check (Mandatory)

Run this before ANY CREATE/UPDATE:

1. QUESTION: what problem, for who, measured how?
2. DELETE: can an existing component/skill/command solve it?
3. SIMPLIFY: smallest change that works (often a project instruction file)
4. ACCELERATE: only after (2) and (3)
5. AUTOMATE: create a component only if it will be reused

If the answer is "no skill", propose:
- a README section
- a small script
- a usage snippet users can copy

## Phase 1: Detect Target + Name

### Target repository layout

This repo layout:

- `/<skill-name>/SKILL.md` (home/router)
- `/<skill-name>/README.md` (short overview)
- optional: `/<skill-name>/references/*.md` (split workflows)

## Spec Rules (Agent Skills)

From the Agent Skills specification:

- Skill folder name must match `name`.
- `name` constraints: 1-64 chars; lowercase letters/numbers/hyphens; no leading/trailing `-`; no `--`.
- `description` should say what + when; max 1024 chars.
- Optional frontmatter fields you may include: `license`, `compatibility`, `metadata`, `allowed-tools`.

Reference: https://agentskills.io/specification

### Naming

- Use kebab-case (`my-skill-name`).
- Avoid generic names (`tools`, `helper`).
- Prefer verbs for commands (`review-pr`, `sync-main`).

## Phase 2: CREATE Flow

### Inputs (minimum)

- Name
- Goal + non-goals
- Triggers (what user says)
- Allowed tools (tightest possible)

### CREATE Steps

1. Discover existing conventions (look at other skills in the repo).
2. Draft a micro-spec (goal/non-goals, routing, tool boundaries).
3. Create `/<skill-name>/SKILL.md` with:
   - front matter (name/description + triggers)
   - router table
   - safety rules
   - minimal workflows (or links to `references/`)
4. Create `/<skill-name>/README.md` with install + entry points.
5. Validate (see Validation).
6. If the repo has an index of skills (commonly a `README.md`), add/update the entry.

### Output Contract (CREATE)

When creating a skill, always return:

- Files created/edited (paths only)
- Trigger phrases added
- One minimal "smoke test" prompt (how to activate it)
- Validation result (pass/fail + what to fix)

## Phase 3: UPDATE Flow

1. Read current skill.
2. Identify actual user goal (avoid refactors).
3. Apply minimal diff.
4. Re-run validation checklist.
5. Keep triggers stable unless explicitly requested.

## Phase 4: DELETE Flow

1. Confirm skill folder.
2. Identify dependents (root `README.md`, other skill references).
3. Remove skill and update references.
4. Provide rollback note (restore from git).

## Phase 5: ADD Content to a Skill

Rules for skill growth:
- Never duplicate trigger phrases across multiple skills in the same install.
- Route by intent first, then load deeper sections.
- Keep SKILL.md readable: prefer short tables + stable templates.

Add steps:
1. Add one new router row.
2. Add the minimal new procedure.
3. If it grows: split into `references/<topic>.md`.
4. Add/adjust examples.
5. Re-check cross-skill consistency.

## Validation

### Skill Validation Checklist

- Front matter includes `name` and `description`.
- Has a router (how to decide what to do).
- Defines what is safe to run without confirmation vs requires confirmation.
- No secrets; no links to private paths.
- No unscoped destructive instructions.
- Trigger hygiene: no overlapping triggers with existing skills in the repo.
- Docs split: if SKILL.md becomes long, move workflows into `references/`.

### Spec Validation (Recommended)

If you have the reference validator available (optional), run:

```bash
skills-ref validate ./<skill-name>
```

If not available, validate manually using the rules in "Spec Rules" above.

### Tool Safety

- Prefer Read/Glob/Grep before Bash.
- If Bash is needed, scope it (git-only, or specific commands).
- Never recommend `rm -rf`, `git reset --hard`, `push --force` as defaults.

## Templates

### Skill Front Matter

```yaml
---
name: my-skill
description: Describe what the skill does and when to use it. Include trigger phrases.
compatibility: Optional. Mention required system tools, network needs, or target environments.
metadata:
  version: "0.1"
allowed-tools: Optional. Space-delimited list. Prefer the narrowest set possible.
---
```

### Progressive Disclosure Pattern

Keep `SKILL.md` as:

1. Frontmatter
2. Router table
3. Safety rules
4. Short workflows
5. Links to `references/*.md` for deep details

## References

- `references/checklist.md` (authoring checklist)
- `references/templates.md` (copy/paste templates)
- `references/validation.md` (validation flow + trigger hygiene)

## What This Skill Is For (Practical Examples)

- "Create a skill that scaffolds new skills" → create a skill + templates + validation.
- "Update my git workflow" → improve the router + split workflows into `references/`.
- "Make skills consistent across repos" → enforce naming/triggers/tool boundaries.
