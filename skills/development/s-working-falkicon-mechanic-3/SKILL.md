---
name: s-work
description: >
  General-purpose skill for Mechanic/Fen ecosystem work. Covers ecosystem context,
  development tools, component overview, and AFD principles. Use for everyday addon
  work, exploration, or when unsure which specialized skill to use.
  Triggers: work, build, develop, create, mechanic, fen, fencore, fenui, ecosystem, addon.
---

# Fen Ecosystem

Expert guidance for working in the Mechanic/Fen WoW addon development ecosystem.

## The Reload Loop (MANDATORY)

After ANY addon code change, you MUST verify the changes in-game:

1. **Ask** the user to `/reload` in WoW (or trigger via keybinding CTRL+SHIFT+R)
2. **Wait** for the user to confirm the reload is complete
3. **Then** use the `addon.output` MCP tool (agent_mode=true) to get errors, tests, and console logs

> **CRITICAL**: Do NOT call `addon.output` immediately after changes. The timing between reload and SavedVariables sync is unpredictable. Always wait for user confirmation before pulling output.

## Ecosystem Components

| Component | Purpose | Key Tools |
|-----------|---------|-----------|
| **Mechanic** | Development hub | `env.status`, `addon.output`, `reload.trigger` |
| **FenCore** | Pure logic library | `fencore.catalog`, `fencore.search`, `fencore.info` |
| **FenUI** | UI widget library | `Layout`, `Panel`, `Tabs`, `Grid`, `Buttons` |
| **MechanicLib** | Bridge library | `RegisterAddon`, `Print`, `RegisterTest` |

## Essential MCP Tools

| Task | MCP Tool |
|------|----------|
| Get Addon Output | `addon.output` (agent_mode=true) |
| Lint Code | `addon.lint` |
| Run Tests | `addon.test` |
| Search APIs | `api.search` |
| Search FenCore | `fencore.search` |
| Env Status | `env.status` |

## AFD Core Principles

Mechanic follows **Agent-First Development (AFD)** — [github.com/Falkicon/afd](https://github.com/Falkicon/afd)

1. **Tool-First**: All functionality must exist as an MCP tool before being added to any UI.
2. **Structured Results**: All tools return predictable JSON schemas with `success`, `data`, and `error`.
3. **Agent Mode**: Use `agent_mode=true` for distilled, AI-optimized output.

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Component details, architecture | [references/components.md](references/components.md) |
| Daily workflows, patterns | [references/workflow.md](references/workflow.md) |
| Quick API reference | [references/quick-api.md](references/quick-api.md) |
| MCP tool reference | [../using-mechanic/references/afd-commands.md](../using-mechanic/references/afd-commands.md) |

