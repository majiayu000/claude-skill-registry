---
name: dev-patterns-coverage-tracking
description: Grid-based surface coverage tracking for territorial game mechanics
category: patterns
---

# Coverage Tracking Pattern

> "Territory control through paint coverage – grid-based tracking with overlap correction."

## When to Use This Skill

Use when:
- Implementing territorial control mechanics (Splatoon-style)
- Tracking surface coverage percentage
- Calculating team scores based on painted area
- Detecting "painted over" scenarios (team B painting over team A)
- Performance matters (cannot track every individual decal)

## Quick Start

```tsx
// Grid-based coverage tracking
const GRID_SIZE = 5; // 5-unit grid cells

interface SurfacePaintData {
  paintedArea: Record<string, number>; // { teamId: area }
  totalArea: number;
  grid: Map<string, { teamId: string; area: number }>;
}

function getGridKey(x: number, z: number): string {
  const gx = Math.floor(x / GRID_SIZE);
  const gz = Math.floor(z / GRID_SIZE);
  return `${gx},${gz}`;
}

function recordPaint(
  data: SurfacePaintData,
  x: number,
  z: number,
  radius: number,
  teamId: string
) {
  const key = getGridKey(x, z);
  const existing = data.grid.get(key);

  // Calculate new paint area (circle)
  const newArea = Math.PI * radius * radius;

  if (existing) {
    // Overlap: subtract previous team's contribution
    data.paintedArea[existing.teamId] -= existing.area;
  }

  // Add to new team
  data.paintedArea[teamId] = (data.paintedArea[teamId] || 0) + newArea;

  // Update grid
  data.grid.set(key, { teamId, area: newArea });
}
```

## Decision Framework

| Approach                    | Accuracy | Performance | Best For                     |
| --------------------------- | -------- | ----------- | ---------------------------- |
| Per-pixel render target     | 100%     | Slow        | Small maps, offline render   |
| Grid-based (coarse)         | ~80%     | Fast        | Large maps, real-time        |
| Grid-based (fine)           | ~95%     | Medium      | Medium maps, real-time       |
| Per-triangle                | ~90%     | Very Slow   | Low-poly meshes only         |

**Recommendation:** Grid-based with grid size ~1-5 units depending on map scale.

## Data Structures

```tsx
// Grid cell key: "x,z" coordinates
type GridKey = string;

// Grid cell value
interface GridCell {
  teamId: string;  // 'orange' | 'blue'
  area: number;    // Painted area in this cell
}

// Surface data
interface SurfacePaintData {
  grid: Map<GridKey, GridCell>;
  paintedArea: Record<string, number>; // { [teamId]: totalArea }
  totalArea: number;  // Total surface area (for percentage calc)
  lastUpdate: number; // Timestamp
}
```

## Overlap Correction

When paint is applied to an already-painted area, we must:
1. Subtract the old team's contribution
2. Add the new team's contribution

```tsx
// Overlap handling
private _applyPaintToSurface(
  surfaceData: SurfacePaintData,
  worldPos: THREE.Vector3,
  radius: number,
  teamId: string
): void {
  const gridKey = this._getGridKey(worldPos.x, worldPos.z);
  const existing = surfaceData.grid.get(gridKey);

  const paintArea = Math.PI * radius * radius;

  if (existing && existing.teamId !== teamId) {
    // Different team - subtract their area first
    surfaceData.paintedArea[existing.teamId] -= existing.area;
  }

  // Add to new team (or same team - no change needed)
  if (!existing || existing.teamId !== teamId) {
    surfaceData.paintedArea[teamId] =
      (surfaceData.paintedArea[teamId] || 0) + paintArea;

    surfaceData.grid.set(gridKey, { teamId, area: paintArea });
  }
}
```

## Coverage Calculation

```tsx
interface CoverageResult {
  coverage: Record<string, number>; // { [teamId]: percentage }
  leadingTeam: string | null;
  timestamp: number;
}

function calculateCoverage(
  surfaces: SurfacePaintData[]
): CoverageResult {
  const totals: Record<string, number> = {};
  let totalPainted = 0;

  surfaces.forEach(surface => {
    Object.entries(surface.paintedArea).forEach(([teamId, area]) => {
      totals[teamId] = (totals[teamId] || 0) + area;
      totalPainted += area;
    });
  });

  const coverage: Record<string, number> = {};
  let maxArea = 0;
  let leadingTeam: string | null = null;

  Object.entries(totals).forEach(([teamId, area]) => {
    const percentage = (area / totalPainted) * 100;
    coverage[teamId] = percentage;

    if (area > maxArea) {
      maxArea = area;
      leadingTeam = teamId;
    }
  });

  return { coverage, leadingTeam, timestamp: Date.now() };
}
```

## Grid Size Selection

| Map Scale      | Grid Size | Cell Count (16x16 map) | Memory     |
| -------------- | --------- | ---------------------- | ---------- |
| Small (64x64)  | 2 units   | ~1,000                 | ~100 KB    |
| Medium (128x128) | 4 units | ~1,000                 | ~100 KB    |
| Large (256x256) | 8 units  | ~1,000                 | ~100 KB    |

**Formula:** `gridSize = mapSize / 16` (target ~1000 cells)

## Multiple Surfaces

```tsx
// Track separate surfaces (floor, walls, etc.)
const surfaces = new Map<string, SurfacePaintData>();

function getSurfaceKey(normal: THREE.Vector3): string {
  // Categorize by normal direction
  if (normal.y > 0.5) return 'floor';
  if (normal.y < -0.5) return 'ceiling';
  if (Math.abs(normal.x) > 0.5) return 'wall_x';
  if (Math.abs(normal.z) > 0.5) return 'wall_z';
  return 'other';
}

function recordPaint(
  position: THREE.Vector3,
  normal: THREE.Vector3,
  radius: number,
  teamId: string
) {
  const surfaceKey = getSurfaceKey(normal);

  let surface = surfaces.get(surfaceKey);
  if (!surface) {
    surface = createSurfaceData();
    surfaces.set(surfaceKey, surface);
  }

  applyPaint(surface, position, radius, teamId);
}
```

## Implementation Checklist

- [ ] Define grid size based on map scale
- [ ] Create SurfacePaintData interface
- [ ] Implement grid key generation (x,z -> string)
- [ ] Add overlap correction (subtract old team, add new team)
- [ ] Aggregate across multiple surfaces
- [ ] Calculate percentages with totalArea normalization
- [ ] Provide polling or event-driven updates
- [ ] Create React hook for UI integration

## Common Pitfalls

| Pitfall                      | Symptom                  | Fix                              |
| ---------------------------- | ------------------------ | -------------------------------- |
| No overlap correction        | Score > 100%             | Subtract old team before adding  |
| Grid size too small          | Too much memory          | Increase grid size               |
| Grid size too large          | Inaccurate percentages   | Decrease grid size               |
| Forgetting totalArea         | Percentages wrong        | Set from actual map geometry     |
| Polling too fast             | Unnecessary re-renders   | Use 1-5 second interval          |
| Not clamping percentages     | Values > 100% or < 0     | Clamp result to [0, 100]         |

## Reference Implementation

See: `src/components/game/effects/PaintDecalManager.tsx`

Key sections:
- SurfacePaintData interface: lines 29-35
- Grid key generation: lines 237-243
- Apply paint with overlap: lines 267-298
- Coverage calculation: lines 326-367
- Coverage hook: lines 373-407
