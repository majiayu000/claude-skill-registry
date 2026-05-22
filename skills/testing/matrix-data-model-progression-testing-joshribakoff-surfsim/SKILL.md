---
name: matrix-data-model-progression-testing
description: Matrix data model verification using ASCII diagrams. Use when working with *Progressions.ts files, defineProgression(), or testing how 2D numeric grids evolve over time. Auto-apply when editing files matching *Progressions.ts or src/test-utils/ascii*.ts.
---

# Matrix Data Model Progression Testing Skill

Verifies how **2D numeric matrices** (the underlying data model) evolve over simulated time. Uses compact ASCII diagrams inspired by RxJS marble testing.

This is about **data correctness**, not rendering. The wave simulation uses matrices to represent:

- Bathymetry (depth values)
- Energy fields (wave energy at each cell)
- Foam density (foam amount at each cell)

## When to Use This

- Editing `*Progressions.ts` files (bathymetry, energy field, foam, etc.)
- Designing new simulation behaviors
- Debugging why a layer produces unexpected **data** output
- Verifying time-series evolution of matrix values

## Architecture

```
src/test-utils/
  asciiMatrix.ts           → ASCII encoding/decoding utilities
  asciiMatrix.test.ts      → Tests for the utilities themselves
  progression.ts           → defineProgression() framework
  progression.test.ts      → Tests for the framework

src/render/*Progressions.ts    → Layer progression definitions
src/state/energyFieldProgressions.ts
```

## ASCII Matrix Format

Each character represents a cell value (0.0-1.0):

| Char | Value Range | Meaning |
|------|-------------|---------|
| `-`  | < 0.05      | No energy / zero |
| `1`  | 0.05-0.14   | Very low |
| `2`  | 0.15-0.24   | Low |
| `3`  | 0.25-0.34   | Low-medium |
| `4`  | 0.35-0.44   | Medium-low |
| `A`  | 0.45-0.54   | Medium |
| `B`  | 0.55-0.64   | Medium-high |
| `C`  | 0.65-0.74   | High |
| `D`  | 0.75-0.84   | Higher |
| `E`  | 0.85-0.94   | Very high |
| `F`  | >= 0.95     | Full energy / max |

### Single Matrix Example

```
FFFFF    ← Row 0: Full energy at horizon
-----    ← Row 1: No energy
-----    ← Row 2: No energy
-----    ← Row 3: No energy
-----    ← Row 4: No energy (shore)
```

### Multi-Frame Progression Example

Shows energy propagating downward over time:

```
t=0s     t=1s     t=2s     t=3s
FFFFF    BBBBB    44444    22222
-----    AAAAA    AAAAA    44444
-----    22222    44444    44444
-----    11111    22222    33333
-----    -----    11111    22222
```

## Core Utilities

```typescript
import {
  matrixToAscii,
  asciiToMatrix,
  progressionToAscii,
  asciiToProgression,
  matricesMatchAscii,
  valueToChar,
  charToValue,
} from '../test-utils/asciiMatrix';

// Single matrix
matrixToAscii([[1.0, 0.5], [0.0, 0.2]])  // → "FA\n-2"
asciiToMatrix("FA\n-2")                   // → [[1.0, 0.5], [0.0, 0.2]]

// Multi-frame progression
progressionToAscii(snapshots)             // → side-by-side frames with headers
asciiToProgression(asciiString)           // → array of {time, matrix}

// Comparison (tolerant to ASCII precision)
matricesMatchAscii(actual, expected)      // → true if same when encoded
```

## defineProgression() Framework

```typescript
import { defineProgression } from '../test-utils/progression';

export const PROGRESSION_ENERGY_PROPAGATION = defineProgression({
  id: 'energy-field/propagation',
  description: 'Energy propagates from horizon toward shore',
  initialMatrix: [
    [1.0, 1.0, 1.0, 1.0, 1.0],  // Horizon: full energy
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],  // Shore: no energy yet
  ],
  updateFn: (matrix, dt) => propagateEnergy(matrix, dt),
  captureTimes: [0, 1, 2, 3, 4, 5],  // Capture snapshots at these times
});

// Access computed snapshots
PROGRESSION_ENERGY_PROPAGATION.snapshots[0].matrix  // t=0
PROGRESSION_ENERGY_PROPAGATION.snapshots[3].matrix  // t=3
```

## Testing Progressions

### Inline ASCII Assertions

```typescript
import { describe, it, expect } from 'vitest';
import { progressionToAscii } from '../test-utils/asciiMatrix';

describe('PROGRESSION_ENERGY_PROPAGATION', () => {
  it('produces expected time evolution', () => {
    const ascii = progressionToAscii(PROGRESSION_ENERGY_PROPAGATION.snapshots);

    expect(ascii).toBe(`
t=0s     t=1s     t=2s     t=3s
FFFFF    BBBBB    44444    22222
-----    AAAAA    AAAAA    44444
-----    22222    44444    44444
-----    11111    22222    33333
-----    -----    11111    22222
`.trim());
  });
});
```

### Point Assertions

```typescript
it('energy reaches row 3 by t=3s', () => {
  const snapshot = PROGRESSION_ENERGY_PROPAGATION.snapshots[3];
  expect(snapshot.matrix[3][0]).toBeGreaterThan(0);
});
```

## Workflow: Designing a New Progression

1. **Sketch ASCII first** - Draw what you expect the evolution to look like
1. **Write the test** - Use `progressionToAscii()` with your expected ASCII
1. **Implement the logic** - Write the `updateFn` that produces this behavior
1. **Run test** - `npx vitest run src/render/myProgressions.test.ts`
1. **Iterate** - Adjust coefficients until ASCII matches expectations

```
Design-first workflow:
  Sketch ASCII → Write test → Implement → Verify

NOT trial-and-error:
  Implement → Run → "Hmm, that looks wrong" → Tweak → Repeat
```

## Why ASCII Over Vitest Snapshots?

| Aspect | ASCII | Vitest Snapshots |
|--------|-------|------------------|
| Readability | Visual pattern obvious | Wall of numbers |
| Size | 7 lines for 6 frames | 1000+ lines |
| Location | Inline in test | Separate file |
| Diffs | Shows exactly which cells changed | Hard to parse |
| Design | Can sketch expected output first | Must run to generate |

## Relationship to Visual Testing

Progression tests verify the **data** (matrix values).
Visual tests verify the **rendering** (pixels on screen).

```
Progression Test (this skill)     Visual Test (visual-testing skill)
        ↓                                    ↓
   Matrix data                         Screenshot
   [1.0, 0.5, 0.2]                    [PNG pixels]
        ↓                                    ↓
   ASCII: "FA2"                       Baseline comparison
```

**Always verify data first.** If the matrix is wrong, the visual will be wrong too. Don't debug rendering when the underlying data is the problem.

See `visual-testing` skill for screenshot-based regression testing.

## Commands

```bash
# Run progression tests
npx vitest run src/render/bathymetryProgressions.test.ts
npx vitest run src/state/energyFieldProgressions.test.ts

# Run all test utilities (including ASCII)
npx vitest run src/test-utils/

# Watch mode for development
npx vitest src/render/foamProgressions.test.ts
```

## Common Patterns

### Testing Boundary Conditions

```typescript
it('handles zero initial energy gracefully', () => {
  const progression = defineProgression({
    initialMatrix: createZeroMatrix(5, 5),
    updateFn: propagateEnergy,
    captureTimes: [0, 1, 2],
  });

  // Should remain zero (no energy to propagate)
  expect(matrixToAscii(progression.snapshots[2].matrix)).toBe(
    '-----\n-----\n-----\n-----\n-----'
  );
});
```

### Testing Conservation Laws

```typescript
it('total energy decreases with damping', () => {
  const snapshots = PROGRESSION_WITH_DAMPING.snapshots;
  const totalEnergy = (m: number[][]) => m.flat().reduce((a, b) => a + b, 0);

  expect(totalEnergy(snapshots[3].matrix))
    .toBeLessThan(totalEnergy(snapshots[0].matrix));
});
```

### Comparing Two Progressions

```typescript
it('damped version has less energy than undamped', () => {
  const damped = PROGRESSION_WITH_DAMPING.snapshots[3].matrix;
  const undamped = PROGRESSION_NO_DAMPING.snapshots[3].matrix;

  const sum = (m: number[][]) => m.flat().reduce((a, b) => a + b, 0);
  expect(sum(damped)).toBeLessThan(sum(undamped));
});
```
