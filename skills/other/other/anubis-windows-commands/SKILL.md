---
name: anubis-windows-commands
description: Prevents Git Bash path conversion issues when running Anubis commands on Windows. Use when building targets with `cargo run` or `anubis.exe` that use `//` target paths.
---

# Anubis Windows Commands

## Problem

When running Claude Code on Windows in Git Bash (MSYS/MinGW environment), the shell automatically converts paths starting with `//` to `/`. This breaks Anubis target paths like `//mode:win_dev` or `//samples/basic/simple_cpp:simple_cpp`.

**Example of the problem:**
```bash
# What you type:
cargo run --release -- build -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp

# What Git Bash sends to the command:
cargo run --release -- build -m /mode:win_dev -t /examples/simple_cpp:simple_cpp
```

This causes Anubis to fail because it expects target paths to start with `//`.

## Solution

Use the `MSYS_NO_PATHCONV=1` environment variable prefix to disable Git Bash path conversion.

## Required Command Format

### For `cargo run` commands:

```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp
```

### For `anubis.exe` directly:

```bash
MSYS_NO_PATHCONV=1 ./target/release/anubis.exe build -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp
```

### For multi-target builds:

```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build --workers 16 -l debug --mode //mode:win_release --targets //samples/basic/nested_staticlib_cpp/...
```

## When to Apply This Fix

Apply `MSYS_NO_PATHCONV=1` when ALL of these conditions are true:

1. **Platform is Windows** (`host_platform` is `windows`)
2. **Shell is Git Bash** (MSYS/MinGW environment - check for `MSYSTEM` env var or `/usr/bin/bash` path)
3. **Command contains `//` paths** (Anubis target notation)

## Detection

To detect if you're in Git Bash on Windows:

```bash
# Check if MSYSTEM is set (Git Bash sets this)
echo $MSYSTEM

# Or check the shell path
echo $SHELL
```

If `MSYSTEM` is set to `MINGW64`, `MINGW32`, or `MSYS`, you're in Git Bash and need the prefix.

## Command Templates

### Build a single target (Windows dev mode):
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp
```

### Build a single target (Windows release mode):
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:win_release -t //samples/basic/simple_cpp:simple_cpp
```

### Build a single target (Linux cross-compile):
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:linux_dev -t //samples/basic/simple_cpp:simple_cpp
```

### Build all targets in a directory (recursive):
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:win_dev -t //samples/basic/...
```

### Build with debug logging:
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -l debug -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp
```

### Build with trace logging and custom worker count:
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build --workers 16 -l trace -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp
```

### Build multiple specific targets:
```bash
MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:win_dev -t //samples/basic/simple_cpp:simple_cpp -t //samples/basic/trivial_cpp:trivial_cpp
```

## Common Anubis Commands Reference

| Action | Command |
|--------|---------|
| Build target | `MSYS_NO_PATHCONV=1 cargo run --release -- build -m //mode:MODE -t //path:target` |
| Install toolchains | `cargo run --release -- install-toolchains` (no `//` paths, no prefix needed) |
| Build Anubis itself | `cargo build --release` (no `//` paths, no prefix needed) |
| Run tests | `cargo test` (no `//` paths, no prefix needed) |

## Notes

- The `MSYS_NO_PATHCONV=1` prefix is harmless on non-Windows systems or non-Git-Bash shells, but it's only necessary in Git Bash on Windows.
- This only affects commands with `//` path arguments. Standard cargo commands like `cargo build` or `cargo test` don't need the prefix.
- The prefix must come before the command, not after.

## Troubleshooting

If you see errors like:
- `Error: Failed to parse target path '/mode:win_dev'`
- `Error: Target path must start with '//'`
- `Error: Invalid target specification`

These indicate Git Bash path conversion is occurring. Add the `MSYS_NO_PATHCONV=1` prefix.
