---
name: rust-dev
description: "Rust development standards for git-review: TDD enforcement, error handling patterns, bounded context architecture, and anti-patterns to avoid. Use when writing or reviewing Rust code."
---

# Rust Development Standards

## Architecture: Bounded Contexts

### Parser
Parses raw `git diff` output into `DiffFile` / `DiffHunk` structures. No side effects, pure transformation. Handles unified diff format, binary files, rename detection.

### State
SQLite persistence via rusqlite. Stores review status per hunk (keyed by SHA-256 content hash). Detects stale hunks when diff content changes. Provides `ReviewDb` as the single entry point.

### TUI
ratatui-based interactive interface. File list on left, hunk view on right. Keyboard-driven: navigate hunks, mark reviewed, view progress. Reads from Parser output, writes to State.

### Gate
Pre-commit hook integration. `check_gate` returns whether all hunks are reviewed. `enable_gate` / `disable_gate` install/remove the git hook. Wrapper command for CI integration.

### CLI
clap derive-based argument parsing. Subcommands: `review` (default TUI), `status` (print progress), `gate` (check/enable/disable), `reset` (clear review state).

## TDD Enforcement

Follow red-green-refactor:
1. Write a failing test first
2. Write minimal code to make it pass
3. Refactor while keeping tests green

Use London School (mock-first) for integration boundaries. Use real implementations for pure logic.

## Error Handling

- `thiserror` for library errors in `src/lib.rs` and modules
- `anyhow` for the binary in `src/main.rs`
- No empty catch blocks or silent error swallowing
- Propagate errors with `?` operator; add context with `.context()`

## Anti-Patterns

- Do NOT shell out to `git diff` without sanitizing arguments
- Do NOT store absolute paths in the SQLite database (use repo-relative)
- Do NOT assume UTF-8 for all diff content (handle binary gracefully)
- Do NOT block the TUI event loop with synchronous I/O
- Do NOT use `unwrap()` in library code; reserve for tests only

## Shell/Regex Patterns

- When writing regex in shell hooks, always test edge cases: dashes as grep options (use `--`), underscores in character classes, special chars in branch names
- Run `cargo build` and `cargo test` after any Rust changes before reporting completion
- Prefer `grep -E` over `egrep` (deprecated) and always use `--` before patterns that might start with `-`

## Build & Test Commands

```bash
cargo build                # Build
cargo test                 # Run all tests
cargo clippy               # Lint
cargo fmt --check          # Format check
cargo check                # Type check only
```

- ALWAYS run `cargo test` after code changes
- ALWAYS run `cargo check` before committing
- ALWAYS run `cargo clippy -- -D warnings` before opening PRs

## Definition of Done

- [ ] All tests pass (`cargo test`)
- [ ] No clippy warnings (`cargo clippy -- -D warnings`)
- [ ] Code formatted (`cargo fmt --check`)
- [ ] No hardcoded paths or credentials
- [ ] Public APIs have doc comments
- [ ] Error cases handled, not ignored

## Security Rules

- Sanitize all file paths to prevent directory traversal
- Validate git refs before passing to shell commands
- Never pass unsanitized user input to `std::process::Command`
- Never hardcode API keys or credentials
