---
name: test-trade-earnings-pattern
description: Test task dependencies for tradeEarnings workflow pattern
context: fork
allowed-tools:
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Write
---

# Test: tradeEarnings Workflow Pattern with Task Dependencies

**Objective**: Create tasks matching the tradeEarnings workflow and verify dependency structure.

## Workflow Pattern

```
Wave 1 (Parallel):
  ├── news-impact (no deps)
  └── guidance-inventory (no deps)
          │
          ▼
Wave 2:
  └── prediction (blocked by news-impact AND guidance-inventory)
          │
          ▼
Wave 3:
  └── attribution (blocked by prediction)
```

## Instructions

### Step 1: Create Tasks

Create these 4 tasks with TaskCreate:

1. Subject: "AAPL-Q1: News Impact Analysis"
   Description: "Analyze news sentiment and events around AAPL Q1 earnings"
   ActiveForm: "Analyzing news impact"

2. Subject: "AAPL-Q1: Guidance Inventory Update"
   Description: "Update cumulative guidance inventory with Q1 data"
   ActiveForm: "Building guidance inventory"

3. Subject: "AAPL-Q1: Earnings Prediction"
   Description: "Predict stock direction at T=0 using PIT data"
   ActiveForm: "Making prediction"

4. Subject: "AAPL-Q1: Earnings Attribution"
   Description: "Analyze why stock moved after earnings (T+1)"
   ActiveForm: "Attributing movement"

### Step 2: Set Up Dependencies

Using TaskUpdate with addBlockedBy:
- Task 3 (prediction) blocked by tasks 1 AND 2
- Task 4 (attribution) blocked by task 3

### Step 3: Verify Structure

Run TaskList and TaskGet for each task to verify:
- Tasks 1 and 2 have NO blockers (can run parallel)
- Task 3 blocked by 1 and 2
- Task 4 blocked by 3

### Step 4: Simulate Execution

1. Mark tasks 1 and 2 as in_progress (simulating parallel execution)
2. Mark tasks 1 and 2 as completed
3. Verify task 3 is now unblocked
4. Mark task 3 as in_progress, then completed
5. Verify task 4 is now unblocked
6. Mark task 4 as completed

## Output

Write to: `earnings-analysis/test-outputs/trade-earnings-pattern-result.txt`

Format:
```
TEST: trade-earnings-pattern
TIMESTAMP: {ISO timestamp}

TASK STRUCTURE CREATED:
[List all 4 tasks with their IDs]

DEPENDENCY VERIFICATION:
- Task 1 (news-impact): [no blockers] ✓
- Task 2 (guidance): [no blockers] ✓
- Task 3 (prediction): [blocked by #1, #2] ✓
- Task 4 (attribution): [blocked by #3] ✓

EXECUTION SIMULATION:
Wave 1 Start: Tasks 1,2 marked in_progress
Wave 1 Complete: Tasks 1,2 marked completed
Task 3 Status: [should show unblocked]
Wave 2 Start: Task 3 marked in_progress
Wave 2 Complete: Task 3 marked completed
Task 4 Status: [should show unblocked]
Wave 3 Complete: Task 4 marked completed

FINAL TASK LIST:
{TaskList output showing all 4 completed}

CONCLUSION: tradeEarnings pattern {WORKS|FAILED}
```

Return summary of findings.
