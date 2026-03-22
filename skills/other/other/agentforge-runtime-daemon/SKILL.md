---
name: agentforge-runtime-daemon
description: Work on the persistent Mastra daemon in packages/runtime, including createStandardAgent, daemon lifecycle, environment validation, and runtime channels.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Runtime Daemon

Use this skill for `packages/runtime/`.

## Primary surfaces

- `src/agent/create-standard-agent.ts`
- `src/daemon/daemon.ts`
- `src/channels/http.ts`, `discord.ts`, `telegram.ts`
- runtime tools under `src/tools/`
- environment validation and security helpers

## Rules

- Keep Mastra runtime logic here, not in Convex.
- Reuse `createStandardAgent()` and shared memory setup instead of creating ad hoc agent factories.
- Channel adapters should stream progressively and stay aligned with daemon interfaces.

## References

- Read [runtime-map.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/agentforge-runtime-daemon/references/runtime-map.md).
