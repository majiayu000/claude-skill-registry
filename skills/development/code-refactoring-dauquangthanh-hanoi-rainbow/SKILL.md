---
name: code-refactoring
description: Guides systematic code refactoring to improve code quality, maintainability, and design. Identifies code smells, applies refactoring patterns, ensures test coverage, and follows safe refactoring practices. Produces cleaner, more maintainable code while preserving functionality. Use when improving code quality, eliminating technical debt, preparing for feature additions, addressing code smells, or when users mention refactoring, code cleanup, improving design, reducing complexity, or modernizing legacy code.
---

# Code Refactoring

## Overview

This skill guides systematic code refactoring to improve code quality, maintainability, and design while preserving functionality. Follow the safe refactoring workflow with comprehensive test coverage and incremental changes.

## Refactoring Workflow

## Step 1: Analyze Code and Identify Issues

Examine the codebase to identify code smells and quality issues:

- Long methods (>20-30 lines) or large classes (>300-500 lines)
- Duplicated code blocks or similar logic in multiple places
- Unclear or misleading names for variables, methods, or classes
- Complex conditional logic or deeply nested structures
- Poor separation of concerns or tight coupling between components

**For detailed code smell catalog**: See [code-smells.md](references/code-smells.md)

### Step 2: Verify Test Coverage

Before refactoring ANY code:

1. Check existing test coverage for the code to be refactored
2. If tests are missing or inadequate, write tests FIRST
3. Run all tests to establish baseline (all should pass)
4. Never proceed without adequate test coverage

**For test coverage strategies**: See [testing-strategies.md](references/testing-strategies.md)

### Step 3: Choose Refactoring Technique

Select the appropriate refactoring pattern based on the issue:

- **Extract Method/Function**: Break down long methods into smaller, focused ones
- **Extract Class**: Split large classes with multiple responsibilities
- **Rename**: Improve clarity with better names
- **Move Method/Field**: Relocate functionality to more appropriate classes
- **Replace Conditional with Polymorphism**: Simplify complex conditionals
- **Introduce Parameter Object**: Group related parameters
- **Inline Method/Variable**: Remove unnecessary indirection

**For complete pattern catalog**: See [refactoring-patterns.md](references/refactoring-patterns.md)

### Step 4: Apply Refactoring Incrementally

Make ONE small change at a time:

1. Apply a single refactoring technique
2. Run all tests immediately after the change
3. If tests pass, commit the change
4. If tests fail, revert and try a different approach
5. Repeat for each refactoring needed

**Critical Rules:**

- Never change behavior while refactoring
- Never refactor and add features simultaneously
- Use IDE automated refactoring tools when available
- Keep each refactoring commit small and focused

**For detailed process guidance**: See [refactoring-process.md](references/refactoring-process.md)

### Step 5: Verify and Document

After completing refactorings:

1. Run full test suite to ensure all tests pass
2. Check that code quality metrics improved
3. Review code to confirm readability enhanced
4. Document significant architectural changes if needed
5. Create clear commit messages describing refactorings

## Common Refactoring Scenarios

**Scenario-specific guidance** is available for:

- Legacy code modernization
- Preparing code for new features
- Performance optimization through refactoring
- Reducing technical debt systematically
- Extracting reusable components

See [common-refactoring-scenarios.md](references/common-refactoring-scenarios.md) for detailed examples and approaches.

## Best Practices and Quality Guidelines

Follow established principles for high-quality refactoring:

- Apply SOLID principles (Single Responsibility, Open/Closed, etc.)
- Reduce coupling between components
- Increase cohesion within components
- Eliminate duplication (DRY principle)
- Maintain consistent coding standards

**For comprehensive best practices**: See [refactoring-best-practices.md](references/refactoring-best-practices.md)

## Tools and Automation

Modern IDEs and tools can automate many refactorings safely:

- IDE refactoring features (IntelliJ, VS Code, Visual Studio)
- Static analysis tools for code smell detection
- Test coverage tools
- Automated code formatting and linting

**For tool recommendations and usage**: See [tools-and-automation.md](references/tools-and-automation.md)

## Output Format

When presenting refactoring recommendations:

1. Identify the code smell or quality issue
2. Explain why it's problematic
3. Propose specific refactoring approach
4. Show before/after code examples
5. List tests to verify behavior preservation

**For detailed output templates**: See [output-format.md](references/output-format.md)
