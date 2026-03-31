---
name: rust-dev
description: This skill should be used when working with Rust code, reviewing Rust code, managing Rust dependencies, creating Rust projects, or fixing Rust compilation errors. It provides strict coding standards (especially FAIL FAST error handling), workspace architecture guidance, dependency management automation, and common Rust patterns.
allowed-tools: Read, Bash(python3 *), Bash(cargo *)
---

# Rust Development

## Core Rules

1. **Edition 2024**: Always `edition = "2024"` in Cargo.toml
2. **FAIL FAST**: Every error MUST propagate with `?` or `return Err`. Logging is NOT handling. See [error-handling.md](references/error-handling.md)
3. **Dependency versions**: Use `x.x` format (e.g., `serde = "1.0"`). Find latest with `python3 scripts/check_crate_version.py <crate>`
4. **Workspace architecture**: Root Cargo.toml defines workspace only. Separate crates for lib/cli/client
5. **Error types**: `thiserror` (with backtrace) for libraries, `anyhow` for binaries/tests
6. **CLI-first config**: Never bypass CLI args. Use `from_cli_args()`, never `Default` that reads env
7. **No `env::set_var` in tests**: Pass config through function parameters
8. **Async**: Use tokio consistently
9. **Visibility**: Private (default) > `pub(crate)` > `pub`
10. **No magic numbers**: Use `const` or CLI args

## Adding Dependencies

1. Run `python3 scripts/check_crate_version.py <crate-name>` to find latest version
2. Add to `[workspace.dependencies]` in root Cargo.toml with `x.x` format
3. Reference in member crates: `serde = { workspace = true }`

Common deps: `thiserror = "2.0"`, `anyhow = "1.0"`, `tokio = { version = "1", features = ["full"] }`, `serde = { version = "1.0", features = ["derive"] }`, `clap = { version = "4.5", features = ["derive"] }`

## Creating New Projects

Use the template in `assets/workspace-template/`:

```
project/
├── Cargo.toml              # Workspace root, no code
├── project/                # Library crate (thiserror)
│   ├── Cargo.toml
│   └── src/lib.rs
└── project-cli/            # Binary crate (anyhow + clap)
    ├── Cargo.toml
    └── src/main.rs
```

## Module Organization

Split modules when file exceeds ~500 lines or tests take 50%+ of file. See [module-organization.md](references/module-organization.md) for patterns.

## Error Handling

The most critical standard. See [error-handling.md](references/error-handling.md) for full rules and examples.

**Quick check:** If you see `if let Err` or `match ... Err` without `return Err` or `?`, it's a bug.

## References

- [error-handling.md](references/error-handling.md) — FAIL FAST rules, thiserror/anyhow patterns, error chain preservation
- [module-organization.md](references/module-organization.md) — When/how to split modules, test extraction
- [dependency-guide.md](references/dependency-guide.md) — Workspace deps, feature flags, common crates

## Scripts

- `scripts/check_crate_version.py` — Query crates.io for latest dependency versions
