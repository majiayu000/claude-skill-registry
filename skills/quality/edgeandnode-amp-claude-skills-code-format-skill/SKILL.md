---
name: Code Formatting
description: Format Rust and TypeScript code using justfile tasks (just fmt-file, just fmt-rs, just fmt-ts). Use when user edits .rs/.ts files, mentions formatting, code style, rustfmt, prettier, cleanup, or before commits/PRs. Ensures consistent code style across the codebase.
---

# Code Formatting Skill

This skill provides code formatting operations for the project codebase, which is a Rust workspace with TypeScript components.

## When to Use This Skill

Use this skill when you need to:
- Format code after editing Rust or TypeScript files
- Check if code meets formatting standards
- Ensure code formatting compliance before commits

## Available Commands

### Format Rust Code
```bash
just fmt-rs
```
Formats all Rust code using `cargo +nightly fmt --all`. This is the primary formatting command.

**Alias**: `just fmt` (same as `fmt-rs`)

### Check Rust Formatting
```bash
just fmt-rs-check
```
Checks Rust code formatting without making changes using `cargo +nightly fmt --all -- --check`.

**Alias**: `just fmt-check` (same as `fmt-rs-check`)

### Format Specific File
```bash
just fmt-file <FILE>
```
Formats a specific file (Rust or TypeScript) based on extension. Automatically detects file type.

Examples:
- `just fmt-file src/main.rs` - formats a Rust file
- `just fmt-file typescript/client.ts` - formats a TypeScript file

### Format TypeScript Code
```bash
just fmt-ts
```
Formats all TypeScript code using `pnpm format`.

### Check TypeScript Formatting
```bash
just fmt-ts-check
```
Checks TypeScript code formatting using `pnpm lint`.

## Important Guidelines

### MANDATORY: Format After Every Edit
**You MUST run `just fmt-file <file>` immediately after editing ANY Rust or TypeScript file.**

This is a critical requirement from the project's development workflow:
- Never skip formatting after file edits
- Always use the exact file path that was edited
- Run formatting before any check or test commands

### Example Workflow
1. Edit a Rust file: `src/common/utils.rs`
2. **IMMEDIATELY** run: `just fmt-file src/common/utils.rs`
3. Then run checks: `just check-rs`

## Common Mistakes to Avoid

### ❌ Anti-patterns
- **Never run `cargo fmt` directly** - Use `just fmt-file` or `just fmt-rs`
- **Never run `rustfmt` directly** - The justfile includes proper flags
- **Never skip formatting** - Even "minor" edits need formatting
- **Never format after multiple edits** - Format after EACH file edit
- **Never use `just fmt-rs` for single files** - Use `just fmt-file <file>` for efficiency

### ✅ Best Practices
- Format immediately after each edit
- Use `just fmt-file` for single files (faster)
- Use `just fmt-rs` only when formatting entire codebase
- Run `just fmt-rs-check` to verify formatting before commits

## Next Steps

After formatting your code:
1. **Check compilation** → See `.claude/skills/code-check/SKILL.md`
2. **Run clippy** → See `.claude/skills/code-check/SKILL.md`
3. **Run tests** → See `.claude/skills/code-test/SKILL.md`
