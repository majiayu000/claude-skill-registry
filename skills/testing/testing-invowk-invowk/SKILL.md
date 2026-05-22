---
name: testing
description: Testing patterns for *_test.go files, testscript CLI tests (.txtar), race conditions, TUI component testing, container test timeouts. Use when writing tests, debugging flaky tests, or setting up testscript.
disable-model-invocation: false
---

# Testing Patterns

Use this skill when:
- Writing or modifying test files (`*_test.go`)
- Working with testscript CLI integration tests (`.txtar` files)
- Debugging flaky tests or race conditions
- Testing TUI components (Bubble Tea models)
- Testing container runtimes (Docker/Podman)

---

# Testing

## Test File Organization

### Size Limits

**Test files MUST NOT exceed 800 lines.** Large monolithic test files are difficult to navigate and maintain for both humans and AI agents. When a test file approaches this limit, split it by logical concern.

**Naming convention for split files:**
- `<package>_<concern>_test.go` (e.g., `invkfile_parsing_test.go`, `invkfile_deps_test.go`)
- Each file should cover a single logical area (parsing, dependencies, flags, schema validation, etc.)

### Test Helper Consolidation

**Avoid duplicating test helpers across packages.** Common patterns belong in the `testutil` package:

```go
// WRONG: Duplicated in multiple test files
func testCommand(name, script string) Command { ... }

// CORRECT: Centralized in testutil
import "invowk-cli/internal/testutil/invkfiletest"
cmd := invkfiletest.NewTestCommand("hello", invkfiletest.WithScript("echo hello"))
```

When you need a test helper that might be useful elsewhere, add it to `testutil` with clear documentation.

**Acceptable exceptions (local helpers are OK when):**

1. **Same-package testing**: Test files in `pkg/invkfile/` cannot import `internal/testutil/invkfiletest` because it would create an import cycle (invkfiletest imports invkfile). Local helpers like `testCommand()` are acceptable in this case.

2. **Specialized signatures**: Helpers with package-specific signatures that don't generalize well (e.g., `testCommandWithInterpreter()` in runtime tests for interpreter-specific testing).

3. **Single-use helpers**: Helpers used only within one test file that aren't worth extracting.

**Current intentional local helpers:**
- `pkg/invkfile/invkfile_deps_test.go`: `testCommand()`, `testCommandWithDeps()` (import cycle)
- `internal/runtime/runtime_env_test.go`: `testCommandWithScript()`, `testCommandWithInterpreter()` (specialized signatures)

## Testing Patterns

- Test files are named `*_test.go` in the same package.
- Use `t.TempDir()` for temporary directories (auto-cleaned).
- Use table-driven tests for multiple cases.
- Skip integration tests with `if testing.Short() { t.Skip(...) }`.
- Reset global state in tests using cleanup functions.

```go
func TestExample(t *testing.T) {
    // Setup
    tmpDir := t.TempDir()
    originalEnv := os.Getenv("VAR")
    defer os.Setenv("VAR", originalEnv)

    // Test
    result, err := DoSomething()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    // Assert
    if result != expected {
        t.Errorf("got %v, want %v", result, expected)
    }
}
```

## Avoiding Flaky Tests

### Time-Dependent Tests

**NEVER use `time.Sleep()` to verify time-dependent behavior.** This creates flaky tests that fail intermittently based on system load.

```go
// WRONG: Flaky - may pass or fail based on system speed
func TestTokenExpiration(t *testing.T) {
    token := createToken(ttl: 1*time.Millisecond)
    time.Sleep(10 * time.Millisecond)  // FRAGILE!
    if token.IsValid() {
        t.Error("token should be expired")
    }
}

// CORRECT: Deterministic - use clock injection
func TestTokenExpiration(t *testing.T) {
    clock := testutil.NewFakeClock(time.Time{})
    token := createTokenWithClock(ttl: 1*time.Minute, clock: clock)
    clock.Advance(2 * time.Minute)  // Deterministic advance
    if token.IsValid() {
        t.Error("token should be expired")
    }
}
```

### Filesystem Paths

**Always use `t.TempDir()` instead of hardcoded paths like `/tmp`.**

```go
// WRONG: May fail on some systems, leaves files behind
f, _ := os.Create("/tmp/test-file.txt")

// CORRECT: Auto-cleaned, isolated per test
tmpDir := t.TempDir()
f, _ := os.Create(filepath.Join(tmpDir, "test-file.txt"))
```

### Cross-Platform Path Assertions

**NEVER hardcode path separators in test assertions.** Use `filepath.Join()` to construct expected paths so they match production code behavior on all platforms.

The problem: `filepath.Join()` produces OS-specific paths—forward slashes (`/`) on Unix, backslashes (`\`) on Windows. Tests that hardcode Unix-style paths will fail on Windows CI.

```go
// WRONG: Hardcoded Unix path separator - fails on Windows
recorder.AssertArgsContain(t, "/tmp/build/Dockerfile.custom")
// On Windows, actual value is: \tmp\build\Dockerfile.custom

// CORRECT: Use filepath.Join for cross-platform compatibility
recorder.AssertArgsContain(t, filepath.Join("/tmp/build", "Dockerfile.custom"))
// Produces: /tmp/build/Dockerfile.custom (Unix) or \tmp\build\Dockerfile.custom (Windows)
```

**When this applies:**
- Any test that asserts on file paths constructed by production code
- Mock recorders that capture command-line arguments containing paths
- Path comparison in file operation tests

**Common symptom:** Tests pass locally on Linux/macOS but fail on Windows CI with errors like:
```
expected args to contain "/tmp/build/Dockerfile.custom", got: [build -f \tmp\build\Dockerfile.custom ...]
```

**Note:** The `gocritic` linter's `filepathJoin` check may warn when the first argument contains path separators. This is acceptable when testing production code that joins directory paths with filenames—use `//nolint:gocritic` with an explanatory comment.

## TUI Component Testing

TUI components (Bubble Tea models) should have unit tests even though terminal I/O is difficult to mock. Focus on:

1. **Model state transitions**: Test `Init()`, `Update()` with various messages
2. **Text processing**: Test formatting, truncation, wrapping logic
3. **Edge cases**: Empty inputs, very long inputs, unicode, special characters

```go
// Testing a Bubble Tea model without terminal I/O
func TestChooseModel_Navigation(t *testing.T) {
    model := NewChooseModel([]string{"a", "b", "c"})

    // Simulate key press
    model, _ = model.Update(tea.KeyMsg{Type: tea.KeyDown})

    if model.selected != 1 {
        t.Errorf("expected selected=1, got %d", model.selected)
    }
}
```

## Container Runtime Testing

Container runtime code (Docker/Podman) should have both unit tests and integration tests:

1. **Unit tests**: Mock `exec.Command` to verify argument construction without running containers
2. **Integration tests**: Gate with `testing.Short()` and require actual container engine

```go
// Unit test with mocked exec
func TestDockerBuild_Arguments(t *testing.T) {
    execCmd = mockExecCommand  // Inject mock
    defer func() { execCmd = exec.Command }()

    engine := &DockerEngine{}
    engine.Build(ctx, opts)

    // Verify expected arguments were passed
    if !contains(capturedArgs, "--no-cache") {
        t.Error("expected --no-cache flag")
    }
}

// Integration test with real container engine
func TestDockerBuild_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }
    // ... test with real Docker ...
}
```

## CLI Integration Tests (testscript)

CLI integration tests use [testscript](https://pkg.go.dev/github.com/rogpeppe/go-internal/testscript) for deterministic output verification. Tests live in `tests/cli/testdata/` as `.txtar` files.

### Running CLI Tests

```bash
make test-cli    # Run CLI integration tests
make test        # Runs all tests including CLI tests
```

### Working Directory Management

**CRITICAL**: Do NOT set `env.Cd` in test setup. Each test must control its own working directory.

```go
// BAD: Sets initial CWD that conflicts with tests' cd commands
Setup: func(env *testscript.Env) error {
    env.Cd = projectRoot  // NEVER do this!
    return nil
},

// GOOD: Let each test control its own working directory via environment variable
Setup: func(env *testscript.Env) error {
    binDir := filepath.Dir(binaryPath)
    env.Setenv("PATH", binDir+string(os.PathListSeparator)+env.Getenv("PATH"))
    env.Setenv("PROJECT_ROOT", projectRoot)  // Tests can use 'cd $PROJECT_ROOT'
    return nil
},
```

**Two types of tests require different working directories:**

1. **Tests with embedded `invkfile.cue`** - Use `cd $WORK`:
   ```txtar
   # Set working directory to where embedded files are
   cd $WORK
   exec invowk cmd my-embedded-command
   ```

2. **Tests against project's `invkfile.cue`** - Use `cd $PROJECT_ROOT`:
   ```txtar
   # Run against project's invkfile.cue
   cd $PROJECT_ROOT
   exec invowk cmd some-project-command
   ```

### Environment Variables in Setup

- Only set environment variables that are actually used by production code.
- Do NOT set placeholder env vars "for future use" - they cause confusion.
- If a test needs a specific env var cleared, do it in the test file: `env MY_VAR=`

### Container Runtime Test Conditions

**Custom conditions** for container tests must verify actual functionality, not just CLI availability:

```go
containerAvailable = func() bool {
    engine, err := container.AutoDetectEngine()
    if err != nil || !engine.Available() {
        return false
    }
    // CRITICAL: Run a smoke test to verify Linux containers work.
    // This catches Windows Docker in Windows-container mode.
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    result, err := engine.Run(ctx, container.RunOptions{
        Image:   "debian:stable-slim",
        Command: []string{"echo", "ok"},
        Remove:  true,
    })
    return err == nil && result.ExitCode == 0
}()
```

### Shell Script Behavior in Containers

Scripts executed via `/bin/sh -c` do NOT have `set -e` by default. Always add `set -e` when you want scripts to fail on any command failure:

```cue
script: """
    set -e  # Required for fail-on-error behavior
    echo "Starting..."
    some_command_that_might_fail
    echo "Done"
    """
```

### Writing testscript Tests

Test files use the txtar format with inline assertions:

```txtar
# Test: Basic command execution
exec invowk cmd hello
stdout 'Hello from invowk!'
! stderr .

# Test: Command with flags (use -- to separate invowk flags from command flags)
exec invowk cmd 'flags validation' -- --env=staging
stdout '=== Flag Validation Demo ==='
! stderr .
```

### Test File Structure

Each `.txtar` test file should:
1. Have a descriptive comment at the top explaining what it tests.
2. Include skip conditions for optional features (e.g., `[!container-available] skip`).
3. Use `cd $WORK` to set working directory if it uses embedded files.
4. Include the embedded `invkfile.cue` and any other required files.

Example structure:
```txtar
# Test: Description of what this tests
# Tests specific behavior X and verifies Y

# Skip if required feature is unavailable
[!container-available] skip 'no functional container runtime available'

# Set working directory to where test files are
cd $WORK

# Run tests
exec invowk cmd my-command
stdout 'expected output'

-- invkfile.cue --
cmds: [...]

-- other-file.txt --
content
```

### testscript Syntax Reference

| Command | Description |
|---------|-------------|
| `exec cmd args...` | Run a command |
| `stdout 'pattern'` | Assert stdout matches regex pattern |
| `stderr 'pattern'` | Assert stderr matches regex pattern |
| `! stdout .` | Assert stdout is empty |
| `! stderr .` | Assert stderr is empty |
| `env VAR=value` | Set environment variable |
| `cd path` | Change working directory |

### Environment Isolation

testscript runs tests in an isolated environment:
- `HOME` is set to `/no-home` by default
- `USER` and other env vars are not passed through
- Use `env VAR=value` to explicitly set required variables

Example for tests that need environment variables:

```txtar
env HOME=/test-home
env USER=testuser

exec invowk cmd 'deps env single'
stdout 'HOME = '
```

### Flag Separator (`--`)

When passing flags to invowk commands (not to invowk itself), use `--` to separate:

```txtar
# WRONG: --env is interpreted as invowk global flag
exec invowk cmd 'flags validation' --env=staging

# CORRECT: -- separates invowk flags from command flags
exec invowk cmd 'flags validation' -- --env=staging
```

### Current Test Files

| File | Description |
|------|-------------|
| `simple.txtar` | Basic hello + env hierarchy |
| `virtual.txtar` | Virtual shell runtime |
| `deps_tools.txtar` | Tool dependency checks |
| `deps_files.txtar` | File dependency checks |
| `deps_caps.txtar` | Capability checks |
| `deps_custom.txtar` | Custom validation |
| `deps_env.txtar` | Environment dependencies |
| `flags.txtar` | Command flags |
| `args.txtar` | Positional arguments |
| `env.txtar` | Environment configuration |
| `isolation.txtar` | Variable isolation |

### When to Add CLI Tests

Add CLI tests when:
- Adding new CLI commands or subcommands
- Changing command output format
- Modifying flag/argument handling
- Testing environment variable behavior

## VHS Demo Recordings

VHS is used **only for generating demo GIFs** for documentation and website, not for CI testing.

### Generating Demos

```bash
make vhs-demos     # Generate all demo GIFs (requires VHS, ffmpeg, ttyd)
make vhs-validate  # Validate VHS tape syntax
```

Demo tapes live in `vhs/demos/`. See `vhs/README.md` for details.

## testutil Package Reference

The `internal/testutil` package provides reusable test helpers. All helpers accept `testing.TB` to work with both `*testing.T` and `*testing.B`.

### Current Public API

| Function | Description |
|----------|-------------|
| `MustChdir(t, dir)` | Changes working directory; returns cleanup function |
| `MustSetenv(t, key, value)` | Sets environment variable; returns cleanup function |
| `MustUnsetenv(t, key)` | Unsets environment variable; returns cleanup function |
| `MustMkdirAll(t, path, perm)` | Creates directory tree; fails test on error |
| `MustRemoveAll(t, path)` | Removes path; logs warning on error |
| `MustClose(t, closer)` | Closes io.Closer; fails test on error |
| `MustStop(t, stopper)` | Stops server; logs warning on error |
| `DeferClose(t, closer)` | Returns cleanup function for io.Closer |
| `DeferStop(t, stopper)` | Returns cleanup function for Stopper |

### New Helpers (003-test-suite-audit)

**internal/testutil** (clock and home directory):

| Function | Description |
|----------|-------------|
| `SetHomeDir(t, dir)` | Sets HOME/USERPROFILE; returns cleanup function |
| `NewFakeClock(initial)` | Creates fake clock for time mocking |
| `Clock` interface | `Now()`, `After(d)`, `Since(t)` for time abstraction |
| `RealClock` | Production clock using actual time |
| `FakeClock` | Test clock with `Advance(d)` and `Set(t)` |

**internal/testutil/invkfiletest** (command builder - separate package to avoid import cycles):

| Function | Description |
|----------|-------------|
| `NewTestCommand(name, opts...)` | Creates test command with options pattern |
| `WithScript(s)`, `WithRuntime(r)` | Command options for script, runtime |
| `WithFlag(name, opts...)` | Add flag with `FlagRequired()`, `FlagDefault(v)` |
| `WithArg(name, opts...)` | Add arg with `ArgRequired()`, `ArgVariadic()` |

## Race Condition Testing

### TOCTOU Race Conditions

TOCTOU (Time-Of-Check-Time-Of-Use) race conditions occur when there's a gap between checking a condition and acting on it, during which the condition can change. These are particularly common in concurrent Go code with goroutines.

#### Context Cancellation Race Pattern

When a function accepts a `context.Context` and spawns goroutines, there's a race between:
1. The goroutine completing its work
2. The caller detecting context cancellation

**Vulnerable Pattern:**

```go
func (s *Server) Start(ctx context.Context) error {
    // Setup work that may succeed even with cancelled context
    listener, err := lc.Listen(ctx, "tcp", addr)  // May succeed!
    if err != nil {
        return err
    }

    // Start goroutine that transitions state
    go func() {
        s.state.Store(StateRunning)  // Wins the race!
        close(s.startedCh)
        s.serve()
    }()

    // Race: goroutine may complete before this select runs
    select {
    case <-s.startedCh:
        return nil  // Returns success even though ctx was cancelled
    case <-ctx.Done():
        return ctx.Err()  // Never reached if goroutine wins
    }
}
```

**The Solution - Check context cancellation before any setup work:**

```go
func (s *Server) Start(ctx context.Context) error {
    // Early exit if context is already cancelled
    select {
    case <-ctx.Done():
        s.transitionToFailed(fmt.Errorf("context cancelled before start: %w", ctx.Err()))
        return s.lastErr
    default:
    }

    // Now safe to proceed with setup...
    listener, err := lc.Listen(ctx, "tcp", addr)
    // ...
}
```

**Key Principles:**
1. **Check early**: Validate preconditions (including context) before any work
2. **Check at boundaries**: Re-check context after long-running or async operations
3. **Atomic state transitions**: Use `CompareAndSwap` for state changes to prevent concurrent transitions
4. **Don't trust non-blocking success**: Even if an operation succeeds, the context may have been cancelled

### Testing Race Conditions

When fixing race conditions:

```bash
# Run multiple times with race detector, bypassing cache
for i in {1..10}; do
    go test -count=1 -race ./path/to/package/... -run TestName
done
```

- `-count=1`: Bypasses test cache, forces fresh execution
- `-race`: Enables Go's race detector
- Run 10+ times: A single pass doesn't prove the race is fixed

### Common Symptom: Flaky CI Tests

If a test passes locally but fails in CI (or vice versa), suspect a race condition. Different CPU speeds, scheduling, and runner configurations affect goroutine timing.

**Real-World Example** (GitHub Action failure on ubuntu-latest):
```
=== RUN   TestServerStartWithCancelledContext
INFO ssh-server: SSH server started address=127.0.0.1:45163
    server_test.go:307: Start with cancelled context should return error
    server_test.go:313: State should be Failed, got stopped
--- FAIL: TestServerStartWithCancelledContext
```

The test passed on slower runners (ubuntu-24.04) but failed on faster ones where the goroutine consistently won the race.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Large test files | Hard to navigate, maintain | Split files exceeding 800 lines by logical concern |
| Duplicated helpers | Same code in multiple test files | Consolidate in `testutil` package |
| `time.Sleep()` in tests | Flaky, timing-dependent failures | Use clock injection for deterministic tests |
| Hardcoded `/tmp` paths | Isolation issues, leftover files | Use `t.TempDir()` for auto-cleanup |
| Hardcoded path separators | Tests fail on Windows | Use `filepath.Join()` in assertions |
| Testing struct fields | Testing Go's ability to store values | Test behavior, not struct storage |
| Missing TUI tests | State bugs not caught | Test model state transitions |
| Flaky tests across environments | Passes locally, fails in CI | Suspect race conditions; run with `-race` |
| Setting `env.Cd` in testscript Setup | Tests find wrong `invkfile.cue` | Remove `env.Cd`, let tests use `cd $WORK` |
| CLI-only container check | Windows tests run but fail | Add smoke test that runs actual container |
| Missing `set -e` in scripts | Failed commands don't cause script failure | Add `set -e` at script start |
| Unused env vars in testscript Setup | Confusion, false assumptions | Only set vars used by production code |

See `.claude/rules/windows.md` for comprehensive path handling guidance.
