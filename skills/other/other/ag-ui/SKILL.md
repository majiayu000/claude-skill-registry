---
name: ag-ui
description: "AG-UI protocol implementation guidance for event ordering (`RUN_STARTED`, `TOOL_CALL_*`, `STATE_SNAPSHOT`/`STATE_DELTA`), streaming semantics, and middleware patterns. Use when integrating agent backends with AG-UI clients."
---

# AG-UI

Use this skill to implement AG-UI compliant integrations with correct event ordering, tool lifecycle behavior, and state synchronization semantics.

## Quick Triage

- Use this skill when the task is protocol-level integration between agent backend and UI client.
- Switch to `$langgraph` when graph orchestration/checkpoint logic is the primary issue.
- Switch to `$langchain` when chain or tool orchestration internals are the primary issue.
- Switch to `$copilotkit` when CopilotKit hooks/provider behavior is primary.

## Workflow

1. Define integration mode.
Choose client-side `HttpAgent`, custom `AbstractAgent`, or middleware bridge.
2. Lock event subset and ordering.
Map required lifecycle, text, tool, and state events before implementation.
3. Implement lifecycle first.
Guarantee `RUN_STARTED` and `RUN_FINISHED/RUN_ERROR` framing around all runs.
4. Implement message and tool streams.
Ensure tool call start/args/end/result sequence is valid and complete.
5. Implement state synchronization.
Choose snapshot-only, delta-only, or hybrid strategy intentionally.
6. Add middleware with explicit order.
Enforce auth, filtering, and logging without mutating protocol invariants.
7. Validate against event traces.
Use deterministic replay to confirm ordering and payload shape.

## Default Patterns

- Emit minimal valid event streams rather than custom ad-hoc payloads.
- Keep tool result payloads parseable and bounded.
- Prefer explicit event schemas over inferred client parsing.
- Keep protocol payloads transport-agnostic.

## Failure Modes

- Out-of-order lifecycle or tool events.
- Partial tool-call streams without terminal result events.
- State delta application mismatch on client.
- Middleware mutating payloads into non-compliant shapes.

## Reference Map

Load only what is needed for the current subtask.

- Event contracts: `references/event-contracts.md`
- State sync strategy: `references/state-sync.md`
- Middleware usage: `references/middleware-patterns.md`
- Integration checklist: `references/integration-checklist.md`
