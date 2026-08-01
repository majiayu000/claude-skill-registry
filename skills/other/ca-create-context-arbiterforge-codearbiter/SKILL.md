---
name: ca-create-context
description: Brownfield back-fill — scout an existing codebase and populate .codearbiter/, then lock it initialized.
argument-hint: (none)
---

# $ca-create-context — brownfield populate

Wraps an existing codebase in project state without guessing. Dispatches parallel scouts to read the repository, synthesizes their findings into the surviving `.codearbiter/` doc set, resolves gaps via a targeted interview, and locks the project initialized. No arguments — the skill reads the repo and asks only what it cannot determine.

The only permitted path to populate `.codearbiter/` when meaningful source code already exists. For a greenfield project with no source, use `$ca-decompose`.

## Routes to

The `context-creation` skill (`${CLAUDE_PLUGIN_ROOT}/routines/context-creation/SKILL.md`) — six gated
phases: pre-flight, scout dispatch, synthesis, gap interview, write, lock. Scouts return paths, line
numbers, and named values only — never raw source or secret values. The skill is canonical for the
phases and their gates.

## When NOT to use

- Project already initialized (`<!--INITIALIZED-->` in `CONTEXT.md`) → `$ca-status`.
- Greenfield project, no source → `$ca-decompose`.
- `.codearbiter/` not yet scaffolded → `$ca-init` first.
- Update one doc → edit `<project-root>/.codearbiter/` directly or use `$ca-feature`.

## Hard gate

BLOCK if `<!--INITIALIZED-->` is already present in `CONTEXT.md`. BLOCK if no meaningful source exists
(route to `$ca-decompose`). BLOCK if any scout fails to return before synthesis. BLOCK if any
`[CONFIRM-NN]` exits the gap interview unresolved and undeferred. MUST NOT write `<!--INITIALIZED-->`
until every gap is resolved or deferred to `open-questions.md`.
