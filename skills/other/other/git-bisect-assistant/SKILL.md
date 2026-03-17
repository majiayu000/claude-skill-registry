---
name: git-bisect-assistant
description: Automatically performs git bisect to identify the first bad commit that introduced a bug or failure. Use when debugging regressions, tracking down when a test started failing, or identifying which commit broke functionality. Handles flaky tests with retry logic and provides comprehensive reports with bisect logs and confidence levels.
---

# Git Bisect Assistant

Automates the git bisect process to efficiently identify the first bad commit responsible for a bug or test failure.

## Quick Start

Basic usage pattern:

```bash
python scripts/git_bisect_runner.py \
  --good <known-good-commit> \
  --bad <known-bad-commit> \
  --test "<test-command>"
```

Example:

```bash
python scripts/git_bisect_runner.py \
  --good v1.0.0 \
  --bad HEAD \
  --test "pytest tests/test_feature.py::test_specific_case"
```

## Workflow

1. **Gather Information**
   - Identify the known good revision (commit, tag, or branch)
   - Identify the known bad revision (defaults to HEAD)
   - Determine the test command that fails on bad commits and passes on good commits

2. **Run Bisect**
   - Execute the `git_bisect_runner.py` script with appropriate parameters
   - The script will automatically test commits and narrow down the culprit

3. **Review Results**
   - Examine the identified bad commit
   - Review the bisect log showing all tested commits
   - Check confidence level and assumptions

## Parameters

### Required

- `--good`: Known good revision (commit hash, tag, or branch name)
- `--test`: Shell command to test each commit. Exit code 0 = good, non-zero = bad

### Optional

- `--bad`: Known bad revision (default: `HEAD`)
- `--repo`: Repository path (default: current directory)
- `--retries`: Number of test runs per commit for flaky tests (default: 1)
- `--timeout`: Test execution timeout in seconds (default: no timeout)

## Handling Flaky Tests

For non-deterministic tests, use `--retries` to run the test multiple times per commit:

```bash
python scripts/git_bisect_runner.py \
  --good abc123 \
  --bad HEAD \
  --test "npm test" \
  --retries 3
```

The script uses majority voting: if a test passes 2 out of 3 times, the commit is marked as good.

## Test Command Guidelines

The test command should:
- Exit with code 0 for good commits (test passes)
- Exit with non-zero code for bad commits (test fails)
- Be deterministic or use `--retries` for flaky tests
- Complete within reasonable time or use `--timeout`

Examples:

```bash
# Python test
--test "pytest tests/test_auth.py -v"

# Shell script
--test "./scripts/verify_build.sh"

# Compilation check
--test "make && ./bin/app --version"

# Multiple commands
--test "npm install && npm test"
```

## Output Report

The script generates a comprehensive report including:

- **First Bad Commit**: Hash and commit message of the culprit
- **Confidence Level**: Assessment based on test stability and retry logic
- **Assumptions**: Any assumptions made during bisect (retries, timeouts)
- **Tested Commits**: Complete list of all commits tested with results
- **Bisect Log**: Detailed log of the bisect process

## Common Scenarios

### Scenario 1: Test Started Failing

User: "The integration tests started failing sometime in the last 20 commits"

```bash
python scripts/git_bisect_runner.py \
  --good HEAD~20 \
  --bad HEAD \
  --test "pytest tests/integration/"
```

### Scenario 2: Feature Broke After Release

User: "Feature X worked in v2.1.0 but is broken now"

```bash
python scripts/git_bisect_runner.py \
  --good v2.1.0 \
  --bad HEAD \
  --test "python -c 'import app; assert app.feature_x() == expected'"
```

### Scenario 3: Flaky Test Investigation

User: "A test fails intermittently, need to find when it started"

```bash
python scripts/git_bisect_runner.py \
  --good main \
  --bad feature-branch \
  --test "pytest tests/test_flaky.py" \
  --retries 5 \
  --timeout 30
```

## Tips

- **Ensure clean state**: Commit or stash changes before running bisect
- **Fast tests**: Use focused tests rather than full test suites for faster bisect
- **Build requirements**: Include build steps in test command if needed
- **Dependencies**: Ensure test command handles dependency installation if needed across commits
- **Timeout wisely**: Set timeout slightly longer than expected test duration
- **Retry count**: Use 3-5 retries for flaky tests to get reliable results

## Troubleshooting

**Bisect fails to start**: Verify good and bad revisions exist and are valid git references

**Test command fails unexpectedly**: Test the command manually on a known good/bad commit first

**Inconsistent results**: Increase `--retries` or check for environmental factors affecting tests

**Timeout too short**: Increase `--timeout` or optimize test command
