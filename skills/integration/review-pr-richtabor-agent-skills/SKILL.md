---
name: review-pr
description: Reviews PR comments from GitHub (Copilot, reviewers), evaluates against actual code, replies with reasoning, and resolves threads. Triggers on "review pr comments", "address pr feedback", "fix pr comments", or "review copilot suggestions".
---

# Review PR Comments

Fetch, evaluate, and address PR review comments from GitHub. Many reviewer comments reference outdated code or misunderstand the logic — always verify against the actual codebase before acting.

## Process

**This is a single-pass flow.** Fetch comments, read files, evaluate, present assessment, reply to all comments, resolve all threads, and show the final summary — all without pausing for user confirmation.

### 1. Find the PR

If no PR number is provided, find the PR for the current branch:

```bash
gh pr list --head $(git branch --show-current) --json number,title --jq '.[0]'
```

### 2. Fetch Review Comments

Fetch comments with their IDs:

```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {id: .id, path: .path, line: (.line // .original_line), body: .body, in_reply_to_id: .in_reply_to_id}'
```

Filter to only top-level comments (where `in_reply_to_id` is null).

### 3. Read Referenced Files (Critical Step)

**Before evaluating any comment, read the actual current code.** Reviewers often:
- Reference line numbers from an older commit
- Misread the logic
- Comment on code that's already been fixed

For each unique file path, read the file and verify:
- Does the line number match what the reviewer is describing?
- Has the issue already been addressed?
- Is the reviewer's understanding of the code correct?

### 4. Evaluate All Comments

Categorize each comment:

| Category | Criteria | Response |
|----------|----------|----------|
| **Already addressed** | Issue was fixed in a subsequent commit, or reviewer misread the code | Explain what the code actually does |
| **Fix** | Valid bug, security issue, or typo that exists in current code | Implement the fix |
| **Won't fix** | Over-engineering, style preference, feature request, or would break consistency | Explain reasoning |

### 5. Present Assessment, Reply, and Resolve

**Do all of this in one pass — no pausing for user confirmation.** Present your assessment, reply to each comment, and resolve all threads immediately.

Present ALL comments with your assessment:

```
## PR #[number]: [title]

Found [X] review comments. Here's my assessment:

---

### 1. `path/file.ts:42` — **Already addressed**
> [comment body]

**Issue**: Reviewer concerned about X
**Actual code**: Lines 26-34 already handle this — [brief explanation]

---

### 2. `path/other.ts:15` — **Won't fix**
> [comment body]

**Issue**: Reviewer wants X
**Why skip**: [Over-engineering / Matches existing pattern / Feature request / etc]

---

### 3. `path/file.ts:88` — **Fix**
> [comment body]

**Issue**: Typo in user-facing string
**Proposed change**: Change "Jumpope" to "Jump Rope"

---

## Summary
- **Already addressed**: 6 comments
- **Won't fix**: 8 comments
- **Fix**: 2 comments
```

Then **immediately** reply to all comments and resolve all threads (steps 6-7 below). Don't wait for user input.

### 6. Reply to Comments

For **Already addressed** comments, reply explaining the current state:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -X POST \
  -f body="This is already handled — lines 26-34 fetch the authenticated user and verify user.id === state before proceeding. If they don't match, it rejects with a CSRF error."
```

For **Won't fix** comments, reply with concise reasoning:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -X POST \
  -f body="Won't fix — this matches the exact pattern used for the other integrations in the same file. Changing just this one would be inconsistent."
```

For **Fix** comments, implement the fix first, then reply:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -X POST \
  -f body="Fixed in abc1234"
```

### 7. Resolve All Threads

First, get all unresolved thread IDs:

```bash
cat << 'QUERY' | gh api graphql --input - --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | {threadId: .id, commentId: .comments.nodes[0].databaseId}'
{"query": "query($owner: String!, $repo: String!, $pr: Int!) { repository(owner: $owner, name: $repo) { pullRequest(number: $pr) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 1) { nodes { databaseId } } } } } } }", "variables": {"owner": "OWNER", "repo": "REPO", "pr": 123}}
QUERY
```

Then resolve each thread by ID:

```bash
cat << 'QUERY' | gh api graphql --input -
{"query": "mutation { resolveReviewThread(input: {threadId: \"THREAD_ID_HERE\"}) { thread { isResolved } } }"}
QUERY
```

### 8. Final Summary

After replying and resolving, show the final summary:

```
## Review Complete

All 16 conversations resolved.

### Already addressed (6)
| Comment | Explanation |
|---------|-------------|
| State validation | Already validates user.id === state at lines 26-34 |
| HR zones docs | Comments already say "milliseconds", not "percentage" |

### Won't fix (8)
| Comment | Reason |
|---------|--------|
| Form semantics | Matches existing pattern for other integrations |
| Rate limiting | Self-heals on next cron run, over-engineering |

### Fixed (2)
| Commit | Fix |
|--------|-----|
| `abc123` | Fixed typo "Jumpope" → "Jump Rope" |
```

**Important**: The entire flow (assess → reply → resolve → summarize) happens in one pass. Don't pause to ask "should I proceed?" — just do it.

---

## Evaluation Guidelines

### Already Addressed — Explain, don't fix

Common patterns where the reviewer is wrong:

- **Reviewer references wrong line numbers**: Code has changed since they reviewed
- **Reviewer misread the logic**: e.g., thinks condition is inverted when it's correct
- **Issue was already fixed**: Subsequent commits addressed it
- **Code exists elsewhere**: The check/validation happens in a different function

Response template:
> "This is already handled — [specific location] does [what it does]. [Brief explanation of why it's correct]."

### Fix — Implement and commit

Only fix issues that:
- Actually exist in the current code
- Are bugs, security issues, or typos
- Can be verified by reading the file

### Won't Fix — Explain reasoning

| Reason | Response template |
|--------|-------------------|
| **Matches existing pattern** | "Won't fix — this matches the exact pattern of X, Y, and Z in the same file. Changing just this would be inconsistent." |
| **Over-engineering** | "Won't fix — [the failure mode] will fail obviously / self-heal on retry / is handled by [existing mechanism]." |
| **Feature request** | "Won't fix — this is a feature request rather than a bug. The current flow works: [what it does]. Out of scope for this PR." |
| **Product decision** | "Won't fix — this is a product decision, not a bug. [Current behavior] is intentional because [reason]." |
| **Would break things** | "Won't fix — this would break [existing behavior / consistency with X]." |

---

## Common Reviewer Misunderstandings

### Inverted conditions
Reviewers often misread boolean logic. Example:
```typescript
// "Refresh if expires in less than 5 minutes"
if (expiry.getTime() - Date.now() > 5 * 60 * 1000) {
  return integration.access_token!; // Token is fresh, return early
}
// Proceed to refresh...
```
Reviewer says: "Condition is inverted, tokens never refresh"
Reality: Condition is correct — returns early when fresh, refreshes when stale.

### Missing validation that exists
Reviewer says: "State parameter not validated"
Reality: Lines 26-34 already validate it.
**Always check if the validation exists before agreeing.**

### Tokens in error messages
Reviewer says: "Sensitive tokens logged in error messages"
Reality: The error logs the API's error response, not our tokens.
**Read what's actually in the error string.**

### Code that doesn't exist at that line
Reviewer references line 174, but file only has 161 lines.
**The file has changed since the review.**

---

## Key Principles

1. **Single-pass execution**: Don't pause to ask "should I proceed?" — assess, reply, resolve, and summarize in one flow
2. **Verify before acting**: Always read the actual file before evaluating a comment
3. **Trust the codebase**: If existing patterns work, new code should match them
4. **Explain, don't just dismiss**: Skipped comments deserve clear explanations
5. **Resolve everything**: All threads should be resolved, whether fixed or explained
6. **Be concise**: Responses should be 1-2 sentences, not paragraphs
