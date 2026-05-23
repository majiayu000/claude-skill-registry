---
name: lean4-ffi-constructor-layout
description: |
  Lean 4 FFI memory layout for constructors with mixed object and scalar fields.
  Use when: (1) assertion violation "i < lean_ctor_num_objs(o)" accessing constructor fields,
  (2) assertion violation "offset >= lean_ctor_num_objs(o) * sizeof(void*)" with scalar getters,
  (3) lean_ctor_get_uint8/uint16/uint32 crashes or returns garbage, (4) creating FFI bindings
  for Lean inductives or structures with small integer fields (UInt8, UInt16, UInt32).
  Covers lean_alloc_ctor, lean_ctor_get, lean_ctor_set, and scalar field offset calculation.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# Lean 4 FFI Constructor Memory Layout

## Problem

When writing C FFI bindings for Lean 4 inductives or structures that contain both object
fields (pointers to Lean objects) and scalar fields (small integers like UInt8, UInt16),
the memory layout is non-obvious and incorrect assumptions cause assertion failures at runtime.

## Context / Trigger Conditions

- Assertion: `i < lean_ctor_num_objs(o)` when calling `lean_ctor_get(obj, i)`
- Assertion: `offset >= lean_ctor_num_objs(o) * sizeof(void*)` when calling scalar getters
- `lean_ctor_get_uint8`, `lean_ctor_get_uint16`, etc. return garbage values
- Creating FFI for inductives like:
  ```lean
  inductive SockAddr where
    | ipv4 (addr : IPv4Addr) (port : UInt16)  -- 1 object field, 2 scalar bytes
  ```

## Solution

### Memory Layout Rules

Lean 4 constructors store fields in this order:
1. **Object fields** (pointers): indices 0, 1, 2, ... accessible via `lean_ctor_get(obj, i)`
2. **Scalar fields** (small integers): stored AFTER all object fields

### Scalar Offset Calculation

The offset for scalar fields is relative to the START of the constructor's data, not the
start of the scalar section. Therefore:

```c
// For a constructor with N object fields:
scalar_offset = sizeof(void*) * num_object_fields + byte_offset_within_scalars
```

For the FIRST scalar field, the offset is `sizeof(void*) * num_object_fields`.

### Which Types Are Scalars?

- `UInt8`, `UInt16`, `UInt32`, `UInt64`, `Float`, `Bool` → **Scalar** in inductives
- `String`, `Array`, other inductives/structures → **Object** (pointer)
- A structure with ONLY scalar fields (like 4x UInt8) → Still uses constructor, but with 0 object fields

### Example: Correct FFI for Mixed Constructor

```lean
-- Lean definition
inductive SockAddr where
  | ipv4 (addr : IPv4Addr) (port : UInt16)  -- IPv4Addr is object, UInt16 is scalar
```

```c
// WRONG - treats UInt16 as object field
uint16_t port = lean_unbox(lean_ctor_get(addr, 1));  // CRASHES!

// CORRECT - UInt16 is scalar at offset after 1 object field
uint16_t port = lean_ctor_get_uint16(addr, sizeof(void*));  // Works!
```

### Creating Constructors with Mixed Fields

```c
// lean_alloc_ctor(tag, num_object_fields, num_scalar_bytes)

// For SockAddr.ipv4: 1 object field (IPv4Addr), 2 scalar bytes (UInt16)
lean_obj_res result = lean_alloc_ctor(0, 1, 2);
lean_ctor_set(result, 0, ipv4_obj);           // Object at index 0
lean_ctor_set_uint16(result, sizeof(void*), port);  // Scalar at offset 8 (64-bit)
```

### Structure with Only Scalars

```lean
structure IPv4Addr where
  a : UInt8
  b : UInt8
  c : UInt8
  d : UInt8
```

```c
// 0 object fields, 4 scalar bytes - scalar offset starts at 0
lean_obj_res ipv4 = lean_alloc_ctor(0, 0, 4);
lean_ctor_set_uint8(ipv4, 0, a);  // offset 0
lean_ctor_set_uint8(ipv4, 1, b);  // offset 1
lean_ctor_set_uint8(ipv4, 2, c);  // offset 2
lean_ctor_set_uint8(ipv4, 3, d);  // offset 3
```

## Verification

1. Build passes without Lean assertion violations
2. Run tests that exercise the FFI functions
3. Values round-trip correctly (create in Lean, read in C, write in C, read in Lean)

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Treating scalar as object | `i < lean_ctor_num_objs(o)` assertion | Use `lean_ctor_get_uintN` instead of `lean_ctor_get` |
| Wrong scalar offset | `offset >= ...` assertion or garbage values | Use `sizeof(void*) * num_obj_fields` as base offset |
| Wrong num_scalar_bytes | Memory corruption, crashes | Count actual bytes: UInt8=1, UInt16=2, UInt32=4, etc. |

## Notes

- On 64-bit systems, `sizeof(void*)` is 8
- The scalar offset is in BYTES, not in field indices
- Multiple scalars are packed contiguously after the object fields
- Lean's runtime does NOT automatically box small integers in inductives—they're truly stored inline

## References

- Lean 4 source: `lean.h` contains the constructor macros with assertions
- FFI patterns observed in Lean's own C runtime and mathlib FFI code
