---
name: pr-description
description: Pull request authoring standards — structured descriptions, linking issues, providing test evidence, and writing good summaries. Reference when creating or describing pull requests.
---

# Pull Request Description Standards

## PR Title Conventions

The PR title is the first thing reviewers see. It must communicate the change clearly and concisely.

### Format

```
<type>: <concise description of what changed>
```

### Type Prefixes

| Prefix | Use When |
|---|---|
| `feat:` | Adding new functionality |
| `fix:` | Correcting a bug |
| `refactor:` | Restructuring without behavior change |
| `docs:` | Documentation only |
| `test:` | Adding or updating tests |
| `chore:` | Dependencies, tooling, config |
| `perf:` | Performance improvement |
| `style:` | Formatting, whitespace, naming |
| `ci:` | CI/CD pipeline changes |
| `revert:` | Reverting a previous change |

### Title Rules

1. Keep under 72 characters
2. Use imperative mood: "Add search endpoint" not "Added search endpoint" or "Adds search endpoint"
3. Do not end with a period
4. Be specific: "fix: resolve login redirect loop on expired sessions" not "fix: login bug"
5. Include ticket number if applicable: "feat: add user search (PROJ-1234)"

### Good vs Bad Titles

```
Bad:  "Updates"
Good: "feat: add full-text search to user directory"

Bad:  "Fix bug"
Good: "fix: prevent duplicate charge on payment retry"

Bad:  "Refactoring the auth module and also fixing some tests and updating docs"
Good: "refactor: extract token validation into dedicated service"
```

## PR Description Template

Every PR should follow a structured description. Use this template as a starting point and adapt to your team's needs.

### Standard Template

```markdown
## Summary

A 1-3 sentence overview of what this PR does and why. This should be understandable
by someone who has not read the code.

## Motivation

Why is this change needed? Link to the issue, bug report, or product requirement
that motivated this work.

Closes #123

## Changes

A bulleted list of the specific changes made:

- Added `SearchService` class with full-text query support
- Created `/api/users/search` endpoint with pagination
- Added search index migration for the users table
- Updated API documentation with new endpoint

## Test Plan

How was this change tested? Be specific.

- [ ] Unit tests for `SearchService` covering empty queries, partial matches, and pagination
- [ ] Integration test for the search endpoint with test database
- [ ] Manual testing: verified search returns expected results in staging
- [ ] Load tested with 10k users in the index

## Screenshots / Recordings

If the change has a visual component, include before/after screenshots or a screen
recording. For API changes, include example request/response pairs.

**Before:**
(screenshot or N/A)

**After:**
(screenshot or N/A)

## Notes for Reviewers

Any additional context that will help reviewers:

- I chose cursor-based pagination over offset because [reason]
- The migration is backward-compatible and can be rolled back
- This depends on PR #456 being merged first

## Checklist

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation updated if needed
- [ ] No secrets or credentials included
- [ ] Migration is reversible (if applicable)
- [ ] Breaking changes documented (if applicable)
```

### Minimal Template (for Small Changes)

```markdown
## Summary

Fix null pointer exception when user profile has no avatar set.

Closes #789

## Changes

- Added null check in `UserProfile.getAvatarUrl()`
- Added test case for users without avatars

## Test Plan

- [x] Unit test added for the null avatar case
- [x] Existing tests pass
```

## Linking Issues

### Automatic Issue Closing

Use GitHub keywords in the PR description body to automatically close issues when the PR merges:

```markdown
Closes #123
Fixes #456
Resolves #789
```

- Place these in the **Motivation** or **Summary** section
- Use one keyword per issue, each on its own line for multiple issues
- These keywords are case-insensitive

### Cross-Repository References

```markdown
Closes org/other-repo#123
```

### Linking Without Closing

When a PR is related to but does not fully resolve an issue:

```markdown
Related to #123
Part of #456
See also #789
```

## Draft PRs vs Ready-for-Review

### When to Open a Draft PR

Open a draft PR when:

- You want early feedback on your approach before finishing
- The work is in progress but you want CI to run
- You are working on a stacked PR that depends on another PR
- You want to share progress with the team without requesting formal review
- You need to collaborate with another developer on the branch

### Draft PR Etiquette

1. Prefix the title with `[WIP]` or `[Draft]` in addition to using GitHub's draft status
2. State what is done and what remains in the description:

```markdown
## Status

Done:
- [x] Database schema and migration
- [x] Repository layer

Remaining:
- [ ] Service layer business logic
- [ ] API endpoint
- [ ] Tests

## What I Need Feedback On

- Is the schema design appropriate for the query patterns we expect?
- Should we use a separate table for search metadata?
```

3. Convert to ready-for-review only when all work is complete
4. Do not request specific reviewers on draft PRs unless you need targeted feedback

### Converting to Ready

Before converting a draft PR to ready-for-review:

- [ ] All commits are clean and well-organized
- [ ] Description is complete with all template sections filled
- [ ] CI passes
- [ ] Self-review completed (see checklist below)
- [ ] WIP or Draft prefix removed from title

## PR Size Guidelines

### Target Size

| Metric | Target | Maximum |
|---|---|---|
| Lines changed | 50-200 | 400 |
| Files changed | 1-8 | 15 |
| Commits | 1-5 | 10 |
| Review time | 15-30 min | 60 min |

### Why Small PRs Matter

- Faster review turnaround (hours not days)
- Higher quality reviews (reviewers stay focused)
- Easier to revert if something breaks
- Less merge conflict risk
- Better git history for debugging

### Breaking Down Large Changes

When a change exceeds size guidelines, split it into a sequence of PRs:

1. **Infrastructure first** -- Schema changes, new interfaces, configuration
2. **Core logic** -- Business logic implementation
3. **Integration** -- Wiring components together, endpoint creation
4. **Polish** -- Error handling improvements, logging, documentation

Each PR should be independently mergeable and should not break existing functionality.

### Acceptable Large PRs

Some PRs are legitimately large:

- Generated code (migrations, protobuf output, lock files)
- Bulk rename or reformatting (use a separate commit or PR)
- Dependency upgrades with lock file changes
- Initial project scaffolding

Mark these clearly in the description: "Note: This PR is large because it includes generated migration files. The actual hand-written changes are in `src/services/` (~80 lines)."

## Stacked PRs

Stacked PRs break a large feature into a chain of dependent PRs that build on each other.

### When to Use Stacked PRs

- A feature requires 500+ lines of changes
- You want reviewers to focus on one logical layer at a time
- Multiple developers are working on interconnected changes

### Stacked PR Workflow

```
PR #1: feat: add user search database schema
  └── PR #2: feat: add search service with query logic
       └── PR #3: feat: add search API endpoint and docs
```

### Stacked PR Rules

1. Each PR in the stack must work independently if merged alone (no broken states)
2. Number the PRs and cross-reference them:

```markdown
## Stack

This is PR 2 of 3 in the search feature stack:
1. #100 - Database schema (merged)
2. **#101 - Search service (this PR)**
3. #102 - API endpoint (draft, depends on this PR)
```

3. Base each PR on the previous PR's branch, not on main:

```bash
# PR 1
git checkout -b feature/search-schema

# PR 2 (based on PR 1)
git checkout -b feature/search-service feature/search-schema

# PR 3 (based on PR 2)
git checkout -b feature/search-endpoint feature/search-service
```

4. When an earlier PR is merged, rebase subsequent PRs onto main
5. Review and merge in order -- do not merge PR 3 before PR 1

### Updating Stacked PRs After Review

When you need to update PR 1 based on review feedback:

```bash
# Make changes on PR 1's branch
git checkout feature/search-schema
# ... make changes, commit ...

# Rebase PR 2 onto updated PR 1
git checkout feature/search-service
git rebase feature/search-schema

# Rebase PR 3 onto updated PR 2
git checkout feature/search-endpoint
git rebase feature/search-service

# Force-push all updated branches
git push --force-with-lease origin feature/search-schema
git push --force-with-lease origin feature/search-service
git push --force-with-lease origin feature/search-endpoint
```

## Self-Review Checklist

Before requesting review, go through the PR yourself as if you were the reviewer.

### Code Quality

- [ ] No commented-out code left behind
- [ ] No debug logging (console.log, print statements) unless intentional
- [ ] No TODO comments without associated issue numbers
- [ ] Variable and function names are clear and consistent
- [ ] No unnecessary complexity -- could this be simpler?
- [ ] No duplicated logic that should be extracted

### Correctness

- [ ] Edge cases handled (null, empty, boundary values)
- [ ] Error cases handled with appropriate messages
- [ ] No race conditions in concurrent code
- [ ] Database queries are efficient (no N+1, proper indexes)
- [ ] Feature flags used for incomplete or experimental features

### Security

- [ ] No secrets, API keys, or credentials in the code
- [ ] User input is validated and sanitized
- [ ] Authentication and authorization checks present where needed
- [ ] SQL injection, XSS, and CSRF protections in place
- [ ] Sensitive data is not logged

### Testing

- [ ] New code has corresponding tests
- [ ] Tests cover happy path and error cases
- [ ] Tests are deterministic (no flaky tests)
- [ ] Test names clearly describe what they verify

### Documentation

- [ ] Public APIs have documentation
- [ ] Complex logic has explanatory comments
- [ ] README updated if setup steps changed
- [ ] CHANGELOG updated for user-facing changes
- [ ] API documentation updated for endpoint changes

### Diff Review

- [ ] Reviewed the full diff on GitHub before requesting review
- [ ] No unintended file changes (formatting, unrelated fixes)
- [ ] Commit history is clean and logical
- [ ] No merge commits from pulling main (rebase instead)

## Responding to Review Feedback

### Etiquette

1. Respond to every comment, even if just with "Done" or "Fixed"
2. If you disagree, explain your reasoning respectfully and propose alternatives
3. Do not resolve comments yourself unless your team convention allows it -- let the reviewer resolve their own comments
4. If a discussion becomes lengthy, move it to a call and summarize the outcome in the PR
5. Push review fixes as new commits during review, squash before merge

### Handling Requested Changes

```markdown
## Review Response

- **[Comment about error handling]** Fixed -- added try/catch with proper logging in abc123
- **[Comment about naming]** Renamed `processData` to `validateAndStorePayment` in def456
- **[Comment about test coverage]** Added edge case tests for empty input in ghi789
- **[Comment about architecture]** I'd prefer to keep this in a single service for now --
  the traffic doesn't justify the complexity of splitting. Happy to discuss further.
```

## Example: Well-Written PR

```markdown
# feat: add cursor-based pagination to user search endpoint

## Summary

Replaces the offset-based pagination on `/api/users/search` with cursor-based
pagination to handle our growing user base without performance degradation.

## Motivation

The user directory now has 2M+ records. Offset pagination causes increasingly
slow queries at high page numbers because the database must scan and discard
rows. Cursor-based pagination maintains constant performance regardless of
position.

Closes #1234

## Changes

- Replaced `page` and `per_page` params with `cursor` and `limit`
- Added `next_cursor` and `has_more` to response envelope
- Updated `UserRepository.search()` to use keyset pagination on `(created_at, id)`
- Added database index on `(created_at, id)` for the users table
- Marked old `page` parameter as deprecated with warning header
- Updated API docs with new pagination format

## Test Plan

- [x] Unit tests for cursor encoding/decoding
- [x] Integration tests verifying correct page traversal over 1000 records
- [x] Verified backward compatibility: requests with `page` param still work (with deprecation warning)
- [x] Load test: p99 latency at page 10000 dropped from 2.3s to 45ms

## Notes for Reviewers

- The cursor is a base64-encoded JSON of `{created_at, id}` -- intentionally opaque to clients
- Old `page` parameter will be removed in v3.0 (tracked in #1235)
- Migration `20240115_add_users_pagination_index.sql` is safe to run on production without downtime
```
