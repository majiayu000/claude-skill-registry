---
name: deterministic-checks
description: Use before committing, opening a PR, or reporting a task done — when you want ground-truth confirmation there are no conflict markers, live-looking credentials, debug leftovers, untracked TODOs, or oversized files, without spending a model turn re-reading every file yourself.
---

# Deterministic Checks

## Overview

A shell script that scans a repository for five specific, mechanically-detectable problems and reports file:line locations. Zero model cost — it never asks Claude to "be careful" about something a regex can already prove.

**Core principle:** If a check can be regex or `wc -c`, it should never be a paragraph of instructions asking the model to look carefully. Reserve judgment calls for the model; hand mechanical checks to the script.

## What it checks

| Check | Catches | Misses (by design) |
|---|---|---|
| Conflict markers | `<<<<<<<`, `=======`, `>>>>>>>` at line start | Markers inside a fenced code block that's *documenting* conflict markers (a known false-positive class — see below) |
| Live-looking credentials | AWS keys, GitHub tokens, PEM private keys, `sk-`-style API keys | Anything not matching those four shapes — this is not a general secret scanner |
| Debug leftovers | `console.log`/`console.debug`, `debugger;`, `pdb.set_trace()`, `binding.pry` in JS/TS/Python/Go/Ruby files | Debug prints in languages/patterns not listed |
| Untracked TODO/FIXME | `TODO`/`FIXME`/`XXX` with no `#123` or `TICKET-123` reference nearby | TODOs that reference a ticket — those are considered tracked |
| Oversized files | Any file over 5MB, excluding lockfiles and `.min.js` | Nothing — this one has no heuristic gap |

## Usage

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/scan.sh [path]   # defaults to .
```

Exit code 0 = clean, 1 = findings printed to stdout, 2 = usage error. In a git repo it scans tracked + untracked-but-not-ignored files (via `git ls-files`); outside git it walks the filesystem, skipping `node_modules`, `.git`, `dist`, `build`, `vendor`.

**Excluding a path** (e.g. a docs file that intentionally shows conflict-marker syntax):

```bash
SCAN_EXCLUDE='path/to/docs-with-examples\.md' bash ${CLAUDE_SKILL_DIR}/scripts/scan.sh .
```

`SCAN_EXCLUDE` is a `grep -Ev` pattern matched against each file path.

## Known false-positive class

Any file that *documents* these patterns — a git tutorial showing `<<<<<<< HEAD`, a security post pasting a fake `AKIA...` example, this skill's own README — will trigger a match. The script cannot distinguish "this is a real conflict" from "this is prose about conflicts" with a line-oriented regex. When a finding is a documentation example, exclude that path with `SCAN_EXCLUDE` rather than trying to make the regex smarter — a regex that understands fenced-code-block context is not worth the fragility it adds. This is the same trade every pre-commit secret scanner makes.

## When to use vs. when not to

**Use before:** committing, opening a PR, reporting "done" on a task that touched files, merging a branch.

**Don't use for:** language-specific type checking, style/formatting (use the project's linter), security review beyond the four credential shapes above (use `agents/security-audit-prompt.md` for judgment-requiring review), or as a substitute for tests.

## Wiring it as a hook instead of running it manually

This is also usable as a `Stop` hook so it runs automatically instead of you remembering to invoke it — see the `hooks/hooks.json` pattern in [`agents/hooks-automation-prompt.md`](../../../prompts/english/agents/hooks-automation-prompt.md). A `Stop` hook that exits 1 blocks the turn from ending until the findings are addressed or explicitly accepted.

## Remember

> This script proves the absence of five specific problems. It proves nothing else. Don't report "clean" as "reviewed" — it's a floor, not a review.
