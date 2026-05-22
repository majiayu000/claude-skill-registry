---
name: review
description: >
  Code review with confidence-based filtering.
  Use to review code for bugs, security issues, and quality problems.
  Only reports issues with high confidence to reduce noise.
---

# Code Review with Confidence Filtering

## Overview

Review code thoroughly but only report issues you're confident about.
Filter out noise - stylistic preferences and uncertain concerns don't belong in reviews.
Focus on bugs, security issues, and clear violations.

**Core principle:** Only report issues with >= 80% confidence.

**Announce at start:** "I'm using the review skill to review this code."

## When to Request Review

**Mandatory:**
- After completing a feature
- Before merging to main
- After fixing complex bugs

**Optional but valuable:**
- When stuck (fresh perspective helps)
- Before major refactoring
- After implementing unfamiliar patterns

## The Review Process

### Step 1: Gather Context

**Get the diff:**
```bash
BASE_SHA=$(git merge-base HEAD main)  # or specific commit
HEAD_SHA=$(git rev-parse HEAD)
git diff $BASE_SHA..$HEAD_SHA
```

**Check existing patterns:**
```bash
kodo query "code style"      # Project conventions
kodo query "error handling"  # Error patterns used
```

### Step 2: Review for Issues

**Priority categories:**

| Priority | Confidence | Action | Examples |
|----------|------------|--------|----------|
| Critical | >= 90% | Must fix before merge | Security holes, data loss, crashes |
| Important | >= 80% | Should fix | Logic bugs, missing error handling |
| Minor | >= 80% | Nice to fix | Performance, readability |

**DO report (>= 80% confidence):**
- Clear bugs with specific line numbers
- Obvious security issues
- Missing error handling that will cause failures
- Logic errors you can prove with example input

**DO NOT report (< 80% confidence):**
- Stylistic preferences ("I would have done X")
- Uncertain concerns ("This might cause issues")
- Opinions without evidence
- Things that "feel wrong" but you can't explain why

### Step 3: Document Findings

**Report format:**

```markdown
## Code Review: [Feature/PR Name]

**Commits reviewed:** `BASE_SHA..HEAD_SHA`
**Files changed:** X files, +Y/-Z lines

### Strengths
- [What's done well - acknowledge good work]

### Issues

#### Critical: [Title] (Confidence: XX%)
**File:** `path/to/file.rs:42`
**Problem:** [Specific description]
**Evidence:** [Why you're confident this is wrong]
**Fix:**
```rust
// Suggested fix
```

#### Important: [Title] (Confidence: XX%)
...

### Assessment
[ ] APPROVE - Ready to merge
[ ] REQUEST CHANGES - Fix critical/important issues first
```

### Step 4: Handle Feedback

**If reviewer feedback is disputed:**
- Push back with technical reasoning
- Show code or tests that prove it works
- Ask for clarification on vague feedback

**If you're the reviewer and author disagrees:**
- Listen to their reasoning
- Verify your concern is valid (>= 80% confidence)
- Accept that you might be wrong

## Integration with Kodo

**Capture review insights:**
```bash
kodo reflect --signal "Found common bug pattern: missing null check in X"
kodo reflect --signal "Project uses Y pattern for error handling"
```

**Check if similar issues were caught before:**
```bash
kodo query "review bugs"     # Past review findings
kodo query "common mistakes" # Known pitfalls
```

## Confidence Calibration

**90%+ confidence means:**
- You can explain exactly why it's wrong
- You can show an input that triggers the bug
- The issue violates documented requirements

**80%+ confidence means:**
- You're fairly certain but can't prove it
- The code contradicts established patterns
- The behavior is clearly unintended

**< 80% means:**
- Don't report it
- Or preface with "Question:" not "Issue:"

## Key Principles

- **High confidence only** - Filter noise, report signal
- **Be specific** - Line numbers, exact problems, concrete fixes
- **Acknowledge strengths** - Reviews aren't just criticism
- **Push back respectfully** - If reviewer is wrong, say so with evidence
- **Learn from reviews** - Capture patterns with `kodo reflect`

## Red Flags

**You're doing it wrong if:**
- Reporting "I would have done it differently"
- No line numbers or specific locations
- Confidence below 80% on reported issues
- Only criticism, no acknowledgment of strengths
- Accepting invalid feedback without pushback
- Not capturing insights for future sessions
