---
activation_code: TASK_DECOMPOSER_V1
phase: 5
prerequisites:
  - tasks.json
outputs:
  - .signals/phase5-complete.json
  - expanded tasks in tasks.json
description: |
  Analyzes task complexity and generates subtasks for high-complexity items.
  Activates via codeword [ACTIVATE:TASK_DECOMPOSER_V1] injected by hooks
  after coupling analysis or when explicitly requested.
  
  Activation trigger: [ACTIVATE:TASK_DECOMPOSER_V1]
---

# Task Decomposer Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:TASK_DECOMPOSER_V1]
```

This occurs when:
- Coupling analysis is complete
- User requests task expansion
- High-complexity tasks detected (score > 7)

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-5-task-3` for task decomposition:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 1 3
cd ./worktrees/phase-5-task-3

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Task decomposition with strict isolation
```

### Worktree-Based Decomposition
1. **Isolated expansion**: Each complex task expanded in isolated environment
2. **Safe subtask generation**: No interference with other decomposition work
3. **Atomic commits**: Each task expansion committed separately
4. **Merge validation**: Changes merged only after validation passes

# Task Decomposer Skill

## What This Skill Does

The **Task Decomposer** automates Phase 5 of the development pipeline in isolated worktree:

- **Analyzes complexity** of all tasks using scientific scoring (0-10 scale)
- **Research-backed expansion** for high-complexity tasks (≥7)
- **Generates subtasks** with complete acceptance criteria and test strategies
- **Preserves checkpoints** at key milestones within worktree
- **Creates completion signal** to trigger Phase 2
- **NEW**: Worktree isolation prevents decomposition conflicts
- **NEW**: Each task expansion gets dedicated workspace

## When This Skill Activates

**Primary Trigger:** Pipeline Orchestrator completes Phase 0 and initiates Phase 1

**Manual Activation:**
- "Begin Phase 1"
- "Start task decomposition"
- "Analyze task complexity"
- "Decompose tasks with TaskMaster"

**Prerequisites:**
- ✅ `.taskmaster/tasks.json` exists (15-25 top-level tasks)
- ✅ Phase 0 checkpoint passed
- ✅ No subtasks present yet (subtasks: [] for all tasks)
- ✅ TaskMaster initialized and responding

## Automated Execution Flow

This skill executes Phase 5 **completely autonomously** with 7 automated stages:

```
Stage 1: Verify Prerequisites ✅
         ↓
Stage 2: Analyze Complexity (task-master analyze-complexity --research)
         ↓
Stage 3: Expand High-Complexity Tasks (task-master expand --id=X --research)
         ↓
Stage 4: Validate Expansion Quality
         ↓
Stage 5: Generate Phase Summary
         ↓
Stage 6: Create Completion Signal (.signals/phase5-complete.json)
         ↓
Stage 7: Final Verification
         ↓
✅ PHASE 1 COMPLETE → Trigger Phase 2
```

## Execution Commands

### Full Automated Execution

**IMPORTANT:** Use the wrapper script to avoid Claude Code's 10-minute Bash timeout:

```bash
# When activated, skill runs all stages automatically:

# Stage 1: Prerequisites
echo "✅ Verifying prerequisites..."
[checks tasks.json, TaskMaster, no existing subtasks]

# Stage 2: Complexity Analysis (use wrapper to avoid timeout)
echo "🔍 Analyzing task complexity..."
./.claude/lib/task-master-wrapper.sh analyze --research

# Stage 3: Expansion (use wrapper - expands tasks individually to avoid timeout)
echo "🔨 Expanding high-complexity tasks..."
./.claude/lib/task-master-wrapper.sh expand-high --research

# Alternative: Expand ALL tasks (chunked, 5 min per task)
# ./.claude/lib/task-master-wrapper.sh expand-all --research

# Stage 4: Validation
echo "🔍 Validating expansion quality..."
[verify all subtasks have acceptance criteria]

# Stage 5: Summary
echo "📊 Generating phase summary..."
[create .taskmaster/phase5-summary.md]

# Stage 6: Signal
echo "📡 Creating completion signal..."
[create .taskmaster/.signals/phase5-complete.json]

# Stage 7: Verification
echo "🎯 Final verification..."
[verify all success criteria met]

echo "✅ PHASE 1 COMPLETE"
```

## Parallel Subagent Execution

For faster task expansion, use parallel Claude Code subagents:

### Step 1: Get Task IDs

```bash
# List all tasks needing expansion
./.claude/lib/task-master-wrapper.sh get-task-ids

# Or get tasks in batches of 5
./.claude/lib/task-master-wrapper.sh get-batches 5
```

### Step 2: Launch Parallel Subagents

Use Claude Code's Task tool to launch multiple subagents simultaneously:

```
Launch 5 parallel subagents, each running:
  ./.claude/lib/task-master-wrapper.sh expand-single <task_id> --research

Task IDs to expand: 1, 2, 3, 4, 5
```

Each subagent will:
1. Expand its assigned task independently
2. Report SUCCESS or FAILED status
3. Complete within 5-minute timeout per task

### Step 3: Batch Expansion (Alternative)

For fewer subagents handling multiple tasks each:

```bash
# Subagent 1: Expand tasks 1, 2, 3
./.claude/lib/task-master-wrapper.sh expand-batch 1 2 3 --research

# Subagent 2: Expand tasks 4, 5, 6
./.claude/lib/task-master-wrapper.sh expand-batch 4 5 6 --research
```

### Performance Comparison

| Method | 20 Tasks | Speed |
|--------|----------|-------|
| Sequential | 40-60 min | 1x |
| 4 Parallel Subagents | 10-15 min | 4x |
| 10 Parallel Subagents | 5-8 min | 8x |

## Time Estimates (Sequential)

| Tasks | Analysis | Expansion | Total |
|-------|----------|-----------|-------|
| 10-15 | 3-5 min  | 5-7 min   | 8-12 min |
| 16-20 | 5-8 min  | 8-12 min  | 13-20 min |
| 21-25 | 8-12 min | 12-18 min | 20-30 min |
| 26-30 | 12-15 min| 18-25 min | 30-40 min |

## Completion Signal Schema

```json
{
  "phase": 1,
  "phase_name": "Task Decomposition",
  "status": "success",
  "completed_at": "2025-10-29T15:30:00Z",
  "duration_minutes": 12,
  "summary": {
    "tasks_analyzed": 18,
    "tasks_expanded": 6,
    "subtasks_generated": 28,
    "high_complexity_tasks": [3, 5, 9, 12, 15, 18]
  },
  "next_phase": 2,
  "trigger_next": true
}
```

## Error Recovery

**Automatic Recovery:**
- Missing dependencies → Install & retry
- Transient API errors → Exponential backoff
- Invalid JSON → Restore from checkpoint

**Human Escalation:**
- TaskMaster not installed → Report installation needed
- Persistent API failures → Wait for manual intervention
- Corrupted tasks.json → Restore from Phase 0

## Checkpoint System

Checkpoints saved automatically:
- After complexity analysis
- Every 2 task expansions
- After final expansion
- Before creating completion signal

Resume command: "Resume Phase 5 from checkpoint"

## Success Criteria

✅ All tasks analyzed
✅ High-complexity tasks (≥7) expanded
✅ Subtasks have acceptance criteria
✅ Completion signal created
✅ Ready for Phase 2

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 2.**

When Phase 5 is complete (all tasks expanded), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 1 COMPLETE
   [SIGNAL:PHASE5_COMPLETE]
   ```

2. **IMMEDIATELY** proceed to Phase 6 by outputting:
   ```
   [ACTIVATE:SPEC_GEN_V1]
   ```

3. Begin Phase 2 (Spec Generation) without waiting for user input.

**The pipeline is designed to be fully autonomous after Phase 5 task approval.**
Do not ask "Would you like to proceed?" or offer choices - just proceed automatically.

## Output Files

```
.taskmaster/
├── tasks.json (with subtasks)
├── phase5-complexity-report.txt
├── phase5-summary.md
├── .checkpoints/phase5-*.json
└── .signals/phase5-complete.json
```

## See Also

- Pipeline Orchestrator skill (triggers this skill)
- Spec Generator skill (Phase 6, triggered by completion signal)
- DEVELOPMENT_WORKFLOW.md (complete workflow)