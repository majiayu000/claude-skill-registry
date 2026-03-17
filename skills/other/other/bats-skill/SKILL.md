---
name: bats
description: "Bash Automated Testing System (BATS) for TDD-style testing of shell scripts. Use when: (1) Writing unit or integration tests for Bash scripts, (2) Testing CLI tools or shell functions, (3) Setting up test infrastructure with setup/teardown hooks, (4) Mocking external commands (curl, git, docker), (5) Generating JUnit reports for CI/CD, (6) Debugging test failures or flaky tests, (7) Implementing test-driven development for shell scripts."
---

# BATS Testing Framework

BATS (Bash Automated Testing System) is a TAP-compliant testing framework for Bash 3.2+. Think of it as **JUnit for Bash**—structured, repeatable testing for shell scripts.

## Workflow Decision Tree

### Creating New Test Suite
1. Initialize project structure (see "Project Setup" below)
2. Create test files with `.bats` extension
3. Load helper libraries in `setup()`
4. Write tests using `@test` blocks

### Writing Tests
- **Testing script output?** → Use `run` + `assert_output`
- **Testing exit codes?** → Use `run` + `assert_success/assert_failure`
- **Testing file operations?** → Use `bats-file` assertions
- **Mocking external commands?** → See [gotchas.md](references/gotchas.md#mocking-external-commands)

### Debugging Failures
- **Test hangs?** → Check for background tasks holding FD 3
- **Pipes don't work?** → Use `bash -c` wrapper or `bats_pipe`
- **Negation doesn't fail?** → Use `run !` (BATS 1.5+)
- **Variables disappear?** → Don't use `run` for assignments
- See [gotchas.md](references/gotchas.md) for complete troubleshooting

## Project Setup

### Recommended Structure

```
project/
├── src/
│   └── my_script.sh
├── test/
│   ├── bats/                    # bats-core submodule
│   ├── test_helper/
│   │   ├── bats-support/        # Output formatting
│   │   ├── bats-assert/         # Assertions
│   │   ├── bats-file/           # Filesystem assertions
│   │   └── common-setup.bash    # Shared setup logic
│   ├── unit/
│   │   └── parser.bats
│   └── integration/
│       └── api.bats
└── .gitmodules
```

### Initialize Submodules

```bash
git submodule add https://github.com/bats-core/bats-core.git test/bats
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert
git submodule add https://github.com/bats-core/bats-file.git test/test_helper/bats-file
```

### Common Setup Helper

Create `test/test_helper/common-setup.bash`:

```bash
_common_setup() {
    load "$BATS_TEST_DIRNAME/test_helper/bats-support/load"
    load "$BATS_TEST_DIRNAME/test_helper/bats-assert/load"
    load "$BATS_TEST_DIRNAME/test_helper/bats-file/load"
    
    PROJECT_ROOT="$(cd "$BATS_TEST_DIRNAME/.." && pwd)"
    export PATH="$PROJECT_ROOT/src:$PATH"
}
```

## Test File Template

```bash
#!/usr/bin/env bats

setup_file() {
    # Runs ONCE before all tests in file (expensive setup)
    export SHARED_RESOURCE="initialized"
}

setup() {
    # Runs before EACH test
    load 'test_helper/common-setup'
    _common_setup
    TEST_DIR="$BATS_TEST_TMPDIR"
}

teardown() {
    # Runs after EACH test (cleanup)
    rm -rf "$TEST_DIR" 2>/dev/null || true
}

teardown_file() {
    # Runs ONCE after all tests (final cleanup)
    unset SHARED_RESOURCE
}

@test "describe expected behavior" {
    run my_command arg1 arg2
    
    assert_success
    assert_output --partial "expected substring"
}
```

## The `run` Helper

`run` captures exit status and output in a subshell:

```bash
run command arg1 arg2

# Available after run:
$status              # Exit code
$output              # Combined stdout+stderr
${lines[@]}          # Array of output lines
${lines[0]}          # First line

# Implicit status checks (BATS 1.5+)
run -1 failing_command      # Expect exit code 1
run ! command               # Expect non-zero exit
run --separate-stderr cmd   # Separate $output and $stderr
```

**Critical**: `run` always returns 0 to BATS. Always check `$status` explicitly or use assertions.

## Core Assertions (bats-assert)

```bash
# Exit status
assert_success                    # $status == 0
assert_failure                    # $status != 0
assert_failure 1                  # $status == 1

# Output
assert_output "exact match"
assert_output --partial "substring"
assert_output --regexp "^[0-9]+$"

# Lines
assert_line "any line matches"
assert_line --index 0 "first line"
assert_line --partial "substring"

# Negations
refute_output "not this"
refute_line "not in output"
```

## File Assertions (bats-file)

```bash
assert_file_exists "/path/to/file"
assert_dir_exists "/path/to/dir"
assert_file_executable "/path/to/script"
assert_file_not_empty "/path/to/file"
assert_file_contains "/path/to/file" "search text"
```

## Temporary Directories

| Variable | Scope | Use Case |
|----------|-------|----------|
| `$BATS_TEST_TMPDIR` | Per test | **Always use for isolation** |
| `$BATS_FILE_TMPDIR` | Per file | Shared fixtures in `setup_file` |
| `$BATS_RUN_TMPDIR` | Per run | Rarely needed |

```bash
@test "file operations" {
    echo "data" > "$BATS_TEST_TMPDIR/file.txt"
    run process_file "$BATS_TEST_TMPDIR/file.txt"
    assert_success
    # Automatically cleaned up
}
```

## Mocking External Commands

Mock via PATH manipulation:

```bash
@test "mock curl" {
    mkdir -p "$BATS_TEST_TMPDIR/bin"
    cat > "$BATS_TEST_TMPDIR/bin/curl" <<'EOF'
#!/bin/bash
echo '{"status":"ok"}'
EOF
    chmod +x "$BATS_TEST_TMPDIR/bin/curl"
    export PATH="$BATS_TEST_TMPDIR/bin:$PATH"
    
    run script_using_curl
    assert_output --partial "status"
}
```

## Running Tests

```bash
# Basic execution
bats test/                           # All tests
bats -r test/                        # Recursive
bats --jobs 4 test/                  # Parallel

# Filtering
bats --filter "login" test/          # By name regex
bats --filter-tags api,!slow test/   # By tags
bats --filter-status failed test/    # Re-run failures

# Output formats
bats --formatter junit --output ./reports test/  # JUnit for CI
bats --timing test/                              # Show durations
```

## Tagging Tests

```bash
# bats test_tags=api,smoke
@test "user login" { }

# Run tagged tests
bats --filter-tags api test/           # Has 'api'
bats --filter-tags api,!slow test/     # Has 'api' but not 'slow'
```

## Skip Tests

```bash
@test "not ready" {
    skip "Feature not implemented"
}

@test "requires docker" {
    command -v docker || skip "Docker not installed"
    run docker ps
}
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run tests
  run: ./test/bats/bin/bats --formatter junit --output ./reports test/

- name: Publish results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: reports/report.xml
```

### GitLab CI

```yaml
test:
  script:
    - bats --formatter junit --output reports/ test/
  artifacts:
    reports:
      junit: reports/report.xml
```

## Reference Documentation

- **Common pitfalls and debugging**: See [references/gotchas.md](references/gotchas.md)
- **Complete assertion reference**: See [references/assertions.md](references/assertions.md)
- **Real-world project examples**: See [references/projects.md](references/projects.md)
- **CI/CD integration patterns**: See [references/ci-integration.md](references/ci-integration.md)

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Test passes but should fail | Use `assert_failure` or check `$status` |
| Pipes don't work with `run` | Use `run bash -c "cmd1 \| cmd2"` |
| `! true` doesn't fail test | Use `run ! true` (BATS 1.5+) |
| Variables lost after `run` | Don't use `run` for assignments |
| Test hangs indefinitely | Close FD 3 for background tasks: `cmd 3>&- &` |
| Output has ANSI colors | Use `strip_colors` helper or `NO_COLOR=1` |

## Code Style

- Use `run` for capturing output, direct execution for state changes
- Always check `$status` or use assertions
- Prefer `$BATS_TEST_TMPDIR` over hardcoded paths
- Mock external dependencies, not internal logic
- Name tests to describe expected behavior
