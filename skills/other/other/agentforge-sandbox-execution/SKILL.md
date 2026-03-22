---
name: agentforge-sandbox-execution
description: Work on sandbox execution in packages/core, including local, Docker, and E2B providers plus security constraints.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Sandbox Execution

Use this skill for `packages/core/src/sandbox/` and CLI flows that select or configure sandbox providers.

## Focus areas

- provider selection and fallback,
- container pool behavior,
- file and process boundaries,
- security constraints for unsafe execution paths.

## Rules

- Prefer the safest default that still supports the feature.
- Make trust-boundary changes explicit.
- Keep CLI messaging clear when execution is unsandboxed or partially sandboxed.
