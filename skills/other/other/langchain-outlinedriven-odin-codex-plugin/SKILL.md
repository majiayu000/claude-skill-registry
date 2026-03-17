---
name: langchain
description: "LangChain workflows for `create_agent`, LCEL chains, `bind_tools`, middleware, and structured output with production-safe orchestration. Use when implementing or refactoring LangChain application logic in Python or TypeScript."
---

# LangChain

Use this skill to build or refactor LangChain application logic with predictable tool use, structured outputs, and clean runtime boundaries.

## Quick Triage

- Use this skill when the task is primarily chain/agent composition, tool calling, middleware, output schemas, or prompt wiring.
- Switch to `$langgraph` when the core problem is graph topology, node routing, checkpoints, interrupts, or multi-step state machines.
- Switch to `$ag-ui` when the core problem is event protocol compliance between backend and UI.
- Switch to `$copilotkit` when the core problem is frontend coagent UX, hooks, and runtime provider wiring.

## Workflow

1. Confirm language/runtime surface first.
Choose Python or TypeScript and identify existing package boundaries before code edits.
2. Define the contract before implementation.
Lock input shape, output shape, tool schema, and failure behavior.
3. Choose abstraction level deliberately.
Use simple LCEL chains when tools are not required; use `create_agent` when iterative tool use is needed.
4. Add tools and middleware in a deterministic order.
Validate schema compatibility and tool side effects before adding retries or guardrails.
5. Enforce structured output and state rules.
Use explicit schema validation and avoid ad-hoc parsing.
6. Add observability and limits.
Set timeouts, retries, and tracing hooks before rollout.
7. Verify with focused tests.
Run unit tests for tool bindings and integration tests for end-to-end agent loops.

## Default Patterns

- Prefer explicit tool schemas over implicit argument parsing.
- Keep tool side effects isolated from prompt logic.
- Keep prompt templates and business logic separate.
- Validate all structured outputs at boundaries.
- Keep retries bounded and idempotent.

## Failure Modes

- Tool schema drift between prompt and implementation.
- Unbounded agent loops due to missing stop conditions.
- Silent parsing failures from weak output contracts.
- Middleware order causing policy bypass.
- State growth without trimming/summarization rules.

## Reference Map

Load only what is needed for the current subtask.

- Core workflow patterns: `references/core-workflows.md`
- Tooling and middleware: `references/tooling-and-middleware.md`
- Structured output and state: `references/structured-output-and-state.md`
- Debugging and recovery: `references/troubleshooting.md`
