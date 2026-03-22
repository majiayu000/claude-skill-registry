---
name: pr-standards
description: >
  Enforce pull request best practices: size limits, description templates, testing
  requirements, and review workflows. Activate whenever the user creates a PR, asks about
  PR best practices, sets up PR templates, discusses code review turnaround, or mentions
  PR size, review requirements, or branch protection rules.
---

# Pull Request Standards

Define and enforce PR best practices to keep reviews fast, thorough, and productive.
Small PRs with clear descriptions get reviewed faster and have fewer bugs.

## When to Use
- Creating a pull request
- Setting up PR templates for a repository
- Establishing team review guidelines
- Configuring branch protection rules
- Discussing why PRs are too large or reviews are slow

## Core Patterns

### PR Size Limits

Keep PRs small and focused. Target under 400 lines of meaningful changes.

```
Size Guidelines:
  XS  (1-50 lines)    - Typo fix, config change, one-liner bug fix
  S   (51-200 lines)   - Small feature, focused bug fix, single-file refactor
  M   (201-400 lines)  - Standard feature, multi-file change
  L   (401-800 lines)  - Large feature (split if possible)
  XL  (800+ lines)     - Too large. Must be split into smaller PRs.

Lines counted: Additions + deletions in application code.
Excluded from count: Lock files, generated code, snapshots, migrations.
```

Strategies for splitting large PRs:

```markdown
1. Layer-by-layer: Database schema -> Backend API -> Frontend UI
2. Feature flags: Merge incomplete features behind flags
3. Refactor-then-feature: Separate refactoring PR from feature PR
4. Vertical slices: One complete user story per PR
```

### PR Description Template

```markdown
<!-- .github/pull_request_template.md -->
## Summary
<!-- What does this PR do and why? 1-3 bullet points. -->

## Changes
<!-- List the key changes made. Group by area if helpful. -->

## Testing
<!-- How was this tested? Include commands to reproduce. -->
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Edge cases covered

## Screenshots
<!-- If UI changes, include before/after screenshots. -->

## Related
<!-- Link to issue, Jira ticket, or previous PR. -->
Closes #

## Checklist
- [ ] Self-review completed
- [ ] No console.log or debug statements
- [ ] No hardcoded secrets
- [ ] Tests pass locally
- [ ] Documentation updated (if applicable)
```

### Branch Protection Rules

Configure branch protection to enforce quality gates.

```yaml
# Repository Settings -> Branches -> Branch protection rules for "main"

Required checks:
  - CI / lint (required)
  - CI / test (required)
  - CI / build (required)

Review requirements:
  - Required approving reviews: 1 (2 for large teams)
  - Dismiss stale reviews when new commits are pushed: true
  - Require review from CODEOWNERS: true

Other settings:
  - Require branches to be up to date before merging: true
  - Require linear history: true (encourages rebase over merge commits)
  - Restrict who can push: maintainers only
  - Do not allow bypassing the above settings: true
```

### Label System

Use labels to communicate PR status and type at a glance.

```markdown
## Type Labels
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring (no behavior change)
- `docs` - Documentation only
- `test` - Test additions or fixes
- `chore` - Build, CI, dependencies

## Size Labels (auto-applied via GitHub Action)
- `size/XS` - 1-50 lines
- `size/S` - 51-200 lines
- `size/M` - 201-400 lines
- `size/L` - 401-800 lines (triggers warning comment)
- `size/XL` - 800+ lines (blocks merge)

## Status Labels
- `needs-review` - Ready for review
- `changes-requested` - Author must address feedback
- `approved` - Ready to merge
- `blocked` - Waiting on external dependency
- `do-not-merge` - Intentionally held
```

Auto-label PR size with a GitHub Action:

```yaml
# .github/workflows/pr-size.yml
name: PR Size Label
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  size-label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_max_size: 50
          s_max_size: 200
          m_max_size: 400
          l_max_size: 800
          fail_if_xl: true
          message_if_xl: >
            This PR exceeds 800 lines. Please split it into smaller,
            focused PRs for easier review.
```

### Review Turnaround Time

Set expectations for review responsiveness.

```markdown
## Review SLA (Service Level Agreement)

| Priority | First Review | Follow-up |
|----------|-------------|-----------|
| Critical (P0) | 2 hours | 1 hour |
| High (P1) | 4 hours | 2 hours |
| Normal (P2) | 1 business day | 4 hours |
| Low (P3) | 2 business days | 1 business day |

## Guidelines for Authors
- Request review only when PR is truly ready (CI passes, self-reviewed)
- Tag specific reviewers; avoid "anyone" requests
- Respond to review comments within 4 hours
- Mark conversations as resolved after addressing them
- Re-request review after addressing all comments

## Guidelines for Reviewers
- Acknowledge the PR within the SLA even if full review takes longer
- Distinguish blocking (CRITICAL/HIGH) from non-blocking (MEDIUM/LOW) feedback
- Approve with comments for non-blocking suggestions
- Avoid starting a review you cannot finish within 2 hours
```

### Self-Review Before Requesting Review

```markdown
## Author Self-Review Checklist (do before requesting review)

1. Read every line of your own diff in the GitHub UI
2. Verify all tests pass in CI
3. Remove debug statements and TODOs
4. Check for accidental file inclusions (.env, IDE configs)
5. Confirm the PR description is complete
6. Verify the PR is against the correct base branch
7. Check that commit messages follow conventions
8. If UI change: attach screenshots or screen recordings
```

## Anti-Patterns
- Submitting PRs with thousands of lines and expecting thorough review
- Using "WIP" PRs as a status update mechanism instead of draft PRs
- Requesting review before CI passes
- Approving PRs without reading the code ("LGTM" culture)
- Merging your own PRs without any review
- Leaving PRs open for days without response from either side
- Squashing all commits into one, losing useful commit history
- Using PR descriptions like "fixes stuff" or leaving them empty

## Quick Reference

| Standard | Target |
|----------|--------|
| PR size | Under 400 lines of application code |
| Description | Summary + changes + testing + related issue |
| Required reviews | 1 minimum (2 for critical paths) |
| CI checks | Lint + test + build must pass |
| Review turnaround | Under 1 business day for normal priority |
| Author response | Under 4 hours for review comments |
| Self-review | Always before requesting review |
| Labels | Type + size applied to every PR |
