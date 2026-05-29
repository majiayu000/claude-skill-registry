---
name: batch-processor
description: "Apply operations across multiple files in parallel. Use when user says 'rename across', 'update all', 'add to every', or needs to apply same change to many files."
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep
---

# Batch Processor

Apply the same operation across multiple files in parallel using background agents.

## When To Use

**Trigger Phrases:**
- "Rename X to Y across the codebase"
- "Add error handling to all API endpoints"
- "Update imports in all test files"
- "Apply this change to every service"
- "Fix this pattern in all files"

**Auto-Trigger Signals:**
- Glob returns >10 files that need same change
- User describes repeating operation
- Pattern-based refactoring across codebase

## Inputs

- Operation to apply (rename, add, remove, update)
- Target pattern (file glob, grep match)
- Optional: test command to verify each batch

## Outputs

- Success/failure count
- List of modified files
- Any failures with details

---

## Execution Pattern

### Step 1: Identify Target Files

Use Explore agent to find all targets:

```
Task:
  subagent_type: Explore
  description: "Find batch targets"
  prompt: |
    Find all files matching: [pattern]
    Return: file paths only, one per line
    Max: 100 files
```

### Step 2: Create Batches

Group files into batches of 5 for parallel processing:

```
Files found: 30
Batches created:
- Batch 1: files 1-5
- Batch 2: files 6-10
- Batch 3: files 11-15
- Batch 4: files 16-20
- Batch 5: files 21-25
- Batch 6: files 26-30
```

**Why 5 per batch?**
- Enough for efficiency gains
- Small enough for reliable execution
- Easy to retry on failure

### Step 3: Spawn Parallel Agents

In a SINGLE message, spawn agents for each batch:

```
Task:
  subagent_type: general-purpose
  description: "Batch 1: files 1-5"
  prompt: |
    Apply operation: [operation description]

    Files:
    - path/to/file1.ts
    - path/to/file2.ts
    - path/to/file3.ts
    - path/to/file4.ts
    - path/to/file5.ts

    For each file:
    1. Read file
    2. Apply change: [specific change]
    3. Write file
    4. Run test: [test command] (if applicable)

    Return: JSON with {success: [], failed: []}
  run_in_background: true

Task:
  subagent_type: general-purpose
  description: "Batch 2: files 6-10"
  prompt: |
    [Same structure, different files]
  run_in_background: true

# ... spawn all batches in parallel
```

### Step 4: Poll and Aggregate

```
# Poll all batches
for batch_id in batch_ids:
    TaskOutput: { task_id: batch_id, block: true }

# Aggregate results
Total files: 30
Successful: 28
Failed: 2
  - path/to/file7.ts: Syntax error after change
  - path/to/file23.ts: Test failed
```

### Step 5: Handle Failures

For failed files, attempt one more time or report to user:

```
Failed files require attention:
1. path/to/file7.ts - Syntax error
   Suggested: Manual review needed

2. path/to/file23.ts - Test failed
   Suggested: Check edge case in test
```

---

## Common Operations

### Rename Variable/Function

```
Operation: Rename "oldName" to "newName"
Pattern: **/*.ts
Exclude: node_modules, dist

For each file:
1. Read content
2. Replace /\boldName\b/g with "newName"
3. Write file
4. Run: npm run typecheck
```

### Add Import

```
Operation: Add import { Logger } from '@/utils/logger'
Pattern: src/services/**/*.ts

For each file:
1. Read content
2. If not already imported, add import statement
3. Write file
```

### Update Pattern

```
Operation: Replace console.log with logger.info
Pattern: src/**/*.ts
Exclude: *.test.ts

For each file:
1. Read content
2. Replace console.log( with logger.info(
3. Add logger import if not present
4. Write file
5. Run: eslint --fix
```

---

## Parallel Efficiency

| Batch Size | Files | Agents | Time (est) |
|------------|-------|--------|------------|
| 5 | 30 | 6 | ~30 sec |
| 5 | 50 | 10 | ~30 sec |
| 5 | 100 | 20 | ~45 sec |

vs Sequential:
- 30 files × 10 sec/file = 5 minutes
- **Parallel: 30 seconds (10x faster)**

---

## Context Efficiency

Each batch agent:
- Runs in isolated context
- Only returns success/failure summary
- ~100 tokens per batch returned

Main agent context:
- Batch setup: ~500 tokens
- Results aggregation: ~200 tokens
- Total: ~700 tokens

vs Sequential (all in main context):
- 30 files × 500 tokens = 15,000 tokens
- **Savings: 95%**

---

## Safety Features

### Dry Run Mode

```
/batch-processor --dry-run "rename foo to bar" **/*.ts

Output:
Would modify 23 files:
- src/services/auth.ts (3 occurrences)
- src/services/user.ts (1 occurrence)
- ...
```

### Rollback on Failure

```
# Create git checkpoint before batch
git stash push -m "batch-processor checkpoint"

# Run batch

# If >20% failures, rollback
git stash pop
```

### Test After Each Batch

```
For each batch:
1. Apply changes
2. Run test command
3. If fails: revert batch, mark as failed
4. If passes: continue
```

---

## Integration

### With beads

```bash
# Track batch operation
bd create "Batch: rename foo to bar" -t batch --json
bd create "Batch 1: files 1-5" --deps parent:$BATCH_ID -t agent_task --json
bd create "Batch 2: files 6-10" --deps parent:$BATCH_ID -t agent_task --json
# ...
```

### With git-workflow

```bash
# After successful batch
git add -A
git commit -m "refactor: rename foo to bar across codebase

Batch processed 30 files in 6 parallel agents.
All tests passing.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Command Shortcuts

```bash
# Interactive batch
/batch-processor

# Direct batch with dry-run
/batch-processor --dry-run "add @ts-expect-error" src/**/*.test.ts

# Direct batch with execution
/batch-processor "rename getUserById to findUserById" src/**/*.ts

# Batch with custom test
/batch-processor --test "npm test" "update imports" src/**/*.ts
```

---

## Anti-Patterns

- Processing one file at a time (use batches)
- Running all in main context (use background agents)
- Not testing after changes (always verify)
- Batches too large (>10 files risk timeout)
- Not creating checkpoint (always git stash first)
- Ignoring failures (always review failed files)

---

## Keywords

batch, bulk, mass, multiple files, across codebase, rename all, update all, fix all, parallel, concurrent
