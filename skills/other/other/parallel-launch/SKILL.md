---
name: parallel-launch
description: Decompose a task into independent concerns and execute them through broadly parallel, specialized agent groups. Use when a request involves multiple independent sub-tasks, research across separate domains, or work that can be parallelized across files or modules.
---
# Parallel Launch

Decompose the given task into independent agent groups and execute them in broad parallel.

## Process

1. **Analyze the task** and identify independent concerns that can run concurrently.
   - Each concern must be self-contained: no shared mutable state, no ordering dependency.
   - If concerns have dependencies, sequence the dependent batch after the independent batch completes.
   - Consult [delegation scenarios](./references/delegation-scenarios.md) for parallelism decisions.

2. **Design agent groups** — for each independent concern:
   - Assign a clear, scoped objective (one concern per agent).
   - Select the appropriate agent type (Explore, Plan, general-purpose, or domain specialist).
   - Define expected output format so results can be composed.

3. **Launch all independent agents in a single tool call** — never sequentially when parallel is possible.

4. **Compose results** once all agents complete:
   - Merge non-conflicting outputs directly.
   - For conflicting or overlapping results, reconcile and present trade-offs to the user.
   - If any agent failed or returned incomplete results, report the gap and propose a targeted follow-up.

5. **Review composed output** — dispatch a review agent to verify:
   - **Completeness:** All original concerns addressed, no gaps.
   - **Consistency:** No contradictions between agent outputs.
   - **Accuracy:** Claims are substantiated, sources checked, no hallucinated findings.
   - **Scope:** Nothing extra built beyond what was asked.
   - For implementation work, additionally verify spec compliance and code quality.

6. **Report to user** only after review passes.

## Constraints

- Agents per batch: match the number of truly independent concerns (avoid artificial splitting).
- Each agent prompt must include full context — agents do not share memory.
- Do not launch agents for trivially sequential work (single file, single concern).
- If the task has fewer than 2 independent concerns, execute directly instead of launching agents.

## Red Flags

- **Never skip review.** Composed output must always pass through a review agent before reporting.
- **Never accept unverified composed output.** If agents return conflicting results, the review agent must flag them — not silently pick one.
- **Never report to user before review passes.** The review step is mandatory, not advisory.
