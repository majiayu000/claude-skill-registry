---
name: context-creation
description: The brownfield back-fill. Routed to by /create-context, and by startup when .codearbiter/CONTEXT.md lacks the <!--INITIALIZED--> body marker but source code exists. Six gated phases — pre-flight, scout dispatch, synthesis, gap interview, write, lock. Reads the existing codebase through parallel scouts, drafts every surviving project-state doc, resolves gaps with the user, and locks the project as initialized.
---

# context-creation

Wrap an existing codebase in project state, without guessing. Routed to by `/create-context`, and by startup when `.codearbiter/CONTEXT.md` exists but carries no `<!--INITIALIZED-->` body marker and meaningful source code is present. When no meaningful source exists, this is the wrong skill — route to `decompose` instead.

This back-fills from existing source. It complements `/ca-init`, which scaffolds an empty `.codearbiter/` for a fresh project; here the docs are derived from what is already on disk.

## Pre-flight

Read these, or STOP and surface the gap — never guess project identity or a command:

- `<project-root>/.codearbiter/CONTEXT.md` — if it already carries `<!--INITIALIZED-->`, context exists. Stop and route to normal operation.
- The repository root listing (one level deep) — the source surface this skill extracts from.

The excluded set (not "meaningful source"): `.git/`, `.codearbiter/`, `.claude/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitmodules`, and standard tooling dotfiles (`.editorconfig`, `.prettierrc`, etc.). Meaningful source MUST exist beyond it.

## Phase 1 — Pre-flight confirmation · gate: BLOCK

Confirm the repository is a brownfield codebase safe for scout-based extraction:

1. Confirm `<!--INITIALIZED-->` is absent from `CONTEXT.md`.
2. Confirm meaningful source code is present beyond the excluded set.
3. Identify the primary source directories (`src/`, `backend/`, `frontend/`, `lib/`, `app/`, or equivalent).

State the finding to the user: existing source detected, beginning scout-based extraction.

Gate: `<!--INITIALIZED-->` absent AND meaningful source present. If the marker is present, stop and route to normal operation. If no meaningful source exists, stop and route to `decompose`. Neither condition met → do not proceed.

## Phase 2 — Scout dispatch · gate: BLOCK

A **scout** is a restricted, read-only role, not an unconstrained
`general-purpose` agent. A scout reads one targeted slice of the codebase and
returns a structured findings report — file paths, line numbers, and named
values only, never raw code excerpts. Scouts are internal to this skill; they
are never invoked from a command.

Dispatch six isolated `scout` subagents simultaneously. If the active host
cannot provide isolated subagents, BLOCK context creation and report the host
capability gap. The general inline-role fallback does not apply here: this
skill's report-only synthesis contract depends on the orchestrator never
loading the scouts' raw source into its own context.
Each reads only its assigned slice:

- **Scout A — Tech stack.** Read `package.json`, lockfiles, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `*.gemspec`, `Gemfile`. Report languages, runtime versions, frameworks, key dependencies, the dependency manager, license fields.
- **Scout B — Infrastructure.** Read CI/CD config (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`), `Dockerfile*`, `docker-compose*.yml`, `Makefile`, `*.tf`, IaC. Report CI/CD platform, build/test/lint commands, deployment targets, environment names, containerization, IaC tool.
- **Scout C — Architecture.** Read the source tree (names and structure only), entry points (`main.ts`, `index.ts`, `app.py`, `server.go`), and imports in entry points only. Report component list, entry points, module boundaries, architectural pattern, public interfaces.
- **Scout D — Security posture.** Read auth files (`auth*`, `middleware*`, `guard*`, `jwt*`, `session*`, `oauth*`), crypto import lines, secret-loading sites (`process.env`, `os.environ`, vault/KMS call sites — paths and line numbers only, never values), `.env.example` (never `.env`). Report auth mechanism, crypto libraries, secret-loading patterns (paths + lines, no values), vault/KMS integration, hardcoded-secret risk files (paths only).
- **Scout E — Testing.** Read test files and test config (`vitest.config.*`, `jest.config.*`, `pytest.ini`, Makefile test flags), coverage config. Report test framework, runner command, coverage tool, coverage thresholds in config, naming convention, approximate test count by type, fixtures.
- **Scout F — Data model.** Read migration files (`migrations/`, `drizzle/`, `alembic/`, `db/migrate/`), schema definitions (`schema.ts`, `*.prisma`, `*.sql`, `models/`), ORM config, DB connection config (keys only, never credentials). Report database type, ORM/query builder, entity names, migration tool, approximate entity count, multi-tenancy patterns.

The orchestrator reads only the scout reports in later phases — never the raw source — to preserve working context. A scout that finds nothing returns an explicit "not found" report, never silence.

**Content hashes:** Scouts additionally emit a `git hash-object <path>` content oid per cited file in the hash field of their evidence entry. The scout already Read those files — no additional pass is needed, and no raw content is forwarded to the orchestrator.

Gate: all six scout reports returned. A missing report is a blocking gap — do not proceed with an incomplete picture. Re-dispatch a failing scout before Phase 3.

## Phase 3 — Synthesis · gate: BLOCK

Draft every surviving project-state doc from the six reports, working only from the reports. Map source to destination:

| Scout source | Destination |
|---|---|
| A (tech stack), B (build/test/lint commands), E (test runner) | `tech-stack.md` |
| C (architecture), E (structure) | `coding-standards.md` |
| D (security) | `security-controls.md` (thin) |
| All scouts | `CONTEXT.md` (project identity, purpose, scope, NOT-building) |

Classify every finding by confidence:

- **HIGH** — directly and unambiguously in a report (e.g., `"jest"` in `package.json`). Write it as fact.
- **MEDIUM** — inferred from an indirect signal (directory layout implies layered architecture, no explicit config). Write it with a note: inferred from [signal], verify before relying on it.
- **LOW** — no signal, or conflicting signals. Write a `[CONFIRM-NN]` placeholder.

Every `[CONFIRM-NN]` carries: a sequential ID, one sentence on what is unknown, why it matters, and what would resolve it. IDs are sequential with `open-questions.md`.

Gate: every surviving doc drafted; every low-confidence inference carries a `[CONFIRM-NN]`. No silent omission. A domain with no scout signal gets a doc with a `[CONFIRM-NN]` for the whole section — never an empty file.

## Phase 4 — Gap interview · gate: BLOCK

Resolve `[CONFIRM-NN]` items with the user. Ask only what the scouts could not answer with HIGH confidence.

1. Present the `[CONFIRM-NN]` list grouped by category — gaps the scan could not resolve.
2. Ask ONE targeted question per item. No compound questions. Do not re-ask anything scouts answered with HIGH confidence.
3. Per answer: if it resolves the gap, replace the placeholder with content; if the user explicitly defers, keep the placeholder, mark it deferred with the date, and record it in `open-questions.md`; if the answer is vague, challenge it and demand a concrete answer before recording anything.

Gate: every `[CONFIRM-NN]` has exactly one outcome — resolved (replaced with content) or explicitly deferred (marked and recorded in `open-questions.md`). No item is silently dropped. Do not proceed with unacknowledged gaps.

## Phase 5 — Project-state write · gate: BLOCK

Write the surviving docs to `<project-root>/.codearbiter/`. Every doc carries actual content — no unresolved placeholder may remain where a value was determined:

| File | Content |
|---|---|
| `CONTEXT.md` | Project identity, purpose, scope, primary users, NOT-building. Frontmatter MUST include `arbiter: enabled` (the activation flag the SessionStart hook keys on) and `stage:` set to a single maturity number (default `1`; the user may raise it if the project is further along). |
| `tech-stack.md` | Languages, frameworks, test runner, lint command, build command, coverage command, issue-tracker command (e.g. `gh issue create`). |
| `coding-standards.md` | Structural patterns, naming conventions, style rules. |
| `security-controls.md` | Thin: auth mechanism, banned crypto primitives, secret-loading stance. Only what a security boundary actually requires. |
| `open-questions.md` | Every deferred `[CONFIRM-NN]` in `CONFIRM-NN: <description>` form. |
| `open-tasks.md` | The task backlog if scouts found one; otherwise a stub noting the user must populate it. |
| `overrides.log` | Empty append-only audit log, created so `/override` has a sink. |

If scouts found existing decision records (`docs/decisions/`, `adr/`), summarize them as entries under `.codearbiter/decisions/` in the standard ADR format. If a record cannot be fully parsed, summarize what is known, flag the uncertainty, and note the source path for review.

**Provenance and code-map (small addition, not a Phase 5 rebuild):**

- Write ONE provenance file per derived doc to `.codearbiter/.provenance/<doc>.json` via `_provenancelib.write_provenance` and `new_record`. Each entry carries: `path` (repo-relative), `hash` (the scout's `git hash-object` oid), `drift_trigger` (from `_provenancelib.classify_source(path)`), and the `claims` array with `lines`, `claim`, and `confidence` drawn from the scout evidence.
- Synthesize `.codearbiter/code-map.md` (concern → path → ≤1-line role) from Scout C (architecture) evidence. Use concern headings (`## <concern>`) and column-0 bullets (`- \`path\` — role`). Keep it coarse — module/concern granularity only, no full file listing.

Do NOT scaffold any cut doc — see `<plugin-root>/includes/cut-docs.md` for the canonical never-scaffold list. Maturity lives in the `stage:` frontmatter of `CONTEXT.md`, not a separate file.

Gate: every surviving doc written; `CONTEXT.md` frontmatter carries `arbiter: enabled` and `stage:`; no resolved value left as a placeholder. Deferred `[CONFIRM-NN]` items are acceptable only in `open-questions.md`.

## Phase 6 — Initialization lock · gate: BLOCK

Lock the project state as initialized and return to normal orchestration:

1. Write the `<!--INITIALIZED-->` marker into the body of `CONTEXT.md`.
2. List `.codearbiter/` and display the populated tree.
3. Confirm each required file is present and non-empty: `CONTEXT.md` (with `arbiter: enabled` frontmatter and the `<!--INITIALIZED-->` body marker), `tech-stack.md`, `coding-standards.md`, `security-controls.md`, `open-questions.md`, `open-tasks.md`, `overrides.log`.
4. State the return to normal operation: extraction complete, project state initialized and locked, `/ca-feature` available to begin work. Deferred questions live in `open-questions.md`.

Gate: `arbiter: enabled` set and `<!--INITIALIZED-->` present in `CONTEXT.md`; every required file present and non-empty. Do not close this skill without confirming both markers are written.

## Hard rules

- MUST NOT write `<!--INITIALIZED-->` while any `[CONFIRM-NN]` is unaddressed — every gap must be resolved or explicitly deferred to `open-questions.md` first.
- MUST NOT resolve a `[CONFIRM-NN]` by guessing — surface the question to the user or defer it.
- MUST NOT proceed past Phase 2 with fewer than six scout reports.
- MUST NOT run Phase 2 inline — isolated scout subagents are required for the report-only synthesis boundary.
- MUST NOT load raw source into the orchestrator context after Phase 1 — synthesize from scout reports only.
- MUST NOT record a scout finding that exposes a secret value — paths and line numbers only.
- MUST NOT scaffold a cut doc — see `<plugin-root>/includes/cut-docs.md` for the canonical never-scaffold list. Maturity is the `stage:` frontmatter number in `CONTEXT.md`.
- MUST NOT run when `CONTEXT.md` already carries `<!--INITIALIZED-->` — stop and route to normal operation.
