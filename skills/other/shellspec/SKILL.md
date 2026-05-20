---
name: shellspec
description: Comprehensive unit testing framework for Bash and POSIX shell scripts using ShellSpec with TDD/BDD best practices. Use when writing tests for shell scripts, debugging test failures, refactoring scripts for testability, setting up test infrastructure, mocking external dependencies, or implementing test-driven development for Bash/shell projects. Covers test structure, isolation, mocking, output capture, coverage, CI integration, and troubleshooting.
---

# ShellSpec Unit Testing Guide

ShellSpec is a full-featured BDD unit testing framework for bash, ksh, zsh, dash and all POSIX shells. It brings professional-grade Test-Driven Development (TDD) practices to shell scripting.

**Think of ShellSpec as**: A translator between natural language test intentions and shell execution verification - like having a bilingual interpreter who understands both "what you want to test" and "how shells actually work."

## Quick Start

### Installation

```bash
# Install ShellSpec
curl -fsSL https://git.io/shellspec | sh -s -- -y

# Initialize project
shellspec --init
```

### Basic Test Example

```bash
# lib/calculator.sh
add() { echo "$(($1 + $2))"; }

# spec/calculator_spec.sh
Describe 'Calculator'
  Include lib/calculator.sh
  
  It 'performs addition'
    When call add 2 3
    The output should eq 5
  End
End
```

**Run tests**: `shellspec`

## Project Structure

```
project/
├── .shellspec              # Project configuration (mandatory)
├── .shellspec-local        # Local overrides (gitignored)
├── lib/                    # Production code
│   ├── module1.sh
│   └── module2.sh
├── spec/                   # Test specifications
│   ├── spec_helper.sh      # Global test setup
│   ├── support/            # Shared test utilities
│   │   ├── mocks.sh
│   │   └── helpers.sh
│   └── lib/
│       ├── module1_spec.sh
│       └── module2_spec.sh
├── coverage/               # Coverage reports (generated)
└── report/                 # Test reports (generated)
```

## Test Structure

### DSL Hierarchy

```bash
Describe 'Feature Name'              # Top-level grouping
  BeforeEach 'setup_function'        # Runs before each test
  AfterEach 'cleanup_function'       # Runs after each test
  
  Context 'when condition X'         # Scenario grouping
    It 'behaves in way Y'            # Individual test
      # GIVEN: Setup (arrange)
      local input="test data"
      
      # WHEN: Execute (act)
      When call function_under_test "$input"
      
      # THEN: Verify (assert)
      The output should equal "expected"
      The status should be success
    End
  End
End
```

**Analogy**: Think of tests like a filing cabinet - `Describe` is the drawer, `Context` is the folder, `It` is the document.

### Execution Modes

| Mode              | Use Case            | Isolation         | Coverage |
| ----------------- | ------------------- | ----------------- | -------- |
| `When call func`  | Unit test functions | Same shell (fast) | Yes      |
| `When run script` | Integration test    | New process       | Yes      |
| `When run source` | Hybrid approach     | Subshell          | Yes      |

**Recommended**: Use `When call` for unit tests (fastest), `When run script` for integration tests.

## Making Scripts Testable

### Pattern 0: Logger-Driven Testability (Foundation)

**Analogy**: Like a black box flight recorder - captures execution paths for post-flight analysis, enabling verification of which code branches executed.

For scripts verification via tests, use the project's logger (`.scripts/_logger.sh`). Each module declares its own unique logger tag that can be partially enabled or disabled via the `DEBUG` environment variable.

**Module Setup**:

```bash
#!/bin/bash
# my_module.sh

# shellcheck source=.scripts/_logger.sh
source "${E_BASH:-$(dirname "$0")}/_logger.sh"

process_data() {
  local input="$1"
  
  if [[ -z "$input" ]]; then
    echo:Mymodule "validation failed: empty input"
    return 1
  fi
  
  echo:Mymodule "processing: $input"
  # ... actual processing ...
  echo:Mymodule "completed successfully"
  return 0
}

# DO NOT allow execution of code bellow those line in shellspec tests
${__SOURCED__:+return}

# Declare unique logger for this module
logger:init "mymodule" "[mymodule] " ">&2"

```

**Controlling Logger Output**:

```bash
# Enable specific loggers via DEBUG variable
DEBUG=mymodule ./my_module.sh       # Enable only 'mymodule' logger
DEBUG=mymodule,hooks ./my_module.sh # Enable multiple loggers
DEBUG=* ./my_module.sh              # Enable all loggers
DEBUG=*,-mymodule ./my_module.sh    # Enable all except 'mymodule'
```

**Test Verification Strategy**:

```bash
Describe 'my_module'
  Include .scripts/_logger.sh
  Include my_module.sh
  
  # Helper functions to strip ANSI color codes for comparison
  # $1 = stdout, $2 = stderr, $3 = exit status
  no_colors_stderr() { echo -n "$2" | sed -E $'s/\x1B\\[[0-9;]*[A-Za-z]//g; s/\x1B\\([A-Z]//g; s/\x0F//g' | tr -s ' '; }
  no_colors_stdout() { echo -n "$1" | sed -E $'s/\x1B\\[[0-9;]*[A-Za-z]//g; s/\x1B\\([A-Z]//g; s/\x0F//g' | tr -s ' '; }
  
  BeforeEach 'enable_logger'
  enable_logger() {
    TAGS[mymodule]=1  # Enable logger output for verification
  }
  
  Context 'when input is empty'
    It 'logs validation failure and returns error'
      When call process_data ""
      The status should be failure
      # Verify execution path via logger output
      The stderr should include "validation failed: empty input"
    End
  End
  
  Context 'when input is valid'
    It 'logs processing steps and succeeds'
      When call process_data "test-data"
      The status should be success
      # Verify which branch executed via log messages
      The result of no_colors_stderr should include "processing: test-data"
      The result of no_colors_stderr should include "completed successfully"
    End
  End
End
```

**Testability Balance**: Achieve comprehensive test coverage by combining:

| Verification Method | Use Case                                    | Example                                                                    |
| ------------------- | ------------------------------------------- | -------------------------------------------------------------------------- |
| **Logger output**   | Verify execution paths, internal decisions  | `The stderr should include user-friendly message like "branch A executed"` |
| **stdout**          | Verify user-facing output, function results | `The output should eq "result"`                                            |
| **stderr**          | Verify error messages, warnings             | `The error should include "warning"`                                       |
| **Exit status**     | Verify success/failure outcomes             | `The status should be failure`                                             |
| **Mocks/Spies**     | Verify external command calls in isolation  | `Mock curl; ...; End`                                                      |

**Test Isolation Pattern** (Mocking Logger Functions):

The practical approach used in tests is to:
1. Set `DEBUG=tag` once at the file level to enable specific logger(s)
2. Mock `logger:init` to suppress logger initialization side effects
3. Mock `echo:Tag` and `printf:Tag` functions to redirect output for verification

```bash
#!/usr/bin/env bash
# spec/mymodule_spec.sh

eval "$(shellspec - -c) exit 1"

# 1. Enable debug output for this module at file level
export DEBUG="mymodule"

# 2. Mock logger initialization to prevent side effects
Mock logger:init
  return 0
End

# 3. Mock logger output functions - redirect to stderr for test verification
Mock printf:Mymodule
  printf "$@" >&2
End

Mock echo:Mymodule
  echo "$@" >&2
End

# Helper to strip ANSI color codes for comparison
# $1 = stdout, $2 = stderr, $3 = exit status
no_colors_stderr() { 
  echo -n "$2" | sed -E $'s/\x1B\\[[0-9;]*[A-Za-z]//g; s/\x1B\\([A-Z]//g; s/\x0F//g' | tr -s ' '
}

Include ".scripts/mymodule.sh"

Describe 'mymodule'
  It 'verifies execution path via logger output'
    When call process_data "test"

    The status should be success
    # Verify which code branch executed via logger messages
    The result of function no_colors_stderr should include "processing: test"
  End
End
```

**Alternative: Suppress Logger Output Entirely**:

When you don't need to verify logger output but want to prevent noise:

```bash
# Mock logger functions to suppress all output
Mock echo:Mymodule
  :  # No-op - silently ignore
End

Mock printf:Mymodule
  :  # No-op - silently ignore
End
```

**Pros**: Precise verification of code paths, debuggable tests, controlled verbosity
**Cons**: Requires logger discipline in production code
**Recommended action**: Add unique logger to each module, use `DEBUG=tag` to control output, verify logs in tests

### Pattern 1: Source Guard (Critical)

**Analogy**: Like a bouncer at a club - decides whether to let execution in based on context.

```bash
#!/bin/bash
# my_script.sh

# Testable functions
process_data() {
  validate_input "$1" || return 1
  transform_data "$1"
}

validate_input() {
  [[ -n "$1" ]] || return 1
}

# Source guard - prevents execution when sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  # Only runs when executed, not when sourced for testing
  process_data "$@"
fi
```

**Test file**:
```bash
Describe 'my_script'
  Include my_script.sh  # Loads functions without executing
  
  It 'validates input'
    When call validate_input ""
    The status should be failure
  End
End
```

**Pros**: Functions become unit-testable, zero test pollution in production code
**Cons**: Requires discipline, legacy scripts need refactoring
**Recommended action**: Always add source guards to new scripts

### Pattern 2: Extract Functions from Pipelines

```bash
# ❌ BAD: Untestable inline pipeline
cat /etc/passwd | grep "^${USER}:" | cut -d: -f6

# ✅ GOOD: Testable functions
get_user_home() {
  local user="${1:-$USER}"
  grep "^${user}:" /etc/passwd | cut -d: -f6
}

process_user_homes() {
  local home
  home=$(get_user_home "$1")
  [[ -n "$home" ]] && check_bashrc "$home"
}
```

**Recommended action**: Extract every logical step into a named function

### Pattern 3: Exit Call Interception for Testability

**Problem**: Functions that call `exit 1` terminate the entire test suite, making them untestable.

**Real Example**:
```bash
function check_working_tree_clean() {
    if ! git diff-index --quiet HEAD --; then
        echo "❌ You have uncommitted changes."
        exit 1  # ❌ Terminates entire test suite
    fi
}
```

**Solution**: Function-specific mocking that preserves logic but replaces `exit` with `return`:

```bash
Describe 'git verification'
  It 'prevents patching with uncommitted changes'
    # Modify tracked file to create uncommitted changes
    echo "modification" >> test_file.txt

    # Mock the function to avoid test termination
    check_working_tree_clean() {
      if ! git diff-index --quiet HEAD --; then
        echo "❌ You have uncommitted changes."
        return 1  # Return 1 instead of exit 1
      fi
      return 0
    }

    When call check_working_tree_clean
    The status should be failure
    The stderr should include "uncommitted changes"
  End
End
```

**Key Learning**: Test what the function does (detect uncommitted changes) rather than how it does it (calling exit).

**Pros**: Makes functions with exit calls testable without modifying production code
**Cons**: Requires duplicating function logic in tests
**Recommended action**: For new code, use `return` instead of `exit` in library functions. For existing code, use the mock pattern above.

## Dependency Isolation and Mocking

### Three-Tier Mocking Strategy

**1. Function-Based Mocks** (Fastest)
```bash
Describe 'function mocking'
  date() { echo "2024-01-01 00:00:00"; }
  
  It 'uses mocked date'
    When call get_timestamp
    The output should eq "2024-01-01 00:00:00"
  End
End
```

**2. Mock Block** (Cleaner)
```bash
Describe 'command mocking'
  Mock curl
    echo '{"status": "success"}'
    return 0
  End
  
  It 'handles API response'
    When call fetch_data
    The output should include "success"
  End
End
```

**3. Intercept Pattern** (For Built-ins)
```bash
Describe 'intercepting built-ins'
  Intercept command
  
  __command__() {
    if [[ "$2" == "rm" ]]; then
      echo "MOCK: rm intercepted"
      return 0
    fi
    command "$@"
  }
  
  It 'safely mocks dangerous operations'
    When run source ./cleanup_script.sh
    The output should include "MOCK: rm intercepted"
  End
End
```

**Decision Matrix**:

| Dependency                  | Mock?       | Rationale           |
| --------------------------- | ----------- | ------------------- |
| Network (curl, wget)        | ✅ Always    | Slow, unreliable    |
| Date/time                   | ✅ Always    | Reproducibility     |
| Random values               | ✅ Always    | Deterministic tests |
| System commands (grep, sed) | ❌ Rarely    | Fast, stable        |
| File I/O                    | ⚠️ Sometimes | Use temp dirs       |

**Recommended action**: Mock boundaries (network, time, random), trust stable commands

## Output Capture and Comparison

### Capturing stdout, stderr, and exit status

```bash
It 'captures all output streams'
  When call function_with_output
  The output should eq "stdout message"      # stdout
  The error should eq "error message"        # stderr
  The status should be success               # exit code (0)
End
```

### Comparing Without Color Codes

```bash
# Helper functions to strip ANSI color codes for comparison
# $1 = stdout, $2 = stderr, $3 = exit status
no_colors_stderr() { echo -n "$2" | sed -E $'s/\x1B\\[[0-9;]*[A-Za-z]//g; s/\x1B\\([A-Z]//g; s/\x0F//g' | tr -s ' '; }
no_colors_stdout() { echo -n "$1" | sed -E $'s/\x1B\\[[0-9;]*[A-Za-z]//g; s/\x1B\\([A-Z]//g; s/\x0F//g' | tr -s ' '; }

It 'compares without colors'
  When call colored_output
  The result of no_colors_stdout should eq "Plain text"
  The result of no_colors_stderr should eq "Plain text"
End

# Alternative: Disable colors via environment
It 'disables colors'
  BeforeCall 'export NO_COLOR=1'
  BeforeCall 'export TERM=dumb'
  When call my_command
  The output should not include pattern '\x1B\['
End
```

**Recommended action**: Set `NO_COLOR=1` in test environment to avoid color-stripping

## Test Environment Management

### Temporary Directories

```bash
eval "$(shellspec - -c) exit 1"

# shellcheck disable=SC2288
% TEST_DIR: "$SHELLSPEC_TMPBASE/tmprepo"

Describe 'isolated environment'
  BeforeEach 'setup_test_env'
  AfterEach 'cleanup_test_env'
  
  setup_test_env() {
    mkdir -p "$TEST_DIR" || true
    cd "$TEST_DIR" || exit 1
  }
  
  cleanup_test_env() {
    cd - >/dev/null
    rm -rf "$TEST_DIR"
  }
  
  It 'works in isolation'
    When call touch test.txt
    The path test.txt should be file
  End
End
```

**Pros**: Complete isolation, no test interference
**Cons**: Requires discipline in cleanup
**Recommended action**: Always use temp dirs, never write to fixed paths

### Parameterized Tests

```bash
Describe 'data-driven tests'
  Parameters
    "#1" "valid"   "success" 0
    "#2" "invalid" "error"   1
    "#3" "empty"   "missing" 1
  End
  
  It "handles $1 input"
    When call validate "$2"
    The output should include "$3"
    The status should eq $4
  End
End
```

**Recommended action**: Use Parameters to avoid copy-paste test code

## Code Coverage

### Enable Coverage

```bash
# .shellspec configuration
--kcov
--kcov-options "--include-pattern=.sh"
--kcov-options "--exclude-pattern=/spec/,/coverage/"
--kcov-options "--fail-under-percent=80"

# Run with coverage
shellspec --kcov

# View report
open coverage/index.html
```

**Coverage Goals**:
- Critical paths: 100%
- Main functionality: 80-90%
- Utility functions: 70-80%

**Recommended action**: Enable coverage from day 1, set minimum thresholds

## Test Execution

### Running Tests

```bash
# All tests
shellspec

# Specific file
shellspec spec/module_spec.sh

# Specific line
shellspec spec/module_spec.sh:42

# Only previously failed
shellspec --quick

# Stop on first failure
shellspec --fail-fast

# Parallel execution (4 jobs)
shellspec --jobs 4

# With debug trace
shellspec --xtrace

# Focus mode (run only fIt, fDescribe)
shellspec --focus
```

### Focus Mode for TDD

```bash
Describe 'feature under development'
  fIt 'focused test - runs only this'
    When call new_feature
    The status should be success
  End
  
  It 'other test - skipped during focus'
    When call other_feature
  End
End
```

**Recommended action**: Use `--quick` and `--focus` for rapid TDD cycles

## Cross-Platform Testing

### GNU vs BSD Tool Compatibility

**Problem**: Shell scripts that work on Linux (GNU tools) often fail on macOS (BSD tools) due to command syntax differences.

**Common Differences**:

| Feature         | GNU (Linux)          | BSD (macOS)          | Portable Alternative    |
| --------------- | -------------------- | -------------------- | ----------------------- |
| Remove last line | `head -n -1`         | Not supported        | `sed '$d'`              |
| Remove first line | `tail -n +2`        | Works differently    | `sed '1d'`              |
| In-place editing | `sed -i 's/old/new'` | `sed -i '' 's/...'`  | Use `sponge` or temp file |

**Real Example**: Function to display function body

```bash
# ❌ GNU-only - fails on macOS
show_function() {
  declare -f "$1" | tail -n +3 | head -n -1
}

# ✅ Cross-platform - works on both
show_function() {
  declare -f "$1" | tail -n +3 | sed '$d'
}
```

**Test Detection Pattern**:
```bash
# Test failure on macOS looks like:
head: illegal line count -- -1
```

**Best Practices**:

1. **Use portable alternatives by default**:
```bash
# Instead of: head -n -1 (remove last N lines)
Use: sed '$d'              # Delete last line

# Instead of: tail -n +2 (skip first N lines)
Use: sed '1d'              # Delete first line
```

2. **Test on multiple platforms**:
```yaml
# .github/workflows/test.yml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - run: shellspec --kcov
```

3. **Use conditional logic only when necessary**:
```bash
# Detect platform when you must use different approaches
if [[ "$(uname -s)" == "Darwin" ]]; then
  # BSD-specific code
  sed -i '' 's/old/new' file
else
  # GNU-specific code
  sed -i 's/old/new' file
fi
```

4. **Document platform-specific requirements** in your README

**Prevention Checklist**:
- [ ] Avoid `head -n -N` (negative line counts)
- [ ] Avoid `tail -n +N` for offset beyond first line
- [ ] Use portable `sed '$d'` instead of `head -n -1`
- [ ] Test on both Linux and macOS in CI
- [ ] Document any platform-specific dependencies

**Recommended action**: Always prefer portable commands, use platform detection only when unavoidable

## CI/CD Integration

### JUnit Reports

```bash
# .shellspec configuration
--format junit
--output report/junit.xml

# Run in CI
shellspec --kcov --format junit
```

### GitHub Actions Example

```yaml
name: ShellSpec Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Install ShellSpec
      run: curl -fsSL https://git.io/shellspec | sh -s -- -y
    - name: Run tests
      run: shellspec --kcov --format junit
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

**Recommended action**: Generate JUnit reports for CI integration

## Troubleshooting

### Debug Failed Tests

```bash
# Show execution trace
shellspec --xtrace spec/failing_spec.sh

# Check spec syntax
shellspec --syntax-check spec/failing_spec.sh

# See generated shell code
shellspec --translate spec/failing_spec.sh

# Inspect output during test
It 'debugs with Dump'
  When call my_function
  Dump  # Shows stdout, stderr, status
  The output should not be blank
End
```

### Common Issues

**Problem**: File assertion fails even though code works correctly
**Solution**: This is caused by ShellSpec's execution order - `After` hooks run BEFORE file assertions

**Critical: ShellSpec Execution Order Violation**

ShellSpec's execution order violates the expected "setup → test → cleanup" flow:

```
# Expected flow: setup → test → cleanup
# Actual flow: setup → test → After hooks → assertions → cleanup
```

**The Problem**: `After` hooks run **BEFORE** file assertions are evaluated. Any file cleanup in `After` will delete files before assertions can check them.

**Pattern**: Negative assertions can mask cleanup issues, while positive assertions expose them.

```bash
# ✅ Negative assertions often pass (deleted file doesn't contain content)
The file ".config" should not include "removed_setting"

# ❌ Positive assertions fail (file no longer exists after cleanup)
The file ".config" should include "preserved_setting"
```

**The Fix**: Capture file content in the same execution as the command:

```bash
# ❌ WRONG - File assertion happens AFTER After hooks
It 'should check file content after command'
  When run ./my_script.sh
  The file ".config" should include "important_setting"
End

# ✅ CORRECT - Capture content in same execution
It 'should check file content after command'
  When run sh -c './my-script.sh && cat .config'
  The output should include "important_setting"
End

# ✅ EVEN BETTER - Use separator for clarity
It 'should modify files and verify content'
  When run sh -c './script.sh && echo "=== FILE: config ===" && cat config'
  The output should include "=== FILE: config ==="
  The output should include "important_setting"
End
```

**When to Suspect This Issue**:
- Test checks `The file "somefile" should include "content"`
- Test runs a command that creates/modifies files
- Test has `After` cleanup hooks
- Manual verification shows the code works correctly

**Problem**: "Evaluation has already been executed. Only one Evaluation allow per Example."
**Solution**: ShellSpec enforces exactly one `When run` per example - chain commands instead

**One-Evaluation Rule**

```bash
# ❌ WRONG - Multiple evaluations not allowed
It 'should verify multiple things'
  When run ./script.sh
  When run cat result.txt  # ERROR: Evaluation already executed
  The output should include "success"
End

# ✅ CORRECT - Chain commands in single execution
It 'should verify multiple things'
  When run sh -c './script.sh && echo "=== SEPARATOR ===" && cat result.txt'
  The output should include "success"
  The output should include "=== SEPARATOR ==="
End
```

**Problem**: Test passes alone but fails in suite
**Solution**: Check for global state leakage, ensure cleanup in `AfterEach`

**Problem**: Can't mock external command
**Solution**: Use `Mock` block or `Intercept` for built-ins

**Problem**: Tests are slow
**Solution**: Enable parallel execution with `--jobs 4`

**Problem**: Coverage doesn't work
**Solution**: Ensure kcov is installed, check `--kcov-options`

## Best Practices Checklist

- [ ] All scripts have source guards
- [ ] External dependencies are mocked
- [ ] Tests use temporary directories
- [ ] Each test verifies one behavior
- [ ] Tests follow GIVEN/WHEN/THEN structure
- [ ] Coverage is enabled and > 80%
- [ ] Tests run in parallel (`--jobs`)
- [ ] JUnit reports generated for CI
- [ ] No hard-coded paths or commands
- [ ] Side effects are documented and tested

## Common Anti-Patterns to Avoid

❌ **Global state mutation**
```bash
COUNTER=0  # Bad: mutable global
increment() { COUNTER=$((COUNTER + 1)); }
```

✅ **Return values**
```bash
increment() { echo $(($1 + 1)); }  # Good: pure function
counter=$(increment "$counter")
```

❌ **Testing implementation details**
```bash
It 'calls grep with -E flag'  # Bad: too coupled
```

✅ **Testing behavior**
```bash
It 'finds files matching pattern'  # Good: tests outcome
```

❌ **Unmocked network calls**
```bash
It 'fetches real data' curl https://api.com  # Bad: slow, flaky
```

✅ **Mocked dependencies**
```bash
Mock curl; echo "mock"; End  # Good: fast, reliable
```

## Advanced Topics

For deeper coverage of advanced patterns, see:

- **Advanced Patterns**: See [references/advanced-patterns.md](references/advanced-patterns.md) for complex mocking, spies, state management
- **Troubleshooting Guide**: See [references/troubleshooting.md](references/troubleshooting.md) for systematic debugging
- **Real-World Examples**: See [references/real-world-examples.md](references/real-world-examples.md) for production patterns from top OSS projects
- **Collected Experience**: See [references/collected-experience.md](references/collected-experience.md) for lessons learned from multiple projects

## Quick Reference

```bash
# Common commands
shellspec                   # Run all tests
shellspec --quick           # Re-run failures only
shellspec --xtrace          # Debug trace
shellspec --kcov            # With coverage
shellspec --format junit    # JUnit output

# DSL basics
Describe/Context/It/End     # Test structure
When call/run/source        # Execution
The output/status/error     # Assertions
Mock/Intercept              # Mocking
BeforeEach/AfterEach        # Hooks
Parameters                  # Data-driven tests
Dump                        # Debug helper
```

**Recommended action**: Start with simple unit tests, add coverage, then integrate into CI
