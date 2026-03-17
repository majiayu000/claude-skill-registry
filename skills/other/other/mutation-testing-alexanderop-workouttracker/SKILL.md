---
name: mutation-testing
description: |
  Mutation testing patterns for verifying test effectiveness. Use when analyzing branch code
  to find weak or missing tests. Triggers: "mutation testing", "test effectiveness",
  "would tests catch this bug", "weak tests", "are my tests good enough", "surviving mutants".
---

# Mutation Testing

Mutation testing answers: **"Would my tests catch this bug?"** by actually introducing bugs and running tests.

---

## Execution Workflow

**CRITICAL**: This skill actually mutates code and runs tests. Follow this exact process:

### Step 1: Identify Target Code

```bash
# Get changed files on the branch
git diff main...HEAD --name-only | grep -E '\.(ts|js|tsx|jsx|vue)$' | grep -v '\.test\.' | grep -v '\.spec\.'
```

### Step 2: For Each Function to Test

Execute this loop for each mutation:

```
1. READ the original file and note exact content
2. APPLY one mutation (edit the code)
3. RUN tests: pnpm test --run (or specific test file)
4. RECORD result: KILLED (test failed) or SURVIVED (test passed)
5. RESTORE original code immediately
6. Repeat for next mutation
```

### Step 3: Report Results

After all mutations, provide a summary table:

```
| Mutation | Location | Result | Action Needed |
|----------|----------|--------|---------------|
| `>` → `>=` | file.ts:42 | SURVIVED | Add boundary test |
| `&&` → `||` | file.ts:58 | KILLED | None |
```

---

## Mutation Operators to Apply

### Priority 1: Boundary Mutations (Most Likely to Survive)

| Original | Mutate To | Why It Matters |
|----------|-----------|----------------|
| `<` | `<=` | Boundary not tested |
| `>` | `>=` | Boundary not tested |
| `<=` | `<` | Equality case missed |
| `>=` | `>` | Equality case missed |

### Priority 2: Boolean Logic Mutations

| Original | Mutate To | Why It Matters |
|----------|-----------|----------------|
| `&&` | `\|\|` | Only tested when both true |
| `\|\|` | `&&` | Only tested when both false |
| `!condition` | `condition` | Negation not verified |

### Priority 3: Arithmetic Mutations

| Original | Mutate To | Why It Matters |
|----------|-----------|----------------|
| `+` | `-` | Tested with 0 only |
| `-` | `+` | Tested with 0 only |
| `*` | `/` | Tested with 1 only |

### Priority 4: Return/Early Exit Mutations

| Original | Mutate To | Why It Matters |
|----------|-----------|----------------|
| `return x` | `return null` | Return value not asserted |
| `return true` | `return false` | Boolean return not checked |
| `if (cond) return` | `// removed` | Early exit not tested |

### Priority 5: Statement Removal

| Original | Mutate To | Why It Matters |
|----------|-----------|----------------|
| `array.push(x)` | `// removed` | Side effect not verified |
| `await save(x)` | `// removed` | Async operation not verified |
| `emit('event')` | `// removed` | Event emission not tested |

---

## Practical Execution Example

### Example: Testing a Validation Function

**Original code** (`src/utils/validation.ts:15`):
```typescript
export function isValidAge(age: number): boolean {
  return age >= 18 && age <= 120;
}
```

**Mutation 1**: Change `>=` to `>`
```typescript
export function isValidAge(age: number): boolean {
  return age > 18 && age <= 120;  // MUTATED
}
```

**Run tests**:
```bash
pnpm test --run src/__tests__/validation.test.ts
```

**Result**: Tests PASS → **SURVIVED** (Bad! Need test for `isValidAge(18)`)

**Restore original code immediately**

**Mutation 2**: Change `&&` to `||`
```typescript
export function isValidAge(age: number): boolean {
  return age >= 18 || age <= 120;  // MUTATED
}
```

**Run tests**:
```bash
pnpm test --run src/__tests__/validation.test.ts
```

**Result**: Tests FAIL → **KILLED** (Good! Tests catch this bug)

**Restore original code immediately**

---

## Results Interpretation

### Mutant States

| State | Meaning | Action |
|-------|---------|--------|
| **KILLED** | Test failed with mutant | Tests are effective |
| **SURVIVED** | Tests passed with mutant | **Add or strengthen test** |
| **TIMEOUT** | Tests hung (infinite loop) | Counts as detected |

### Mutation Score

```
Score = (Killed + Timeout) / Total Mutations * 100
```

| Score | Quality |
|-------|---------|
| < 60% | Weak - significant test gaps |
| 60-80% | Moderate - improvements needed |
| 80-90% | Good - minor gaps |
| > 90% | Strong test suite |

---

## Fixing Surviving Mutants

When a mutant survives, add a test that would catch it:

### Surviving: Boundary mutation (`>=` → `>`)

```typescript
// Add boundary test
it('accepts exactly 18 years old', () => {
  expect(isValidAge(18)).toBe(true);  // Would fail if >= became >
});
```

### Surviving: Logic mutation (`&&` → `||`)

```typescript
// Add test with mixed conditions
it('rejects when only one condition met', () => {
  expect(isValidAge(15)).toBe(false);  // Would pass if && became ||
});
```

### Surviving: Statement removal

```typescript
// Add side effect verification
it('saves to database', async () => {
  await processOrder(order);
  expect(db.save).toHaveBeenCalledWith(order);  // Would fail if save removed
});
```

---

## Quick Checklist During Mutation

For each mutation, ask:

1. **Before mutating**: Does a test exist for this code path?
2. **After running tests**: Did any test actually fail?
3. **If survived**: What specific test would catch this?
4. **After fixing**: Re-run mutation to confirm killed

---

## Common Surviving Mutation Patterns

### Tests Only Check Happy Path

```typescript
// WEAK: Only tests success case
it('validates', () => {
  expect(validate(goodInput)).toBe(true);
});

// STRONG: Tests both cases
it('validates good input', () => {
  expect(validate(goodInput)).toBe(true);
});
it('rejects bad input', () => {
  expect(validate(badInput)).toBe(false);
});
```

### Tests Use Identity Values

```typescript
// WEAK: Mutation survives
expect(multiply(5, 1)).toBe(5);  // 5*1 = 5/1 = 5

// STRONG: Mutation detected
expect(multiply(5, 3)).toBe(15);  // 5*3 ≠ 5/3
```

### Tests Don't Assert Return Values

```typescript
// WEAK: No return value check
it('processes', () => {
  process(data);  // No assertion!
});

// STRONG: Asserts outcome
it('processes', () => {
  const result = process(data);
  expect(result).toEqual(expected);
});
```

---

## Important Rules

1. **ALWAYS restore original code** after each mutation
2. **Run tests immediately** after applying mutation
3. **One mutation at a time** - don't combine mutations
4. **Focus on changed code** - prioritize branch diff
5. **Track all results** - report full mutation summary

---

## Summary Report Template

After completing mutation testing, provide:

```markdown
## Mutation Testing Results

**Target**: `src/features/workout/utils.ts` (functions: X, Y, Z)
**Total Mutations**: 12
**Killed**: 9
**Survived**: 3
**Score**: 75%

### Surviving Mutants (Action Required)

| # | Location | Original | Mutated | Suggested Test |
|---|----------|----------|---------|----------------|
| 1 | line 42 | `>=` | `>` | Test boundary value |
| 2 | line 58 | `&&` | `\|\|` | Test mixed conditions |
| 3 | line 71 | `emit()` | removed | Verify event emission |

### Killed Mutants (Tests Effective)

- Line 35: `+` → `-` killed by `calculation.test.ts`
- Line 48: `true` → `false` killed by `validate.test.ts`
- ...
```

---

## Related Skills

- `systematic-debugging` - Root cause analysis
- `testing-conventions` - Query priority, expect.poll()
- `vue-integration-testing` - Page objects, browser mode
- `vitest-mocking` - Test doubles and mocking patterns
