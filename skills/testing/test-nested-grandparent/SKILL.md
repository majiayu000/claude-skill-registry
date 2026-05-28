---
name: test-nested-grandparent
description: Layer 1 (outermost forked) - tests if Layer 2 returns here or skips to Main
allowed-tools: Write, Skill, Read
context: fork
---

# Nested Return Test - Layer 1 (Grandparent of Layer 3)

You are LAYER 1. You call Layer 2, which calls Layer 3.
This tests GitHub Issue #17351 - whether nested forked skills return correctly.

## Task (Execute in STRICT order)

### Step 1: Write start marker
Write to `earnings-analysis/test-outputs/nested-L1-started.txt`:
```
LAYER1_STARTED
Timestamp: [ISO timestamp]
About to call Layer 2 (which will call Layer 3)
```

### Step 2: Call Layer 2
Invoke: `/test-nested-parent`
Store the return value - it should be "SECRET_L2_888"

### Step 3: Write what you received (CRITICAL TEST)
**This proves Layer 2 returned to Layer 1, not to Main.**

Write to `earnings-analysis/test-outputs/nested-L1-received.txt`:
```
LAYER1_RECEIVED_FROM_CHILD
Timestamp: [ISO timestamp]
Child (Layer 2) returned: [the exact value you received]
Expected: SECRET_L2_888
Match: [YES or NO]
```

### Step 4: Read all layer files and compile summary
Read:
- nested-L1-started.txt
- nested-L2-started.txt
- nested-L2-received.txt
- nested-L3-executed.txt

### Step 5: Write final verification
Write to `earnings-analysis/test-outputs/nested-final-verification.txt`:
```
=== NESTED FORKED SKILL RETURN TEST ===
=== GitHub Issue #17351 Verification ===
Timestamp: [ISO timestamp]
Claude Code Version: [if known]

LAYER EXECUTION:
- Layer 1 started: [YES/NO based on file existence]
- Layer 2 started: [YES/NO]
- Layer 3 executed: [YES/NO]
- Layer 2 received from Layer 3: [value or MISSING]
- Layer 1 received from Layer 2: [value or MISSING]

RETURN PATH VERIFICATION:
- Layer 3 → Layer 2: [CORRECT if L2 received SECRET_L3_999, else BROKEN]
- Layer 2 → Layer 1: [CORRECT if L1 received SECRET_L2_888, else BROKEN]

CONCLUSION:
[If all correct: "Nested forked skills return correctly to their parent, NOT grandparent. GH #17351 does NOT affect this setup."]
[If broken: "BUG CONFIRMED - returns skip to grandparent"]
```
