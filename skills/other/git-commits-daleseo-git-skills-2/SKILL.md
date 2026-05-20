---
name: git-commits
description: Best practices for creating high-quality Git commits. Covers commit message conventions (Conventional Commits), atomic commits, staging strategies, and when to amend vs create new commits. Helps AI agents generate clean, meaningful commit history.
---

# Git Commit Best Practices

**Purpose:** This skill teaches AI agents to create high-quality commits with clear messages, proper granularity, and effective use of the staging area.

## Core Principles

1. **Atomic Commits** - One logical change per commit
2. **Clear Messages** - Follow Conventional Commits format
3. **Meaningful History** - Each commit tells a story
4. **Smart Staging** - Stage only what belongs together

## Commit Message Format

### Conventional Commits Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type Categories

```bash
# ✓ CORRECT: Use these standard types
feat:     # New feature for the user
fix:      # Bug fix
docs:     # Documentation changes
style:    # Formatting, missing semicolons, etc. (no code change)
refactor: # Code change that neither fixes a bug nor adds a feature
perf:     # Performance improvement
test:     # Adding or updating tests
chore:    # Maintenance tasks, dependencies, config

# Examples:
feat(auth): add password reset functionality
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(parser): simplify token extraction logic
```

### Subject Line Guidelines

```bash
# ✓ GOOD: Clear, concise, imperative mood
feat(auth): add OAuth2 login support
fix(cart): prevent duplicate items
docs(api): document rate limiting

# ✗ BAD: Vague, past tense, too long
feat(auth): added some authentication stuff
fix(cart): fixed a bug
docs(api): updated the documentation to include information about rate limiting
```

**Rules:**
- Use imperative mood ("add" not "added" or "adds")
- No period at the end
- Keep under 50 characters
- Capitalize first letter after type
- Be specific about what changed

### Body Guidelines

```bash
# ✓ GOOD: Explains WHY and context
feat(cache): add Redis caching layer

Improves API response time by 80% for frequently accessed data.
Uses Redis with 1-hour TTL for user profile and product catalog
endpoints. Falls back to database if Redis is unavailable.

Related to performance optimization initiative.

# ✗ BAD: Just repeats the subject
feat(cache): add Redis caching layer

Added Redis caching.
```

**When to include body:**
- Why the change was needed
- How it solves the problem
- Any important implementation decisions
- Side effects or limitations
- Related issues or context

**When to skip body:**
- Self-explanatory changes (e.g., "fix(typo): correct variable name")

### Footer Guidelines

```bash
# Breaking changes
feat(api): change user endpoint response format

BREAKING CHANGE: User API now returns camelCase instead of snake_case.
Migration guide: https://docs.example.com/migration/v2

# Issue references
fix(auth): prevent token expiration race condition

Closes #123
Refs #456

# Co-authors
feat(search): implement full-text search

Co-authored-by: Jane Doe <jane@example.com>
```

## Atomic Commits

### What is an Atomic Commit?

**Definition:** One commit = one logical change

```bash
# ✓ GOOD: Atomic commits
git commit -m "feat(auth): add login endpoint"
git commit -m "feat(auth): add logout endpoint"
git commit -m "test(auth): add login tests"

# ✗ BAD: Non-atomic commit
git commit -m "feat(auth): add login, logout, password reset, and tests"
```

### Benefits

1. **Easy to review** - Reviewer focuses on one change
2. **Easy to revert** - Undo specific change without affecting others
3. **Easy to cherry-pick** - Apply specific change to another branch
4. **Clear history** - Each commit has clear purpose

### How to Create Atomic Commits

```bash
# ✓ CORRECT: Stage related changes only
# You made changes to auth.js, api.js, and tests.js

# Commit 1: Feature implementation
git add src/auth.js src/api.js
git commit -m "feat(auth): add token refresh mechanism"

# Commit 2: Tests
git add tests/auth.test.js
git commit -m "test(auth): add token refresh tests"

# ✗ WRONG: Stage everything together
git add .
git commit -m "feat(auth): add token refresh and tests"
```

### Decision Tree: Should This Be One Commit?

```
Does this change have a single, clear purpose?
├─ YES → Can it be described in one sentence?
│  ├─ YES → One commit ✓
│  └─ NO  → Multiple commits
│
└─ NO → Multiple commits

Examples:
├─ "Add login validation" → One commit ✓
├─ "Add login and signup" → Two commits
└─ "Add login, fix bug, update docs" → Three commits
```

## Staging Strategies

### Strategy 1: Partial File Staging

```bash
# You changed multiple things in one file
# Only stage the lines related to current commit

git add -p src/app.js

# Interactive prompts:
# y - stage this hunk
# n - don't stage this hunk
# s - split into smaller hunks
# e - manually edit the hunk

# Then commit only staged changes
git commit -m "feat(app): add error handling"

# Stage and commit remaining changes separately
git add -p src/app.js
git commit -m "refactor(app): extract validation logic"
```

### Strategy 2: Multiple Commits from Unstaged Work

```bash
# ✓ WORKFLOW: Create multiple atomic commits from current changes

# Check what changed
git status
git diff

# Commit 1: Feature A
git add src/feature-a.js src/utils.js
git commit -m "feat(feature-a): implement feature A"

# Commit 2: Feature B
git add src/feature-b.js
git commit -m "feat(feature-b): implement feature B"

# Commit 3: Tests
git add tests/
git commit -m "test: add tests for features A and B"
```

### Strategy 3: Amend Last Commit

```bash
# Use case: You forgot to include a file in the last commit

# ✓ CORRECT: Amend if commit is NOT pushed yet
git add forgotten-file.js
git commit --amend --no-edit

# OR update the commit message too
git commit --amend -m "feat(auth): add login endpoint and middleware"

# ✗ WRONG: Amend if commit is already pushed
# This rewrites history and causes problems for collaborators

# If already pushed, create new commit instead:
git add forgotten-file.js
git commit -m "feat(auth): add missing middleware file"
```

## Common Workflows

### Workflow 1: Making a Feature Commit

```bash
# 1. Check current state
git status
git diff

# 2. Stage related changes only
git add src/feature.js src/api.js

# 3. Review what will be committed
git diff --staged

# 4. Commit with conventional format
git commit -m "feat(feature): add user profile customization

Allows users to customize avatar, bio, and theme preferences.
Settings are persisted to user preferences API endpoint.

Closes #234"

# 5. Verify commit
git log -1 --stat
```

### Workflow 2: Making Multiple Atomic Commits

```bash
# You worked on multiple things, now need to commit separately

# 1. Check all changes
git status

# 2. First commit: Core feature
git add src/core.js
git commit -m "feat(core): add data validation layer"

# 3. Second commit: API integration
git add src/api.js
git commit -m "feat(api): integrate validation with endpoints"

# 4. Third commit: Tests
git add tests/
git commit -m "test(validation): add comprehensive validation tests"

# 5. Fourth commit: Documentation
git add docs/
git commit -m "docs(validation): document validation rules"
```

### Workflow 3: Fixing a Bug

```bash
# ✓ GOOD: Clear bug fix commit

git add src/buggy-file.js
git commit -m "fix(cart): prevent duplicate items on double-click

Added debounce to 'Add to Cart' button and server-side duplicate
check. Prevents race condition when users click rapidly.

Fixes #567"

# Include:
# - What the bug was
# - How you fixed it
# - Issue reference
```

### Workflow 4: Amending vs New Commit Decision

```
Did I already push this commit?
├─ NO → Safe to amend
│  └─> git commit --amend
│
└─ YES → Create new commit instead
   └─> git commit -m "fix: ..."

Is this a fixup for recent commit?
└─> Consider git commit --fixup=<sha>
    Then use git rebase -i --autosquash before pushing
```

### Workflow 5: Refactoring Commits

```bash
# ✓ GOOD: Separate refactoring from behavior changes

# Commit 1: Pure refactor (no behavior change)
git add src/parser.js
git commit -m "refactor(parser): extract token validation to separate function

No behavior change. Makes code more testable and readable."

# Commit 2: Behavior change
git add src/parser.js
git commit -m "feat(parser): add support for nested tokens

Now supports tokens in format {{parent.child.value}}"

# Why separate?
# - Easy to verify refactor doesn't change behavior
# - Easy to revert feature without losing refactor
# - Clear history
```

## Common Mistakes to Avoid

### Mistake 1: Vague Commit Messages

```bash
# ✗ BAD: No context
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
git commit -m "wip"

# ✓ GOOD: Clear and specific
git commit -m "feat(auth): add JWT token expiration check"
git commit -m "fix(api): handle null values in user profile endpoint"
git commit -m "refactor(parser): simplify regex patterns"
git commit -m "docs(readme): add Docker setup instructions"
```

### Mistake 2: Mixing Unrelated Changes

```bash
# ✗ BAD: Multiple unrelated changes in one commit
git add .
git commit -m "feat: add login, fix cart bug, update docs"

# ✓ GOOD: Separate commits
git add src/auth.js
git commit -m "feat(auth): add OAuth login support"

git add src/cart.js
git commit -m "fix(cart): prevent negative quantities"

git add docs/
git commit -m "docs(api): update authentication endpoints"
```

### Mistake 3: Committing Debug Code

```bash
# ✗ BAD: Leaving console.log, debugger statements
git add src/app.js  # Contains console.log debugging
git commit -m "feat(app): add feature"

# ✓ GOOD: Review before committing
git diff --staged  # Check for debug code
# Remove debug statements
git add src/app.js
git commit -m "feat(app): add feature"
```

### Mistake 4: Too Large or Too Small Commits

```bash
# ✗ TOO LARGE: Entire feature in one commit
git commit -m "feat(auth): complete authentication system"
# 50 files changed, 2000+ lines

# ✗ TOO SMALL: Meaningless micro-commits
git commit -m "add semicolon"
git commit -m "fix typo"
git commit -m "add newline"

# ✓ GOOD: Right-sized atomic commits
git commit -m "feat(auth): add login endpoint"
git commit -m "feat(auth): add logout endpoint"
git commit -m "feat(auth): add token refresh mechanism"
git commit -m "test(auth): add authentication tests"
```

### Mistake 5: Amending Pushed Commits

```bash
# ✗ DANGEROUS: Amending after push
git push origin feature-branch
# Oh, forgot a file!
git add forgotten.js
git commit --amend --no-edit
git push --force origin feature-branch  # ← Causes problems!

# ✓ SAFE: New commit instead
git push origin feature-branch
# Oh, forgot a file!
git add forgotten.js
git commit -m "feat(auth): add missing validation helper"
git push origin feature-branch
```

## Commit Message Templates

### Template for Features

```bash
feat(<scope>): <what you added>

<why this feature is needed>
<how it works (if not obvious)>
<any limitations or considerations>

Closes #<issue-number>
```

### Template for Bug Fixes

```bash
fix(<scope>): <what you fixed>

<what was wrong>
<how you fixed it>
<why this approach>

Fixes #<issue-number>
```

### Template for Refactoring

```bash
refactor(<scope>): <what you refactored>

No behavior change. <why refactor was needed>
<what improved (readability, performance, maintainability)>
```

## Integration with AI Code Generation

When AI agents generate code that needs committing:

### 1. Analyze Changes Before Committing

```bash
# ✓ CORRECT: Check what changed
git status
git diff

# Determine:
# - Is this one logical change or multiple?
# - What type of change? (feat, fix, refactor, etc.)
# - What scope? (auth, api, ui, etc.)
```

### 2. Create Appropriate Commit Message

```bash
# ✓ GOOD: AI-generated message with context
git commit -m "feat(api): add rate limiting middleware

Implements token bucket algorithm with 100 requests/minute limit.
Returns 429 status with Retry-After header when limit exceeded.

Addresses security requirement from issue #789"

# ✗ BAD: Generic AI message
git commit -m "add rate limiting"
```

### 3. Split Large Changes

```bash
# If AI generated multiple files for different purposes:

# ✓ CORRECT: Separate commits
git add src/rate-limiter.js
git commit -m "feat(api): add rate limiting middleware"

git add tests/rate-limiter.test.js
git commit -m "test(api): add rate limiter tests"

git add docs/api.md
git commit -m "docs(api): document rate limiting"

# ✗ WRONG: One large commit
git add .
git commit -m "add rate limiting with tests and docs"
```

## Quick Reference Checklist

Before every commit, ask:

- [ ] Is this one logical change?
- [ ] Did I stage only related files?
- [ ] Is my commit message in Conventional Commits format?
- [ ] Does the subject line clearly describe what changed?
- [ ] Did I explain why (not just what) in the body?
- [ ] Did I remove debug code and comments?
- [ ] Is this commit NOT already pushed? (if planning to amend)
- [ ] Would this be easy to review?
- [ ] Would this be easy to revert if needed?

## Advanced: Commit Message Psychology

Good commit messages answer:

1. **What changed?** (Subject line)
2. **Why was it needed?** (Body - business reason)
3. **How does it work?** (Body - technical approach)
4. **What are the side effects?** (Body - impacts)

```bash
# ✓ EXCELLENT: Answers all questions
feat(search): implement fuzzy search algorithm

Users frequently make typos in search queries, resulting in zero
results and poor experience. Implemented Levenshtein distance-based
fuzzy matching with tolerance of 2 characters.

Performance impact: ~50ms additional latency for searches, acceptable
given improved user experience. Results are cached for 5 minutes.

Closes #456
```

## Summary

**Key Principles:**
1. **One commit = one logical change** (atomic commits)
2. **Use Conventional Commits format** (type, scope, clear subject)
3. **Explain why, not just what** (meaningful commit messages)
4. **Stage strategically** (use `git add -p` for partial staging)
5. **Never amend pushed commits** (creates new commit instead)

**Quick Command Reference:**
```bash
git add <file>                    # Stage specific file
git add -p <file>                 # Stage parts of file interactively
git diff --staged                 # Review what will be committed
git commit -m "type(scope): msg"  # Commit with message
git commit --amend --no-edit      # Amend last commit (if not pushed)
git log -1 --stat                 # Verify last commit
```

**Remember:** Commits are documentation of your project's history. Write them for humans who will read them 6 months from now.
