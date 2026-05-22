---
name: tmux-tdd
description: Interact with tmux-based TDD environments. Use when running tests in tmux panes, checking test output, parsing test failures, or orchestrating TDD workflows. Works with any language (Rust, Python, JavaScript, Go, etc). Read test output directly from tmux panes.
---

# tmux TDD Skill

Orchestrate Test-Driven Development in a tmux environment by reading test output directly from panes. Language agnostic.

## Environment Layout

```
┌────────────────┬────────────────┐
│                │                │
│   Pane 0.0     │   Pane 0.1     │
│   Claude Code  │   Test Runner  │
│                │                │
└────────────────┴────────────────┘
```

- **Pane 0.0**: Claude Code (where you are)
- **Pane 0.1**: Test runner (cargo watch, pytest, jest, go test, etc.)

## Instructions

### Step 1: Check Current Test Status

Capture output directly from the test pane:

```bash
tmux capture-pane -t 0.1 -p -S -50
```

Options:
- `-t 0.1`: Target pane (test runner)
- `-p`: Print to stdout
- `-S -50`: Last 50 lines (use `-S -` for full history)

### Step 2: Parse Test Results

Look for pass/fail patterns based on the language:

**Rust (cargo test):**
```
test result: ok. 6 passed; 0 failed
test result: FAILED. 4 passed; 2 failed
error[E0425]: cannot find value `x` in this scope
```

**Python (pytest):**
```
6 passed in 0.12s
2 failed, 4 passed in 0.15s
FAILED tests/test_app.py::test_add - AssertionError
E       assert 4 == 5
```

**JavaScript (jest/vitest):**
```
Tests:       6 passed, 6 total
Tests:       2 failed, 4 passed, 6 total
FAIL src/app.test.js
  ✕ should add numbers (5 ms)
```

**Go (go test):**
```
ok      mypackage    0.005s
FAIL    mypackage    0.005s
--- FAIL: TestAdd (0.00s)
    app_test.go:10: expected 5, got 4
```

### Step 3: Make Code Changes

Edit the source files to fix failures. If using a watch mode, tests will automatically re-run.

### Step 4: Verify Fix

Wait for tests to re-run, then capture pane again:

```bash
tmux capture-pane -t 0.1 -p -S -30
```

### Step 5: Send Commands to Test Pane (if needed)

```bash
# Run command in test pane
tmux send-keys -t 0.1 "your-test-command" C-m

# Stop running process
tmux send-keys -t 0.1 C-c
```

## Common Test Commands by Language

| Language | Watch Mode | Single Run |
|----------|------------|------------|
| Rust | `cargo watch -x test` | `cargo test` |
| Python | `ptw` or `pytest-watch` | `pytest` |
| JavaScript | `jest --watch` or `vitest` | `jest` or `npm test` |
| Go | `gotestsum --watch` | `go test ./...` |
| Ruby | `guard` | `rspec` |

## Quick Reference

| Task | Command |
|------|---------|
| Read test output | `tmux capture-pane -t 0.1 -p -S -50` |
| Full history | `tmux capture-pane -t 0.1 -p -S -` |
| Send command | `tmux send-keys -t 0.1 "command" C-m` |
| Stop process | `tmux send-keys -t 0.1 C-c` |
| List panes | `tmux list-panes` |

## TDD Workflow

1. **RED**: Write a failing test, verify it fails via pane capture
2. **GREEN**: Write minimal code to make it pass
3. **REFACTOR**: Clean up while keeping tests green

Always check test status before and after making changes.

## Troubleshooting

**Empty pane output?**
- Test runner may not be running
- Check: `tmux capture-pane -t 0.1 -p -S -5`
- Restart the test watcher in pane 0.1

**Can't connect to pane?**
- Verify tmux session exists: `tmux list-sessions`
- List panes: `tmux list-panes`
