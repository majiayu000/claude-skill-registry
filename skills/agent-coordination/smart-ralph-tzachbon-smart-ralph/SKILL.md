---
name: smart-ralph
description: Core Smart Ralph skill defining common arguments, execution modes, and shared behaviors across all Ralph plugins.
version: 0.1.0
---

# Smart Ralph

Core skill for all Ralph plugins. Defines common arguments, execution modes, and shared behaviors.

## Common Arguments

All Ralph commands support these standard arguments:

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--quick` | `-q` | Skip interactive phases, auto-generate artifacts, start execution immediately | false |
| `--commit` | `-c` | Commit and push spec/feature files after generation | true (normal), false (quick) |
| `--no-commit` | | Explicitly disable committing files | - |
| `--max-task-iterations` | `-m` | Max retries per failed task before stopping | 5 |
| `--fresh` | `-f` | Force new spec/feature, overwrite if exists | false |

## Argument Parsing Rules

```text
Priority Order (highest to lowest):
1. --no-commit (explicit disable)
2. --commit (explicit enable)
3. --quick mode default (false)
4. Normal mode default (true)
```

### Parsing Logic

```text
commitSpec = true  // default

if "--no-commit" in args:
  commitSpec = false
else if "--commit" in args:
  commitSpec = true
else if "--quick" in args:
  commitSpec = false  // quick mode defaults to no commit
// else keep default (true)
```

## Execution Modes

### Normal Mode (Interactive)

- User reviews artifacts between phases
- Phase transitions require explicit commands
- Each phase sets `awaitingApproval: true`
- Commits spec files by default

### Quick Mode (`--quick`)

- Skips all interactive prompts and interviews
- Auto-generates all artifacts in sequence
- Immediately starts execution after generation
- Does NOT commit by default (use `--commit` to override)
- Still delegates to subagents (delegation is mandatory)

## State File Structure

All Ralph plugins use a state file with common fields:

```json
{
  "phase": "research|requirements|design|tasks|execution",
  "taskIndex": 0,
  "totalTasks": 0,
  "taskIteration": 1,
  "maxTaskIterations": 5,
  "awaitingApproval": false
}
```

Plugins may extend with additional fields.

## Commit Behavior

When `commitSpec` is true:

1. Stage spec/feature files after generation
2. Commit with message: `chore(<plugin>): commit spec files before implementation`
3. Push to current branch

When `commitSpec` is false:

- Files remain uncommitted
- User can manually commit later

## Execution Loop (Self-Contained)

The execution loop is self-contained via the built-in stop-hook. No external plugins are required.

```text
1. Coordinator outputs task delegation prompt
2. Stop-hook detects task completion signals
3. Stop-hook outputs continuation prompt for next task
4. Loop ends when coordinator outputs ALL_TASKS_COMPLETE
```

### Coordinator Prompt

The implement command includes the coordinator prompt inline. The stop-hook (`hooks/scripts/stop-watcher.sh`) reads `.speckit-state.json` to determine continuation behavior.

## Task Completion Protocol

### Executor Signals

| Signal | Meaning |
|--------|---------|
| `TASK_COMPLETE` | Task finished successfully |
| `VERIFICATION_PASS` | Verification task passed |
| `VERIFICATION_FAIL` | Verification failed, needs retry |

### Coordinator Signals

| Signal | Meaning |
|--------|---------|
| `ALL_TASKS_COMPLETE` | All tasks done, end loop |

## Error Handling

### Max Retries

When `taskIteration` exceeds `maxTaskIterations`:

1. Output error with task index and attempt count
2. Include last failure reason
3. Suggest manual intervention
4. Do NOT output ALL_TASKS_COMPLETE
5. Do NOT continue execution

### State Corruption

If state file missing or invalid:

1. Output error with state file path
2. Suggest re-running the implement command
3. Do NOT continue execution

## Branch Management

All Ralph plugins follow consistent branch strategy:

1. Check current branch before starting
2. If on default branch (main/master): prompt for branch strategy
3. If on feature branch: offer to continue or create new
4. Quick mode: auto-create branch, no prompts
