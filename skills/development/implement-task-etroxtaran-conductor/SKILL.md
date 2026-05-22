---
name: implement-task
description: Implement a task using TDD (tests first, then minimal code)
tags:
  technology: [python, typescript, javascript]
  feature: [workflow, implementation]
  priority: high
---

# Implement Task Skill

## When to Use

Use this skill when you have a task with:
- Clear acceptance criteria
- Defined file scope
- Testable requirements

## Instructions

### Step 1: Analyze the Task

Read the task definition and extract:
- Acceptance criteria (what must be true when done)
- Files to create/modify
- Dependencies on other code

### Step 2: Write Failing Tests

For each acceptance criterion:

```python
# tests/test_<feature>.py
def test_<criterion>():
    # Arrange: Set up test data
    ...
    # Act: Call the function/method
    result = function_under_test(...)
    # Assert: Verify expected behavior
    assert result == expected
```

Run tests to confirm they fail:
```bash
pytest tests/test_<feature>.py -v
```

### Step 3: Implement Minimal Code

Write the simplest code that makes tests pass:
- No premature optimization
- No extra features
- Follow existing patterns

### Step 4: Verify

Run all tests:
```bash
pytest tests/ -v
```

### Step 5: Report

Output format:
```json
{
  "status": "completed",
  "tests_written": 3,
  "tests_passed": 3,
  "files_created": ["src/feature.py"],
  "files_modified": ["src/utils.py"]
}
```

## Completion Signal

When finished, output:
```
<promise>DONE</promise>
```
