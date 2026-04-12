---
name: ralph-loop
description: "Ralph Wiggum-inspired automation loop for specification-driven development. Orchestrates task implementation, review, cleanup, and synchronization using a Python script. Use when: user runs /loop command, user asks to automate task implementation, user wants to iterate through spec tasks step-by-step, or user wants to run development workflow automation with context window management. One step per invocation. State machine: init → choose_task → implementation → review → fix → cleanup → sync → update_done. Supports --from-task and --to-task for task range filtering. State persisted in fix_plan.json."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---

# Ralph Loop — Python Orchestrator

⚠️ **IMPORTANT**: This skill uses a Python orchestrator script. Do NOT execute arbitrary bash commands. Use `Bash` ONLY to run `ralph_loop.py`. All task commands (like `/specs:task-implementation`) are shown to the user to execute manually.

## Overview

The Ralph Loop applies Geoffrey Huntley's "Ralph Wiggum as a Software Engineer" technique to specification-driven development. It uses a **Python orchestrator script** that manages a state machine: one invocation = one step, state persisted in `fix_plan.json`.

**Key insight**: Implementing + reviewing + syncing in one invocation explodes the context window. Solution: each loop iteration does exactly one step, saves state to `fix_plan.json`, and stops. The next iteration resumes from saved state.

**Key improvement**: The Python script `ralph_loop.py` handles all state management, task selection, and command generation. It does NOT execute task commands directly — it shows you the correct command to execute in your CLI.

## When to Use

- User runs `/loop` command for recurring automation
- User asks to "automate implementation" or "run tasks in loop"
- User wants to "iterate through tasks step-by-step" or "run workflow automation"
- User needs "context window management" across multiple SDD commands
- User wants to "process task range" from TASK-N to TASK-M
- User needs multi-agent support (different CLIs for different tasks)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   ralph_loop.py │────▶│   fix_plan.json │────▶│  User executes  │
│   (orchestrator)│     │   (state file)  │     │  command in CLI │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         │                                               ▼
         │                                      ┌─────────────────┐
         └──────────────────────────────────────│   Task result   │
                                                │   (success/     │
                                                │   failure)      │
                                                └─────────────────┘
```

**One Step Flow:**
1. Run `ralph_loop.py --action=loop`
2. Script reads `fix_plan.json` and determines current step
3. Script shows the command to execute (e.g., `/specs:task-implementation`)
4. User executes the command in their CLI
5. User runs `ralph_loop.py --action=loop` again
6. Script updates state based on result and shows next command

## State Machine

```
fix_plan.json state machine:
┌─────────────────────────────────────────────────────────────┐
│  state: "init"                                            │
│    → --action=start: Initialize fix_plan.json              │
│    → Load tasks from tasks/TASK-*.md files                │
│    → Apply task_range filter                              │
│                                                             │
│  state: "choose_task"                                      │
│    → Pick next pending task (within range, deps satisfied)│
│    → No tasks in range → state: "complete"               │
│    → Task found → state: "implementation"                │
│                                                             │
│  state: "implementation"                                  │
│    → Show /specs:task-implementation command             │
│    → User executes, then runs loop again                  │
│    → Next state: "review"                                │
│                                                             │
│  state: "review"                                          │
│    → Show /specs:task-review command                     │
│    → User reviews results, then runs loop again          │
│    → Issues found → state: "fix" (retry ≤ 3)             │
│    → Clean → state: "cleanup"                            │
│                                                             │
│  state: "fix"                                             │
│    → Show commands to fix issues                         │
│    → User applies fixes, then runs loop again            │
│    → Next state: "review"                                │
│                                                             │
│  state: "cleanup"                                         │
│    → Show /developer-kit-specs:specs-code-cleanup command│
│    → Next state: "sync"                                  │
│                                                             │
│  state: "sync"                                            │
│    → Show /specs:spec-sync-with-code command             │
│    → Next state: "update_done"                           │
│                                                             │
│  state: "update_done"                                     │
│    → Mark task done, commit git changes                  │
│    → Re-evaluate dependencies                            │
│    → state: "choose_task"                                │
│                                                             │
│  state: "complete" | "failed"                            │
│    → Print result, stop                                   │
└─────────────────────────────────────────────────────────────┘
```

## File Location Requirements

**⚠️ CRITICAL**: The `fix_plan.json` file MUST ALWAYS be located in:

```
docs/specs/[ID-feature]/_ralph_loop/fix_plan.json
```

This is enforced by the script to prevent LLMs from creating files in wrong locations.

**Migration**: If you have an old `fix_plan.json` in the root of your spec folder, the script will automatically migrate it to `_ralph_loop/` on first run.

## Instructions

### Phase 1: Initialize

Run the Python script with `--action=start` to scan task files and create `fix_plan.json` in the correct location:

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=start \
  --spec=docs/specs/001-feature/ \
  --from-task=TASK-036 \
  --to-task=TASK-041
```

### Phase 2: Execute Loop Steps

Run the script with `--action=loop` to get the current state and the command to execute:

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=loop \
  --spec=docs/specs/001-feature/
```

The script will show you the exact command to execute for the current step. Execute it in your CLI, then run the loop command again.

### Phase 3: Advance State (Manual)

After executing the shown command, manually advance to the next step:

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=next \
  --spec=docs/specs/001-feature/
```

This updates `fix_plan.json` to the next state (e.g., `implementation` → `review`).

### Phase 4: Monitor Progress

Check status anytime with `--action=status`:

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=status \
  --spec=docs/specs/001-feature/
```

## Quick Start

### 1. Initialize

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=start \
  --spec=docs/specs/001-feature/ \
  --from-task=TASK-036 \
  --to-task=TASK-041 \
  --agent=claude
```

### 2. Run Loop

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=loop \
  --spec=docs/specs/001-feature/
```

The script will show you the command to execute. Run it, then run the loop again.

### 3. Check Status

```bash
python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=status \
  --spec=docs/specs/001-feature/
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--action` | `start` (init), `loop` (run one step), `status`, `resume`, `next` (advance step) |
| `--spec` | Spec folder path (e.g. `docs/specs/001-feature/`) |
| `--from-task` | Start of task range (e.g. `TASK-036`) |
| `--to-task` | End of task range (e.g. `TASK-041`) |
| `--agent` | Default agent: `claude`, `codex`, `copilot`, `kimi`, `gemini`, `glm4`, `minimax` |
| `--no-commit` | Skip git commits (for testing) |

## Step Details

### Step 1: Initialize (`--action=start`)

The script:
1. Scans `tasks/TASK-*.md` files in the spec folder
2. Extracts metadata from YAML frontmatter (id, title, status, lang, dependencies, agent)
3. Applies `--from-task` and `--to-task` filters
4. Creates `fix_plan.json` with full state

### Step 2: Choose Task (`choose_task`)

The script:
1. Finds pending tasks within range
2. Checks dependencies are satisfied
3. Selects next task
4. Updates `fix_plan.json` with `current_task`
5. Shows command to execute

### Step 3: Implementation (`implementation`)

The script shows:
```
→ Implementation: TASK-037

Execute:
  /specs:task-implementation --task=TASK-037

After execution, update state:
  python3 ralph_loop.py --action=loop --spec=docs/specs/001-feature/
```

### Step 4: Review (`review`)

The script shows:
```
→ Review: TASK-037 | Retry: 0/3

Execute:
  /specs:task-review --task=TASK-037

Review the generated review report, then update state:
  python3 ralph_loop.py --action=loop --spec=docs/specs/001-feature/
```

### Step 5: Fix (`fix`) - If Review Failed

If issues found, script shows fix instructions. After fixes, user runs loop again.

### Step 6: Cleanup (`cleanup`)

The script shows:
```
→ Cleanup: TASK-037

Execute:
  /developer-kit-specs:specs-code-cleanup --task=TASK-037
```

### Step 7: Sync (`sync`)

The script shows:
```
→ Sync: TASK-037

Execute:
  /specs:spec-sync-with-code docs/specs/001-feature/ --after-task=TASK-037
```

### Step 8: Update Done (`update_done`)

The script:
1. Marks task as completed in `fix_plan.json`
2. Commits git changes (unless `--no-commit`)
3. Updates iteration count
4. Returns to `choose_task`

## Multi-Agent Support

### Default Agent for All Tasks

```bash
python3 ralph_loop.py --action=start --spec=... --agent=codex
```

### Per-Task Agent

Specify agent in task file YAML frontmatter:

```yaml
---
id: TASK-036
title: Refactor user service
status: pending
lang: java
agent: codex
---
```

Supported agents: `claude`, `codex`, `copilot`, `kimi`, `gemini`, `glm4`, `minimax`

## Using with /loop (Claude Code)

For automatic scheduling every 5 minutes:

```bash
/loop 5m python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=loop \
  --spec=docs/specs/001-feature/
```

This will repeatedly run the loop, showing you the next command each time.

**Note**: The Ralph Loop is now managed directly through the Python script. The deprecated `/specs:ralph-loop` command has been removed.

## Task File Format

Each task should be a separate file: `tasks/TASK-XXX.md`

```markdown
---
id: TASK-036
title: Implement user authentication
status: pending
lang: java
dependencies: []
complexity: medium
agent: claude
---

## Description

Implement JWT-based authentication for the API.

## Acceptance Criteria

- [ ] Login endpoint returns JWT token
- [ ] Token validation middleware
- [ ] Refresh token mechanism
```

## Examples

### Example 1: Basic Usage

```bash
# Initialize
python3 ralph_loop.py --action=start \
  --spec=docs/specs/001-feature/ \
  --from-task=TASK-001 \
  --to-task=TASK-005

# Loop until complete
while true; do
  python3 ralph_loop.py --action=loop --spec=docs/specs/001-feature/
  # Execute the shown command manually
  # Then continue loop
done
```

### Example 2: With Claude Code /loop

```bash
# Start with specific range
/loop 5m python3 plugins/developer-kit-specs/skills/ralph-loop/scripts/ralph_loop.py \
  --action=loop \
  --spec=docs/specs/002-tdd-command \
  --from-task=TASK-001 \
  --to-task=TASK-010
```

### Example 3: Multi-Agent Setup

```bash
# Initialize with Claude as default
python3 ralph_loop.py --action=start \
  --spec=docs/specs/001-feature/ \
  --agent=claude

# Some tasks have "agent: codex" in their frontmatter
# Those will show Codex-formatted commands
```

## Best Practices

- **One step per invocation**: Execute exactly one step, save state, stop
- **Trust the state**: Read from `fix_plan.json`, write to `fix_plan.json`
- **No context accumulation**: State lives in the file, not in context
- **Manual command execution**: The script shows commands; you execute them in your CLI
- **Retry on review failure**: Max 3 retries before failing
- **Range filtering**: Always filter by `task_range`
- **Dependencies first**: Only pick tasks where all dependencies are done
- **Git commits**: The script auto-commits after each completed task

## Constraints and Warnings

- **Context explosion**: Do NOT implement + review + sync in one invocation — context will overflow
- **Max retries**: Review failures retry up to 3 times, then fail
- **Git state**: Ensure clean git state before starting
- **Test infrastructure**: Loop requires tests to pass — without tests, backpressure is ineffective
- **Strict state validation**: Valid `state.step` values are ONLY: `init`, `choose_task`, `implementation`, `review`, `fix`, `cleanup`, `sync`, `update_done`, `complete`, `failed`
- **NO automatic command execution**: The script shows commands but does NOT execute them — you must run them in your CLI

## Troubleshooting

### "fix_plan.json not found"

Run `--action=start` first:
```bash
python3 ralph_loop.py --action=start --spec=docs/specs/001-feature/
```

The script will create `fix_plan.json` in the correct location:
```
docs/specs/001-feature/_ralph_loop/fix_plan.json
```

### "fix_plan.json in wrong location"

If you see a warning about the file being in the wrong location, the script will guide you through migration:

```bash
# Manual migration if needed
mkdir -p docs/specs/001-feature/_ralph_loop
mv docs/specs/001-feature/fix_plan.json docs/specs/001-feature/_ralph_loop/fix_plan.json
```

The script will automatically migrate old files on first run.

### "Invalid spec folder"

Run `--action=start` first:
```bash
python3 ralph_loop.py --action=start --spec=docs/specs/001-feature/
```

### Task files not found

Ensure tasks are in `tasks/TASK-XXX.md` format with YAML frontmatter.

### Wrong agent commands

Check `--agent` parameter or task `agent:` frontmatter field.

## References

- `references/state-machine.md` - Complete state machine documentation
- `references/multi-cli-integration.md` - Multi-CLI setup guide
- `references/loop-prompt-template.md` - Prompt template for shell loops
