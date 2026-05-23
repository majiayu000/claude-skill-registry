---
name: Resource Budgets
description: |
  This skill provides resource budget planning for Nethercore ZX games. Use when the user asks about "budget", "ROM size", "RAM limit", "VRAM", "memory", "size limits", "how much space", "resource planning", or "state snapshot".

  **Load references when:**
  - Genre-specific budgets → `references/genre-budgets.md`
version: 1.0.0
---

# Resource Budgets for Nethercore ZX

## Console Limits

| Resource | Hard Limit | Typical | Warning |
|----------|------------|---------|---------|
| **ROM Total** | 16 MB | 8-12 MB | > 12 MB |
| **WASM Code** | 4 MB | 0.5-2 MB | > 2 MB |
| **Data Pack** | 12 MB | 4-10 MB | > 10 MB |
| **RAM** | 4 MB | 1-3 MB | > 3 MB |
| **VRAM** | 4 MB | 2-4 MB | > 3.5 MB |
| **State Snapshot** | - | 50-150 KB | > 200 KB |

## Data Pack Budget

Typical allocation (12 MB max):

| Asset Type | Percentage | Budget |
|------------|------------|--------|
| Textures | 40-60% | 4.8-7.2 MB |
| Meshes | 20-30% | 2.4-3.6 MB |
| Audio | 10-20% | 1.2-2.4 MB |
| Animations | 5-15% | 0.6-1.8 MB |

## State Snapshot Sizing

For rollback netcode:

| Size | Frame Budget | Status |
|------|--------------|--------|
| < 50 KB | < 1ms | Excellent |
| 50-100 KB | 1-2ms | Good |
| 100-200 KB | 2-4ms | Acceptable |
| > 200 KB | > 4ms | **Optimize** |

## Quick Size Estimation

```
Texture: width × height × 0.5 bytes (BC7)
Mesh: vertices × 12-40 bytes (format dependent)
Audio: seconds × 44100 bytes (22050Hz mono)
XM Music: 50-200 KB per song
```

## Build Analysis

```bash
nether build --verbose
```

Use the **build-analyzer** agent for detailed breakdown.
