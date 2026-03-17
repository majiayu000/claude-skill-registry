---
name: copilotkit
description: "CopilotKit integration patterns for providers, runtime wiring, `useCoAgent`, `useCopilotAction`, `useLangGraphInterrupt`, shared state, and HITL with LangGraph. Use when building agent-native product UX."
---

# CopilotKit

Use this skill to implement CopilotKit-based agent UX with correct provider wiring, runtime selection, shared state, frontend actions, and interrupt handling.

## Quick Triage

- Use this skill for CopilotKit provider setup, runtime endpoints, hooks, shared-state rendering, and human-in-the-loop UX.
- Switch to `$langgraph` when backend graph behavior is the main issue.
- Switch to `$ag-ui` when protocol event compliance is the main issue.
- Switch to `$langchain` when core model/tool orchestration logic is the main issue.

## Workflow

1. Choose runtime topology.
Decide LangGraph platform endpoint vs remote backend runtime before UI edits.
2. Configure provider boundary.
Set `<CopilotKit>` provider and runtime endpoint settings first.
3. Select hooks by responsibility.
Use `useCoAgent` for state coupling, `useCopilotAction` for frontend actions, and interrupt hooks for HITL flow.
4. Define shared state contract.
Separate input/output/internal state and keep serialization stable.
5. Implement HITL path.
Map interrupt payloads to explicit frontend action handlers.
6. Implement persistence behavior.
Choose thread/message persistence strategy and ensure resume consistency.
7. Validate end-to-end UX.
Test streaming, tool visibility, shared-state render, and resume flow.

## Default Patterns

- Keep runtime and UI concerns separated.
- Keep shared-state schema explicit and minimal.
- Keep action handlers idempotent.
- Treat interrupts as typed control flow, not free-form messages.

## Failure Modes

- Endpoint mismatch (wrong runtime URL/type).
- Hooks bound to wrong agent name or provider scope.
- Shared-state updates not reflected due schema mismatch.
- Interrupt action handlers not wired to expected payload type.

## Reference Map

Load only what is needed for the current subtask.

- Runtime and provider setup: `references/runtime-and-provider.md`
- Hooks and actions: `references/hooks-and-actions.md`
- CoAgents and shared state: `references/coagents-shared-state.md`
- HITL and troubleshooting: `references/hitl-and-troubleshooting.md`
