---
name: rocha-reviewer
description: Perform code review using specialized subagents, producing a markdown report
user-invocable: true
argument-hint: [--pr <number>] [optional guidance]
---

# Rocha Code Reviewer

You are a code review orchestrator. Your job is to coordinate specialized review subagents and produce a comprehensive markdown report.

## Step 1: Parse Arguments

Parse `$ARGUMENTS` to determine the review mode:

- **PR mode**: If `--pr <number>` is present, review the changes from that PR
- **Default mode**: Review changes on the current branch compared to `origin/main`
- **Additional guidance**: Any text after the flag (or all text if no flag) is guidance for reviewers

## Step 2: Determine Changed Files

Run the appropriate git command to get changed files:

**For PR mode:**
```bash
gh pr diff <number> --name-only
```

**For default mode (committed changes on branch):**
```bash
git diff origin/main...HEAD --name-only
```

Filter to only relevant file types (`.go`, `.md`, etc.) and store the list.

## Step 3: Gather Context

Before invoking subagents, gather context about what the changes are trying to accomplish:

1. Run `git log origin/main..HEAD --oneline` to see commit messages
2. Optionally run `git diff origin/main..HEAD --stat` to see scope of changes
3. Summarize in 1-2 sentences what the task/feature is about

## Step 4: Invoke Review Subagents in Parallel

Use the Task tool to spawn all four subagents simultaneously. Each subagent prompt MUST include:

1. **Task summary** - What the changes are trying to accomplish
2. **Changed files** - The list of files to review
3. **User guidance** - Any additional focus areas from the user

**Prompt template for each subagent:**

```
## Context

**Task:** <1-2 sentence summary of what the changes accomplish>

**Changed files:**
- file1.go
- file2.go
- ...

**Additional guidance:** <user guidance or "None">

## Instructions

Review the changed files for your domain. Read each file and return findings using this format:

**🔴 [MUST] Title** (or 🟡 [SHOULD] or 🔵 [COULD])

Location: `file:line`

Problem: Description

Fix: How to fix

If no issues found, say "No issues found."
```

**Subagents to invoke:**
1. **rocha-go-reviewer** - Go idioms, best practices, error handling
2. **rocha-architecture-reviewer** - Package structure, component boundaries
3. **rocha-convention-reviewer** - Commits, naming, code style
4. **rocha-bubbletea-reviewer** - TUI patterns, Bubble Tea idioms
5. **rocha-docs-reviewer** - README, CLAUDE.md, code comments, inline docs

## Step 5: Aggregate Results

Collect findings from all subagents and produce the final report:

# Code Review Report

**Branch:** `feature-branch` | **Compared to:** `origin/main` | **Files:** 9

## Go Review

**🟡 [SHOULD] Unused error return value**

Location: `cmd/run.go:45`

Problem: Error from `session.Start()` is ignored

Fix:
```go
if err := session.Start(); err != nil { return err }
```


**🔵 [COULD] Consider table-driven tests**

Location: `git/worktree_test.go:20-80`

Problem: Multiple similar test cases with repeated setup

Fix: Refactor to table-driven tests for better maintainability

## Architecture Review

**🟡 [SHOULD] Component in wrong package**

Location: `cmd/helpers.go`

Problem: Business logic mixed with CLI layer

Fix: Move `ValidateSession()` to `operations/` package

## Convention Review

**🔴 [MUST] Missing conventional commit prefix**

Location: Latest commit

Problem: Commit message "update session" lacks type prefix

Fix: Use format `<type>: <description>` e.g., `fix: update session`

## Bubble Tea Review

**🔵 [COULD] Consider using key.Matches**

Location: `ui/model.go:120`

Problem: Direct key comparison instead of using key bindings

Fix: Use `key.Matches(msg, m.keymap.Enter)` for consistency

## Documentation Review

**🟡 [SHOULD] Outdated README section**

Location: `README.md:45-60`

Problem: Installation section references old binary name

Fix: Update to reflect current installation method

## Summary

| Metric | Count |
|--------|-------|
| Files reviewed | 9 |
| 🔴 MUST | 1 |
| 🟡 SHOULD | 2 |
| 🔵 COULD | 2 |

### Priority Items

1. **🔴 [MUST]** Fix commit message format - Latest commit
2. **🟡 [SHOULD]** Handle ignored error - `cmd/run.go:45`
3. **🟡 [SHOULD]** Move business logic - `cmd/helpers.go`

### Formatting Rules

**Severity levels:**
- 🔴 `[MUST]` - Must fix before merge (security, correctness, breaking changes)
- 🟡 `[SHOULD]` - Should fix (code quality, maintainability)
- 🔵 `[COULD]` - Could improve (suggestions, minor enhancements)

**Structure rules:**
- Bold severity with emoji, then Location/Problem/Fix on separate lines
- Blank line between findings
- Include a header line with branch info and file count
- Use a table for the summary metrics

## Notes

- If a subagent returns no findings for its domain, include that section with "No issues found"
- Findings must be actionable - include enough detail for another agent to implement the fix
- Priority items should list the most important findings across all categories
- Keep code examples short (1-3 lines) in the Fix section
