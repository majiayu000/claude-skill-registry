---
name: logic-testing
description: Pure logic and math testing with Vitest. Use for single-point assertions on functions, state transitions, and physics calculations. Auto-apply when editing *.test.ts files (except *Progressions.test.ts).
---

# Logic Testing Skill

Tests **pure functions and logic** in isolation using Vitest. Single-point assertions that verify one behavior at a time.

For testing how matrices evolve over time, see the `matrix-data-model-progression-testing` skill instead.

## Commands

```bash
# Run specific test file (preferred - fast feedback)
npx vitest run src/path/file.test.ts

# Run all unit tests
npm test

# Run test utilities (validate test framework)
npx vitest run src/test-utils/

# Watch mode for development
npx vitest src/path/file.test.ts
```

## File Structure

Tests live next to source files:

```
src/state/waveModel.ts           → src/state/waveModel.test.ts
src/render/energyField.ts        → src/render/energyField.test.ts
src/test-utils/progression.ts    → src/test-utils/progression.test.ts
```

## Test Structure

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('ModuleName', () => {
  describe('functionName', () => {
    it('should handle specific case', () => {
      // Arrange
      const input = createTestData();

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toMatchObject({ expected: 'shape' });
    });
  });
});
```

## Testing Physics/Math Code

This codebase has wave simulation physics. Key patterns:

```typescript
// Test boundary conditions
it('handles zero depth', () => {
  expect(() => calculateWaveHeight(0)).not.toThrow();
});

// Test physical invariants
it('wave height increases in shallow water (shoaling)', () => {
  const deep = calculateWaveHeight({ depth: 100 });
  const shallow = calculateWaveHeight({ depth: 10 });
  expect(shallow).toBeGreaterThan(deep);
});

// Use toBeCloseTo for floats
it('energy conserved within tolerance', () => {
  expect(totalEnergy).toBeCloseTo(initialEnergy, 5);
});
```

## Test Utilities Must Be Tested

Files in `src/test-utils/` are foundational. If they're broken, all tests are untrustworthy.

```
src/test-utils/
├── matrixField.ts          # Matrix↔field conversion
├── matrixField.test.ts     # REQUIRED
├── asciiMatrix.ts          # ASCII encoding (see matrix-progression skill)
├── asciiMatrix.test.ts     # REQUIRED
├── progression.ts          # defineProgression() framework
├── progression.test.ts     # REQUIRED
└── index.ts
```

**Always run after modifying test utils:**

```bash
npx vitest run src/test-utils/
```

## Common Patterns

### Testing State Transitions

```typescript
it('transitions from idle to breaking when depth threshold crossed', () => {
  const wave = createWave({ amplitude: 1.0 });
  expect(getWaveState(wave, { depth: 10 })).toBe('propagating');
  expect(getWaveState(wave, { depth: 0.5 })).toBe('breaking');
});
```

### Testing Time-Dependent Values

```typescript
it('progress increases over time', () => {
  const t0 = getProgress(0);
  const t5 = getProgress(5000);
  expect(t5).toBeGreaterThan(t0);
});
```

### Testing Edge Cases

```typescript
it('handles empty input', () => {
  expect(processData([])).toEqual([]);
});

it('handles negative values', () => {
  expect(clamp(-5, 0, 10)).toBe(0);
});
```

## Debugging Failed Tests

1. **Run single test** - Isolate the failure
1. **Check test data** - Is the fixture correct?
1. **Add console.log** - Inspect intermediate values
1. **Check physics** - Does the math match expectations?

## Related Skills

- **matrix-model-testing** - For testing how 2D matrices evolve over time (ASCII diagrams)
- **visual-regression** - For testing rendered pixel output (screenshots)
