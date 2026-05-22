---
name: bug-hunt
description: 'Investigate suspected bugs with git archaeology and root cause analysis. Triggers: "bug", "broken", "doesn''t work", "failing", "investigate bug".'
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

## Failure Tracking

**Track failures by TYPE - not all failures are equal:**

| Failure Type | Counts Toward Limit? | Action |
|--------------|----------------------|--------|
| `root_cause_not_found` | YES | Re-investigate from Phase 1 |
| `fix_failed_tests` | YES | New hypothesis in Phase 3 |
| `design_rejected` | YES | Rethink approach |
| `execution_timeout` | NO (reset counter) | Retry same approach |
| `external_dependency` | NO (escalate) | Report blocker |

**The 3-Failure Rule:**
- Count only `root_cause_not_found`, `fix_failed_tests`, `design_rejected`
- After 3 such failures: **STOP and question architecture**
- Output: "3+ fix attempts failed. Escalating to architecture review."
- Do NOT count timeouts or external blockers toward limit

**Track in issue notes:**
```bash
bd update <issue-id> --append-notes "FAILURE: <type> at $(date -Iseconds) - <reason>" 2>/dev/null
```

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

**USE THE TASK TOOL** to explore the code:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Trace bug execution path"
  prompt: |
    Trace the execution path for: <symptom>

    1. Find the entry point where the bug manifests
    2. Trace backward to find where bad data/state originates
    3. Identify all functions in the path
    4. Look for recent changes to these functions

    Return:
    - Execution path (function call chain)
    - Likely location of root cause
    - Recent changes that might be responsible
```

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

```bash
# Count failures (excluding timeouts and external blockers)
failures=$(bd show <issue-id> --json 2>/dev/null | jq '[.notes[]? | select(startswith("FAILURE:")) | select(contains("root_cause") or contains("fix_failed") or contains("design_rejected"))] | length')

if [[ "$failures" -ge 3 ]]; then
    echo "3+ fix attempts failed. Escalating to architecture review."
    bd update <issue-id> --append-notes "ESCALATION: Architecture review needed after 3 failures" 2>/dev/null
    exit 1
fi
```

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

**Write to:** `.agents/research/YYYY-MM-DD-bug-<slug>.md`

```markdown
# Bug Report: <Short Description>

**Date:** YYYY-MM-DD
**Severity:** <critical|high|medium|low>
**Status:** <investigating|root-cause-found|fix-designed>

## Symptom
<What the user sees>

## Expected Behavior
<What should happen>

## Reproduction Steps
1. <step 1>
2. <step 2>
3. <observe bug>

## Root Cause Analysis

### Location
- **File:** <path>
- **Line:** <line number>
- **Function:** <function name>

### Cause
<Explanation of what's wrong>

### When Introduced
- **Commit:** <hash>
- **Date:** <date>
- **Author:** <author>

## Proposed Fix

### Changes Required
1. <change 1>
2. <change 2>

### Risks
- <potential risk>

### Tests Needed
- <test to add/update>

## Related
- <related issues or PRs>
```

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
