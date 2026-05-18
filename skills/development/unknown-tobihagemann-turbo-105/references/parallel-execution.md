# Parallel Execution in Codex

Codex supports parallel sub-agents via `spawn_agent` and `wait_agent` tools. This works in both interactive and `codex exec` mode.

## How It Works

- **`spawn_agent`** creates a new agent thread with its own conversation context. Returns an agent ID.
- **`wait_agent`** waits for one or more agents to complete and returns their results.
- Sub-agents run concurrently, not blocking the parent.
- The parent can spawn multiple agents, do its own work, then wait for results.

## Gating Rule

The model will not fan out into sub-agents unless the prompt **explicitly requests parallel delegation**. The `spawn_agent` tool description gates itself on explicit user permission:

> "Only use spawn_agent if and only if the user explicitly asks for sub-agents, delegation, or parallel agent work."

Prompts must clearly say to use sub-agents or parallel execution.

## Prompt Pattern

To trigger parallel fan-out, structure the prompt like:

```
Delegate each of the following tasks to a separate sub-agent using spawn_agent so they run in parallel. Wait for all agents to complete, then synthesize their findings into a unified report.

1. [Task A description]
2. [Task B description]
3. [Task C description]
```

Key elements:
- Explicitly mention `spawn_agent` or "sub-agent" or "parallel"
- List the tasks to fan out
- Instruct to wait for all results and synthesize

## Limitations

- **Thread limits**: `agents.max_threads` in codex config caps concurrent sub-agents (Codex default 6; Turbo's `codex/SETUP.md` recommends raising it to 16). The hard ceiling enforced by Codex is 64.
- **Depth limits**: `agents.max_depth` (default 1) prevents unbounded recursion — a sub-agent cannot itself spawn sub-agents under the default config
- **No structured output**: Sub-agents return text via `wait_agent` / `resume_agent` results; there is no schema-typed channel
