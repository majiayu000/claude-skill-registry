---
name: fetch-pr-comments
description: "Fetch and summarize review feedback and conversation from a GitHub PR (unresolved review threads, review bodies, and PR conversation comments) without making changes. Use when the user asks to \"fetch PR comments\", \"show PR comments\", \"check PR for unresolved comments\", \"list review comments\", \"what comments are on the PR\", \"show unresolved threads\", or \"summarize PR feedback\"."
---

# Fetch PR Comments

Fetch unresolved review comments, top-level review body comments, and PR conversation comments from a GitHub PR and present them in a readable summary. This is a read-only skill -- it does not evaluate, fix, or reply to any comments.

## Step 1: Fetch Comments

Auto-detect owner, repo, and PR number from current branch if not provided. Then run `scripts/fetch-pr-data.sh`, which handles full pagination (review threads, inner comment pages for long threads, reviews, issue comments) and emits a single merged JSON document:

```bash
bash <skill-dir>/scripts/fetch-pr-data.sh <owner> <repo> <pr_number>
```

Output shape:

```jsonc
{
  "meta":          { "title", "url", "headRefName", "baseRefName" },
  "reviewThreads": [ { "id", "isResolved", "isOutdated", "comments": { "nodes": [ { "author", "body", "path", "line", "originalLine", "diffHunk" } ] } } ],
  "reviews":       [ { "author", "body", "state" } ],
  "issueComments": [ { "author", "body", "createdAt", "url" } ]
}
```

Filter review threads to unresolved only. Filter reviews to those with a non-empty body, excluding `PENDING` state (unsubmitted drafts). Filter issue comments to those with a non-empty body.

## Step 2: Present Results

Display a summary header followed by comments grouped by file.

**Summary header:**

- PR title and link
- Branch: `head` -> `base`
- Total threads / unresolved threads

**Top-level review comments (if any):**

Show reviews with non-empty body before the file-grouped threads:

```
## Review Comments

### @reviewer (CHANGES_REQUESTED)
> Review body text here

### @another-reviewer (COMMENTED)
> Another review body here
```

**Issue comments (if any):**

Show PR conversation comments after review comments, ordered by `createdAt`:

```
## Issue Comments

### @commenter (2026-04-20)
> Issue comment body here

### @another-commenter (2026-04-21)
> Another issue comment body here
```

**Inline threads grouped by file:**

For each file with unresolved threads, show:

````
## `path/to/file.ts`

### Line 42 (by @reviewer)
```diff
<diffHunk from first comment>
```
> Comment body here

### Line 10 (by @another-reviewer) [outdated]
```diff
<diffHunk from first comment>
```
> First comment body
>
> **@reply-author:** Reply body
````

**Formatting rules:**
- Show top-level review body comments first, grouped under "Review Comments"
- Show PR conversation comments next, grouped under "Issue Comments", ordered by `createdAt`
- Then group threads by file path, in the order they appear
- Within each file, order threads by line number
- Show the `diffHunk` from the first comment in each thread as a fenced diff code block before the comment body. This is the code context the reviewer was looking at.
- For the line number, use `line` if available. Fall back to `originalLine` for outdated comments where `line` is null.
- Show all comments in a thread (the first is the original review comment; subsequent ones are replies)
- Mark outdated threads with `[outdated]`
- Use blockquotes for comment bodies
- For threads with multiple comments, show each comment with its author
- If there are zero unresolved threads, zero review body comments, and zero issue comments, say so and stop

Then use the TaskList tool and proceed to any remaining task.

## Rules

- If the user wants to fix or reply to comments, direct them to use `/resolve-pr-comments`.
