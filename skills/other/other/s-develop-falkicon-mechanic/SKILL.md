---
name: s-develop
description: >
  Core WoW addon development patterns using Ace3 framework and Blizzard UI APIs.
  Covers event-driven design, SavedVariables, frame architecture, and API resilience.
  Use when building addons, designing systems, or integrating libraries.
  Triggers: addon, WoW, Lua, Ace3, frame, event, SavedVariables, architecture.
---

# Developing WoW Addons

Expert guidance for building World of Warcraft addons with a focus on testability and maintenance.

## Related Commands

- [c-develop](../../commands/c-develop.md) - Build or extend addon features workflow

## CLI Commands (Use These First)

> **MANDATORY**: Always use CLI commands before manual exploration.

| Task | Command |
|------|---------|
| Create Addon | `mech call addon.create -i '{"name": "MyAddon"}'` |
| Sync Junctions | `mech call addon.sync -i '{"addon": "MyAddon"}'` |
| Validate TOC | `mech call addon.validate -i '{"addon": "MyAddon"}'` |
| Check Libraries | `mech call libs.check -i '{"addon": "MyAddon"}'` |
| Sync Libraries | `mech call libs.sync -i '{"addon": "MyAddon"}'` |

## Capabilities

1. **Event-Driven Design** — Register events, handle callbacks, bucket patterns
2. **Frame Architecture** — Three-layer design (Core/Bridge/View), layouts, templates
3. **SavedVariables** — Database design, AceDB, versioning, defaults
4. **Combat Lockdown** — Protected functions, taint avoidance, secure handlers
5. **API Resilience** — Defensive programming, C_ namespaces, secret values

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Addon architecture, layers | [../../docs/addon-architecture.md](../../docs/addon-architecture.md) |
| Event registration, callbacks | [references/event-patterns.md](references/event-patterns.md) |
| Frame creation, UI engineering | [references/frame-engineering.md](references/frame-engineering.md) |
| SavedVariables, AceDB | [references/saved-variables.md](references/saved-variables.md) |
| Combat lockdown, secure code | [references/combat-lockdown.md](references/combat-lockdown.md) |
| Blizzard API, C_ namespaces | [references/api-patterns.md](references/api-patterns.md) |
| MechanicLib integration | [../../docs/integration/mechaniclib.md](../../docs/integration/mechaniclib.md) |
| Performance profiling | [../../docs/integration/performance.md](../../docs/integration/performance.md) |

## Quick Reference

### Create New Addon
```bash
mech call addon.create -i '{"name": "MyAddon", "author": "Name"}'
mech call addon.sync -i '{"addon": "MyAddon"}'
```

### Core Principles
1. **Headless Core**: Keep logic in pure Lua functions (Layer 1)
2. **Event-Driven**: Avoid `OnUpdate` polling; use events (Layer 2)
3. **Defensive API**: Always check for `nil` and use `pcall` for uncertain APIs
4. **Combat Aware**: Never modify protected frames in combat
