---
name: langgraph
description: "LangGraph state-machine design and debugging for `StateGraph`, node/edge routing, checkpoints, `interrupt`, and HITL flows. Use when building or troubleshooting graph-based agents with conditional edges and thread state."
---

# LangGraph

Use this skill to design, implement, and debug LangGraph workflows with explicit state contracts, deterministic routing, and robust interrupt handling.

## Quick Triage

- Use this skill when the task involves graph nodes/edges, conditional routing, checkpointing, thread state, or HITL interrupts.
- Switch to `$langchain` when the task is mostly prompt/tool chain composition without graph-level orchestration.
- Switch to `$ag-ui` when the task is protocol-level event synchronization with a frontend client.
- Switch to `$copilotkit` when the task is CopilotKit provider/hooks/shared-state UI integration.

## Workflow

1. Define state schema first.
Include only fields required for routing, retries, and outputs.
2. Define node contracts.
Each node should have one clear responsibility and explicit input/output assumptions.
3. Define edges and routers.
Map all normal, retry, and terminal paths before implementing node internals.
4. Add persistence strategy.
Choose checkpointer configuration and thread identity contract early.
5. Add interrupt strategy.
Define where human approvals occur and how resume payloads are parsed.
6. Compile and visualize.
Validate graph shape before running large test scenarios.
7. Verify with scenario tests.
Cover pass, retry, skip, and max-retry termination paths.

## Default Patterns

- Keep routing predicates pure and side-effect free.
- Keep node outputs explicit and minimal.
- Use separate nodes for validation vs generation to reduce coupling.
- Route by failure class (recoverable vs terminal) rather than generic “error”.

## Failure Modes

- Implicit state mutations causing routing drift.
- Retry loops without cap or fallback exit.
- Interrupt payload mismatch between backend and UI.
- Missing thread/checkpoint identity causing non-reproducible flows.

## Reference Map

Load only what is needed for the current subtask.

- Graph design patterns: `references/graph-design-patterns.md`
- State and checkpoints: `references/state-and-checkpointing.md`
- HITL interrupts: `references/hitl-interrupts.md`
- Debugging playbook: `references/debugging-playbook.md`
