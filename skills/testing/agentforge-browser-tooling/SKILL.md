---
name: agentforge-browser-tooling
description: Work on browser automation support in AgentForge, including the browser tool abstraction and Playwright-backed execution.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Browser Tooling

Use this skill for browser automation behavior in `packages/core/src/browser-tool.ts` and related CLI or agent surfaces.

## Focus areas

- navigation and action contracts,
- screenshot and extraction behavior,
- sandbox interactions for browser execution,
- reliability and deterministic test patterns.

## Rules

- Prefer stable selectors and explicit action semantics.
- Keep browser capability boundaries clear to agents and users.
- When the change affects execution environment, cross-check sandbox behavior too.
