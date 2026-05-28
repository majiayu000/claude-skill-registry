---
name: test-nested-parent
description: Layer 2 (middle) - tests if child returns here or skips to grandparent
allowed-tools: Write, Skill, Read
context: fork
---

# Nested Return Test - Layer 2 (Parent)

You are LAYER 2 (the middle layer). This tests GitHub Issue #17351.

## Task (Execute in STRICT order)

### Step 1: Write start marker
Write to `earnings-analysis/test-outputs/nested-L2-started.txt`:
```
LAYER2_STARTED
Timestamp: [ISO timestamp]
About to call Layer 3 child
```

### Step 2: Call Layer 3
Invoke: `/test-nested-child`
Store the return value - it should be "SECRET_L3_999"

### Step 3: Write what you received (CRITICAL TEST)
**This proves Layer 3 returned to Layer 2, not to Layer 1 or Main.**

Write to `earnings-analysis/test-outputs/nested-L2-received.txt`:
```
LAYER2_RECEIVED_FROM_CHILD
Timestamp: [ISO timestamp]
Child (Layer 3) returned: [the exact value you received]
Expected: SECRET_L3_999
Match: [YES or NO]
```

### Step 4: Return to Layer 1
Return this EXACT text: `SECRET_L2_888`
