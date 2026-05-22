---
name: 'test-factory-patterns'
description: 'This skill provides guidance for writing test factories in the Packmind codebase. It should be used when creating or updating factory functions in `**/test/*Factory.ts` files to ensure realistic test data with variety.'
---

# Test Factory Patterns

## Overview

Test factories create realistic test data with variety. Good factories generate multiple plausible instances and randomly select one, while allowing partial overrides. Poor factories return identical static data every time.

## The Pattern

### Good Factory Structure

A well-designed factory:

1. Defines an array of multiple realistic instances with meaningful, varied content
2. Uses `randomIn()` to select one instance randomly
3. Spreads partial overrides to allow customization

```typescript
import { Factory, randomIn } from '@packmind/test-utils';
import { Entity, createEntityId } from '@packmind/types';
import { v4 as uuidv4 } from 'uuid';

export const entityFactory: Factory<Entity> = (entity?: Partial<Entity>) => {
  const entities: Entity[] = [
    {
      id: createEntityId(uuidv4()),
      name: 'Meaningful Name One',
      slug: 'meaningful-name-one',
      content: `Realistic content that represents actual usage...`,
      // ... other fields with realistic values
    },
    {
      id: createEntityId(uuidv4()),
      name: 'Different Meaningful Name',
      slug: 'different-meaningful-name',
      content: `Different realistic content...`,
      // ... other fields with different realistic values
    },
    // Add 3-5 varied instances
  ];

  return {
    ...randomIn(entities),
    ...entity,
  };
};
```

### Bad Factory Structure (Avoid)

Avoid factories that return identical static data:

```typescript
// BAD: Always returns the same data
export const entityFactory: Factory<Entity> = (entity?: Partial<Entity>) => {
  return {
    id: createEntityId(uuidv4()),
    name: 'Test Entity', // Static, meaningless
    content: 'test content', // Not realistic
    ...entity,
  };
};
```

## Guidelines

### Content Quality

- Use realistic, domain-appropriate content (not "test", "foo", "bar")
- Include variety that reflects actual usage patterns
- Make names and slugs consistent with each other

### Instance Count

- Include 3-5 varied instances in the array
- Each instance should represent a plausible real-world case

### Required Imports

```typescript
import { Factory, randomIn } from '@packmind/test-utils';
```

### ID Generation

- Always generate fresh UUIDs for IDs using `createXxxId(uuidv4())`
- Never hardcode static UUIDs

### Override Support

- Always spread partial overrides last: `...entity`
- This allows tests to customize specific fields while keeping realistic defaults