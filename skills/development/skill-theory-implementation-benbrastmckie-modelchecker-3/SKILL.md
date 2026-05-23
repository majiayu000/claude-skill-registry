---
name: skill-theory-implementation
description: Implement semantic theories and Python/Z3 code with TDD. Invoke for Python-language implementation tasks.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(PYTHONPATH=* pytest *), Bash(PYTHONPATH=* python *), Bash(cd Code && python -m build)
context: fork
---

# Theory Implementation Skill

Execute Python/Z3 semantic theory implementation with strict TDD workflow.

## Trigger Conditions

This skill activates when:
- Task language is "python"
- /implement command targets a Python task
- Code changes to semantic theories needed

## Core Workflow: TDD

**MANDATORY**: All implementations follow Test-Driven Development:

```
RED → GREEN → REFACTOR

1. RED: Write failing test first
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve while tests pass
```

## Essential Commands

### Run Tests
```bash
# All tests
PYTHONPATH=Code/src pytest Code/tests/ -v

# Specific theory
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/logos/tests/ -v

# Single file
PYTHONPATH=Code/src pytest path/to/test_file.py -v

# With coverage
PYTHONPATH=Code/src pytest --cov=model_checker --cov-report=term-missing
```

### Quick Validation
```bash
# Check imports
PYTHONPATH=Code/src python -c "from model_checker.theory_lib.logos import get_theory"

# Run examples
cd Code && ./dev_cli.py examples/logos_example.py
```

## Implementation Strategy

### 1. Plan Review

Load and understand the implementation plan:
- What components to create/modify
- What approach to use
- What tests are needed

### 2. TDD Cycle

For each component:

```
1. Write test file first (test_*.py)
2. Run test - verify it fails (RED)
3. Write minimal implementation
4. Run test - verify it passes (GREEN)
5. Refactor if needed
6. Run all related tests - verify no regressions
```

### 3. Theory Component Pattern

For semantic theories, implement in this order:

```python
# 1. Tests first (tests/unit/test_semantic.py)
def test_new_operator_verifier():
    """Test new operator verifier semantics."""
    ...

# 2. Semantic clause (semantic.py)
def new_operator_verifier(self, ...):
    """Z3 constraint for verifier clause."""
    ...

# 3. Operator registration (operators.py)
Operator(
    name='new_op',
    verifier=semantic.new_operator_verifier,
    ...
)

# 4. Examples (examples.py)
BuildExample(
    premises=['A new_op B'],
    conclusions=['...'],
    ...
)
```

## Code Patterns

### Semantic Clause Pattern
```python
def operator_verifier(self, sentence, eval_world):
    """
    Verifier clause for operator.

    Args:
        sentence: Sentence object with operator and arguments
        eval_world: Z3 BitVec for evaluation world

    Returns:
        Z3 constraint for verifier condition
    """
    left = sentence.arguments[0]
    right = sentence.arguments[1]

    # Get verifier constraints for subformulas
    left_ver = self.true_at(left, eval_world)
    right_ver = self.true_at(right, eval_world)

    # Combine according to operator semantics
    return z3.And(left_ver, right_ver)
```

### Test Pattern
```python
import pytest
from model_checker.theory_lib.logos import get_theory, get_examples

class TestNewOperator:
    """Tests for new operator implementation."""

    @pytest.fixture
    def theory(self):
        return get_theory()

    def test_verifier_basic(self, theory):
        """Test basic verifier case."""
        # Arrange
        example = BuildExample(
            premises=['A op B'],
            conclusions=['C'],
            settings={'N': 3}
        )

        # Act
        result = example.check(theory)

        # Assert
        assert result.valid == True
```

### Import Pattern
```python
# Standard library
import os
from pathlib import Path
from typing import Dict, List, Optional

# Third-party
import z3
from z3 import And, Or, Not, Implies

# Local - prefer relative imports within package
from .models import Model
from ..utils import z3_helpers
from ...syntactic import Sentence
```

## Execution Flow

```
1. Receive task context with plan
2. Load plan and find resume point
3. For each phase:
   a. Write tests first (TDD RED)
   b. Verify tests fail
   c. Implement minimal code (TDD GREEN)
   d. Verify tests pass
   e. Refactor if beneficial
   f. Run full test suite
   g. Git commit phase
4. Final validation:
   a. Run all affected tests
   b. Check imports work
   c. Verify no regressions
5. Create implementation summary
6. Return results
```

## Common Operations

### Add New Operator

1. Add test in `theory_lib/{theory}/tests/unit/test_operators.py`
2. Add semantic clause in `semantic.py`
3. Register in `operators.py`
4. Add examples in `examples.py`
5. Run theory tests

### Modify Existing Code

1. Find existing tests for component
2. Add test for new behavior
3. Modify implementation
4. Verify all tests pass

### Add New Theory Feature

1. Check existing theory for pattern
2. Write tests for new feature
3. Implement following existing patterns
4. Update theory __init__.py if needed

## Verification Checklist

Before marking phase complete:

- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] Imports work from package root
- [ ] Type hints present for new code
- [ ] Docstrings for public functions
- [ ] No TODO/FIXME left in code

## Return Format

```json
{
  "status": "completed|partial",
  "summary": "Implemented N components with full test coverage",
  "artifacts": [
    {
      "path": "Code/src/model_checker/theory_lib/logos/semantic.py",
      "type": "implementation",
      "description": "Added new operator semantics"
    },
    {
      "path": "Code/src/model_checker/theory_lib/logos/tests/unit/test_operators.py",
      "type": "test",
      "description": "Tests for new operator"
    }
  ],
  "tests_added": 5,
  "tests_passed": 5,
  "coverage_change": "+2.3%"
}
```

## Error Handling

### Test Failure
1. Read full test output
2. Identify failing assertion
3. Fix implementation (not test, unless test is wrong)
4. Re-run specific test
5. Continue when passing

### Import Error
1. Check PYTHONPATH is set
2. Verify relative import path
3. Check __init__.py exports

### Z3 Error
1. Check constraint types match
2. Verify solver context
3. Add timeout if needed
4. Simplify constraints if possible

## Key Locations

- **Theories**: `Code/src/model_checker/theory_lib/`
- **Models**: `Code/src/model_checker/models/`
- **Tests**: `Code/tests/` and `*/tests/` within packages
- **Standards**: `Code/docs/core/TESTING_GUIDE.md`
