---
name: bug-hunt
description: 'Investigate suspected bugs with git archaeology and root cause analysis. Triggers: "bug", "broken", "doesn''t work", "failing", "investigate bug", "debug", "find the bug", "troubleshoot".'
metadata:
  tier: execution
  dependencies:
    - beads  # optional - for issue tracking
---

# Bug Hunt Skill

> **Quick Ref:** 4-phase investigation (Root Cause → Pattern → Hypothesis → Fix). Output: `.agents/research/YYYY-MM-DD-bug-*.md`

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Systematic investigation to find root cause and design a complete fix.

**Requires:**
- session-start.sh has executed (creates `.agents/` directories for output)
- bd CLI (beads) for issue tracking if creating follow-up issues

## The 4-Phase Structure

| Phase | Focus | Output |
|-------|-------|--------|
| **1. Root Cause** | Find the actual bug location | file:line, commit |
| **2. Pattern** | Compare against working examples | Differences identified |
| **3. Hypothesis** | Form and test single hypothesis | Pass/fail for each |
| **4. Implementation** | Fix at root, not symptoms | Verified fix |

**For failure category taxonomy and the 3-failure rule, read `skills/bug-hunt/references/failure-categories.md`.**

## Execution Steps

Given `/bug-hunt <symptom>`:

---

## Phase 1: Root Cause Investigation

### Step 1.1: Confirm the Bug

First, reproduce the issue:
- What's the expected behavior?
- What's the actual behavior?
- Can you reproduce it consistently?

**Read error messages carefully.** Do not skip or skim them.

If the bug can't be reproduced, gather more information before proceeding.

### Step 1.2: Locate the Symptom

Find where the bug manifests:
```bash
# Search for error messages
grep -r "<error-text>" . --include="*.py" --include="*.ts" --include="*.go" 2>/dev/null | head -10

# Search for function/variable names
grep -r "<relevant-name>" . --include="*.py" --include="*.ts" --include="*.go" 2>/dev/null | head -10
```

### Step 1.3: Git Archaeology

Find when/how the bug was introduced:

```bash
# When was the file last changed?
git log --oneline -10 -- <file>

# What changed recently?
git diff HEAD~10 -- <file>

# Who changed it and why?
git blame <file> | grep -A2 -B2 "<suspicious-line>"

# Search for related commits
git log --oneline --grep="<keyword>" | head -10
```

### Step 1.4: Trace the Execution Path

**USE THE TASK TOOL** (subagent_type: "Explore") to trace the execution path:
- Find the entry point where the bug manifests
- Trace backward to find where bad data/state originates
- Identify all functions in the path and recent changes to them
- Return: execution path, likely root cause location, responsible changes

### Step 1.5: Identify Root Cause

Based on tracing, identify:
- **What** is wrong (the actual bug)
- **Where** it is (file:line)
- **When** it was introduced (commit)
- **Why** it happens (the logic error)

---

## Phase 2: Pattern Analysis

### Step 2.1: Find Working Examples

Search the codebase for similar functionality that WORKS:
```bash
# Find similar patterns
grep -r "<working-pattern>" . --include="*.py" --include="*.ts" --include="*.go" 2>/dev/null | head -10
```

### Step 2.2: Compare Against Reference

Identify ALL differences between:
- The broken code
- The working reference

Document each difference.

---

## Phase 3: Hypothesis and Testing

### Step 3.1: Form Single Hypothesis

State your hypothesis clearly:
> "I think X is wrong because Y"

**One hypothesis at a time.** Do not combine multiple guesses.

### Step 3.2: Test with Smallest Change

Make the SMALLEST possible change to test the hypothesis:
- If it works → proceed to Phase 4
- If it fails → record failure, form NEW hypothesis

### Step 3.3: Check Failure Counter

Check failure count per `skills/bug-hunt/references/failure-categories.md`. After 3 countable failures, escalate to architecture review.

---

## Phase 4: Implementation

### Step 4.1: Design the Fix

Before writing code, design the fix:
- What needs to change?
- What are the edge cases?
- Will this fix break anything else?
- Are there tests to update?

### Step 4.2: Create Failing Test (if possible)

Write a test that demonstrates the bug BEFORE fixing it.

### Step 4.3: Implement Single Fix

Fix at the ROOT CAUSE, not at symptoms.

### Step 4.4: Verify Fix

Run the failing test - it should now pass.

---

## Step 5: Write Bug Report

**For bug report template, read `skills/bug-hunt/references/bug-report-template.md`.**

### Step 6: Report to User

Tell the user:
1. Root cause identified (or not yet)
2. Location of the bug (file:line)
3. Proposed fix
4. Location of bug report
5. Failure count and types encountered
6. Next step: implement fix or gather more info

## Key Rules

- **Reproduce first** - confirm the bug exists
- **Use git archaeology** - understand history
- **Trace systematically** - follow the execution path
- **Identify root cause** - not just symptoms
- **Design before fixing** - think through the solution
- **Document findings** - write the bug report

## Quick Checks

Common bug patterns to check:
- Off-by-one errors
- Null/undefined handling
- Race conditions
- Type mismatches
- Missing error handling
- State not reset
- Cache issues

## Examples

### Investigating a Test Failure

**User says:** `/bug-hunt "tests failing on CI but pass locally"`

**What happens:**
1. Agent confirms bug by checking CI logs vs local test output
2. Agent uses git archaeology to find recent changes to test files
3. Agent traces execution path to identify environment-specific differences
4. Agent forms hypothesis about missing environment variable
5. Agent creates failing test locally by unsetting the variable
6. Agent implements fix by adding default value
7. Bug report written to `.agents/research/2026-02-13-bug-test-failure.md`

**Result:** Root cause identified as missing ENV variable in CI configuration. Fix applied and verified.

### Tracking Down a Regression

**User says:** `/bug-hunt "feature X broke after yesterday's deployment"`

**What happens:**
1. Agent reproduces issue in current state
2. Agent uses `git log --since="2 days ago"` to find recent commits
3. Agent uses `git bisect` to identify exact breaking commit
4. Agent compares broken code against working examples in codebase
5. Agent forms hypothesis about introduced type mismatch
6. Agent implements minimal fix and verifies with existing tests
7. Bug report documents commit sha, root cause, and fix

**Result:** Regression traced to commit abc1234, type conversion error fixed at root cause in validation logic.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Can't reproduce bug | Insufficient environment context or intermittent issue | Ask user for specific steps, environment variables, input data. Check for race conditions or timing issues. |
| Git archaeology returns too many commits | Broad search or high-churn file | Narrow timeframe with `--since` flag, focus on specific function with `git blame`, search commit messages for related keywords. |
| Hit 3-failure limit during hypothesis testing | Multiple incorrect hypotheses or complex root cause | Escalate to architecture review. Read `failure-categories.md` to determine if failures are countable. Consider asking for domain expert input. |
| Bug report missing key information | Incomplete investigation or skipped steps | Verify all 4 phases completed. Ensure root cause identified with file:line. Check git blame ran for responsible commit. |
