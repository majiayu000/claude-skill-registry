---
name: cockpit
description: Display full ecosystem cockpit with dependency graph, repo health, and proactive alerts. The airplane cockpit that sees everything across all repos.
user-invocable: true
---

# /cockpit - CYNIC Ecosystem Cockpit

*"Le cockpit qui voit tout"* - The cockpit that sees everything

## Quick Start

```
/cockpit
```

## What It Does

Provides omniscient awareness across the entire ecosystem:

- **Repo Health**: Status of all repos in /workspaces
- **Dependencies**: Inter-repo dependency graph
- **Alerts**: Proactive warnings (uncommitted changes, drift, conflicts)
- **Summary**: Unified ecosystem metrics

## Views

### Full Status (default)
```
/cockpit
```

### Alerts Only
```
/cockpit alerts
```

### Dependencies
```
/cockpit deps
```

### Single Repo
```
/cockpit GASdf
```

## Implementation

The cockpit runs automatically at session start (via `awaken.cjs`) and stores state in `~/.cynic/cockpit/`.

### Manual Scan

To run a fresh scan:

```javascript
// In hooks/lib context
const cockpit = require('./scripts/lib/cockpit.cjs');
const state = cockpit.fullScan();
console.log(cockpit.formatCockpitStatus(state));
```

### Read Cached State

```javascript
const state = cockpit.getCockpitState();
```

## Data Files

| File | Purpose |
|------|---------|
| `status.json` | Full ecosystem scan results |
| `alerts.json` | Active alerts (TTL: 1 hour) |
| `dependencies.json` | Dependency graph |

## Repo Health States

| State | Icon | Meaning |
|-------|------|---------|
| healthy | ✅ | Clean, on main, up to date |
| warning | ⚠️ | Uncommitted changes or behind remote |
| critical | 🔴 | Major issues needing attention |
| unknown | ❓ | Not a git repo or scan failed |

## Alert Types

| Type | Trigger |
|------|---------|
| `health_critical` | Repo in critical state |
| `uncommitted_changes` | >10 modified files in critical repo |
| `behind_remote` | >5 commits behind origin |
| `non_main_branch` | Critical repo not on main |
| `dependency_issue` | Circular dependency detected |

## Ecosystem Knowledge

The cockpit knows about these core repos:

| Repo | Role | Critical |
|------|------|----------|
| CYNIC-new | core brain | ✅ |
| GASdf | gasless infra | ✅ |
| HolDex | K-Score oracle | ✅ |
| asdf-brain | legacy proto | ❌ |
| asdf-manifesto | philosophy | ❌ |

## φ-Alignment

- Scan interval: 61.8 seconds (φ × 100ms × 618)
- Alert TTL: 1 hour
- Max alerts: 100

## See Also

- `/health` - CYNIC services health
- `/ecosystem` - Tracked repo updates
- `/patterns` - Detected patterns
