---
name: iterative-plan-execution
description: |
  Autonomous phase-by-phase plan implementation with journaling.
  Decomposes phases into atomic tasks and verifies each via
  typecheck + spike + export resolution triad.
triggers:
  - "iterate.*plan"
  - "phase.*by.*phase"
  - "execute.*plan"
  - "implement.*phases"
  - "ralph.*plan"
---

# Iterative Plan Execution

## Purpose

Execute multi-phase implementation plans autonomously with:
- Progressive phase-by-phase advancement
- Atomic task decomposition per phase
- Verification triad after each task
- Persistent journaling for context recovery
- Beads integration for work tracking

---

## Execution Protocol

### 1. Plan Ingestion

```
READ plan file completely
IDENTIFY total phase count
CREATE beads issue per phase: bd create --title="Phase N: <description>" --type=task
SET current_phase = 1
```

### 2. Phase Loop

```
WHILE current_phase <= total_phases:
    READ phase N requirements from plan
    DECOMPOSE into atomic tasks using TodoWrite
    FOR each task in phase:
        MARK task as in_progress
        IMPLEMENT task
        VERIFY via triad
        WRITE journal entry
        MARK task as completed
    END FOR
    UPDATE plan checkboxes for phase N
    REPORT phase completion
    INCREMENT current_phase
END WHILE
```

### 3. Task Verification Triad

Every task must pass ALL three checks:

| Check | Command | Purpose |
|-------|---------|---------|
| Type Safety | `bun run typecheck` | Catch compile errors |
| Runtime Smoke | `bun run scripts/spike-<feature>-phase-N.ts` | Exercise new code |
| Export Resolution | Import in scratch file | Verify module wiring |

---

## Journaling Protocol

### File Location

```
.agents/val/journal/YYYY-MM-DD-<feature>-phase-N-task-M.md
```

### Template

```markdown
# Phase N Task M

**Feature**: <feature-name>
**Date**: YYYY-MM-DD HH:MM
**Status**: complete | blocked | partial

## Files Touched

- path/to/file1.ts
- path/to/file2.ts

## Implementation Summary

<2-3 sentences describing what was done>

## Verification

### Type Safety
- [ ] bun run typecheck passed

### Runtime Smoke
- [ ] Spike script executed successfully
- Script: scripts/spike-<feature>-phase-N.ts

### Export Resolution
- [ ] Imports resolve in test file

## Learnings

<Discoveries and patterns worth noting>

## Blockers

<If status is blocked - describe the blocker>

## Next

<What follows this task>
```

---

## Spike Generation Per Phase

For each phase create a minimal spike script:

### Naming Convention

```
scripts/spike-<feature>-phase-N.ts
```

### Spike Template

```typescript
/**
 * Spike: <Feature> Phase N Verification
 *
 * Tests that Phase N implementation works correctly.
 * Run: bun run scripts/spike-<feature>-phase-N.ts
 */

import { Effect } from 'effect'

// Import the new modules from this phase
// import { ... } from '@/lib/<feature>/...'

async function main() {
  console.log('=== Phase N Verification ===\n')

  // H1: Basic instantiation
  console.log('H1: Basic instantiation')
  // ... test basic creation works

  // H2: Core functionality
  console.log('H2: Core functionality')
  // ... test main feature works

  // H3: Integration
  console.log('H3: Integration')
  // ... test integration with existing code

  console.log('\n=== Phase N Verification Complete ===')
}

main().catch(console.error)
```

---

## Beads Integration

### Phase Start

```bash
bd create --title="<Feature> Phase N: <phase-description>" --type=task
bd update <issue-id> --status=in_progress
```

### Phase End

```bash
bd close <issue-id>
bd sync --from-main
```

### Blocked

```bash
bd update <issue-id> --status=blocked
# Add blocker details to journal
```

---

## Plan File Updates

After completing each phase section update the plan:

```markdown
### Phase 1: G2 Theme Infrastructure

- [x] Create vanta-theme.ts
- [x] Create palettes.ts
- [x] Create index.ts
- [x] Verify theme renders correctly
```

Use Edit tool to check off completed items.

---

## Recovery Protocol

If context compacts or session restarts:

```
1. READ .agents/val/journal/ directory for latest entries
2. IDENTIFY last completed phase and task
3. READ plan file for checkbox state
4. RESUME from next uncompleted item
```

---

## Error Handling

### Typecheck Fails

```
1. READ error message
2. FIX type errors
3. RE-RUN typecheck
4. CONTINUE only when passing
```

### Spike Fails

```
1. ANALYZE failure output
2. IDENTIFY root cause
3. FIX implementation
4. RE-RUN spike
5. If 3+ failures: MARK as blocked and REPORT
```

### Export Resolution Fails

```
1. CHECK index.ts exports
2. VERIFY barrel exports chain
3. FIX missing exports
4. RE-TEST import
```

---

## Self-Prompts

### Before Starting Phase

```
"Reading Phase N requirements. Decomposing into atomic tasks."
```

### Before Each Task

```
"Task M of Phase N: <task-description>. Implementing now."
```

### After Task Verification

```
"Task M verified. Writing journal entry."
```

### Phase Complete

```
"Phase N complete. All tasks verified. Updating plan checkboxes."
```

### Blocker Encountered

```
"BLOCKED on Task M of Phase N: <blocker-description>.
Journaling and requesting guidance."
```

---

## Example Execution Flow

```
> Invoke /iterative-plan-execution with plan: .claude/plans/chart-styling.md

Reading plan...
Found 5 phases.

Creating beads issues...
  beads-101: Chart Styling Phase 1: G2 Theme Infrastructure
  beads-102: Chart Styling Phase 2: Per-Chart Style Atoms
  beads-103: Chart Styling Phase 3: ChartRenderer Integration
  beads-104: Chart Styling Phase 4: Layered Styler Services
  beads-105: Chart Styling Phase 5: Effectful Streaming

Starting Phase 1...
  Decomposed into 4 tasks:
    1. Create vanta-theme.ts
    2. Create palettes.ts
    3. Create index.ts
    4. Run verification

  Task 1/4: Creating vanta-theme.ts
    [implementing...]
    [typecheck: PASS]
    [spike: PASS]
    [exports: PASS]
    [journal written: 2026-01-18-chart-styling-phase-1-task-1.md]

  Task 2/4: Creating palettes.ts
    ...

Phase 1 complete. 4/4 tasks verified.
Updating plan checkboxes...
bd close beads-101

Proceed to Phase 2? [continuing...]
```

---

## Invocation

### From Ralph Prompt

```
/iterative-plan-execution .claude/plans/<plan-file>.md
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| Plan path | Required - path to plan markdown file |
| --start-phase N | Optional - start from specific phase |
| --dry-run | Optional - show decomposition without executing |

---

## Related Skills

| Skill | Use |
|-------|-----|
| `/spike-testing` | Spike methodology for verification |
| `/implement_plan` | Alternative non-iterative execution |
| `/beads-issue-management` | Work tracking commands |
