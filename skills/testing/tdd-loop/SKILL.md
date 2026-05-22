---
name: tdd-loop
description: Test-driven development loop for workflows - write tests first, then implementation
---

# TDD Loop Skill

Use this skill to follow test-driven development practices for workflow implementation.

## TDD Cycle

1. **Write Test First**: Define expected behavior in test.py
2. **Run Test (Red)**: Verify test fails with clear error
3. **Write Implementation**: Add minimal code to make test pass
4. **Run Test (Green)**: Verify test passes
5. **Refactor**: Clean up code while keeping tests green
6. **Repeat**: Move to next test case

## Workflow Testing Pattern

### test.py Structure

```python
#!/usr/bin/env python3
"""Tests for workflow."""

from pathlib import Path
from workflow_name import WorkflowClass, WorkflowParams

def test_workflow_basic():
    """Test basic workflow execution."""
    params = WorkflowParams()
    workflow = WorkflowClass(params, workflow_dir=Path(__file__).parent)

    result = workflow.run()

    assert result == 0  # Success
    # Add more assertions

def test_workflow_with_params():
    """Test workflow with specific parameters."""
    params = WorkflowParams(param1="value")
    workflow = WorkflowClass(params, workflow_dir=Path(__file__).parent)

    result = workflow.run()

    assert result == 0
    # Verify outputs, side effects, etc.

def test_workflow_error_handling():
    """Test workflow handles errors gracefully."""
    params = WorkflowParams(invalid="value")
    workflow = WorkflowClass(params, workflow_dir=Path(__file__).parent)

    # Should handle error, not crash
    result = workflow.run()
    assert result != 0  # Non-zero exit code for errors
```

## dry_run.py Testing

The dry run is a form of integration testing with mocks:

```python
#!/usr/bin/env python3
"""Dry run with mock data."""

from raw_runtime import DryRunContext

def mock_external_api(ctx: DryRunContext):
    """Mock API call that would normally fetch real data."""
    return {
        "data": "mock_value",
        "status": "success"
    }

def mock_file_write(ctx: DryRunContext):
    """Mock file writing - don't actually write."""
    ctx.log("Would write to file: results/output.json")
    return True
```

## TDD Benefits

1. **Clear Requirements**: Tests document expected behavior
2. **Regression Prevention**: Existing tests catch breaking changes
3. **Refactoring Safety**: Change internals without breaking API
4. **Design Feedback**: Hard-to-test code signals design issues

## When to Use

- Adding new workflow functionality
- Fixing bugs (write failing test, then fix)
- Refactoring existing code
- Integrating new tools

## Red-Green-Refactor Example

```python
# 1. RED: Write failing test
def test_fetch_stock_data():
    result = fetch_stock_data("AAPL")
    assert result["symbol"] == "AAPL"
    assert "price" in result
# Run: pytest test.py -k test_fetch (FAILS - function doesn't exist)

# 2. GREEN: Minimal implementation
def fetch_stock_data(symbol: str) -> dict:
    return {"symbol": symbol, "price": 150.0}  # Hardcoded for now
# Run: pytest test.py -k test_fetch (PASSES)

# 3. REFACTOR: Real implementation
def fetch_stock_data(symbol: str) -> dict:
    from tools.yahoo_finance import get_quote
    data = get_quote(symbol)
    return {"symbol": data.symbol, "price": data.current_price}
# Run: pytest test.py -k test_fetch (PASSES)
```
