---
name: plugin-test
description: Run comprehensive tests on plugin components using the modular test runner. Validates hooks, agents, skills, and plugin structure across all PopKit plugin packages.
---

# Plugin Test Runner (Modular Architecture)

Execute PopKit's modular test suite to validate plugin integrity across all distributed plugin packages.

## When to Use

- User runs `/popkit:plugin test`
- Post-implementation validation
- Pre-release verification
- Debugging plugin issues
- CI/CD integration

## Arguments

| Flag          | Description                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| (category)    | Test category: `agents`, `hooks`, `skills`, `structure` (default: all plugins) |
| `--verbose`   | Show detailed test output including passing tests                              |
| `--fail-fast` | Stop on first test failure                                                     |

## Process

### Step 1: Parse Arguments

Determine which test runner to execute based on arguments:

- **No category**: Run `run_all_tests.py` (tests all 5 plugin packages)
- **Category specified**: Run `run_tests.py <category>` (tests popkit-core only)
- **--verbose**: Add `--verbose` flag to command
- **--fail-fast**: Add `--fail-fast` flag to command

### Step 2: Execute Test Runner

Use the Bash tool to run the appropriate Python test runner:

**Test all plugins (default):**

```bash
cd packages/popkit-core && python run_all_tests.py
```

**Test all plugins with verbose:**

```bash
cd packages/popkit-core && python run_all_tests.py --verbose
```

**Test specific category (single plugin):**

```bash
cd packages/popkit-core && python run_tests.py agents
cd packages/popkit-core && python run_tests.py hooks
cd packages/popkit-core && python run_tests.py skills
cd packages/popkit-core && python run_tests.py structure
```

### Step 3: Parse and Summarize Results

The test runner outputs structured results to stdout. Parse the output and provide a summary:

**Key metrics to report:**

- Total plugins tested
- Plugins passed/failed
- Total test cases executed
- Pass rate percentage
- Duration
- List of failures (if any)

**Example summary format:**

```
PopKit Plugin Tests Complete
============================

Plugins Tested: 5
- popkit-core: PASS (19/31 tests passed)
- popkit-dev: SKIP (no tests)
- popkit-ops: SKIP (no tests)
- popkit-research: SKIP (no tests)
- popkit-suite: SKIP (no tests)

Overall Results:
- Test Cases: 31
- Passed: 19 (61.3%)
- Failed: 12 (38.7%)
- Duration: 6.23s

Status: Tests completed with failures
```

### Step 4: Report Failures

If there are failures, show the first few with details:

```
Failures:
- popkit-core - Bash command completion tracking
  Reason: Exit code mismatch
- popkit-core - Write tool triggers quality gate
  Reason: Exit code mismatch
...
```

## Notes

- **Modular Architecture**: Tests run independently per plugin package
- **No Centralized Config**: Agents validated from markdown files, not config.json
- **Cross-Plugin Validation**: Checks for naming conflicts across all plugins
- **Hook Tests May Fail**: Some hook tests require runtime environments and may fail in isolation
- **Test Runners**: Uses `run_all_tests.py` (modular) or `run_tests.py` (single plugin)

## Dependencies

- `packages/shared-py/popkit_shared/utils/test_runner.py`
- `packages/shared-py/popkit_shared/utils/plugin_validator.py`
- `packages/shared-py/popkit_shared/utils/agent_validator.py`
- `packages/shared-py/popkit_shared/utils/skill_validator.py`
- `packages/shared-py/popkit_shared/utils/hook_validator.py`

## Related Commands

- `/popkit:plugin test` - Run all tests
- `/popkit:plugin test agents` - Test agent definitions
- `/popkit:plugin test --verbose` - Detailed output
