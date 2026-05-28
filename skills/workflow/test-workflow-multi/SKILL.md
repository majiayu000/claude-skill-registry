---
name: test-workflow-multi
description: Tests workflow continuation with MULTIPLE sequential child skill calls
allowed-tools: Write, Read, Skill
context: fork
---

# Multi-Child Workflow Continuation Test

**RIGOROUS TEST**: Parent calls multiple children in sequence, with work between each.

## Steps (Execute ALL in strict sequence)

### Step 1: Initial marker
Write to `earnings-analysis/test-outputs/workflow-multi-step1.txt`:
```
MULTI_STEP1
Timestamp: [ISO timestamp]
Starting multi-child workflow test
```

### Step 2: Call FIRST child
Invoke: `/test-workflow-child`
Store return value as CHILD1_RESULT.

### Step 3: Post-first-child marker (CRITICAL TEST 1)
Write to `earnings-analysis/test-outputs/workflow-multi-step3.txt`:
```
MULTI_STEP3_AFTER_CHILD1
Timestamp: [ISO timestamp]
First child returned: [CHILD1_RESULT]
Continuing to second child...
```

### Step 4: Call SECOND child
Invoke: `/test-workflow-child` again
Store return value as CHILD2_RESULT.

### Step 5: Post-second-child marker (CRITICAL TEST 2)
Write to `earnings-analysis/test-outputs/workflow-multi-step5.txt`:
```
MULTI_STEP5_AFTER_CHILD2
Timestamp: [ISO timestamp]
Second child returned: [CHILD2_RESULT]
Both children completed, workflow still running!
```

### Step 6: Read child's file and do computation
Read: `earnings-analysis/test-outputs/workflow-child.txt`
Count characters in the file.

### Step 7: Final summary
Write to `earnings-analysis/test-outputs/workflow-multi-final.txt`:
```
MULTI_WORKFLOW_COMPLETE
Timestamp: [ISO timestamp]

=== MULTI-CHILD WORKFLOW TEST RESULTS ===

Step 1 (before any child): EXECUTED
Step 2 (call child 1): EXECUTED
Step 3 (after child 1): EXECUTED - proves continuation after 1st child
Step 4 (call child 2): EXECUTED
Step 5 (after child 2): EXECUTED - proves continuation after 2nd child
Step 6 (read & compute): EXECUTED
Step 7 (this file): EXECUTED

Child 1 return value: [CHILD1_RESULT]
Child 2 return value: [CHILD2_RESULT]
Child file character count: [count]

ALL 7 STEPS COMPLETED.
GitHub Issue #17351 does NOT affect multi-child sequential workflows.
```

## Expected Files If Working
1. workflow-multi-step1.txt
2. workflow-child.txt (from child)
3. workflow-multi-step3.txt (CRITICAL - after 1st child)
4. workflow-multi-step5.txt (CRITICAL - after 2nd child)
5. workflow-multi-final.txt

If bug exists at any point, subsequent files won't be created.
