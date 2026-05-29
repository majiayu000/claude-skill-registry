---
name: task-continue
description: Resume spec implementation from checkpoint. Use when continuing task-dispatch after context limit or session break.
user-invocable: continue
---

# Task Continue Skill

Resume spec implementation from the last checkpoint. Picks up where `task-dispatch` left off.

---

## When to Use

- After hitting context limit during `/implement`
- Starting a new session to continue a spec
- Recovering from interruption mid-implementation

---

## Workflow

### Step 1: Find Checkpoint

1. Parse spec name from argument (e.g., `/continue auth-system`)
2. If no argument: find most recent checkpoint in `./specs/active/*/checkpoint.yaml`
3. If no checkpoint found: suggest `/implement` instead

```bash
# Find most recent checkpoint
ls -t ./specs/active/*/checkpoint.yaml | head -1
```

### Step 2: Load Context

Read these files (in parallel):

```
./specs/active/<spec>/checkpoint.yaml  # Session state
./specs/active/<spec>/spec.md          # Requirements
./specs/active/<spec>/tasks.yaml       # Task definitions
./specs/active/<spec>/dependencies.yaml # Batch structure
./specs/active/<spec>/validation.yaml  # Review config
```

### Step 3: Verify Branch State

```bash
# Checkout spec branch
git checkout <checkpoint.branch>

# Verify at expected commit
git log -1 --format="%H" | head -c 8
# Should match checkpoint.last_commit

# If mismatch, warn user and ask to proceed or abort
```

### Step 4: Report Progress

Present concise status:

```
## Resuming: <spec_name>

**Progress:** Batch <last_batch>/<total_batches> complete
**Completed:** <N> tasks
**Remaining:** <M> tasks

**Next batch:** #<next_batch.number>
- <task_id>: <task_name>
- <task_id>: <task_name>
[parallel: yes/no]

**Deferred issues:** <count>
[list if any]

Continuing with three-phase pipeline...
```

### Step 5: Resume Three-Phase Pipeline

Execute the next batch using the same pipeline as `task-dispatch`:

```
Phase A: TESTERS
├── Dispatch task-tester(s) for next_batch.tasks
└── Wait for completion

Phase B: IMPLEMENTERS
├── Dispatch task-implementer(s) with tester reports
└── Wait for completion

Phase C: REVIEWERS
├── Dispatch 1 Claude + N OpenCode reviewers (from review_config)
└── Wait for completion + synthesize
```

**CRITICAL:** Follow all `task-dispatch` rules:
- Always use `model: opus` for subagents
- Dispatch parallel subagents in single message
- Never skip reviewer phase
- Fix Critical/High issues before proceeding

### Step 6: Update Checkpoint

After batch completes:

1. Update tasks.yaml statuses
2. Write new checkpoint.yaml
3. Commit with batch info
4. Continue to next batch or report completion

---

## Quick Resume Template

When resuming, use this condensed context for subagents:

**For Tester:**
```
Task: <task_id> - <task_name>
From: <spec_name> (batch <N>)
Requirements: [from tasks.yaml]
Test hints: [from tasks.yaml]

Invoke `code-test` skill. Write failing tests (RED).
Report tester_report YAML.
```

**For Implementer:**
```
Task: <task_id> - <task_name>
From: <spec_name> (batch <N>)
Tester report: [paste tester_report]

Invoke `code-implement` skill. Make tests pass (GREEN).
Report implementer_report YAML.
```

**For Reviewer:**
```
Batch <N> review for <spec_name>
Tasks: <task_ids>
Implementer reports: [paste all]
Spec requirements: [from tasks.yaml]

Invoke `code-review` skill. Evaluate gates.
Report reviewer_report YAML.
```

---

## Handling Edge Cases

**Checkpoint not found:**
```
No checkpoint found for <spec>.
Run /implement <spec> to start fresh.
```

**Branch mismatch:**
```
Warning: Current branch differs from checkpoint.
Expected: feat/<spec> at <sha>
Actual: <current_branch> at <current_sha>

Options:
1. Checkout checkpoint branch and continue
2. Abort and investigate
```

**Checkpoint stale (tasks.yaml modified):**
```
Warning: tasks.yaml modified since checkpoint.
Checkpoint: <timestamp>
tasks.yaml: <modified_time>

Regenerating next batch from current state...
```

**All tasks complete:**
```
All tasks complete for <spec>.
Run final review? [Y/n]
```

---

## Integration

**Command:** `/continue [spec-name]`

**Related skills:**
- `task-dispatch` - Initial execution (writes checkpoints)
- `spec-update` - Sync task status from git history
- `spec-archive` - Archive completed spec

---

## Example Session

```
User: /continue

Claude: Found checkpoint for auth-system

## Resuming: auth-system

**Progress:** Batch 2/4 complete
**Completed:** 4 tasks (T001-T004)
**Remaining:** 3 tasks

**Next batch:** #3
- T005: Add session management
- T006: Add token refresh
[parallel: yes]

**Deferred issues:** 1
- [M1] Variable naming in auth.py:45 (batch 2)

Continuing with three-phase pipeline...

[Dispatches 2 testers in parallel]
[Dispatches 2 implementers in parallel]
[Dispatches 1 Claude + 2 OpenCode reviewers in parallel]
[Synthesizes review, no critical issues]
[Writes checkpoint, commits batch 3]

Batch 3 complete. 1 batch remaining.
Continue in this session or /continue later.
```
