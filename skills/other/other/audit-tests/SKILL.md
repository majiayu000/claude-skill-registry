---
name: audit-tests
description: Audit the test suite for useless tests, consolidation opportunities, over-mocking, weak assertions, placement/organization issues, xdist safety violations, and other test quality issues. Use when user says "audit tests", "audit test suite", "review tests", or "test quality check". Generates an improvement plan in temp/ with explanations for each proposed change.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: audit-tests] Auditing test suite...'"
          once: true
---

# Test Suite Audit Skill

Audit the test suite to identify useless tests, consolidation opportunities, quality issues, and tests that don't validate what they claim. Produces an actionable improvement plan with explanations.

## When to Use

- User says "audit tests", "audit test suite", "review tests"
- User wants "test quality check" or "test cleanup"
- User asks to "find useless tests" or "consolidate tests"

## Intended Test Directory Structure

The test suite mirrors the source sub-package hierarchy rather than using a type-based unit/integration split — the project's L0–L3 layer boundaries already encode isolation levels. Each sub-package gets its own test directory. Cross-cutting concerns go in dedicated directories:

```
tests/
├── conftest.py          # Shared: MockSubprocessRunner, tool_ctx fixture (wired via make_context)
├── CLAUDE.md            # xdist safety guidelines
├── core/                # L0: tests for autoskillit/core/ (io, logging, paths, types, protocols)
├── config/              # L1: tests for autoskillit/config/
├── pipeline/            # L1: tests for autoskillit/pipeline/ (audit, gate, context, tokens)
├── execution/           # L1: tests for autoskillit/execution/ (db, github, headless, process, quota, session, testing)
├── workspace/           # L1: tests for autoskillit/workspace/ (cleanup, clone, skills)
├── recipe/              # L2: tests for autoskillit/recipe/ (io, loader, schema, validator, rules, smoke)
├── migration/           # L2: tests for autoskillit/migration/ (engine, loader, store)
├── server/              # L3: tests for autoskillit/server/ (_factory, git, helpers, tools_*)
├── cli/                 # L3: tests for autoskillit/cli/
├── arch/                # Cross-cutting: AST architecture enforcement, import contracts, layer rules
├── contracts/           # Cross-cutting: instruction surface, MCP/API surface, version consistency
└── infra/               # Cross-cutting: CI/dev config checks (.pre-commit, .gitleaks, .github/)
```

**File naming convention:** Within each sub-directory, the file name should match the source module being tested. Examples:
- `tests/execution/test_db.py` — tests `execution/db.py` (not `test_db_tools.py`)
- `tests/execution/test_testing.py` — tests `execution/testing.py` (not `test_test_runner.py`)
- `tests/execution/test_process.py` — tests `execution/process.py` (not `test_process_lifecycle.py`)
- `tests/execution/test_session.py` — tests `execution/session.py` (not `test_session_result.py`)
- `tests/recipe/test_io.py` — tests `recipe/io.py` (not `test_recipe_io.py`)
- `tests/core/test_io.py` — tests `core/io.py` (not `test_yaml_extended.py`)

Tests that span two modules should be placed in the directory of their primary concern, or split into two files when test counts are substantial enough to warrant it.

## Critical Constraints

**NEVER:**
- Modify any source or test code files
- Flag tests as useless without reading and understanding them
- Recommend removing tests that guard against real regressions
- Recommend changes that would reduce meaningful coverage

**ALWAYS:**
- Use subagents for parallel exploration
- Read both the test AND the code it tests before judging
- Provide file paths, line numbers, and an explanation for each finding
- Write the improvement plan to `temp/audit-tests/test_audit_{YYYY-MM-DD_HHMMSS}.md`
- Categorize findings by issue type and severity

---

## Issue Categories

### Category 1: Useless Tests (HIGH)

Tests that provide no meaningful coverage. They pass regardless of whether the code works correctly.

**What to look for:**
- Tests that assert always-true conditions (e.g., `assert result is not None` when the function never returns None)
- Tests that verify tautologies (e.g., confirming an enum member is a valid enum member)
- Tests whose assertions would pass even if the code under test were completely broken
- Tests with no assertions at all (just call a function and check it doesn't crash)
- Tests in "testing mode" that bypass the logic they claim to test

### Category 2: Redundant / Consolidatable Tests (MEDIUM)

Tests that duplicate each other or could be combined without losing coverage.

**What to look for:**
- Multiple tests asserting the exact same behavior with trivially different inputs (candidates for parameterization)
- Identical fixtures or setup code defined in multiple places
- Tests in different files that exercise the same code path
- Contract tests that duplicate what unit tests already cover
- Integration tests that only exercise unit-level logic (no actual integration)

### Category 3: Over-Mocked Tests (HIGH)

Tests that mock so aggressively they no longer test real behavior. The test validates the mock wiring, not the production code.

**What to look for:**
- Tests that mock the system under test (mocking the handler inside a handler test)
- Auto-mocked database/IO layers where the test then only verifies mock call counts
- Tests that patch internal module functions instead of external boundaries
- Dependency injection tests that only verify args are passed through
- Tests where removing the production code entirely would still pass

### Category 4: Weak Assertions (HIGH)

Tests that have assertions too loose to catch real bugs.

**What to look for:**
- Inequality assertions where exact values are known (e.g., `assert count >= 2` when it should be `== 3`)
- Substring checks where full string comparison is appropriate
- `assert result` (truthy check) when specific value/type should be verified
- Mock call verification without checking call arguments
- Tests that check collection length but not contents

### Category 5: Misleading Tests (MEDIUM)

Tests whose name, docstring, or structure misrepresents what they actually verify.

**What to look for:**
- Test name says "error handling" but doesn't verify the error path
- Docstring describes behavior the test doesn't actually assert
- Test claims to verify integration but mocks all dependencies
- Exception tests that don't verify the exception was actually raised or caught
- Tests named for edge cases that actually test the happy path
- Architecture/AST enforcement tests that claim to check a constraint but the check is trivially defeatable (e.g., a regex that matches any file content)

### Category 6: Stale / Outdated Tests (MEDIUM)

Tests that no longer align with the current codebase.

**What to look for:**
- Tests for deprecated or removed functionality
- Tests that reference old file paths, class names, or module structure
- Fixtures marked as deprecated that are still defined
- Tests that are always skipped or conditionally disabled
- Tests whose setup creates state the production code no longer uses
- `CLAUDE.md` test file list that diverges from the actual files on disk — flag if the documented inventory is incomplete or contains stale entries

### Category 7: Fixture Issues (LOW)

Problems in test fixtures that make tests harder to understand and maintain.

**What to look for:**
- Same fixture defined in multiple places with slight variations
- Deeply nested fixture chains where the dependency graph is unclear
- `autouse=True` fixtures where a significant portion of tests in scope don't need them. Assess the usage ratio: if more than ~30% of tests don't need the fixture, it should be explicit instead of autouse. The more expensive the fixture, the lower the tolerance for unnecessary execution.
- Overly complex fixtures (50+ lines of mock configuration)
- Dead fixtures that no test references
- Tests that create temporary files/directories directly instead of using test framework fixtures (e.g., pytest's `tmp_path`)
- Tests that manually set up resources the framework provides as fixtures

### Category 8: Placement / Organization Issues (MEDIUM)

Tests placed in the wrong directory relative to the intended sub-package hierarchy, or test files named inconsistently with the source module they test.

**What to look for:**
- Any test file living at the `tests/` root other than `conftest.py` and `CLAUDE.md` — all test files should be inside sub-directories
- Tests for L0 (`core/`) modules not in `tests/core/`
- Tests for L1 modules (`config`, `pipeline`, `execution`, `workspace`) not in their corresponding `tests/<subpackage>/` directory
- Tests for L2 modules (`recipe`, `migration`) not in their corresponding `tests/<subpackage>/` directory
- Tests for L3 modules (`server`, `cli`) not in their corresponding `tests/<subpackage>/` directory
- AST-based architecture enforcement tests (import contracts, layer rules, structural checks) outside `tests/arch/`
- Instruction surface / MCP contract / SKILL.md contract tests outside `tests/contracts/`
- CI/dev infrastructure tests checking `.pre-commit-config.yaml`, `.gitleaks.toml`, or `.github/workflows/` files outside `tests/infra/`
- Test file names carrying redundant sub-package prefixes (e.g., `test_recipe_io.py` inside `tests/recipe/` should be `test_io.py`)
- Test file names that don't reflect the source module: `test_db_tools.py` → `test_db.py`, `test_test_runner.py` → `test_testing.py`, `test_yaml_extended.py` → `test_io.py`, `test_process_lifecycle.py` → `test_process.py`, `test_session_result.py` → `test_session.py`, `test_headless_runner.py` → `test_headless.py`, `test_skill_resolver.py` → `test_skills.py`, `test_git_operations.py` → `test_git.py`
- Test files that cover modules from two different layers without a clear rationale (candidates for splitting)

### Category 9: Oversized Files (MEDIUM)

Test files or supporting files exceeding 750 lines. Flag files approaching the threshold (800+) as warnings.

### Category 10: xdist Safety Violations (HIGH)

Tests that are unsafe for parallel execution under pytest-xdist (`-n 4 --dist worksteal`). This project runs tests in parallel by default with explicit safety rules defined in `tests/CLAUDE.md`.

**What to look for:**
- Tests that create temporary files or directories at fixed paths instead of using `tmp_path` (pytest provides unique per-test paths; on Linux these should land under `/dev/shm/pytest-tmp` per `tests/CLAUDE.md` guidance)
- `scope="module"` or `scope="session"` fixtures that mutate state (module-level dicts, cached objects, singletons) without full teardown via `yield` — these can leak state across workers
- Tests that use `monkeypatch.setattr()` on a fixture but the fixture itself has `scope != "function"` — the patch won't be reverted between tests that share the fixture instance
- Tests that bind to fixed network ports; use `port=0` and capture the OS-assigned port via fixture
- Module-level singletons mutated directly (e.g., appending to a module-level list, patching a module-level `_ctx`) without `monkeypatch` — parallel workers each import independently but share no memory, so this is only a problem for same-worker ordering, not cross-worker; still flag for ordering-dependency risk
- Tests that write to or read from paths shared with other tests (e.g., a hardcoded `temp/` subpath without a unique suffix)
- Tests that rely on execution order (pass in isolation, fail when another test runs first) — detect by checking for setup that assumes prior state

---

## Audit Workflow

### Step 1: Launch Parallel Subagents

Spawn 6 domain-based subagents. Each covers all issue categories (C1–C10) within its area. Group by source domain, not by issue category. Each subagent must read both test files AND the corresponding production code before making judgements.

- **Group 1 — Core + Config (L0 + L1):** Tests for `core/` and `config/` sub-packages. Also check `conftest.py` for fixture quality.
- **Group 2 — Pipeline + Workspace (L1):** Tests for `pipeline/` and `workspace/` sub-packages.
- **Group 3 — Execution (L1):** Tests for `execution/` sub-package.
- **Group 4 — Recipe + Migration (L2):** Tests for `recipe/` and `migration/` sub-packages.
- **Group 5 — Server + CLI (L3):** Tests for `server/` and `cli/` sub-packages.
- **Group 6 — Cross-cutting:** Architecture enforcement tests, instruction surface/contract tests, CI/dev infrastructure tests. Also audit `tests/CLAUDE.md` for accuracy against the actual test files on disk.

For each finding, note the file, line range, issue category, and a brief explanation of why it's a problem and what should change.

### Step 2: Consolidate and Deduplicate

After subagents complete:
1. Merge findings across subagents
2. Deduplicate (same test flagged from different angles)
3. Cross-reference fixture issues across test configuration files
4. Identify patterns that repeat across the codebase (systemic issues vs. one-offs)
5. Compile a **Placement Map** from all Category 8 findings: a table mapping every misplaced file to its intended target location in the new directory structure

### Step 3: Generate Improvement Plan

Write a structured plan to: `temp/audit-tests/test_audit_{YYYY-MM-DD_HHMMSS}.md`

Organize the plan into phases grouped by issue type. Each finding must include:
- **File path and line range**
- **Issue category and severity**
- **Explanation**: What the test does, why it's a problem, and what the concrete improvement is
- **Action**: Remove, consolidate, strengthen assertion, reduce mocking, relocate, etc.

For Category 8 findings, include a **Placement Map** section at the top of the plan — a table with columns: `Current File` | `Target Directory` | `Target Filename` | `Rename?` | `Split?`. This map is the primary deliverable for guiding the reorganization effort.

Include a summary table at the top with counts by category.

### Step 4: Terminal Summary

Output a summary including:
- Plan file location
- Total findings by category and severity
- Top systemic issues (patterns that appear across many files)
- Estimated test count reduction from consolidation
- Placement map summary: N files to relocate, N files to rename, target directory breakdown
- Next steps

---

## Exclusions

Do NOT flag:
- Tests that guard against known regressions (even if they look simple)
- Property-based tests (different testing philosophy)
- Test utilities and helper functions in test support directories
- Test infrastructure and safety mechanisms
- Tests that are intentionally minimal as smoke tests
- Shared fixtures in centralized test configuration
- Architecture enforcement tests (`test_architecture.py`, `test_import_paths.py`) for having "weak assertions" or "no meaningful coverage" — AST rule enforcement tests validate source code structure, not runtime behavior, and are correctly evaluated against whether the structural rule they enforce is correct and complete, not by normal assertion-strength standards
