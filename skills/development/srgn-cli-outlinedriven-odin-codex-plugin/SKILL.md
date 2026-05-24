---
name: srgn-cli
description: "Practical guide for building safe, syntax-aware srgn CLI commands for source-code search and transformation. Use when users ask for srgn commands, scoped refactors (comments/docstrings/imports/functions), multi-file rewrites with --glob, custom tree-sitter query usage, or CI-style checks with --fail-any/--fail-none."
---

# srgn CLI

## Overview

Use this skill to convert user intent into precise `srgn` commands with safe defaults.
Focus on CLI workflows for search, transformation, scoped migrations, and lint-like checks.

## Workflow Decision Tree

1. Classify the request.
   - Search only: no content changes expected.
   - Transform in stream: stdin/stdout pipeline usage.
   - Transform files: in-place updates over globs.
2. Identify scope strategy.
   - Regex scope only.
   - Language scope only.
   - Combined language + regex scope.
   - Custom tree-sitter query scope.
3. Identify action strategy.
   - Replacement (positional replacement argument after `--`).
   - Composable actions (`--upper`, `--lower`, `--titlecase`, `--normalize`, `--symbols`, `--german`).
   - Standalone actions (`-d`, `-s`).
4. Apply safety controls.
   - Prefer `--dry-run` for file operations.
   - Keep globs quoted.
   - Add `--fail-no-files` when missing files should fail CI.
5. Choose output mode.
   - Human-readable (default tty).
   - Machine-readable (`--stdout-detection force-pipe`).
6. Validate behavior.
   - Confirm expected match count.
   - Confirm no out-of-scope edits.
   - Re-run with stricter scope if needed.

## Safety Protocol

1. Default to non-destructive behavior first.
   - Prefer stdin-based or search-mode examples before in-place rewrites.
2. For file edits, require preview path.
   - Use `--dry-run` first.
   - Then run the same command without `--dry-run` only after confirmation.
3. Protect shell parsing boundaries.
   - Quote regex.
   - Quote globs: `--glob '**/*.py'`.
   - Use `--` before replacement values.
4. Use the narrowest scope that solves the task.
   - Prefer language scope + anchored regex over broad regex-only replacement.
5. Treat `-d` and `-s` as high-risk operations.
   - Always provide explicit scope for them.

## Command Construction Template

Use this template when building commands:

```bash
srgn [LANGUAGE_SCOPE_FLAGS...] [GLOBAL_FLAGS...] [ACTION_FLAGS...] [SCOPE_REGEX] -- [REPLACEMENT]
```

Build incrementally:

1. Scope first.
   - Example: `--python 'imports'`
2. Regex filter second.
   - Example: `'^old_pkg'`
3. Action third.
   - Replacement: `-- 'new_pkg'`
   - Or composable flag: `--upper`
4. File mode flags fourth (if needed).
   - `--glob '**/*.py' --dry-run`
5. CI behavior last.
   - `--fail-any` or `--fail-none`

## High-Value Task Recipes

1. Rename module imports in Python only:
```bash
srgn --python 'imports' '^old_pkg' --glob '**/*.py' --dry-run -- 'new_pkg'
```

2. Convert `print` calls to logging in Python call-sites only:
```bash
srgn --python 'function-calls' '^print$' --glob '**/*.py' --dry-run -- 'logging.info'
```

3. Rename Rust `use` prefixes without touching strings/comments:
```bash
srgn --rust 'uses' '^good_company' --glob '**/*.rs' --dry-run -- 'better_company'
```

4. Remove C# comments only:
```bash
srgn --csharp 'comments' -d '.*'
```

5. Search for Rust `unsafe` language keyword usage only:
```bash
srgn --rust 'unsafe'
```

6. Fail CI if undesirable pattern appears in Python docstrings:
```bash
srgn --python 'doc-strings' --fail-any 'param.+type'
```

7. Force machine-readable output for downstream parsers:
```bash
srgn --python 'strings' --stdout-detection force-pipe '(foo|bar)'
```

8. Preview multi-file changes with deterministic ordering:
```bash
srgn --typescript 'imports' '^legacy-lib' --glob 'src/**/*.ts' --sorted --dry-run -- 'modern-lib'
```

For broader, categorized examples, load `references/cli-cookbook.md`.

## Failure and Debug Playbook

1. No matches when matches are expected.
   - Verify language scope and prepared query name.
   - Remove regex temporarily to test scope alone.
   - Add `--stdout-detection force-pipe` to inspect exact matched columns.
2. Too many matches.
   - Anchor regex (`^...$`) where possible.
   - Narrow from generic language scope to a specific prepared query.
3. Wrong files targeted.
   - Confirm `--glob` pattern and shell quoting.
   - Add `--fail-no-files` in CI to catch empty globs.
4. Unclear behavior across multiple language scopes.
   - Default is intersection (left-to-right narrowing).
   - Use `-j` for OR behavior.
5. Special characters misinterpreted as regex.
   - Use `--literal-string` when literal matching is intended.

## Reference Loading Guide

Load reference files based on request type:

1. `references/cli-cookbook.md`
   - Load for routine command construction and practical recipes.
2. `references/language-scopes.md`
   - Load for prepared query selection by language.
3. `references/advanced-patterns.md`
   - Load for custom queries, capture substitutions, join semantics, and CI failure modes.
4. `references/deepwiki-recursive-notes.md`
   - Load for complete DeepWiki-derived background and architecture context.
## Intent-to-Command Map

Use this map to respond quickly:

1. "Rename imports safely"
   - Use language import scope + anchored regex + `--glob ... --dry-run`.
2. "Update function calls only"
   - Use language call-site scope (for example `--python 'function-calls'`) + exact name regex.
3. "Only comments/docstrings"
   - Use prepared comment/docstring scopes, add `-j` only when OR semantics are required.
4. "CI should fail if pattern appears"
   - Use scoped search + `--fail-any`.
5. "CI should fail if required pattern is missing"
   - Use scoped search + `--fail-none`.
6. "I need parseable output"
   - Use `--stdout-detection force-pipe`.
7. "Regex escaping is painful"
   - Use `--literal-string` and explicit replacement via `--`.

## Execution Checklist

Before returning a final command, verify:

1. Scope is minimal and syntax-aware where possible.
2. Replacement argument is after `--` (if replacement is used).
3. Globs are quoted.
4. `--dry-run` is present for file edits unless user requested direct apply.
5. Join semantics are explicit when multiple language scopes are used (`-j` vs default intersect).
6. Failure flags align with user intent (`--fail-any`, `--fail-none`, `--fail-no-files`).
7. Output mode is explicit if user needs machine parsing.
