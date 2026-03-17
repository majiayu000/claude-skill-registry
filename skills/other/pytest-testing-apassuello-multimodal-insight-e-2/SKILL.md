---
name: Pytest Testing Patterns
description: Apply pytest best practices and project testing conventions. Use when writing or modifying tests.
---

# Pytest Testing Patterns for Constitutional AI

## When to Apply

Automatically activate when:
- Creating new test files
- Modifying existing tests
- Debugging test failures
- Writing test fixtures or mocks

## Project Testing Conventions

### Test File Structure

**Naming convention:**
```
tests/test_{module}.py  # Matches source: constitutional_ai/{module}.py
```

**Example mapping:**
```
constitutional_ai/framework.py  →  tests/test_framework.py
constitutional_ai/trainer.py    →  tests/test_trainer.py
constitutional_ai/principles.py →  tests/test_principles.py
```

### Test Function Naming

```python
def test_{functionality}():
    """Test {what it does}."""
    pass

def test_{class}_{method}():
    """Test {Class}.{method} does {what}."""
    pass

def test_{edge_case}_raises_{exception}():
    """Test that {edge case} raises {ExceptionType}."""
    pass
```

**Examples:**
```python
def test_framework_initialization():
    """Test ConstitutionalFramework initializes with default principles."""

def test_evaluate_text_returns_dict():
    """Test evaluate_text returns dictionary with expected keys."""

def test_invalid_principle_raises_value_error():
    """Test that invalid principle configuration raises ValueError."""
```

## Pytest Core Patterns

### Basic Test Structure

```python
import pytest
from constitutional_ai import ConstitutionalFramework


def test_example():
    # Arrange
    framework = ConstitutionalFramework()

    # Act
    result = framework.evaluate_text("test input")

    # Assert
    assert result is not None
    assert 'any_flagged' in result
```

### Fixtures for Setup

```python
@pytest.fixture
def framework():
    """Provide a configured ConstitutionalFramework for tests."""
    from constitutional_ai import setup_default_framework
    return setup_default_framework()


@pytest.fixture
def mock_model():
    """Provide a mock model for testing."""
    from tests.mocks.mock_model import MockModel
    return MockModel()


def test_with_fixtures(framework, mock_model):
    """Test using fixtures."""
    result = framework.evaluate_text("test", model=mock_model)
    assert result['any_flagged'] == False
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_text,expected_flagged", [
    ("helpful response", False),
    ("harmful content", True),
    ("neutral statement", False),
])
def test_evaluation_cases(framework, input_text, expected_flagged):
    """Test evaluation with various inputs."""
    result = framework.evaluate_text(input_text)
    assert result['any_flagged'] == expected_flagged
```

### Testing Exceptions

```python
def test_invalid_input_raises():
    """Test that invalid input raises ValueError."""
    framework = ConstitutionalFramework()

    with pytest.raises(ValueError, match="must not be empty"):
        framework.evaluate_text("")


def test_missing_model_raises():
    """Test that missing model raises appropriate error."""
    with pytest.raises(RuntimeError):
        generate_text(prompt="test", model=None, tokenizer=None)
```

## Mocking AI Components

### Use Project Mocks

The project has mocks in `tests/mocks/` directory:

```python
from tests.mocks.mock_model import MockModel
from tests.mocks.mock_tokenizer import MockTokenizer

def test_with_mock_model():
    """Test using mock model for deterministic results."""
    model = MockModel()
    tokenizer = MockTokenizer()

    # Mock returns predictable outputs
    output = model.generate(inputs)
    assert output is not None
```

### Why Mock AI Components?

1. **Determinism**: Real models are stochastic
2. **Speed**: Avoid expensive model loading/inference
3. **Isolation**: Test logic independently of model behavior
4. **Portability**: Tests run without GPU or large models

### When to Mock vs Real Models

```python
# ✅ Mock for unit tests
def test_critique_revision_logic():
    """Test critique-revision pipeline logic."""
    model = MockModel()  # Fast, deterministic
    # Test the pipeline logic, not model quality

# ✅ Real model for integration tests (marked slow)
@pytest.mark.slow
def test_end_to_end_training():
    """Test full training pipeline with real model."""
    model = load_model("gpt2")  # Real model
    # Test complete system integration
```

## Coverage Best Practices

### Project Coverage Target

- **Current**: ~45% coverage
- **Target**: This is **acceptable for ML research code**
- **Why**: Training loops, model internals are hard to test exhaustively

### Focus Testing On

1. **Framework logic** (high value, testable)
   - Principle management
   - Evaluation logic
   - Configuration handling

2. **Data processing** (deterministic, testable)
   - Dataset creation
   - Tokenization
   - Preference pair generation

3. **Edge cases** (prevent regressions)
   - Empty inputs
   - Invalid configurations
   - Missing dependencies

### Skip Detailed Testing For

1. **Model internals** (PyTorch's responsibility)
2. **Stochastic generation** (unless mocked)
3. **Long training runs** (expensive, flaky)

## Test Organization Patterns

### Grouping with Classes

```python
class TestConstitutionalFramework:
    """Tests for ConstitutionalFramework class."""

    def test_initialization(self):
        """Test framework initializes correctly."""
        framework = ConstitutionalFramework()
        assert framework is not None

    def test_add_principle(self):
        """Test adding a principle."""
        framework = ConstitutionalFramework()
        principle = ConstitutionalPrinciple(name="test", weight=1.0)
        framework.add_principle(principle)
        assert "test" in framework.principles
```

### Setup and Teardown

```python
class TestWithSetup:
    def setup_method(self):
        """Run before each test method."""
        self.framework = setup_default_framework()

    def teardown_method(self):
        """Run after each test method."""
        # Cleanup if needed
        pass

    def test_example(self):
        """Test using setup."""
        result = self.framework.evaluate_text("test")
        assert result is not None
```

## Running Tests (Common Commands)

### All tests
```bash
pytest tests/ -v
```

### With coverage
```bash
pytest tests/ --cov=constitutional_ai --cov-report=term-missing
```

### Specific module
```bash
pytest tests/test_framework.py -v
```

### Stop on first failure
```bash
pytest tests/ -x
```

### Only failed tests from last run
```bash
pytest tests/ --lf
```

### Parallel execution
```bash
pytest tests/ -n auto
```

### Slow tests only
```bash
pytest tests/ -m slow
```

### Skip slow tests
```bash
pytest tests/ -m "not slow"
```

## Test Quality Checklist

Before committing tests:
- [ ] Test file named `test_{module}.py`
- [ ] Test functions named `test_{functionality}`
- [ ] Docstrings explain what is being tested
- [ ] AI components mocked for determinism
- [ ] Edge cases covered (empty inputs, invalid configs)
- [ ] Assertions are specific and meaningful
- [ ] Tests are independent (no shared state)
- [ ] Fast tests are unmarked, slow tests marked `@pytest.mark.slow`

## Current Test Status

**Metrics:**
- Total tests: 658
- Passing: ~100% (after recent fixes)
- Coverage: ~45% (acceptable for ML code)
- Test files: 14

**Key test modules:**
- test_framework.py - Framework and principle management
- test_principles.py - Evaluation functions
- test_critique_revision.py - Phase 1 pipeline
- test_reward_model.py - Reward model training
- test_ppo_trainer.py - PPO optimization
- test_trainer.py - Supervised fine-tuning
- test_evaluator.py - Evaluation logic
- test_model_utils.py - Model loading and generation

## Example: Complete Test File Template

```python
"""Tests for constitutional_ai/{module}.py"""
import pytest
from constitutional_ai import SomeClass
from tests.mocks.mock_model import MockModel


@pytest.fixture
def instance():
    """Provide configured instance for testing."""
    return SomeClass()


class TestSomeClass:
    """Tests for SomeClass."""

    def test_initialization(self, instance):
        """Test SomeClass initializes correctly."""
        assert instance is not None

    def test_method(self, instance):
        """Test method does expected thing."""
        result = instance.method("input")
        assert result == "expected"

    @pytest.mark.parametrize("input,expected", [
        ("a", 1),
        ("b", 2),
    ])
    def test_parametrized(self, instance, input, expected):
        """Test method with various inputs."""
        assert instance.method(input) == expected

    def test_edge_case_raises(self, instance):
        """Test edge case raises appropriate error."""
        with pytest.raises(ValueError):
            instance.method(None)


@pytest.mark.slow
def test_integration():
    """Test end-to-end with real components."""
    # Use real models, expensive operations
    pass
```
