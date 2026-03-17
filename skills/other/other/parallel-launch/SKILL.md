---
name: parallel-launch
description: Decompose a task into independent concerns and execute them through aggressively parallel, specialized agent groups. Use when a request involves multiple independent sub-tasks, research across separate domains, or work that can be parallelized across files or modules.
---
# Parallel Launch

Decompose the given task into independent agent groups and execute them in maximum parallel.

## Process

1. **Analyze the task** and identify independent concerns that can run concurrently.
   - Each concern must be self-contained: no shared mutable state, no ordering dependency.
   - If concerns have dependencies, sequence the dependent batch after the independent batch completes.

2. **Design agent groups** — for each independent concern:
   - Assign a clear, scoped objective (one concern per agent).
   - Select the appropriate agent type (Explore, Plan, general-purpose, or domain specialist).
   - Define expected output format so results can be composed.

3. **Launch all independent agents in a single tool call** — never sequentially when parallel is possible.

4. **Compose results** once all agents complete:
   - Merge non-conflicting outputs directly.
   - For conflicting or overlapping results, reconcile and present trade-offs to the user.
   - If any agent failed or returned incomplete results, report the gap and propose a targeted follow-up.

## Constraints

- Maximum agents per batch: match the number of truly independent concerns (avoid artificial splitting).
- Each agent prompt must include full context — agents do not share memory.
- Do not launch agents for trivially sequential work (single file, single concern).
- If the task has fewer than 2 independent concerns, execute directly instead of launching agents.
