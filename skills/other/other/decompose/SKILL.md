---
name: decompose
description: "Phase 3: Dependency decomposition. Only invoke when explicitly requested by the user or by the yoink orchestrator."
argument-hint: "[--package PACKAGE_NAME]"
---

# Decompose

> **Do not invoke this skill unless explicitly requested.** It is called by `/yoink:yoink` or run standalone by the user.

**Prerequisite:** `/yoink:curate-tests` must have been completed first.

Seed the decomposition queue with the target package:

```bash
uv run python ${CLAUDE_SKILL_DIR}/scripts/decomp.py enqueue <PACKAGE_NAME>
```

Then run the decomposition loop below until the queue is empty.

---

## Decomposition Loop

**Begin loop.** Repeat until the queue is empty.

### 1. Dequeue

```bash
uv run python ${CLAUDE_SKILL_DIR}/scripts/decomp.py dequeue
```

- If **queue is empty** then **decomposition complete, remove the real library and stop**.
  ```bash
  uv remove <PACKAGE_NAME>
  ```

### 2. Evaluate

Use the **yoink:decomp-evaluator** agent to evaluate whether the dequeued library should be kept or decomposed.

Pass input as JSON:

```json
{
  "library_name": "<DEQUEUED_LIBRARY>",
  "package_name": "yoink_<PACKAGE_NAME>"
}
```

- If **Keep** then **go back to step 1**.
- If **Decompose** then **continue to step 3** with the evaluation output.

### 3. Prepare the sub-package for the implementer agent

Complete these steps IN ORDER before entering the loop.

> **Exception:** When the dequeued item is `{original_package}` (the first item in the queue), skip steps 3a–3c and go straight to 3d. Baseline verification (3a) was already completed by `/yoink:curate-tests`, scaffolding (3c) was already done by `/yoink:setup`, and import rewriting (3b) is a no-op for the original package since there are no sub-package imports to rewrite yet.

#### a. Verify baseline

Run the top-level generated tests:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/run_tests.py --project-dir . 2>&1
```

- If **all tests pass** then **proceed to step b**.
- If **any test fails** then **the baseline is broken and must be fixed before proceeding**. Investigate the test failures, fix the issues, and re-run the tests until they all pass.

#### b. Rewrite imports

Swap `{sub_package}` imports in `yoink_{top_package}/` source code to point at `yoink_{sub_package}`:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/rewrite_imports.py --package {sub_package} --target-dir yoink_{top_package}
```

#### c. Scaffold the sub-package

```bash
mkdir -p yoink_{sub_package}
touch yoink_{sub_package}/__init__.py
```

#### d. Seed & populate state body

Seed the state file with placeholder values:

```bash
"${CLAUDE_SKILL_DIR}/scripts/activate-inner-yoink-loop.sh" --max-iterations 10
```

#### e. Populate loop state

Read `.claude/decomp_context.md` and fill in the `PLACEHOLDER` values in the JSON block inside `.claude/inner-yoink-loop.local.md`:

| Field | Where to get the value |
|---|---|
| top_package | `{top_package}` |
| sub_package | `{sub_package}` |
| category | from `decomp_context.md` |
| strategy | from `decomp_context.md` |
| functions_to_replace | JSON array of strings from `decomp_context.md` |
| reference_material | from `decomp_context.md`, default: `.yoink/reference/{sub_package}/` |
| acceptable_sub_dependencies | JSON array of strings from `decomp_context.md` |

### 4. Implement & Validate

Use the **yoink:decomp-implementer** agent to implement the sub-package.

- If **completion_promise = `DONE`** then **proceed to step 5**.
- If **completion_promise = `MAX_ITERATIONS_REACHED`** then **stop the loop and report back to the user that the maximum number of iterations has been reached**.
- If **the agent exits without returning `DONE`** then **spin up a new yoink:decomp-implementer agent to continue the task.**

### 5. Enqueue new dependencies

Using **new_imports** from the implementer's output, enqueue external libraries that `yoink_<PACKAGE>/` now depends on:

```bash
uv run python ${CLAUDE_SKILL_DIR}/scripts/decomp.py enqueue <lib1> <lib2> ...
```

Only enqueue what `yoink_<PACKAGE>/` actually imports, not the full dependency tree of the original library. Use `uv run python ${CLAUDE_SKILL_DIR}/scripts/decomp.py deps <library>` to see pip dependencies as reference.

**Loop back to step 1.**
