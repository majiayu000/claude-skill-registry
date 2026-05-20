---
name: agentforge-a2a
description: Work on Agent-to-Agent protocol support, registry behavior, and delegation flows in packages/core.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge A2A

Use this skill for the A2A surfaces in `packages/core/src/a2a/`.

## Focus areas

- client and server protocol contracts,
- registry behavior,
- streaming and delegation semantics,
- security boundaries around which agents may call which peers.

## Rules

- Keep protocol shapes explicit and typed.
- Preserve streaming semantics when extending delegation flows.
- Audit allowlist and trust assumptions before broadening access.
