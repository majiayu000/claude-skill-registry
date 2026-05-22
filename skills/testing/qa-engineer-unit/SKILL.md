---
name: qa-engineer-unit
description: Write focused unit tests for complex logic with Vitest
---

# QA Engineer for Unit Testing

## Responsibilities

- This skill ensures complex logic has focused, fast unit coverage.
- Tests remain small, explicit, and easy to reason about.
- Direct value assertions are preferred over elaborate mocks.

## When to use

Unit tests are optional and only required for complex code paths that are hard to cover in integration tests. Use this skill to supplement the required integration coverage. Do not use it to replace integration tests.

## Best practices

- Keep the test subject pure: avoid filesystem and network interactions, and use plain inputs and outputs.
- Prefer `describe` and focused `it` cases that each validate one behavior.
- Test titles must always start with `should`.

## Patterns to follow

- **Setup:** Create minimal fixtures with helpers (e.g., `makeMockEntity`, `makeSchema`, `makeMaps`).
- **Action:** Call the function under test directly with explicit inputs.
- **Assertions:** Verify each output field or side effect with `expect(...).toBe(...)` or `toEqual(...)`.
- **Coverage:** Include a case for success, edge cases, and missing-data behavior if relevant.

Example shape (simplified):

```ts
import { describe, expect, it } from 'vitest';
import { transformEntity } from './transform-entity';
import { makeMockEntity } from './__tests__/helpers';

describe('transformEntity', () => {
  it('should map identifiers from the map', () => {
    const entity = makeMockEntity();
    const idMap = new Map([[entity.id, 'new-id']]);

    const result = transformEntity(entity, { idMap });

    expect(result.id).toBe('new-id');
  });

  it('should report missing schema when not provided', () => {
    const entity = makeMockEntity();

    const result = transformEntity(entity, { idMap: new Map(), schema: {} });

    expect(Array.from(result.missingSchemas)).toEqual(['entity']);
  });
});
```
