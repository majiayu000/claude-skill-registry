---
name: test-sync
description: Detect orphaned tests, obsolete assertions, and test-code misalignment. Use for test suite maintenance, cleanup, and traceability validation. Use when relevant to the task.
---


# Test Sync Skill

## Purpose

Maintain alignment between test files and source code. Detect orphaned tests (code deleted but tests remain), missing tests, and implementation-coupled tests. Based on UTRefactor research showing automated test maintenance can achieve 89% smell reduction.

## Research Foundation

| Concept | Source | Reference |
|---------|--------|-----------|
| Test Refactoring | UTRefactor (ACM 2024) | [89% smell reduction](https://dl.acm.org/doi/10.1145/3715750) |
| Test Smells | Meszaros (2007) | "xUnit Test Patterns" |
| Test-Code Traceability | IEEE TSE | Test maintenance research |

## When This Skill Applies

- After major refactoring
- During test suite health audits
- When tests fail for deleted code
- Before releases (cleanup validation)
- When test count seems disconnected from codebase

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Find orphaned tests" | Detect tests for deleted code |
| "Sync tests with code" | Full alignment analysis |
| "Are my tests up to date?" | Test-code sync check |
| "Clean up test suite" | Find removable tests |
| "Test coverage gaps" | Find missing tests |

## Sync Analysis Types

### 1. Orphaned Test Detection

Tests that reference deleted or renamed code:

```python
def find_orphaned_tests(project_dir):
    """Find tests for code that no longer exists"""
    orphans = []

    for test_file in glob(f"{project_dir}/test/**/*.test.ts"):
        # Extract tested module from import/path
        tested_module = infer_tested_module(test_file)

        if not exists(tested_module):
            orphans.append({
                "test_file": test_file,
                "expected_source": tested_module,
                "status": "source_deleted"
            })

        # Check for unused test helpers
        for helper in extract_test_helpers(test_file):
            if not is_used_in_assertions(test_file, helper):
                orphans.append({
                    "test_file": test_file,
                    "item": helper,
                    "status": "unused_helper"
                })

    return orphans
```

### 2. Missing Test Detection

Source files without corresponding tests:

```python
def find_missing_tests(project_dir):
    """Find source files without tests"""
    missing = []

    for src_file in glob(f"{project_dir}/src/**/*.ts"):
        if is_testable(src_file):  # Exclude types, index files
            test_file = get_test_path(src_file)
            if not exists(test_file):
                missing.append({
                    "source": src_file,
                    "expected_test": test_file,
                    "functions": extract_public_functions(src_file),
                    "priority": assess_priority(src_file)
                })

    return missing
```

### 3. Implementation-Coupled Test Detection

Tests that test implementation details rather than behavior:

```python
COUPLING_PATTERNS = [
    # Testing private methods
    (r'\.\_\w+\(', "Tests private method"),

    # Testing internal state
    (r'\.__\w+', "Accesses internal state"),

    # Mocking too deeply
    (r'mock.*mock.*mock', "Over-mocking"),

    # Testing exact implementation
    (r'toHaveBeenCalledWith.*\{.*\{', "Assertion on implementation details"),
]

def find_coupled_tests(test_file):
    """Detect implementation-coupled tests"""
    content = read_file(test_file)
    issues = []

    for pattern, description in COUPLING_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            issues.append({
                "pattern": pattern,
                "description": description,
                "count": len(matches),
                "risk": "Tests may break on safe refactors"
            })

    return issues
```

### 4. Test-Code Mapping

Verify traceability between tests and source:

```python
def build_test_map(project_dir):
    """Build mapping of tests to source files"""
    mapping = {}

    for test_file in glob(f"{project_dir}/test/**/*.test.ts"):
        source_file = infer_source(test_file)
        imports = extract_imports(test_file)

        mapping[test_file] = {
            "inferred_source": source_file,
            "actual_imports": imports,
            "coverage": get_coverage_for(test_file),
            "alignment": "aligned" if source_file in imports else "misaligned"
        }

    return mapping
```

## Output Format

```markdown
## Test Sync Report

**Project**: my-project
**Analysis Date**: 2024-12-12
**Test Files**: 45
**Source Files**: 78

### Summary

| Category | Count | Action |
|----------|-------|--------|
| Orphaned tests | 3 | Delete |
| Missing tests | 8 | Create |
| Implementation-coupled | 5 | Refactor |
| Aligned | 37 | None |

### Orphaned Tests (Safe to Delete)

#### 1. `test/auth/legacy-login.test.ts`
**Status**: Source deleted
**Original Source**: `src/auth/legacy-login.ts` (deleted in commit abc123)
**Last Modified**: 45 days ago
**Action**: DELETE

```bash
rm test/auth/legacy-login.test.ts
```

#### 2. `test/utils/string-helpers.test.ts`
**Status**: Function removed
**Details**: Tests `formatCurrency()` which was removed
**Action**: DELETE specific test, keep file

```typescript
// Remove this test block:
describe('formatCurrency', () => { ... });
```

### Missing Tests (Should Create)

#### 1. `src/payment/processor.ts` (HIGH PRIORITY)

**Reason**: Payment processing - critical path
**Public Functions**:
- `processPayment(amount, method)` - No test
- `refundPayment(transactionId)` - No test
- `validateCard(cardInfo)` - No test

**Suggested Test File**: `test/payment/processor.test.ts`

```typescript
// Scaffold
describe('PaymentProcessor', () => {
  describe('processPayment', () => {
    it('should process valid payment');
    it('should reject insufficient funds');
    it('should handle network errors');
  });

  describe('refundPayment', () => {
    it('should refund valid transaction');
    it('should reject invalid transaction');
  });
});
```

### Implementation-Coupled Tests (Refactor)

#### 1. `test/api/user-service.test.ts:45`

**Issue**: Tests private method `_validateEmail`
**Risk**: Will break on internal refactoring
**Current**:
```typescript
it('should validate email', () => {
  expect(service._validateEmail('test@test.com')).toBe(true);
});
```

**Suggested Fix**:
```typescript
it('should reject user with invalid email', () => {
  expect(() => service.createUser({ email: 'invalid' }))
    .toThrow('Invalid email');
});
```

### Test-Code Mapping

| Test File | Source File | Status |
|-----------|-------------|--------|
| test/auth/login.test.ts | src/auth/login.ts | ✅ Aligned |
| test/user/profile.test.ts | src/user/profile.ts | ✅ Aligned |
| test/api/old-client.test.ts | (deleted) | ❌ Orphaned |
| (missing) | src/payment/processor.ts | ⚠️ Missing |

### Recommendations

1. **Immediate**: Delete 3 orphaned test files
2. **This Sprint**: Create tests for `processor.ts` (critical)
3. **Debt Reduction**: Refactor 5 implementation-coupled tests
4. **Ongoing**: Add test-sync to CI pipeline

### CI Integration

Add to pre-commit or CI:

```yaml
- name: Test Sync Check
  run: |
    npx test-sync --project . --strict
    # Fails if orphaned tests or missing critical tests
```
```

## Cleanup Actions

### Safe Deletions (Automated)

```bash
# Delete orphaned test files
rm test/auth/legacy-login.test.ts
rm test/utils/old-helpers.test.ts

# Remove orphaned test blocks
sed -i '/describe.*formatCurrency/,/^});$/d' test/utils/string.test.ts
```

### Manual Review Required

- Tests for code moved to different module
- Tests that may cover shared utilities
- Tests with unclear naming

## Integration Points

- Works with `/check-traceability` command
- Reports to Test Architect
- Feeds into test health metrics
- Part of `/project-health-check`

## Script Reference

### test_sync.py
Run sync analysis:
```bash
python scripts/test_sync.py --project . --output report.md
```

### cleanup_orphans.py
Remove orphaned tests:
```bash
python scripts/cleanup_orphans.py --project . --dry-run
```
