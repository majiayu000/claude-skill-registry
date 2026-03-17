---
name: 30-03-test-driven-refactoring
description: Drive structural refactors with compile-failing tests that define the end state. Write tests first that assert the target architecture — module paths, function signatures, ownership boundaries, absence of old code. Tests are red until the refactor is complete. Use when planning or executing large refactors, codebase reorganizations, module moves, or architectural migrations.
---

# 30.03 Test-Driven Refactoring (TDR)

Write tests that describe the end state of the refactor. They fail. Do the refactor. They pass.

The compiler and test runner enforce the spec. No manual checking. No "I think it's done."

## When To Use

- Codebase reorganization (moving modules, renaming directories)
- Architecture migration (layer splits, domain extraction)
- API reshaping (changing where functions live, signature changes)
- Any refactor where "done" has a structural definition

## Core Principle

A TDR test asserts **where things live and what shape they have** — not how they work internally. The existing behavioral tests cover correctness. TDR covers structure.

## The Three Test Layers

### Layer 1: Compile-Time (strongest)

`use` statements and fn pointer type assignments. If the module doesn't exist at the target path with the right signature, the crate won't compile.

```rust
// Module must exist at this path
use crate::components::weapon::system::Weapon;

// Function must exist with this EXACT signature — wrong args/return = compile error
use crate::domain::entity::create_entity;
let _: fn(&ReducerContext, Option<PlayerId>) -> EntityId = create_entity;
```

**Why fn pointer pinning matters:** `use X as _` only checks "something exists." A fn pointer assignment checks the full signature. An empty `pub fn create_entity() {}` shim won't type-match.

### Layer 2: Runtime Structural (binary assertions)

Filesystem walks that verify old paths are gone and ownership boundaries hold. These are binary — the dir exists or it doesn't.

```rust
// Old directory must not exist
assert!(!dir_exists("components/old_name/"));

// No .rs file in the crate references the old path
walk_all_rs_files(|path, content| {
    assert!(!content.contains("old_name"),
        "{} still references old_name", path);
});
```

### Layer 3: Runtime Anti-Bypass (catch shims)

Prevent greening via `pub use` re-exports instead of actual moves.

```rust
// The target must define pub fn, not just re-export
assert!(any_rs_in_dir("domain/entity", |content|
    content.contains("pub fn create_entity")),
    "must define create_entity, not just re-export it");

// A catch-all file must have NO business logic remaining
let c = read_file("components/mod.rs");
assert_eq!(count_occurrences(c, "pub fn "), 0);
assert_eq!(count_occurrences(c, "macro_rules!"), 0);
assert_eq!(count_occurrences(c, "pub trait "), 0);
```

## What Makes a Good TDR Assertion

**Good (binary, structural):**
- Module exists at path → `use crate::new_path::Thing as _`
- Function has correct signature → fn pointer assignment
- Old directory does not exist → `assert!(!dir_exists(...))`
- No file references old path → walk + string check
- Catch-all file has no logic → count `pub fn` = 0
- Struct has expected field → `let _: &FieldType = &thing.field`
- Ownership boundary → "file X must not contain pattern Y"

**Bad (brittle, arbitrary):**
- Line count minimums → punishes clean code, invites padding
- Specific implementation strings → breaks on valid refactors
- Arbitrary numeric caps → "why 15 and not 18?"
- File size thresholds → same problem as line counts

**The test:** Could a correct refactor ever fail this assertion? If yes, it's brittle. Remove it.

## Process

### 1. Write the Spec

Before writing tests, articulate the end state:
- What directories exist?
- What moves where?
- What gets deleted?
- What are the new public APIs (fn signatures)?
- What ownership boundaries exist (X must not contain Y)?

### 2. Create the Test File

In the crate being refactored, add a `#[cfg(test)]` module. Every test maps to one spec line.

Organize tests by gap/goal, not by layer:

```rust
#[cfg(test)]
mod architecture {
    // ── G1: Description of structural goal ──
    #[test] fn g1_new_path_compiles() { ... }
    #[test] fn g1_old_path_gone() { ... }
    #[test] fn g1_no_stale_refs() { ... }

    // ── G2: Next goal ──
    ...

    // ── CONTRACT: Must never break ──
    #[test] fn contract_public_types() { ... }
}
```

### 3. Verify All Red

Run the tests. Every architecture test must fail. If any pass already, either the spec is wrong or the test is too weak.

Count the errors — this is the scorecard:
```bash
cargo test architecture 2>&1 | grep "^error\[" | wc -l
```

### 4. Do the Refactor

Work through the spec. After each phase, re-run:
```bash
cargo test architecture 2>&1 | grep "^error\[" | wc -l
```

The number goes down. When it hits 0 and all runtime assertions pass, the refactor is complete.

### 5. Verify Behavioral Tests Still Pass

TDR tests structure. Existing tests cover behavior. Both must pass:
```bash
cargo test  # all tests — architecture + behavioral
```

Same pass count, same fail count (minus the architecture tests going from fail→pass).

## Handling Discoveries

TDR often surfaces real constraints that weren't in the spec. Examples from practice:

- **SpacetimeDB accessor collision:** Renaming `collider_comp/` to `collider/` fails because SpacetimeDB generates a table accessor trait named `collider` that collides with the module name. This is a real architectural constraint the test surfaced before any refactoring code was written. The fix (tables.rs submodule pattern) was designed in response to the test failure.

- **Re-export barrel dependency:** Removing `lib.rs` re-exports reveals every internal consumer still using the barrel path. The compiler error list IS the migration checklist.

Record these in the spec. They're not test failures — they're design information.

## Contract Tests

Always include a section of tests that must NEVER fail — they verify the refactor doesn't break the public API:

```rust
// ── CONTRACT: public types always importable ──
#[test]
fn contract_core_tables() {
    use crate::Position as _;
    use crate::Velocity as _;
    use crate::Entity as _;
}
```

These are green from day one and must stay green. If a contract test breaks, the refactor changed something it shouldn't have.

## Scaffold: Filesystem Helpers

TDR tests need filesystem access. Standard helpers:

```rust
fn src_dir() -> PathBuf {
    let manifest = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    Path::new(&manifest).join("src")
}

fn file_exists(rel: &str) -> bool { src_dir().join(rel).exists() }
fn dir_exists(rel: &str) -> bool { let p = src_dir().join(rel); p.exists() && p.is_dir() }
fn read_file(rel: &str) -> String { fs::read_to_string(src_dir().join(rel)).unwrap() }
fn count_matches(s: &str, pat: &str) -> usize {
    s.lines().filter(|l| l.contains(pat)).count()
}

fn walk_rs(dir: &Path, cb: &mut dyn FnMut(&Path, &str)) {
    if let Ok(entries) = fs::read_dir(dir) {
        for e in entries.flatten() {
            let p = e.path();
            if p.is_dir() { walk_rs(&p, cb); }
            else if p.extension().map_or(false, |x| x == "rs") {
                if let Ok(c) = fs::read_to_string(&p) { cb(&p, &c); }
            }
        }
    }
}

fn any_rs_in_dir(rel: &str, pred: &dyn Fn(&str) -> bool) -> bool {
    let mut found = false;
    walk_rs(&src_dir().join(rel), &mut |_, c| { if pred(c) { found = true; } });
    found
}
```

## TypeScript Variant

Same principle, different tools. Use a test file that imports from target paths:

```typescript
// architecture.test.ts
import { createEntity } from '../domain/entity'    // must exist
import { Weapon } from '../components/weapon'       // must exist

// Type assertions
const _: (id: EntityId) => void = createEntity      // signature pinned

// Runtime structural
test('old paths gone', () => {
    expect(fs.existsSync('src/components/collider_comp')).toBe(false)
})

test('no stale imports', () => {
    const files = glob.sync('src/**/*.ts')
    for (const f of files) {
        expect(fs.readFileSync(f, 'utf8')).not.toContain('collider_comp')
    }
})
```

## Relationship to Other Skills

- **30.01 Full Refactor Guide:** TDR is the verification layer. 30.01 is the execution method. Use together — TDR defines "done," 30.01 defines "how."
- **Test-Driven Development:** TDD tests behavior before implementation. TDR tests structure before refactoring. Same red→green philosophy, different axis.
- **Convergence Audit (30.02):** Audit finds what's wrong. TDR encodes the fix as tests.
