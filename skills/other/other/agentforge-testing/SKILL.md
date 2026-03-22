---
name: agentforge-testing
description: Run and extend AgentForge test coverage across packages, CLI flows, runtime behavior, MCP integrations, and dashboard-adjacent logic.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Testing

Use this skill when the change spans packages or touches contract-heavy behavior.

## Expected checks

- package-local Vitest suites,
- cross-package CLI tests,
- `pnpm test`,
- `pnpm typecheck`,
- targeted manual sanity checks for runtime or CLI behavior when relevant.

## References

- Read [test-matrix.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/agentforge-testing/references/test-matrix.md).
