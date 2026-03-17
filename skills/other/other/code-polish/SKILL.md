---
argument-hint: ''
context: fork
disable-model-invocation: false
name: code-polish
user-invocable: true
description: This skill should be used when the user asks to "polish code", "simplify and review", "clean up and review code", "full code polish", "simplify then review", "refactor and review", "simplify and fix", "clean up and fix", or wants a combined simplification and review workflow on recently changed code.
---

# Code Polish

Combined simplification and review pipeline. This skill orchestrates two sub-skills in sequence:

1. **`code-simplify`** — simplify for readability and maintainability
2. **`code-review --fix`** — review for correctness, security, and quality, auto-applying all fixes

Both sub-skills share the same scope resolution: **only** session-modified files are in scope. If there are no session-modified files, they fall back to all uncommitted tracked changes. See each sub-skill for full details.

## Workflow

### 1) Run `code-simplify`

Invoke the `code-simplify` skill, forwarding `$ARGUMENTS` as-is.

### 2) Run `code-review --fix`

Invoke the `code-review` skill with the `--fix` flag appended to `$ARGUMENTS`.

### 3) Report

Combine the outputs from both skills into a single summary:

1. **Scope**: Files and functions touched.
2. **Simplifications**: Key changes from `code-simplify`.
3. **Review findings and fixes**: Findings and applied fixes from `code-review`.
4. **Verification**: Commands run and outcomes.
5. **Residual risks**: Assumptions or items needing manual review.
