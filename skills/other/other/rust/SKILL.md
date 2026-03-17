---
name: rust
description: Write production-quality Rust code following industry best practices and idiomatic patterns. Use for any Rust coding task including applications, libraries, refactoring, debugging, or code review — with particular expertise in cross-platform GUI development.
---

## Instructions

### 1. Planning & Analysis

**Before writing any code:**
- Understand the full requirements and constraints
- Review the existing codebase for conventions, utilities, and patterns already in use
- Check for shared/common modules before creating new utilities
- Consider edge cases within reason unless the user specifically asks for more
- For GUI work: identify which platforms are targeted and any platform-specific constraints

### 2. Design Principles

**Rust-Specific:**
- Prefer borrowing over cloning; pass `&str` not `&String`, `&Path` not `&PathBuf`, `&[T]` not `&Vec<T>`
- Use enums, newtypes, and the type system to make illegal states unrepresentable
- Parse raw input into well-typed structures at the boundary, then pass typed data inward
- Leverage `impl Into<T>`, `AsRef<T>`, and other conversion traits for ergonomic public APIs

**General:**
- **YAGNI**: Implement only what is required; add complexity as the need arises
- **KISS**: Favor simplicity and clarity over cleverness
- **DRY**: Extract shared logic into common modules or helper functions
- Follow the repo's existing conventions over personal preference

### 3. Error Handling (anyhow required)

**Use `anyhow` as the primary error-handling crate.** Do not introduce `thiserror`, `eyre`, or other error libraries unless explicitly approved.

- All fallible functions return `anyhow::Result<T>`
- Attach context at every level with `.context("message")` or `.with_context(|| format!(...))`
- Propagate errors with `?`; never use `unwrap()` or `expect()` outside test code
- Use `anyhow::anyhow!("message")` or `anyhow::bail!("message")` for ad-hoc errors
- At the entrypoint: handle errors gracefully — print to `stderr` and exit with appropriate code

### 4. Project Structure

Follow the structure established by the project. For new projects, use idiomatic Rust conventions:

**Workspace projects:**
- Place crates under a `crates/` directory; list them in root `Cargo.toml` `[workspace.members]`
- Shared utilities go in a common crate (e.g., `crates/common/` or `crates/shared/`)
- Each crate has a focused responsibility

**Single-crate projects:**
- `src/main.rs` — thin entrypoint: init, parse args/config, call into app logic, handle exit
- `src/lib.rs` — public API surface; re-exports from submodules
- `src/models.rs` — domain types, config structs, enums
- `src/app.rs` (or domain-named module) — core logic

**General guidelines:**
- Keep `main.rs` thin — it orchestrates; logic lives in library code
- One module per concern; split files when they exceed ~300 lines
- Additional modules are fine when they keep things tidy and well-scoped
- `#[derive(Debug, Clone)]` on config/model structs; add `Copy`, `PartialEq`, `Eq` where appropriate
- Enums for discrete modes/states; `Option<T>` for optional fields

### 5. Cross-Platform GUI Development

When building GUI applications, apply these practices:

Before doing any visual changes, check the `ui-guidelines.md` at the root of the repo for general guidelines and best 
practices for UI/UX development.

**Architecture:**
- Separate core logic from UI: business logic in a library crate, UI in the binary crate
- Use a message/command pattern to communicate between UI and logic layers
- Keep platform-specific code isolated behind trait abstractions or `#[cfg(target_os)]` gates
- Design for the event loop: avoid blocking the main/UI thread

**Framework guidance (choose based on project needs):**
- **iced** — Elm-inspired, pure Rust, good for data-driven UIs. Strengths: type-safe message passing, no unsafe, cross-platform. Use `iced::Application` or `iced::Sandbox` traits.
- **egui / eframe** — immediate-mode, excellent for tools, dashboards, debug UIs. Strengths: very fast iteration, minimal boilerplate, easy embedding. Use `eframe::App` trait.
- **Tauri** — web-tech frontend with Rust backend. Strengths: small binary size, leverage web ecosystem, strong IPC. Use for apps where web UI is preferred.
- **Slint** — declarative UI with `.slint` markup language. Strengths: designer-friendly, embedded-capable, good accessibility.
- **gtk4-rs / relm4** — GTK4 bindings. Strengths: mature widget set, strong Linux integration. Use `relm4` for Elm-style architecture on top of GTK4.
- **Dioxus** — React-like with RSX syntax. Strengths: familiar to web devs, cross-platform (desktop, web, mobile).

**Cross-platform considerations:**
- Test on all target platforms early and regularly (Windows, macOS, Linux at minimum)
- Use `dirs` or `directories` crate for platform-appropriate config/data/cache paths
- Handle HiDPI/scaling — use logical pixels, not physical pixels
- Respect platform conventions for keyboard shortcuts (Cmd vs Ctrl), file paths, and native look-and-feel
- Use `cfg(target_os)` sparingly and only when truly needed; prefer cross-platform abstractions
- For file dialogs, system notifications, and other OS integration, use `rfd`, `notify-rust`, or similar cross-platform crates

**State management:**
- Treat application state as a single source of truth; UI renders from state
- Use message/event enums to describe state transitions
- Keep state serializable where practical (enables save/restore, undo/redo)
- For complex state, consider a reducer pattern or `Arc<Mutex<State>>` for thread-safe sharing

**Async and threading in GUI apps:**
- Never block the UI thread — offload heavy work to background threads or async tasks
- Use channels (`std::sync::mpsc`, `crossbeam-channel`, `tokio::sync::mpsc`) to send results back to the UI
- For async runtimes alongside GUI event loops, use the framework's built-in async support or run `tokio` on a separate thread
- Debounce expensive operations triggered by rapid UI events (typing, resizing)

### 6. Code Style

- Use the repo's `rustfmt` and `clippy` configuration; never change them; fix all warnings
- `snake_case` for functions/variables/modules/files; `PascalCase` for types; `UPPER_SNAKE_CASE` for constants
- Group imports: `crate::`, external crates, `std::`; no glob imports in production code
- Doc comments (`///`) on all public items with `# Errors` / `# Panics` sections where applicable
- Comments explain "why", not "what"; no commented-out code
- Functions ~50 lines max; extract helpers when they grow
- `match` over `if let` chains for multiple variants; guard clauses for early returns

### 7. Dependencies

- Check the existing `Cargo.toml` before adding new dependencies
- Prefer well-maintained, widely used crates (check download counts, recent activity, `unsafe` usage)
- Pin major versions; use `cargo update` for patch updates
- Feature-gate optional functionality to keep compile times and binary size down
- For cross-platform apps, verify that dependencies support all target platforms
- Dependencies should be always kept up-to-date with the latest stable versions

**Commonly useful crates:**
- CLI: `clap` (derive), `indicatif` (progress bars)
- Serialization: `serde` + `serde_json` / `toml` / `ron`
- Async: `tokio` (only when genuinely needed)
- Logging: `tracing` or `log` + `env_logger`
- File I/O: `tempfile` (tests), `walkdir` (traversal)
- Cross-platform paths: `dirs`, `directories`

### 8. Performance

- Use `BufReader`/`BufWriter` for file I/O
- Pre-allocate `Vec` capacity when size is known; use `Cow<'_, str>` to avoid unnecessary allocations
- Use `std::sync::LazyLock` (or `once_cell::sync::Lazy`) for expensive one-time inits like compiled regexes
- Profile before optimizing — use `cargo flamegraph`, `criterion` for benchmarks
- For GUI: keep frame budgets in mind (~16ms for 60fps); avoid allocations in hot render paths

### 9. Testing

- Unit tests: `#[cfg(test)] mod tests` at the bottom of each file; `use super::*`
- File-based tests: `tempfile::tempdir()` for temporary directories
- Follow Arrange-Act-Assert; use helper functions to build test fixtures
- Use `assert!(matches!(...))` for enum variant checks
- Test happy paths, error conditions, and meaningful boundary values
- Add tests where it makes sense; don't add them purely for coverage numbers
- For GUI: test logic and state management independently from rendering; use snapshot/golden tests for UI if the framework supports it

### 10. Forbidden

- `unsafe` code unless explicitly approved by the user
- `unwrap()` / `expect()` in non-test code
- Error libraries other than `anyhow` (no `thiserror`, `eyre`, etc.) unless explicitly approved
- Changing `rustfmt` or `clippy` settings without explicit approval
- Blocking the UI/main thread in GUI applications

### 11. Quality Validation

Run before completion (adjust package name to match the project):
```bash
cargo build -p <package-name>
cargo clippy -p <package-name> -- -D warnings
cargo test -p <package-name>
cargo fmt -p <package-name> -- --check
```

For workspace-wide checks:
```bash
cargo build --workspace
cargo clippy --workspace -- -D warnings
cargo test --workspace
cargo fmt --all -- --check
```

Never run git commit. Summarize changes to the user alongside any problems and caveats.

## When to Use This Skill

- Writing new Rust applications, libraries, or tools
- Building cross-platform GUI applications in Rust
- Adding functionality to existing crates
- Refactoring, debugging, or reviewing Rust code
- Any Rust task where production-quality, idiomatic code is expected