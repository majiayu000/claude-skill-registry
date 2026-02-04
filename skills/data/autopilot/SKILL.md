---
name: autopilot
description: This skill should be used when the user asks to "run autopilot", "autopilot feature N", "implement all phases", "run all phases sequentially", "autopilot 003", or wants to automatically implement all phases of a feature in sequence without manual intervention.
---

# Autopilot: Sequential Phase Implementation

Run all phases of a feature sequentially via subagents, respecting dependencies.

## User Input

ARGUMENTS = $ARGUMENTS

Accept a feature number (e.g., "003") or use current branch if not provided.

```bash
/autopilot 003        # Run all phases for feature 003
/autopilot            # Run all phases for current branch's feature
```

## Execution Flow

```
/autopilot 003
       │
       ▼
┌─────────────────────┐
│  Load Feature       │
│  • Find tasks.md    │
│  • Parse phases     │
│  • Build order      │
└─────────┬───────────┘
       │
       ▼
┌─────────────────────┐
│  For Each Phase:    │
│                     │
│  ┌───────────────┐  │
│  │ Spawn Agent   │  │
│  │ /implement    │  │
│  │ "Phase N"     │  │
│  └───────┬───────┘  │
│          │          │
│          ▼          │
│  ┌───────────────┐  │
│  │ Wait for      │  │
│  │ Completion    │  │
│  └───────┬───────┘  │
│          │          │
│          ▼          │
│  ┌───────────────┐  │
│  │ Report Status │  │
│  │ → Next Phase  │  │
│  └───────────────┘  │
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Final Summary      │
└─────────────────────┘
```

## Workflow

### Step 1: Resolve Feature

1. If ARGUMENTS provided, use as feature number (e.g., "003")
2. If no ARGUMENTS, extract from current git branch:
   ```bash
   git branch --show-current
   # feature/003-agent-behavior-statecharts → 003
   ```
3. Find feature folder in `backlog/plans/{NNN}-*/`

### Step 2: Parse Phases from tasks.md

Read `{feature-path}/tasks.md` and extract phases:

```
## Phase 1: Core Types
## Phase 2: Statechart Engine
## Phase 3: LLM Reasoner
...
```

Build ordered list: `["Phase 1", "Phase 2", "Phase 3", ...]`

### Step 3: Sequential Execution

For each phase in order:

1. **Spawn subagent** using Task tool:
   ```
   Task(
     subagent_type: "general-purpose",
     description: "Implement Phase N",
     prompt: """
   Implement Phase N for feature {feature-id}.

   CRITICAL: Your first action must be to invoke the implement skill:

   Skill(skill: "implement", args: "Phase N")

   The implement skill will guide you through TDD workflow for all tasks in this phase.
   Do NOT try to implement tasks manually - invoke the Skill tool first.

   Report success or failure when the phase is complete.
   """,
     run_in_background: false  # Wait for completion
   )
   ```

2. **Wait for completion** before starting next phase

3. **Check result** - if phase fails, stop and report

### Step 4: Progress Reporting

After each phase completes, report:

```
✅ Phase 1: Complete (T001-T006)
🔄 Phase 2: In Progress...
```

### Step 5: Final Summary

After all phases complete:

```
🎉 Autopilot Complete: Feature 003

✅ Phase 1: Core Types (T001-T006)
✅ Phase 2: Statechart Engine (T007-T015)
✅ Phase 3: LLM Reasoner (T016-T023)
✅ Phase 4: Timeout Transitions (T024-T029)
✅ Phase 5: Agent Integration (T030-T039)
✅ Phase 6: Queries + Validation (T040-T047)

All 47 tasks completed.

Next steps:
1. Run linting: uv run ruff check . && uv run flake8 .
2. Run tests: uv run pytest
3. Run spec tests: /spec-tests specs/tests/003-*.md
4. Create PR when ready
```

## Error Handling

If a phase fails:

1. **Stop execution** - don't proceed to dependent phases
2. **Report failure** with context:
   ```
   ❌ Phase 3 failed

   Completed: Phase 1, Phase 2
   Failed: Phase 3 (LLM Reasoner)
   Skipped: Phase 4, Phase 5, Phase 6

   Error: [error details from agent]

   To resume: /implement "Phase 3"
   ```
3. **Preserve progress** - completed phases remain done

## Running in Background

For long-running features, run autopilot in background:

```
# In the skill execution, use:
Task(
  ...
  run_in_background: true
)
```

Then check progress with:
```bash
tail -100 {output_file}
```

## Example Session

```
User: /autopilot 003

Claude: Starting autopilot for feature 003-agent-behavior-statecharts

Found 6 phases to implement:
1. Phase 1: Core Types (T001-T006)
2. Phase 2: Statechart Engine (T007-T015)
3. Phase 3: LLM Reasoner (T016-T023)
4. Phase 4: Timeout Transitions (T024-T029)
5. Phase 5: Agent Integration (T030-T039)
6. Phase 6: Queries + Validation (T040-T047)

🔄 Phase 1: Starting...
[Agent implements Phase 1]
✅ Phase 1: Complete

🔄 Phase 2: Starting...
[Agent implements Phase 2]
✅ Phase 2: Complete

...continues through all phases...

🎉 Autopilot Complete!
```

## Notes

- Each phase runs as a separate subagent for isolation
- Phases execute sequentially to respect dependencies
- Progress is reported after each phase
- On failure, stops immediately to prevent cascading issues
- User can resume from failed phase with `/implement "Phase N"`
