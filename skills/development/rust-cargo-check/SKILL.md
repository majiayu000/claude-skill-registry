---
name: rust-cargo-check
description: Prefer `cargo check` over `cargo build` when making Rust code changes. Use `cargo check` to quickly verify code compiles; only use `cargo build` when you need to run the executable.
---

# Rust: Prefer `cargo check` Over `cargo build`

## Key Principle

When working with Rust code, use `cargo check` to verify code compiles. Only use `cargo build` when you actually need to run the resulting executable.

## Why `cargo check` is Preferred

| Command | What it does | Speed |
|---------|--------------|-------|
| `cargo check` | Type-checks and validates code compiles | **Fast** |
| `cargo build` | Full compilation + produces executable | Slow |

`cargo check` skips the code generation and linking phases, making it **significantly faster** than `cargo build` - often 2-5x faster or more.

## When to Use Each Command

### Use `cargo check` when:

- Making code changes and verifying they compile
- Iterating on fixes for compiler errors
- Refactoring code
- Adding new functions, structs, or modules
- Fixing type errors
- Any time you just need to know "does this compile?"

```bash
# Quick compilation check
cargo check

# Check with all features
cargo check --all-features

# Check in release mode (catches some additional warnings)
cargo check --release
```

### Use `cargo build` when:

- You need to run the executable afterward
- You're about to execute `cargo run`
- You need to test the actual binary output
- You're preparing a release artifact

```bash
# Build and run
cargo build --release && ./target/release/myapp

# Or just use cargo run (which builds implicitly)
cargo run --release -- <args>
```

## Workflow Example

### Fixing a Compile Error

```bash
# 1. Make code changes to fix the error

# 2. Quick check - does it compile?
cargo check

# 3. If errors remain, fix and check again
cargo check

# 4. Once it compiles, run tests
cargo test

# 5. Only build if you need to run the binary
cargo build --release
```

### Iterating on Code Changes

```bash
# Edit code...
cargo check    # Fast feedback

# Edit more...
cargo check    # Fast feedback

# Edit more...
cargo check    # Fast feedback

# Ready to test the actual program
cargo run --release -- <args>
```

## Common Patterns

### After Editing Rust Files

```bash
# DO: Quick compile check
cargo check

# DON'T: Slow full build just to check compilation
cargo build
```

### Before Running Tests

```bash
# Tests compile the code anyway, so just run them directly
cargo test

# No need to cargo build first
```

### When You Need to Run the Binary

```bash
# cargo run builds automatically, so use it directly
cargo run --release -- build -m //mode:win_dev -t //target:name

# Or build then run separately if you prefer
cargo build --release
./target/release/anubis build -m //mode:win_dev -t //target:name
```

## Summary

| Situation | Command |
|-----------|---------|
| Check if code compiles | `cargo check` |
| Run tests | `cargo test` |
| Run the program | `cargo run` |
| Build for distribution | `cargo build --release` |
| Iterate on fixes | `cargo check` (repeatedly) |

**Default to `cargo check`** - it's your fast feedback loop for Rust development.
