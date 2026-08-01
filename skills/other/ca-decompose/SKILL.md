---
name: ca-decompose
description: Greenfield decomposition interview — a layered interview that populates .codearbiter/ and locks it initialized.
argument-hint: (none)
---

# /ca-decompose — greenfield populate

Stands up project state for a greenfield project — one with no meaningful source code yet. A senior-architect persona drives a six-layer interview eliciting purpose, scope, primary users, domain vocabulary, and architectural constraints, persisting each layer to disk so a context reset loses nothing, then writes the surviving `.codearbiter/` doc set and locks the project initialized. No arguments — the skill interviews the user (a handoff summary may be supplied freely during the interview).

The only permitted path to populate `.codearbiter/` when no meaningful source exists. For an existing codebase, use `/ca-create-context`.

## Routes to

The `decompose` skill (`<plugin-root>/routines/decompose/SKILL.md`) — six gated phases:
pre-flight, persona adoption, layered interview, synthesis, population, lock. The skill is canonical
for the layers and their gates.

## When NOT to use

- Project already initialized (`<!--INITIALIZED-->` in `CONTEXT.md`) → `/ca-status`.
- Existing codebase with source present → `/ca-create-context`.
- `.codearbiter/` not yet scaffolded → `/ca-init` first.
- Update one doc → edit `<project-root>/.codearbiter/` directly or use `/ca-feature`.

## Hard gate

BLOCK if `<!--INITIALIZED-->` is already present in `CONTEXT.md`. BLOCK if meaningful source is
detected (route to `/ca-create-context`). BLOCK if any `[CONFIRM-NN]` exits synthesis unresolved and
undeferred. MUST NOT write `<!--INITIALIZED-->` until every required doc is present and non-empty.
