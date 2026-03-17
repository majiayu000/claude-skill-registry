---
name: implement-agents
description: This skill should be used when the user asks to "implement in parallel", "run phases concurrently", "parallel implement", "implement-agents phase X phase Y", or wants to orchestrate multiple agents running /implement simultaneously.
---

# Implement with Agents

Orchestrate multiple agents to run `/implement` in parallel.

## User Input

ARGUMENTS = $ARGUMENTS

Accept one or more phases, task IDs, or task ranges. Examples:

```bash
# Single (runs one agent)
/implement-agents "Phase 3"
/implement-agents "T011-T014"

# Multiple (runs parallel agents)
/implement-agents "Phase 3" "Phase 5"
/implement-agents "T011-T014" "T018-T023"
```

## Execution Flow

```
/implement-agents "Phase 3" "Phase 5"
              │
              ▼
    ┌─────────────────────┐
    │  Parse Arguments    │
    │  → ["Phase 3",      │
    │     "Phase 5"]      │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │  Spawn Agents       │
    │  (parallel)         │
    └─────────┬───────────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
┌─────────┐      ┌─────────┐
│ Agent A │      │ Agent B │
│         │      │         │
│ Runs:   │      │ Runs:   │
│/implement│      │/implement│
│"Phase 3"│      │"Phase 5"│
└────┬────┘      └────┬────┘
     │                 │
     └────────┬────────┘
              ▼
    ┌─────────────────────┐
    │  Wait & Report      │
    └─────────────────────┘
```

## Step 1: Parse Arguments

Parse ARGUMENTS into a list of work units:

```
Input: "Phase 3" "Phase 5"
Output: ["Phase 3", "Phase 5"]

Input: "Phase 3" "T018-T023"
Output: ["Phase 3", "T018-T023"]

Input: "Phase 3"
Output: ["Phase 3"]
```

## Step 2: Spawn Parallel Agents

For each work unit, spawn a background agent that runs `/implement`:

**CRITICAL**: Use the `Skill` tool to invoke `/implement` within each agent.

```
For each WORK_UNIT in parsed arguments:

  Task(
    subagent_type: "general-purpose",
    description: "Implement {WORK_UNIT}",
    prompt: """
Run /implement for {WORK_UNIT}.

Use the Skill tool:
  skill: "implement"
  args: "{WORK_UNIT}"
""",
    run_in_background: true
  )
```

**IMPORTANT**: Spawn ALL agents in a **single message** with multiple Task tool calls to ensure true parallelism.

## Step 3: Monitor Progress

Check agent progress periodically:

```bash
# Read output files returned by Task tool
tail -100 {output_file_A}
tail -100 {output_file_B}
```

Or use `TaskOutput` with `block: false` for non-blocking status checks.

## Step 4: Wait for Completion

Wait for all agents to finish:

```
TaskOutput(task_id: agent_A_id, block: true, timeout: 600000)
TaskOutput(task_id: agent_B_id, block: true, timeout: 600000)
```

## Step 5: Report Results

After all agents complete, summarize what happened:

```
✅ Phase 3: Complete (T011-T014)
✅ Phase 5: Complete (T018-T023)
```

Optionally check `tasks.md` and `git log` to confirm.

## Error Handling

If an agent fails:

1. **Report which agent failed** and what work unit it was assigned
2. **Show the error** from the agent's output
3. **Check tasks.md** for partial progress
4. **Ask user** how to proceed:
   - Retry failed agent
   - Continue with remaining agents
   - Abort and investigate

## Conflict Detection

Before spawning agents, check for potential conflicts:

```
Phase 3 files: proto/aegis.proto, src/grpc/service.rs
Phase 5 files: src/controller/tools/*.rs

Overlap: None → Safe to parallelize
```

If files overlap, warn the user:

```
⚠️ Phase 3 and Phase 4 both modify src/controller/mcp/manager.rs

Options:
1. Run sequentially (Phase 3 first, then Phase 4)
2. Proceed anyway (may cause merge conflicts)
```

## When to Use

**Good for parallelization:**
- Independent phases touching different files
- Multiple task ranges in different modules
- Large features where throughput matters

**Run sequentially instead (`/implement` twice):**
- Phases with dependencies
- Tasks that modify the same files
- When review between phases is needed

## Example Session

```
User: /implement-agents "Phase 3" "Phase 5"

Claude: Spawning 2 agents in parallel...
- Agent A: /implement "Phase 3"
- Agent B: /implement "Phase 5"

[Waits for completion]

✅ Phase 3: Complete
✅ Phase 5: Complete
```

## Notes

- Each agent runs `/progress` via `/implement`, so no additional progress logging needed
- If an agent fails, its output file shows what went wrong
