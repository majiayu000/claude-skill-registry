---
name: smart-test
version: 1.1.0
description: |
  Intelligent test selection based on code changes. Maps source files to tests via import analysis,
  implements tiered testing (fast < 1 min, impacted < 5 min, full suite), and tracks test reliability.
  Use when running tests after code changes to optimize feedback loops and CI time.
auto_activates:
  - "run affected tests"
  - "run impacted tests"
  - "smart test"
  - "intelligent testing"
  - "which tests to run"
  - "test selection"
  - "fast tests"
  - "quick tests"
  - "tests for changes"
  - "tests for this PR"
priority_score: 42.0
evaluation_criteria:
  frequency: HIGH
  impact: HIGH
  complexity: MEDIUM
  reusability: HIGH
  philosophy_alignment: HIGH
  uniqueness: MEDIUM
invokes:
  - type: skill
    name: test-gap-analyzer
  - type: skill
    name: outside-in-testing
  - type: skill
    name: pre-commit-diagnostic
  - type: subagent
    path: .claude/agents/amplihack/tester.md
dependencies:
  tools:
    - Read
    - Bash
    - Grep
    - Glob
  external:
    - "pytest"
    - "git"
  data_files:
    - ".claude/data/test-mapping/code_to_tests.yaml"
    - ".claude/data/test-mapping/reliability.yaml"
philosophy:
  - principle: Ruthless Simplicity
    application: Three-tier system (Fast/Impacted/Full) avoids over-engineering test strategies
  - principle: Zero-BS Implementation
    application: Real pytest commands ready to copy-paste; no placeholder data
  - principle: Modular Design
    application: YAML storage enables cache regeneration; skill is self-contained
  - principle: Testing Pyramid
    application: Tier 1 prioritizes unit tests (60%), Tier 2 adds integration (30%), Tier 3 includes E2E (10%)
maturity: production
maturity_reason: |
  - Complete documentation with usage examples, error handling, and troubleshooting
  - Clear "When to Avoid" guidance prevents misuse
  - Realistic example data files demonstrate expected structure
  - Integrates with existing pytest markers and workflow steps
  - Philosophy-aligned with testing pyramid and ruthless simplicity
---

# Smart Test Selection Skill

## Purpose

Optimizes test execution by intelligently selecting which tests to run based on code changes. Instead of running the full test suite every time, this skill:

1. Maps code changes to affected test files using import dependency analysis
2. Provides tiered testing strategies for different feedback loop needs
3. Tracks test reliability to prioritize stable tests in fast runs

## When I Activate

I automatically load when you mention:

- "run affected tests" or "run impacted tests"
- "smart test" or "intelligent testing"
- "which tests to run" or "test selection"
- "fast tests" or "quick tests"
- "tests for changes" or "tests for this PR"

## Core Concepts

### Test Tiers

**Tier 1: Fast Tests (< 1 minute)**

- Directly affected unit tests (imports changed file)
- High-reliability tests only (no flaky tests)
- Run on every save or pre-commit
- Command: `pytest -m "not slow and not integration" [selected_tests]`

**Tier 2: Impacted Tests (< 5 minutes)**

- All tests affected by changes (direct + transitive dependencies)
- Includes integration tests for changed modules
- Run before commit or on PR draft
- Command: `pytest [selected_tests]`

**Tier 3: Full Suite**

- Complete test suite
- Run on PR ready-for-review or CI
- Command: `pytest`

### Import Dependency Analysis

The skill builds a dependency graph by analyzing Python imports:

```
source_file.py
    |
    +-- Imported by: module_a.py, module_b.py
    |       |
    |       +-- Tested by: test_module_a.py, test_module_b.py
    |
    +-- Tested by: test_source_file.py (direct test)
```

**Direct Tests**: Files matching pattern `test_{module}.py` or `{module}_test.py`
**Indirect Tests**: Tests that import modules which import the changed file

### Reliability Tracking

Tests are scored on reliability (0.0 to 1.0):

- **1.0**: Always passes (stable)
- **0.5-0.9**: Occasional failures (investigate)
- **< 0.5**: Frequently fails (flaky - excluded from Tier 1)

Reliability is tracked in `.claude/data/test-mapping/reliability.yaml`

## Usage

### Analyze Changes and Get Test Commands

```
User: What tests should I run for my changes?

Claude (using smart-test):
1. Analyzes git diff or staged changes
2. Maps changed files to test dependencies
3. Returns tiered test commands

Example Output:
------------------------------------------
Smart Test Analysis
------------------------------------------

Changed Files:
- src/amplihack/core/processor.py
- src/amplihack/utils/helpers.py

Tier 1 (Fast - 45s estimated):
  pytest tests/unit/test_processor.py tests/unit/test_helpers.py -v

Tier 2 (Impacted - 3m estimated):
  pytest tests/unit/test_processor.py tests/unit/test_helpers.py \
         tests/integration/test_pipeline.py -v

Tier 3 (Full - 12m estimated):
  pytest

Recommendation: Start with Tier 1 for quick feedback.
```

### Build or Refresh Mapping Cache

```
User: Build the test mapping for this project

Claude:
1. Scans all Python files
2. Builds import dependency graph
3. Maps source files to test files
4. Saves to .claude/data/test-mapping/code_to_tests.yaml
```

### Check Test Reliability

```
User: Show flaky tests

Claude:
1. Reads reliability.yaml
2. Lists tests with reliability < 0.8
3. Suggests investigation or quarantine
```

## Process

### Step 1: Identify Changed Files

```bash
# For staged changes
git diff --cached --name-only --diff-filter=ACMR

# For all uncommitted changes
git diff --name-only --diff-filter=ACMR

# For PR changes (vs main)
git diff main...HEAD --name-only --diff-filter=ACMR
```

Filter to only Python source files (exclude tests themselves for mapping).

### Step 2: Build Import Graph

For each Python file, extract imports:

```python
# Patterns to detect:
import module
from module import item
from package.module import item
from . import relative
from ..parent import item
```

Build bidirectional mapping:

- Forward: file -> what it imports
- Reverse: file -> what imports it

### Step 3: Map to Tests

For each changed file, find tests via:

1. **Direct test match**: `test_{filename}.py` or `{filename}_test.py`
2. **Import-based**: Tests that import the changed module
3. **Transitive**: Tests that import modules that import changed module (1 level)

### Step 4: Apply Reliability Filter

For Tier 1 only, exclude tests with reliability < 0.8.

### Step 5: Generate Commands

Output pytest commands with appropriate markers:

```bash
# Tier 1
pytest -m "not slow and not integration" tests/a.py tests/b.py

# Tier 2
pytest tests/a.py tests/b.py tests/c.py

# Tier 3
pytest
```

## Data Storage

### code_to_tests.yaml

```yaml
# .claude/data/test-mapping/code_to_tests.yaml
version: 1
last_updated: "2025-11-25T10:00:00Z"
mappings:
  src/amplihack/core/processor.py:
    direct_tests:
      - tests/unit/test_processor.py
    indirect_tests:
      - tests/integration/test_pipeline.py
    transitive_tests:
      - tests/e2e/test_full_workflow.py

  src/amplihack/utils/helpers.py:
    direct_tests:
      - tests/unit/test_helpers.py
    indirect_tests:
      - tests/unit/test_processor.py # processor imports helpers
```

### reliability.yaml

```yaml
# .claude/data/test-mapping/reliability.yaml
version: 1
last_updated: "2025-11-25T10:00:00Z"
tests:
  tests/unit/test_processor.py::test_basic:
    passes: 98
    failures: 2
    reliability: 0.98
    last_failure: "2025-11-20"

  tests/integration/test_api.py::test_timeout:
    passes: 45
    failures: 15
    reliability: 0.75
    last_failure: "2025-11-24"
    flaky_reason: "Network dependent"
```

## Integration with Workflow

This skill integrates with DEFAULT_WORKFLOW.md:

**Step 12: Run Tests and Pre-commit Hooks**

- Use Tier 1 (fast) for pre-commit
- Quick feedback on changed code

**Step 13: Mandatory Local Testing**

- Use Tier 2 (impacted) before commit
- Ensures affected code paths are tested

**CI Pipeline**

- Use Tier 2 on draft PRs
- Use Tier 3 (full) on ready-for-review PRs

## Markers Integration

Works with existing pytest markers from pyproject.toml:

- `slow` - Excluded from Tier 1
- `integration` - Excluded from Tier 1
- `e2e` - Excluded from Tier 1 and 2
- `neo4j` - Requires special environment
- `requires_docker` - Requires Docker daemon

## Quick Reference

| Scenario   | Tier | Time Budget | Command Pattern                   |
| ---------- | ---- | ----------- | --------------------------------- |
| Pre-commit | 1    | < 1 min     | `pytest -m "not slow" [affected]` |
| Pre-push   | 2    | < 5 min     | `pytest [affected + transitive]`  |
| Draft PR   | 2    | < 5 min     | `pytest [affected + transitive]`  |
| Ready PR   | 3    | Full        | `pytest`                          |
| CI main    | 3    | Full        | `pytest`                          |

## Philosophy Alignment

### Ruthless Simplicity

- Simple tier system (1, 2, 3)
- YAML storage over database
- Import analysis over complex AST parsing

### Zero-BS Implementation

- Real pytest commands (copy-paste ready)
- Actual time estimates based on test count
- No placeholder data or mock reliability scores

### Testing Pyramid

- Tier 1 prioritizes unit tests (60%)
- Tier 2 adds integration tests (30%)
- Tier 3 includes E2E tests (10%)

## Complementary Skills

- **test-gap-analyzer**: Identifies missing tests
- **outside-in-testing**: Creates E2E test scenarios
- **tester agent**: Writes new tests for gaps
- **pre-commit-diagnostic**: Fixes pre-commit failures

## Common Patterns

### Pattern 1: Quick Iteration

```
[Developer makes small change]
Claude: Run affected tests (Tier 1)
[45 seconds later]
Claude: 3/3 tests passed. Ready for commit.
```

### Pattern 2: Pre-Push Validation

```
[Developer about to push]
Claude: Run impacted tests (Tier 2)
[3 minutes later]
Claude: 12/12 tests passed including integrations.
```

### Pattern 3: Flaky Test Investigation

```
User: Tests keep failing randomly

Claude: Checking reliability data...
Found 2 flaky tests (< 0.8 reliability):
- test_api_timeout (0.75) - Network dependent
- test_concurrent_write (0.68) - Race condition

Recommend: Quarantine these tests or fix root cause.
```

## Limitations

- Python-only import analysis
- Single-level transitive analysis (deeper chains excluded)
- Reliability data requires initial seeding from test runs
- Does not detect dynamic imports or string-based imports

## When to Avoid

Do NOT use smart-test when:

1. **First time setting up tests** - No mapping cache exists yet; run full suite first
2. **Major refactoring** - When module structure changes significantly, mappings become stale
3. **Configuration changes** - Changes to `pytest.ini`, `conftest.py`, or fixtures affect all tests
4. **CI environment variables changed** - Environment-dependent tests may all need re-running
5. **Database schema migrations** - All database-touching tests should run
6. **Flaky test investigation** - Run full suite to get accurate reliability data
7. **Pre-merge final check** - Always run Tier 3 (full suite) before merging to main

**Rule of thumb**: When in doubt, run the full suite. Smart-test optimizes iteration speed, not correctness.

## Error Handling and Troubleshooting

### Common Issues

**Issue: "No tests found for changed file"**

```
Cause: File is new or not yet mapped
Fix: Rebuild the mapping cache
     User: "Rebuild test mapping cache"
```

**Issue: "Import analysis failed"**

```
Cause: Syntax error in Python file or circular imports
Fix: 1. Check file for syntax errors: python -m py_compile file.py
     2. Resolve circular imports
     3. Rebuild mapping cache
```

**Issue: "Reliability data missing"**

```
Cause: No test runs have been recorded yet
Fix: Run full test suite once, then:
     User: "Update test reliability with these results"
```

**Issue: "Tier 1 tests taking too long"**

```
Cause: Too many tests marked as "fast" or slow tests not marked
Fix: 1. Add @pytest.mark.slow to tests > 1 second
     2. Add @pytest.mark.integration to integration tests
     3. Review test granularity
```

**Issue: "Cache is stale / wrong tests selected"**

```
Cause: Module structure changed since last cache build
Fix: Delete cache and rebuild:
     rm -rf .claude/data/test-mapping/*.yaml
     User: "Rebuild test mapping cache"
```

### Recovery Commands

```bash
# Verify test mapping is valid
python -c "import yaml; yaml.safe_load(open('.claude/data/test-mapping/code_to_tests.yaml'))"

# Check reliability data
python -c "import yaml; print(yaml.safe_load(open('.claude/data/test-mapping/reliability.yaml')))"

# Force full suite (bypass smart-test)
pytest --ignore-glob='**/test_slow_*'

# Find tests with no source mapping (orphaned tests)
find tests -name "test_*.py" -exec basename {} \; | sort > /tmp/tests.txt
```

## Cache Maintenance

The mapping cache should be rebuilt when:

- New test files are added
- Module structure changes significantly
- Cache is older than 7 days

Trigger manually: "Rebuild test mapping cache"

---

**Note**: Start with Tier 1 for rapid feedback. If tests pass, you likely caught any regressions. Only escalate to higher tiers when approaching commit/push milestones.
