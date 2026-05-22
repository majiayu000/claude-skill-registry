---
name: test-structure-analysis
description: Analyzes test directory structure, coverage gaps, and helper consolidation opportunities. Produces coverage reports and refactoring recommendations. Use when auditing test suites, planning test improvements, or identifying coverage gaps.
---

# Test Structure Analysis

Systematic analysis of test organization, coverage, and maintainability.

## When to Use

- Auditing existing test suites
- Planning test coverage improvements
- Identifying helper consolidation opportunities
- Reviewing test directory structure

## MCP Workflow

```python
# 1. Get test directory structure
serena.list_dir(relative_path="tests/", recursive=True)

# 2. Find all test files
serena.find_file(file_mask="test_*.py", relative_path="tests/")

# 3. Count tests per file
serena.search_for_pattern("def test_", paths_include_glob="**/test_*.py")

# 4. Find helper functions
serena.search_for_pattern("def (get_|create_|make_|assert_)", paths_include_glob="**/test_*.py")

# 5. Identify source files without tests
serena.list_dir(relative_path="src/", recursive=True)
```

---

## Analysis Framework

### Step 1: Structure Inventory

```markdown
## Test Structure: {project}

### Directory Layout
```
tests/
├── cli/           [N files, M tests]
├── core/          [N files, M tests]
│   ├── module_a/  [N files, M tests]
│   └── module_b/  [N files, M tests]
└── conftest.py
```

### Statistics
| Metric | Value |
|--------|-------|
| Total test files | N |
| Total tests | M |
| Tests per file (avg) | X |
| conftest files | Y |
```

### Step 2: Coverage Mapping

Create source-to-test mapping:

```markdown
### Coverage Map

| Source | Test File | Coverage |
|--------|-----------|----------|
| src/commands/metric.py | tests/cli/test_metric_cmd.py | HIGH |
| src/core/client.py | tests/core/test_client.py | MEDIUM |
| src/core/models.py | (none) | MISSING |
```

Coverage levels:
- **HIGH**: Core paths tested, edge cases covered
- **MEDIUM**: Core paths tested, gaps exist
- **LOW**: Minimal tests, major gaps
- **MISSING**: No test file exists

### Step 3: Helper Analysis

Identify duplicated helpers:

```markdown
### Helper Functions

| Helper | Location | Count | Action |
|--------|----------|-------|--------|
| get_output() | test_a.py, test_b.py | 2 | Consolidate |
| create_mock_client() | test_c.py | 1 | Keep |
| assert_table() | test_a.py, test_d.py, test_e.py | 3 | Move to helpers.py |
```

---

## Coverage Gap Analysis

### Priority Framework

| Priority | Criteria | Action |
|----------|----------|--------|
| **P1-CRITICAL** | Core business logic, no tests | Create immediately |
| **P2-HIGH** | Public API, minimal tests | Add before release |
| **P3-MEDIUM** | Internal logic, partial tests | Add when touching |
| **P4-LOW** | Utilities, adapters | Optional |

### Gap Identification Pattern

```python
# For each source module
for src_file in source_files:
    test_file = find_corresponding_test(src_file)
    if not test_file:
        # MISSING coverage
        priority = assess_priority(src_file)
    else:
        # Analyze test quality
        test_count = count_tests(test_file)
        public_functions = count_public_functions(src_file)
        coverage_ratio = test_count / public_functions
```

---

## Naming Convention Audit

### Expected Patterns

| Source Type | Test File Pattern |
|-------------|-------------------|
| `commands/{cmd}.py` | `tests/cli/test_{cmd}_cmd.py` |
| `core/{module}/models.py` | `tests/core/{module}/test_models.py` |
| `core/client.py` | `tests/core/test_client.py` |

### Violations

```markdown
### Naming Issues

| File | Issue | Suggested |
|------|-------|-----------|
| tests/test_utils.py | Location unclear | tests/core/test_utils.py |
| tests/cli/metric_tests.py | Wrong prefix | tests/cli/test_metric_cmd.py |
```

---

## Consolidation Recommendations

### When to Consolidate

| Signal | Action |
|--------|--------|
| Same function in 2+ test files | Move to `helpers.py` |
| Same fixture in 2+ test files | Move to `conftest.py` |
| Test file > 500 lines | Consider splitting |
| 0 tests in directory | Remove or add tests |

### Target Structure

```
tests/
├── conftest.py          # Shared fixtures
├── helpers.py           # Shared utility functions
├── fixtures/            # Test data files
│   ├── sample_data.json
│   └── mock_responses.yaml
├── cli/
│   ├── conftest.py      # CLI-specific fixtures
│   └── test_*.py
└── core/
    ├── conftest.py      # Core-specific fixtures
    └── {module}/
        └── test_*.py
```

---

## Output Format

### Quick Analysis

```markdown
## Test Structure: {project}

| Category | Count | Status |
|----------|-------|--------|
| Test files | N | |
| Total tests | M | |
| Coverage gaps | X | P1: Y, P2: Z |
| Duplicate helpers | N | |

### Top Priorities
1. [Most critical gap]
2. [Second priority]
3. [Third priority]
```

### Detailed Report

```markdown
## Test Structure Analysis: {project}

### Summary
- **Total test files**: N
- **Total tests**: M
- **Average tests per file**: X
- **Directories with conftest**: Y/Z

### Coverage Assessment

#### P1-CRITICAL Gaps
| Source | Issue | Recommendation |
|--------|-------|----------------|
| core/client.py | No error path tests | Add 3-4 tests |

#### P2-HIGH Gaps
| Source | Issue | Recommendation |
|--------|-------|----------------|
| commands/workflow.py | Missing backfill tests | Add before release |

### Consolidation Opportunities

#### Helpers to Consolidate
| Helper | Current Locations | Target |
|--------|-------------------|--------|
| get_output() | test_a.py, test_b.py | helpers.py |

#### Fixtures to Consolidate
| Fixture | Current Locations | Target |
|---------|-------------------|--------|
| sample_path | test_a.py, test_c.py | conftest.py |

### Structure Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

### Action Items
- [ ] Create tests/core/module/test_models.py
- [ ] Move get_output() to tests/helpers.py
- [ ] Add conftest.py to tests/core/workflow/
```

---

## Quality Checklist

- [ ] All source modules have corresponding test files
- [ ] Test file naming follows conventions
- [ ] No duplicate helper functions across files
- [ ] Fixtures consolidated in appropriate conftest.py
- [ ] P1 coverage gaps identified and prioritized
- [ ] Directory structure is logical and consistent
