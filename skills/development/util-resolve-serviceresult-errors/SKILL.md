---
name: util-resolve-serviceresult-errors
description: |
  Fix ServiceResult pattern mistakes causing test failures and type errors.
  Use when seeing "dict object has no attribute success", "mock not returning ServiceResult",
  mock assertions failing, or type errors with ServiceResult. Analyzes .py test files
  and service implementations. Covers async/await patterns, monad operations (map, bind, flatmap),
  and proper mock configuration.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - MultiEdit
---

# Resolve ServiceResult Errors

## Purpose

Systematic diagnostic and fix workflow for ServiceResult pattern mistakes in tests and service implementations, focusing on mock configuration errors, async patterns, and type safety.

## Quick Start

Diagnose and fix common mistakes when working with the ServiceResult pattern in project-watch-mcp, focusing on test failures caused by incorrect mock configurations and improper ServiceResult usage.

**Most common use case:**
```bash
# Test fails with: 'dict' object has no attribute 'success'

❌ WRONG:
mock_service.get_data = AsyncMock(return_value={"items": []})

✅ CORRECT:
from project_watch_mcp.domain.common import ServiceResult
mock_service.get_data = AsyncMock(return_value=ServiceResult.ok({"items": []}))

Result: Test passes, ServiceResult pattern enforced
```

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [What This Skill Does](#what-this-skill-does)
3. [Instructions](#instructions)
4. [Usage Examples](#usage-examples)
5. [Expected Outcomes](#expected-outcomes)
6. [Requirements](#requirements)
7. [Troubleshooting](#troubleshooting)
8. [Red Flags to Avoid](#red-flags-to-avoid)
9. [Automation Scripts](#automation-scripts)

---

## When to Use This Skill

Use this skill when seeing:
- **Mock errors:** `'dict' object has no attribute 'success'`
- **Async errors:** `coroutine object has no attribute 'success'`
- **Type errors:** `Incompatible types in assignment` with ServiceResult[T]
- **Unwrap errors:** `Cannot unwrap None data from successful result`
- **Test failures:** Mock assertions failing with ServiceResult

**Trigger phrases:**
- "Mock not returning ServiceResult"
- "dict object has no attribute success"
- "Fix ServiceResult errors"
- "ServiceResult type errors"
- "Mock configuration incorrect"

---

## What This Skill Does

This skill provides systematic fixes for:

1. **Mock configuration errors** - Fix mocks returning dict instead of ServiceResult
2. **Async ServiceResult patterns** - Configure AsyncMock with proper return_value
3. **ServiceResult chaining** - Use composition utilities (map, bind, flatmap)
4. **Type error resolution** - Fix ServiceResult[T] type mismatches
5. **Unwrap safety** - Handle None data and failure cases correctly

See Instructions section below for detailed diagnostic workflow.

---

## Instructions

### Step 1: Identify the Error Pattern

Run the test and classify the error:

```bash
uv run pytest tests/path/to/failing_test.py -v
```

**Common Error Signatures:**

1. **Mock Returns Dict**
   - Error: `'dict' object has no attribute 'success'`
   - Cause: Mock configured with `return_value = {"key": "value"}`
   - Fix: Use `return_value = ServiceResult.ok({"key": "value"})`

2. **Async Mock Missing Await**
   - Error: `coroutine object has no attribute 'success'`
   - Cause: AsyncMock returns coroutine, not ServiceResult
   - Fix: Use `AsyncMock(return_value=ServiceResult.ok(...))`

3. **Type Error with Chaining**
   - Error: `Incompatible types in assignment`
   - Cause: ServiceResult[T] type mismatch in chained operations
   - Fix: Use proper type annotations and composition utilities

4. **Unwrap on None Data**
   - Error: `Cannot unwrap None data from successful result`
   - Cause: `ServiceResult.ok(None).unwrap()`
   - Fix: Check `result.data is not None` before unwrapping

### Step 2: Fix Mock Configuration

**❌ WRONG - Mock Returns Dict:**
```python
mock_service.get_data = AsyncMock(return_value={"items": []})
# Causes: 'dict' object has no attribute 'success'
```

**✅ CORRECT - Mock Returns ServiceResult:**
```python
from project_watch_mcp.domain.common import ServiceResult

mock_service.get_data = AsyncMock(
    return_value=ServiceResult.ok({"items": []})
)
```

**Pattern for Multiple Mock Methods:**
Use MultiEdit to fix all mocks in one operation:

```python
# Fix all mocks in test file at once
mock_repo.file_exists = AsyncMock(return_value=ServiceResult.ok(False))
mock_repo.store_file = AsyncMock(return_value=ServiceResult.ok())
mock_service.create_chunks = AsyncMock(return_value=ServiceResult.ok(chunks))
```

### Step 3: Fix ServiceResult Chaining

**Common Chaining Mistakes:**

1. **Direct Data Access Without Check**
   ```python
   # ❌ WRONG - No success check
   result = service.get_data()
   data = result.data  # Could be None on failure!

   # ✅ CORRECT - Check success first
   result = service.get_data()
   if result.success:
       data = result.data
   else:
       return ServiceResult.fail(result.error)
   ```

2. **Sequential Operations**
   ```python
   # ❌ WRONG - Manual chaining
   result1 = service1.operation()
   if result1.success:
       result2 = service2.operation(result1.data)
       if result2.success:
           return result2
   return result1 if not result1.success else result2

   # ✅ CORRECT - Use composition utilities
   from project_watch_mcp.domain.common.service_result_utils import compose_results

   result = service1.operation()
   result = compose_results(lambda d: service2.operation(d), result)
   return result
   ```

3. **Async Context**
   ```python
   # ✅ CORRECT - Async ServiceResult pattern
   async def process_file(file_path: Path) -> ServiceResult[dict]:
       result = await self.reader.read_file(file_path)
       if result.is_failure:
           return ServiceResult.fail(result.error)

       # result.success guarantees result.data is not None
       content = result.data
       return ServiceResult.ok({"content": content})
   ```

### Step 4: Use ServiceResult Composition Utilities

Import composition utilities for complex workflows:

```python
from project_watch_mcp.domain.common.service_result_utils import (
    compose_results,    # Monadic bind (flatMap)
    map_result,         # Functor map
    chain_results,      # Chain multiple results
    collect_results,    # Collect list of results
    flatten_results,    # Flatten nested results
    unwrap_or_fail,     # Convert to exception
)
```

**Examples:**

```python
# Map over successful result
result = ServiceResult.ok([1, 2, 3])
doubled = map_result(lambda items: [x * 2 for x in items], result)
# Result: ServiceResult.ok([2, 4, 6])

# Compose operations (flatMap)
def validate(data: dict) -> ServiceResult[dict]:
    if "required_field" in data:
        return ServiceResult.ok(data)
    return ServiceResult.fail("Missing required field")

result = ServiceResult.ok({"required_field": "value"})
validated = compose_results(validate, result)

# Chain multiple results
result1 = ServiceResult.ok(10)
result2 = ServiceResult.ok(20)
result3 = ServiceResult.ok(30)
combined = chain_results(result1, result2, result3)
# Result: ServiceResult.ok([10, 20, 30])
```

### Step 5: Fix Type Errors

**Common Type Issues:**

1. **Generic Type Mismatch**
   ```python
   # ❌ WRONG - Type mismatch
   def process() -> ServiceResult[list[str]]:
       result: ServiceResult[dict] = get_data()
       return result  # Type error!

   # ✅ CORRECT - Proper type transformation
   def process() -> ServiceResult[list[str]]:
       result: ServiceResult[dict] = get_data()
       if result.is_failure:
           return ServiceResult.fail(result.error)

       items = list(result.data.keys())
       return ServiceResult.ok(items)
   ```

2. **Optional Data Handling**
   ```python
   # ❌ WRONG - Not handling None
   result = ServiceResult.ok(None)
   value = result.unwrap()  # Raises ValueError!

   # ✅ CORRECT - Use unwrap_or for optional data
   result = ServiceResult.ok(None)
   value = result.unwrap_or([])  # Returns default on None/failure
   ```

### Step 6: Validate Fix

After fixing mocks and ServiceResult usage:

```bash
# Run the specific test
uv run pytest tests/path/to/test_file.py::test_name -v

# Run all related tests
uv run pytest tests/unit/application/ -v -k "service"

# Verify type safety
uv run pyright src/project_watch_mcp/
```

## Usage Examples

### Example 1: Fix Mock Returns Dict Error

**Scenario:** Test fails with `'dict' object has no attribute 'success'`

**Before (Failing Test):**
```python
@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=CodeRepository)
    # ❌ WRONG - Returns dict, not ServiceResult
    repo.get_files = AsyncMock(return_value={"files": []})
    return repo

async def test_get_files(mock_repository):
    handler = FileHandler(mock_repository)
    result = await handler.process()

    # Fails: 'dict' object has no attribute 'success'
    assert result.success is True
```

**After (Fixed Test):**
```python
from project_watch_mcp.domain.common import ServiceResult

@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=CodeRepository)
    # ✅ CORRECT - Returns ServiceResult
    repo.get_files = AsyncMock(
        return_value=ServiceResult.ok({"files": []})
    )
    return repo

async def test_get_files(mock_repository):
    handler = FileHandler(mock_repository)
    result = await handler.process()

    # Now works correctly
    assert result.success is True
    assert result.data == {"files": []}
```

### Example 2: Fix Async ServiceResult Pattern

**Scenario:** Async mock returning coroutine instead of ServiceResult

**Fix:**
```python
from project_watch_mcp.domain.common import ServiceResult

# ❌ WRONG - AsyncMock without proper return_value
service.embed_text = AsyncMock()

# ✅ CORRECT - AsyncMock with ServiceResult return_value
service.embed_text = AsyncMock(
    return_value=ServiceResult.ok([0.1, 0.2, 0.3])
)
```

For more examples, see **[references/troubleshooting.md](./references/troubleshooting.md)** and **[templates/serviceresult-patterns.md](./templates/serviceresult-patterns.md)**.

## Expected Outcomes

**Successful Fix:**
- Test passes after mock returns ServiceResult
- AsyncMock configured with proper return_value
- Type annotations match ServiceResult[T]
- No pyright errors
- Unwrap safety checks in place

**Refactoring Opportunity Identified:**
- Sequential `if result.success:` checks detected
- Recommendation: Use compose_results() utilities
- See Step 4 in Instructions for composition utilities

---

## Requirements

**Imports:**
- `from project_watch_mcp.domain.common import ServiceResult`
- `from project_watch_mcp.domain.common.service_result_utils import <utility>`
- `from unittest.mock import AsyncMock` (for async methods)

**Tools:**
- Read - View test files and service implementations
- Edit/MultiEdit - Fix mock configurations and ServiceResult usage
- Grep - Find all occurrences of pattern
- Glob - Locate test files with ServiceResult issues

**Knowledge:**
- ServiceResult pattern (success/failure monad)
- AsyncMock vs MagicMock differences
- Python type annotations (ServiceResult[T])
- Composition utilities (map, bind, flatmap)

**Optional:**
- Understanding of monad pattern
- Familiarity with functional programming concepts

---

## Troubleshooting

For detailed troubleshooting steps and validation workflows, see **[references/troubleshooting.md](./references/troubleshooting.md)**.

**Quick fixes:**
- `'dict' object has no attribute 'success'` → Use `ServiceResult.ok(data)` instead of `data`
- `coroutine object has no attribute 'success'` → Add `return_value` to AsyncMock
- Type errors → Check ServiceResult[T] generic type matches
- Unwrap errors → Use `unwrap_or(default)` for optional data

---

## Red Flags to Avoid

1. **Forgetting ServiceResult Wrapper**
   - ❌ `return_value = data`
   - ✅ `return_value = ServiceResult.ok(data)`

2. **Not Checking Success Before Data Access**
   - ❌ `data = result.data`
   - ✅ `if result.success: data = result.data`

3. **Using unwrap() Without Null Check**
   - ❌ `value = result.unwrap()`  (raises on None)
   - ✅ `value = result.unwrap_or(default)`

4. **Mixing Async and Sync Mocks**
   - ❌ `MagicMock(return_value=ServiceResult.ok(...))` for async method
   - ✅ `AsyncMock(return_value=ServiceResult.ok(...))` for async method

5. **Not Propagating Errors**
   - ❌ Silently ignoring failure results
   - ✅ Returning failure immediately: `if result.is_failure: return result`

## Automation Scripts

Powerful automation utilities to detect and fix ServiceResult issues automatically.

### Available Scripts

1. **[fix_serviceresult_mocks.py](./scripts/fix_serviceresult_mocks.py)** - Auto-fix test mock errors
2. **[validate_serviceresult_usage.py](./scripts/validate_serviceresult_usage.py)** - Validate ServiceResult patterns
3. **[find_serviceresult_chains.py](./scripts/find_serviceresult_chains.py)** - Identify refactoring opportunities

**Usage:**
```bash
# Fix all test mocks automatically
python scripts/fix_serviceresult_mocks.py --all tests/

# Find all violations in codebase
python scripts/validate_serviceresult_usage.py src/

# Get refactoring suggestions
python scripts/find_serviceresult_chains.py --suggest-refactor src/
```

---

## See Also

### Supporting Files

- **[references/troubleshooting.md](./references/troubleshooting.md)** - Detailed troubleshooting guide with validation workflows
- **[references/advanced-patterns.md](./references/advanced-patterns.md)** - Integration points, benefits analysis, and success metrics
- **[templates/serviceresult-patterns.md](./templates/serviceresult-patterns.md)** - Quick reference templates
- **[references/monad-pattern.md](./references/monad-pattern.md)** - Understanding the monad pattern

### Related Skills

- **test-debug-failures** - Fix ServiceResult-specific test failures
- **python-best-practices-type-safety** - Resolve ServiceResult[T] type mismatches
- **test-setup-async** - Configure AsyncMock with ServiceResult
- **implement-cqrs-handler** - Ensure handlers return ServiceResult
- **implement-repository-pattern** - Validate repository ServiceResult returns
