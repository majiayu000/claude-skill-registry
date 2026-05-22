---
name: test-coverage-analyst
description: "Guides on analyzing and improving test coverage for Python (pytest-cov) and JavaScript (c8) projects. Use when a user asks to set up test coverage, generate coverage reports, understand why coverage is low, or improve their test coverage."
---

# Test Coverage Analyst

## Overview

This skill provides a structured workflow for analyzing and improving test coverage in Python and JavaScript projects. It covers configuration, report generation, and strategies for increasing coverage.

## Workflow

Follow these steps to help a user with test coverage.

### 1. Identify Project Type and Tools

First, determine the project's language and package manager.

-   **Python**: Look for `requirements.txt`, `pyproject.toml`, or a `venv` directory. The primary coverage tool is `pytest-cov`.
-   **JavaScript**: Look for `package.json`. The recommended coverage tool is `c8`.

### 2. Check for Existing Configuration

Before adding new configurations, inspect existing files for coverage setup.

-   For Python, check `pyproject.toml`, `setup.cfg`, or `.coveragerc`.
-   For JavaScript, check the `"c8"` key or scripts in `package.json`, or a `.nycrc.json` file.

### 3. Configure and Install Tools

If coverage tools are not set up, guide the user through installation and configuration.

-   **For Python (`pytest-cov`)**:
    -   Install `pytest-cov`.
    -   Create or update the configuration, usually in `pyproject.toml`.
    -   For detailed instructions, see [Python Test Coverage with pytest-cov](references/python-pytest-cov.md).

-   **For JavaScript (`c8`)**:
    -   Install `c8` as a dev dependency.
    -   Create or update the configuration, usually in `package.json`.
    -   For detailed instructions, see [JavaScript Test Coverage with c8](references/js-c8.md).

### 4. Run Coverage and Generate Reports

Execute the coverage tool to run tests and generate a report. The most useful reports are the terminal summary and the interactive HTML report.

-   **Terminal Report**: Provides a quick summary of coverage percentages.
-   **HTML Report**: Provides a detailed, line-by-line view of code coverage, which is essential for identifying untested code.
-   **XML/LCOV Report**: These are for integrating with third-party CI services like Codecov.

Refer to the language-specific guides for exact commands.

### 5. Analyze the Report and Formulate a Strategy

-   **Interpret the results**: Explain the difference between line and branch coverage. Use the HTML report to pinpoint exactly which lines and branches are not covered.
-   **Develop an improvement plan**: Based on the report, create a plan to improve coverage.
-   For a deep dive into analysis and strategies, consult the [Test Coverage Improvement Strategies](references/improvement-strategies.md) guide.

### 6. Continuous Integration (CI)

For ongoing coverage monitoring, help the user integrate coverage checks into their CI pipeline.
-   This usually involves generating a report (XML or LCOV) and uploading it to a service like Codecov.
-   For example configurations, see the [CI Integration for Coverage](references/ci-integration.md) guide.

## Resources

This skill includes the following reference guides:

-   [`references/python-pytest-cov.md`](references/python-pytest-cov.md): Detailed guide for `pytest-cov`.
-   [`references/js-c8.md`](references/js-c8.md): Detailed guide for `c8`.
-   [`references/ci-integration.md`](references/ci-integration.md): Examples for integrating coverage in CI.
-   [`references/improvement-strategies.md`](references/improvement-strategies.md): In-depth strategies for improving test coverage.
