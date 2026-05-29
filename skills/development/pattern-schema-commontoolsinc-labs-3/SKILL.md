---
name: pattern-schema
description: Design schemas.tsx with Input/Output types for patterns
user-invocable: false
---

Use `Skill("ct")` for ct CLI documentation when running commands.

# Schema Design Phase

## Goal
Create `schemas.tsx` with all data types and Input/Output types BEFORE any pattern code.

## Read First
- `docs/common/concepts/types-and-schemas/default.md`
- `docs/common/concepts/types-and-schemas/writable.md`
- `docs/common/concepts/pattern.md` (Input/Output section)

## Rules
1. **ALWAYS use `pattern<Input, Output>()`** - Never use single-type `pattern<State>()`. Single-type patterns cannot be tested via `.send()`.
2. Every editable field needs `Writable<>` in Input type (for write access)
3. **Output types never use `Writable<>`** - they reflect returned data shape
4. Fields that could be undefined initially: use `Default<T, value>`
5. Actions in Output type: `Stream<T>` (enables testing and linking)
6. Sub-patterns need `[NAME]: string` and `[UI]: VNode` in Output type

## Template

```tsx
import { Default, NAME, Stream, UI, VNode, Writable } from "commontools";

// ============ DATA TYPES ============
export interface Item {
  name: Default<string, "">;
  done: Default<boolean, false>;
}

// ============ PATTERN INPUT/OUTPUT ============
export interface ItemInput {
  item: Writable<Item>;  // Writable in Input = pattern will modify
}

export interface ItemOutput {
  [NAME]: string;        // Required for sub-patterns
  [UI]: VNode;           // Required for sub-patterns
  item: Item;            // No Writable in Output
  toggle: Stream<void>;  // Actions as Stream<T>
}
```

## Done When
- All data types defined with correct Writable/Default wrapping
- All Input/Output types defined for each sub-pattern
- No TypeScript errors: `deno task ct check schemas.tsx --no-run`
