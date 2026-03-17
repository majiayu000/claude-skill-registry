---
name: k-docs
description: >
  Index of Mechanic documentation with summaries and links. Load this
  to understand what documentation exists and where to find detailed
  information on specific topics.
  Triggers: docs, documentation, reference, guide, help.
---

# Documentation Index

Quick reference to all Mechanic documentation.

## Core Documentation

| Document | Path | Summary |
|----------|------|---------|
| **AGENTS.md** | `AGENTS.md` | Agent guidance, project structure, AFD standards |
| **CLAUDE.md** | `CLAUDE.md` | Quick reference for AI assistants |
| **README.md** | `README.md` | Project overview and getting started |
| **CHANGELOG.md** | `CHANGELOG.md` | Version history and release notes |

## Integration Guides

Located in `docs/integration/`:

| Document | Summary |
|----------|---------|
| **mechaniclib.md** | How to integrate addons with MechanicLib |
| **testing.md** | Sandbox, Busted, and in-game testing strategies |
| **console.md** | Structured logging via MechanicLib:Print |
| **errors.md** | BugGrabber integration and error tracking |
| **performance.md** | Profiling and performance baselines |
| **release.md** | Release workflow and changelog format |
| **inspect.md** | Frame inspector usage |
| **troubleshooting.md** | Common issues and solutions |

## Architecture Documentation

| Document | Path | Summary |
|----------|------|---------|
| **addon-architecture.md** | `docs/addon-architecture.md` | Core/Bridge/View layer pattern |
| **addon-integration.md** | `docs/addon-integration.md` | How to integrate with Mechanic |
| **cli-reference.md** | `docs/cli-reference.md` | Full CLI command reference |

## .claude System Documentation

| Document | Path | Summary |
|----------|------|---------|
| **AGENTS.md** | `.claude/AGENTS.md` | Command/skill taxonomy (c-/s-/k-) |

## Skill References

Each skill has its own `references/` folder with deep-dive content:

| Skill | Key References |
|-------|---------------|
| **s-debug** | `error-patterns.md`, `debugging-strategies.md` |
| **s-develop** | `event-patterns.md`, `frame-engineering.md`, `saved-variables.md`, `combat-lockdown.md`, `api-patterns.md` |
| **s-test** | `busted-patterns.md`, `wow-mocking.md` |
| **s-research** | `api-research.md`, `blizzard-ui.md`, `ace3-patterns.md` |
| **k-mechanic** | `cli-commands.md`, `afd-commands.md`, `ingame-modules.md`, `mechaniclib.md`, `dashboard.md` |

## MCP Tool Discovery

Use these MCP tools to explore available functionality:

```
env.status()              # Environment and paths
docs.generate()           # Generate full CLI reference
api.stats()               # API database statistics
fencore.catalog()         # All FenCore functions
```

## Quick Links by Topic

| Topic | Where to Look |
|-------|---------------|
| Getting started | `README.md`, `docs/addon-integration.md` |
| Debugging issues | `s-debug` skill, `docs/integration/troubleshooting.md` |
| Writing tests | `s-test` skill, `docs/integration/testing.md` |
| Releasing addons | `s-release` skill, `docs/integration/release.md` |
| WoW API research | `s-research` skill, `api.search` MCP tool |
| Architecture decisions | `docs/addon-architecture.md` |
