---
name: plan-iteration-checkpoint
description: |
  Iteration checkpoint protocol for multi-phase plan execution.
  Assess progress, determine next steps, document current intention.
triggers:
  - "iteration.*checkpoint"
  - "plan.*progress"
  - "assess.*plan"
  - "next.*phase"
  - "document.*intention"
---

# Plan Iteration Checkpoint

## Purpose

This skill provides a structured checkpoint protocol for agents (like Ralph) executing multi-phase implementation plans. It ensures each iteration cycle:

1. **Assesses current progress** against the plan
2. **Determines next steps** forward
3. **Documents current intention** for continuity

## When to Use

- At the start of each iteration cycle in a multi-phase plan
- When resuming work on a long-running implementation
- Before session close to capture state
- When the `iteration-summary` hook triggers

## Protocol

### Phase 1: Progress Assessment

Read the plan file and compare against actual state:

```bash
# Locate the plan (check common locations)
PLAN_FILE="${PLAN_FILE:-thoughts/shared/plans/CTL_TUI_ARCHITECTURE_PLAN.md}"

# If plan path provided as arg, use it
[ -n "$1" ] && PLAN_FILE="$1"
```

For each phase in the plan:
- [ ] Check completion markers
- [ ] Verify artifacts exist (files created, tests passing)
- [ ] Note blockers or deviations

Output format:
```
## Progress Assessment

### Completed Phases
- [x] Phase 1: Foundation - DONE (files: src/core/domain/*.ts)
- [x] Phase 2: Ink Rendering - DONE (tests: passing)

### Current Phase
- [ ] Phase 3: Agent Output Mode - IN PROGRESS
  - Created: src/render/agent/schemas.ts
  - Remaining: serializer.ts, streaming.ts

### Blocked/Deferred
- Phase 7: OpenTUI - BLOCKED (dependency: TanStack Router setup)
```

### Phase 2: Next Steps Determination

Based on progress, identify the immediate next action:

```
## Next Steps

### Immediate (This Iteration)
1. Complete `src/render/agent/serializer.ts`
2. Wire `--agent` flag to AgentOutputService
3. Add unit tests for CtlAgentOutput schema

### Dependencies
- Requires: CtlAgentOutput schema (DONE)
- Enables: Phase 4 (Project Discovery)

### Decision Points
- [ ] Choose streaming format: NDJSON vs SSE
```

### Phase 3: Intention Documentation

Write a clear statement of intent for continuity:

```
## Current Intention

**Goal**: Complete Agent Output Mode (Phase 3)

**Approach**: Implement the serializer using Effect.Match for
discriminated union handling, output CtlAgentOutput JSON to stdout
when --agent flag detected.

**Success Criteria**:
- `ctl health --agent` outputs valid CtlAgentOutput JSON
- Schema validates with Effect.Schema.decodeUnknown
- Streaming updates emit progressive chunks

**Time Box**: 1 iteration cycle (~30 min focused work)
```

## Output Location

Write checkpoint to `.agents/val/journal/YYYY-MM-DD-iteration-N.md`:

```bash
JOURNAL_DIR="$CLAUDE_PROJECT_DIR/.agents/val/journal"
DATE=$(date +%Y-%m-%d)
ITERATION=$(ls "$JOURNAL_DIR/$DATE-iteration-"*.md 2>/dev/null | wc -l)
ITERATION=$((ITERATION + 1))
CHECKPOINT_FILE="$JOURNAL_DIR/$DATE-iteration-$ITERATION.md"
```

## Full Checkpoint Template

```markdown
# Iteration Checkpoint: {DATE} #{N}

## Plan Reference
- **Plan**: {PLAN_FILE}
- **Target Phase**: {CURRENT_PHASE}

## Progress Assessment

### Completed
{LIST_COMPLETED_ITEMS}

### In Progress
{LIST_IN_PROGRESS_ITEMS}

### Blocked
{LIST_BLOCKED_ITEMS}

## Next Steps

### Immediate
{ORDERED_NEXT_ACTIONS}

### Decision Points
{PENDING_DECISIONS}

## Current Intention

**Goal**: {SINGLE_SENTENCE_GOAL}

**Approach**: {HOW_TO_ACHIEVE}

**Success Criteria**:
{MEASURABLE_CRITERIA}

---
*Checkpoint written: {TIMESTAMP}*
```

## Integration with Hooks

The `iteration-summary` hook (SessionEnd) will:
1. Invoke this skill to generate final checkpoint
2. Write summary to journal
3. Update beads if applicable

## Usage in Ralph One-Liner

```bash
claude --print "invoke /plan-iteration-checkpoint with plan at $PLAN_FILE, then continue implementing the next phase until iteration budget exhausted"
```

## Related Skills

- `/implement_plan` - Execute plans from thoughts/shared/plans
- `/create_handoff` - Create handoff documents for session transfer
- `/beads-session-workflow` - Beads issue tracking integration
