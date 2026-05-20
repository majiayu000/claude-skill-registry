---
name: safe-over-unsafe
description: Use when designing safe public APIs that wrap unsafe Rust code, adding unsafe blocks to existing types, reviewing unsafe code for soundness, or creating new types backed by raw pointers, MaybeUninit, or FFI
---

# Safe API Design Over Unsafe Rust

Module privacy is the soundness boundary — not the `unsafe` keyword. The
`unsafe {}` block is a syntax marker; the real safety mechanism is private
fields behind a safe public API, within a module (or crate) where all code
is trusted.

## When to Use

- Designing a new type backed by `MaybeUninit`, raw pointers, or FFI
- Adding `unsafe` blocks to existing code for performance
- Reviewing unsafe code for soundness
- Implementing `Send`/`Sync`/`Drop` for types with unsafe internals

## Design Checklist

Follow every step. Skipping any step is how soundness bugs happen.

### 1. Establish the Safety Boundary

- **Private fields, private module, safe public API.** Every public method
  — safe or not — is part of the soundness proof. Changing `<` to `<=` in
  a safe bounds check can make all unsafe blocks unsound.
- **Consider crate-level isolation.** Consumer crate uses
  `#![forbid(unsafe_code)]`; unsafe lives in a dedicated crate.
- **Enable lints at the crate root:**
  ```rust
  #![deny(unsafe_op_in_unsafe_fn)]
  #![deny(clippy::undocumented_unsafe_blocks)]
  ```

### 2. Document Invariants at the Type Level

Two kinds of invariants exist — conflating them causes bugs:

- **Validity invariant**: Must hold at ALL times. Violation is instant UB
  even if the value is never "used." (Example: `bool` must be 0 or 1.)
- **Safety invariant**: Must hold at API boundaries. May be temporarily
  violated internally. (Example: `Vec`'s `len <= cap`.)

Document both in a module-level `//!` or struct-level `///` doc comment:
```rust
/// # Invariants
/// - `len <= CAPACITY` (safety)
/// - Slots `[head..head+len)` (mod cap) are initialized (safety)
/// - Initialized slots contain valid `T` values (validity)
```

### 3. Enforce at Compile Time First

Every invariant should be evaluated: can this be a const assertion,
a NonZero type, or a typestate transition instead of a runtime check?

```rust
const { assert!(N > 0 && N.is_power_of_two()) }; // compile-time
```

Compile-time enforcement eliminates entire bug classes. Runtime
`debug_assert!` is the fallback — use `assert!` in public API
preconditions that guard unsafe code in the implementation.

### 4. Write SAFETY Comments as Proof Sketches

Every `// SAFETY:` comment must argue invariant preservation, not just
state a fact. Use this structure:

```rust
// SAFETY: [what unsafe operation is being performed]
// Invariant: [which safety invariant holds here — and WHY from the code path]
// Implies: [which validity invariant this satisfies for the unsafe op]
// Preserved: [what invariants remain intact after this operation]
```

Bad: `// SAFETY: index is in bounds`
Good: `// SAFETY: physical = idx & MASK, so physical < CAPACITY (mask clears
// high bits). The element is initialized because idx < self.len, and our
// safety invariant guarantees slots [head..head+len) are initialized.
// This satisfies assume_init_ref's requirement that the value is valid T.`

For `unsafe fn`, use `# Safety` doc sections documenting caller obligations.

### 5. Get Variance, PhantomData, and Send/Sync Right

**Incorrect Send/Sync is the #1 real-world unsafe soundness bug** (tokio
RUSTSEC-2025-0023, lock_api RUSTSEC-2020-0070, windows RUSTSEC-2022-0008).

| Situation | Action |
|-----------|--------|
| Type uses `[MaybeUninit<T>; N]` | Auto-derive is correct. No PhantomData needed. |
| Type uses raw pointers | Add `PhantomData<T>` for owned data (covariant, correct Send/Sync). |
| Need manual Send/Sync | **Red flag.** Bound generics: `unsafe impl<T: Send + Sync> Sync for MyType<T> {}` |
| Unsure about variance | If the type *owns* T, it should be covariant (like Vec). Use `PhantomData<T>`. |

Always prefer auto-derivation. Add compile-time assertions:
```rust
const _: () = {
    fn assert_send<T: Send>() { fn requires_send<S: Send>() {} requires_send::<MyType<T>>(); }
    fn assert_sync<T: Sync>() { fn requires_sync<S: Sync>() {} requires_sync::<MyType<T>>(); }
};
```

### 6. Handle Panic Safety

If an operation modifies state in multiple steps and any step can panic
(e.g., `T::drop()`, `T::clone()`), use the **decrement-before-drop** or
**guard** pattern:

```rust
// Decrement-before-drop: len reflects reality even if drop panics
while self.len > 0 {
    self.len -= 1;
    unsafe { self.buf[self.len].assume_init_drop(); }
}
```

Test with a deliberately-panicking `Drop` impl via `catch_unwind`.

### 7. Defend Against Generic Parameters

Unsafe code cannot trust safe trait implementations. `T::drop()` can
panic. `T::clone()` can panic. `Ord` impls can be inconsistent. Write
defensively so broken trait impls cause wrong results, never UB.

## Verification Layers

All three are required. No single tool is sufficient.

| Layer | Tool | What It Catches | Required |
|-------|------|----------------|----------|
| Dynamic UB | `cargo +nightly miri test` | Aliasing, uninit, alignment, use-after-free | **Every test run** |
| Aliasing model | `MIRIFLAGS="-Zmiri-tree-borrows" cargo +nightly miri test` | Tree Borrows violations | **CI** |
| Reference model | proptest vs known-correct safe impl (e.g., VecDeque) | Logic errors, edge cases | **Every test run** |
| Drop correctness | `DropTracker` with `Arc<AtomicUsize>` | Double-drop, leaks | **Every test run** |
| Bounded proof | Kani proof harnesses | Exhaustive invariant verification | **Critical code** |

## Risk Checklist

Before declaring unsafe code "done," verify each:

- [ ] No manual `unsafe impl Send/Sync` without restrictive bounds on generics
- [ ] All values crossing safe→unsafe boundary are validated
- [ ] `MaybeUninit`: using `write()` for init, tracking init state, never `mem::uninitialized`
- [ ] Multi-step operations handle panics (guard/decrement-before-drop pattern)
- [ ] `len`/`capacity` updated atomically with the memory operation
- [ ] Public API preconditions use `assert!` (not just `debug_assert!`)
- [ ] PhantomData matches ownership semantics (covariant for owned data)
- [ ] Miri passes under both Stacked Borrows and Tree Borrows

## Pattern Catalog

| Pattern | When to Use | Exemplar |
|---------|------------|----------|
| Private fields + safe API | Always | std Vec |
| Crate-level `#![forbid(unsafe_code)]` | Multi-crate projects | Fuchsia, gossip-rs |
| Compile-time const assertions | Numeric invariants | RingBuffer power-of-2 |
| `MaybeUninit` + init tracking | Uninitialized storage | std MaybeUninit docs |
| PhantomData for variance | Raw pointer containers | Rustonomicon Vec |
| Guard struct for panic safety | Multi-step mutations | hashbrown HashMap |
| Typestate (generic state param) | State-dependent operations | serde Serializer |
| Sealed trait | Fixed impl set | zerocopy |
| `unsafe trait` as capability gate | External impls needed | bytemuck Pod |
| Lifetime-encoded validity | Temporal access control | crossbeam-epoch Guard |

## References

1. [Rustonomicon: Working with Unsafe](https://doc.rust-lang.org/nomicon/working-with-unsafe.html)
2. [Ralf Jung: The Scope of Unsafe](https://www.ralfj.de/blog/2016/01/09/the-scope-of-unsafe.html)
3. [Unsafe Code Guidelines: Glossary](https://rust-lang.github.io/unsafe-code-guidelines/glossary.html)
4. [std::mem::MaybeUninit](https://doc.rust-lang.org/std/mem/union.MaybeUninit.html)
5. [Miri](https://github.com/rust-lang/miri)
6. [Kani Rust Verifier](https://model-checking.github.io/kani/)
7. [Stacked Borrows (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/)
8. [Tree Borrows](https://www.ralfj.de/blog/2023/06/02/tree-borrows.html)
9. [Fuchsia Unsafe Guidelines](https://fuchsia.dev/fuchsia-src/development/languages/rust/unsafe)
10. [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
11. [RustSec Advisory Database](https://rustsec.org/advisories/)
