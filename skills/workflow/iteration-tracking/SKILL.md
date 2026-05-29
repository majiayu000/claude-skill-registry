---
name: Iteration Tracking
description: Tracks iteration progress and state management. Use when starting, checkpointing, or ending iteration cycles, or when user mentions iteration tracking, progress monitoring, or iteration state.
allowed-tools: Read, Bash, Write
---

# Iteration Tracking

This skill provides iteration state management, progress tracking, and checkpoint creation for development cycles.

## What This Skill Provides

### 1. Iteration State Management
- Initialize new iteration cycles
- Track iteration status and progress
- Manage iteration metadata

### 2. Checkpoint System
- Create mid-iteration checkpoints
- Capture git state at checkpoints
- Track progress between checkpoints

### 3. Iteration Reports
- Progress summaries
- Change tracking
- Time and effort metrics

## Instructions

### Starting an Iteration

When user wants to start a new iteration:

1. Create iteration directory structure:
   !{bash mkdir -p .multiagent/iterations/$ITERATION_NAME}

2. Initialize state file with JSON:
   ```json
   {
     "name": "$ITERATION_NAME",
     "status": "in_progress",
     "started_at": "timestamp",
     "checkpoints": []
   }
   ```

3. Create symlink to current iteration:
   !{bash ln -sf $ITERATION_NAME .multiagent/iterations/current}

### Creating Checkpoints

When user wants to create a checkpoint:

1. Load current iteration
2. Create checkpoint directory
3. Capture git status and diff
4. Update state with checkpoint metadata

### Ending an Iteration

When user completes an iteration:

1. Create final snapshot
2. Update state to "completed"
3. Remove current symlink
4. Generate summary report

## State File Structure

```json
{
  "name": "feature-auth",
  "status": "in_progress",
  "started_at": "2025-10-24T10:00:00Z",
  "checkpoints": [
    {
      "id": "1234567890",
      "timestamp": "2025-10-24T11:00:00Z",
      "message": "Initial implementation"
    }
  ],
  "completed_at": null
}
```

## Success Criteria

- ✅ Iteration state is persisted and trackable
- ✅ Checkpoints capture meaningful progress
- ✅ Reports show clear progress metrics
- ✅ State transitions are clean and consistent

---

**Plugin**: 04-iterate
**Skill Type**: State Management + Tracking
**Auto-invocation**: Yes (via description matching)
