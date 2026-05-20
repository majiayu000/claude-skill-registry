---
name: pr-operations
description: Use when working with PR review comments, resolving threads, or replying to discussion comments. Essential for understanding the correct erk exec commands for PR thread operations.
---

# PR Operations Skill

## Core Rule

> **CRITICAL: Use ONLY `erk exec` Commands for PR Thread Operations**
>
> - ❌ DO NOT use raw `gh api` calls for thread operations
> - ❌ DO NOT use `gh pr` commands directly for thread resolution
> - ✅ ONLY use `erk exec` commands listed below
>
> The `erk exec` commands handle thread resolution correctly. Raw API calls only reply without resolving.

## Quick Reference

| Command                       | Purpose                           | Key Point                          |
| ----------------------------- | --------------------------------- | ---------------------------------- |
| `get-pr-review-comments`      | Fetch unresolved review threads   | Returns threads with line info     |
| `get-pr-discussion-comments`  | Fetch PR discussion comments      | Returns top-level comments         |
| `resolve-review-thread`       | Reply AND resolve a single thread | Does both in one operation         |
| `resolve-review-threads`      | Batch resolve multiple threads    | JSON stdin, one call for N threads |
| `reply-to-discussion-comment` | Reply to discussion comment       | For non-code feedback              |
| `post-pr-inline-comment`      | Post new inline comment           | Creates new review thread          |

## When to Use Each Command

### Fetching Comments

```bash
# Get all unresolved review threads (code comments)
erk exec get-pr-review-comments

# Get all discussion comments (top-level PR comments)
erk exec get-pr-discussion-comments

# Include resolved threads (for reference)
erk exec get-pr-review-comments --all
```

### Resolving Review Threads

```bash
# Resolve a single thread
erk exec resolve-review-thread --thread-id "PRRT_abc123" --comment "Fixed in commit abc1234"

# Batch resolve multiple threads (preferred for pr-address batches)
echo '[{"thread_id": "PRRT_abc", "comment": "Fixed"}, {"thread_id": "PRRT_def", "comment": "Applied"}]' | erk exec resolve-review-threads
```

### Replying to Discussion Comments

```bash
# For PR discussion comments (not code review threads)
erk exec reply-to-discussion-comment --comment-id 12345 --reply "**Action taken:** Updated the docs as requested."
```

## Common Mistakes

| Mistake                                        | Why It's Wrong                | Correct Approach                      |
| ---------------------------------------------- | ----------------------------- | ------------------------------------- |
| Using `gh api repos/.../comments/{id}/replies` | Only replies, doesn't resolve | Use `erk exec resolve-review-thread`  |
| Using `gh pr comment`                          | Doesn't resolve threads       | Use `erk exec resolve-review-thread`  |
| Skipping resolution for outdated threads       | Threads stay open in PR       | Always resolve, even if already fixed |
| Generic replies like "Noted"                   | Not useful for PR history     | Include investigation findings        |

## Replying vs Resolving

> **IMPORTANT: Replying ≠ Resolving**
>
> - **Replying** (via raw `gh api .../replies`): Adds a comment but thread stays OPEN
> - **Resolving** (via `erk exec resolve-review-thread`): Adds a comment AND marks thread as RESOLVED
>
> Always use `erk exec resolve-review-thread` (single) or `erk exec resolve-review-threads` (batch) - they do both in one operation.

## Comment Classification Model

When analyzing PR feedback, classify comments by complexity and group into batches.

### Complexity Categories

- **Local fix**: Single comment → single location change (e.g., "Fix typo", "Add type annotation")
- **Multi-location**: Single comment → changes in multiple spots in one file
- **Cross-cutting**: Single comment → changes across multiple files
- **Related**: Multiple comments that inform a single unified change

### Batch Ordering

Process batches from simplest to most complex:

| Batch | Complexity                 | Description                         | Example                                                   |
| ----- | -------------------------- | ----------------------------------- | --------------------------------------------------------- |
| 1     | Local fixes                | One file, one location per comment  | "Use LBYL pattern at line 42"                             |
| 2     | Single-file multi-location | One file, multiple locations        | "Rename this variable everywhere in this file"            |
| 3     | Cross-cutting              | Multiple files affected             | "Update all callers of this function"                     |
| 4     | Complex/Related            | Multiple comments inform one change | "Fold validate into prepare" + "Use union types for this" |

**Note**: Discussion comments requiring doc updates go in Batch 3 (cross-cutting).

### Batch Confirmation Flow

- **Batch 1-2 (simple)**: Auto-proceed without confirmation
- **Batch 3-4 (complex)**: Show plan and wait for user approval

## Inline Comment Deduplication

When posting inline review comments, always deduplicate to prevent re-posting existing comments:

1. **Build dedup key**: `(file_path, line_number, body_prefix)` where prefix is first 80 characters of comment body
2. **Check proximity**: Match within 2-line tolerance (line 42 matches existing comments at lines 40–44)
3. **Skip duplicates**: If a matching key exists, do not post the comment

This prevents the same feedback from appearing multiple times across review iterations. See [Inline Comment Deduplication](../../docs/learned/review/inline-comment-deduplication.md) for full algorithm details.

## Detailed Documentation

For complete command documentation including JSON output formats, options, and examples:

@references/commands.md
