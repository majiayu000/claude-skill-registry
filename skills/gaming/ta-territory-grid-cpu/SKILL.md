---
name: ta-territory-grid-cpu
description: CPU-based territory tracking grid for multiplayer server-authoritative scoring. Use for territory control, paint tracking, and coverage calculation.
category: shader
---

# Territory Grid (CPU-Based) Skill

> "Server-authoritative territory tracking for anti-cheat and network validation."

## Overview

The CPU-based territory grid replaces RenderTexture-based tracking for multiplayer games. This enables:
- **Server validation** - Territory state can be verified server-side
- **Anti-cheat** - Clients can't fake territory percentages
- **Network sync** - Grid state transmitted efficiently
- **Height multiplier** - Strategic value from elevation

## When to Use This Skill

Use when your task involves:
- Multiplayer territory control
- Server-authoritative scoring
- Paint system validation
- Height-based territory multipliers
- Network-efficient state sync

**NOT for:** Single-player visual effects, GPU-only paint demos

## Core Concepts

### CPU vs GPU Territory Tracking

| Aspect | CPU Grid (This Skill) | GPU RenderTexture (Old) |
|--------|----------------------|-------------------------|
| Server validation | ✅ Yes | ❌ No |
| Network sync | ✅ Efficient | ❌ Full texture transfer |
| Anti-cheat | ✅ Client can't fake | ❌ Client can modify |
| Height multiplier | ✅ Easy to add | ❌ Requires compute shader |
| Debug | ✅ Inspect state | ❌ Black box |
| Performance | <10ms per update | <1ms but no validation |

### Grid Architecture

```
128×128 Grid (2m cells = 256m map)
    │
    ├──> Each cell tracks:
    │     - owner: orange | blue | neutral | contested
    │     - paintLayers: { team, amount, age }[]
    │     - lastUpdated: timestamp
    │
    ├──> Coverage calculation:
    │     - Count cells by owner
    │     - Apply height multiplier (1.5x at 10m+)
    │     - Return percentages
    │
    └──> Network format:
          - Uint8Array (16KB for full grid)
          - Delta updates (only changed cells)
```

## Implementation Pattern

### 1. TerritoryGrid System

```typescript
// src/systems/territory/TerritoryGrid.ts
export interface TerritoryCell {
  x: number;
  z: number;
  owner: 'orange' | 'blue' | 'neutral' | 'contested';
  paintLayers: PaintLayer[];
  lastUpdated: number;
  height: number;  // For multiplier calculation
}

export interface PaintLayer {
  team: 'orange' | 'blue';
  amount: number;  // 0-1
  age: number;     // For fading (optional)
  timestamp: number;
}

export interface TerritoryGridConfig {
  width: number;      // 128 cells
  height: number;     // 128 cells
  cellSize: number;   // 2 meters
  maxHeight: number;  // 24 meters (for multiplier)
  heightMultiplierThreshold: number; // 10m
  heightMultiplierValue: number;     // 1.5x
}

export interface TerritoryStats {
  orange: number;  // 0-100 percentage
  blue: number;    // 0-100 percentage
  neutral: number; // 0-100 percentage
  orangeWeighted: number; // With height multiplier
  blueWeighted: number;
}

export class TerritoryGrid {
  private cells: TerritoryCell[][];
  private config: TerritoryGridConfig;
  private dirtyCells: Set<string> = new Set();

  constructor(config: Partial<TerritoryGridConfig> = {}) {
    this.config = {
      width: 128,
      height: 128,
      cellSize: 2,
      maxHeight: 24,
      heightMultiplierThreshold: 10,
      heightMultiplierValue: 1.5,
      ...config
    };

    this.initializeGrid();
  }

  private initializeGrid(): void {
    this.cells = [];
    for (let z = 0; z < this.config.height; z++) {
      const row: TerritoryCell[] = [];
      for (let x = 0; x < this.config.width; x++) {
        row.push({
          x, z,
          owner: 'neutral',
          paintLayers: [],
          lastUpdated: Date.now(),
          height: 0  // Will be set from terrain
        });
      }
      this.cells.push(row);
    }
  }

  /**
   * Set terrain height for a cell (for multiplier)
   */
  setCellHeight(gx: number, gz: number, height: number): void {
    if (this.isInBounds(gx, gz)) {
      this.cells[gz][gx].height = height;
    }
  }

  /**
   * Apply paint at world position
   */
  applyPaint(
    worldX: number,
    worldZ: number,
    team: 'orange' | 'blue',
    amount: number = 0.5,
    radius: number = 1
  ): void {
    const { cellSize } = this.config;

    // Convert world position to grid coords
    const centerGx = Math.floor((worldX + 128) / cellSize);
    const centerGz = Math.floor((worldZ + 128) / cellSize);

    // Get affected cells (circular radius)
    const affectedCells = this.getCellsInRadius(centerGx, centerGz, radius);

    for (const cell of affectedCells) {
      // Add paint layer
      cell.paintLayers.push({
        team,
        amount,
        age: 0,
        timestamp: Date.now()
      });

      // Limit paint layers
      if (cell.paintLayers.length > 10) {
        cell.paintLayers.shift(); // Remove oldest
      }

      // Update ownership
      this.updateCellOwner(cell);

      // Mark dirty for network sync
      this.dirtyCells.add(`${cell.x},${cell.z}`);
    }
  }

  /**
   * Get cells within radius (for paint splats)
   */
  private getCellsInRadius(gx: number, gz: number, radius: number): TerritoryCell[] {
    const cells: TerritoryCell[] = [];
    const r = Math.ceil(radius);

    for (let dz = -r; dz <= r; dz++) {
      for (let dx = -r; dx <= r; dx++) {
        if (dx * dx + dz * dz <= radius * radius) {
          const nx = gx + dx;
          const nz = gz + dz;
          if (this.isInBounds(nx, nz)) {
            cells.push(this.cells[nz][nx]);
          }
        }
      }
    }

    return cells;
  }

  /**
   * Update cell ownership based on paint layers
   */
  private updateCellOwner(cell: TerritoryCell): void {
    const orangeTotal = this.getTeamPaint(cell, 'orange');
    const blueTotal = this.getTeamPaint(cell, 'blue');

    if (orangeTotal > blueTotal && orangeTotal > 0.1) {
      cell.owner = 'orange';
    } else if (blueTotal > orangeTotal && blueTotal > 0.1) {
      cell.owner = 'blue';
    } else if (orangeTotal > 0.1 || blueTotal > 0.1) {
      cell.owner = 'contested';
    } else {
      cell.owner = 'neutral';
    }

    cell.lastUpdated = Date.now();
  }

  /**
   * Get total paint amount for a team in a cell
   */
  private getTeamPaint(cell: TerritoryCell, team: 'orange' | 'blue'): number {
    return cell.paintLayers
      .filter(l => l.team === team)
      .reduce((sum, l) => sum + l.amount, 0);
  }

  /**
   * Calculate territory coverage
   */
  calculateCoverage(): TerritoryStats {
    let orange = 0, blue = 0, neutral = 0;
    let orangeWeighted = 0, blueWeighted = 0;

    const { heightMultiplierThreshold, heightMultiplierValue, maxHeight } = this.config;

    for (let z = 0; z < this.config.height; z++) {
      for (let x = 0; x < this.config.width; x++) {
        const cell = this.cells[z][x];

        // Height multiplier
        const multiplier = cell.height >= heightMultiplierThreshold
          ? heightMultiplierValue
          : 1.0;

        if (cell.owner === 'orange') {
          orange++;
          orangeWeighted += multiplier;
        } else if (cell.owner === 'blue') {
          blue++;
          blueWeighted += multiplier;
        } else {
          neutral++;
        }
      }
    }

    const total = this.config.width * this.config.height;

    return {
      orange: (orange / total) * 100,
      blue: (blue / total) * 100,
      neutral: (neutral / total) * 100,
      orangeWeighted: (orangeWeighted / total) * 100,
      blueWeighted: (blueWeighted / total) * 100
    };
  }

  /**
   * Get cell at grid coordinates
   */
  getCell(gx: number, gz: number): TerritoryCell | null {
    if (this.isInBounds(gx, gz)) {
      return this.cells[gz][gx];
    }
    return null;
  }

  /**
   * Get cell at world position
   */
  getCellAtWorld(worldX: number, worldZ: number): TerritoryCell | null {
    const { cellSize } = this.config;
    const gx = Math.floor((worldX + 128) / cellSize);
    const gz = Math.floor((worldZ + 128) / cellSize);
    return this.getCell(gx, gz);
  }

  /**
   * Check if coordinates are in bounds
   */
  private isInBounds(gx: number, gz: number): boolean {
    return gx >= 0 && gx < this.config.width &&
           gz >= 0 && gz < this.config.height;
  }

  /**
   * Get network delta (dirty cells only)
   */
  getNetworkDelta(): Uint8Array {
    // Format: [x, z, owner, height_multiplier] per cell
    const data: number[] = [];

    for (const key of this.dirtyCells) {
      const [x, z] = key.split(',').map(Number);
      const cell = this.cells[z][x];

      // Owner encoding: 0=neutral, 1=orange, 2=blue, 3=contested
      const ownerCode = ['neutral', 'orange', 'blue', 'contested'].indexOf(cell.owner);

      // Height multiplier (0-1, encoded as 0-255)
      const multiplier = cell.height >= this.config.heightMultiplierThreshold
        ? this.config.heightMultiplierValue
        : 1.0;
      const multiplierByte = Math.floor((multiplier - 1.0) * 255);

      data.push(x, z, ownerCode, multiplierByte);
    }

    this.dirtyCells.clear();

    return new Uint8Array(data);
  }

  /**
   * Apply network delta from server
   */
  applyNetworkDelta(data: Uint8Array): void {
    for (let i = 0; i < data.length; i += 4) {
      const x = data[i];
      const z = data[i + 1];
      const ownerCode = data[i + 2];
      const multiplierByte = data[i + 3];

      if (this.isInBounds(x, z)) {
        const cell = this.cells[z][x];
        cell.owner = ['neutral', 'orange', 'blue', 'contested'][ownerCode] as any;
        // Multiplier info could affect scoring display
      }
    }
  }

  /**
   * Clear all paint
   */
  clear(): void {
    for (let z = 0; z < this.config.height; z++) {
      for (let x = 0; x < this.config.width; x++) {
        const cell = this.cells[z][x];
        cell.owner = 'neutral';
        cell.paintLayers = [];
        cell.lastUpdated = Date.now();
      }
    }
    this.dirtyCells.clear();
  }

  /**
   * Get grid data for visualization
   */
  getGridData(): Uint8Array {
    // RGBA format for texture: R=orange, B=blue, G=reserved, A=multiplier
    const data = new Uint8Array(this.config.width * this.config.height * 4);

    for (let z = 0; z < this.config.height; z++) {
      for (let x = 0; x < this.config.width; x++) {
        const cell = this.cells[z][x];
        const index = (z * this.config.width + x) * 4;

        data[index] = cell.owner === 'orange' ? 255 : 0;      // R
        data[index + 1] = 0;                                 // G (reserved)
        data[index + 2] = cell.owner === 'blue' ? 255 : 0;  // B

        // Alpha = ownership strength
        const strength = this.getTeamPaint(cell, 'orange') +
                        this.getTeamPaint(cell, 'blue');
        data[index + 3] = Math.min(255, strength * 255);
      }
    }

    return data;
  }
}
```

### 2. React Hook Integration

```typescript
// src/hooks/useTerritoryGrid.ts
import { useMemo } from 'react';
import { TerritoryGrid } from '@/systems/territory/TerritoryGrid';

export function useTerritoryGrid() {
  const grid = useMemo(() => new TerritoryGrid(), []);

  const applyPaint = (
    worldX: number,
    worldZ: number,
    team: 'orange' | 'blue'
  ) => {
    grid.applyPaint(worldX, worldZ, team);
  };

  const getCoverage = () => {
    return grid.calculateCoverage();
  };

  const getCellAt = (worldX: number, worldZ: number) => {
    return grid.getCellAtWorld(worldX, worldZ);
  };

  return {
    applyPaint,
    getCoverage,
    getCellAt,
    grid
  };
}
```

## GDD Specifications

From `docs/design/gdd/4_territory_control.md`:

| Property | Value | Source |
|----------|-------|--------|
| Map Size | 256m × 256m | GDD |
| Grid Cells | 128×128 | GDD |
| Cell Size | 2 meters | GDD |
| Height Multiplier | 1.5x at 10m+ | DEC-105 |
| Win Threshold | 60% coverage | GDD |
| Update Rate | 1 Hz for territory | GDD |

## Height Multiplier Logic

```typescript
// DEC-105: Higher terrain = more territory points
function getHeightScore(height: number, maxHeight: number): number {
  const THRESHOLD = 10;  // meters
  const MULTIPLIER = 1.5;

  if (height >= THRESHOLD) {
    return MULTIPLIER;
  }
  return 1.0;
}

// Usage in coverage calculation
for (const cell of cells) {
  const multiplier = getHeightScore(cell.height, maxHeight);
  if (cell.owner === 'orange') {
    orangeScore += multiplier;
  } else if (cell.owner === 'blue') {
    blueScore += multiplier;
  }
}
```

## Unit Test Pattern

```typescript
// tests/unit/TerritoryGrid.test.ts
import { describe, it, expect } from 'vitest';
import { TerritoryGrid } from '@/systems/territory/TerritoryGrid';

describe('TerritoryGrid', () => {
  it('should initialize to neutral', () => {
    const grid = new TerritoryGrid();
    const coverage = grid.calculateCoverage();

    expect(coverage.orange).toBe(0);
    expect(coverage.blue).toBe(0);
    expect(coverage.neutral).toBe(100);
  });

  it('should update ownership on paint', () => {
    const grid = new TerritoryGrid();
    grid.applyPaint(0, 0, 'orange', 1.0);

    const coverage = grid.calculateCoverage();
    expect(coverage.orange).toBeGreaterThan(0);
  });

  it('should calculate coverage accurately within 1%', () => {
    const grid = new TerritoryGrid({ width: 64, height: 64 });

    // Fill 25% with orange
    for (let z = 0; z < 32; z++) {
      for (let x = 0; x < 32; x++) {
        grid.applyPaint(x * 2, z * 2, 'orange', 1.0);
      }
    }

    const coverage = grid.calculateCoverage();
    expect(Math.abs(coverage.orange - 25)).toBeLessThan(1);
  });

  it('should apply height multiplier correctly', () => {
    const grid = new TerritoryGrid();

    // Paint at low elevation
    grid.setCellHeight(0, 0, 5);  // Below threshold
    grid.applyPaint(0, 0, 'orange', 1.0);

    // Paint at high elevation
    grid.setCellHeight(10, 10, 15);  // Above threshold
    grid.applyPaint(20, 20, 'orange', 1.0);

    const coverage = grid.calculateCoverage();
    expect(coverage.orangeWeighted).toBeGreaterThan(coverage.orange);
  });
});
```

## Network Optimization

### Delta Encoding

Only send changed cells:

```typescript
// Client -> Server: Paint events
{
  "type": "paint",
  "x": 50,
  "z": 30,
  "team": "orange",
  "amount": 0.5
}

// Server -> Client: Grid delta (1 Hz)
{
  "type": "territory_update",
  "delta": [50, 30, 1, 0, 51, 30, 1, 0, ...],
  "coverage": { orange: 45.2, blue: 38.1, neutral: 16.7 }
}
```

### Compression

```typescript
// RLE encoding for runs of same owner
function compressGrid(grid: TerritoryGrid): Uint8Array {
  const compressed: number[] = [];
  let currentOwner = 0;
  let runLength = 0;

  for (const cell of grid.cells.flat()) {
    const owner = ['neutral', 'orange', 'blue', 'contested'].indexOf(cell.owner);

    if (owner === currentOwner) {
      runLength++;
    } else {
      compressed.push(currentOwner, runLength);
      currentOwner = owner;
      runLength = 1;
    }
  }

  compressed.push(currentOwner, runLength);
  return new Uint8Array(compressed);
}
```

## Debug Visualization

```typescript
// Debug: Visualize grid ownership
function createGridHelper(grid: TerritoryGrid): THREE.Mesh {
  const geometry = new THREE.PlaneGeometry(256, 256, 128, 128);
  const colors = new Float32Array(128 * 128 * 3);

  for (let z = 0; z < 128; z++) {
    for (let x = 0; x < 128; x++) {
      const cell = grid.getCell(x, z);
      const index = (z * 128 + x) * 3;

      if (cell.owner === 'orange') {
        colors[index] = 1; colors[index + 1] = 0.42; colors[index + 2] = 0.21;
      } else if (cell.owner === 'blue') {
        colors[index] = 0.29; colors[index + 1] = 0.56; colors[index + 2] = 0.85;
      } else {
        colors[index] = 0.5; colors[index + 1] = 0.5; colors[index + 2] = 0.5;
      }
    }
  }

  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  return new THREE.Mesh(
    geometry,
    new THREE.MeshBasicMaterial({ vertexColors: true, wireframe: true })
  );
}
```

## Common Issues

### Coverage Doesn't Match Visual Paint

**Cause:** Grid resolution mismatch with visual paint texture.

**Fix:** Ensure both use same cell size (2m).

```typescript
// Verify alignment
const worldX = 0;  // Center of map
const gridX = Math.floor((worldX + 128) / 2);  // Should be 64
console.log('Grid coord:', gridX);  // Should be 64
```

### Performance Degradation

**Cause:** Too many paint layers accumulating.

**Fix:** Limit layers and age old paint.

```typescript
// Age and remove old paint
function agePaintLayers(cell: TerritoryCell, dt: number): void {
  cell.paintLayers = cell.paintLayers.filter(layer => {
    layer.age += dt;
    return layer.age < 60;  // Remove after 60 seconds
  });
}
```

### Network Sync Issues

**Cause:** Dirty cells not properly tracked.

**Fix:** Always mark cells dirty after paint.

```typescript
applyPaint(...) {
  // ... paint logic ...
  this.dirtyCells.add(`${cell.x},${cell.z}`);
}
```

## Related Skills

For paint overlay visualization: `Skill("ta-paint-territory")`
For terrain height sampling: `Skill("ta-terrain-mesh")`
For E2E testing: `Skill("ta-terrain-testing")`

## External References

- Implementation plan: `docs/implementation/terrain-refactor-plan.md` (Phase 5)
- GDD: `docs/design/gdd/4_territory_control.md`
- GDD: `docs/design/gdd/11_level_design.md`
