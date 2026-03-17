---
name: checkpoint
description: Robust workflow checkpoint and resume. Handles session interruption, state recovery, and safe resume across all workflow phases.
allowed-tools: Read, Write, Glob
---

# Checkpoint & Resume Skill

Pattern for saving workflow state and resuming after interruption.

## When to Load This Skill

- Starting a workflow that might be interrupted
- Resuming after `claude -r`
- Recovering from crashes or timeouts

## Core Concept

The dotagent workflow uses **file-based state** that survives session interruption:

```
Session crash/exit
        ↓
State files persist on disk:
  - memory/state/phase.json        # Which phase we're in
  - memory/state/execution.json    # Task-level progress
  - memory/reports/*.json          # Completed phase outputs
        ↓
claude -r (resume session)
        ↓
Orchestrator reads state, continues from last checkpoint
```

## Checkpoint Files

### Phase Checkpoint: `memory/state/phase.json`

```json
{"workflow_id":"string","started_at":"ISO-8601","last_updated":"ISO-8601","current_phase":"REQUIREMENTS|ARCHITECTURE|IMPLEMENTATION|VERIFICATION|REFLECTION","phase_status":"pending|in_progress|complete|failed","completed_phases":[{"phase":"REQUIREMENTS","completed_at":"ISO-8601","output":"memory/reports/demand.json"}],"user_checkpoints":[{"phase":"REQUIREMENTS","approved_at":"ISO-8601"}],"interruption_safe":true}
```

### Execution Checkpoint: `memory/state/execution.json`

See executor agent for detailed schema with:
- Task status tracking
- Timestamps (started_at, completed_at)
- Output file paths for verification

## Resume Protocol

### Step 1: Detect Resume Scenario

```
ON WORKFLOW START:
  checkpoint = Read("memory/state/phase.json")

  IF checkpoint exists AND checkpoint.phase_status == "in_progress":
    → This is a RESUME
    → Log: "Detected interrupted workflow: {workflow_id}"
    → Go to Step 2
  ELSE:
    → Fresh start, create new checkpoint
```

### Step 2: Validate State Integrity

```
VALIDATE:
  1. Check all referenced output files exist
  2. Check timestamps are reasonable (not future, not ancient)
  3. Check phase progression is valid
  4. Check for incomplete writes (interruption_safe flag)

IF validation fails:
  → Ask user: "State appears corrupted. Start fresh? [y/N]"
  → Archive corrupted state to memory/state/.archive/
```

### Step 3: Determine Resume Point

```
RESUME LOGIC by phase:

REQUIREMENTS (in_progress):
  - Check if demand.json exists and is valid
  - If valid: advance to ARCHITECTURE
  - If not: re-spawn PM agent

ARCHITECTURE (in_progress):
  - Check for design files in memory/reports/designs/
  - Check for final_design.json
  - If final exists: advance to IMPLEMENTATION
  - If designs exist but no final: spawn Roundtable
  - If no designs: re-spawn Architects

IMPLEMENTATION (in_progress):
  - Read execution.json
  - Run executor recovery checks
  - Continue execution loop

VERIFICATION (in_progress):
  - Check for verification.json
  - If exists: advance to REFLECTION
  - If not: re-spawn QA

REFLECTION (in_progress):
  - Check for reflection file
  - If exists: workflow complete
  - If not: re-spawn Reflector
```

### Step 4: Inform User and Continue

```
LOG to user:
  "Resuming workflow {id} from {phase} phase"
  "Last activity: {timestamp}"
  "Completed: {list of completed phases}"

IF current_phase requires user approval (was at checkpoint):
  → Re-confirm with user before proceeding
```

## Safe Checkpoint Writing

Always update checkpoint atomically:

```
# BAD: Can leave corrupted state
Write(checkpoint_file, new_state)

# GOOD: Atomic update
1. Set interruption_safe = false
2. Write to checkpoint_file.tmp
3. Rename checkpoint_file.tmp → checkpoint_file
4. Set interruption_safe = true
```

## Recovery from Specific Scenarios

### Scenario 1: Ctrl-C During Subagent

```
State: task-001 status="running", no output file

Recovery:
- Detect orphaned task
- Increment attempts
- Reset to "pending"
- Re-spawn on next loop
```

### Scenario 2: Crash After Write, Before State Update

```
State: task-001 status="running", output file EXISTS

Recovery:
- Detect output file
- Read status from output
- Update state to match
```

### Scenario 3: Interrupted During User Approval

```
State: phase=ARCHITECTURE, has designs but no final_design

Recovery:
- Detect we're at approval checkpoint
- Re-present options to user
- Don't re-run architects
```

### Scenario 4: Ancient State File

```
State: started_at is 7 days ago

Recovery:
- Warn user about stale state
- Offer to archive and start fresh
- If continue: proceed with caution
```

## Checkpoint Frequency

Update checkpoint after:
- Phase completion
- User approval
- Each task status change (in executor)
- Before spawning expensive agents (opus)

## Archiving Old State

When starting fresh or after completion:

```
Archive pattern:
  memory/state/.archive/{workflow_id}_{timestamp}/
    - phase.json
    - execution.json

Keep last 5 archives, delete older
```

## Integration with Workflow

### In /develop Command

```markdown
## Resume Check

Before starting workflow:
1. Check for existing phase.json
2. If exists and in_progress:
   - Show resume prompt to user
   - "Resume workflow from {phase}? [Y/n]"
3. If user confirms: load checkpoint, continue
4. If user declines: archive old state, start fresh
```

### In Each Phase Agent

```markdown
## On Completion

Before returning:
1. Write output file
2. Update phase.json:
   - Add to completed_phases
   - Advance current_phase
   - Set phase_status = complete
3. Log checkpoint saved
```

## Principles

1. **State on disk** - Never rely on conversation memory alone
2. **Validate before resume** - Don't blindly trust old state
3. **Inform the user** - Always tell them what's being resumed
4. **Atomic writes** - Prevent half-written state
5. **Archive, don't delete** - Keep old state for debugging
