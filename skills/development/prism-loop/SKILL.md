---
name: prism-loop
description: Start PRISM TDD workflow loop using Ralph Wiggum pattern. Auto-progresses through Planning, TDD RED (failing tests), TDD GREEN (implementation), and Review phases. Use when user wants to run the core development cycle.
version: 3.3.0
author: PRISM
---

# PRISM Workflow Loop

TDD-driven workflow orchestration using the Ralph Wiggum self-referential loop pattern.

## When to Use

- User wants to run the PRISM core development cycle
- Starting a new story implementation with TDD
- Need automated workflow progression with gates

## How It Works

1. **Stop Hook** intercepts session exit and re-injects the next step instruction
2. **Agent steps** auto-progress (SM → QA → DEV)
3. **Gate steps** pause for `/prism-approve` (or `/prism-reject` at red_gate)
4. **Validation** runs tests to verify TDD state (RED = fail, GREEN = pass)

## Workflow Steps (7 steps)

| # | Phase | Step | Agent | Type |
|---|-------|------|-------|------|
| 1 | Planning | review_previous_notes | SM | agent |
| 2 | Planning | draft_story | SM | agent |
| 3 | TDD RED | write_failing_tests | QA | agent |
| 4 | TDD RED | red_gate | - | **gate** |
| 5 | TDD GREEN | implement_tasks | DEV | agent |
| 6 | TDD GREEN | verify_green_state | QA | agent |
| 7 | TDD GREEN | green_gate | - | **gate** |

## Commands

### *prism-loop [prompt]

Start the PRISM workflow loop.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/setup_prism_loop.py" "$ARGUMENTS"
```

The prompt provides context to the SM agent for planning.

**Example:**
```
*prism-loop implement user authentication feature
```

### *prism-approve

Approve the current gate and advance to next phase.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_approve.py"
```

- At `red_gate`: Proceeds to GREEN phase (implementation)
- At `green_gate`: Completes workflow

### *prism-reject

Reject at red_gate and loop back to planning (step 1).

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_reject.py"
```

Only valid at `red_gate`. Use when tests need redesign.

### *prism-status

Check current workflow state.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/prism_status.py"
```

Shows progress through all 7 steps.

### *cancel-prism

Cancel the active workflow.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/prism-loop/scripts/cancel_prism_loop.py"
```

Removes state file and stops the loop.

## TDD Validation

The stop hook validates before advancing:

- **write_failing_tests** → Tests must FAIL (assertion errors, not syntax errors)
- **implement_tasks** → All tests must PASS
- **verify_green_state** → Tests + lint must pass

Claude cannot "think" it's done - the hook runs tests to verify.

## State File

Located at `.claude/prism-loop.local.md`

Tracks:
- `current_step`: Active step
- `current_step_index`: Position (0-6)
- `story_file`: Path to story file (set after draft_story)
- `paused_for_manual`: True at gates

## Integration

The stop hook is registered in `hooks/hooks.json`:

```json
{
  "Stop": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/prism_stop_hook.py"
    }]
  }]
}
```

## Example Session

```bash
# Start workflow
*prism-loop implement login feature

# SM agent runs planning phases automatically
# QA writes failing tests
# Stop hook blocks until tests fail correctly

# At red_gate - approve to continue
*prism-approve

# DEV implements until tests pass
# QA verifies

# At green_gate - complete
*prism-approve

# Done!
```

## Triggers

This skill activates when you mention:
- "prism loop" or "prism workflow"
- "start development cycle"
- "TDD workflow" or "core development cycle"
- "/prism" or "/prism-loop"

---

**Version**: 3.3.0
**Last Updated**: 2025-01-09
