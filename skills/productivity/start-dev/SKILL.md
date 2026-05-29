---
name: start-dev
description: Start working on a task by updating its status to IN PROGRESS in MASTER_PLAN.md. Usage "/start-dev TASK-123" or "/start-dev 123". Updates all 3 locations in MASTER_PLAN.md. Triggers on "/start-dev", "start task", "begin task", "start working on".
---

# Start Dev - Task Status Updater

Start working on a task by updating its status to **IN PROGRESS** in `docs/MASTER_PLAN.md`.

## Usage

```
/start-dev TASK-123
/start-dev 123
/start-dev BUG-456
```

## Workflow

### Step 1: Parse Task ID

Extract the task ID from the argument:
- If just a number (e.g., `123`), assume `TASK-123`
- If prefixed (e.g., `TASK-123`, `BUG-456`, `FEATURE-789`), use as-is
- Normalize to uppercase

**Valid prefixes**: `TASK`, `BUG`, `FEATURE`, `ROAD`, `IDEA`, `ISSUE`

### Step 2: Verify Task Exists

Search MASTER_PLAN.md for the task ID:

```bash
grep -n "TASK-123" docs/MASTER_PLAN.md | head -20
```

**If not found**: Report error and stop.

**If found with strikethrough** (`~~TASK-123~~`): Task is already DONE. Ask user if they want to reopen it.

**If found**: Continue to update.

### Step 3: Update MASTER_PLAN.md

**CRITICAL**: Tasks appear in **3 locations** in MASTER_PLAN.md. Update ALL of them:

#### 3a. Summary Table (Roadmap section)

Find the task row and update the Status column:

**Before:**
```markdown
| **TASK-123** | **Feature Name** | **P1** | PLANNED | - |
```

**After:**
```markdown
| **TASK-123** | **Feature Name** | **P1** | IN PROGRESS | - |
```

Common status values to replace:
- `PLANNED` → `IN PROGRESS`
- `NEXT` → `IN PROGRESS`

#### 3b. Detailed Section (#### headers)

Find the detailed task section and update the header status:

**Before:**
```markdown
### TASK-123: Feature Name (PLANNED)
```
or
```markdown
### TASK-123: Feature Name (NEXT)
```

**After:**
```markdown
### TASK-123: Feature Name (IN PROGRESS)
```

Also update any Status line in the details:

**Before:**
```markdown
**Status**: PLANNED (2026-01-24)
```

**After:**
```markdown
**Status**: IN PROGRESS (2026-01-24)
```

#### 3c. Subtasks Lists (if referenced)

If the task appears as a subtask or dependency, no status change needed there.

### Step 4: Verification

Run grep to verify all occurrences updated:

```bash
grep "TASK-123" docs/MASTER_PLAN.md
```

Confirm:
- Roadmap table shows `IN PROGRESS`
- Detailed section header shows `(IN PROGRESS)`
- No `PLANNED` or `NEXT` status remains

### Step 5: Report

Output summary to user:

```
Started working on [TASK-ID]

Updated in MASTER_PLAN.md:
- Roadmap table: IN PROGRESS
- Detailed section: IN PROGRESS

Ready to begin implementation.
```

## Examples

### Example 1: Start a TASK

```
User: /start-dev 1017
```

Updates:
- `| **TASK-1017** | ... | PLANNED |` → `| **TASK-1017** | ... | IN PROGRESS |`
- `### TASK-1017: Feature (PLANNED)` → `### TASK-1017: Feature (IN PROGRESS)`

### Example 2: Start a BUG

```
User: /start-dev BUG-359
```

Updates all occurrences of BUG-359 to IN PROGRESS status.

### Example 3: Task Already Done

```
User: /start-dev TASK-100
```

If task shows `~~TASK-100~~` (strikethrough), ask:
> "TASK-100 is marked as DONE. Do you want to reopen it?"

## Status Mappings

| Find Pattern | Replace With |
|--------------|--------------|
| `PLANNED` | `IN PROGRESS` |
| `NEXT` | `IN PROGRESS` |
| `PAUSED` | `IN PROGRESS` |
| `REVIEW` | `IN PROGRESS` |

## Important Rules

- **Always verify task exists** before updating
- **Update ALL locations** in MASTER_PLAN.md (table + detailed section)
- **Preserve task ID format** (don't add/remove prefixes)
- **Don't modify strikethrough tasks** without user confirmation
- **Run verification grep** after updates
