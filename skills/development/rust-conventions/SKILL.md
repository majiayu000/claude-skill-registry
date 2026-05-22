---
name: rust-conventions
description: Work on Rust crates in packages/rust_viterbo. Use for crate layout, commands (fmt/clippy/test/bench), and coding conventions.
---

# Rust Conventions (rust_viterbo)

## Crates

- `geom` (math)
- `algorithm` (symplectic capacity algorithms)
- `ffi` (PyO3/Maturin bindings)

## Commands

- `cargo fmt`
- `cargo clippy --workspace --all-targets`
- `cargo test --workspace`
- `cargo test --release <filter>`
- `cargo bench`

## Conventions

- Favor pure functions with immutable types.
- Follow best practices for mathematically correct Rust code.
- Use `nalgebra` for linear algebra operations.

## Testing and profiling

- Cover happy paths, edge cases, error paths.
- Benchmark only after profiling identifies hotspots.
- Document why changes are made (e.g., performance impact).

## Caching

- Shared target dir: `/workspaces/worktrees/shared/target` (set by worktree script).
