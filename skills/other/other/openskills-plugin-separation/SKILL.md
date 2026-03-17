---
name: openskills-plugin-separation
description: Enforce clean separation between core openskills-runtime and optional WASM build plugins so plugin compilation does not break runtime consumers or language bindings.
---

# OpenSkills Plugin Separation

Use this skill when changing plugin features, build-tool wiring, or runtime dependency topology.

## Objective

Keep core runtime usable without plugin toolchains, especially for bindings and non-build execution paths.

## Key Files

- `runtime/Cargo.toml`
- `runtime/src/lib.rs`
- `runtime/src/bin/openskills-runtime.rs`
- `runtime/src/build/**`
- `bindings/ts/Cargo.toml`
- `bindings/python/Cargo.toml`

## Separation Rules

1. Build plugins must be gated behind explicit features.
2. Core runtime defaults should not force plugin toolchains.
3. Bindings should opt out of plugin-heavy default features when appropriate.
4. Public exports for build functions must be feature-gated.
5. CLI build commands must degrade gracefully when build features are disabled.

## Validation Checklist

- `cargo check -p openskills-runtime` passes with default features.
- Bindings compile without pulling plugin-specific dependencies unintentionally.
- Runtime tests that do not require plugin build paths continue to pass.

## Output Format

- Feature graph summary
- Leakage findings (if any)
- Minimal patch plan
- Post-change verification commands
