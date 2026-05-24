---
name: way-magefile
description: Build tool for Go projects. Use when the user wants to create, edit, or understand Way-specific Magefiles, build targets, or automate Go project tasks.
---

# Mage

Mage is a make-like build tool using Go. You write plain-old go functions, and Mage automatically uses them as Makefile-like runnable targets.

## When to Use

- Creating build scripts for Go projects.
- Automating tasks (install, build, clean, release).
- Managing dependencies between tasks.

## Core Concepts

### 1. Magefiles

- Any Go file with `//go:build mage` (or `+build mage` for older Go).
- Usually named `magefile.go` or placed in `magefiles/` directory.
- `package main`.

### 2. Targets

- Exported functions with specific signatures:
- `func Target()`
- `func Target() error`
- `func Target(ctx context.Context) error`
- First sentence of doc comment is the short description (`mage -l`).

### 3. Dependencies

- Use `mg.Deps(Func)` to declare dependencies.
- Dependencies run exactly once per execution.
- `mg.Deps` runs in parallel; `mg.SerialDeps` runs serially.

## Quick Start

To create a new magefile:
`mage -init`

## Common Tasks

**Running Commands:**
Use `github.com/magefile/mage/sh` for shell execution.

```go
import "github.com/magefile/mage/sh"
// ...
err := sh.Run("go", "build", "./...")
```

**Clean Up:**

```go
import "github.com/magefile/mage/sh"
// ...
sh.Rm("bin")
```

## References

- **Way Conventions**: See [references/way-style.md](references/way-style.md) for Way-specific patterns and helpers.
- **API Documentation**: See [references/api.md](references/api.md) for `mg`, `sh`, and `target` package details.
- **Examples**: See [references/examples.md](references/examples.md) for common patterns.
