---
name: commit-format
description: Ensures all git commits follow the Conventional Commits specification with consistent types and scopes. Use this skill when making any commit to maintain consistent commit message format, improve git history readability, and enable automatic changelog generation.
license: MIT
metadata:
  version: "1.0.0"
  specification: "https://www.conventionalcommits.org/"
---

# Commit Message Format

All commits MUST follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Format Structure

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Format Rules

- **Type** (required): One of the types below, lowercase
- **Scope** (optional, but recommended): Area of codebase affected, lowercase, in parentheses
- **Description** (required): Short summary in imperative mood (e.g., "Add feature" not "Added feature")
- **Body** (optional): Detailed explanation, wrapped at 72 characters
- **Footer** (optional): Breaking changes or issue references

## Commit Types

- `feat`: New feature for users
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, whitespace, etc.)
- `refactor`: Code refactoring (no feature change or bug fix)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system or dependency changes
- `ci`: CI/CD configuration changes
- `chore`: Other changes (maintenance tasks, tooling, etc.)

## Common Scopes

Scopes help categorize commits by area of the codebase. Examples:

- `api`: API layer
- `auth`: Authentication/authorization
- `db`: Database related
- `ui`: User interface components
- `core`: Core business logic
- `utils`: Utility functions
- `tests`: Test files
- `docs`: Documentation
- `scripts`: Scripts and tooling
- `config`: Configuration files
- `deps`: Dependencies

**Note**: Choose scopes that match your project structure. Scopes should be lowercase and descriptive.

## Examples

### Feature Commits

```
feat(api): Add GET /health endpoint
feat(auth): Implement OAuth2 authentication
feat(ui): Add user dashboard component
feat(core): Add data validation layer
```

### Fix Commits

```
fix(api): Handle shutdown state in health endpoint
fix(db): Correct connection pool timeout
fix(ui): Fix form validation error display
fix(core): Resolve race condition in cache
```

### Documentation Commits

```
docs(readme): Update setup instructions
docs(api): Add API endpoint documentation
docs(contributing): Add contribution guidelines
```

### Test Commits

```
test(api): Add integration tests for health endpoint
test(core): Add unit tests for validation layer
test(ui): Add component rendering tests
```

### Refactoring Commits

```
refactor(core): Extract validation logic into separate module
refactor(api): Simplify error handling middleware
refactor(db): Optimize query performance
```

### Multi-scope Commits

When changes span multiple areas, use the primary scope or omit scope:

```
feat: Implement authentication with API and UI updates
fix: Resolve validation errors across core and api modules
```

### Detailed Commits (with body)

```
feat(api): Implement GET /health endpoint

- Track server start time for uptime calculation
- Track shutdown state for unhealthy status (503)
- Return status, timestamp (ISO 8601), uptime_seconds, version
- Complete within 100ms

Tests:
- Add 5 integration tests for health endpoint
- Test healthy status (200), timestamp format, uptime precision
- Test response time (<100ms), shutdown status (503)

Files:
- src/api/main.py: Add /health endpoint with state tracking
- tests/integration/api/test_health.py: Add comprehensive tests
- docs/api.md: Update API documentation
```

## Best Practices

1. **Be specific**: "Add health endpoint" is better than "Update API"
2. **Use imperative mood**: "Add feature" not "Added feature" or "Adds feature"
3. **Keep first line short**: < 72 characters when possible
4. **Include scope**: Helps categorize and filter commits
5. **Reference acceptance criteria**: Use AC-X.Y.Z format when applicable
6. **List files changed**: Especially useful for larger commits
7. **Group related changes**: One logical change per commit

## When to Use Each Type

- **feat**: New functionality that users/consumers will see or use
- **fix**: Correcting bugs or incorrect behavior
- **docs**: Only documentation (README, comments, plans, etc.)
- **test**: Only test files (new tests, test updates, test infrastructure)
- **refactor**: Code restructuring without changing behavior
- **chore**: Maintenance tasks, dependency updates, tooling changes

## Multiple Commits for Large Changes

For large features, you may make multiple commits:

```
feat(api): Implement GET /health endpoint
test(api): Add integration tests for health endpoint
docs(api): Update API documentation
```

Or combine into a single detailed commit if all changes are tightly coupled.

## Common Edge Cases

### Handling Breaking Changes

Use the `BREAKING CHANGE:` footer for breaking changes:

```
feat(api): Change response format

BREAKING CHANGE: Response now uses snake_case instead of camelCase
```

### Referencing Issues

Reference issues in the footer:

```
fix(game): Resolve validation bug

Fixes #123
```

### Combining Multiple Related Changes

When multiple related files are changed for a single feature:

```
feat(core): Add timeout handling

- Add timeout configuration to service layer
- Implement timeout enforcement with ThreadPoolExecutor
- Add fallback mechanisms for each service stage

Files:
- src/core/service.py: Core timeout logic
- tests/integration/test_service.py: Timeout tests
- docs/architecture.md: Update architecture documentation
```
