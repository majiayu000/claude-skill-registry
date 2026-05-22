---
name: tests-kit
description: "Test case management for Synnovator platform. Two modes: (1) Guard mode — before any synnovator skill or implementation change, verify existing test cases in specs/testcases/ are not broken. Use when modifying synnovator skill code, endpoint scripts, engine logic, or data model specs. (2) Insert mode — add new test cases to specs/testcases/. Use when user requests adding business scenarios, new feature test coverage, or regression tests. Triggers: 'run tests', 'check testcases', 'add test case', 'verify tests', 'test coverage', or any synnovator implementation change."
---

# Tests Kit

Test case guardian and insertion tool for the Synnovator platform's business scenarios defined in `specs/testcases/`.

## Mode 1: Guard — Verify Existing Test Cases

Run this workflow **before committing any change** to synnovator skill scripts, data model docs, or spec files.

### Guard Workflow

1. **Run validation script** to check structural integrity:
   ```bash
   uv run python .claude/skills/tests-kit/scripts/check_testcases.py
   ```
   This checks: TC ID format, uniqueness across files, file structure, and format conventions.

2. **Identify affected test cases** based on the change:
   - Read [references/testcase-index.md](references/testcase-index.md) to find TC IDs related to the changed module
   - Map changes to affected TC prefixes:
     - `content.py` / endpoint scripts → `TC-USER`, `TC-CAT`, `TC-RULE`, `TC-GRP`, `TC-POST`, `TC-RES`, `TC-IACT`
     - `relations.py` → `TC-REL-*`
     - `cascade.py` → `TC-DEL-*`
     - `cache.py` → `TC-IACT-003`, `TC-IACT-013`, `TC-IACT-021` (counter tests)
     - `rules.py` → `TC-RULE-100+`, `TC-ENGINE-*`, `TC-ENTRY-*`, `TC-CLOSE-*`
     - `docs/data-types.md` → All content type TCs
     - `docs/relationships.md` → `TC-REL-*`, `TC-FRIEND-*`, `TC-STAGE-*`, `TC-TRACK-*`, `TC-PREREQ-*`
     - `docs/crud-operations.md` → `TC-PERM-*`, all CRUD TCs
     - `docs/rule-engine.md` → `TC-ENGINE-*`, `TC-ENTRY-*`, `TC-CLOSE-*`

3. **Read the affected test case files** in `specs/testcases/` and verify each scenario still holds given the proposed change.

4. **Report conflicts** — If any test case would be broken:
   - List each broken TC ID with explanation
   - Propose how to resolve (fix implementation to preserve TC, or update TC with user approval)

## Mode 2: Insert — Add New Test Cases

Run this workflow when the user wants to add new test scenarios.

### Insert Workflow

1. **Understand the scenario** the user wants to test. Ask for:
   - What business behavior should be covered?
   - Which content types / relations / rules are involved?

2. **Check existing coverage** — Read [references/testcase-index.md](references/testcase-index.md) and search for overlapping or similar TCs. If the scenario is already covered, inform the user.

3. **Try to fit within existing specs** — Before proposing any spec changes:
   - Read relevant files in `docs/` and `specs/` to understand current data model and constraints
   - Attempt to express the test using **existing** content types, relations, and rule engine features
   - Consider: Can the test be decomposed into multiple steps using existing primitives?
   - Consider: Can an existing data type (e.g., `interaction`, `post:post` relation) serve as an indirect wrapper?
   - If the scenario can be expressed without spec changes, proceed to step 5

4. **If spec changes are needed** — Present to the user:
   - Which spec file(s) need modification
   - What the minimum change would be
   - Impact analysis: which existing TCs might be affected
   - Wait for user approval before proceeding

5. **Determine placement** — Read [references/testcase-format.md](references/testcase-format.md) for conventions:
   - Identify the correct file (by module) or decide if a new file is needed
   - Pick the next available TC ID number within the appropriate range
   - Place positive cases in 001-099 (or 100-199 for feature-specific), negative in 900-999

6. **Write the test case** following format conventions:
   - Chinese language
   - `**TC-PREFIX-NNN：Title**` format
   - Scenario + expected result only, no test method
   - Single paragraph unless multi-effect cascade

7. **Run validation** after insertion:
   ```bash
   uv run python .claude/skills/tests-kit/scripts/check_testcases.py
   ```

## Resources

### scripts/

- `check_testcases.py` — Validate all test case files for format consistency, TC ID uniqueness, and structural correctness. Run with `uv run python .claude/skills/tests-kit/scripts/check_testcases.py`.

### references/

- [testcase-index.md](references/testcase-index.md) — Complete catalog of all 267 test cases with TC IDs, descriptions, and file locations. Read this to find related test cases or check coverage.
- [testcase-format.md](references/testcase-format.md) — File naming, TC ID conventions, number ranges, writing rules, and structural template. Read this before writing new test cases.
