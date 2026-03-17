---
name: compact-core:language-reference
description: Use when writing Compact smart contracts and need reference for primitive types (Field, Boolean, Uint), composite types (struct, enum, Vector, Bytes), circuit/witness syntax, control flow (if/else, for loops, assert), or module system (import, include, export).
---

# Compact Language Reference

Complete reference for the Compact smart contract language used on Midnight Network.

## Quick Reference

### Primitive Types

| Type | Description | Example |
|------|-------------|---------|
| `Field` | ZK-native field element (~254 bits) | `const f: Field = 42;` |
| `Boolean` | True/false value | `const b: Boolean = true;` |
| `Uint<N>` | Unsigned integer (N bits, N ≤ 248) | `const n: Uint<64> = 100;` |

### Composite Types

| Type | Description | Example |
|------|-------------|---------|
| `Bytes<N>` | Fixed-size byte array | `const h: Bytes<32> = ...;` |
| `struct` | Named record type | `struct Point { x: Field, y: Field }` |
| `enum` | Tagged union | `enum Maybe<T> { Some(T), None }` |
| `Vector<T, N>` | Fixed-size array | `const v: Vector<Field, 3> = [1, 2, 3];` |

### Special Types

| Type | Description | Example |
|------|-------------|---------|
| `Opaque<'string'>` | UTF-8 string from TypeScript | `witness get_name(): Opaque<'string'>;` |
| `Opaque<'Uint8Array'>` | Binary data from TypeScript | `witness get_data(): Opaque<'Uint8Array'>;` |

## Circuit Syntax

```compact
// Public circuit callable from TypeScript
export circuit transfer(to: Bytes<32>, amount: Uint<64>): [] {
    // Circuit body
}

// Private helper circuit
circuit helper(x: Field): Field {
    return x * x;
}
```

## Witness Syntax

```compact
// Declaration (implemented in TypeScript)
witness get_private_key(): Bytes<32>;

// Usage in circuit
export circuit sign(message: Bytes<32>): Bytes<64> {
    const key = get_private_key();
    // Use key...
}
```

## Control Flow

```compact
// Conditional
if (condition) {
    // then branch
} else {
    // else branch
}

// Bounded loop (bounds must be compile-time constant)
for i in 0..10 {
    // loop body
}

// Assertion
assert condition, "Error message";
```

## Module System

```compact
// Import specific items
import { hash } from "CompactStandardLibrary";

// Include entire file
include "utils.compact";

// Export for external use
export circuit public_fn(): Field { ... }
```

## References

For detailed documentation on each topic:

- [Type System](./references/type-system.md) - Complete type reference with constraints
- [Circuits](./references/circuits.md) - Circuit and witness patterns
- [Control Flow](./references/control-flow.md) - Conditionals, loops, assertions
- [Modules](./references/modules.md) - Import, include, export, COMPACT_PATH
