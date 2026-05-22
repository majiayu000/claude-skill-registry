---
name: curate-tests
description: "Phase 2: Generate and discover tests, validate against real library. Only invoke when explicitly requested by the user or by the yoink orchestrator."
argument-hint: "PROMPT [--package PACKAGE_NAME] [--skip-test-discoverer]"
---

# Curate Tests

> **Do not invoke this skill unless explicitly requested.** It is called by `/yoink:yoink` or run standalone by the user.

**Prerequisite:** `/yoink:setup` must have been run first (reference dir and real library must exist).

Parse your prompt to identify:
- **Package name**: from the `Package:` line or `--package` argument
- **Target function/feature**: from the `Task:` line or prompt body

> **Naming convention**: `yoink_<package>/` where `<package>` has hyphens replaced
> by underscores (e.g., package `litellm` -> `yoink_litellm/`).

---

### 1. Discover relevant tests

- If **`--skip-test-discoverer` is present** then **skip to step 2**.

Use the **yoink:test-discoverer** agent to search for relevant tests from the original library's test suite.

Pass input as JSON:

```json
{
  "package_name": "<PACKAGE>",
  "target_function": "<TARGET_FUNCTION>"
}
```

> **Discovered tests are reference material only.** They exist so the test-generator
> can study real-world patterns and assertions. They are **never executed** during
> validation or any later step -- only generated tests are run.

### 2. Generate focused tests

Use the **yoink:test-generator** agent to write original pytest tests for the target function.

Pass input as JSON:

```json
{
  "package_name": "<PACKAGE>",
  "target_function": "<TARGET_FUNCTION>"
}
```

### 3. Validate generated tests against the real library

Run **only the generated tests** using the script below against the installed real library.
Do NOT run discovered tests -- they are reference only and may depend on API keys, network
access, or fixtures that are not available.

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/run_tests.py --project-dir . 2>&1
```

- If **all tests pass** then **proceed to the next step**.
- If **any tests fail or error** then **investigate and fix the generated tests**. Do NOT proceed to the next step until all generated tests pass against the real library.

### 4. Rewrite imports

After validation passes, rewrite imports in generated tests so they target `yoink_<package>/`:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/rewrite_imports.py --package <PACKAGE> --target-dir yoink_<PACKAGE>/tests/generated
```

### 5. Sanity check

Run the test suite against the empty `yoink_<package>/` to confirm tests fail:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/run_tests.py --project-dir . --summary-only
```

Score should be ~0.0 (tests should fail against empty `yoink_<package>/`).

- If **score > 0** then **something is wrong, investigate before proceeding**.
