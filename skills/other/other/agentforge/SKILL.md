---
name: agentforge
description: Index skill for working in the AgentForge monorepo. Routes to runtime, CLI, dashboard, MCP, channels, testing, template sync, and Convex/Mastra skills.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Repo Skills

Use this as the entrypoint for work in this repository.

## Route by subsystem

- `agentforge-runtime-daemon`: `packages/runtime/`, daemon lifecycle, standard agents, HTTP/Discord/Telegram channels.
- `agentforge-cli`: `packages/cli/`, command behavior, scaffolding, local dev flows.
- `agentforge-dashboard`: `packages/web/`, TanStack Router dashboard and Convex-backed UI flows.
- `agentforge-mcp-integration`: MCP client/server work, dynamic tool loading, connection UX, recommended external MCPs.
- `agentforge-skills-marketplace`: skill discovery, install flow, parser/registry/marketplace behavior.
- `agentforge-channel-adapters`: Slack, Discord, Telegram, WhatsApp adapters and runtime channels.
- `agentforge-a2a`: agent-to-agent protocol, registry, and delegation flows.
- `agentforge-sandbox-execution`: sandbox manager, Docker/E2B/local execution, and security boundaries.
- `agentforge-browser-tooling`: browser tool behavior and Playwright-backed automation surfaces.
- `agentforge-research-orchestrator`: research orchestration and multi-tool synthesis flows.
- `agentforge-testing`: Vitest coverage across packages, integration checks, QA gates.
- `agentforge-template-sync`: template source of truth and sync workflow.
- `convex`: Convex data-layer work.
- `mastra`: Mastra-specific runtime work.

## Always align with

- [CLAUDE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/CLAUDE.md)
- [AGENTS.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/AGENTS.md)
- [docs/TECH-REFERENCE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/docs/TECH-REFERENCE.md)
