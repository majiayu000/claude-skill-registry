---
name: building-mechanics
description: Three.js 3D building system with spatial indexing, structural physics, and multiplayer networking. Use when creating survival games, sandbox builders, or any game with player-constructed structures. Covers performance optimization (spatial hash grids, octrees, chunk loading), structural validation (arcade/heuristic/realistic physics modes), and multiplayer sync (delta compression, client prediction, conflict resolution).
---

# 3D Building Mechanics

Complete building system for Three.js games with performance optimization, structural physics, and multiplayer networking.

## Quick Start

```javascript
import { SpatialHashGrid } from './scripts/spatial-hash-grid.js';
import { HeuristicValidator } from './scripts/heuristic-validator.js';

// Spatial indexing for fast queries
const spatialIndex = new SpatialHashGrid(10);
spatialIndex.insert(piece, piece.position);
const nearby = spatialIndex.queryRadius(position, 15);

// Structural validation (Rust/Valheim style)
const validator = new HeuristicValidator({ mode: 'heuristic' });
validator.addPiece(piece);
const canPlace = validator.validatePlacement(newPiece);
```

## Reference Files

Read these for detailed implementation guidance:

- `references/performance-at-scale.md` - Spatial partitioning, chunk loading, instancing, LOD
- `references/structural-physics-advanced.md` - Arcade vs heuristic vs realistic physics
- `references/multiplayer-networking.md` - Authority models, delta sync, conflict resolution

## Scripts

### Performance (references/performance-at-scale.md)
- `scripts/spatial-hash-grid.js` - O(1) queries for uniform distribution
- `scripts/octree.js` - Adaptive queries for clustered bases
- `scripts/chunk-manager.js` - World streaming for large maps
- `scripts/performance-profiler.js` - Benchmarking utilities

### Structural Physics (references/structural-physics-advanced.md)
- `scripts/heuristic-validator.js` - Fast validation (Fortnite/Rust/Valheim modes)
- `scripts/stability-optimizer.js` - Caching and batch updates
- `scripts/damage-propagation.js` - Damage states, cascading collapse
- `scripts/physics-engine-lite.js` - Optional realistic physics

### Multiplayer (references/multiplayer-networking.md)
- `scripts/delta-compression.js` - Only send changed state
- `scripts/client-prediction.js` - Optimistic placement with rollback
- `scripts/conflict-resolver.js` - Handle simultaneous builds
- `scripts/building-network-manager.js` - Complete server/client system

## Key Patterns

### Spatial Indexing Selection
| Pieces | Distribution | Use |
|--------|-------------|-----|
| <1,000 | Any | Array |
| 1-5k | Uniform | SpatialHashGrid |
| 1-5k | Clustered | Octree |
| 5k+ | Any | ChunkManager + Octree |

### Physics Mode Selection
- **Arcade** (Fortnite): Connectivity only, instant collapse, best for combat
- **Heuristic** (Rust/Valheim): Stability %, predictable, best for survival
- **Realistic**: Full stress/strain, expensive, best for engineering sims

### Multiplayer Pattern
Server-authoritative with client prediction. Use delta compression for sync.
