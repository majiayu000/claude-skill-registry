---
name: pr-thread-resolution-enforcement
description: Use when resolving PR review threads. Enforces that all threads are marked resolved before completion.
version: "1.0.0"
author: "JacobPEvans"
---

# PR Thread Resolution Enforcement

<!-- markdownlint-disable-file MD013 -->

Standardized patterns for enforcing PR review thread resolution. All commands that work with PR feedback must verify using this skill before reporting work complete.

## Purpose

Ensures that PR review threads are **ALWAYS** marked as `isResolved: true` in GitHub before commands report their work is done. This creates a single enforcement point across all PR management workflows.

## Critical Requirements

### 1. Atomicity: Reply AND Resolve Together

There are exactly two resolution paths:

1. **Technical Resolution**: Implement change → Commit → Reply with commit details → Resolve thread
2. **Response-Only Resolution**: Explain why change not needed → Reply with reasoning → Resolve thread

**CRITICAL**: Never reply without resolving, never resolve without replying. These are ONE atomic action.

### 2. Verification MUST Pass Before Reporting Completion

Before any command (especially `/manage-pr` and `/resolve-pr-review-thread`) reports work as complete:

1. Run the verification query (see below)
2. Count unresolved threads
3. MUST equal 0 or command fails with clear error message

### 3. No Exceptions

This applies to:

- `/manage-pr` before requesting user review
- `/resolve-pr-review-thread` before reporting completion
- `/review-pr` when creating new threads (verify they're resolvable)
- Any custom workflow touching PR reviews

## Enforcement Pattern

### Step 1: Verify All Threads Resolved

Use this GraphQL query to verify zero unresolved threads:

```bash
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { isResolved } } } } }' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length'
```

**Success Criteria**: Returns `0`

**Failure Criteria**: Returns any number > 0

### Step 2: Command Behavior on Verification

**If Verification Passes (0 unresolved threads)**:

- Command may proceed to report completion
- Clear confirmation: "✅ All review threads resolved - proceeding"

**If Verification Fails (>0 unresolved threads)**:

- Command MUST abort with error
- Clear message format: "❌ Cannot complete - {N} unresolved review threads remain. Use /resolve-pr-review-thread to address them."
- Include list of remaining threads (optional but helpful)

### Step 3: Resolution Workflow

Before verification passes, follow this workflow for each unresolved thread:

1. **Read the comment**: Understand reviewer's concern
2. **Determine action**: Fix code or explain why not needed
3. **Implement if needed**: Use Edit tool for code changes
4. **Reply to comment**: Post technical response using gh CLI

   ```bash
   gh pr comment <PR_NUMBER> --body "Response text"
   ```

5. **Resolve the thread**: GraphQL mutation (see github-graphql skill)

   ```bash
   gh api graphql --raw-field 'query=mutation { resolveReviewThread(input: {threadId: "{THREAD_ID}"}) { thread { id isResolved } } }'
   ```

6. **Verify resolution**: Confirm thread now shows `isResolved: true`

## Integration with GitHub GraphQL Skill

This skill works with the github-graphql skill for:

- **Thread resolution mutation**: `resolveReviewThread` patterns
- **Commit operations**: Signed commits for code changes
- **Verification queries**: All GraphQL operations
- **ID handling**: GraphQL node IDs vs REST numeric IDs

See GitHub GraphQL Skill for complete patterns.

## Verification Implementation

### For `/manage-pr` Command

**Location**: Phase 3 (Pre-Handoff Verification), before requesting user review

```bash
# Verify all conversations resolved using verification query above
# Store result in variable
UNRESOLVED_COUNT=$(gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { nodes { isResolved } } } } }' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length')

# Check result
if [ "$UNRESOLVED_COUNT" -ne 0 ]; then
  echo "❌ Cannot complete - $UNRESOLVED_COUNT unresolved review threads remain."
  echo "Use /resolve-pr-review-thread to address them."
  exit 1
fi

echo "✅ All review threads resolved - proceeding with merge readiness check"
```

### For `/resolve-pr-review-thread` Command

**Location**: After pr-thread-resolver agent completes

Run the verification query. Only report success if result is 0.

### Success Output Examples

```text
✅ ALL REVIEW THREADS RESOLVED - PR #123

Verification:
✅ All threads marked isResolved: true
✅ Changes committed and pushed
✅ Ready for user review
```

```text
⚠️ PARTIAL RESOLUTION - PR #45

Unresolved: 1 thread (requires clarification from author)
Resolved: 4 threads
Next steps: Author needs to respond to blocking feedback on line 89
```

## Placeholder Reference

| Placeholder | Description | Example |
| --- | --- | --- |
| `{OWNER}` | Repository owner | `JacobPEvans` |
| `{REPO}` | Repository name | `ai-assistant-instructions` |
| `{NUMBER}` | PR number | `42` |
| `{THREAD_ID}` | GraphQL thread ID | `PRRT_kwDOO1m-OM5gtgeQ` |

## Common Scenarios

### Scenario 1: Simple Bug Fix

1. Reviewer suggests code change in suggestion block
2. Author implements exact change
3. Author replies with commit hash
4. Author marks thread resolved via mutation
5. Verification returns 0 - ✅

### Scenario 2: Design Question

1. Reviewer asks "Why did you choose X instead of Y?"
2. Author replies with technical reasoning
3. Author marks thread resolved (no code change needed)
4. Verification returns 0 - ✅

### Scenario 3: Blocking Issue

1. Reviewer marks as "BLOCKING - must fix"
2. Author implements fix
3. Author replies with details
4. Author marks thread resolved
5. Verification returns 0 - ✅

### Scenario 4: Disagreement

1. Reviewer suggests unnecessary refactor
2. Author replies explaining why current approach is better
3. Reviewer acknowledges in same thread or separate comment
4. Author marks thread resolved
5. If verification still returns >0, new thread needs resolution
6. Repeat until all resolved

## Commands Using This Skill

- `/manage-pr` - MUST verify before Phase 3 (Pre-Handoff Verification)
- `/resolve-pr-review-thread [all]` - MUST verify before reporting completion
- `/review-pr` - Uses implicitly (doesn't create threads but respects enforcement)

## Related Resources

- github-graphql skill - Mutation patterns, node ID handling
- pr-thread-resolver agent - Full implementation patterns
- /resolve-pr-review-thread command - Orchestrator using this skill
- /manage-pr command - Uses verification pattern

## Troubleshooting

### Issue: Verification returns wrong count

**Cause**: PR has mixed thread states or pagination issues

**Solution**: Use `last: 100` (never `first: ##`) in queries to ensure all threads fetched

### Issue: Thread shows resolved but verification still counts it

**Cause**: GraphQL cache not updated yet

**Solution**: Wait 2-3 seconds, then re-run verification query

### Issue: Cannot mark thread as resolved

**Cause**: Missing write permissions or invalid thread ID

**Solution**: Verify `gh auth status` shows repo write access and thread ID starts with `PRRT_`

## Best Practices

1. **Always verify before reporting completion** - Make it automatic in all workflows
2. **Be specific in replies** - Reference what was changed or why change wasn't made
3. **Respect reviewer feedback** - Don't dismiss concerns lightly
4. **Disagree respectfully** - Provide technical reasoning, not opinion
5. **Use verification query consistently** - Exact same query, every time
6. **Check count, not just existence** - Verify returns exactly `0`
