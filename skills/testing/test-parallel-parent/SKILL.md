---
name: test-parallel-parent
description: Test parallel skill execution - calls two children simultaneously
context: fork
allowed-tools:
  - Skill
  - Read
  - Write
---

# Parallel Execution Test

**Goal**: Test if two skills can be called in parallel.

## Task

1. Record start time
2. Call BOTH skills in a SINGLE message (parallel):
   - /test-parallel-child-a
   - /test-parallel-child-b
3. Record end time
4. Read both output files
5. Write results to `earnings-analysis/test-outputs/parallel-parent-result.txt`

Include:
- Start/end timestamps
- Whether both children executed
- Whether they ran in parallel (timestamps close) or sequential (timestamps far apart)
- Total elapsed time

**IMPORTANT**: Call both child skills in ONE message to test parallel execution.
