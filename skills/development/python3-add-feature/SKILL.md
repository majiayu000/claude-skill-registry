---
name: python3-add-feature
description: Guided workflow for adding new features to Python projects. Use when planning a new feature implementation, when adding functionality with proper test coverage, or when following TDD to build features incrementally.
user-invocable: true
argument-hint: "<feature-description>"
---

# Python Feature Addition Workflow

The model guides feature development through discovery, planning, implementation, and verification phases.

## Arguments

$ARGUMENTS

## Instructions

1. **Understand the feature request** from arguments
2. **Discover project context** (structure, patterns, existing code)
3. **Plan implementation** (files to create/modify, dependencies)
4. **Implement with tests** following TDD
5. **Verify quality** (linting, types, coverage)

---

## Phase 1: Discovery

### Gather Project Context

```text
CHECK:
- [ ] pyproject.toml exists and has project configuration
- [ ] src/ or packages/ directory structure
- [ ] tests/ directory with existing test patterns
- [ ] Linting configuration (ruff, mypy)
- [ ] Existing patterns for similar features
```

### Identify Integration Points

Determine where the feature fits:

- Which module/package owns this functionality?
- What existing classes/functions will interact with it?
- What new files need to be created?

---

## Phase 2: Planning

### Feature Specification

Create a clear specification:

```markdown
## Feature: [Name]

**Purpose**: [One sentence describing what this enables]

**User Story**: As a [user type], I want [capability] so that [benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Files to Create/Modify**:
- `src/module/new_feature.py` - Main implementation
- `tests/test_new_feature.py` - Test suite
- `src/module/__init__.py` - Export new functionality

**Dependencies**:
- Internal: [existing modules to import]
- External: [new packages if any]
```

### Design Interface First

Define the public API before implementation:

```python
# Define function signatures and docstrings
def new_feature(
    input_data: InputType,
    *,
    option: str = "default",
) -> ResultType:
    """Process input data with new feature capability.

    Args:
        input_data: The data to process
        option: Configuration option

    Returns:
        Processed result

    Raises:
        ValidationError: If input_data is invalid
    """
    ...
```

---

## Phase 3: Test-Driven Implementation

### Write Tests First

```python
import pytest
from pytest_mock import MockerFixture

class TestNewFeature:
    """Tests for new_feature functionality."""

    def test_basic_operation(self) -> None:
        """Test basic feature operation with valid input."""
        # Arrange
        input_data = create_valid_input()

        # Act
        result = new_feature(input_data)

        # Assert
        assert result.status == "success"

    def test_handles_invalid_input(self) -> None:
        """Test feature raises error for invalid input."""
        with pytest.raises(ValidationError, match="Invalid input"):
            new_feature(invalid_input)

    def test_option_affects_behavior(self) -> None:
        """Test that option parameter changes processing."""
        result_default = new_feature(data, option="default")
        result_custom = new_feature(data, option="custom")

        assert result_default != result_custom
```

### Implement to Pass Tests

1. Run tests - they should fail (red)
2. Implement minimal code to pass (green)
3. Refactor for quality (refactor)
4. Repeat for each test case

### Implementation Checklist

```text
- [ ] All functions have complete type hints
- [ ] Docstrings follow Google style
- [ ] Error handling uses specific exceptions
- [ ] No hardcoded values (use constants or config)
- [ ] Follows existing project patterns
```

---

## Phase 4: Integration

### Update Module Exports

```python
# src/module/__init__.py
from .new_feature import new_feature, ResultType

__all__ = [
    "new_feature",
    "ResultType",
    # ... existing exports
]
```

### Add to CLI (if applicable)

```python
@app.command()
def feature_command(
    input_file: Annotated[Path, typer.Argument(help="Input file")],
) -> None:
    """Run new feature on input file."""
    result = new_feature(load_data(input_file))
    console.print(f"Result: {result}")
```

---

## Phase 5: Verification

### Run Quality Checks

```bash
# Linting
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Type checking
uv run mypy src/ tests/

# Tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

### Coverage Requirements

- New feature code: 100% coverage
- Integration points: Covered by integration tests
- Overall project: Maintain or improve existing coverage

### Documentation

Update relevant documentation:

- README.md if user-facing feature
- API docs if public interface
- CHANGELOG.md with feature description

---

## Example Workflow

**Request**: "Add CSV export functionality to the report module"

### Discovery

```text
Project structure:
- src/reports/generator.py - existing report generation
- src/reports/formats/ - existing format handlers
- tests/reports/ - existing report tests

Pattern: Format handlers inherit from BaseFormatter
```

### Planning

```markdown
## Feature: CSV Export

**Purpose**: Export reports in CSV format

**Files**:
- `src/reports/formats/csv_formatter.py` - CSV implementation
- `tests/reports/formats/test_csv_formatter.py` - Tests

**Interface**:
class CsvFormatter(BaseFormatter):
    def format(self, report: Report) -> str: ...
```

### Implementation

1. Write tests for CsvFormatter
2. Implement CsvFormatter class
3. Register in format factory
4. Add CLI option `--format csv`
5. Run verification checks

---

## Quality Standards

The model MUST ensure:

1. **Type Safety**: All code passes mypy --strict
2. **Linting**: Zero ruff errors or warnings
3. **Tests**: New code has 100% coverage
4. **Patterns**: Follows existing project conventions
5. **Documentation**: Docstrings on all public interfaces

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
