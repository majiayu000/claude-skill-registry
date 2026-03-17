---
name: retro-resolve
description: Scan retro.md files across all skills, resolve open issues, and update retro entries.
argument-hint: "[--skill <name>] [--dry-run]"
allowed-tools: Bash, Write, Read, Glob, Grep, Edit
---

## Purpose

Batch-process open retro issues across all skills. Reads each `status: open` entry, investigates the root cause, applies the fix, and updates the retro entry.

## Arguments

- `--skill <name>` — Only process issues for a specific skill (default: all skills)
- `--dry-run` — Report open issues without applying fixes

## Workflow

### 1. Discover

Glob for `**/retro.md` in the skills directory. Parse each file for entries containing `status: open`.

### 2. Report

Print: "Found N open issues across M skills" with a summary table.

If `--dry-run`, stop here.

### 3. Resolve (sequential by skill)

For each open entry:

1. **Read context** — read the skill's SKILL.md and any referenced files
2. **Read the retro entry** — understand context, root-cause, and resolution-hint
3. **Investigate** — determine the fix (read relevant code, templates, references)
4. **Apply the fix** — edit SKILL.md, template, or reference file
5. **Update the retro entry:**
   - Replace `status: open` with a description of what was changed
   - Add `files-changed` listing modified files
   - Append `(resolved by /retro-resolve YYYY-MM-DD)` to the fix line

### 4. Summary

Print a table listing each issue, its skill, and resolution status (fixed / skipped / needs-review).

## Constraints

- Do not change skill behavior or semantics — only fix gaps, errors, and omissions
- If a fix would change behavior significantly, leave the entry open and add a review note
- Process issues sequentially within each skill (related issues may interact)
- Always read the skill's SKILL.md before attempting a fix
