---
name: k-ecosystem
description: >
  Context for the Mechanic/Fen WoW addon development ecosystem. Covers all
  components (Mechanic, FenCore, FenUI, MechanicLib), their relationships,
  and AFD principles. Load this at the start of addon work.
  Triggers: ecosystem, fen, fencore, fenui, mechanic, addon, context.
---

# Fen Ecosystem

The Mechanic/Fen ecosystem is a unified platform for WoW addon development.

## The Reload Loop (MANDATORY)

After ANY addon code change, you MUST verify the changes in-game:

1. **Ask** the user to `/reload` in WoW (or trigger via keybinding CTRL+SHIFT+R)
2. **Wait** for the user to confirm the reload is complete
3. **Then** use the `addon.output` MCP tool (agent_mode=true) to get errors, tests, and console logs

> **CRITICAL**: Do NOT call `addon.output` immediately after changes. The timing between reload and SavedVariables sync is unpredictable. Always wait for user confirmation.

## Ecosystem Components

| Component | Purpose | Key Tools |
|-----------|---------|-----------|
| **Mechanic** | Development hub (CLI, MCP, Dashboard) | `env.status`, `addon.output`, `addon.lint`, `addon.test` |
| **FenCore** | Pure logic library (no UI dependencies) | `fencore.catalog`, `fencore.search`, `fencore.info` |
| **FenUI** | UI widget library (frames, layouts) | `Layout`, `Panel`, `Tabs`, `Grid`, `Buttons` |
| **MechanicLib** | Bridge library (addon ↔ Mechanic) | `RegisterAddon`, `Print`, `RegisterTest` |

## Component Relationships

```
┌─────────────────────────────────────────────────────┐
│                    Your Addon                        │
├─────────────────────────────────────────────────────┤
│  Core Layer     │  Bridge Layer   │  View Layer     │
│  (Pure Logic)   │  (Events/Data)  │  (UI Frames)    │
│                 │                 │                 │
│  Uses: FenCore  │  Uses: Ace3     │  Uses: FenUI    │
└─────────────────────────────────────────────────────┘
         │                 │                 │
         └────────────┬────┴─────────────────┘
                      │
              ┌───────▼───────┐
              │  MechanicLib  │  (Registers addon with Mechanic)
              └───────┬───────┘
                      │
              ┌───────▼───────┐
              │   Mechanic    │  (Development hub)
              └───────────────┘
```

## Essential MCP Tools

| Task | MCP Tool |
|------|----------|
| Get Addon Output | `addon.output(agent_mode=true)` |
| Lint Code | `addon.lint(addon="MyAddon")` |
| Run Tests | `addon.test(addon="MyAddon")` |
| Search APIs | `api.search(query="*Spell*")` |
| Search FenCore | `fencore.search(query="clamp")` |
| Env Status | `env.status()` |

## AFD Core Principles

Mechanic follows **Agent-First Development (AFD)** — [github.com/Falkicon/afd](https://github.com/Falkicon/afd)

1. **Tool-First**: All functionality exists as an MCP tool before any UI
2. **Structured Results**: Tools return predictable JSON with `success`, `data`, `error`
3. **Agent Mode**: Use `agent_mode=true` for AI-optimized output

## Related Knowledge

- [k-mechanic](../k-mechanic/SKILL.md) - Deep dive into Mechanic tools
- [k-fencore](../k-fencore/SKILL.md) - FenCore library details
- [k-fenui](../k-fenui/SKILL.md) - FenUI widget library
