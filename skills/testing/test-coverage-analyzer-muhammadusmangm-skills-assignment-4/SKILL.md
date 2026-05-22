---
name: test-coverage-analyzer
description: Automated test coverage analysis with support for multiple testing frameworks, coverage reporting, gap identification, metric tracking, and quality gate enforcement. Use when Claude needs to analyze test coverage, identify untested code, generate coverage reports, or enforce quality standards for testing practices.
---

# Test Coverage Analyzer

## Overview
This skill provides comprehensive test coverage analysis to ensure code quality and identify areas requiring additional testing across multiple programming languages and testing frameworks.

## When to Use This Skill
- Analyzing current test coverage metrics
- Identifying untested code paths
- Generating detailed coverage reports
- Setting up quality gates for coverage thresholds
- Comparing coverage between code versions
- Identifying high-risk areas with low coverage

## Supported Testing Frameworks
- JavaScript: Jest, Mocha, Jasmine, Cypress
- Python: pytest, unittest, nose
- Java: JUnit, TestNG
- C#: NUnit, xUnit, MSTest
- Ruby: RSpec, minitest
- Go: built-in testing package
- Node.js: various testing libraries

## Coverage Metrics

### Line Coverage
- Percentage of executable lines covered
- Identification of uncovered lines
- Branch coverage analysis
- Function/method coverage

### Branch Coverage
- Conditional statement coverage
- Loop coverage analysis
- Decision point coverage
- Path coverage evaluation

### Advanced Metrics
- Statement coverage
- Condition coverage
- Modified condition/decision coverage (MCDC)
- Cyclomatic complexity correlation

## Analysis Process

### 1. Coverage Collection
- Execute tests with coverage instrumentation
- Collect coverage data from all test suites
- Aggregate coverage from multiple test runs
- Generate coverage reports in standard formats

### 2. Gap Identification
- Identify untested code blocks
- Highlight complex functions with low coverage
- Find unused code paths
- Detect dead code

### 3. Risk Assessment
- Calculate risk scores based on coverage gaps
- Prioritize areas needing attention
- Identify critical functionality with insufficient testing
- Assess change impact on test coverage

## Quality Gates
- Minimum coverage thresholds (e.g., 80% line coverage)
- Per-file coverage requirements
- New code coverage requirements (e.g., 90% for new code)
- Critical module coverage requirements

## Reporting Capabilities
- Detailed coverage reports with file-by-file breakdown
- Interactive HTML reports with clickable source code
- Coverage trend analysis over time
- Comparison reports showing coverage changes
- Risk assessment summaries

## Recommendations
- Suggest specific test cases for uncovered code
- Identify areas where mocking might improve testability
- Recommend test strategy improvements
- Highlight code that should be refactored for better testability

## Integration Points
- CI/CD pipeline integration
- Pull request status checks
- Code quality dashboards
- Team notification systems

## Standards and Best Practices
- Industry-standard coverage targets
- Framework-specific best practices
- Performance considerations for coverage tools
- Handling of generated/boilerplate code

## Scripts Available
- `scripts/run-coverage-analysis.js` - Execute coverage analysis
- `scripts/generate-report.js` - Generate detailed coverage reports
- `scripts/check-thresholds.js` - Validate coverage meets quality gates
- `scripts/compare-coverage.js` - Compare coverage between versions

## References
- `references/coverage-metrics.md` - Detailed coverage metrics and calculation methods
- `references/testing-strategies.md` - Testing strategies and coverage patterns for different test types