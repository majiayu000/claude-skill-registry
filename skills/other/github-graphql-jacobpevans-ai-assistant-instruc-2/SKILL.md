---
name: github-graphql
description: Use when querying GitHub via GraphQL. Provides patterns for PR threads, comments, and mutations.
version: "1.0.0"
author: "JacobPEvans"
---

# GitHub GraphQL Patterns

<!-- markdownlint-disable-file MD013 -->

Standardized GraphQL patterns for GitHub PR and review thread operations. All commands
that interact with GitHub's GraphQL API should reference this skill instead of duplicating queries.

## Critical Requirements

### 1. Single-Line Format Required

**ALWAYS use single-line GraphQL queries with `--raw-field` in Claude Code.**

Multi-line GraphQL queries cause encoding issues. Use this pattern:

```bash
# CORRECT: Single-line with --raw-field
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { id isResolved } } } } }'
```

**Shell Quoting Notes:**

- **Single quotes** (as above) prevent shell variable expansion - use when query contains literal placeholders like `{OWNER}`
- **Double quotes** needed only for shell variable substitution (e.g., `$OWNER`) - must escape inner quotes with `\"`
- **Single-line** refers to the GraphQL query itself (no newlines), not shell quoting style
- **Placeholders** like `{OWNER}`, `{REPO}`, `{NUMBER}` are documentation notation - replace with actual values before running

### 2. Always Use `last: 100` Not `first: ##`

**NEVER use `first: ##` in GraphQL queries.** Always use `last: 100` to ensure you get ALL recent
items and don't miss threads/comments due to pagination cutoff.

### 3. No For Loops

**NEVER use for loops or while loops** - they require permission prompts and break automation.
Instead:

- Run single `gh api graphql` commands against single thread IDs
- Process threads one at a time with individual approved commands
- If possible, include multiple thread IDs as separate parameters in a single call

### 4. Commits Must Be Signed

When making direct commits for PR changes, **ALL commits MUST be signed**.

## Core Query Patterns

### 1. Get Review Threads

**Purpose:** Fetch all review threads for a PR with resolution status and comments.

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { id isResolved path line startLine comments(last: 100) { nodes { id databaseId body author { login } createdAt } } } } } } }'
```

**Key Fields:**

| Field | Description |
| ----- | ----------- |
| `id` | Thread ID for resolution (format: `PRRT_xxx`) |
| `isResolved` | Boolean resolution status |
| `path` | File path the comment is on |
| `line`/`startLine` | Line numbers in the file |
| `comments.nodes[].body` | Comment text |
| `comments.nodes[].databaseId` | Numeric ID for REST API operations |

### 2. Resolve Review Thread

**Purpose:** Mark a review thread as resolved.

```bash
gh api graphql --raw-field 'query=mutation { resolveReviewThread(input: {threadId: "{THREAD_ID}"}) { thread { id isResolved } } }'
```

**Requirements:**

- Thread ID must be a valid GraphQL node ID starting with `PRRT_`
- You must have write access to the repository

### 3. Verify All Threads Resolved

**Purpose:** Check if any unresolved threads remain on a PR.

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { isResolved } } } } }' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length'
```

**Success Criteria:** Returns `0` (no unresolved threads).

### 4. Get PR Mergeable Status

**Purpose:** Check if a PR can be merged.

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { mergeable statusCheckRollup { state } reviewDecision } } }'
```

**Mergeable Values:**

- `MERGEABLE` - Can be merged
- `CONFLICTING` - Has merge conflicts
- `UNKNOWN` - Status still being calculated

## Thread Resolution Workflow

### Step 1: Get Unresolved Thread IDs

Run the query to get all threads, then use jq to extract unresolved thread IDs:

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { id isResolved } } } } }' | jq -r '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | .id'
```

### Step 2: Resolve Each Thread Individually

For each thread ID from Step 1, run the resolve mutation as a **separate command**:

```bash
gh api graphql --raw-field 'query=mutation { resolveReviewThread(input: {threadId: "PRRT_kwDOxxxxx"}) { thread { id isResolved } } }'
```

**Important:** Do NOT use loops. Run each resolve command individually.

### Step 3: Verify Resolution

After resolving all threads, verify none remain unresolved:

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { isResolved } } } } }' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length'
```

## Node ID Handling

GitHub uses two ID systems. Understanding when to use each is critical.

### GraphQL Node IDs (base64 encoded)

Used for GraphQL operations:

- Review thread: `PRRT_kwDOO1m-OM5gtgeQ`
- PR comment: `PRRC_kwDOO1m-OM5gtgeR`
- Pull request: `PR_kwDOO1m-OM4...`

Get via GraphQL query `nodes[].id` fields.

### REST API Numeric IDs

Used for REST API operations:

- Get via: `gh api repos/{OWNER}/{REPO}/pulls/{NUMBER}/comments | jq '.[].id'`
- Or via GraphQL: `comments.nodes[].databaseId`

### ID Usage Table

| Operation | ID Type | How to Get |
| --------- | ------- | ---------- |
| Resolve thread | GraphQL node ID (`PRRT_xxx`) | From `reviewThreads.nodes[].id` |
| Reply to comment | Numeric ID | From REST API or `databaseId` |
| React to comment | Numeric ID | From REST API or `databaseId` |
| Get thread status | GraphQL node ID | From `reviewThreads.nodes[].id` |

## Making Changes to PRs

When resolving review threads requires code changes:

### Option 1: Use Worktree (Preferred)

1. Create or switch to the PR's worktree:

   ```bash
   BRANCH="{BRANCH}"
   SANITIZED_BRANCH="$(printf '%s' "$BRANCH" | tr -c 'A-Za-z0-9._-' '_')"
   git worktree add "$HOME/git/{REPO}/$SANITIZED_BRANCH" "$BRANCH"
   cd "$HOME/git/{REPO}/$SANITIZED_BRANCH"
   ```

2. Make changes normally
3. Commit with signature: `git commit -S -m "message"`
4. Push: `git push origin {BRANCH}`

### Option 2: Direct Signed Commit (Small Changes Only)

For small single-file fixes, you can commit directly **if and only if commits are signed**:

```bash
# Ensure GPG signing is configured
git config --global commit.gpgsign true
git config --global user.signingkey {YOUR_KEY_ID}

# Make the change and commit with signature
git commit -S -m "fix: address review feedback"
git push origin {BRANCH}
```

**Never:**

- Create branches in /tmp folders
- Output temporary scripts
- Make unsigned commits

## Placeholder Reference

**NOTE**: Placeholders below use `{CURLY_BRACES}` notation for documentation clarity. These are NOT bash variables and will NOT be expanded by the shell. You must manually replace them with actual values before running commands.

| Placeholder | Description | Example |
| ----------- | ----------- | ------- |
| `{OWNER}` | Repository owner (replace with actual value) | `JacobPEvans` |
| `{REPO}` | Repository name (replace with actual value) | `ai-assistant-instructions` |
| `{NUMBER}` | PR number integer (replace with actual value) | `123` |
| `{THREAD_ID}` | Thread ID from GraphQL query (replace with actual value) | `PRRT_kwDOO1m-OM5gtgeQ` |
| `{BRANCH}` | Branch name (replace with actual value) | `fix/my-feature` |

## Common Errors and Solutions

| Error | Cause | Solution |
| ----- | ----- | -------- |
| "Field 'reviewThreads' doesn't exist" | Wrong API version | Use GraphQL v4 (default) |
| "Resource not accessible by integration" | Missing permissions | Check `gh auth status`, ensure repo access |
| "Invalid node ID" | Wrong ID format | Verify ID starts with correct prefix (`PRRT_`, etc.) |
| Encoding/parsing issues | Multi-line query | Use single-line format with `--raw-field` |
| "Could not resolve to a PullRequest" | Wrong PR number | Verify PR exists and number is correct |

## Commands Using This Skill

- `/resolve-pr-review-thread [all]` - Primary consumer for thread resolution
- `/manage-pr` - Thread resolution during PR management
- `/review-pr` - Creating and reading review threads
- `/pr-review-feedback` - Reference documentation for GraphQL patterns

## Best Practices

1. **Always use `last: 100`**: Never use `first: ##` to avoid missing threads
2. **No loops**: Run individual commands, don't batch with loops
3. **Verify resolution**: After resolving, query again to confirm `isResolved: true`
4. **Sign all commits**: Use `git commit -S` for all direct commits
5. **Use worktrees**: Prefer worktrees over /tmp folders for code changes
6. **Check permissions first**: Run `gh auth status` before GraphQL operations
7. **Use jq for parsing**: Extract specific fields with `jq` rather than parsing raw JSON
