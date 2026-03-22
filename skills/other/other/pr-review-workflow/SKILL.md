---
name: pr-review-workflow
description: Orchestrate incremental PR review feedback addressing with systematic triage and verification
category: Delivery
---

# Skill: pr-review-workflow

## What I do

I provide a structured workflow for handling pull request feedback. I guide you through fetching comments, triaging them into actionable tasks, and verifying fixes incrementally. This ensures no feedback is missed and the PR remains stable during updates.

## When to use me

- When a reviewer has requested changes on your pull request.
- When you need to address a large number of comments across multiple files.
- When you want to ensure your PR is rebased and verified before final merge.

## Core principles

1. **Triage before action**. List every comment before you start changing code. This prevents context switching and missed items.
2. **Incremental updates**. Address one concern at a time. Run tests and checks after each fix.
3. **Continuous verification**. Use language server diagnostics and test suites to confirm each change.
4. **Individual accountability**. Reply to every comment thread on GitHub. A general summary is not enough for reviewers.
5. **Fresh history**. Keep your branch up to date with the target branch through regular rebasing.

## Workflow

1. **Fetch feedback**. Use `github-expert` to retrieve all inline and general comments.
2. **Triage items**. Create a task list using `todowrite`. Group related comments if they touch the same logic.
3. **Address concerns**. For each item, apply the fix. Use `respond-to-review` for the detailed implementation and evidence gathering.
4. **Verify fixes**. Run `lsp_diagnostics` and relevant tests. Do not wait until the end to find regressions.
5. **Sync and push**. Rebase onto the target branch once all items are addressed. Use `gh` to reply to each thread before pushing.
6. **Resolve threads**. Resolve each addressed thread via GraphQL API.
7. **Final check**. Run the `pre-merge` checklist to ensure the PR is ready for approval.

## Patterns & examples

**Fetching comments with `github-expert`:**
```bash
# Get inline comments for a specific PR
gh api repos/{owner}/{repo}/pulls/{PR}/comments | jq '.[] | {id: .id, path: .path, line: .line, body: .body}'
```

**Creating a triage list:**
```typescript
todowrite({
  todos: [
    { content: "Fix typo in variable name in server.go", priority: "low", status: "pending" },
    { content: "Refactor database connection logic to use pooling", priority: "high", status: "pending" },
    { content: "Add missing unit test for error handling", priority: "medium", status: "pending" }
  ]
})
```

**Replying to threads:**
```bash
# Reply to a specific comment ID
gh api repos/{owner}/{repo}/pulls/{PR}/comments -X POST -f body="Addressed by extracting the function for better reuse." -F in_reply_to={comment_id}
```

**Resolving threads via GraphQL:**
```bash
# Get thread IDs
gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: NUM) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              databaseId
              body
            }
          }
        }
      }
    }
  }
}'

# Resolve thread
gh api graphql -f query='mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread {
      isResolved
    }
  }
}'
```

## Anti-patterns to avoid

- ❌ **Bulk fixes**. Making dozens of changes before running tests. This makes debugging regressions difficult.
- ❌ **General replies**. Posting a single "Done" comment at the PR level instead of replying to individual threads.
- ❌ **Ignoring feedback**. Not addressing or justifying why a requested change was rejected.
- ❌ **Stale branches**. Addressing feedback on an old version of the branch without rebasing.
- ❌ **Replying to comments without resolving the thread**. Forgetting to mark addressed threads as resolved.

## KB Reference
`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Delivery/PR Review Workflow.md`

## Related skills
- `code-reviewer` - For understanding the reviewer's perspective and performing your own reviews.
- `respond-to-review` - For the specific methodology of implementing and documenting individual feedback items.
- `pre-merge` - For final validation once all feedback is addressed.
- `github-expert` - For GitHub CLI operations and API queries.
