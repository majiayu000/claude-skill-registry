---
name: git-commit-message
description: "Use only when the user explicitly asks for a git commit message or semantic commit guidance. Goal: commit messages are semantic and communicate the change intent and effect clearly."
---

# Git Commit Message

Generate one semantic commit message that captures the change at the right level: intent and effect first, details second.

## Response Contract

- Deliverable: no artifact changes.
- Chat output: provide one recommended commit message and one sentence explaining the chosen type, scope, and summary.

## Message Model

### Default format

`<type>(<scope>): <summary>`

Omit `(scope)` when it does not add signal.

### Components

- **Type**: the change class.
- **Scope**: the primary area changed, when it improves precision.
- **Summary**: a short statement of intent and effect.

## Standards

Apply these standards throughout the suggestion. Each standard is single-sourced here and referenced elsewhere by its ID.

- **format.default — Default format**
  Use the default format and omit scope when it is unclear or low-signal.

- **type.minimal — Minimal accurate type**
  Choose the smallest type that fits the change: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`.

- **scope.signal — Scope adds signal**
  Use a narrow, stable scope that names the main area changed. Avoid repeating obvious repo or product context.

- **summary.intent_effect — Intent and effect first**
  Prefer the user’s stated intent and the observable effect of the change over mechanical descriptions of edits.

- **signal.dense — Dense and non-redundant**
  Keep `type`, `scope`, and `summary` complementary. Avoid overlap and embellishment.

## Workflow

1. Extract the user’s stated intent, the change’s effect, and the primary area.
2. Select type. Apply `type.minimal`.
3. Select scope only if it adds precision. Apply `scope.signal`, `format.default`.
4. Write a concise summary focused on intent and effect. Apply `summary.intent_effect`, `signal.dense`.
5. Emit the final message per the Response Contract.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `format.default`, `type.minimal`, `scope.signal`, `summary.intent_effect`, `signal.dense`.
