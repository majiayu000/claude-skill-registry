---
name: status
description: Display CYNIC's self-status including packages, tests, integrations, and auto-generated roadmap. Use when asked about development status, project health, what's working, or CYNIC v1 completion.
user-invocable: true
---

# /status - CYNIC Self-Status

*"Connais-toi toi-même, puis vérifie"* - κυνικός

Auto-tracks CYNIC's own development state. Unlike static ROADMAP.md, this is **live truth**.

## Quick Start

```
/status           # Full scan (runs tests ~3min)
/status quick     # Quick scan (cached, no tests)
/status json      # JSON output for processing
```

## What It Shows

1. **Packages** - Test status for all 12 packages
2. **Integrations** - Hooks, skills, agents, MCP status
3. **Features** - Implemented vs missing (derived from tests)
4. **Roadmap** - Auto-generated from actual code state

## Implementation

Run the self-monitor module:

```bash
# Full scan (with tests)
node scripts/lib/self-monitor.cjs

# Quick scan (no tests, uses cache)
node scripts/lib/self-monitor.cjs --quick

# JSON output
node scripts/lib/self-monitor.cjs --json

# Status line only
node scripts/lib/self-monitor.cjs --status
```

## Output Example

```
╔═══════════════════════════════════════════════════════════════════╗
║            🐕 CYNIC SELF-STATUS (Auto-generated)                  ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  PACKAGES: 12/12 healthy
║  TESTS: 1980/1980 passing (100.0%)
║                                                                   ║
║  ✅* core         117/117 tests
║  ✅* protocol     230/230 tests
║  ✅* persistence  179/179 tests
║  ✅  anchor        54/54 tests
║  ✅  burns         75/75 tests
║  ✅* identity      50/50 tests
║  ✅  emergence     43/43 tests
║  ✅* node         614/614 tests
║  ✅* mcp          492/492 tests
║  ✅  holdex        44/44 tests
║  ✅  gasdf         36/36 tests
║  ✅  zk            46/46 tests
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  HOOKS: 5   SKILLS: 12   AGENTS: 13   LIB: 95
║  MCP: healthy
║                                                                   ║
║  ROADMAP: ✅ Core  🔄 Integration  📋 External
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  * = critical package   φ⁻¹ = 61.8% max confidence               ║
╚═══════════════════════════════════════════════════════════════════╝
```

## Data Storage

Results are cached in `~/.cynic/self/`:
- `packages.json` - Package test results
- `integrations.json` - Claude Code integration state
- `features.json` - Feature detection
- `roadmap.json` - Auto-generated roadmap

## Triggering

- **On demand**: Run `/status`
- **Session start**: Can be added to awaken.cjs for startup check
- **Post-commit**: Can be triggered by git hooks

## V1 Completion Criteria

CYNIC v1 is complete when:
- All 6 critical packages healthy (core, protocol, persistence, identity, node, mcp)
- All hooks operational
- All skills accessible
- MCP server healthy

## See Also

- `/health` - CYNIC services health (runtime)
- `/cockpit` - Ecosystem repos overview
- `/ecosystem` - Cross-project status
