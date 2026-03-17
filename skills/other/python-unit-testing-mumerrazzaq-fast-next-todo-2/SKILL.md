---
name: python-unit-testing
description: >-
  A skill for creating comprehensive Python unit tests using pytest. It provides
  guidance and templates for test structure, fixtures, mocking, parameterization,
  and coverage. Use this when you need to write unit tests for Python code, set up
  a testing environment with pytest, or apply testing best practices.
---

# Python Unit Testing with Pytest

This skill provides a structured workflow and resources for writing effective unit tests in Python using the `pytest` framework.

## Core Workflow

1.  **Setup (`pytest.ini`, `conftest.py`)**: If the project doesn't have a testing setup, copy the templates from the `assets/` directory.
    -   `assets/pytest.ini`: Standard pytest and coverage configuration.
    -   `assets/conftest.py`: Reusable fixtures, including mocks for a database and an API client.
2.  **Create Test File**: For a given source file `path/to/module.py`, create a corresponding test file `tests/path/to/test_module.py`.
    -   For guidance, read `references/01_organization.md`.
    -   Follow the naming conventions in `references/02_naming_conventions.md`.
3.  **Write Tests**: Write test functions using the Arrange-Act-Assert pattern.
    -   Start with a template from `assets/templates/`.
        -   `simple_test.py`: For basic tests.
        -   `parameterized_test.py`: For testing with multiple inputs.
        -   `mocking_test.py`: For testing code with external dependencies.
4.  **Run and Iterate**: Run `pytest` and use the output to refine tests. If coverage is configured, use the report to find untested code.

## Reference Guides

When you need to implement a specific pattern, consult the relevant reference guide. Read them as needed.

-   **`references/01_organization.md`**: How to structure your `tests` directory.
-   **`references/02_naming_conventions.md`**: How to name test files and functions.
-   **`references/03_fixtures.md`**: How to use `pytest` fixtures for setup and teardown.
-   **`references/04_mocking.md`**: How to mock external dependencies like APIs and databases.
-   **`references/05_parameterization.md`**: How to run one test with multiple different inputs.
-   **`references/06_assertions.md`**: Best practices for `assert` statements and checking for exceptions.
-   **`references/07_coverage.md`**: How to measure and interpret test coverage.

Always start by using the templates in `assets/` as a base for new test files.
