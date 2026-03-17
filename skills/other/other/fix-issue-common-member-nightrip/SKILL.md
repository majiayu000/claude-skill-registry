---
name: fix-issue
description: Fix a GitHub issue using SDD workflow. Reads the issue, reproduces the bug with a failing test, then fixes it.
disable-model-invocation: true
argument-hint: "[issue-number]"
---

# Fix GitHub Issue #$ARGUMENTS

Follow the SDD workflow to fix this bug. Write a failing test first, then fix.

---

## Step 1: Understand the Issue

```bash
gh issue view $ARGUMENTS
```

Read carefully and identify:
- What behavior is reported as broken?
- What is the expected behavior?
- Are there reproduction steps?

---

## Step 2: Find the Root Cause

Search for relevant code:

1. Find the relevant model/controller/view
2. Read existing specs for this area
3. Reproduce the issue mentally — understand WHY it's broken

---

## Step 3: Write a Failing Test

Write a spec that **reproduces the bug**:

```bash
# Add to existing spec file, or create new one
bundle exec rspec <spec-file> --format documentation
```

The spec should FAIL with the current (buggy) code. If it passes, it's not testing the right thing.

For regression tests, add to the appropriate spec file:
- `spec/models/` — model behavior bugs
- `spec/requests/` — HTTP/controller bugs
- `spec/system/` — user-facing UI bugs

---

## Step 4: Fix the Bug

Implement the minimal fix:
- Fix ONLY what's needed to pass the test
- Don't refactor unrelated code
- Don't change behavior beyond what the test covers
- Follow existing patterns in the codebase

---

## Step 5: Verify

```bash
# Run the regression test
bundle exec rspec <spec-file> --format documentation

# Run related specs
bundle exec rspec spec/models/<model>_spec.rb

# Run full test suite (ensure no regressions)
bundle exec rspec

# Auto-fix linting
bin/rubocop -a

# Security scan
bin/brakeman --no-pager
```

---

## Step 6: Commit

Create a commit:
- Message format: `fix: <brief description of what was fixed>`
- Reference the issue in the PR description

Summarize what was changed and which tests were added.
