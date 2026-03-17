---
name: task-pull-request
description: Author pull requests and respond to review feedback. Use when creating PRs, requesting reviews, reading comments, addressing feedback, or merging changes.
---

# Pull Request Workflow

This skill covers the end-to-end workflow for authoring pull requests using the GitHub CLI (`gh`).

## When to Use This Skill

Use this skill when:
- Creating a pull request from your changes
- Requesting review from teammates
- Reading and responding to review comments
- Addressing requested changes
- Merging completed PRs

## The PR Lifecycle

```
┌──────────────┐
│  Create PR   │
└──────┬───────┘
       ↓
┌──────────────┐
│Request Review│
└──────┬───────┘
       ↓
┌──────────────┐     ┌────────────────┐
│ Wait/Check   │────→│ Read Feedback  │
│   Status     │     └───────┬────────┘
└──────────────┘             ↓
       ↑            ┌────────────────┐
       │            │Address Changes │
       │            └───────┬────────┘
       │                    ↓
       └────────────┌───────────────┐
                    │  Push Updates │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Merge      │
                    └───────────────┘
```

---

## Creating a Pull Request

### Basic Creation

```bash
# Interactive mode (prompts for details)
gh pr create

# With title and body inline
gh pr create --title "feat: add user authentication" --body "Adds login flow"

# Create as draft (not ready for review)
gh pr create --draft

# Target a specific base branch
gh pr create --base develop
```

### Multi-line PR Body (Recommended)

Use a heredoc for well-formatted PR descriptions:

```bash
gh pr create --title "feat: add user authentication" --body "$(cat <<'EOF'
## Summary
- Added login/logout endpoints
- Implemented session management
- Added auth middleware

## Test Plan
- [ ] Run `npm test` to verify unit tests
- [ ] Manual test: login flow works
- [ ] Manual test: protected routes require auth

## Notes
- Requires `AUTH_SECRET` env var in production
EOF
)"
```

### PR Description Best Practices

Include these sections:

| Section | Purpose |
|---------|---------|
| **Summary** | What changed and why (bullet points) |
| **Test Plan** | How to verify the changes work |
| **Notes** | Deployment considerations, breaking changes |

---

## Requesting Review

### Add Reviewers

```bash
# Request review from specific users
gh pr edit <number> --add-reviewer username1,username2

# Or during creation
gh pr create --reviewer username1,username2

# Request review from a team
gh pr edit <number> --add-reviewer org/team-name
```

### Re-request Review After Updates

After addressing feedback, re-request review:

```bash
# Re-request from the same reviewers
gh pr edit <number> --add-reviewer username
```

---

## Checking PR Status

### View PR Details

```bash
# View current branch's PR
gh pr view

# View specific PR
gh pr view 123

# Open in browser
gh pr view 123 --web

# JSON output for specific fields
gh pr view 123 --json state,reviews,comments,statusCheckRollup
```

### Check CI Status

```bash
# View CI checks on current PR
gh pr checks

# View checks on specific PR
gh pr checks 123

# Watch checks until complete
gh pr checks 123 --watch
```

### List PRs

```bash
# List open PRs
gh pr list

# Your PRs
gh pr list --author @me

# PRs requesting your review
gh pr list --search "review-requested:@me"

# PRs with specific state
gh pr list --state merged
gh pr list --state closed
```

---

## Reading Review Feedback

### View PR Comments and Reviews

```bash
# Get PR review comments (inline code comments)
gh api repos/{owner}/{repo}/pulls/123/comments --jq '.[] | {path: .path, line: .line, body: .body, user: .user.login}'

# Get conversation comments (not inline)
gh api repos/{owner}/{repo}/issues/123/comments --jq '.[] | {body: .body, user: .user.login}'

# Get review summaries
gh api repos/{owner}/{repo}/pulls/123/reviews --jq '.[] | {state: .state, body: .body, user: .user.login}'
```

### Quick View with gh pr view

```bash
# See comments in terminal
gh pr view 123 --comments
```

### Understanding Review States

| State | Meaning |
|-------|---------|
| `APPROVED` | Reviewer approved the changes |
| `CHANGES_REQUESTED` | Reviewer wants changes before merge |
| `COMMENTED` | Reviewer left comments without approval/rejection |
| `PENDING` | Review started but not submitted |

---

## Responding to Feedback

### The Response Cycle

1. **Read** the feedback carefully
2. **Address** each comment with code changes
3. **Commit** with clear messages referencing the feedback
4. **Push** updates
5. **Reply** to comments explaining what changed
6. **Re-request** review if needed

### Making Targeted Fixes

```bash
# Make changes to address feedback
# ... edit files ...

# Commit with clear message
git add <files>
git commit -m "fix(review): add input validation per feedback"

# Push updates
git push
```

### Replying to Comments

Sign agent-generated comments to distinguish them from human comments:

```bash
# Add a general comment to the PR
gh pr comment 123 --body "$(cat <<'EOF'
Addressed all feedback. Ready for re-review.

---
*Generated by [Claude Code](https://claude.ai/code)*
EOF
)"

# Reply to a specific review comment
gh api repos/{owner}/{repo}/pulls/123/comments/<comment_id>/replies \
  -f body="Fixed in commit abc123. Added the validation you suggested.

---
*Generated by [Claude Code](https://claude.ai/code)*"
```

**Always sign agent comments** so reviewers know the response was AI-generated.

### Structured Response Format

When responding to multiple review comments:

```markdown
Addressed review feedback:

**Changed:**
- Added input validation (commit abc123)
- Fixed error handling in parse() (commit def456)
- Added test for edge case (commit ghi789)

**Not changed:**
- Kept existing error format per project conventions (discussed in comment)

**Verified:**
- All tests pass
- Manual testing complete

---
*Generated by [Claude Code](https://claude.ai/code)*
```

---

## Handling Common Feedback Patterns

### "Add tests for this"

```bash
# Add the test
# ... write test ...
git add tests/
git commit -m "test: add coverage for new validation logic"
git push
```

### "This could be null/undefined"

```bash
# Add null check
# ... fix code ...
git add src/
git commit -m "fix: add null check per review feedback"
git push
```

### "Please split this PR"

If the PR is too large or mixes concerns:

1. Note which changes to separate
2. Create a new branch for the split-off work
3. Remove those changes from current PR
4. Create separate PR for split-off work

---

## Merging the PR

### Agent Self-Review (Recommended)

If you're an AI agent authoring a PR, request independent review before merging:

```
Use the tsc-reviewer agent to review this PR
```

The reviewer agent will:
1. Run `gh pr diff` to analyze changes
2. Evaluate correctness, security, and maintainability
3. Return findings with a verdict (APPROVED / CHANGES REQUESTED)

**Why self-review matters:**
- You cannot impartially review your own code
- Independent review catches blind spots and confirmation bias
- Mandatory for repositories with quality gates

Loop until approved:
```
Create PR → spawn reviewer → fix blockers → re-spawn reviewer → approved → merge
```

### Pre-merge Checklist

Before merging, verify:
- [ ] All review comments addressed
- [ ] CI checks passing (`gh pr checks`)
- [ ] Approved by required reviewers
- [ ] No merge conflicts

### Merge Commands

```bash
# Merge (uses repo's default strategy)
gh pr merge 123

# Specific strategies
gh pr merge 123 --squash        # Squash commits into one
gh pr merge 123 --merge         # Create merge commit
gh pr merge 123 --rebase        # Rebase onto base branch

# Delete branch after merge
gh pr merge 123 --squash --delete-branch

# Auto-merge when checks pass
gh pr merge 123 --auto --squash
```

### Verify Merge

```bash
# Confirm PR was merged
gh pr view 123 --json state,mergedAt
```

---

## Handling Merge Conflicts

### Resolve Conflicts Locally

```bash
# Fetch latest and rebase
git fetch origin
git rebase origin/main

# Resolve conflicts in editor
# ... fix conflicts ...

# Continue rebase
git add <resolved-files>
git rebase --continue

# Force push (safe for feature branches)
git push --force-with-lease
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| Create draft PR | `gh pr create --draft` |
| Request review | `gh pr edit 123 --add-reviewer user` |
| View PR | `gh pr view 123` |
| Check CI status | `gh pr checks 123` |
| View comments | `gh pr view 123 --comments` |
| Add comment | `gh pr comment 123 --body "..."` |
| Merge (squash) | `gh pr merge 123 --squash --delete-branch` |
| Verify merged | `gh pr view 123 --json state,mergedAt` |

---

## Anti-Patterns to Avoid

### Merging Without Addressing Feedback

**Wrong**: Get comments → ignore → merge anyway

**Right**: Get comments → address each one → get approval → merge

### Giant "Address Feedback" Commits

**Wrong**: Fix 10 issues in one commit with vague message

**Right**: Targeted commits per issue: `fix(review): add null check`, `test: add edge case coverage`

### Silent Fixes

**Wrong**: Fix issue → push → say nothing

**Right**: Fix issue → push → reply to comment explaining the fix

### Premature Merge

**Wrong**: Create PR → CI green → merge immediately

**Right**: Create PR → request review → address feedback → get approval → merge
