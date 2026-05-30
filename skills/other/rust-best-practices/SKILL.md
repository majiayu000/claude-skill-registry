---
name: rust-best-practices
description: >
  Development guidance for writing idiomatic Rust. Use when:
  (1) writing new Rust functions or modules,
  (2) choosing between borrowing, cloning, or ownership patterns,
  (3) implementing error handling with Result types,
  (4) optimizing Rust code for performance,
  (5) configuring clippy and linting for a project,
  (6) deciding between static and dynamic dispatch,
  (7) writing documentation or doc tests.
---

# Rust Best Practices

Guidance for writing idiomatic, performant, and safe Rust code. This is a development skill, not a review skill -- use it when building, not reviewing.

## Quick Reference

| Topic | Key Rule | Reference |
|-------|----------|-----------|
| Ownership | Borrow by default, clone only when you need a separate owned copy | [references/coding-idioms.md](references/coding-idioms.md) |
| Clippy | Run `cargo clippy -- -D warnings` on every commit; configure workspace lints | [references/clippy-config.md](references/clippy-config.md) |
| Performance | Don't guess, measure. Profile with `--release` first. Watch monomorphization + cache-line alignment at scale | [references/performance.md](references/performance.md) |
| Generics | Static dispatch by default, dynamic dispatch when you need mixed types | [references/generics-dispatch.md](references/generics-dispatch.md) |
| Type State | Encode state in the type system when invalid operations should be compile errors | [references/type-state-pattern.md](references/type-state-pattern.md) |
| Documentation | `//` for why, `///` for what and how, `//!` for module/crate purpose | [references/documentation.md](references/documentation.md) |
| Pointers | Choose pointer types based on ownership needs and threading model | [references/pointer-types.md](references/pointer-types.md) |
| API Design | Unsurprising, flexible, obvious, constrained — encode invariants in types; watch hidden contracts (re-exports, auto-traits) | [references/api-design.md](references/api-design.md) |
| Wild Patterns | Drop guards, extension traits, index pointers, crate preludes — battle-tested idioms from mature crates | [references/coding-idioms.md](references/coding-idioms.md) |
| Ecosystem | Evaluate crates, pick error handling strategy, stay current | [references/ecosystem-patterns.md](references/ecosystem-patterns.md) |

## Gates

Short **sequences with pass conditions** before claiming outcomes that need evidence (not an internal “I checked”).

### Clippy clean

1. From the workspace root (or with `-p <crate>`), run: `cargo clippy --all-targets --all-features -- -D warnings`.
2. **Pass:** exit status is `0` and the invocation finishes without Clippy-deny failures.

### Performance claim

1. Build with `cargo build --release` (or your benchmark harness) under the same profile you ship or measure.
2. Capture a **before** and **after** number from the same tool and metric (name both), e.g. Criterion `ns/iter`, `heaptrack` allocations, or a flamegraph path on disk.
3. **Pass:** you can cite both measurements, **or** you explicitly state that only correctness or readability changed and you are **not** claiming a performance delta.

### Docs for symbols you changed

1. Run `cargo doc --no-deps` for the crate you edited (add `-p <crate>` in workspaces).
2. **Pass:** the doc build succeeds; if `#![deny(missing_docs)]` (or crate policy) applies, there are no new missing-doc errors for those symbols.

## Coding Idioms

Prefer `&T` over `.clone()`, use `&str`/`&[T]` in parameters, and chain iterators instead of index-based loops. For Option/Result, use `let Ok(x) = expr else { return }` for early returns and `?` for propagation. For scoped state changes, use **drop guards** (`let _guard = ...`, never `let _ = ...`) with `mem::replace` or `scopeguard::defer!`. Add methods to foreign types via **extension traits** (`trait MyExt; impl<T: Bound> MyExt for T`). For graph and tree shapes, prefer **index pointers** (`slotmap::DefaultKey`, generational indices) over `&T` to side-step lifetimes without unsafe. Curate a lean **crate prelude** for ergonomic glob imports; prelude additions are semver-minor (RFC 1105). See [references/coding-idioms.md](references/coding-idioms.md) for ownership, iterator, import patterns, and these ecosystem-level idioms.

## Error Handling

Return `Result<T, E>` for fallible operations. Use `thiserror` for library error types, `anyhow` for binaries. Propagate with `?`, never `unwrap()` outside tests. See [references/coding-idioms.md](references/coding-idioms.md) for Option/Result patterns.

## Clippy Discipline

Run `cargo clippy --all-targets --all-features -- -D warnings` on every commit. Configure workspace lints in `Cargo.toml` and use `#[expect(clippy::lint)]` (not `#[allow]`) as the standard for lint suppression -- it warns when the suppression becomes stale. See [references/clippy-config.md](references/clippy-config.md) for lint configuration and key lints.

## Performance Mindset

Always benchmark with `--release`, profile before optimizing, and avoid cloning in loops or premature `.collect()` calls. Keep small types on the stack and heap-allocate only recursive structures and large buffers. For workspaces at scale, watch **monomorphization budgets** (extract type-independent inner functions; switch internal generics to `dyn` where peak inlining isn't critical) and **false sharing** (`#[repr(align(64))]` or `crossbeam::utils::CachePadded` on per-thread atomics; `align(128)` on Apple Silicon). Benchmark with `criterion` — persist a baseline (`--save-baseline main`) and compare in CI, use `criterion::black_box` (with `as_ptr()` for pointer inputs), and isolate I/O into `iter_batched` setup. See [references/performance.md](references/performance.md) for profiling tools, allocation guidance, monomorphization patterns, cache-line alignment, and criterion discipline.

## Generics and Dispatch

Use static dispatch (`impl Trait` / `<T: Trait>`) by default for zero-cost monomorphization. Switch to `dyn Trait` only for heterogeneous collections or plugin architectures, preferring `&dyn Trait` over `Box<dyn Trait>` when ownership isn't needed. In edition 2024, `-> impl Trait` captures all in-scope lifetimes by default -- use `+ use<'a, T>` for precise capture control. Prefer native `async fn` in traits over the `async-trait` crate for static dispatch. See [references/generics-dispatch.md](references/generics-dispatch.md) for dispatch trade-offs, RPIT capture rules, and async trait guidance.

## Type State Pattern

Encode valid states in the type system so invalid operations become compile errors. Use for builders with required fields, protocol state machines, and workflow pipelines. See [references/type-state-pattern.md](references/type-state-pattern.md) for implementation patterns and when to avoid.

## Documentation

Use `//` for why, `///` for what/how on public APIs, and `//!` for module purpose. Every `TODO` needs a linked issue and library crates should enable `#![deny(missing_docs)]`. Use `#[diagnostic::on_unimplemented]` to provide custom compiler errors for your public traits. See [references/documentation.md](references/documentation.md) for doc test patterns, comment conventions, and diagnostic attributes.

## API Design

Follow four principles: unsurprising (reuse standard names and traits), flexible (use generics and `impl Trait` to avoid unnecessary restrictions), obvious (encode invariants in the type system so misuse is a compile error), and constrained (expose only what you can commit to long-term). Use `#[non_exhaustive]` for types that may grow, seal traits you need to extend without breaking changes, and wrap foreign types in newtypes to control your SemVer surface. Watch for **hidden contracts** — re-exported foreign types, auto-trait propagation through `-> impl Trait`, and accidental `!Send` futures — and lock them down with a compile-time `is_normal<T: Sized + Send + Sync + Unpin>()` test for public types. Ship new traits with blanket impls for `&T`/`Box<T>` early (adding later is breaking). For fallible cleanup, expose an explicit `close()`/`shutdown()` returning `Result`; `Drop` cannot fail or `.await`. See [references/api-design.md](references/api-design.md) for builder patterns, sealed traits, object-safety mechanics, `Deref` discipline, fallible destructors, and SemVer implications.

## Ecosystem Patterns

Evaluate crates by recent download trends, maintenance activity, documentation quality, and transitive dependency weight. Use `thiserror` for library error types, `anyhow` for binaries, and `eyre` when you need custom error reporters. Prefer vendoring or writing code yourself when a crate pulls heavy dependencies for a small feature. Run `cargo-deny` for license and vulnerability auditing and `cargo-udeps` to trim unused dependencies. See [references/ecosystem-patterns.md](references/ecosystem-patterns.md) for crate evaluation criteria, edition migration, and essential tooling.

## Pointer Types

Choose pointer types based on ownership and threading: `Box<T>` for single-owner heap allocation, `Rc<T>`/`Arc<T>` for shared ownership, `Cell`/`RefCell`/`Mutex`/`RwLock` for interior mutability. Use `LazyLock`/`LazyCell` (stable since 1.80) instead of `lazy_static` or `once_cell`. See [references/pointer-types.md](references/pointer-types.md) for the full single-thread vs multi-thread decision table and migration guidance.

## Destructors and Cleanup

`Drop::drop(&mut self)` cannot return an error or `.await`. For fallible cleanup (I/O flush, network shutdown, async commit), expose an explicit `close()` or `shutdown()` method returning `Result<(), Error>` (or `impl Future`) and run best-effort cleanup in `Drop` as a fallback. Patterns for "consume self in Drop": `Option<T>`-newtype with `mem::take`, per-field `mem::take`, or `ManuallyDrop<T>`. Never `block_on(...)` in `Drop` (deadlock under async runtimes). For scoped state changes (toggle, restore, run on panic), use a **drop guard** bound with `let _guard = ...` — never `let _ = ...`, which drops immediately. `scopeguard::defer!` is the battle-tested option; note that drop guards do NOT run under `panic = "abort"`. See [references/coding-idioms.md](references/coding-idioms.md) and [references/api-design.md](references/api-design.md) for the explicit-destructor pattern.

## Async APIs

`async fn` lowers to a state machine returning an anonymous `impl Future`. Lock down the **Send-ness** contract on public APIs with `-> impl Future<...> + Send + '_` (or an explicit lifetime tied to `&self`) — auto-trait propagation through `-> impl Trait` is silent and a single `Rc<...>` or `std::sync::MutexGuard` held across `.await` downgrades the whole future to `!Send`, breaking downstream callers. Add `+ 'static` only when the future must be spawned onto a multi-threaded executor (e.g. `tokio::spawn`); a blanket `'static` on every signature forbids borrowing from `&self` and is the wrong default. **Drop equals cancel**: when a future is dropped mid-poll, locals drop, no cleanup runs. Document **cancel-safety** on every public `async fn`: cancel-safe (`recv`, observation-only) vs cancel-unsafe (`read_exact`, `write_all`, anything holding cross-poll invariants). For runtime-agnostic library code, take `impl Future` or use `futures` crate primitives — do NOT spawn internally, and document the required runtime. Use `std::pin::pin!` macro for stack-pinned local futures; `Box::pin` only when heap allocation is acceptable.
