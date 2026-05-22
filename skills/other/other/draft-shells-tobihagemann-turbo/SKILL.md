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
3. Resolve open questions
4. Write shell files
5. Present summary

If decomposition lands on one shell, the Single-Shell Bail-out at the end of Step 2 marks tasks 3-5 deleted via `TaskUpdate` and exits.

## Step 1: Resolve the Source Spec

Determine which spec to decompose using these rules in order:

1. **Explicit path** — If the user passed a file path, use it
2. **Explicit slug** — If a slug was passed, resolve to `.turbo/specs/<slug>.md`
3. **Single file** — Glob `.turbo/specs/*.md`. If exactly one file exists, use it
4. **Most recent** — If multiple files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/specs/` does not exist but `.turbo/spec.md` exists, use it
6. **Nothing found** — If no spec exists, nothing to decompose; stop

The slug of the resolved spec becomes the prefix for shell file names: a spec at `.turbo/specs/<slug>.md` produces shells at `.turbo/shells/<slug>-NN-<title>.md`. For the legacy fallback, use slug `legacy`.

State the resolved spec path and target shell directory before continuing.

Read the spec and identify:
- **Scope** — total surface area of work
- **Work categories** — UI, backend, data layer, infrastructure, tests, documentation, tooling
- **Spec requirements** — enumerate the `R<N>` IDs from the spec's `## Requirements` section. Every R-id must be tracked in at least one shell's Covers field.
- **Dependencies** — which pieces must exist before others can start
- **Greenfield vs existing** — is there an established codebase to work within
- **Open questions** — decisions the spec deferred that will need to be answered at implementation time

If the spec has no `## Requirements` section or contains no `R<N>`-numbered items, use `AskUserQuestion` with two options: re-run `/draft-spec` (then restart Step 1 with the resulting spec) or stop so the user can add a `## Requirements` section with enumerated `R<N>` IDs manually. Shells depend on stable R-ids for coverage tracking.

## Step 2: Decompose Into Shells

Split the spec into shells where each shell fits a single Claude Code context session.

### Shell-Worthiness

The default is one shell. Adding a shell costs a fresh-session handoff: lost in-memory context, a repeated pattern survey, and an extra `/pick-next-shell` round. Splitting is justified only when a forcing condition for splitting applies:

- **Context-window pressure.** The combined work would exhaust a single Claude Code session before completing: too much code to read in full, too many distinct codebase conventions to absorb, or too much output to generate in one window. Judge from the actual scope and codebase shape, not from headcounts. Distinct Produces/Consumes boundaries between two pieces are not enough on their own to justify a split.
- **Hard dependency ordering.** A later piece cannot be meaningfully drafted or expanded until an earlier piece's concrete output exists, such as generated types, framework wiring, or established patterns that later sessions need to survey against.
- **Independent subsystems with no overlap.** Two or more pieces share no coupling and no overlap in pattern surveys, so separate focused sessions give a real benefit over one combined session.

If none of these apply, the work is one shell. Do not invent dependencies to hit a multi-shell shape. A spec's suggested groupings are a starting point — collapse adjacent suggestions into a single shell when no forcing condition separates them. Trust larger units of work; most spec items do not earn their own shell.

Items folded into a shell go into that shell's Implementation Steps. If several folded items have no clear home, group them into a single "minor fixes" shell at the end.

**Forcing condition — atomic ripple (forces combination).** When a breaking change to a shared interface requires every consumer across multiple modules to update in lockstep, the change and all consumer updates must land in one shell regardless of size. Splitting leaves intermediate states that break dependents.

### Sizing

- One shell = one logical unit of work (a feature, a subsystem, a layer)
- Never split tightly-coupled pieces across shells (if UI + API + tests are inseparable, keep them together)
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
- **Consumes** — What this shell depends on that must already exist. Either listed in a prior shell's Produces (and that producing shell named directly in this shell's frontmatter `depends_on`), or marked "from existing codebase" if it predates this decomposition. Every Consumes entry must be traceable to a source.
- **Covers spec requirements** — Which `R<N>` IDs from the spec's `## Requirements` section this shell implements. The union of Covers across all shells must equal the full set of R-ids in the spec. Every R-id must appear in at least one shell's Covers. Write one R-id per bullet in the Step 4 template. For partial coverage of a single R-id, mark the entry `R<N> (partial: <what's deferred>)` and name the deferred work in that shell's Open Questions. A bare `R<N>` for partial coverage breaks the invariant. Do not invent variant annotations such as `(finished: ...)` or `(closing: ...)`.

### Shell Slug

Each shell gets a slug derived from its title using spec slug rules (lowercase, hyphenated, ≤40 chars), prefixed with the shell number: `<spec-slug>-NN-<title-slug>`. The shell keeps this file name when `/expand-shell` fills it in.

Example: spec slug `photo-sorter-v2`, Shell 3 titled "Build duplicate detection" → slug `photo-sorter-v2-03-build-duplicate-detection`, written to `.turbo/shells/photo-sorter-v2-03-build-duplicate-detection.md`.

### Single-Shell Bail-out

If decomposition lands on exactly one shell, do not write a shell file. A one-shell decomposition is structurally equivalent to a plan: `depends_on` is empty, Covers lists every R-id, Produces/Consumes has no consumers, and `/pick-next-shell` automation has nothing to coordinate.

Present this message:

> Decomposition produced one shell, so no shell file was written. The spec at `<resolved spec path>` fits a single session and is plan-shaped.

Mark the remaining `/draft-shells` tasks ("Resolve open questions", "Write shell files", "Present summary") as deleted via `TaskUpdate`. Do not create `.turbo/shells/`. Then use the TaskList tool and proceed to any remaining task.

## Step 3: Resolve Open Questions

If no open questions emerged during decomposition or carried over from the spec, skip this step.

For each open question:

1. Analyze the question against the spec, decomposition context, and any consulted references. State the trade-offs of the leading options in plain text so the user can see the reasoning.
2. Use `AskUserQuestion` to offer 2-3 concrete resolution options with short descriptions, plus a **Defer to expansion** option (leaves the question on the relevant shell's Open Questions list). Mark the strongest option "(Recommended)" and place it first.
3. If resolved, update the in-memory decomposition (Produces, Consumes, Covers, Implementation Steps) to reflect the answer. If deferred, record it against the relevant shell in the in-memory decomposition.

If the user selects "Other" and provides a freeform answer, accept it and proceed.

Default to resolving. Defer only when the answer genuinely needs codebase or pattern-survey context that is not yet available.

If an answer would restructure the decomposition significantly (changes shell count, merges existing shells, or splits one shell into several), re-run Step 2 with the new constraint before continuing to Step 4. If the new count is 1, the Single-Shell Bail-out at the end of Step 2 applies.

## Step 4: Write Shell Files

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

- R<N>
- R<N>
- R<M> (partial: <what's deferred>)
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
- Concrete `file_path` references with named functions or symbols for each Implementation Step
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

## Step 5: Present Summary

Present a brief summary: number of shells, one-line description of each shell's scope, and any assumptions made about ambiguities. Tell the user the next step:

> To start implementation, run `/pick-next-shell`. After it halts, run `/implement-plan` in a fresh session.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Never merge setup and finalization into the same shell
- If the spec is ambiguous about what belongs together, prefer combining: fewer, larger shells are safer than over-split ones
- Each shell must be self-contained with enough structural context (Context, Produces, Consumes, Covers) to understand the work without reading the full spec
- Shell files are the only outputs. Do not modify the spec or project files.
- Every Consumes entry must be backed by an explicit edge in the shell's frontmatter `depends_on` (or marked "from existing codebase").
- The union of all Covers fields must equal the full set of R-ids in the spec's `## Requirements` section. Every R-id must appear in at least one shell's Covers.
- Coverage notations: only bare `R<N>` (full, claimed exactly once) and `R<N> (partial: <what's deferred>)`. Do not invent variants like `(finished: ...)`.
- Implementation Steps (High-Level) describe build work. Exclude `git commit`, `git push`, and PR creation.
