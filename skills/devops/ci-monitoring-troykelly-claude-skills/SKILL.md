---
name: ci-monitoring
description: Use after creating PR - monitor CI pipeline, resolve failures, address review feedback, and merge when all gates pass
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
  - Glob
  - mcp__github__*
model: opus
---

# CI Monitoring

Monitor CI pipeline, resolve failures, address review feedback, and merge when ready.

**Core principle:** CI failures AND unresolved review feedback are blockers.

**Announce:** "I'm monitoring CI and review feedback, and will resolve any issues before merging."

## The Loop

```
PR Created
     │
     ▼
┌─────────────┐
│ Wait for CI │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
 Green   Red ──► Fix → Push → Loop back
   │
   ▼
┌──────────────────────┐
│ Unresolved Reviews?  │
└──────────┬───────────┘
       ┌───┴───┐
       │       │
     None    Yes ──► For each: Evaluate → Fix/Pushback → Reply → Resolve → Push → Loop back
       │
       ▼
┌─────────────┐
│ MERGE PR    │
└─────────────┘
```

## Gate: Green CI + No Unresolved Reviews = Merge

When both conditions met, merge immediately:

```bash
gh pr merge [PR_NUMBER] --squash --delete-branch
gh issue edit [ISSUE_NUMBER] --remove-label "status:in-review" --add-label "status:done"
```

Do NOT stop to report or ask. Continue to next issue.

**Exception:** PRs with `do-not-merge` label.

## Checking CI

```bash
gh pr checks [PR_NUMBER]
gh pr checks [PR_NUMBER] --watch
```

## Handling CI Failures

1. Identify: `gh run view [RUN_ID] --log-failed`
2. Reproduce locally
3. Fix and push
4. Wait for CI, repeat if needed

**Detailed patterns:** See [reference/ci-failures.md](reference/ci-failures.md)

## Handling Review Feedback

After CI green, check for unresolved threads:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes { id isResolved isOutdated comments(first: 1) { nodes { body author { login } path } } }
      }
    }
  }
}' -f owner="[OWNER]" -f repo="[REPO]" -F pr=[PR_NUMBER]
```

For each unresolved thread (`isResolved: false`):

| Step | Action |
|------|--------|
| 1 | Read and understand feedback |
| 2 | Verify: technically valid for this codebase? |
| 3 | Fix, defer (with issue), or push back with reasoning |
| 4 | Reply in thread: `gh api repos/.../pulls/.../comments/[ID]/replies -f body="..."` |
| 5 | Resolve: `gh api graphql -f query='mutation { resolveReviewThread(...) }'` |
| 6 | Push fixes, loop back to CI |

**Detailed commands:** See [reference/review-feedback.md](reference/review-feedback.md)

### Security Feedback

Security flags from automated reviewers (Codex, CodeRabbit, etc.) should be treated seriously and verified against the codebase.

## Best Practices

**Run locally first.** CI validates, doesn't discover.

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

If CI finds bugs you didn't find locally, your local testing was insufficient.

## Checklist

CI:
- [ ] All checks green
- [ ] Failures fixed (if any)

Review feedback:
- [ ] All threads resolved
- [ ] Each: evaluated → fixed/pushback → replied → resolved

Merge:
- [ ] `gh pr merge --squash --delete-branch`
- [ ] Issue marked Done
- [ ] Continue to next issue

## Integration

Called by: `issue-driven-development`, `autonomous-orchestration`

Follows: `pr-creation`

Uses: `receiving-code-review` (principles for evaluating feedback)

Completes: PR lifecycle
