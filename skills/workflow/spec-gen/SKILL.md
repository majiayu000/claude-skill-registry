---
activation_code: SPEC_GEN_V1
phase: 6
prerequisites:
  - tasks.json with coupling analysis
outputs:
  - .openspec/proposals/*.md
  - .signals/phase2-complete.json
description: |
  Generates OpenSpec proposals from TaskMaster tasks based on coupling analysis.
  Activates via codeword [ACTIVATE:SPEC_GEN_V1] injected by hooks when
  moving to Phase 2 specification generation.
  
  Activation trigger: [ACTIVATE:SPEC_GEN_V1]
---

# Spec Generator Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:SPEC_GEN_V1]
```

This occurs when:
- Phase 5 is complete (task decomposition done)
- User requests OpenSpec proposal generation
- Moving to Phase 6 of development

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in dedicated worktrees per batch `phase-2-task-N`:

```bash
# For each batch:
./lib/worktree-manager.sh create 2 <batch_number>
cd ./worktrees/phase-2-task-<batch_number>

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Spec generation with batch isolation
```

### Batch-Worktree Strategy
1. **One worktree per batch**: Each batch (5-10 tasks) gets isolated workspace
2. **Sequential batch processing**: Complete batch N before starting batch N+1
3. **Atomic batch commits**: Each batch merged separately to prevent conflicts
4. **Cross-batch isolation**: No dependencies between batch worktrees


## What This Skill Does

Automates Phase 6: OpenSpec proposal creation from TaskMaster subtasks in isolated worktrees

- **Batched processing** (5-10 master tasks per batch) in separate worktrees
- **1 proposal per subtask** (simple 1:1 mapping, no conditional logic)
- **OpenSpec proposal creation** (with TDD) per batch worktree
- **Integration map updates** merged sequentially
- **Completion signal** → triggers Phase 6.1
- **NEW**: Worktree isolation prevents cross-batch contamination
- **NEW**: Atomic batch processing with merge validation
- **SIMPLIFIED**: Always creates 1 proposal per subtask for clarity

## Execution Flow

```
Stage 1: Load TaskMaster Results (hierarchical format)
Stage 2: Determine Batching (by master tasks)
Stage 3: Process Batches
         - Extract all subtasks from master tasks
         - Create 1 proposal per subtask
         - Update map
Stage 4: Validate Proposals
Stage 5: Generate Summary
Stage 6: Create Signal → Phase 6.1
```

## Stage 1: Load TaskMaster Results

### Read TaskMaster Hierarchical Format

Load `.taskmaster/tasks/tasks.json`:
```json
{
  "master": {
    "tasks": [
      {
        "id": 1,
        "name": "User Authentication",
        "subtasks": [
          {"id": 1, "title": "Create user model", "testStrategy": "..."},
          {"id": 2, "title": "Add authentication", "testStrategy": "..."},
          {"id": 3, "title": "Add profile fields", "testStrategy": "..."}
        ]
      }
    ]
  }
}
```

**Extract:**
- Master task count (expect 8-12)
- Subtasks per master task (expect 3-8 each)
- Total subtasks (expect 30-60)
- Dependencies from TaskMaster structure

## Stage 2: Determine Batching

**Batch by master tasks (5-10 per batch):**
- Batch 1: Process master tasks 1-8
- Batch 2: Process master tasks 9-12 (if needed)

**Within each batch:**
- Process all subtasks from included master tasks
- Create 1 proposal per subtask (simple 1:1 mapping)

## Stage 3: Create OpenSpec Proposals

**For each subtask in each master task:**

1. **Create proposal file:**
   - Path: `openspec/changes/[change-id]/proposal.md`
   - Name pattern: `[master-task-name]-subtask-[id]`
   - Example: `user-authentication-subtask-1`

2. **Proposal content from subtask:**
   - Title: From subtask.title
   - Test Strategy: From subtask.testStrategy
   - Acceptance Criteria: From subtask.acceptanceCriteria
   - Dependencies: From TaskMaster dependencies

3. **Update TASKMASTER_OPENSPEC_MAP.md:**
   ```markdown
   ## Master Task 1: User Authentication
   - Subtask 1.1 → Proposal: user-authentication-subtask-1
   - Subtask 1.2 → Proposal: user-authentication-subtask-2
   - Subtask 1.3 → Proposal: user-authentication-subtask-3
   ```

**Result:** Total proposals = Total subtasks (30-60 proposals)

## Sequential Batch Execution (Context-Safe)

To prevent context exhaustion, process proposals in **sequential batches of 2 master tasks**.

### Why Sequential Batches?

Parallel subagents can exhaust context when:
- Each agent generates substantial proposal content
- Multiple agents return results simultaneously
- Combined context exceeds available window

**Sequential batches trade speed for reliability.**

### Step 1: Group Master Tasks into Batches of 2

```
Batch 1: Master tasks 1-2 → Wait for completion
Batch 2: Master tasks 3-4 → Wait for completion
Batch 3: Master tasks 5-6 → Wait for completion
Batch 4: Master tasks 7-8 → Wait for completion
Batch 5: Master tasks 9-10 → Wait for completion
Batch 6: Master tasks 11-12 → Wait for completion (if present)
```

### Step 2: Process Each Batch Sequentially

**For each batch (2 master tasks):**

1. **Launch 2 parallel subagents** (one per master task):
   ```
   Subagent A: Create proposals for master task N
     - Process all subtasks under task N
     - Create 1 proposal per subtask
     - Return summary when done

   Subagent B: Create proposals for master task N+1
     - Process all subtasks under task N+1
     - Create 1 proposal per subtask
     - Return summary when done
   ```

2. **Wait for BOTH to complete** before proceeding

3. **Update TASKMASTER_OPENSPEC_MAP.md** after batch completes

4. **Proceed to next batch**

### Step 3: Validate After All Batches

```bash
# Validate proposal count matches subtask count
proposal_count=$(ls -1 openspec/changes/*/proposal.md 2>/dev/null | wc -l)
subtask_count=$(jq '[.tasks[].subtasks | length] | add' .taskmaster/tasks/tasks.json)
echo "Proposals: $proposal_count, Subtasks: $subtask_count"

# Verify TASKMASTER_OPENSPEC_MAP.md is complete
# Each subtask should map to exactly 1 proposal
```

### Context Management

| Batch Size | Parallel Agents | Context Risk | Recommended |
|------------|-----------------|--------------|-------------|
| 1 task     | 1 agent         | Very Low     | For large tasks |
| 2 tasks    | 2 agents        | Low          | **Default** |
| 3 tasks    | 3 agents        | Medium       | If tasks are small |
| 4+ tasks   | 4+ agents       | HIGH         | Avoid |

**CRITICAL:** Never launch more than 2 parallel subagents at once.

### Performance Estimate

| Master Tasks | Batches | Subtasks | Time (sequential batches) |
|--------------|---------|----------|---------------------------|
| 8-10         | 4-5     | 30-40    | 25-40 min |
| 10-12        | 5-6     | 40-50    | 35-50 min |
| 12-15        | 6-8     | 50-60    | 45-70 min |

Slower than fully parallel, but **reliable** - no context exhaustion.

## Completion Signal

```json
{
  "phase": 6,
  "status": "success",
  "summary": {
    "master_tasks_processed": N,
    "subtasks_processed": M,
    "proposals_created": M,
    "mapping_strategy": "1-proposal-per-subtask"
  },
  "next_phase": 6.1,
  "trigger_next": true
}
```

**Note:** `subtasks_processed` always equals `proposals_created` (1:1 mapping)

## Output Files

- `openspec/changes/*/proposal.md`
- `TASKMASTER_OPENSPEC_MAP.md` (updated)
- `.taskmaster/phase6-summary.md`
- `.taskmaster/.signals/phase6-specs-created.json`

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 6.1.**

When Phase 6 is complete (all proposals created), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 6 COMPLETE
   [SIGNAL:PHASE6_SPECS_CREATED]
   ```

2. **IMMEDIATELY** proceed to Phase 6.1 by outputting:
   ```
   [ACTIVATE:TEST_STRATEGY_V1]
   ```

3. Begin test strategy generation without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- Pipeline Orchestrator (triggers this)
- PRD-to-Tasks skill (generates TaskMaster format)
- TaskMaster documentation (for hierarchical structure)
- Test Strategy Generator skill (Phase 6.1, auto-enhances proposals)