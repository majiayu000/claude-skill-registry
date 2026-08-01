---
name: uloop-run-tests
description: 'Execute Unity Test Runner via uloop CLI. Use when you need to: (1) Run
  unit tests (EditMode tests), (2) Run integration tests (PlayMode tests), (3) Verify
  code changes don''t break existing functionali'
---

---
name: uloop-run-tests
description: Execute Unity Test Runner via uloop CLI. Use when you need to: (1) Run unit tests (EditMode tests), (2) Run integration tests (PlayMode tests), (3) Verify code changes don't break existing functionality.
---

# uloop run-tests

Execute Unity Test Runner.

## Usage

```bash
uloop run-tests [options]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--test-mode` | string | `EditMode` | Test mode: `EditMode`, `PlayMode` |
| `--filter-type` | string | `all` | Filter type: `all`, `exact`, `regex`, `assembly` |
| `--filter-value` | string | - | Filter value (test name, pattern, or assembly) |
| `--save-xml` | boolean | `false` | Save test results as XML |

## Examples

```bash
# Run all EditMode tests
uloop run-tests

# Run PlayMode tests
uloop run-tests --test-mode PlayMode

# Run specific test
uloop run-tests --filter-type exact --filter-value "MyTest.TestMethod"

# Run tests matching pattern
uloop run-tests --filter-type regex --filter-value ".*Integration.*"
```

## Output

Returns JSON with test results including pass/fail counts and details.
