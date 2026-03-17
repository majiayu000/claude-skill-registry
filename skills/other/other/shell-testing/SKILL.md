---
name: shell-testing
description: Use when testing shell scripts with Bats or linting with ShellCheck. Covers mocking strategies, assertion patterns, ShellCheck configuration opinions, and CI integration.
---

# Shell Testing

## Decision: Bats vs Plain Assertions

- **Bats** for anything with >3 test cases, fixtures, or mocking needs
- **Plain bash assertions** for smoke tests or single-function validation
- Always use `bats-core` (not legacy `bats`) -- it supports `setup_file`/`teardown_file`, parallel execution

## Bats Patterns That Matter

### Mocking External Commands via PATH

Preferred over function mocking -- works across subshells and child processes:

```bash
setup() {
    STUBS_DIR="$TMPDIR/stubs"; mkdir -p "$STUBS_DIR"
    export PATH="$STUBS_DIR:$PATH"
}

create_stub() {
    local cmd="$1" output="$2" code="${3:-0}"
    printf '#!/bin/bash\necho "%s"\nexit %s\n' "$output" "$code" > "$STUBS_DIR/$cmd"
    chmod +x "$STUBS_DIR/$cmd"
}
```

Why: `export -f` mocking breaks across `run` boundaries and subshells. PATH stubs are reliable.

### setup_file vs setup

- `setup_file` / `teardown_file` -- expensive one-time work (DB fixtures, compilation)
- `setup` / `teardown` -- per-test isolation (temp dirs, env vars)

Always create temp dirs in `setup`, never reuse across tests.

### Multi-line Output

```bash
@test "parse multi-line" {
    run my_command
    [ "${lines[0]}" = "header" ]
    [ "${lines[2]}" = "data row" ]
}
```

`$output` is the full string; `${lines[@]}` is the array. Use `lines` for structured output validation.

### Fixture Strategy

- Copy fixtures to temp dir before mutating -- never modify originals
- Use `$BATS_TEST_DIRNAME` to locate fixture dir relative to test file
- For generated fixtures, create helper functions, not inline heredocs

## ShellCheck Opinions

### Recommended .shellcheckrc

```
shell=bash
enable=avoid-nullary-conditions,require-variable-braces
disable=SC1091
external-sources=true
```

- **SC1091** (not following sourced files): almost always a false positive in projects with dynamic sourcing -- disable globally
- **SC2086** (unquoted variables): never disable globally; fix each instance or suppress inline with comment explaining why
- **SC2015** (`&& ||` chains): suppress only in one-liners where intent is obvious

### Suppression Rules

- Always add a comment explaining *why* when using `# shellcheck disable=SCXXXX`
- Suppress at the narrowest scope (line > function > file)
- Never disable SC2086 project-wide -- it catches real bugs

### Target Shell Mismatch

Most common source of false positives. If your scripts use bash features, ensure:
- Shebang is `#!/usr/bin/env bash` (not `#!/bin/sh`)
- `.shellcheckrc` has `shell=bash`
- CI runs with `--shell=bash` flag

## CI Integration

### Preferred Setup

```yaml
# GitHub Actions -- run both together
- name: Shell quality
  run: |
    shellcheck --format=gcc **/*.sh
    bats tests/*.bats --jobs 4
```

- Use `--format=gcc` in CI for parseable output
- Use `--jobs N` for parallel Bats execution
- Fail the build on any shellcheck warning (no `--severity` filtering)
- Run shellcheck *before* bats -- catch static issues before spending time on integration tests

### Pre-commit Hook

Lint only changed files:

```bash
git diff --cached --name-only --diff-filter=d | grep '\.sh$' | xargs -r shellcheck
```

## Non-Obvious Gotchas

- `run` captures both stdout and stderr in `$output` -- use `run --separate-stderr` (bats-core 1.5+) if you need to distinguish
- `[ "$status" -eq 0 ]` after `run` checks the *command's* exit code, not the test's
- ShellCheck `--check-sourced` follows `source`/`.` directives but requires files to exist at analysis time
- `bats --filter "pattern"` runs only matching test names -- use for focused debugging
- Parallel bats (`--jobs`) shares nothing between files but `setup_file` resources persist within a file
