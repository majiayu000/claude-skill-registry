---
name: pr-monitor
description: Monitor PR for CI status, reviews, and coordinate response workflow
category: Delivery
---

# Skill: pr-monitor

## What I do

I help you manage and track the progress of pull requests. I focus on monitoring CI/CD status, review comments, and approval states. I ensure that PRs are moved through the pipeline efficiently and that all feedback is addressed promptly.

## When to use me

- When you've submitted a PR and need to track its progress.
- When you're waiting for reviews from teammates.
- When you need to check why a CI build failed.
- When you're preparing to merge a PR.

## Core principles

1. **Continuous monitoring**, check the status of your PRs regularly to avoid delays.
2. **Proactive communication**, respond to review comments quickly and notify reviewers when changes are made.
3. **CI-first approach**, always fix CI failures before asking for a review.
4. **Draft by default**, use draft PRs for work-in-progress to signal that it's not ready for final review.

## Patterns & examples

### Checking PR status with GitHub CLI
Use the `gh` command to stay updated.
- `gh pr status`, See a summary of your PRs.
- `gh pr view`, See details of a specific PR, including reviews and checks.
- `gh pr checks`, List the status of all CI checks.

### Responding to feedback
Address all comments before re-requesting a review.
- **Pattern**, Fix the issue, push the change, and then reply to the comment confirming the fix. If you disagree, explain your reasoning clearly and politely.

### Resolving review threads
After addressing a review comment and replying, resolve the thread via the GraphQL API.

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

### Monitoring for conflicts
Keep your branch up to date with the base branch.
- **Action**, Regularly rebase or merge the base branch (e.g., `main`) into your PR branch to catch conflicts early.

### Quality PR descriptions
Help reviewers by providing context.
- **Good**, Include a summary of changes, why they were made, and how to test them. Link to related issues.

## Anti-patterns to avoid

- ❌ **The "Ghost" PR**, leaving a PR unattended for days while CI is failing or reviewers are waiting.
- ❌ **Merging with failed checks**, never merge a PR if CI/CD checks have failed, unless there is an exceptional and documented reason.
- ❌ **Ignoring negative reviews**, merging a PR without addressing a "Request Changes" review from a teammate.
- ❌ **Too many commits**, avoid pushing dozens of tiny "fix typo" commits. Squash or clean up your history before the final merge.
- ❌ **Leaving threads unresolved after addressing them**. Addressed threads should always be resolved to clear them for the reviewer.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Delivery/PR Monitor.md`

## Related skills

- `github-expert`, for advanced CLI usage.
- `release-management`, for coordinating merges.
- `documentation-writing`, for better PR descriptions.
- `git-master`, for branch management.
