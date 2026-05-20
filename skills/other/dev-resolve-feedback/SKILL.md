---
name: dev-resolve-feedback
description: Ask CodeRabbit to verify and resolve each unresolved feedback thread on a PR. Use when CodeRabbit posts "No actionable comments" but old threads remain open, blocking approval.
user-invokable: true
---

Ask CodeRabbit to verify each unresolved inline feedback thread individually
and resolve it if the issue has been fixed. This is the safe alternative to
`@coderabbitai resolve`, which force-resolves all threads and can miss
genuinely unaddressed feedback.

## When to use

- CodeRabbit posted "No actionable comments were generated in the recent
  review" but old threads are still open and the PR is not approved
- After pushing fixes and requesting a re-review, threads were not
  auto-resolved
- Any time there are stale CodeRabbit threads blocking approval

## Arguments

- PR number (optional) — defaults to the current branch's PR

## How it works

1. **Fetch all inline CodeRabbit comments** on the PR via the GitHub API
2. **Reply to each unresolved thread** with exactly:

   > @coderabbitai please check the latest changes to confirm if this issue
   > has been fixed and if so resolve this item

3. **Report** what was done (comment count and IDs)

## What it does NOT do

- It does NOT post `@coderabbitai resolve` as a general PR comment — that
  force-resolves everything and can mask missed feedback
- It does NOT make code changes
- It does NOT request a new review
- It does NOT merge the PR

## Workflow

### 1. Determine the PR number

If the user provided a PR number, use it. Otherwise, infer from the current
branch:

```bash
gh pr view --json number --jq '.number'
```

### 2. Fetch unresolved CodeRabbit threads

The REST API does not expose thread resolution status. Use GraphQL to fetch
only unresolved threads authored by CodeRabbit:

```bash
gh api graphql -f query='
query($owner:String!, $repo:String!, $pr:Int!, $after:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$pr) {
      reviewThreads(first:100, after:$after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          isResolved
          comments(first:1) {
            nodes {
              databaseId
              path
              line
              author { login }
              body
            }
          }
        }
      }
    }
  }
}' -F owner='{owner}' -F repo='{repo}' -F pr='{pr-number}' \
| jq '
  .data.repository.pullRequest.reviewThreads.nodes
  | map(select(.isResolved == false))
  | map(.comments.nodes[0])
  | map(select(.author.login == "coderabbitai"))
  | map({id: .databaseId, path, line, body: (.body[:100])})'
```

If there are more than 100 threads, paginate using the `after` cursor
from `pageInfo.endCursor`.

**Important:** The GraphQL API returns bot logins without the `[bot]`
suffix (e.g. `"coderabbitai"`), unlike the REST API which returns
`"coderabbitai[bot]"`. The filter above uses the GraphQL form.

### 3. Reply to each unresolved thread

For each unresolved CodeRabbit comment, reply using the threaded reply API
with the comment's `databaseId`:

```bash
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies \
  -f body="@coderabbitai please check the latest changes to confirm if this issue has been fixed and if so resolve this item"
```

**Important:** Use the `replies` endpoint (not `gh pr comment`) so the
reply is threaded under the original feedback, not posted as a standalone
comment. Only reply to threads that are actually unresolved — skip any
that GraphQL reports as `isResolved == true`.

### 4. Report results

```text
Done:
- Replied to N CodeRabbit feedback threads on PR #X
- Comment IDs: 123, 456, 789
```

## Safety

- Only replies to comments authored by CodeRabbit (`coderabbitai` in
  GraphQL, `coderabbitai[bot]` in REST)
- Uses the threaded reply API so each response is scoped to its thread
- Does not modify code, branches, or PR state
- CodeRabbit decides independently whether each thread should be resolved —
  if the issue is not fixed, the thread stays open
