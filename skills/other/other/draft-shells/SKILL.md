---
name: draft-shells
description: "Decompose a specification file into shells with YAML frontmatter. Each shell captures the wiring invariants (Produces, Consumes, Covers) and high-level Implementation Steps without committing to file paths. Use when the user asks to \"draft shells\", \"create shells\", \"break spec into shells\", \"decompose spec into sessions\", \"draft shells from spec\", \"generate shells from spec\", or \"make shells from spec\"."
---

# Draft Shells

Decompose a specification file into shells at `.turbo/shells/<spec-slug>-NN-<title>.md`. Each shell represents one unit of work for a separate Claude Code session.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Resolve the source spec
2. Decompose into shells
3. Write shell files
4. Present summary

## Step 1: Resolve the Source Spec

Determine which spec to decompose using these rules in order:

1. **Explicit path** — If the user passed a file path, use it
2. **Explicit slug** — If a slug was passed, resolve to `.turbo/specs/<slug>.md`
3. **Single file** — Glob `.turbo/specs/*.md`. If exactly one file exists, use it
4. **Most recent** — If multiple files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/specs/` does not exist but `.turbo/spec.md` exists, use it
6. **Nothing found** — If no spec exists, tell the user to run `/draft-spec` first and stop

The slug of the resolved spec becomes the prefix for shell file names: a spec at `.turbo/specs/<slug>.md` produces shells at `.turbo/shells/<slug>-NN-<title>.md`. For the legacy fallback, use slug `legacy`.

State the resolved spec path and target shell directory before continuing.

Read the spec and identify:
- **Scope** — total surface area of work
- **Work categories** — UI, backend, data layer, infrastructure, tests, documentation, tooling
- **Spec requirements** — enumerate the distinct requirements so each can be tracked in a shell's Covers field
- **Dependencies** — which pieces must exist before others can start
- **Greenfield vs existing** — is there an established codebase to work within
- **Open questions** — decisions the spec deferred that will need to be answered at implementation time

## Step 2: Decompose Into Shells

Split the spec into shells where each shell fits a single Claude Code context session.

### Sizing

- One shell = one logical unit of work (a feature, a subsystem, a layer)
- Never split tightly-coupled pieces across shells (if UI + API + tests are inseparable, keep them together)
- Split independent subsystems into separate shells
- If a shell would touch more than ~15-20 files or span 3+ unrelated subsystems, split further
- If the entire scope fits one session, produce a single shell
- Each shell must leave the codebase fully integrated, with no components unreachable from the project's entry points
- When a shell builds infrastructure that a later shell consumes, name the consumer explicitly in the Produces field

### Ordering

Order by dependency, foundational work before dependent work:

1. Setup and scaffolding (project init, config, CI)
2. Data and domain layer (models, schemas, types)
3. Core business logic
4. API and service layer
5. UI and frontend
6. Integration and end-to-end concerns

Mitigate dead code risk in bottom-up ordering by bundling tightly-coupled producer/consumer pairs into the same shell, or having foundation shells include a minimal integration point (e.g., a single working endpoint or CLI command) that proves the code is reachable.

### Wiring Invariants

For each shell, identify the structural contract with the rest of the decomposition:

- **Produces** — What this shell creates that other shells (or the final system) can use. List concrete artifacts at the conceptual level: modules, types, endpoints, data models, UI screens, migration files. File paths are filled in at expansion time.
- **Consumes** — What this shell depends on that must already exist. Either listed in a prior shell's Produces, or marked "from existing codebase" if it predates this decomposition. Every Consumes entry must be traceable to a source.
- **Covers spec requirements** — Which spec sections or requirements this shell implements. The union of Covers across all shells must equal the set of spec requirements.

### Shell Slug

Each shell gets a slug derived from its title using spec slug rules (lowercase, hyphenated, ≤40 chars), prefixed with the shell number: `<spec-slug>-NN-<title-slug>`. The shell keeps this file name when `/expand-shell` fills it in.

Example: spec slug `photo-sorter-v2`, Shell 3 titled "Build duplicate detection" → slug `photo-sorter-v2-03-build-duplicate-detection`, written to `.turbo/shells/photo-sorter-v2-03-build-duplicate-detection.md`.

## Step 3: Write Shell Files

Create `.turbo/shells/` if it does not exist. For each shell, write a file at `.turbo/shells/<shell-slug>.md` using this template:

````markdown
---
spec: <resolved spec path from Step 1>
depends_on: []
---

# Plan: <Shell Title>

## Context

<Why this work matters, drawn from relevant spec sections. Focus on the intended outcome. One or two paragraphs.>

## Produces

- <Conceptual artifact 1 — what it is, what it does>
- <Conceptual artifact 2>
- ...

## Consumes

- <Conceptual dependency 1 — from Shell N, or "from existing codebase">
- <Conceptual dependency 2>
- ...

## Covers Spec Requirements

- <Spec section or requirement ID>
- <Spec section or requirement ID>
- ...

## Implementation Steps (High-Level)

1. **<Step title>**
   - <Description of what this step accomplishes at the conceptual level>
2. **<Step title>**
   - <Description>
3. ...

## Open Questions

- <Question deferred from spec, to be answered at expansion time>
- <Question>
- ...

## Expansion Deferred

The following are filled in when `/expand-shell` runs:

- Pattern survey against the codebase state at implementation time
- Concrete `file_path:line_number` references for each Implementation Step
- Verification section with specific test commands and smoke checks
- Context Files section with the files to read in full before editing
````

### Frontmatter Fields

- **spec** — Absolute or relative path to the source spec
- **depends_on** — List of shell file names (without `.md`) that must be expanded and implemented before this shell can be picked. Use `[]` for shells with no dependencies.

Example `depends_on` for Shell 3 that depends on Shells 1 and 2:
```yaml
depends_on: [photo-sorter-v2-01-setup, photo-sorter-v2-02-models]
```

If a shell has no Open Questions, include the section with "None" so the structure stays consistent.

## Step 4: Present Summary

Present a brief summary: number of shells, one-line description of each shell's scope, and any assumptions made about ambiguities. Tell the user the next step:

> To start implementation, run `/pick-next-shell`. It will pick the next shell, expand it with a fresh pattern survey and concrete references, refine, self-improve, then halt. Run `/implement-plan` in a fresh session afterward.

Check your task list for remaining tasks and proceed.

## Rules

- Never merge setup and finalization into the same shell
- If the spec is ambiguous about what belongs together, split conservatively (smaller shells are safer than oversized ones)
- Each shell must be self-contained with enough structural context (Context, Produces, Consumes, Covers) to understand the work without reading the full spec
- Shell files are the only outputs. Do not modify the spec or project files.
- Every Consumes entry must trace to a prior shell's Produces or to "from existing codebase."
- The union of all Covers fields must equal the set of spec requirements.
