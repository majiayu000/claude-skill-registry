---
name: cui-javascript
description: Core JavaScript development standards covering ES modules, modern patterns, code quality, async programming, and tooling
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JavaScript Development Standards

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

## Overview

This skill provides comprehensive JavaScript development standards for CUI projects, covering modern JavaScript features (ES2022+), code quality practices, async programming patterns, and tooling configuration.

## Prerequisites

To effectively use this skill, you should have:

- Modern JavaScript knowledge (ES2015+, ES modules, async/await)
- Understanding of JavaScript runtime environments (browser, Node.js)
- Experience with npm and JavaScript build tools

## Standards Documents

This skill includes the following standards documents:

- **javascript-fundamentals.md** - ES modules, variables, functions, vanilla JavaScript preference, core patterns
- **code-quality.md** - Complexity limits, refactoring strategies, code organization, maintainability
- **modern-patterns.md** - Destructuring, template literals, spread/rest operators, object/array methods
- **async-programming.md** - Promises, async/await, error handling, concurrent operations
- **tooling-guide.md** - ESLint, Prettier, npm scripts, IDE integration, quality checks

## What This Skill Provides

### JavaScript Fundamentals
- **ES Modules**: Import/export syntax, module organization, circular dependency avoidance
- **Variables**: const/let best practices, no var usage, scope management
- **Functions**: Arrow functions vs regular functions, pure functions, higher-order functions
- **Vanilla JavaScript**: Preference for native APIs (fetch, DOM, etc.) over libraries

### Code Quality
- **Complexity Limits**: Cyclomatic complexity (max 15), statement count (max 20)
- **Refactoring Strategies**: Extract methods, guard clauses, early returns
- **Code Organization**: Single Responsibility Principle, function size limits
- **Maintainability**: Clear naming, documentation, avoiding magic numbers

### Modern Patterns
- **Destructuring**: Object and array destructuring patterns
- **Template Literals**: String interpolation, multi-line strings
- **Spread/Rest**: Object/array spreading, rest parameters
- **Object/Array Methods**: map, filter, reduce, find, destructive vs non-destructive

### Async Programming
- **Promises**: Creation, chaining, error handling
- **Async/Await**: Modern async patterns, try/catch best practices
- **Error Handling**: Proper error propagation, custom errors
- **Concurrent Operations**: Promise.all, Promise.race, parallel execution

### Tooling Guide
- **ESLint**: Configuration, rules, plugins
- **Prettier**: Code formatting, IDE integration
- **npm Scripts**: Development workflow, quality checks
- **Build Pipeline**: Development and production builds

## When to Activate

This skill should be activated when:

1. **JavaScript Development Tasks**: Writing or modifying JavaScript code for CUI projects
2. **Code Review**: Reviewing JavaScript code for standards compliance
3. **Refactoring**: Improving code quality, reducing complexity
4. **Modern Migration**: Updating legacy JavaScript to modern patterns
5. **Tooling Setup**: Configuring ESLint, Prettier, or build tools
6. **Async Operations**: Implementing Promise-based or async/await code
7. **Performance Optimization**: Optimizing JavaScript execution

## Workflow

When this skill is activated:

### 1. Understand Context
- Identify the specific JavaScript task or requirement
- Determine which standards documents are most relevant
- Check project-specific JavaScript configuration

### 2. Apply Standards
- Reference appropriate standards documents for guidance
- Follow ES module patterns for imports/exports
- Use const/let appropriately, avoid var
- Prefer vanilla JavaScript APIs over library dependencies
- Ensure functions meet complexity limits
- Apply modern patterns (destructuring, template literals, etc.)

### 3. Quality Assurance
- Run ESLint to check for rule violations
- Run Prettier to ensure consistent formatting
- Verify code meets complexity thresholds
- Test async operations for proper error handling
- Check for common anti-patterns

### 4. Documentation
- Document complex logic with clear comments
- Explain non-obvious patterns or workarounds
- Note any browser-specific considerations
- Update relevant documentation if adding new patterns

## Tool Access

This skill provides access to JavaScript development standards through:
- Read tool for accessing standards documents
- Standards documents use Markdown format for compatibility
- All standards are self-contained within this skill
- Cross-references between standards use relative paths

## Integration Notes

### Related Skills
For comprehensive frontend development, this skill works with:
- CSS standards (cui-css skill)
- Testing standards (to be provided in separate skill)
- Web components standards (to be provided in separate skill)

### Build Integration
JavaScript standards integrate with:
- npm for package management and scripts
- ESLint for linting and code quality
- Prettier for consistent formatting
- Maven frontend-maven-plugin for build automation

### Quality Tools
JavaScript quality is enforced through:
- ESLint for linting and best practices
- Prettier for consistent formatting
- Jest or similar for unit testing
- Browser DevTools for debugging

## Best Practices

When working with JavaScript in CUI projects:

1. **Always use ES modules** for imports/exports
2. **Prefer const over let**, never use var
3. **Use vanilla JavaScript** where possible (fetch, DOM methods, etc.)
4. **Keep functions simple** - max 15 cyclomatic complexity, max 20 statements
5. **Use modern patterns** - destructuring, template literals, spread/rest
6. **Handle async properly** - async/await with try/catch, Promise error handling
7. **Document complex logic** with clear comments
8. **Run quality tools** before committing (ESLint, Prettier)
