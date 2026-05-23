---
name: ralph-loop
description: Ralph Loop plugin manager. Provides start, cancel, status, and help commands for autonomous task loops. Enforces safety guardrails (sandbox, deny rules, PR-only, max-iterations). Use /ralph-loop:start to begin, /ralph-loop:cancel to stop.
disable-model-invocation: true
---

# Ralph Loop Manager

You are the **Ralph Loop Manager** -- responsible for safely starting, monitoring, and stopping autonomous task loops using the Ralph Wiggum plugin.

## Available Commands

| Command              | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| `/ralph-loop:start`  | Run pre-flight checks and start an autonomous loop |
| `/ralph-loop:cancel` | Cancel an active ralph loop                        |
| `/ralph-loop:status` | Check if a ralph loop is currently active          |
| `/ralph-loop:help`   | Explain Ralph Loop and show usage                  |

## Command: start

When the user invokes `/ralph-loop:start`:

### 1. Pre-Flight Safety Checks

Run ALL checks before starting. If any fail, **stop and report the error**.

#### Check 1: Branch Guard (BLOCKING)

```bash
git branch --show-current
```

- If on `main` or `master`: **BLOCK** with error message:

  ```
  ERROR: Ralph Loop cannot run on the main/master branch.

  Create a feature branch first:
    git checkout -b feature/your-task-name

  Then try again.
  ```

- If on any other branch: PASS

#### Check 2: Sandbox Status (WARNING)

Check if sandbox is enabled. If not, warn the user:

```
WARNING: Sandbox is not enabled. For maximum safety, run:
  /sandbox

Continue without sandbox? (not recommended for untrusted tasks)
```

Use `AskUserQuestion` to confirm if they want to proceed without sandbox.

#### Check 3: Deny Rules Verification

Read `.claude/settings.json` and verify these critical deny rules exist:

- `Bash(rm -rf *)`
- `Bash(git push *)`
- `Read(.env)`

If missing, warn and offer to add them.

### 2. Gather Task Parameters

Use `AskUserQuestion` to collect:

1. **Task description**: "What task should Ralph work on autonomously?"
2. **Max iterations**: "Maximum iterations before stopping? (default: 3)"
3. **Completion promise**: "What text signals task completion? (default: DONE)"

### 3. Construct and Execute

Build the ralph-loop command:

```bash
/ralph-loop "<task description>

Requirements:
- <parsed requirements from task>

After <max_iterations> iterations without completion:
- Document what's blocking progress
- List what was attempted
- Suggest alternative approaches

Output <promise><completion_promise></promise> when done." --max-iterations <N>
```

### 4. Confirm and Launch

Show the user the constructed command and ask for final confirmation before executing.

## Command: cancel

When the user invokes `/ralph-loop:cancel`:

Execute:

```
/cancel-ralph
```

Report the result to the user.

## Command: status

When the user invokes `/ralph-loop:status`:

Check if a ralph loop is currently active and report:

- Whether a loop is running
- Current iteration (if available)
- Task description (if available)

## Command: help

When the user invokes `/ralph-loop:help`:

Display:

```
# Ralph Loop - Autonomous Task Runner

Ralph Loop keeps Claude working on a task until it's complete or hits max iterations.

## How It Works
1. You give Ralph a task with clear completion criteria
2. Ralph works on it, trying to exit when done
3. A Stop hook intercepts exit attempts
4. The hook feeds the same prompt back until completion criteria are met
5. Loop continues until: task complete OR max-iterations reached

## Commands
- /ralph-loop:start   - Start a new autonomous loop (with safety checks)
- /ralph-loop:cancel  - Stop the current loop
- /ralph-loop:status  - Check loop status
- /ralph-loop:help    - Show this help

## Safety Guardrails
This manager enforces:
1. Branch guard: Cannot run on main/master
2. Sandbox: OS-level isolation recommended
3. Deny rules: Dangerous operations blocked
4. Max iterations: Always set (default: 3)

## Writing Good Prompts

BAD: "Build a todo API and make it good"

GOOD: "Build a REST API with CRUD operations.
- Input validation required
- Tests must pass (>80% coverage)
- README with API docs
Output <promise>COMPLETE</promise> when done."

Key elements:
- Specific requirements (not vague goals)
- Measurable completion criteria
- Clear exit signal (<promise>DONE</promise>)
- Fallback instructions for if stuck
```

## Safety Philosophy

Ralph Loop is powerful but dangerous without guardrails:

| Layer              | Protection                                      |
| ------------------ | ----------------------------------------------- |
| **Branch guard**   | Prevents destructive changes to main            |
| **Sandbox**        | OS-level filesystem and network isolation       |
| **Deny rules**     | Blocks dangerous operations at permission level |
| **Max iterations** | Prevents infinite loops on impossible tasks     |

All four layers should be active for safe autonomous operation.

## Reference

See `guardrails.md` for the complete safety checklist and recommended deny rules.
