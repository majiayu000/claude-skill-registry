---
name: test-modules
description: Test script creation and execution for Python modules, focusing on functional testing, unit testing, and integration testing. Use when creating test scripts for software modules, running tests to verify functionality, generating test reports, and ensuring code quality in multi-module projects like YouTube-SC.
---

# Test Modules Skill

This skill provides tools and workflows for creating, running, and managing test scripts for Python modules. It supports functional testing, unit testing, and integration testing across multiple project modules.

## Quick Start

1. **Identify module to test**: Determine which module or function needs testing
2. **Create test script**: Write test cases using pytest or unittest
3. **Run tests**: Execute tests and capture results
4. **Analyze results**: Review test output and fix failures
5. **Generate report**: Create test summary and coverage reports

## Core Workflow

### Test Creation Process

When creating tests for a new module:

1. **Analyze module structure**: Review the module's functions and dependencies
2. **Design test cases**: Identify input/output scenarios and edge cases
3. **Write test functions**: Create test functions for each scenario
4. **Set up fixtures**: Configure test fixtures and mock objects
5. **Run initial tests**: Execute tests to verify they work

### Test Execution Process

When running tests:

1. **Run specific test**: `pytest path/to/test_file.py::test_function`
2. **Run all tests**: `pytest` (discover and run all tests)
3. **Run with coverage**: `pytest --cov=module_name`
4. **Generate report**: `pytest --cov=module_name --cov-report=html`
5. **Debug failures**: `pytest -v` for verbose output

### Test Maintenance Process

When updating tests:

1. **Update test data**: Modify test inputs for changed requirements
2. **Refactor tests**: Improve test structure and readability
3. **Add new tests**: Create tests for new functionality
4. **Remove obsolete tests**: Delete tests for removed features
5. **Review coverage**: Ensure adequate test coverage

## Testing Patterns

### Unit Test Pattern
```python
import pytest
from module_name import function_name

def test_function_basic():
    """Test basic functionality."""
    result = function_name(input_value)
    assert result == expected_value

def test_function_edge_cases():
    """Test edge cases and boundary conditions."""
    result = function_name(edge_case_input)
    assert result is not None

def test_function_error_handling():
    """Test error conditions."""
    with pytest.raises(ExpectedError):
        function_name(invalid_input)
```

### Integration Test Pattern
```python
import pytest
from module_a import function_a
from module_b import function_b

def test_integration():
    """Test interaction between modules."""
    result_a = function_a(input_data)
    result_b = function_b(result_a)
    assert result_b == expected_final_result
```

### Fixture Pattern
```python
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Create sample test data."""
    return pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })

def test_with_fixture(sample_data):
    """Test using fixture data."""
    result = process_data(sample_data)
    assert len(result) == 3
```

### Mock Pattern
```python
from unittest.mock import Mock, patch
import module_name

def test_with_mock():
    """Test using mock objects."""
    mock_dependency = Mock(return_value='mocked_result')

    with patch('module_name.dependency_function', mock_dependency):
        result = module_name.function_to_test()

    assert result == 'expected_result'
    mock_dependency.assert_called_once()
```

## YouTube-SC Project Testing

### Module-Specific Test Strategies

#### 1. Clustering Analysis (`sdr_clustering_analysis`)
- Test data loading from Excel files
- Test clustering algorithm parameters
- Test result validation and visualization
- Test performance metrics calculation

#### 2. ML Sentiment Classification (`sentiment_classification_ML`)
- Test text preprocessing functions
- Test feature extraction pipelines
- Test model training and evaluation
- Test prediction accuracy

#### 3. BERT Sentiment Classification (`sentiment_classification_Bert`)
- Test BERT model loading and initialization
- Test tokenization and encoding
- Test fine-tuning process
- Test inference performance

#### 4. Topic Modeling (`topic_modeling`)
- Test LDA/Gensim model initialization
- Test topic extraction and coherence
- Test visualization functions
- Test document-topic distribution

#### 5. Text Statistics (`text_statistics`)
- Test text analysis functions
- Test statistical calculations
- Test visualization outputs
- Test data export formats

### Project-Wide Test Structure
```
tests/
├── sdr_clustering_analysis/
│   ├── test_data_loading.py
│   ├── test_clustering.py
│   └── test_visualization.py
├── sentiment_classification_ML/
│   ├── test_preprocessing.py
│   ├── test_training.py
│   └── test_evaluation.py
├── sentiment_classification_Bert/
│   ├── test_bert_model.py
│   ├── test_tokenization.py
│   └── test_inference.py
├── topic_modeling/
│   ├── test_lda.py
│   ├── test_topics.py
│   └── test_visualization.py
└── text_statistics/
    ├── test_analysis.py
    ├── test_stats.py
    └── test_export.py
```

## Test Configuration

### pytest Configuration (`pytest.ini`)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Coverage Configuration (`.coveragerc`)
```ini
[run]
source = .
omit =
    .venv/*
    __pycache__/*
    tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    raise AssertionError
    raise NotImplementedError
```

## Error Handling

### Common Test Issues

#### 1. Import Errors
```python
# Solution: Ensure proper PYTHONPATH or module structure
import sys
sys.path.append('path/to/module')
```

#### 2. Missing Dependencies
```bash
# Solution: Install required packages
pip install pytest pytest-cov
```

#### 3. Test Data Issues
```python
# Solution: Use fixtures or mock data
@pytest.fixture
def test_data():
    return create_test_data()
```

#### 4. Flaky Tests
```python
# Solution: Add retries or fix timing issues
@pytest.mark.flaky(reruns=3)
def test_flaky_function():
    # test implementation
```

## Best Practices

### Test Design
- Write independent, isolated tests
- Use descriptive test names
- Test one concept per test function
- Include both positive and negative tests
- Test edge cases and boundary conditions

### Test Organization
- Group related tests in test classes or modules
- Use fixtures for common setup/teardown
- Separate unit tests from integration tests
- Maintain test data separately from test code

### Test Execution
- Run tests frequently during development
- Use CI/CD for automated testing
- Monitor test coverage trends
- Fix failing tests immediately

### Test Documentation
- Document test purpose and assumptions
- Include examples of expected behavior
- Note any test dependencies or constraints
- Update tests when requirements change

## Resources

- **pytest Guide**: See `references/pytest-guide.md` for detailed pytest usage
- **Test Examples**: See `references/test-examples.md` for comprehensive test patterns
- **Coverage Guide**: See `references/coverage-guide.md` for test coverage best practices
- **YouTube-SC Examples**: See `examples/youtube-sc/` for project-specific test implementations

## When to Use This Skill

Use this skill when:
- Creating test scripts for Python modules
- Running tests to verify functionality
- Generating test coverage reports
- Debugging test failures and issues
- Setting up test infrastructure for projects
- Maintaining and updating existing tests
- Ensuring code quality through automated testing