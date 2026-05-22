---
name: document-changes
description: >-
  Generate a markdown report documenting codebase changes from the current session —
  files added, modified, deleted, and a summary of what was done. Use when asked to
  "document changes", "generate change report", "save changes report", "what did I change",
  "session report", "summarize my changes", or "write a changes report".
argument-hint: "[scope-or-description]"
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

# Document Changes

Generate a structured markdown report documenting codebase changes from the current working session. The report captures files changed, commit history, and a human-readable summary suitable for team reviews, handoff documentation, or personal records.

## Arguments

- `$ARGUMENTS` — Optional scope or description for the report (e.g., `"auth refactor"`, `"add OAuth2 support"`). Used to name the output file and populate the report's scope field. If not provided, scope is inferred from commit messages or changed file paths.

## Workflow

Execute these 4 steps in order. **Stop early** if Step 1 or Step 2 determines there is nothing to report.

---

### Step 1: Validate Git Repository

Verify the current directory is inside a git repository:

```bash
git rev-parse --is-inside-work-tree
```

- If the command fails or returns `false`, stop and report: "Not inside a git repository. This skill requires git to gather change data."
- If successful, continue to Step 2.

---

### Step 2: Gather Changes and Metadata

Collect all change data by running these git commands. If any individual command fails, continue with the data that is available.

#### 2.1 Repository Metadata

```bash
git branch --show-current
```

```bash
git config user.name
```

```bash
git remote get-url origin 2>/dev/null
```

```bash
date "+%Y-%m-%d %H:%M %Z"
```

#### 2.2 Uncommitted Changes

```bash
git status --porcelain
```

```bash
git diff --stat
```

```bash
git diff --name-status
```

#### 2.3 Staged Changes

```bash
git diff --cached --stat
```

```bash
git diff --cached --name-status
```

#### 2.4 Recent Commits (up to 20)

```bash
git log --oneline -20
```

```bash
git log --format="%H|%s|%an|%ai" -20
```

#### 2.5 Session Commit Diffs

If there are recent commits (N > 0 from Step 2.4):

```bash
git diff --stat HEAD~N..HEAD
```

```bash
git diff --name-status HEAD~N..HEAD
```

Replace `N` with the number of recent commits found (capped at 20). If the repo has fewer than N commits, use `git diff --stat $(git rev-list --max-parents=0 HEAD)..HEAD` instead.

#### 2.6 Combine and Deduplicate

Build a unified list of all affected files from Steps 2.2–2.5, deduplicating entries. For each file, track:
- **Status**: Added (A), Modified (M), Deleted (D), Renamed (R)
- **Source**: Whether the change is committed, staged, unstaged, or untracked

**Stop condition:** If there are no uncommitted changes (Step 2.2 is empty), no staged changes (Step 2.3 is empty), and no recent commits (Step 2.4 is empty), stop and report: "No changes found in the current repository. Nothing to document."

---

### Step 3: Determine Report Location

#### 3.1 Generate Filename Description

Create a short kebab-case description (2-4 words) for the filename:
- **If `$ARGUMENTS` is provided**: Convert to kebab-case (e.g., `"auth refactor"` → `auth-refactor`)
- **If `$ARGUMENTS` is not provided**: Infer from the most common theme in commit messages or changed file paths (e.g., `api-bug-fixes`, `add-oauth2-support`, `ui-component-updates`)

Build the recommended path: `internal/reports/<description>-YYYY-MM-DD.md` using today's date.

#### 3.2 Ask User for Report Location

Use `AskUserQuestion`:

```
Where should the change report be saved?

Recommended: internal/reports/<description>-YYYY-MM-DD.md
```

Options:
1. "Use recommended path (Recommended)" — Save to `internal/reports/<description>-YYYY-MM-DD.md`
2. "Custom path" — User provides their own file path

**If user selects "Custom path":** Use a follow-up `AskUserQuestion` asking for the full file path.

#### 3.3 Validate Path

- The path must end with `.md`
- If the parent directory does not exist, create it with `mkdir -p`

---

### Step 4: Generate and Write Report

Build the markdown report with the following structure, then write it using the `Write` tool.

#### Report Template

```markdown
# Codebase Changes Report

## Metadata

| Field | Value |
|-------|-------|
| **Date** | YYYY-MM-DD |
| **Time** | HH:MM TZ |
| **Branch** | {current branch} |
| **Author** | {git user.name} |
| **Base Commit** | {earliest commit hash before session changes, or N/A} |
| **Latest Commit** | {most recent commit hash, or "uncommitted"} |
| **Repository** | {remote URL, or "local only"} |

**Scope**: {from $ARGUMENTS, or inferred from changes}

**Summary**: {1-2 sentence executive summary of what was done}

## Overview

{High-level stats paragraph}

- **Files affected**: N
- **Lines added**: +N
- **Lines removed**: -N
- **Commits**: N

## Files Changed

| File | Status | Lines | Description |
|------|--------|-------|-------------|
| `path/to/file.ts` | Modified | +12 / -3 | Brief description of changes |
| `path/to/new.ts` | Added | +45 | Brief description |
| `path/to/old.ts` | Deleted | -20 | Brief description |

## Change Details

### Added

- **`path/to/new.ts`** — Description of the new file and its purpose.

### Modified

- **`path/to/file.ts`** — What was changed and why (based on diff context).

### Deleted

- **`path/to/old.ts`** — Why it was removed or what replaced it.

## Git Status

### Staged Changes

{List of staged files from `git diff --cached --name-status`, or "No staged changes."}

### Unstaged Changes

{List of unstaged modifications from `git diff --name-status`, or "No unstaged changes."}

### Untracked Files

{List of untracked files from `git status --porcelain` (lines starting with `??`), or "No untracked files."}

## Session Commits

| Hash | Message | Author | Date |
|------|---------|--------|------|
| `abc1234` | feat: add login flow | Author Name | 2026-02-21 |

{Or "No commits in this session." if no recent commits}
```

#### Writing the Report

1. If the parent directory does not exist, create it:
   ```bash
   mkdir -p {parent_directory}
   ```
2. Use the `Write` tool to create the report file at the chosen path.
3. If the write fails, report the error and use `AskUserQuestion` to offer an alternative path.

#### Present Summary

After writing the report, present a brief summary of what was generated, then use `AskUserQuestion`:

```
Report written to {path}.

Summary: {1-2 sentence overview}
Files documented: N | Commits: N | Lines: +N / -N

What would you like to do next?
```

Options:
1. "Review report" — Read the report back to the user using `Read`
2. "Commit changes" — Suggest using `/git-commit` to commit outstanding changes
3. "Done" — End the workflow

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Not a git repo | Stop with clear message (Step 1) |
| No changes found | Stop with clear message (Step 2) |
| Individual git command fails | Continue with available data |
| Write fails | Offer alternative path via AskUserQuestion |
| Cannot determine scope | Use `"session-changes"` as the fallback description |

## Section Guidelines

- **Omit empty sections**: If a section has no data (e.g., no deleted files, no untracked files), omit that section or subsection entirely rather than showing "None."
- **File descriptions**: Generate brief descriptions from diff context and file names. Keep each to one sentence.
- **Commit hashes**: Use short hashes (7 characters) in the report for readability.
- **Line counts**: Use `--stat` output to extract per-file line additions/deletions. If unavailable, omit the Lines column.
