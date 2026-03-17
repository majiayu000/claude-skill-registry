---
name: maestro-run-test
description: Run Maestro E2E tests from a file or directory path and capture output to a results directory. Use when the user wants to run a Maestro test, execute a test flow, run E2E tests with output, or mentions "maestro test" with a path.
---

# Run Maestro Test

Run a Maestro test flow (or directory of flows) and capture structured output.

## Instructions

### 1. Resolve the test path

The user provides a path to a `.yml` flow file or a directory of flows. If the path is relative, resolve it from the workspace root.

Verify the path exists before running:

```bash
ls <resolved-path>
```

### 2. Clean previous results

```bash
rm -rf build/maestro-results
```

### 3. Run the test

```bash
maestro test --test-output-dir=build/maestro-results <resolved-path>
```

If the user specifies extra flags (e.g. `--include-tags`, `--exclude-tags`, `--device`), append them.

### 4. Report results

After the command finishes:

1. Read the exit code — `0` means all tests passed, non-zero means failures.
2. List the results directory to find output files:

```bash
ls -la build/maestro-results/
```

3. Read the XML report if present (`build/maestro-results/*.xml`) for a structured summary of pass/fail counts.
4. If there are screenshots in the output dir, mention them to the user.
5. Summarize: total tests, passed, failed, and which tests failed (with the failure reason if available).

### 5. On failure

If tests fail:

- Show the failing test name and the error message from the output.
- If a screenshot was captured at the failure point, reference it.
- Suggest next steps: re-run with `--debug-output` or use the `fix-maestro-test` skill to debug interactively.

## Examples

**Run a single test:**
```
User: run the login test at maestro/flows/auth/LoginWithGustoWelcome.yml
```
```bash
rm -rf build/maestro-results
maestro test --test-output-dir=build/maestro-results maestro/flows/auth/LoginWithGustoWelcome.yml
```

**Run all tests in a directory:**
```
User: run all the auth tests
```
```bash
rm -rf build/maestro-results
maestro test --test-output-dir=build/maestro-results maestro/flows/auth/
```

**Run with tags:**
```
User: run smoke tests from maestro/flows
```
```bash
rm -rf build/maestro-results
maestro test --test-output-dir=build/maestro-results --include-tags=smoke maestro/flows/
```
