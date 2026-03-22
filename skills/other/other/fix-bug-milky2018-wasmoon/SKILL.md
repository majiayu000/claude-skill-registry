---
name: fix-bug
description: Systematic bug fixing workflow with regression tests and PR creation. Use when the user asks to "fix a bug", "debug an issue", "resolve a problem", or provides error messages/failing tests to fix. Handles reproduction, root cause analysis, test creation, fix implementation, and PR submission.
---

# Fix Bug Workflow

Systematic approach to fixing bugs with proper testing and documentation.

## Workflow

### 1. Reproduce the Bug

Run the provided command or test to observe the failure:

```bash
# For WAST tests
./wasmoon test <file>.wast

# For MoonBit tests
moon test -p <package> -f <file>.mbt

# For specific test by index
moon test -p <package> -f <file>.mbt -i <index>
```

Document:
- Error messages
- Stack traces
- Expected vs actual behavior
- Steps to reproduce

### 2. Analyze Root Cause

Investigate the error systematically:

**a) Examine error messages**
- Identify the failing component
- Note line numbers and function names

**b) Locate relevant code**
- Use Glob to find implementation files: `**/*<keyword>*.mbt`
- Use Grep to search for specific functions or patterns
- Read source code in relevant modules

**c) For WASM-related bugs**
```bash
./wasmoon explore <file>.wat --stage ir vcode mc
```
Check IR, VCode, and machine code for issues.

**d) For crashes or segfaults**
```bash
lldb -- ./wasmoon test <file>.wast
(lldb) run
(lldb) bt  # After crash
```

### 3. Create Regression Test

**Before fixing**, write a test that reproduces the bug:

**For WASM execution bugs:**
```moonbit
test "descriptive_bug_name" {
  let source =
    #|(module
    #|  (func (export "test") (result i32)
    #|    ; Bug-reproducing code here
    #|  )
    #|)
  let result = compare_jit_interp(source, "test", [])
  inspect(result, content="matched")
}
```

**For unit tests:**
```moonbit
test "descriptive_bug_name" {
  let result = buggy_function(input)
  inspect(result, content="expected_value")
}
```

Place the test in the appropriate `*_test.mbt` file in the relevant package.

Verify the test fails:
```bash
moon test -p <package> -f <test_file>.mbt
```

### 4. Implement Fix

Make the necessary code changes:

- Fix the root cause, not just symptoms
- Follow coding standards (see ERRATA.md and CLAUDE.md)
- Keep changes minimal and focused
- Avoid refactoring unless necessary

Run tests to verify:
```bash
moon test -p <package>      # Unit tests
moon test                    # All tests
moon build && ./install.sh  # For wasmoon binary changes
```

### 5. Verify No Regressions

Ensure the fix doesn't break other functionality:

```bash
moon test                    # All unit tests
python3 scripts/run_all_wast.py --rec  # All wast tests
```

### 6. Create Pull Request

**a) Create feature branch**
```bash
git checkout -b fix/<descriptive-name>
```

**b) Commit changes**
```bash
moon fmt && moon info
git add .
git commit -m "$(cat <<'EOF'
fix: <brief description>

- Root cause: <explanation>
- Solution: <what was changed>
- Test: <test that verifies the fix>

EOF
)"
```

**c) Push and create PR**
```bash
git push -u origin fix/<descriptive-name>
gh pr create --title "fix: <brief description>" --body "$(cat <<'EOF'
## Summary
- Root cause: <explanation>
- Solution: <what was changed>
- Test: <test file and description>

## Test Plan
- [ ] Regression test passes
- [ ] All existing tests pass
- [ ] Manual verification of fix

EOF
)"
```

## Best Practices

- Always create a regression test before fixing
- Keep fixes minimal and focused
- Test both the fix and potential regressions
- Document the root cause in commit messages
- Follow project commit message conventions
- Never use `commit --amend` or `push --force` on shared branches

## Command Reference

```bash
# Build and install
moon build && ./install.sh

# Run tests
moon test -p <package> -f <file>.mbt
moon test -p <package> -f <file>.mbt -i <index>

# Analyze WASM
./wasmoon explore <file>.wat --stage ir vcode mc
./wasmoon test <file>.wast
./wasmoon test --no-jit <file>.wast

# Debug with LLDB
lldb -- ./wasmoon test <file>.wast

# Git workflow
git checkout -b fix/<name>
git add . && git commit
git push -u origin fix/<name>
gh pr create
```