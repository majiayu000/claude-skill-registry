---
name: quality-standards
description: Defines code quality benchmarks, standards compliance, and best practices for maintaining high-quality codebases
version: 1.0.0
---

## Overview

This skill provides standards and benchmarks for code quality including linting rules, formatting standards, naming conventions, and quality thresholds across programming languages.

## Quality Score Thresholds

- **Excellent**: 90-100
- **Good**: 70-89
- **Acceptable**: 50-69
- **Needs Improvement**: Below 50

## Language-Specific Standards

### Python
- **PEP 8**: Style guide for Python code
- **Type Hints**: Use for public APIs
- **Docstrings**: Google or NumPy style
- **Line Length**: Max 88-100 characters (Black standard)

### JavaScript/TypeScript
- **ESLint**: Use recommended config + project rules
- **Prettier**: For consistent formatting
- **Naming**: camelCase for variables, PascalCase for classes
- **TypeScript**: Enable strict mode

## Quality Components

1. **Tests Passing** (30%): All tests must pass
2. **Standards Compliance** (25%): Linting/formatting adherence
3. **Documentation** (20%): Complete docstrings/comments
4. **Pattern Adherence** (15%): Follow established patterns
5. **Code Metrics** (10%): Complexity and duplication

## When to Apply

Use when validating code quality, enforcing standards, or setting quality benchmarks for projects.
