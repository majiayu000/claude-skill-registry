---
name: preflight
description: "Run all preflight checks (format, gn_check, presubmit, build, tests) to make sure the current work is ready for review."
---

# Preflight Checks

Run all preflight checks to make sure the current work is ready for review. Execute each step sequentially and stop immediately if any step fails.

## Arguments

- **`all`** — Run all test suites (brave_browser_tests, brave_unit_tests, brave_component_unittests) without filters, instead of only running tests affected by the change. Usage: `/preflight all`

## Current State

- Branch: !`git branch --show-current`
- Status: !`git status --short`

## Steps

### 0. Check branch
If on `master`, create a new branch off of master before proceeding (use a descriptive branch name based on the changes).

### 1. Check against best practices (per-category subagents)

Check the branch's changes against best practices using parallel subagents — one per best-practice category. This ensures every rule is systematically checked heading-by-heading rather than relying on a single pass to hold 150+ rules in mind.

#### Step 1a: Get diff and classify changed files

```bash
MERGE_BASE=$(git merge-base HEAD master)
git diff --name-only $MERGE_BASE..HEAD
```

Classify the changed files:
- **has_cpp_files**: `.cc`, `.h`, `.mm` files
- **has_test_files**: `*_test.cc`, `*_browsertest.cc`, `*_unittest.cc`, `*.test.ts`, `*.test.tsx`
- **has_chromium_src**: `chromium_src/` paths
- **has_build_files**: `BUILD.gn`, `DEPS`, `*.gni`
- **has_frontend_files**: `.ts`, `.tsx`, `.js`, `.jsx`

#### Step 1b: Launch category subagents in parallel

Launch one **Task subagent** (subagent_type: "general-purpose") per applicable category. **Use multiple Task tool calls in a single message** so they run in parallel.

| Category | Doc(s) to read | Condition |
|----------|---------------|-----------|
| **coding-standards** | `coding-standards.md` | has_cpp_files |
| **architecture** | `architecture.md`, `documentation.md` | Always |
| **build-system** | `build-system.md` | has_build_files |
| **testing** | `testing-async.md`, `testing-javascript.md`, `testing-navigation.md`, `testing-isolation.md` | has_test_files |
| **chromium-src** | `chromium-src-overrides.md` | has_chromium_src |
| **frontend** | `frontend.md` | has_frontend_files |

All doc paths are under `./brave-core-bot/docs/best-practices/`.

**Always launch at minimum:** architecture (applies to all changes — layering, dependency injection, factory patterns affect every change).

#### Step 1c: Subagent prompt

Each subagent prompt MUST include:

1. **The branch name and repo path** so it can get the diff
2. **Which best practice doc(s) to read** — only the ones for this category (paths above)
3. **Instructions to get the local diff** via `git diff $(git merge-base HEAD master)..HEAD`
4. **The review rules**:
   - Only flag violations in ADDED lines (+ lines), not existing code
   - Also flag bugs introduced by the change (e.g., missing string separators, duplicate DEPS entries, code inside wrong `#if` guard)
   - Read changed files in full for context — don't just rely on the diff
   - Do NOT flag: existing code not being changed, template functions defined in headers, simple inline getters in headers, style preferences not in the documented best practices
5. **The systematic audit requirement** (below)
6. **Required output format** (below)

#### Step 1d: Systematic audit requirement

**CRITICAL — this is what prevents the subagent from stopping after finding a few violations.**

The subagent MUST work through its best practice doc(s) **heading by heading**, checking every `##` rule against the diff. It must output an audit trail listing EVERY `##` heading with a verdict:

```
AUDIT:
PASS: ✅ Always Include What You Use (IWYU)
PASS: ✅ Use Positive Form for Booleans and Methods
N/A: ✅ Consistent Naming Across Layers
FAIL: ❌ Don't Use rapidjson
PASS: ✅ Use CHECK for Impossible Conditions
... (one entry per ## heading in the doc)
```

Verdicts:
- **PASS**: Checked the diff — no violation found
- **N/A**: Rule doesn't apply to the types of changes in this diff
- **FAIL**: Violation found — must have a corresponding entry in VIOLATIONS

#### Step 1e: Required output format

Each subagent MUST return this structured format:

```
CATEGORY: <category name>

AUDIT:
PASS: <rule heading>
N/A: <rule heading>
FAIL: <rule heading>
... (one line per ## heading in the doc(s))

VIOLATIONS:
- file: <path>, line: <line_number>, rule: "<rule heading>", issue: <brief description>, fix: <what should be done instead>
- ...
NO_VIOLATIONS (if none found)
```

#### Step 1f: Aggregate results and fix

After ALL category subagents return:

1. **Aggregate violations** from all category subagents into a single list
2. If violations were found, **fix each violation** before proceeding to step 2
3. If no violations across all categories, note that and proceed

### 2. Format code
Run `npm run format`. If formatting changes any files, stage and include them in the commit later.

### 3. GN check
Run `npm run gn_check`. Fix any issues found and re-run until it passes.

**Skip this step** if the only changes are to test filter files (`test/filters/*.filter`) — filter files don't affect GN build configuration.

### 4. Presubmit
Run `npm run presubmit`. Fix any issues found and re-run until it passes.

### 5. Commit if needed
Check `git status`. If there are any uncommitted changes (staged, unstaged, or untracked files relevant to the work), create a commit. The commit message should be short and succinct, describing what was done. If there are no changes, skip this step.

### 6. Build
Run `npm run build` to make sure the code builds. If it fails, fix the build errors, amend the commit, and retry.

### 7. Run tests

**If the `all` argument was provided:** Run all test suites without filters:

- `npm run test -- brave_browser_tests`
- `npm run test -- brave_unit_tests`
- `npm run test -- brave_component_unittests`

**Otherwise (default):** Determine which test targets are affected by the changes in this branch (compare against `master`). Look at the changed files and identify the corresponding test targets and relevant test filters.

- **Browser tests:** `npm run test -- brave_browser_tests --filter=<TestName>`
- **Unit tests:** `npm run test -- brave_unit_tests --filter=<TestName>`
- **Component unit tests:** `npm run test -- brave_component_unittests --filter=<TestName>`

If no tests are affected, note that and move on.

### 8. Re-check best practices if substantial changes were made
If steps 2–7 required fixes that introduced substantial code changes (not just formatting), re-run the per-category subagent best practices check from step 1 against the new changes. Skip this if the only changes were whitespace/formatting.

### 9. Re-run checks if fixes were needed
If any step required fixes (best practices violations, build errors, test failures, format/lint issues), amend the commit with the fixes and re-run all checks from step 1 until everything passes cleanly.

## Important
- Stop and report if any step fails after exhausting reasonable fix attempts.
- Report a summary of results when all steps complete successfully.
