---
name: test-task-basic
description: Test if TaskCreate/List/Get/Update tools are available in forked skills
context: fork
allowed-tools:
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Write
  - Read
---

# Test: Task Management Tools in Forked Skill

**Objective**: Determine if TaskCreate, TaskList, TaskGet, TaskUpdate tools are available in a forked skill context.

## Instructions

Run these tests IN ORDER and report results to the output file:

### Test 1: Check Available Tools
List what tools you have access to. Specifically check for:
- TaskCreate
- TaskList
- TaskGet
- TaskUpdate

### Test 2: Try TaskCreate
IF TaskCreate is available, create a task:
```
Subject: "Test task from forked skill"
Description: "Created by test-task-basic skill to verify TaskCreate works in fork context"
ActiveForm: "Testing task creation"
```

Record the task ID if successful, or the error message if it fails.

### Test 3: Try TaskList
IF TaskList is available, list all tasks and record:
- How many tasks exist
- Whether the task from Test 2 appears

### Test 4: Try TaskGet
IF TaskGet is available AND Test 2 created a task, get that task by ID and record:
- Whether it returns the task details
- What fields are visible

### Test 5: Try TaskUpdate
IF TaskUpdate is available AND Test 2 created a task, update it:
- Set status to "in_progress"
- Then set status to "completed"
- Record success or failure for each

## Output

Write results to: `earnings-analysis/test-outputs/task-basic-result.txt`

Format:
```
TEST: task-basic (forked skill)
TIMESTAMP: {ISO timestamp}
CLI_VERSION: {if detectable}

TOOL AVAILABILITY:
- TaskCreate: {AVAILABLE|NOT AVAILABLE|ERROR: message}
- TaskList: {AVAILABLE|NOT AVAILABLE|ERROR: message}
- TaskGet: {AVAILABLE|NOT AVAILABLE|ERROR: message}
- TaskUpdate: {AVAILABLE|NOT AVAILABLE|ERROR: message}

TEST RESULTS:
1. TaskCreate: {PASS|FAIL|SKIPPED} - {details}
   Task ID: {id or N/A}
2. TaskList: {PASS|FAIL|SKIPPED} - {details}
   Task count: {n}
3. TaskGet: {PASS|FAIL|SKIPPED} - {details}
4. TaskUpdate (in_progress): {PASS|FAIL|SKIPPED} - {details}
5. TaskUpdate (completed): {PASS|FAIL|SKIPPED} - {details}

CONCLUSION: {Task tools ARE/ARE NOT available in forked skills}
```

After writing the file, return a brief summary of findings.
