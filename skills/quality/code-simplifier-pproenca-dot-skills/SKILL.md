---
name: code-simplifier
description: Code simplification skill for improving clarity, consistency, and maintainability while preserving exact behavior. Use when simplifying code, reducing complexity, cleaning up recent changes, applying refactoring patterns, or improving readability. Triggers on tasks involving code cleanup, simplification, refactoring, or readability improvements.
---

# Community Code Simplification Best Practices

Comprehensive code simplification guide for AI agents and LLMs. Contains 45 rules across 8 categories, prioritized by impact from critical (context discovery, behavior preservation) to incremental (language idioms). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics.

## Core Principles

1. **Context First**: Understand project conventions before making any changes
2. **Behavior Preservation**: Change how code is written, never what it does
3. **Scope Discipline**: Focus on recently modified code, keep diffs small
4. **Clarity Over Brevity**: Explicit, readable code beats clever one-liners

## When to Apply

Reference these guidelines when:
- Simplifying or cleaning up recently modified code
- Reducing nesting, complexity, or duplication
- Improving naming and readability
- Applying language-specific idiomatic patterns
- Reviewing code for maintainability issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Context Discovery | CRITICAL | `ctx-` | 5 |
| 2 | Behavior Preservation | CRITICAL | `behave-` | 6 |
| 3 | Scope Management | HIGH | `scope-` | 5 |
| 4 | Control Flow Simplification | HIGH | `flow-` | 7 |
| 5 | Naming and Clarity | MEDIUM-HIGH | `name-` | 5 |
| 6 | Duplication Reduction | MEDIUM | `dup-` | 5 |
| 7 | Dead Code Elimination | MEDIUM | `dead-` | 5 |
| 8 | Language Idioms | LOW-MEDIUM | `idiom-` | 7 |

## Quick Reference

### 1. Context Discovery (CRITICAL)

- [`ctx-read-claude-md`](references/ctx-read-claude-md.md) - Always read CLAUDE.md before simplifying
- [`ctx-detect-lint-config`](references/ctx-detect-lint-config.md) - Check for linting and formatting configs
- [`ctx-follow-existing-patterns`](references/ctx-follow-existing-patterns.md) - Match existing code style in file and project
- [`ctx-project-over-generic`](references/ctx-project-over-generic.md) - Project conventions override generic best practices
- [`ctx-identify-scope`](references/ctx-identify-scope.md) - Identify recently modified code as default scope

### 2. Behavior Preservation (CRITICAL)

- [`behave-preserve-outputs`](references/behave-preserve-outputs.md) - Preserve all return values and outputs
- [`behave-preserve-errors`](references/behave-preserve-errors.md) - Preserve error messages, types, and handling
- [`behave-preserve-api`](references/behave-preserve-api.md) - Preserve public function signatures and types
- [`behave-preserve-side-effects`](references/behave-preserve-side-effects.md) - Preserve side effects (logging, I/O, state changes)
- [`behave-no-semantics-change`](references/behave-no-semantics-change.md) - Forbid subtle semantic changes
- [`behave-verify-before-commit`](references/behave-verify-before-commit.md) - Verify behavior preservation before finalizing

### 3. Scope Management (HIGH)

- [`scope-recent-code-only`](references/scope-recent-code-only.md) - Focus on recently modified code only
- [`scope-minimal-diff`](references/scope-minimal-diff.md) - Keep changes small and reviewable
- [`scope-no-unrelated-refactors`](references/scope-no-unrelated-refactors.md) - No unrelated refactors
- [`scope-no-global-rewrites`](references/scope-no-global-rewrites.md) - Avoid global rewrites and architectural changes
- [`scope-respect-boundaries`](references/scope-respect-boundaries.md) - Respect module and component boundaries

### 4. Control Flow Simplification (HIGH)

- [`flow-early-return`](references/flow-early-return.md) - Use early returns to reduce nesting
- [`flow-guard-clauses`](references/flow-guard-clauses.md) - Use guard clauses for preconditions
- [`flow-no-nested-ternaries`](references/flow-no-nested-ternaries.md) - Never use nested ternary operators
- [`flow-explicit-over-dense`](references/flow-explicit-over-dense.md) - Prefer explicit control flow over dense expressions
- [`flow-flatten-nesting`](references/flow-flatten-nesting.md) - Flatten deep nesting to maximum 2-3 levels
- [`flow-single-responsibility`](references/flow-single-responsibility.md) - Each code block should do one thing
- [`flow-positive-conditions`](references/flow-positive-conditions.md) - Prefer positive conditions over double negatives

### 5. Naming and Clarity (MEDIUM-HIGH)

- [`name-intention-revealing`](references/name-intention-revealing.md) - Use intention-revealing names
- [`name-nouns-for-data`](references/name-nouns-for-data.md) - Use nouns for data, verbs for actions
- [`name-avoid-abbreviations`](references/name-avoid-abbreviations.md) - Avoid cryptic abbreviations
- [`name-consistent-vocabulary`](references/name-consistent-vocabulary.md) - Use consistent vocabulary throughout
- [`name-avoid-generic`](references/name-avoid-generic.md) - Avoid generic names

### 6. Duplication Reduction (MEDIUM)

- [`dup-rule-of-three`](references/dup-rule-of-three.md) - Apply the rule of three
- [`dup-no-single-use-helpers`](references/dup-no-single-use-helpers.md) - Avoid single-use helper functions
- [`dup-extract-for-clarity`](references/dup-extract-for-clarity.md) - Extract only when it improves clarity
- [`dup-avoid-over-abstraction`](references/dup-avoid-over-abstraction.md) - Prefer duplication over premature abstraction
- [`dup-data-driven`](references/dup-data-driven.md) - Use data-driven patterns over repetitive conditionals

### 7. Dead Code Elimination (MEDIUM)

- [`dead-remove-unused`](references/dead-remove-unused.md) - Delete unused code artifacts
- [`dead-delete-not-comment`](references/dead-delete-not-comment.md) - Delete code, never comment it out
- [`dead-remove-obvious-comments`](references/dead-remove-obvious-comments.md) - Remove comments that state the obvious
- [`dead-keep-why-comments`](references/dead-keep-why-comments.md) - Keep comments that explain why, not what
- [`dead-remove-todo-fixme`](references/dead-remove-todo-fixme.md) - Remove stale TODO/FIXME comments

### 8. Language Idioms (LOW-MEDIUM)

- [`idiom-ts-strict-types`](references/idiom-ts-strict-types.md) - Use strict types over any (TypeScript)
- [`idiom-ts-const-assertions`](references/idiom-ts-const-assertions.md) - Use const assertions and readonly (TypeScript)
- [`idiom-rust-question-mark`](references/idiom-rust-question-mark.md) - Use ? for error propagation (Rust)
- [`idiom-rust-iterator-chains`](references/idiom-rust-iterator-chains.md) - Use iterator chains when clearer (Rust)
- [`idiom-python-comprehensions`](references/idiom-python-comprehensions.md) - Use comprehensions for simple transforms (Python)
- [`idiom-go-error-handling`](references/idiom-go-error-handling.md) - Handle errors immediately (Go)
- [`idiom-prefer-language-builtins`](references/idiom-prefer-language-builtins.md) - Prefer language and stdlib builtins

## Workflow

1. **Discover context**: Read CLAUDE.md, lint configs, examine existing patterns
2. **Identify scope**: Focus on recently modified code unless asked to expand
3. **Apply transformations**: Use rules in priority order (CRITICAL first)
4. **Verify behavior**: Ensure outputs, errors, and side effects remain identical
5. **Keep diffs minimal**: Small, focused changes that are easy to review

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
