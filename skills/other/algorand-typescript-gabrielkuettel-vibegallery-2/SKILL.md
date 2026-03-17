---
name: algorand-typescript
description: Syntax rules and patterns for Algorand TypeScript (PuyaTs) smart contracts. Use when writing TypeScript contract code, encountering Puya compiler errors, asking about AVM types or value semantics, needing guidance on storage patterns (GlobalState, BoxMap), or asking about clone(), arrays, or inner transactions. Strong triggers include "Puya compiler error", "How do I use uint64?", "What is clone() for?", "BoxMap not working", "AVM type error", "GlobalState not updating".
---

# Algorand TypeScript Rules

Critical syntax rules for Algorand TypeScript (PuyaTs) that prevent compiler errors and runtime failures.

**File Extension**: Contract files must use `.algo.ts` extension (e.g., `Counter.algo.ts`).

## Overview / Core Workflow

1. Identify the syntax issue or pattern needed
2. Apply the correct AVM-compatible pattern
3. Use `clone()` for complex types
4. Verify no union types or JavaScript `number`

## How to proceed

1. **Check the most critical rules below**
2. **Consult detailed reference files** for specific topics
3. **Apply the correct pattern** with proper AVM types
4. **Build to verify**: `algokit project run build`

## Important Rules / Guidelines

### Numbers: No JavaScript `number`

```typescript
// CORRECT
const amount: uint64 = Uint64(20)
const total: uint64 = amount + Uint64(100)

// INCORRECT - Compiler error
const amount = 20
```

**Numeric limits**: Algorand TypeScript supports integers up to 2^512. Use `biguint` for values exceeding uint64 (2^64 - 1).

### Value Semantics: Always `clone()`

```typescript
import { clone } from '@algorandfoundation/algorand-typescript'

const state = clone(this.appState.value)     // Read: clone
const updated = clone(state)                  // Modify: clone
this.appState.value = clone(updated)          // Write: clone
```

### No Union Types

```typescript
// CORRECT - Use boolean flags
let found = false
let foundItem: Item = { /* defaults */ }

// INCORRECT - Compiler error
let foundItem: Item | null = null
```

### Arrays: Clone Before Iterating

```typescript
// CORRECT
for (const item of clone(array)) { }
```

## Common Variations / Edge Cases

| Topic | Rule |
|-------|------|
| Numbers | Use `uint64` + `Uint64()`, never `number` |
| Strings | No `.length`; use `text !== ''` for empty check |
| Storage | Clone on read AND write for complex types |
| Arrays | Clone before iterating; indices must be `uint64` |
| Classes | No class properties; use module-level constants |
| Methods | Public = ABI method; private = subroutine |

## References / Further Reading

Detailed rules by topic:

- [Types and Values](./references/types-and-values.md) — AVM types, numbers, clone(), value semantics
- [Storage](./references/storage.md) — GlobalState, LocalState, BoxMap, MBR funding
- [Methods and ABI](./references/methods-and-abi.md) — Decorators, lifecycle methods, visibility
- [Transactions](./references/transactions.md) — Group transactions (gtxn), inner transactions (itxn)
- [Full Reference Index](./references/REFERENCE.md)
