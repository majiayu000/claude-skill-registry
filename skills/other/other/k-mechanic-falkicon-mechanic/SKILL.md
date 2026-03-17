---
name: k-mechanic
description: >
  Context for Mechanic - the WoW addon development hub. Covers the CLI,
  MCP server, dashboard, in-game modules, and MechanicLib. Load this for
  deep understanding of Mechanic tooling.
  Triggers: mechanic, mech, cli, mcp, dashboard, tools, development hub.
---

# Mechanic Development Hub

Mechanic is the unified platform for WoW addon development, providing CLI tools, MCP integration, a web dashboard, and in-game diagnostics.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Mechanic Desktop                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  CLI (mech) │  │ MCP Server  │  │  Dashboard  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────┬───────────────────────────┘
                          │ SavedVariables Sync
┌─────────────────────────▼───────────────────────────┐
│                  !Mechanic Addon                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Console   │  │   Errors    │  │    Tests    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

## MCP Tools (Use These First)

> **MANDATORY**: ALWAYS use MCP tools directly instead of the shell.

| Task | MCP Tool |
|------|----------|
| Env Status | `env.status()` |
| Get Addon Output | `addon.output(agent_mode=true)` |
| Lint Addon | `addon.lint(addon="MyAddon")` |
| Format Addon | `addon.format(addon="MyAddon")` |
| Run Tests | `addon.test(addon="MyAddon")` |
| Sync Addon | `addon.sync(addon="MyAddon")` |
| Search APIs | `api.search(query="*Spell*")` |

## Components

### CLI (`mech`)

Command-line interface for all operations:
- `mech lint <addon>` - Run Luacheck
- `mech format <addon>` - Run StyLua
- `mech test <addon>` - Run Busted tests
- `mech release <addon> <version> "<message>"` - Full release workflow

### MCP Server

Exposes 53 AFD commands as MCP tools for AI agents. All functionality available via `mech call <command>` is also available as MCP tools.

### Dashboard

Web UI at `http://localhost:5173`:
- Real-time SavedVariables sync
- Reload trigger button
- Error/test/console log viewer

### In-Game Modules

The `!Mechanic` addon provides:
- **Console** - Aggregated print output from all registered addons
- **Errors** - BugGrabber integration for Lua error capture
- **Tests** - In-game test results from MechanicLib tests
- **Inspect** - Frame inspector for UI debugging
- **API Bench** - Performance testing for WoW APIs

## MechanicLib Integration

Addons register with Mechanic via MechanicLib:

```lua
local ML = LibStub("MechanicLib")
ML:RegisterAddon("MyAddon", {
    version = "1.0.0",
    Print = function(...) ML:Print("MyAddon", ...) end,
})
```

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| CLI commands | [references/cli-commands.md](references/cli-commands.md) |
| AFD commands | [references/afd-commands.md](references/afd-commands.md) |
| In-game modules | [references/ingame-modules.md](references/ingame-modules.md) |
| MechanicLib | [references/mechaniclib.md](references/mechaniclib.md) |
| Dashboard | [references/dashboard.md](references/dashboard.md) |
