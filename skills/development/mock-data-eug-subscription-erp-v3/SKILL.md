---
name: mock-data
description: Creates typed mock data files in src/data/ following project conventions. Use when needing test data for new features or components.
---

# Mock Data Generator Skill

Creates typed mock data files following project patterns.

## File Pattern

```text
src/data/mock-{feature}.ts
```

## Template Structure

```typescript
// src/data/mock-{feature}.ts

export interface {Feature}Data {
    id: string;
    name: string;
    // Add fields based on requirements
}

export const mock{Feature}Data: {Feature}Data = {
    id: "1",
    name: "Example",
};

// For arrays:
export const mock{Feature}List: {Feature}Data[] = [
    { id: "1", name: "Item 1" },
    { id: "2", name: "Item 2" },
];
```

## Conventions

1. **Filename**: kebab-case with `mock-` prefix
2. **Named exports**: Both interface and data
3. **Type-first**: Define interface before data
4. **Realistic data**: Use meaningful values, not "test123"

## Examples

See these files for reference patterns:

- `src/data/mock-order.ts`
- `src/data/mock-project.ts`
- `src/data/mock-unmatched-items.ts`

## Usage with TanStack Query

```typescript
// hooks/use{Feature}.ts
import { useQuery } from "@tanstack/react-query";
import { mock{Feature}Data, {Feature}Data } from "../data/mock-{feature}";

async function fetch{Feature}Data(): Promise<{Feature}Data> {
    await new Promise((r) => setTimeout(r, 500)); // Simulate API
    return mock{Feature}Data;
}

export function use{Feature}() {
    return useQuery({
        queryKey: ["{feature}"],
        queryFn: fetch{Feature}Data,
    });
}
```
