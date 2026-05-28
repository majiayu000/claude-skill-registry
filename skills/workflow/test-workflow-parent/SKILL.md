---
name: test-workflow-parent
description: Parent skill to test workflow continuation after child returns - CRITICAL BUG TEST
allowed-tools: Write, Read, Skill
context: fork
---

# Workflow Continuation Test (Parent)

**CRITICAL TEST**: This tests GitHub Issue #17351 - whether nested skills return to parent or grandparent.

**IMPORTANT**: Execute steps IN ORDER. Each step MUST complete before the next.

## Steps (Execute Sequentially)

### Step 1: Write BEFORE marker
Write to `earnings-analysis/test-outputs/workflow-step1.txt`:
```
STEP1_BEFORE_CHILD
Timestamp: [current ISO timestamp]
Parent skill started, about to call child
```

### Step 2: Call the child skill
Invoke: `/test-workflow-child`
Store the return value.

### Step 3: Write AFTER marker (CRITICAL - proves continuation)
**THIS IS THE KEY TEST** - If bug #17351 exists, this step will NEVER execute.

Write to `earnings-analysis/test-outputs/workflow-step3.txt`:
```
STEP3_AFTER_CHILD
Timestamp: [current ISO timestamp]
Child returned with: [the return value from step 2]
Parent workflow CONTINUED after child completed!
```

### Step 4: Read and verify child's file
Read: `earnings-analysis/test-outputs/workflow-child.txt`
Verify it contains "CHILD_EXECUTED"

### Step 5: Write FINAL summary
Write to `earnings-analysis/test-outputs/workflow-step5.txt`:
```
STEP5_FINAL_COMPLETE
Timestamp: [current ISO timestamp]
Child file contents: [contents from step 4]
Child return value: [value from step 2]

=== WORKFLOW CONTINUATION TEST RESULT ===
If you see this file, the workflow CONTINUED correctly!
All 5 steps executed in sequence.
GitHub Issue #17351 does NOT affect this execution.
```

## Expected Files After Completion

If working correctly, ALL these files should exist:
1. workflow-step1.txt (before child)
2. workflow-child.txt (written by child)
3. workflow-step3.txt (CRITICAL - after child, proves continuation)
4. workflow-step5.txt (final summary)

If bug exists, only files 1 and 2 will exist.
