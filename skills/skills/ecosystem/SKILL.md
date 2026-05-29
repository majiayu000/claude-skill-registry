---
name: ecosystem
description: View ecosystem updates, tracked repositories, and cross-project status. Use when asked about ecosystem health, repo updates, project status, or what's happening across the codebase.
user-invocable: true
---

# /ecosystem - CYNIC Ecosystem Monitor

*"The pack watches all dens"*

## Quick Start

```
/ecosystem
```

## What It Does

Shows status across the entire ecosystem:
- **Tracked Repos**: GitHub repositories being monitored
- **Recent Updates**: Commits and releases
- **Project Status**: Local project health
- **Cross-Project**: Sync status and drifts

## Views

### Sources (Tracked Repos)
```
/ecosystem sources
```

### Recent Updates
```
/ecosystem updates
```

### Project Status
```
/ecosystem projects
```

### Sync Drifts
```
/ecosystem drifts
```

## Implementation

### Ecosystem Monitor
```javascript
// List tracked sources
brain_ecosystem_monitor({ action: "sources" })

// Get recent updates
brain_ecosystem_monitor({ action: "updates", limit: 20 })

// Fetch new updates
brain_ecosystem_monitor({ action: "fetch", autoAnalyze: true })
```

### Integrator (Cross-Project)
```javascript
// Check project status
brain_integrator({ action: "projects" })

// Find sync drifts
brain_integrator({ action: "drifts" })

// Get sync suggestions
brain_integrator({ action: "suggest" })
```

### Discovery
```javascript
// Scan a repo
brain_discovery({ action: "scan_repo", owner: "zeyxx", repo: "CYNIC" })

// List discovered plugins
brain_discovery({ action: "plugins" })

// Get discovery stats
brain_discovery({ action: "stats" })
```

## Tracked Projects

| Project | Type | Description |
|---------|------|-------------|
| CYNIC | core | This project - the brain |
| HolDex | app | Token quality analyzer |
| GASdf | app | Gasless transactions |
| asdf-brain | service | Legacy plugin |
| claude-mem | service | Memory persistence |

## Update Priorities

| Priority | Meaning |
|----------|---------|
| CRITICAL | Security, breaking changes |
| HIGH | New features, important fixes |
| MEDIUM | Regular updates |
| LOW | Minor changes |
| INFO | Documentation, chores |

## See Also

- `/health` - System health
- `/patterns` - Detected patterns
- [docs/ARCHITECTURE.md](../../../docs/ARCHITECTURE.md) - System architecture
