---
name: shell
description: Shell runtime rules for mvdan/sh virtual shell in internal/runtime/virtual.go. Covers positional arguments gotcha (prepend "--"), bash strict mode (set -euo pipefail), arithmetic increment pitfalls.
disable-model-invocation: false
---

# Invowk Shell Runtime Rules

This skill covers how Invowk handles shell interpreters and script execution internally.
**NOT general bash scripting guidance.**

Use this skill when working on:
- `internal/runtime/virtual.go` - Virtual shell runtime
- `cmd/invowk/internal_exec_virtual.go` - Virtual execution command
- Shell script execution logic

---

## Virtual Shell (mvdan/sh)

The virtual runtime uses [mvdan/sh](https://github.com/mvdan/sh), a pure Go POSIX shell interpreter. This provides cross-platform bash-like script execution without requiring an external shell binary.

### Positional Arguments Gotcha

**CRITICAL: Always prepend `"--"` when passing positional arguments to `interp.Params()`.**

The `interp.Params()` function configures shell parameters, but it follows POSIX shell conventions where arguments starting with `-` are interpreted as shell options (like `-e`, `-u`, `-x`).

#### The Problem

Without `"--"`, positional arguments like `-v` or `--env=staging` are interpreted as shell options:

```go
// WRONG: Will fail with "invalid option: -v"
if len(args) > 0 {
    opts = append(opts, interp.Params(args...))
}
```

Error messages you might see:
- `failed to create interpreter: invalid option: "-v"`
- `failed to create interpreter: invalid option: "--"`
- `failed to create interpreter: invalid option: "--env=staging"`

#### The Solution

Prepend `"--"` to signal the end of options:

```go
// CORRECT: "--" signals end of options, remaining args become $1, $2, etc.
if len(args) > 0 {
    params := append([]string{"--"}, args...)
    opts = append(opts, interp.Params(params...))
}
```

#### Why This Works

In POSIX shells, `"--"` is the standard delimiter that terminates option parsing. Everything after `"--"` is treated as a positional parameter, regardless of whether it starts with `-`:

```bash
# Shell equivalent:
set -- -v --env=staging  # Sets $1="-v", $2="--env=staging"
```

### Affected Locations

When working with mvdan/sh in this codebase, ensure `"--"` is prepended in:

1. `internal/runtime/virtual.go` - `Execute()` method
2. `internal/runtime/virtual.go` - `ExecuteCapture()` method
3. `cmd/invowk/internal_exec_virtual.go` - `runInternalExecVirtual()` function

### Testing

This issue manifests on Windows CI because the virtual runtime is the only bash-compatible option there. When adding new mvdan/sh integration points:

1. Test with arguments starting with `-` (e.g., `-v`, `--flag=value`)
2. Run `make test-cli` to verify flag handling works
3. Ensure Windows CI passes

---

## Bash Script Execution

### Strict Mode (`set -euo pipefail`)

All bash scripts in this project use strict mode for safety:

```bash
set -euo pipefail
```

This enables:
- `-e` (errexit): Exit on any command failure
- `-u` (nounset): Error on undefined variables
- `-o pipefail`: Propagate errors through pipes

### Arithmetic Increment Gotcha

**CRITICAL: Never use `((var++))` with `set -e` when `var` might be 0.**

In bash, arithmetic expressions return exit status based on the expression's value:
- `((0))` returns exit status 1 (false)
- `((1))` returns exit status 0 (true)

The post-increment `((x++))` evaluates to the *original* value of `x`:

```bash
# DANGEROUS with set -e:
COUNTER=0
((COUNTER++))  # Evaluates to 0 (the original value), exits with status 1!
               # Script terminates here due to set -e
```

### Safe Arithmetic Patterns

**Use assignment syntax instead of increment operators:**

```bash
# CORRECT: Assignment always succeeds
COUNTER=$((COUNTER + 1))

# CORRECT: Alternative with let and || true guard
let COUNTER++ || true

# CORRECT: Using arithmetic expansion in assignment
: $((COUNTER++))  # The : (colon) command always succeeds
```

### Anti-Patterns to Avoid

```bash
# WRONG: Will fail if COUNTER is 0
((COUNTER++))

# WRONG: Will fail if FAILED is 0
((FAILED++))

# WRONG: Will fail if SKIPPED is 0
((SKIPPED++))
```

### Real-World Example

The VHS test scripts use counters for PASSED, FAILED, and SKIPPED tests:

```bash
# WRONG - Script exits on first skip when SKIPPED is 0:
SKIPPED=0
if [[ ! -f "$golden_file" ]]; then
    ((SKIPPED++))  # Exit status 1, script terminates!
    continue
fi

# CORRECT - Assignment syntax always works:
SKIPPED=0
if [[ ! -f "$golden_file" ]]; then
    SKIPPED=$((SKIPPED + 1))  # Always succeeds
    continue
fi
```

---

## Common Pitfalls

- **Missing `"--"` delimiter** - Always use `append([]string{"--"}, args...)` when calling `interp.Params()` with user-provided positional arguments.
- **Arithmetic with `set -e`** - Always use `VAR=$((VAR + 1))` instead of `((VAR++))` when `VAR` might be 0.
