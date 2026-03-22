---
name: task
description: Build, test, lint, or run the shizuku application. ALWAYS use this skill instead of invoking Go commands or out/shizuku directly.
---

# Shizuku Task Runner

This project uses Task (taskfile.dev) as its build system. **You MUST always use task commands instead of invoking Go commands directly.**

## Critical Rule

**NEVER run these commands directly:**
- `go build`
- `go run`
- `go fmt`
- `go test`

**ALWAYS use the corresponding task commands below.**

## Available Commands

### Build
Compiles the shizuku binary to `out/shizuku`.

```bash
task build
```

**What it does:** Runs `go build -o out/shizuku cmd/main.go`

### Run
Runs the application with arguments.

```bash
task run -- <args>
```

**Examples:**
```bash
task run -- init
task run -- sync
task run -- sync --verbose
task run -- --help
```

**What it does:** Runs `go run cmd/main.go` with the provided arguments

### Lint
Formats all Go code in the project.

```bash
task lint
```

**What it does:** Runs `go fmt ./...` across the codebase

### Test
Runs all tests or specific tests with optional arguments.

```bash
# Run all tests
task test

# Run tests for a specific package
task test -- ./internal/shizukuconfig

# Run a specific test
task test -- -run TestLoadConfig ./internal/shizukuconfig

# Run tests with verbose output
task test -- -v ./...
```

**What it does:** Runs `go test` with the provided arguments (defaults to `./...`)

## Usage Pattern

When you need to:
1. **Build the binary** → Use `task build`
2. **Run the app** → Use `task run -- <args>`
3. **Format code** → Use `task lint`
4. **Run tests** → Use `task test` (with optional `-- <args>`)

## Why Use Task?

1. **Source tracking** - Task watches Go source files and only rebuilds when needed
2. **Consistency** - All developers and CI use the same commands
3. **Simplicity** - Single entry point for all build operations
4. **Project standard** - This is the established pattern for this codebase

## Passing Arguments

When passing arguments to `task run` or `task test`, always use the `--` separator:

```bash
task run -- arg1 arg2       # Correct
task run arg1 arg2          # Wrong - task will interpret these as task flags

task test -- -v ./...       # Correct
task test -v ./...          # Wrong
```

## Integration with Development Workflow

1. After creating or modifying code, run `task lint` to format
2. Run `task test` to ensure tests pass
3. Run `task build` to compile the binary
4. Run `task run -- sync` to test the built functionality

## Automatic Invocation

This skill should be invoked automatically whenever:
- You're about to build the project
- You're about to run the application
- You're about to format code
- You're about to run tests

**Always default to task commands. If you catch yourself about to use `go build`, `go run`, `go fmt`, or `go test`, STOP and use the appropriate task command instead.**

