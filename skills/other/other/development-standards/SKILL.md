---
name: development-standards
description: Development standards and best practices. Use when development standards guidance is required.
---
## Purpose

Provide development standards and best practices that can be applied consistently across languages to improve maintainability, readability, and correctness in new and existing code.

## IO Semantics

Input: Codebases, configuration files, and development workflows that require consistent standards.

Output: Concrete naming, structure, performance, and review expectations that can be enforced via linters, CI pipelines, and manual reviews.

Side Effects: When applied, may require refactoring existing code, updating style guides, and adjusting linters or CI configurations.

## Deterministic Steps

### 1. Naming Convention Enforcement

Enforce identifier naming rules consistently:

Variables and Functions:
- Use camelCase for JavaScript/TypeScript variables and functions
- Use snake_case for Python variables and functions
- Use PascalCase for Go public functions and variables
- Use descriptive, meaningful names that reveal intent

Classes and Types:
- Use PascalCase for class names in all languages
- Use descriptive names that indicate purpose and behavior
- Avoid abbreviations unless widely understood
- Apply consistent prefixes for related concepts

Constants and Configuration:
- Use UPPER_SNAKE_CASE for constants
- Use descriptive names for configuration values
- Group related constants in logical structures
- Avoid magic numbers and string literals

Perform naming consistency validation:
- Use linters with naming convention rules
- Configure language-specific style guides
- Apply naming convention checks in CI/CD
- Enforce consistent naming across interfaces

### 2. Code Structure Principles

Apply single responsibility and modularity principles systematically:

Single Responsibility Principle:
- Each function performs one clear action
- Each class represents one concept
- Keep functions under 20 lines when possible
- Use composition over inheritance

Open/Closed Principle:
- Design for extension through interfaces
- Use abstract classes for common behavior
- Implement plugin architectures
- Avoid modifying existing code for new features

Enforce clean module boundaries and dependency management:
- Define clear interfaces between modules
- Use dependency injection for loose coupling
- Apply the dependency inversion principle
- Organize code in logical packages/modules

Module organization patterns:
- Group related functionality together
- Separate concerns into different layers
- Use consistent import/export patterns
- Implement proper abstraction levels

### 3. Performance Optimization Guidelines

Apply appropriate algorithmic complexity:
- Use O(1) for constant-time operations
- Apply O(log n) for search operations where possible
- Use O(n) for linear operations
- Avoid O(n²) algorithms for large datasets

Memory optimization techniques:
- Use appropriate data structures for the problem
- Implement object pooling for frequently created objects
- Apply streaming for large data processing
- Use lazy loading for expensive operations

### Code Performance Profiling

Implement systematic performance analysis:
- Profile critical code paths regularly
- Measure before and after optimizations
- Focus on actual bottlenecks, not premature optimization
- Document performance characteristics and limits

Performance monitoring integration:
- Add performance metrics to critical functions
- Implement benchmarking for regression detection
- Use performance budgets for new features
- Monitor production performance continuously

# Defensive Programming Implementation

## Input Validation and Error Handling

### Comprehensive Input Validation

Validate all external inputs at boundaries:
- Check for null/None/undefined values
- Validate data types and ranges
- Sanitize string inputs for security
- Implement schema validation for structured data

Boundary condition handling:
- Handle empty collections and edge cases
- Validate array indices and string lengths
- Check for numeric overflow/underflow
- Implement proper default value handling

### Robust Error Handling

Implement systematic error handling:
- Use language-specific error handling mechanisms
- Provide meaningful error messages
- Implement error recovery strategies
- Log errors with appropriate context

Exception management patterns:
- Catch specific exceptions, not general ones
- Implement custom exception types for domain errors
- Use fail-fast principles for unrecoverable errors
- Apply circuit breaker patterns for external dependencies

## Code Maintainability Standards

### Documentation and Comments

Write self-documenting code:
- Use meaningful variable and function names
- Structure code to reveal intent
- Add comments for complex business logic
- Document API contracts and invariants

Comment quality standards:
- Explain why, not what
- Keep comments current with code changes
- Use consistent comment formatting
- Avoid obvious or redundant comments

### Code Organization and Structure

Apply consistent code organization:
- Use consistent indentation and formatting
- Group related code together
- Implement proper file/module organization
- Use standard design patterns appropriately

Code readability practices:
- Keep functions focused and small
- Use meaningful variable names
- Avoid deep nesting and complex control flow
- Implement proper abstraction levels

# Quality Assurance Integration

## Code Review Standards

### Systematic Review Process

Implement comprehensive code reviews:
- Review for functionality and correctness
- Check for security vulnerabilities
- Validate performance characteristics
- Ensure adherence to coding standards

Review effectiveness metrics:
- Track defect detection rates
- Monitor review time and quality
- Collect feedback on review process
- Implement review checklists

### Automated Quality Checks

Integrate automated quality tools:
- Static analysis for bug detection
- Complexity analysis for maintainability
- Security scanning for vulnerability detection
- Performance testing for regression detection

Quality gate implementation:
- Define quality thresholds for code metrics
- Implement automated quality gates in CI/CD
- Block deployments on quality failures
- Provide actionable feedback for fixes

## Technical Debt Management

### Debt Identification and Tracking

Systematically identify technical debt:
- Track code complexity metrics
- Monitor test coverage gaps
- Identify outdated dependencies
- Document performance limitations

Technical debt prioritization:
- Assess impact on business value
- Evaluate maintenance cost implications
- Consider security and compliance requirements
- Plan debt reduction activities

### Refactoring Implementation

Apply systematic refactoring:
- Use automated refactoring tools when possible
- Maintain test coverage during refactoring
- Refactor in small, incremental steps
- Document architectural decisions and changes

Refactoring validation:
- Run comprehensive test suites after refactoring
- Validate performance characteristics
- Ensure functionality remains unchanged
- Update documentation as needed
