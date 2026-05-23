---
name: clear-context
description: |
  Automatic context management with graceful handoff to continuation subagent.

  Triggers: context pressure, 80% threshold, auto-clear, context full,
  continuation, session state, checkpoint

  Use when: Context usage approaches 80% during long-running tasks.
  This skill enables automatic continuation without manual /clear.

  The key insight: Subagents have fresh context windows. By delegating
  remaining work to a continuation subagent, we achieve effective "auto-clear"
  without stopping the workflow.
category: conservation
token_budget: 200
progressive_loading: true

hooks:
  PreToolUse:
    - matcher: "Task"
      command: |
        echo "[skill:clear-context] Subagent delegation at $(date)" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/clear-context-audit.log
version: 1.3.5
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [The Auto-Clear Pattern](#the-auto-clear-pattern)
- [Thresholds](#thresholds)
- [Auto-Clear Workflow](#auto-clear-workflow)
- [Integration with Existing Hooks](#integration-with-existing-hooks)
- [Self-Monitoring Pattern](#self-monitoring-pattern)

# Clear Context Skill

## Quick Start

When context pressure reaches critical levels (80%+), invoke this skill to:
1. Save current session state
2. Delegate continuation to a fresh subagent
3. Continue work without manual intervention

```
Skill(conserve:clear-context)
```

## When to Use

- **Proactively**: Before starting large multi-chained tasks
- **Reactively**: When context warning indicates 80%+ usage
- **Automatically**: Integrated into long-running workflows

## The Auto-Clear Pattern

Since `/clear` requires user action, we achieve automatic context clearing without interruption through **subagent delegation**:

```
Main Agent (high context)
    ↓
    Saves state to .claude/session-state.md
    ↓
    Spawns continuation subagent (fresh context)
    ↓
    Subagent reads state, continues work
```

## Thresholds

| Level | Threshold | Action |
|-------|-----------|--------|
| WARNING | 40% | Monitor, plan optimization |
| CRITICAL | 50% | Prepare for handoff |
| EMERGENCY | 80% | **Execute auto-clear now** |

**Configuration** (environment variables):
- `CONSERVE_EMERGENCY_THRESHOLD`: Override 80% default (e.g., `0.75` for 75%)
- `CONSERVE_SESSION_STATE_PATH`: Override `.claude/session-state.md` default

## Auto-Clear Workflow

### Step 1: Assess Current State

Before triggering auto-clear, gather:
- Current task/goal description
- Progress made so far
- Key decisions and rationale
- Files being actively worked on
- Open TodoWrite items

### Step 2: Save Session State

**IMPORTANT**: If `.claude/session-state.md` already exists, you MUST Read it first before writing (Claude Code requires reading existing files before overwriting). Create the `.claude/` directory if it doesn't exist.

Write to `.claude/session-state.md` (or `$CONSERVE_SESSION_STATE_PATH`):

```markdown
# Session State Checkpoint
Generated: [timestamp]
Reason: Context threshold exceeded (80%+)

## Execution Mode

**Mode**: [unattended | interactive | dangerous]
**Auto-Continue**: [true | false]
**Source Command**: [do-issue | execute-plan | etc.]
**Remaining Tasks**: [list of pending items]

> **CRITICAL**: If `auto_continue: true` or mode is `dangerous`/`unattended`,
> the continuation agent MUST NOT pause for user confirmation.
> Continue executing all remaining tasks until completion.

## Current Task
[What we're trying to accomplish]

## Progress Summary
[What's been done so far]

## Key Decisions
- Decision 1: [rationale]
- Decision 2: [rationale]

## Active Files
- path/to/file1.py - [status]
- path/to/file2.md - [status]

## Pending TodoWrite Items
- [ ] Item 1
- [ ] Item 2

## Continuation Instructions
[Specific next steps for the continuation agent]
```

**Execution Mode Detection**:

Before writing state, detect the execution mode:

```python
# Detect execution mode from environment/context
execution_mode = {
    "mode": "interactive",  # default
    "auto_continue": False,
    "source_command": None,
    "remaining_tasks": [],
    "dangerous_mode": False
}

# Check for dangerous/unattended mode indicators
if os.environ.get("CLAUDE_DANGEROUS_MODE") == "1":
    execution_mode["mode"] = "dangerous"
    execution_mode["auto_continue"] = True
    execution_mode["dangerous_mode"] = True
elif os.environ.get("CLAUDE_UNATTENDED") == "1":
    execution_mode["mode"] = "unattended"
    execution_mode["auto_continue"] = True

# Inherit from parent session state if exists
if parent_state and parent_state.get("execution_mode"):
    execution_mode = parent_state["execution_mode"]
```

### Step 3: Spawn Continuation Agent

Use the Task tool to delegate. **CRITICAL**: Include execution mode in the task prompt:

```
Task: Continue the work from session checkpoint

Instructions:
1. Read .claude/session-state.md for full context
2. Check the "Execution Mode" section FIRST
3. If `auto_continue: true` or mode is `dangerous`/`unattended`:
   - DO NOT pause for user confirmation
   - Continue executing ALL remaining tasks until completion
   - Only stop on actual errors or when all work is done
4. Verify understanding of current task and progress
5. Continue from where the previous agent left off
6. If you also approach 80% context, repeat this handoff process
   - PRESERVE the execution mode when creating your own checkpoint

The session state file contains all necessary context to continue without interruption.

**EXECUTION MODE INHERITANCE**: You MUST inherit and propagate the execution
mode from the session state. If the parent was in dangerous/unattended mode,
you are also in that mode. Do not ask the user for confirmation.
```

**For batch/multi-issue workflows** (e.g., `/do-issue 42 43 44`):

```
Task: Continue batch processing from session checkpoint

Instructions:
1. Read .claude/session-state.md for full context
2. EXECUTION MODE: This is a batch operation with auto_continue=true
3. Process ALL remaining tasks in the queue:
   - Remaining: [issue #43, issue #44]
4. DO NOT stop between tasks - continue until all are complete
5. If you hit 80% context, hand off with the same execution mode
6. Only pause for:
   - Actual errors requiring human judgment
   - Completion of ALL tasks

This is an unattended batch operation. Continue without user prompts.
```

### Step 4: Graceful Exit

After spawning continuation agent:
- Report that handoff is complete
- Provide link to session state for reference
- Exit current task (subagent continues)

## Integration with Existing Hooks

This skill works with `context_warning.py` hook:

1. Hook fires on PreToolUse
2. At 80%+ threshold, hook injects emergency guidance
3. Guidance recommends invoking this skill
4. Skill executes auto-clear workflow

## Module Loading

For detailed session state format and examples:
- See `modules/session-state.md` for checkpoint format and handoff patterns

## Self-Monitoring Pattern

For workflows that might exceed context, add periodic checks:

```python
# Pseudocode for context-aware workflow
def long_running_task():
    for step in task_steps:
        execute_step(step)

        # Check context after each major step
        if estimate_context_usage() > 0.80:
            invoke_skill("conserve:clear-context")
            return  # Continuation agent takes over
```

## Estimation Without CLAUDE_CONTEXT_USAGE

If the environment variable isn't available, estimate using:

1. **Turn count heuristic**: ~5-10K tokens per complex turn
2. **Tool invocation count**: Heavy tool use = faster context growth
3. **File read tracking**: Large files consume significant context

```python
def estimate_context_pressure():
    """Rough estimation when env var unavailable."""
    # Heuristics (tune based on observation)
    turns_weight = 0.02  # Each turn ~2% of typical context
    file_reads_weight = 0.05  # Each file read ~5%

    estimated = (turn_count * turns_weight) + (file_reads * file_reads_weight)
    return min(estimated, 1.0)
```

## Example: Brainstorm with Auto-Clear

```markdown
## Brainstorm Session with Context Management

1. Before starting, note current context level
2. Set checkpoint after each brainstorm phase:
   - Problem definition checkpoint
   - Constraints checkpoint
   - Approaches checkpoint
   - Selection checkpoint

3. If context exceeds 80% at any checkpoint:
   - Save brainstorm state
   - Delegate to continuation agent
   - Agent continues from checkpoint
```

## Best Practices

1. **Checkpoint Frequently**: During long tasks, save state at natural breakpoints
2. **Clear Instructions**: Continuation agent needs specific, actionable guidance
3. **Verify Handoff**: Ensure state file is written before spawning subagent
4. **Monitor Recursion**: Continuation agents can also hit limits - design for chaining

## Troubleshooting

### Continuation agent doesn't have full context
- Ensure session-state.md is comprehensive
- Include all relevant file paths
- Document implicit assumptions

### Subagent fails to continue properly
- Check that state file path is correct
- Verify file permissions
- Add more specific continuation instructions

### Context threshold not detected
- CLAUDE_CONTEXT_USAGE may not be set
- The `context_warning` hook uses fallback estimation from session file size
- Manual invocation always works

## Hook Integration

This skill is triggered automatically by the **context_warning hook** (`hooks/context_warning.py`):

- **40% usage**: WARNING - plan optimization soon
- **50% usage**: CRITICAL - immediate optimization required
- **80% usage**: EMERGENCY - this skill should be invoked immediately

The hook monitors context via:
1. `CLAUDE_CONTEXT_USAGE` environment variable (when available)
2. Fallback: estimates from session JSONL file size (~800KB = 100%)

Configure thresholds via environment:
- `CONSERVE_EMERGENCY_THRESHOLD`: Override 80% default (e.g., "0.75")
- `CONSERVE_CONTEXT_ESTIMATION`: Set to "0" to disable fallback
- `CONSERVE_CONTEXT_WINDOW_BYTES`: Override 800000 byte estimate
