---
name: gh-issue-fix-flow
description: End-to-end GitHub issue fix workflow using gh, local code changes, builds/tests, and git push. Use when asked to take an issue number, inspect the issue via gh, implement a fix, run XcodeBuildMCP builds/tests, commit with a closing message, and push.
---

# Gh Issue Fix Flow

## Overview

Resolve a GitHub issue from intake through fix, validation, and push using gh, local edits, XcodeBuildMCP, and git.

## Workflow

### 1) Intake and issue context

1. Use `gh issue view <id> --repo <owner/repo> --comments` to get the full issue context.
2. If the repo is unclear, run `gh repo view --json nameWithOwner` to confirm.
3. Capture reproduction steps, expected behavior, and any maintainer notes.

### 2) Locate the code path

1. Use `rg -n` to locate likely files and entry points.
2. Read the relevant code paths with `sed -n` or `rg -n` context.
3. Follow repo-specific conventions (AGENTS/CLAUDE instructions).

### 3) Implement the fix

1. Edit the minimal set of files.
2. Keep changes aligned with existing architecture and style.
3. Add tests when behavior changes and test coverage is practical.

### 4) Build and test

1. Use XcodeBuildMCP for required builds/tests:
   - Set defaults once: `mcp__XcodeBuildMCP__session-set-defaults`.
   - Build: `mcp__XcodeBuildMCP__build_macos` or `mcp__XcodeBuildMCP__build_sim`.
   - Tests: prefer targeted schemes (e.g., `mcp__XcodeBuildMCP__test_sim`).
2. If macOS tests fail due to deployment target mismatches, run the equivalent iOS simulator tests.
3. Report warnings or failures; do not hide them.

### 5) Commit and push

1. Check for unrelated changes with `git status --short`.
2. Stage only the fix (exclude unrelated files).
3. Commit with a closing message: `Fix … (closes #<issue>)`.
4. Push with `git push`.

### 6) Report back

1. Summarize what changed and where.
2. Provide test results (including failures).
3. Note any follow-ups or blocked items.
