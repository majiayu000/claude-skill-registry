---
name: git-branch-namer
description: "Use only when the user explicitly asks for a git branch name or naming suggestion. Goal: branch names are convention-aligned and communicate type, scope, and intent at a glance."
---

# Git Branch Namer

Suggest a git branch name that encodes type, scope, and intent with high information density and minimal redundancy.

## Response Contract

- Deliverable: no artifact changes.
- Chat output: provide one recommended branch name and one sentence explaining the chosen type, scope, and intent.

## Naming Model

### Default pattern

Use `<type>/<scope>/<intent>` unless the user specifies another convention.

### Components

- **Type**: the change class.
- **Scope**: the primary area being changed.
- **Intent**: a concise action phrase describing the work.

## Standards

Apply these standards throughout the suggestion. Each standard is single-sourced here and referenced elsewhere by its ID.

- **pattern.follow — Follow the user’s convention**
  If the user provides a naming convention, follow it. Otherwise use the default pattern.

- **type.minimal — Minimal accurate type**
  Choose the smallest type that fits the change: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`.

- **scope.primary — Primary scope**
  Choose a scope that names the main module, product area, or capability being changed.

- **intent.form — Intent form**
  Intent must be verb-first kebab-case.

- **signal.dense — Dense and non-redundant**
  Avoid repeating scope terms in intent unless it adds clarity. Do not encode obvious repo context.

## Workflow

1. Determine the pattern from the user’s convention or the default. Apply `pattern.follow`.
2. Select type. Apply `type.minimal`.
3. Select scope. Apply `scope.primary`.
4. Write intent. Apply `intent.form`, `signal.dense`.
5. Output per Response Contract.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `pattern.follow`, `type.minimal`, `scope.primary`, `intent.form`, `signal.dense`.
