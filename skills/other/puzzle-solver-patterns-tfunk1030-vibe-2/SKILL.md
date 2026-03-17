---
name: puzzle-solver-patterns
description: Constraint satisfaction patterns for the Pips puzzle solver
allowed-tools: [Read, Edit, Write, Bash, Grep]
---

# Puzzle Solver Patterns

Patterns and best practices for working with the constraint satisfaction solver in the Pips puzzle app.

## When to Use

- Adding new constraint types (e.g., "product", "even/odd", "sequential")
- Optimizing the backtracking algorithm
- Debugging solver failures ("No solution found")
- Improving solver performance for larger grids
- Understanding why puzzles are unsolvable

## Current Solver Architecture

The solver uses **backtracking with constraint propagation**:

```
src/lib/services/solver.ts     - Main solver implementation
src/lib/types/puzzle.ts        - Type definitions
```

### Key Components

1. **Constraint Types** (line 13-19 in puzzle.ts):
   - `sum`: Pips sum to exact value
   - `equal`: All pips identical
   - `different`: All pips unique
   - `greater`: All pips > value
   - `less`: All pips < value
   - `any`: No constraint

2. **Heuristics**:
   - **MRV (Minimum Remaining Values)**: Choose cell with fewest uncovered neighbors (line 133-161)
   - **Early pruning**: Check partial constraints during search (line 220-227)

3. **Validation**:
   - Cell/domino count validation (line 258-266)
   - Orphan cell handling (cells not in any region) (line 276-289)

## Adding a New Constraint Type

### Step 1: Add Type Definition

**File:** `src/lib/types/puzzle.ts`

```typescript
export type ConstraintType =
  | 'sum'
  | 'equal'
  | 'different'
  | 'greater'
  | 'less'
  | 'any'
  | 'product'      // NEW: Product of pips equals value
  | 'sequential';  // NEW: Pips form sequence (1,2,3,4)
```

### Step 2: Add Display Label

**File:** `src/lib/types/puzzle.ts` (line 112-129)

```typescript
export function constraintLabel(constraint: RegionConstraint): string {
  switch (constraint.type) {
    // ... existing cases
    case 'product':
      return `Π${constraint.value}`;  // Product symbol
    case 'sequential':
      return '→';  // Arrow for sequence
    default:
      return '';
  }
}
```

### Step 3: Implement Full Constraint Check

**File:** `src/lib/services/solver.ts` (checkConstraint function, line 60-82)

```typescript
function checkConstraint(
  constraint: { type: string; value?: number },
  pips: number[]
): boolean {
  if (pips.length === 0) return true;

  switch (constraint.type) {
    // ... existing cases

    case 'product':
      const product = pips.reduce((a, b) => a * b, 1);
      return product === constraint.value;

    case 'sequential':
      const sorted = [...pips].sort((a, b) => a - b);
      for (let i = 1; i < sorted.length; i++) {
        if (sorted[i] !== sorted[i-1] + 1) return false;
      }
      return true;

    default:
      return true;
  }
}
```

### Step 4: Implement Partial Constraint Check

**File:** `src/lib/services/solver.ts` (checkPartialConstraint function, line 84-109)

This is **critical** for early pruning to avoid exploring invalid branches.

```typescript
function checkPartialConstraint(
  constraint: { type: string; value?: number },
  pips: number[]
): boolean {
  if (pips.length === 0) return true;

  switch (constraint.type) {
    // ... existing cases

    case 'product':
      // Product so far shouldn't exceed target
      const product = pips.reduce((a, b) => a * b, 1);
      return product <= (constraint.value ?? Infinity);

    case 'sequential':
      // Check if partial sequence is valid
      const sorted = [...pips].sort((a, b) => a - b);
      for (let i = 1; i < sorted.length; i++) {
        if (sorted[i] !== sorted[i-1] + 1) return false;
      }
      return true;

    default:
      return true;
  }
}
```

### Step 5: Update UI Components

**File:** `src/components/RegionEditor.tsx`

Add the new constraint type to the picker/selector UI.

## Debugging Solver Failures

When the solver returns "No solution found", check these patterns:

### 1. Enable Debug Logging

The solver already logs extensively (line 242-335). Check console output:

```typescript
console.log('[Solver] Starting solve...', {
  cells: puzzle.validCells.length,
  dominoes: puzzle.availableDominoes.length,
  regions: puzzle.regions.length,
});
```

### 2. Check Invariants

**Cell/Domino Count** (line 258-266):
```typescript
// Must be exactly 2 cells per domino
cells === dominoes * 2
```

**Sum Constraints** (line 318-334):
```typescript
// Total of all sum constraints must equal total of all pips
sumConstraintsTotal === pipSum
```

### 3. Analyze Pip Distribution

Check if available pips can satisfy constraints:

```typescript
// Check unique values for "different" constraints
const uniquePips = new Set(allPips).size;
if (region.constraint.type === 'different' && region.cells.length > uniquePips) {
  // IMPOSSIBLE: Need 6 unique values but only 4 unique pips available
}
```

### 4. Test Constraint Satisfaction Separately

Extract a failing region and test in isolation:

```typescript
// Test if constraint is even theoretically possible
const testPips = [1, 2, 3, 4];
console.log(checkConstraint({ type: 'sum', value: 10 }, testPips));
```

## Optimization Patterns

### 1. Improve Cell Selection Heuristic

Current: **MRV** (Minimum Remaining Values) - pick cell with fewest neighbors

Alternative heuristics to try:

**Degree Heuristic**: Pick cell in most constrained region first

```typescript
function findBestUncoveredCell(
  validCells: Cell[],
  coveredCells: Set<string>,
  validCellSet: Set<string>,
  regions: Region[]  // NEW parameter
): Cell | null {
  // Score cells by region constraint complexity
  for (const cell of validCells) {
    if (coveredCells.has(cellKey(cell))) continue;

    // Find which region this cell belongs to
    const region = regions.find(r =>
      r.cells.some(c => cellKey(c) === cellKey(cell))
    );

    // Prioritize cells in 'sum' or 'different' regions (harder constraints)
    const score = region?.constraint.type === 'sum' ? 3 :
                  region?.constraint.type === 'different' ? 2 : 1;
  }
}
```

### 2. Add Domino Ordering

Try dominoes in specific order (e.g., high values first):

```typescript
// Before: try dominoes in array order
for (let i = 0; i < puzzle.availableDominoes.length; i++) {
  // ...
}

// After: sort by pip sum (descending)
const sortedIndices = puzzle.availableDominoes
  .map((d, i) => ({ index: i, sum: d.pips[0] + d.pips[1] }))
  .sort((a, b) => b.sum - a.sum)
  .map(x => x.index);

for (const i of sortedIndices) {
  // ...
}
```

### 3. Forward Checking

Check if remaining uncovered cells can still be paired:

```typescript
// After each placement, verify remaining cells have valid pairing
const remainingCells = validCells.filter(c => !coveredCells.has(cellKey(c)));

// If any cell has ZERO uncovered neighbors, this branch is dead
for (const cell of remainingCells) {
  const neighbors = getAdjacentCells(cell, validCellSet);
  const uncoveredNeighbors = neighbors.filter(n => !coveredCells.has(cellKey(n)));

  if (uncoveredNeighbors.length === 0) {
    return null;  // Prune this branch early
  }
}
```

## Common Issues & Solutions

### Issue: "Invalid puzzle: X cells but Y dominoes"

**Cause**: Cell count doesn't equal 2 × domino count

**Solution**: Check image extraction in `src/lib/services/gemini.ts`:
- Grid detection may have missed cells
- Domino list may be incomplete

### Issue: "No solution found" but puzzle looks correct

**Cause**: Constraints are unsatisfiable

**Debug steps**:
1. Check console logs for pip distribution
2. Verify sum constraints total matches pip sum
3. Test if "different" regions have enough unique values
4. Try removing regions one-by-one to isolate the problem

### Issue: Solver takes too long (>5 seconds)

**Cause**: Combinatorial explosion on larger grids

**Solutions**:
1. Improve cell selection heuristic (try degree heuristic)
2. Add forward checking (detect dead ends earlier)
3. Order dominoes by constraint relevance
4. Consider iterative deepening or timeout

## Testing New Constraints

Use the L-shaped test puzzle:

**File:** `src/lib/services/gemini.ts` - `createLShapedPuzzle()`

```typescript
export function createLShapedPuzzle(): PuzzleData {
  return {
    width: 5,
    height: 5,
    validCells: [
      { row: 0, col: 0 }, { row: 0, col: 1 },
      // ... add cells for your test case
    ],
    regions: [
      {
        id: 'test-region',
        cells: [{ row: 0, col: 0 }, { row: 0, col: 1 }],
        color: '#E53935',
        constraint: { type: 'product', value: 12 }  // TEST NEW CONSTRAINT
      }
    ],
    availableDominoes: [
      { id: '3-4', pips: [3, 4] },  // Product = 12 ✓
      // ... other dominoes
    ],
    blockedCells: []
  };
}
```

Then test via: "Try L-shaped puzzle" button in the app.

## Key Files Reference

```
src/lib/types/puzzle.ts           - Type definitions, constraint types
src/lib/services/solver.ts        - Main backtracking solver
src/lib/services/gemini.ts        - Image extraction + test puzzles
src/components/RegionEditor.tsx   - UI for editing constraints
src/lib/state/puzzle-store.ts     - State management
```

## Examples

### Example 1: Add "Odd/Even" Constraint

```typescript
// 1. Add type
type ConstraintType = ... | 'odd' | 'even';

// 2. Label
case 'odd': return 'O';
case 'even': return 'E';

// 3. Full check
case 'odd': return pips.every(p => p % 2 === 1);
case 'even': return pips.every(p => p % 2 === 0);

// 4. Partial check (same as full for this constraint)
case 'odd': return pips.every(p => p % 2 === 1);
case 'even': return pips.every(p => p % 2 === 0);
```

### Example 2: Debug Unsolvable Puzzle

```typescript
// Add this after line 335 in solver.ts
console.log('[DEBUG] Analyzing unsatisfiable constraints...');

for (const region of regionsToCheck) {
  const availablePipsForRegion = puzzle.availableDominoes.flatMap(d => d.pips);

  if (region.constraint.type === 'different') {
    const uniqueAvailable = new Set(availablePipsForRegion).size;
    if (region.cells.length > uniqueAvailable) {
      console.error(`[DEBUG] Region ${region.id} needs ${region.cells.length} unique values but only ${uniqueAvailable} available!`);
    }
  }
}
```

## Best Practices

1. **Always implement both full AND partial constraint checks**
   - Full: Used when region is complete
   - Partial: Used during search for early pruning

2. **Test with small puzzles first**
   - Use `createLShapedPuzzle()` or `createSamplePuzzle()`
   - Verify constraint works before trying on real puzzles

3. **Add console logging**
   - Log constraint evaluations during debug
   - Remove before committing

4. **Consider mathematical properties**
   - Can constraint be violated early? (e.g., product already too large)
   - Can you detect impossibility before trying all combinations?

5. **Update UI components**
   - Don't forget to add new constraint to RegionEditor
   - Add appropriate symbols/labels to constraintLabel()
