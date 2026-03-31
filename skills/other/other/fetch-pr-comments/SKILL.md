---
name: fetch-pr-comments
description: "Fetch and summarize unresolved GitHub PR review comments without making changes. Use when the user asks to \"fetch PR comments\", \"show PR comments\", \"check PR for unresolved comments\", \"list review comments\", \"what comments are on the PR\", \"show unresolved threads\", or \"summarize PR feedback\"."
---

# Fetch PR Comments

Fetch unresolved review comments and top-level review body comments from a GitHub PR and present them in a readable summary. This is a read-only skill -- it does not evaluate, fix, or reply to any comments.

## Step 1: Fetch Comments

Fetch review threads and top-level review body comments from the PR:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      title url
      reviewThreads(first: 100) {
        nodes {
          id isResolved isOutdated
          comments(first: 50) {
            nodes { author { login } body path line }
          }
        }
      }
      reviews(first: 50) {
        nodes {
          author { login }
          body state
        }
      }
    }
  }
}' -f owner='{owner}' -f repo='{repo}' -F pr={pr_number}
```

Auto-detect owner, repo, and PR number from current branch if not provided. Filter review threads to unresolved only. Filter reviews to those with a non-empty body, excluding `PENDING` state (unsubmitted drafts).

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

**Inline threads grouped by file:**

For each file with unresolved threads, show:

```
## `path/to/file.ts`

### Line 42 (by @reviewer)
> Comment body here

### Lines 10-15 (by @another-reviewer) [outdated]
> First comment body
>
> **@reply-author:** Reply body
```

**Formatting rules:**
- Show top-level review body comments first, grouped under "Review Comments"
- Then group threads by file path, in the order they appear
- Within each file, order threads by line number
- Show all comments in a thread (the first is the original review comment; subsequent ones are replies)
- Mark outdated threads with `[outdated]`
- Use blockquotes for comment bodies
- For threads with multiple comments, show each comment with its author
- If there are zero unresolved threads and zero review body comments, say so and stop

## Rules

- If the user wants to fix or reply to comments, direct them to use `/resolve-pr-comments`.
