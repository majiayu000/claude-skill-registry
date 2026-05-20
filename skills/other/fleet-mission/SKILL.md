---
name: fleet-mission
description: Parallel agent fleet dispatch with progress tracking and result aggregation. Launch N agents, monitor completion, merge results. Proven at 7-agent scale.
version: 1.0.0
---

# Fleet Mission

Activates when a task requires launching multiple agents in parallel to cover different aspects of the same work.

## When to Use

- Research requiring 3+ parallel investigation tracks
- Document expansion across multiple files simultaneously
- Fact-checking large document sets
- Data gathering from multiple sources
- Any work that decomposes into independent parallel units

## Dispatch Pattern

```
1. DECOMPOSE work into N independent units
2. LAUNCH agents in a single message (parallel tool calls)
3. Use run_in_background: true for all agents
4. MONITOR — agents report back via task notifications
5. AGGREGATE results as agents complete
6. COMMIT incrementally — don't wait for all to finish
```

## Fleet Sizing

| Work Type | Recommended Fleet | Agent Type |
|-----------|------------------|------------|
| Research (broad topic) | 3-4 agents | general-purpose or gsd-phase-researcher |
| Document expansion | 2-4 agents (split by doc range) | gsd-executor or document-builder |
| Fact-checking | 2 agents (split by doc range) | fact-checker |
| Data gathering | 3 agents (by data domain) | market-researcher |

## Rules

- Maximum 5-6 agents per fleet (diminishing returns beyond that)
- Each agent gets a COMPLETE brief — they have no shared context
- Use worktree isolation for agents that write files
- Commit results incrementally as agents complete — don't batch
- Always have a fallback plan to write directly if an agent fails

## Worktree Management

Agents in worktrees write to isolated copies. After completion:
```bash
cp worktree-path/output/file.md main-repo/output/file.md
```
Then commit from the main repo branch.

## Proven Scale

- 4 parallel document-builder agents: HEL expansion (20K → 79K words)
- 5 parallel deep-research agents: OOPS fleet (5 docs, ~16K words)
- 4 parallel research agents: HEL refinement (He-3, shortage history, Silicon Forest, regulatory)
- 3 parallel data-gathering agents: HEL data fidelity (market, space, PNW)
