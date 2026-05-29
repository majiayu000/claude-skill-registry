---
name: bb80-invariant-construction
description: "Extract invariants from specification, encode in types/structure, enable single-pass construction."
allowed_tools: "Read, Write, Edit"
---

# Big Bang 80/20: Invariant Construction

## Core Concept

**Big Bang 80/20** means single-pass construction in low-entropy domains.

Key: **Extract invariants from specification, encode in types, never violate.**

## What Are Invariants?

Invariants are **properties that must always be true**:

| Domain | Invariant | Rust Type |
|--------|-----------|-----------|
| Error handling | All errors Result<T,E> | `Result<T, Error>` |
| File paths | No traversal | `SafePath` wrapper |
| Age | 0 ≤ age ≤ 150 | `newtype Age(u8)` |
| Cache size | ≤ 10,000 entries | `BoundedCache<T>` |

## Type-Safe Design

```rust
// ✅ Invariant encoded in type
pub struct Age(u8);  // 0-255 enforced by type

impl Age {
    pub fn new(value: u8) -> Result<Self, Error> {
        if value > 150 {
            Err(Error::InvalidAge)
        } else {
            Ok(Age(value))
        }
    }
}
```

## Reference
See CLAUDE.md sections:
- Constitutional Rules (Type-First)
- Automatic (Type-safe design)
- Holographic Factory Metaphor (Corollary)
