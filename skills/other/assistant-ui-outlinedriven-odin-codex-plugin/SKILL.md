---
name: assistant-ui
description: "Build and maintain assistant-ui based React chat apps with reliable setup, runtime selection, LangGraph wiring, tool UI integration, and upgrade workflows. Use when tasks explicitly involve `assistant-ui` dependencies or APIs, including `assistant-ui` CLI commands (`create/init/add/update/upgrade/codemod`), `@assistant-ui/*` providers/runtimes, `AssistantRuntimeProvider`, Thread/Composer primitives, cloud persistence, or tool rendering behavior. Do not use for generic React chat work, backend-only LangGraph tasks, or non-assistant-ui UI work. If the prompt explicitly says without/no/not assistant-ui, do not trigger this skill."
---

# Assistant UI

## Overview

Use this skill to implement or debug assistant-ui integration end to end: CLI setup, runtime wiring, UI primitives, tool UI, and migration-safe upgrades. Load only the reference file needed for the current subtask to keep context focused.

## Workflow

1. Classify the task before coding.
Determine whether the request is setup, runtime wiring, primitives, tools, cloud persistence, or migration.
If the request includes explicit exclusion language (`without/no/not assistant-ui`), stop and do not use this skill.
2. Select runtime and architecture first.
Choose AI SDK, LangGraph, or external-store path before editing components.
3. Apply setup commands with minimum blast radius.
Prefer the smallest CLI operation (`add` for existing projects, `create` for new projects).
4. Wire provider and thread lifecycle.
Ensure `AssistantRuntimeProvider` and runtime hook are configured before Thread/Composer work.
5. Implement tool UI using current APIs.
Prefer `useAui + Tools({ toolkit })` for registration; use `makeAssistantToolUI` for UI-only bindings.
6. Validate and migrate safely.
Run dry-run upgrade checks first, then codemods, then verification.

## Runtime Decision Rules

- Choose AI SDK runtime when backend communication is a chat endpoint and no graph thread state is required.
- Choose LangGraph runtime when thread lifecycle (`initialize/create/load`) and interrupts are required.
- Choose external store runtime when app state is controlled outside assistant-ui.
- Add Assistant Cloud only when persistence, auth-linked thread continuity, or multi-device resume is required.

Load `references/runtime-selection.md` for the matrix and expected outputs.

## Execution Protocol

1. Read `references/setup-and-cli.md` for command sequence and flags.
2. Read exactly one runtime reference.
- Read `references/langgraph-runtime.md` for LangGraph.
- Read `references/runtime-selection.md` for AI SDK or external-store decisions.
3. Read `references/tool-ui-patterns.md` only if tools are in scope.
4. Read `references/cloud-persistence.md` only if cloud is in scope.
5. Read `references/troubleshooting.md` only when failures appear.

## Output Contract

When implementing assistant-ui tasks, deliver these artifacts unless the user scope explicitly excludes them:

- Runtime provider wiring that matches the chosen runtime.
- Thread and composer integration that compiles with the chosen runtime.
- Tool registration and rendering behavior consistent with current APIs.
- Environment variable expectations for cloud flows.
- Upgrade path or migration notes if dependency upgrades are requested.

## Guardrails

- Prefer `Tools({ toolkit })` over legacy registration helpers.
- Use `makeAssistantToolUI` only for UI bindings to already-defined backend tools.
- Keep LangGraph thread handling explicit: `initialize`, `create`, and `load`.
- Execute upgrade sequence in this order: `update --dry` -> `upgrade` -> `codemod` -> test.
- Avoid broad documentation dumps; load only relevant references.
- Do not activate this workflow for comparison-only requests that do not require assistant-ui implementation changes.

## Reference Map

- Setup and CLI: `references/setup-and-cli.md`
- Runtime selection: `references/runtime-selection.md`
- LangGraph runtime wiring: `references/langgraph-runtime.md`
- Tool UI patterns: `references/tool-ui-patterns.md`
- Cloud persistence: `references/cloud-persistence.md`
- Debug and recovery: `references/troubleshooting.md`
