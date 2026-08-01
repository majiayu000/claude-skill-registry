---
name: hardened-outline-driven-development-for-rust
description: 'HODD-RUST: Validation-first Rust development. Strictly validation-first
  before-and-after(-and-while) planning and execution. Merges Type-driven + Spec-first
  + Proof-driven + Design-by-contracts. Use f'
---

---
name: hardened-outline-driven-development-for-rust
description: HODD-RUST: Validation-first Rust development. Strictly validation-first before-and-after(-and-while) planning and execution. Merges Type-driven + Spec-first + Proof-driven + Design-by-contracts. Use for Rust projects requiring formal verification, safety proofs, comprehensive validation, or when working with unsafe code, concurrency, or FFI boundaries. This skill provides both reference documentation AND execution capabilities for the full PLAN -> CREATE -> VERIFY -> REMEDIATE workflow.
---

# HODD-RUST: Hard Outline-Driven Development for Rust

## Philosophy: Strict Validation-First

Strictly validation-first before-and-after(-and-while) planning and execution.

**BEFORE** (Planning Phase):

- Design type specifications (Rust types/Flux)
- Design formal specifications (Quint)
- Design proofs (Lean4/Kani)
- Design contracts (`contracts` crate)

**WHILE** (Execution Phase):

- CREATE verification artifacts from plan
- VERIFY each artifact as created
- REMEDIATE failures immediately

**AFTER** (Completion):

- Run full validation pipeline
- Ensure all stages pass
- Document verification coverage

**Four Paradigms**:

- **Type-driven**: Rust's type system + Flux for refined types
- **Spec-first**: Quint specifications and Kani bounded model checking
- **Proof-driven**: Lean4 formal proofs for critical algorithms
- **Design-by-contracts**: `contracts` crate for pre/postconditions and invariants

---

## When to Use

- Rust projects requiring formal verification
- Safety proofs for critical code
- Unsafe code validation
- Concurrent/parallel code with atomics
- FFI boundaries
- Lock-free algorithms

---

## Workflow Overview

```nomnoml
[<start>Requirements] -> [Phase 1: PLAN]
[Phase 1: PLAN|
  Safety analysis
  Tool selection
  Design validations
] -> [Phase 2: CREATE]
[Phase 2: CREATE|
  contracts annotations
  Kani proofs
  Loom tests
] -> [Phase 3: VERIFY]
[Phase 3: VERIFY|
  Run validation pipeline
  Basic -> Type -> Contract -> Proof
] -> [Phase 4: REMEDIATE]
[Phase 4: REMEDIATE|
  Fix failures
  Re-verify
] -> [<end>Success]
```

---

## Tool Selection Decision Matrix

| Scenario                     | Primary Tool  | Secondary     | Avoid         |
| ---------------------------- | ------------- | ------------- | ------------- |
| Unsafe code, raw pointers    | **Miri**      | Kani          | -             |
| Undefined behavior detection | **Miri**      | -             | CI (too slow) |
| Concurrent code, atomics     | **Loom**      | Miri          | Kani          |
| Lock-free algorithms         | **Loom**      | -             | -             |
| Array bounds verification    | **Flux**      | Kani          | -             |
| Integer overflow proofs      | **Kani**      | Flux          | -             |
| Public API contracts         | **contracts** | Flux          | -             |
| Algorithm correctness        | **Kani**      | Lean4         | -             |
| Protocol state machines      | **Quint**     | Typestate     | -             |
| FFI boundaries               | **Miri**      | Manual review | -             |

---

## Tool Stack

| Tool                    | Usage                  | When to Use                   |
| ----------------------- | ---------------------- | ----------------------------- |
| rustc, rustfmt, Clippy  | Standard toolchain     | Always                        |
| cargo-audit, cargo-deny | Security/dependency    | CI mandatory                  |
| Miri                    | Runtime UB detection   | Unsafe code, FFI (local only) |
| Loom                    | Concurrency testing    | Atomics, lock-free            |
| Flux                    | Refined types          | Array bounds, overflow        |
| contracts               | Pre/postconditions     | Public APIs                   |
| Kani                    | Bounded model checking | Overflow, assertions          |
| Lean4                   | Formal proofs          | Algorithms                    |
| Quint                   | Spec-first design      | Protocol specs                |

---

## 1. Type-Driven Development

### Rust Native Type Patterns

#### Typestate Pattern

Encode state machines in the type system; invalid states become unrepresentable.

```rust
use std::marker::PhantomData;

// States as zero-sized types
struct Draft;
struct Published;
struct Archived;

// State encoded in type parameter
struct Article<State> {
    content: String,
    _state: PhantomData<State>,
}

impl Article<Draft> {
    fn publish(self) -> Article<Published> {
        Article { content: self.content, _state: PhantomData }
    }
}

impl Article<Published> {
    fn archive(self) -> Article<Archived> {
        Article { content: self.content, _state: PhantomData }
    }
}

// COMPILE ERROR: Cannot archive a draft directly
// let archived = draft_article.archive();
```

**Commands**:

```bash
# Verify typestate transitions compile correctly
cargo check

# Ensure no runtime state checks needed
cargo clippy -- -D clippy::unnecessary_unwrap
```

#### Newtype Pattern

Wrap primitives to prevent semantic confusion.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct UserId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct OrderId(u64);

// COMPILE ERROR: Cannot pass OrderId where UserId expected
fn get_user(id: UserId) -> User { /* ... */ }
```

**Commands**:

```bash
# Generate newtype boilerplate
cargo add derive_more

# Validate type distinctions
cargo check 2>&1 | grep -E "(expected|found).*Id"
```

#### Phantom Types

Carry compile-time information without runtime cost.

```rust
use std::marker::PhantomData;

struct Meters;
struct Feet;

struct Distance<Unit> {
    value: f64,
    _unit: PhantomData<Unit>,
}

impl Distance<Meters> {
    fn to_feet(self) -> Distance<Feet> {
        Distance { value: self.value * 3.28084, _unit: PhantomData }
    }
}
```

### Flux: Refined Types (Advanced)

**Installation**:

```bash
# Install Flux (requires nightly)
rustup install nightly-2024-04-15
cargo install flux-rs

# Add to project
# Cargo.toml
[dependencies]
flux-rs = "0.1"
```

**Usage**:

```rust
#[flux::sig(fn(x: i32{x > 0}) -> i32{v: v > x})]
fn increment_positive(x: i32) -> i32 {
    x + 1
}

#[flux::sig(fn(v: &[i32][@n]) -> i32 requires n > 0)]
fn first_element(v: &[i32]) -> i32 {
    v[0]  // Proved safe: n > 0 guarantees non-empty
}
```

**Commands**:

```bash
# Run Flux refinement type checker
cargo flux

# Check specific file
cargo flux -- src/lib.rs

# Verbose output for debugging
FLUX_LOG=debug cargo flux
```

**Pass Criteria**:

- [ ] All type patterns encode domain invariants
- [ ] No `unwrap()` on domain-critical paths
- [ ] Phantom types prevent unit confusion
- [ ] Flux refinements verify bounds/preconditions

**Fail Actions**:

- Type pattern insufficient -> Add more states or constraints
- Flux verification fails -> Strengthen preconditions or fix logic
- Compile error on valid code -> Relax phantom constraints

---

## 2. Validation-First / Architecture Validation

### External: Quint Prototyping

Model Rust state machines in Quint before implementation.

**Workflow**:

```
1. Write Quint spec modeling Rust types/transitions
2. Verify invariants and temporal properties
3. Generate test traces
4. Implement Rust code matching spec
5. Compare Rust execution traces to Quint traces
```

**Commands**:

```bash
# Typecheck Quint spec
quint typecheck specs/state_machine.qnt

# Simulate to explore behaviors
quint run specs/state_machine.qnt --max-steps=1000

# Verify safety invariants
quint verify specs/state_machine.qnt --invariant=NoDataRace
quint verify specs/state_machine.qnt --invariant=NoDeadlock

# Verify liveness
quint verify specs/state_machine.qnt --temporal=EventuallyCompletes

# Generate traces for Rust tests
quint run specs/state_machine.qnt --out-itf=traces/scenario1.itf.json
```

**Example Quint Spec for Rust**:

```quint
module RustChannel {
    type Message = { id: int, payload: str }

    var buffer: List[Message]
    var capacity: int

    action send(msg: Message): bool = all {
        length(buffer) < capacity,
        buffer' = buffer.append(msg),
    }

    action receive(): Message = {
        require(length(buffer) > 0)
        val msg = buffer.head()
        buffer' = buffer.tail()
        msg
    }

    // Safety: buffer never exceeds capacity
    val SafetyInvariant = length(buffer) <= capacity

    // Liveness: sent messages eventually received
    temporal Liveness = always(eventually(length(buffer) == 0))
}
```

### Internal: Kani Model Checker

Use for critical paths, unsafe code, and algorithmic correctness.

**Installation**:

```bash
# Install Kani
cargo install --locked kani-verifier
kani setup

# Or via cargo-binstall (faster)
cargo binstall kani-verifier
kani setup
```

**Usage**:

```rust
#[cfg(kani)]
mod verification {
    use super::*;

    #[kani::proof]
    fn verify_no_overflow() {
        let x: u32 = kani::any();
        let y: u32 = kani::any();

        // Assume inputs are bounded
        kani::assume(x < 1000);
        kani::assume(y < 1000);

        // Verify no overflow
        let result = checked_add(x, y);
        kani::assert(result.is_some(), "addition should not overflow");
    }

    #[kani::proof]
    #[kani::unwind(10)]  // Bound loop iterations
    fn verify_sorting_invariant() {
        let mut arr: [i32; 5] = kani::any();
        bubble_sort(&mut arr);

        // Verify sorted
        for i in 0..arr.len() - 1 {
            kani::assert(arr[i] <= arr[i + 1], "array should be sorted");
        }
    }
}
```

**Commands**:

```bash
# Run all Kani proofs
cargo kani

# Run specific proof
cargo kani --harness verify_no_overflow

# Concrete playback (reproduce counterexample)
cargo kani --harness verify_no_overflow --concrete-playback=print

# Check for specific issues
cargo kani --checks=overflow,bounds,pointer

# Generate coverage report
cargo kani --coverage

# Increase solver timeout
cargo kani --solver-timeout 300

# Use specific SAT solver
cargo kani --solver cadical
```

**Kani Attributes Reference**:

```rust
#[kani::proof]              // Mark as verification harness
#[kani::unwind(N)]          // Bound loop unwinding
#[kani::solver(cadical)]    // Specify SAT solver
#[kani::stub(foo, bar)]     // Replace foo with bar for verification

// Kani APIs
kani::any::<T>()            // Symbolic value of type T
kani::assume(cond)          // Assume condition holds
kani::assert(cond, msg)     // Assert condition, fail if false
kani::cover(cond, msg)      // Coverage goal
```

**Pass Criteria**:

- [ ] All Kani proofs pass (VERIFICATION SUCCESSFUL)
- [ ] No overflow/bounds/null pointer issues
- [ ] Coverage goals met
- [ ] Critical paths verified

**Fail Actions**:

- Verification failure -> Analyze counterexample, fix code
- Timeout -> Add `#[kani::unwind]` bounds or simplify
- Unsupported feature -> Use `#[kani::stub]` or refactor

---

## 3. Proof-Driven Development

### Lean 4 for Rust Algorithm Verification

Prove algorithm correctness in Lean 4, then implement in Rust.

**Workflow**:

```
1. Formalize algorithm in Lean 4
2. Prove correctness properties
3. Extract/translate to Rust
4. Verify Rust matches Lean specification
```

**Commands**:

```bash
# Initialize Lean 4 project
lake init rust_proofs

# Build proofs
lake build

# Check specific file
lake env lean --run src/Algorithm.lean

# Interactive development (in editor with Lean 4 extension)
# Use #check, #eval, #reduce for exploration
```

**Example Lean 4 Proof**:

```lean
-- Lean 4 specification for binary search
def binarySearch (arr : Array Int) (target : Int) : Option Nat :=
  go 0 arr.size
where
  go (lo hi : Nat) : Option Nat :=
    if lo >= hi then none
    else
      let mid := (lo + hi) / 2
      if arr[mid]! < target then go (mid + 1) hi
      else if arr[mid]! > target then go lo mid
      else some mid
  termination_by hi - lo

-- Correctness theorem
theorem binarySearch_correct (arr : Array Int) (target : Int)
    (sorted : forall i j, i < j -> j < arr.size -> arr[i]! <= arr[j]!) :
    match binarySearch arr target with
    | some idx => arr[idx]! = target
    | none => forall i, i < arr.size -> arr[i]! != target := by
  sorry  -- Proof to be completed
```

**Pass Criteria**:

- [ ] All theorems proven (no `sorry`)
- [ ] Termination verified
- [ ] Rust implementation matches Lean spec

**Fail Actions**:

- Proof stuck -> Use `sorry`, analyze, refine approach
- Termination failure -> Add decreasing measure

---

## 4. Design by Contracts

### Static Assertions First (PREFER OVER CONTRACTS)

**Principle**: Use compile-time static assertions before runtime contracts. If a property can be verified at compile time, do NOT add a runtime contract for it.

**Hierarchy**: `Static Assertions > Contracts > Runtime Checks`

**Installation**:

```toml
# Cargo.toml
[dependencies]
static_assertions = "1.1"
```

**Usage**:

```rust
use static_assertions::{assert_eq_size, assert_impl_all, const_assert};

// Size constraints - checked at compile time
assert_eq_size!(u64, usize);  // Ensure 64-bit platform
assert_eq_size!([u8; 16], u128);

// Trait bounds - verified statically
assert_impl_all!(String: Send, Sync, Clone);
assert_impl_all!(Buffer: Send);

// Const assertions - arbitrary boolean conditions
const_assert!(std::mem::size_of::<usize>() >= 4);
const_assert!(MAX_BUFFER_SIZE > 0);
const_assert!(MAX_BUFFER_SIZE <= 1024 * 1024);  // 1MB limit

// Type relationships
use static_assertions::assert_type_eq_all;
assert_type_eq_all!(u32, u32);  // Types must be identical
```

**Const Functions for Compile-Time Validation**:

```rust
const fn validate_config(size: usize, alignment: usize) -> bool {
    size > 0 && size.is_power_of_two() && alignment > 0
}

const BUFFER_SIZE: usize = 256;
const ALIGNMENT: usize = 8;

// Fails compilation if validation fails
const _: () = assert!(validate_config(BUFFER_SIZE, ALIGNMENT));
```

**Build-Time Assertions in Const Context**:

```rust
pub struct Config<const N: usize> {
    data: [u8; N],
}

impl<const N: usize> Config<N> {
    // Compile-time validation via const
    const VALID: () = assert!(N > 0 && N <= 4096, "N must be 1..=4096");

    pub const fn new() -> Self {
        let _ = Self::VALID;  // Force validation
        Self { data: [0; N] }
    }
}

// Compile error: N=0 violates constraint
// let bad: Config<0> = Config::new();
```

**When to Use Static vs Contracts** (Expanded Hierarchy):

| Property                       | Static                   | test_*         | debug_*           | Always-on   |
| ------------------------------ | ------------------------ | -------------- | ----------------- | ----------- |
| Type size/alignment            | `assert_eq_size!`        | -              | -                 | -           |
| Trait implementations          | `assert_impl_all!`       | -              | -                 | -           |
| Const value bounds             | `const_assert!`          | -              | -                 | -           |
| Generic const params           | `const { assert!(...) }` | -              | -                 | -           |
| Expensive O(n)+ verification   | -                        | `test_ensures` | -                 | -           |
| Reference impl equivalence     | -                        | `test_ensures` | -                 | -           |
| Internal state invariants      | -                        | -              | `debug_invariant` | -           |
| Development preconditions      | -                        | -              | `debug_requires`  | -           |
| Public API input validation    | -                        | -              | -                 | `requires`  |
| Safety-critical postconditions | -                        | -              | -                 | `ensures`   |
| Production state invariants    | -                        | -              | -                 | `invariant` |

**Legend**: `-` = Do not use for this property

**Commands**:

```bash
# Static assertions verified during compilation
cargo check

# Build fails if any static assertion fails
cargo build 2>&1 | grep "assertion failed"
```

**Pass Criteria**:

- [ ] All compile-time verifiable properties use static assertions
- [ ] No contracts (debug/test/runtime) for properties provable at compile time
- [ ] Const functions used for complex compile-time validation
- [ ] Generic const parameters validated in const context
- [ ] If static assertions suffice, NO additional contracts added

**Fail Actions**:

- Static assertion fails -> Fix the violated invariant or adjust constraints
- Property not statically verifiable -> Fall through to debug/test contracts first, then runtime if necessary

---

### Debug and Test Contracts (PREFER OVER RUNTIME)

**Principle**: Use the least-cost assertion level that catches the bug. Debug/test contracts are stripped in release builds, reducing production overhead.

**Contract Modes** (from `contracts` crate):

| Mode       | Attributes                                           | Internal Mechanism          | When Active       |
| ---------- | ---------------------------------------------------- | --------------------------- | ----------------- |
| **Test**   | `test_requires`, `test_ensures`, `test_invariant`    | `if cfg!(test) { assert! }` | Test builds only  |
| **Debug**  | `debug_requires`, `debug_ensures`, `debug_invariant` | `debug_assert!`             | Debug builds only |
| **Always** | `requires`, `ensures`, `invariant`                   | `assert!`                   | All builds        |

**When to Use Each Mode**:

| Scenario                                         | Use       | Rationale                            |
| ------------------------------------------------ | --------- | ------------------------------------ |
| Expensive O(n)+ verification (e.g., `is_sorted`) | `test_*`  | Too slow for debug builds            |
| Reference implementation equivalence             | `test_*`  | Only needed for correctness proofs   |
| Internal state invariants                        | `debug_*` | Development aid, not production need |
| Development-time preconditions                   | `debug_*` | Catch bugs early, strip in release   |
| Public API input validation                      | Always-on | External users need protection       |
| Safety-critical postconditions                   | Always-on | Must verify in production            |

**Example - Progressive Contract Levels**:

```rust
use contracts::*;

impl SortedVec {
    // EXPENSIVE: Only verify sorting in tests (O(n) check)
    #[test_ensures(self.is_sorted(), "must maintain sorted invariant")]
    pub fn insert(&mut self, value: i32) {
        let pos = self.data.binary_search(&value).unwrap_or_else(|p| p);
        self.data.insert(pos, value);
    }

    // CHEAP: Check in debug builds (O(1) check)
    #[debug_requires(!self.data.is_empty(), "cannot pop from empty")]
    #[debug_ensures(self.data.len() == old(self.data.len()) - 1)]
    pub fn pop(&mut self) -> Option<i32> {
        self.data.pop()
    }

    // CRITICAL: Always check public API boundaries
    #[requires(index < self.data.len(), "index out of bounds")]
    pub fn get(&self, index: usize) -> i32 {
        self.data[index]
    }
}
```

**Decision Flow**:

```
Can type system encode it? ──yes──> Use types (typestate, newtype)
         │no
         v
Verifiable at compile-time? ──yes──> static_assertions / const_assert!
         │no
         v
Expensive O(n)+ check? ──yes──> test_* (test builds only)
         │no
         v
Internal development aid? ──yes──> debug_* (debug builds only)
         │no
         v
Must enforce in production? ──yes──> Always-on contracts
         │no
         v
Consider if check is needed at all
```

**Pass Criteria**:

- [ ] Expensive O(n)+ checks use `test_*` variants
- [ ] Internal invariants use `debug_*` variants
- [ ] Always-on contracts only for properties that MUST be checked in production
- [ ] No performance regression from contract overhead in release builds

**Fail Actions**:

- Test contract fails -> Fix algorithm or strengthen test coverage
- Debug contract fails -> Fix internal logic, add regression test
- Need expensive check in production -> Reconsider design or accept overhead

---

### The `contracts` Crate (Runtime Properties - Use Sparingly)

**Installation**:

```toml
# Cargo.toml
[dependencies]
contracts = "0.6"

[features]
# Enable contract checking in debug builds
default = ["contracts/mirai_assertions"]
```

**Usage**:

```rust
use contracts::*;

#[invariant(self.len > 0, "buffer must never be empty")]
struct Buffer {
    data: Vec<u8>,
    len: usize,
}

impl Buffer {
    #[requires(capacity > 0, "capacity must be positive")]
    #[ensures(ret.len == capacity, "buffer initialized to capacity")]
    pub fn new(capacity: usize) -> Self {
        Buffer {
            data: vec![0; capacity],
            len: capacity,
        }
    }

    #[requires(!self.is_empty(), "cannot read from empty buffer")]
    #[ensures(ret.is_some() -> self.len == old(self.len) - 1)]
    pub fn read(&mut self) -> Option<u8> {
        if self.len > 0 {
            self.len -= 1;
            Some(self.data[self.len])
        } else {
            None
        }
    }

    #[requires(self.len < self.data.len(), "buffer not full")]
    #[ensures(self.len == old(self.len) + 1)]
    pub fn write(&mut self, byte: u8) {
        self.data[self.len] = byte;
        self.len += 1;
    }

    #[ensures(ret == (self.len == 0))]
    pub fn is_empty(&self) -> bool {
        self.len == 0
    }
}
```

**Contract Attributes**:

```rust
#[requires(precondition)]       // Must hold before function call
#[ensures(postcondition)]       // Must hold after function returns
#[invariant(condition)]         // Must hold for struct at all times
#[debug_requires(cond)]         // Only checked in debug builds
#[debug_ensures(cond)]          // Only checked in debug builds

// Special expressions in contracts
old(expr)   // Value of expr before function execution
ret         // Return value (in ensures)
```

**Commands**:

```bash
# Build with contract checking (debug mode)
cargo build

# Run tests with contracts enabled
cargo test

# Release build (contracts optionally disabled)
cargo build --release

# Check contract coverage
cargo test 2>&1 | grep -E "(requires|ensures|invariant)"
```

**Pass Criteria**:

- [ ] All public functions have `#[requires]` and `#[ensures]`
- [ ] All structs with invariants have `#[invariant]`
- [ ] No contract violations in test suite
- [ ] Contracts document the API completely

**Fail Actions**:

- Precondition violation -> Fix caller or document requirement
- Postcondition violation -> Fix implementation
- Invariant broken -> Identify corruption, add internal checks

---

## 5. Runtime UB Prevention & Unsafe Validation

### Loom for Concurrency Validation (Critical Paths)

Exhaustively test concurrent code by exploring all possible thread interleavings.

**Installation**:

```toml
# Cargo.toml
[dev-dependencies]
loom = "0.7"

[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ['cfg(loom)'] }
```

**Usage Pattern**:

```rust
// Production code with loom compatibility
#[cfg(not(loom))]
use std::sync::atomic::{AtomicUsize, Ordering};
#[cfg(not(loom))]
use std::sync::Arc;

#[cfg(loom)]
use loom::sync::atomic::{AtomicUsize, Ordering};
#[cfg(loom)]
use loom::sync::Arc;

pub struct Counter {
    value: AtomicUsize,
}

impl Counter {
    pub fn new() -> Self {
        Counter { value: AtomicUsize::new(0) }
    }

    pub fn increment(&self) -> usize {
        self.value.fetch_add(1, Ordering::SeqCst)
    }

    pub fn get(&self) -> usize {
        self.value.load(Ordering::SeqCst)
    }
}

#[cfg(loom)]
#[test]
fn test_concurrent_increment() {
    loom::model(|| {
        let counter = Arc::new(Counter::new());

        let c1 = counter.clone();
        let t1 = loom::thread::spawn(move || {
            c1.increment();
        });

        let c2 = counter.clone();
        let t2 = loom::thread::spawn(move || {
            c2.increment();
        });

        t1.join().unwrap();
        t2.join().unwrap();

        assert_eq!(counter.get(), 2);
    });
}
```

**Advanced Usage - Mutex and Condvar**:

```rust
#[cfg(loom)]
use loom::sync::{Arc, Mutex, Condvar};

#[cfg(loom)]
#[test]
fn test_producer_consumer() {
    loom::model(|| {
        let data = Arc::new((Mutex::new(None), Condvar::new()));

        let producer_data = data.clone();
        let producer = loom::thread::spawn(move || {
            let (lock, cvar) = &*producer_data;
            let mut guard = lock.lock().unwrap();
            *guard = Some(42);
            cvar.notify_one();
        });

        let consumer_data = data.clone();
        let consumer = loom::thread::spawn(move || {
            let (lock, cvar) = &*consumer_data;
            let mut guard = lock.lock().unwrap();
            while guard.is_none() {
                guard = cvar.wait(guard).unwrap();
            }
            assert_eq!(*guard, Some(42));
        });

        producer.join().unwrap();
        consumer.join().unwrap();
    });
}
```

**Loom-Compatible Types**:

```rust
// Replace std types with loom equivalents in tests
loom::sync::Arc                    // Arc<T>
loom::sync::Mutex                  // Mutex<T>
loom::sync::RwLock                 // RwLock<T>
loom::sync::Condvar                // Condvar
loom::sync::atomic::*              // AtomicBool, AtomicUsize, etc.
loom::sync::mpsc::channel          // mpsc channel
loom::thread::spawn                // thread::spawn
loom::cell::UnsafeCell             // UnsafeCell<T>
loom::lazy_static!                 // lazy_static replacement
```

**Commands**:

```bash
# Run loom tests (requires --release for reasonable performance)
RUSTFLAGS="--cfg loom" cargo test --release --lib

# Run specific loom test
RUSTFLAGS="--cfg loom" cargo test --release test_concurrent_increment

# With increased iteration limit for complex tests
LOOM_MAX_PREEMPTIONS=3 RUSTFLAGS="--cfg loom" cargo test --release

# Log execution paths (debugging)
LOOM_LOG=trace RUSTFLAGS="--cfg loom" cargo test --release 2>&1 | head -1000

# Checkpoint for long-running tests
LOOM_CHECKPOINT_FILE=loom.json RUSTFLAGS="--cfg loom" cargo test --release
```

**Environment Variables**:

```bash
LOOM_MAX_PREEMPTIONS=N      # Limit preemption points (default: varies)
LOOM_MAX_BRANCHES=N         # Limit branch exploration
LOOM_CHECKPOINT_FILE=path   # Save/resume exploration state
LOOM_CHECKPOINT_INTERVAL=N  # Checkpoint every N iterations
LOOM_LOG=level              # trace, debug, info, warn, error
```

**Pass Criteria**:

- [ ] All loom tests pass without deadlock
- [ ] No assertion failures across all interleavings
- [ ] State space fully explored (or bounded appropriately)
- [ ] Critical concurrent data structures validated

**Fail Actions**:

- Deadlock detected -> Analyze lock ordering, add timeout or restructure
- Assertion failure -> Fix race condition, strengthen synchronization
- State explosion -> Reduce threads/operations or bound with `LOOM_MAX_PREEMPTIONS`
- Timeout -> Checkpoint and resume, or simplify test

---

### Kani for Unsafe Code

```rust
#[cfg(kani)]
mod unsafe_verification {
    use super::*;

    #[kani::proof]
    fn verify_unsafe_buffer_access() {
        let mut buffer: [u8; 16] = kani::any();
        let idx: usize = kani::any();

        kani::assume(idx < buffer.len());

        // Verify unsafe access is within bounds
        let ptr = buffer.as_mut_ptr();
        unsafe {
            let val = *ptr.add(idx);
            kani::cover!(val != 0, "non-zero value accessed");
        }
    }

    #[kani::proof]
    fn verify_no_use_after_free() {
        let boxed: Box<i32> = Box::new(kani::any());
        let ptr = Box::into_raw(boxed);

        unsafe {
            // First access is valid
            let _val = *ptr;

            // Deallocate
            drop(Box::from_raw(ptr));

            // Second access would be UB - Kani should catch this if uncommented
            // let _val2 = *ptr;  // UB!
        }
    }
}
```

**Commands**:

```bash
# Verify unsafe code with Kani
cargo kani --harness verify_unsafe_buffer_access

# Check for memory safety issues
cargo kani --checks=pointer,bounds
```

### Miri for Dynamic UB Detection

**Installation**:

```bash
rustup +nightly component add miri
```

**Commands**:

```bash
# Run program under Miri
cargo +nightly miri run

# Run tests under Miri
cargo +nightly miri test

# Run specific test
cargo +nightly miri test test_name

# With additional checks
MIRIFLAGS="-Zmiri-symbolic-alignment-check" cargo +nightly miri test
MIRIFLAGS="-Zmiri-strict-provenance" cargo +nightly miri test

# Track memory leaks
MIRIFLAGS="-Zmiri-track-leaks" cargo +nightly miri test

# Ignore known issues
MIRIFLAGS="-Zmiri-ignore-leaks" cargo +nightly miri test

# Clean Miri cache
cargo +nightly miri clean
```

**Miri Flags Reference**:

```bash
-Zmiri-symbolic-alignment-check   # Stricter alignment checks
-Zmiri-strict-provenance          # Check pointer provenance
-Zmiri-track-raw-pointers         # Track raw pointer origins
-Zmiri-track-leaks                # Detect memory leaks
-Zmiri-ignore-leaks               # Ignore leak detection
-Zmiri-seed=N                     # Reproducible randomness
-Zmiri-isolation-error=warn       # Warn on isolation violations
```

**Pass Criteria**:

- [ ] Miri runs without UB detection
- [ ] All unsafe blocks verified by Kani
- [ ] No memory leaks (or documented intentional)
- [ ] Provenance rules respected

**Fail Actions**:

- UB detected -> Analyze Miri output, fix unsafe code
- Leak detected -> Add proper cleanup or document
- Alignment issue -> Use aligned types or manual alignment

---

## Phase 1: PLAN (Validation Design)

### Process

1. **Understand Requirements**
   - Identify safety requirements (memory, concurrency, panic-freedom)
   - Use sequential-thinking to plan multi-tool validation
   - Map requirements to Rust verification tools

2. **Artifact Detection**
   ```bash
   rg '#\[(requires|ensures|invariant)' -t rust $ARGUMENTS  # contracts
   rg '#\[kani::proof\]' -t rust $ARGUMENTS                  # Kani
   rg '#\[flux::' -t rust $ARGUMENTS                         # Flux
   rg 'loom::' -t rust $ARGUMENTS                            # Loom
   ```

3. **Design Rust Validation Stack**
   - Layer 0: rustc/clippy + cargo-audit/deny
   - Layer 1-2: Miri (unsafe), Loom (concurrency)
   - Layer 3: Flux refinements, contracts annotations
   - Layer 4-5: External proofs (Lean4, Quint)
   - Layer 6: Kani bounded model checking

---

## Phase 2: CREATE (Generate Artifacts)

### contracts Annotations

```rust
use contracts::*;

#[requires(x > 0, "x must be positive")]
#[ensures(result > x, "result must exceed input")]
fn double_positive(x: i32) -> i32 {
    x * 2
}

#[requires(slice.len() > 0, "slice must not be empty")]
#[ensures(result < slice.len(), "result must be valid index")]
fn find_min_index(slice: &[i32]) -> usize {
    let mut min_idx = 0;
    for i in 1..slice.len() {
        if slice[i] < slice[min_idx] {
            min_idx = i;
        }
    }
    min_idx
}
```

### Kani Proofs

```rust
#[cfg(kani)]
mod verification {
    use super::*;

    #[kani::proof]
    fn verify_no_overflow() {
        let x: u8 = kani::any();
        let y: u8 = kani::any();
        kani::assume(x < 128 && y < 128);
        assert!(x.checked_add(y).is_some());
    }

    #[kani::proof]
    #[kani::unwind(10)]
    fn verify_vec_bounds() {
        let len: usize = kani::any();
        kani::assume(len > 0 && len <= 10);
        let vec: Vec<u32> = (0..len).map(|_| kani::any()).collect();
        let idx: usize = kani::any();
        kani::assume(idx < len);
        let _ = vec[idx];
    }
}
```

### Loom Concurrency Verification

```rust
#[cfg(loom)]
mod loom_tests {
    use loom::sync::atomic::{AtomicUsize, Ordering};
    use loom::sync::Arc;
    use loom::thread;

    #[test]
    fn verify_concurrent_counter() {
        loom::model(|| {
            let counter = Arc::new(AtomicUsize::new(0));
            let c1 = counter.clone();
            let c2 = counter.clone();

            let t1 = thread::spawn(move || c1.fetch_add(1, Ordering::SeqCst));
            let t2 = thread::spawn(move || c2.fetch_add(1, Ordering::SeqCst));

            t1.join().unwrap();
            t2.join().unwrap();

            assert_eq!(counter.load(Ordering::SeqCst), 2);
        });
    }
}
```

### Flux Refinement Types

```rust
#[flux::sig(fn(x: i32{x > 0}) -> i32{v: v > 0})]
fn positive_double(x: i32) -> i32 { x * 2 }

#[flux::sig(fn(slice: &[i32][@n], idx: usize{idx < n}) -> i32)]
fn safe_index(slice: &[i32], idx: usize) -> i32 {
    slice[idx]  // Guaranteed in-bounds at compile time
}
```

---

## Phase 3: VERIFY (Validation Pipeline)

### Basic (Precondition Check)

```bash
command -v rustc >/dev/null || exit 11
cargo fmt --check || exit 12
cargo clippy -- -D warnings || exit 13
```

### Security Audit

```bash
cargo audit || exit 14
cargo deny check || exit 14
```

### Formal Verification

```bash
# contracts crate (checked at compile time in debug builds)
cargo build || exit 15
cargo test || exit 15

# Kani bounded model checking
rg '#\[kani::proof\]' -q -t rust && cargo kani || exit 15

# Flux refined types
rg '#\[flux::' -q -t rust && cargo flux || exit 15

# Loom concurrency
rg 'loom::' -q -t rust && RUSTFLAGS='--cfg loom' cargo test --release || exit 15
```

---

## Phase 4: REMEDIATE (Fix Failures)

### Error Scenarios

| Tool      | Error Message                | Fix                           |
| --------- | ---------------------------- | ----------------------------- |
| Miri      | `pointer out of bounds`      | Check slice/array bounds      |
| Miri      | `memory leaked`              | Ensure Drop impl              |
| Miri      | `data race detected`         | Use atomic or sync            |
| Loom      | `deadlock detected`          | Review lock ordering          |
| Kani      | `VERIFICATION FAILED`        | Check counterexample          |
| Kani      | `unwinding assertion failed` | Increase `#[kani::unwind(N)]` |
| contracts | `precondition violated`      | Strengthen caller             |
| contracts | `postcondition violated`     | Fix implementation            |
| Flux      | `refinement type error`      | Ensure input constraints      |

---

## Complete HODD-Rust Workflow

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== HODD-Rust Validation Pipeline ==="

# Phase 1: Type Design
echo "[1/7] Type Checking..."
cargo check
cargo clippy -- -D warnings

# Phase 2: Contract Verification
echo "[2/7] Contract Verification..."
cargo build
cargo test --lib

# Phase 3: Specification Validation (Quint)
echo "[3/7] Quint Specification..."
if [ -d "specs" ]; then
    quint typecheck specs/*.qnt
    quint verify specs/*.qnt --invariant=Safety
fi

# Phase 4: Proof Verification (Lean 4)
echo "[4/7] Lean 4 Proofs..."
if [ -f "lakefile.toml" ]; then
    lake build
fi

# Phase 5: Kani Model Checking
echo "[5/7] Kani Verification..."
if grep -rq "kani::proof" src/; then
    cargo kani
fi

# Phase 6: Loom Concurrency Validation
echo "[6/7] Loom Concurrency Check..."
if grep -rq "cfg(loom)" src/ tests/; then
    RUSTFLAGS="--cfg loom" cargo test --release --lib
fi

# Phase 7: Miri UB Detection
echo "[7/7] Miri UB Check..."
cargo +nightly miri test

echo "=== All Validations Passed ==="
```

---

## Quick Reference Card

| Tool           | Purpose                | Command                                       |
| -------------- | ---------------------- | --------------------------------------------- |
| `cargo check`  | Type verification      | `cargo check`                                 |
| `cargo clippy` | Lint analysis          | `cargo clippy -- -D warnings`                 |
| contracts      | Runtime contracts      | `cargo build && cargo test`                   |
| Flux           | Refinement types       | `cargo flux`                                  |
| Quint          | Spec modeling          | `quint verify spec.qnt`                       |
| Lean 4         | Formal proofs          | `lake build`                                  |
| Kani           | Model checking         | `cargo kani`                                  |
| Loom           | Concurrency validation | `RUSTFLAGS="--cfg loom" cargo test --release` |
| Miri           | UB detection           | `cargo +nightly miri test`                    |

---

## Exit Codes

| Code | Meaning                         | Action                |
| ---- | ------------------------------- | --------------------- |
| 0    | All validations pass            | Proceed to deployment |
| 11   | Toolchain missing               | Install rustup/cargo  |
| 12   | Format violations               | Run `cargo fmt`       |
| 13   | Clippy failures                 | Fix warnings          |
| 14   | Security/dependency issues      | Review audit findings |
| 15   | Formal verification failed      | Fix proofs/contracts  |
| 16   | External tool validation failed | Fix Lean4/Quint specs |

---

## Detection Commands

```bash
rg 'unsafe\s*\{' -t rust                                    # Unsafe blocks
rg 'extern\s+"C"' -t rust                                   # FFI
rg 'Arc|Mutex|RwLock|atomic|thread::spawn' -t rust         # Concurrency
rg '#\[(requires|ensures|invariant)\]' -t rust             # contracts
rg '#\[kani::proof\]' -t rust                               # Kani
rg '#\[flux::' -t rust                                      # Flux
```

---

## Anti-Patterns (AVOID)

1. **Unsafe Without Kani** - All `unsafe` blocks need formal verification
2. **Skipping Contracts** - Public APIs must have `#[requires]`/`#[ensures]` (for runtime properties only)
3. **Miri in CI** - Miri is for development/debugging, not CI (too slow)
4. **Ignoring Counterexamples** - Kani counterexamples reveal real bugs
5. **Typestate Bypass** - Don't use `unsafe` to skip typestate checks
6. **Runtime Checks for Static Properties** - If types can enforce it, don't runtime check
7. **Contracts for Compile-Time Properties** - Use `static_assertions` / `const_assert!` instead of `#[requires]` for compile-time verifiable invariants
8. **Always-On Contracts for Development Checks** - Use `debug_*` variants for internal invariants that don't need production enforcement
9. **Always-On Expensive Checks** - Use `test_*` for O(n)+ verification (e.g., `is_sorted`, reference implementation equivalence)
10. **Redundant Contracts** - If static assertions already verify a property, do NOT add debug/test/runtime contracts for the same property

---

## Common Pitfalls

### Pitfall 1: Miri in CI

**Problem:** Too slow for CI.
**Solution:** Use Miri locally, Kani for CI.

### Pitfall 2: Kani Loop Unrolling

**Problem:** Timeout on unbounded loops.
**Solution:** Add `#[kani::unwind(N)]` + assume bounds.

### Pitfall 3: Loom State Explosion

**Problem:** Too many thread interleavings.
**Solution:** Start with 2-3 threads, tune `LOOM_MAX_PREEMPTIONS`.

### Pitfall 4: Contract Annotation Bloat

**Problem:** Over-annotated code.
**Solution:** Annotate public API boundaries only.

### Pitfall 5: Ignoring Counterexamples

**Problem:** Silencing Kani with assumes.
**Solution:** Analyze and fix root cause.

---

## Pass/Fail Decision Matrix

| Check          | Pass             | Fail Action            |
| -------------- | ---------------- | ---------------------- |
| `cargo check`  | No errors        | Fix type errors        |
| `cargo clippy` | No warnings      | Address all warnings   |
| `cargo test`   | All pass         | Fix failing tests      |
| `cargo flux`   | Verified         | Strengthen refinements |
| `quint verify` | No violations    | Fix spec or impl       |
| `lake build`   | No sorry         | Complete proofs        |
| `cargo kani`   | SUCCESSFUL       | Fix counterexample     |
| `loom test`    | No deadlock/race | Fix synchronization    |
| `miri test`    | No UB            | Fix unsafe code        |

**Rule**: Do not ship if any check fails.

---

## Best Practices

1. **Unsafe Blocks**: Document safety invariants; validate with Miri locally
2. **Concurrency**: Use Loom for lock-free algorithms
3. **Contracts**: Apply contracts selectively to public APIs
4. **Proofs**: Use Kani for bounded verification
5. **External Tools**: Keep specs in `.outline/`
6. **CI Pipeline**: rustfmt -> clippy -> audit -> deny -> contracts -> Kani
7. **Counterexamples**: Never ignore; always fix

---

## Resources

- [Kani Documentation](https://model-checking.github.io/kani/)
- [Loom GitHub](https://github.com/tokio-rs/loom)
- [Miri Documentation](https://github.com/rust-lang/miri)
- [Flux Refinement Types](https://flux-rs.github.io/flux/)
- [Verus Verified Rust](https://github.com/verus-lang/verus)
- [Contracts crate](https://crates.io/crates/contracts)
