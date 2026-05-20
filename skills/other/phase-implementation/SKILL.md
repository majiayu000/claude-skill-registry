---
name: phase-implementation
description: Guides implementation of features following an established workflow pattern. Use when implementing any feature to ensure consistent process: read requirements, create todos, implement code, write tests, update documentation, commit and push.
license: MIT
metadata:
  version: "1.0.0"
  workflow: "requirements -> todos -> code -> tests -> update docs -> commit"
---

# Feature Implementation Pattern

This skill defines the standard workflow for implementing features from your project's requirements or implementation plan.

## Implementation Workflow

### 1. Read Requirements

- Locate the feature/requirement in your project documentation
- Understand the requirements, acceptance criteria, and test coverage expectations
- Identify files to create/modify
- Note any specification references

### 2. Create TODO List

Use `todo_write` tool to track implementation tasks:

```python
todo_write(merge=False, todos=[
    {'id': 'feature_implementation', 'content': 'Implement feature X', 'status': 'in_progress'},
    {'id': 'feature_tests', 'content': 'Write tests for feature X', 'status': 'pending'},
    {'id': 'feature_docs', 'content': 'Update documentation', 'status': 'pending'}
])
```

### 3. Implement Code

- Create/modify source files as specified
- Follow project conventions (type hints, docstrings, error codes)
- Use established patterns and models
- Implement error handling with custom error codes
- Add necessary imports

### 4. Write Tests

Follow the test-writing pattern:
- Write incremental tests first (for development)
- Then verify acceptance criteria
- Use descriptive test names
- Add type annotations: `-> None`
- Test both success and error cases

### 5. Run Quality Checks

Before marking complete:
- Run linters: `ruff` and `black`
- Run type checker: `mypy --strict --explicit-package-bases src/`
- Run tests: `pytest tests/ -v`
- **Ensure all tests pass** before proceeding
- Fix any issues

### 6. Update Documentation

Update project documentation:

- Mark feature as complete in relevant docs
- Add **Implementation Notes** section with key details
- Update test coverage documentation
- Update acceptance criteria status
- Update any API or user documentation

### 7. Commit and Push

**Only commit after all tests pass and quality checks succeed.**

Follow commit format conventions:

```
feat(<scope>): Implement <feature name>

- [List of key implementations]
- [Key features added]

Tests:
- [List of tests added]

Files:
- [List of files changed with descriptions]
```

**Important**: Only commit after:
- ✅ All tests pass (`pytest tests/ -v`)
- ✅ Linters pass (`ruff` and `black`)
- ✅ Type checker passes (`mypy`)
- ✅ Documentation updated
- ✅ Feature verified to work correctly

After committing, push to GitHub automatically.

## Feature Types

### Core Business Logic

- Implement domain models and business rules
- Add validators for data integrity
- Write comprehensive unit tests
- Target: 100% coverage on core logic

### Service Layer

- Implement service logic
- Write comprehensive unit tests
- Test all edge cases and error scenarios
- Target: ≥90% coverage on services

### API Endpoints

- Follow API endpoint implementation patterns
- Create REST routes
- Write integration tests with test client
- Verify acceptance criteria

### UI Components

- Implement user interface components
- Write component tests
- Test user interactions and state management
- Verify accessibility and responsiveness

## Common Patterns

### Error Handling

- Use consistent error codes
- Return appropriate result wrappers with error codes
- Return HTTP status codes for API endpoints
- Follow error handling patterns

### Test Organization

- Unit tests: `tests/unit/<module>/test_<component>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- API tests: `tests/integration/api/test_<endpoint>.py`

### File Structure

- Source files: Follow project structure conventions
- Test files mirror source structure
- Follow naming conventions (snake_case for Python)

## Best Practices

1. **Read implementation plan**: Always read `docs/implementation-plan.md` first to understand requirements, acceptance criteria, and test specifications
2. **Track internally**: Use TODO list for internal progress tracking (this is your internal mechanism, not part of the spec)
3. **Test-driven**: Write tests as specified in the implementation plan - tests are called out in the plan with specific acceptance criteria
4. **One at a time**: Only implement one section/sub-phase at a time. Wait for explicit user command before proceeding to the next section/sub-phase.
5. **Verify AC**: Ensure all acceptance criteria from the plan are met
6. **Update plan**: Mark features complete in `docs/implementation-plan.md` immediately after implementation
7. **Commit frequently**: Commit after each completed sub-phase, then push to GitHub

## Edge Cases

### When Implementation Differs from Plan

- Update the plan to reflect actual implementation
- Document deviations in **Implementation Notes**
- Ensure acceptance criteria are still met

### When Tests Reveal Issues

- Fix issues in code before marking complete
- Update plan if requirements change
- Document lessons learned

### When Multiple Files Need Updates

- Group related changes in single commit
- Use detailed commit message with file list
- Ensure all tests pass before committing
