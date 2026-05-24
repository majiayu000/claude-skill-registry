---
name: pr-comment-limit-enforcement
description: Use when posting PR comments. Enforces 50-comment limit to prevent infinite review cycles.
version: "1.0.0"
author: "JacobPEvans"
---

# PR Comment Limit Enforcement

<!-- markdownlint-disable-file MD013 -->

Standardized patterns for checking and enforcing the 50-comment limit on pull requests. All commands that post comments must use these patterns.

## Purpose

Prevents infinite AI review cycles by capping PR comments at 50. Provides single source of truth for comment counting, limit checking, and auto-resolution patterns.

## The Limit

### Hard Limit: 50 Comments Per Pull Request

### What Counts

A "comment" includes:

- PR review threads (code review comments in conversation threads)
- Inline code comments (comments on specific lines)
- General PR comments (discussions on the PR body)
- **Resolved comments** (still count toward the limit)

### Why Count Resolved Comments?

Prevents gaming the system by resolving old comments to post new ones. All comments take up space in the review conversation.

## Pre-Comment Check Pattern

Before posting ANY new comments on a PR, MUST check limit:

### Step 1: Count Comments

```bash
# Get total comment count (review threads + PR comments)
COMMENT_COUNT=$(gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { comments { totalCount } reviewThreads { totalCount } } } }' | jq '.data.repository.pullRequest.comments.totalCount + .data.repository.pullRequest.reviewThreads.totalCount')
```

### Step 2: Check Limit

```bash
if [ "$COMMENT_COUNT" -ge 50 ]; then
  echo "❌ PR has reached 50-comment limit. Skipping comment posting."
  echo "See PR Comment Limits rule for details."
  exit 0
fi
```

### Step 3: Proceed if Under Limit

```bash
# Only if COMMENT_COUNT < 50
gh pr comment "$PR_NUMBER" --body "Your comment here..."
```

## Auto-Resolution Pattern

When limit is reached, auto-resolve all unresolved threads with standard message:

### Resolution Message Template

```text
This PR has reached the 50-comment limit. All subsequent comments are being
automatically resolved to allow the PR to be merged. Please address any
critical feedback on a follow-up PR.
```

### Auto-Resolution Workflow

1. **Detect limit exceeded**:

   ```bash
   COMMENT_COUNT=$(... count query ...)
   if [ "$COMMENT_COUNT" -ge 50 ]; then
     # Limit exceeded
   fi
   ```

2. **Get unresolved threads**:

   ```bash
   # Use GitHub GraphQL Skill patterns for fetching unresolved threads
   gh api graphql --raw-field 'query=query { ... reviewThreads(last: 100) { nodes { id isResolved } } }'
   ```

3. **Post auto-resolution message** (as general PR comment):

   ```bash
   gh pr comment "$PR_NUMBER" --body "This PR has reached the 50-comment limit..."
   ```

4. **Resolve all unresolved threads**:

   ```bash
   # For each unresolved thread ID
   gh api graphql --raw-field 'query=mutation { resolveReviewThread(input: {threadId: "{THREAD_ID}"}) { thread { id isResolved } } }'
   ```

## Command Integration

### For Comment-Posting Commands

Commands that post comments (`/review-pr`, `/manage-pr`, custom review tools) MUST:

1. **Check limit BEFORE** posting any comments
2. **Exit gracefully** if limit reached (return success code, not error)
3. **Log the skip** with clear message explaining why

### For Comment-Resolution Commands

Commands that resolve comments (`/resolve-pr-review-thread`) SHOULD:

1. **Check limit** as informational (doesn't block resolution)
2. **Continue resolving** even if limit exceeded (help reduce count)
3. **Report limit status** in final output

## Commands Using This Skill

- `/review-pr` - MUST check before posting review comments
- `/manage-pr` - MUST check before posting feedback
- Any command that posts PR comments

## Related Resources

- pr-comment-limits rule - Policy and rationale
- github-graphql skill - Query patterns for comment counting
- pr-thread-resolution-enforcement skill - Thread resolution patterns

## Examples

### Example 1: PR with 45 Comments

```bash
COMMENT_COUNT=45

if [ "$COMMENT_COUNT" -ge 50 ]; then
  exit 0  # This branch NOT taken
fi

# Proceed with posting comments
gh pr comment 123 --body "Review feedback here..."
```

Result: Comment posted normally

### Example 2: PR with 50 Comments

```bash
COMMENT_COUNT=50

if [ "$COMMENT_COUNT" -ge 50 ]; then
  echo "❌ PR #123 has reached 50-comment limit. Skipping new comments."
  exit 0  # Exit gracefully
fi

# This line never executes
```

Result: No comment posted, command exits cleanly

### Example 3: PR with 52 Comments (Auto-Resolve)

```bash
COMMENT_COUNT=52

# Limit exceeded - trigger auto-resolution
gh pr comment 123 --body "This PR has reached the 50-comment limit..."

# Get unresolved threads
THREAD_IDS=$(... GraphQL query ...)

# Resolve each thread in parallel using the resolve-pr-thread-graphql agent
# Launch one agent per thread ID
Task(subagent_type='resolve-pr-thread-graphql', prompt='Resolve thread: thread_id_1', run_in_background=true)
Task(subagent_type='resolve-pr-thread-graphql', prompt='Resolve thread: thread_id_2', run_in_background=true)
Task(subagent_type='resolve-pr-thread-graphql', prompt='Resolve thread: thread_id_3', run_in_background=true)
# ... (continue for all thread IDs)
# Wait for all agents to complete using TaskOutput
```

Result: All threads resolved, message posted

## Troubleshooting

### Issue: Comment count query returns incorrect total

**Cause**: Query might not be counting both comments and reviewThreads

**Solution**: Ensure query sums both: `comments.totalCount + reviewThreads.totalCount`

### Issue: Auto-resolution doesn't prevent new comments

**Cause**: Commands not checking limit before posting

**Solution**: Add pre-comment check to all comment-posting commands

### Issue: Critical feedback gets auto-resolved

**Cause**: PR legitimately needs more than 50 comments worth of feedback

**Solution**: PR should be split into smaller PRs, or critical issues addressed in follow-up

## Best Practices

1. **Always check before posting** - Never post without checking limit first
2. **Exit gracefully** - Return success (0), not error, when skipping due to limit
3. **Clear logging** - Explain why comment was skipped
4. **Use standard message** - Same auto-resolution message everywhere
5. **Reference rule** - Point users to PR Comment Limits rule for context
6. **Count everything** - Don't try to exclude certain comment types
7. **Respect the limit** - No workarounds or exceptions
