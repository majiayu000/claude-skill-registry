---
name: code-editing
description: Use when writing, modifying, or removing Rust code in the mdvs codebase. Covers implementation workflow, testing, verification, and downstream updates (specs, example_kb, mdbook).
---

# Code Editing Conventions

## Before Writing Code

- Read the relevant existing code first. Explore patterns, naming conventions, module structure, and error handling style already in use.
- Match the existing style — don't introduce new patterns unless discussed with the user.
- If the change is non-trivial, plan it with the user before coding.

## Writing Code

### Style

- No wildcard imports (`use arrow::array::*` → explicit imports)
- Name intermediate data structures — no unnamed tuples or raw HashMaps
- `From` impls for infallible type conversions; constructors when extra parameters are needed
- Functions that don't use `self` should be free functions, not methods
- `anyhow::Result` for error handling in commands and I/O
- Follow the enum-based dispatch pattern (not traits) for runtime choices
- Never silently drop data — serialize to JSON rather than storing NULL
- Check for collisions with internal column prefix when adding new fields

### Cross-cutting changes

If the change touches the type system, a violation type, a command's output, or storage format — trace through the full pipeline:

`discover → schema/config → validation → storage → search → output`

Verify each stage handles the change correctly.

## Testing

- Write unit tests (`#[cfg(test)] mod tests`) for the changed module
- Write integration tests for user-facing behavior changes
- Run the full test suite, not just the changed module:

```bash
cargo test
cargo clippy
cargo fmt
```

Always run `cargo fmt` after `cargo clippy`.

## Updating Specs

- Update the relevant spec in `docs/spec/` if the change affects documented behavior
- Use the `spec` skill for spec writing conventions

## Testing Against `example_kb`

- Run the affected commands against `example_kb` to verify the change works end-to-end
- If the change needs a new edge case, add it to `example_kb`:
  - Create or modify files to exercise the new behavior
  - Update `example_kb/.plan.md` with the new edge case
  - Re-run `mdvs update example_kb` and `mdvs build example_kb --force`

## Updating the mdbook

- If the change affects any command output, re-run those commands and update the book pages with fresh output
- If the change adds new behavior, add a section to the relevant book page (use the `book` skill)
- Check for collateral effects — changes to `example_kb` may invalidate existing output examples across multiple pages
- Search the book for references to affected fields, commands, or concepts

## TODOs

- If the work corresponds to a spec TODO, updating it to done is part of the commit workflow — see the `commit` skill
