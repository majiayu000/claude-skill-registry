---
name: l-thread
description: |
  Long-duration autonomous task with checkpoints and verification. Use when:
  - User says "overnight", "long running", "autonomous task"
  - User mentions "l-thread", "extended task"
  - Task will consume significant context window
  - Multi-phase implementation requiring persistence across interruptions
context: fork
---

# Long-Duration Thread: Autonomous Execution with Checkpoints

For tasks too large for a single context window. Implements checkpoint/restore, automatic verification, and graceful recovery.

## When to Use

- Large refactors spanning 10+ files
- Full feature implementation with tests
- Migration tasks (dependency upgrades, API changes)
- Any task estimated at >50% context window

## Checkpoint Strategy

### Automatic Checkpoints

Checkpoints are saved automatically at context usage thresholds. See `hooks/checkpoint.md` for actions at 70% / 80% / 90%.

### Manual Checkpoints

Save checkpoints at these milestones:
- After completing a logical phase
- Before risky operations (schema changes, large refactors)
- After passing verification

### Checkpoint Contents

See `hooks/checkpoint.md` for the full checkpoint JSON schema, storage location, and auto-checkpoint threshold actions.

### Save/Restore Commands

```bash
# Save checkpoint
/checkpoint save "Completed phase 3"

# List checkpoints
/checkpoint list

# Restore from latest
/checkpoint restore
```

## Verification Stack

Every checkpoint must pass Levels 1-3 before saving. Full verification (Levels 1-5) at task completion. See `hooks/verification-check.md` for the complete 5-level stack, per-agent requirements, and failure handling.

## Workflow

### Phase 1: Planning

```
Task(planner, "Break down [task] into phases with dependencies and estimates")
```

Produce a phased plan with:
- Ordered phases with dependencies
- Token estimates per phase
- Checkpoint points identified
- Verification criteria per phase

### Phase 2: Execution Loop

For each phase:

1. **Start**: Log phase start
2. **Implement**: Execute the phase work
3. **Verify**: Run verification stack
4. **Checkpoint**: Save state if milestone reached
5. **Monitor**: Check context usage, checkpoint if threshold hit

### Phase 3: Completion

```markdown
## Verification Summary
- [x] TypeScript compiles
- [x] Biome lint passes
- [x] Tests pass (N/N)
- [x] All phases completed

<promise>COMPLETE</promise>
```

## Recovery from Interruption

When resuming after interruption:

1. Run `checkpoint.sh restore` to load latest state
2. Check git status for uncommitted work
3. Review remaining todos
4. Run verification to confirm baseline
5. Continue from next incomplete phase

## Completion Promise

The task is NOT complete until:

```
1. All phases done
2. Verification passes (compile + lint + test)
3. Git is clean (all changes committed)
4. Summary provided with what was done
```

Only then output:

```
<promise>COMPLETE</promise>
```

**Never claim completion with failing verification.**

## Example

```
User: "Migrate all class components to hooks across the app"

→ Task(planner, "Break migration into phases by module")
Plan: 6 phases, ~4 context windows estimated

Phase 1: Core hooks (auth, routing)
  → Implement → Verify → Checkpoint at 30%
Phase 2: Feature hooks (dashboard, settings)
  → Implement → Verify → Checkpoint at 55%
  → Context at 70% → auto-checkpoint, continue
Phase 3: Shared components
  → Context at 90% → auto-checkpoint, hand off
  [New session resumes from checkpoint]
Phase 4-6: Continue...
  → Final verification → <promise>COMPLETE</promise>
```
