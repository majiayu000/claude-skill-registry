---
name: branch-naming
description: Defines branch naming conventions for issue work. Use when creating branches for issues, understanding work status from branches, or linking commits to issues.
---

# Branch Naming Conventions

## Purpose

This skill establishes consistent branch naming conventions that:
1. Clearly link branches to GitHub issues
2. Enable automated detection of work status
3. Support the issue-review skill in determining issue states

## Branch Naming Format

### Standard Pattern

```
<issue-number>-<short-description>
```

**Examples:**
- `42-build-caching`
- `15-linker-error-fix`
- `28-simplify-job-system`

### Claude-Specific Branches

When Claude Code creates branches, use this pattern:

```
claude/<issue-number>-<short-description>-<session-id>
```

**Examples:**
- `claude/42-build-caching-Abc12`
- `claude/15-linker-error-Xyz99`

The session ID suffix ensures uniqueness across multiple Claude sessions.

## Naming Rules

### DO:
- Start with the issue number
- Use lowercase letters and hyphens only
- Keep descriptions short (2-4 words)
- Use descriptive slugs that summarize the work

### DON'T:
- Use spaces or underscores
- Include special characters (except hyphens)
- Create overly long branch names (max ~50 chars)
- Omit the issue number for issue-related work

### Examples

| Good | Bad | Why |
|------|-----|-----|
| `42-build-caching` | `42` | Too vague |
| `15-null-ptr-fix` | `15-fix-the-bug-where-null-pointer-exception-occurs` | Too long |
| `28-refactor-parser` | `28-misc-changes` | Not descriptive |

## Commit Message Conventions

### Keywords for Issue Linking

| Keyword | Effect | Use When |
|---------|--------|----------|
| `Fixes #N` | Closes issue when PR merges | Work completely resolves the issue |
| `Closes #N` | Closes issue when PR merges | Same as Fixes |
| `Refs #N` | Links without closing | Work is partial or related |

### Examples

```
Add build result caching

Implement file-based caching for compilation results.

Fixes #42
```

```
Extract cache module

Move caching logic to dedicated module.

Refs #42
```

## Detecting Work Status from Branches

The issue-review skill can determine issue status by analyzing branches:

### Branch Detection

```bash
# Find branches for a specific issue
git branch -a | grep -E "^[^/]*${ISSUE_NUMBER}-|/${ISSUE_NUMBER}-"

# Or using GitHub CLI
gh pr list --search "head:${ISSUE_NUMBER}" --state all --json number,state,isDraft,headRefName
```

### Status Inference

| Branch State | PR State | Inferred Issue Status |
|--------------|----------|----------------------|
| Branch exists, no PR | - | **In-progress** |
| Branch exists, draft PR | Draft | **In-progress** |
| Branch exists, open PR | Open (ready) | **Ready to Review** |
| Branch merged | PR Merged | **Done** |
| Branch deleted, PR closed | Closed (not merged) | Work abandoned, check issue |

## Workflow Integration

### Starting Work on an Issue

1. **Create branch:**
   ```bash
   git checkout -b 42-build-caching
   ```

2. **Make commits with issue references:**
   ```bash
   git commit -m "Implement cache storage

   Refs #42"
   ```

3. **Create PR:**
   ```bash
   gh pr create --title "Add build caching (#42)" \
     --body "Implements build result caching.

   Fixes #42"
   ```

### Issue-Review Integration

The issue-review skill uses branch/PR information to:

1. **Detect work in progress:**
   - Search for branches containing issue numbers
   - Check for draft PRs linked to issues

2. **Verify status accuracy:**
   - Issue marked "Ready to Review" should have an open PR
   - Issue marked "In-progress" should have a branch or draft PR
   - Issue marked "Done" should have a merged PR

3. **Identify stale work:**
   - Branches with no commits in 14+ days
   - Draft PRs with no updates in 7+ days

## Quick Reference

### Branch Naming

```
<issue>-<description>           # Standard
claude/<issue>-<desc>-<session> # Claude sessions
```

### Commit Keywords

```
Fixes #N    # Closes issue on merge
Closes #N   # Closes issue on merge
Refs #N     # Links without closing
```

### Status Detection

```
Branch only           → In-progress
Branch + Draft PR     → In-progress
Branch + Open PR      → Ready to Review
Merged PR             → Done
No branch/PR          → Check issue status
```

## Guidelines

- Always include issue numbers in branch names for trackable work
- Keep branch names concise but descriptive
- Reference issues in commits for traceability
- Use closing keywords only when work fully resolves the issue
- Delete branches after PR merge to keep repository clean
