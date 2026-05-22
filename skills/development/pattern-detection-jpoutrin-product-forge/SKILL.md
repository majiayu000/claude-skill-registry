---
name: pattern-detection
description: Auto-detects reusable patterns, best practices, and automation opportunities during implementation. Recognizes repetitive structures and generalizable solutions that could become skills.
user-invocable: false
---

# Pattern Detection Skill

Recognize and note reusable patterns during implementation for potential contribution to Product Forge.

## Purpose

When working on projects, Claude often implements patterns that could benefit the broader Product Forge ecosystem. This skill helps identify those patterns so they can be captured by the feedback hooks and potentially become new skills, commands, or templates.

## Pattern Categories

### Code Patterns

Implementations that follow consistent, reusable structures:

- **Factory patterns** - Test fixtures, mock builders, data generators
- **Service layer patterns** - Repository, command, query separation
- **Error handling** - Consistent error types, recovery strategies
- **API patterns** - Response formatting, pagination, filtering
- **Testing patterns** - Fixtures, assertions, mocking strategies

### Workflow Patterns

Multi-step processes that could be automated:

- **Project setup** - Directory structures, config files, initial scaffolding
- **Code review** - Checklists, validation steps, quality gates
- **Deployment** - Build, test, deploy sequences
- **Documentation** - Auto-generation, formatting, templates

### Configuration Patterns

Settings and configurations that are commonly needed:

- **Tool configurations** - Linter rules, formatters, CI/CD
- **Environment setup** - Development, staging, production
- **Integration patterns** - API keys, service connections

## Recognition Triggers

Note patterns when you observe:

1. **Repetition**: Same structure implemented 3+ times
2. **Best practice**: Industry-standard patterns being applied
3. **Automation opportunity**: Manual process that could be scripted
4. **Convention enforcement**: Rules applied manually that could be automated
5. **Boilerplate reduction**: Repeated code that could be templated

## Quality Criteria

Only patterns worth capturing should be:

| Criterion | Description |
|-----------|-------------|
| **Reusable** | Applies to multiple projects or contexts |
| **Non-trivial** | More than simple one-liners or obvious code |
| **Generalizable** | Not too specific to one codebase |
| **Documented** | Can be explained clearly to others |
| **Tested** | Validated in at least one real project |

## Examples of Good Patterns

### Django Model Factory Pattern
```python
# Consistent factory for test fixtures
class UserFactory:
    @classmethod
    def create(cls, **overrides):
        defaults = {"name": "Test User", "email": "test@example.com"}
        defaults.update(overrides)
        return User.objects.create(**defaults)
```
**Why it's a good pattern**: Reusable across Django projects, reduces test boilerplate, follows established factory pattern.

### API Response Wrapper
```python
# Consistent API response format
def api_response(data=None, error=None, status=200):
    return {
        "success": error is None,
        "data": data,
        "error": error,
        "timestamp": datetime.now().isoformat()
    }
```
**Why it's a good pattern**: Standardizes API responses, easy to implement, improves API consistency.

### Pre-commit Hook Configuration
```yaml
# Standard Python project pre-commit
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
```
**Why it's a good pattern**: Common Python setup, enforces code quality, easy to adapt.

## Examples of Poor Patterns

### Too Specific
```python
# Only works for this exact database schema
def get_acme_corp_users_with_subscription():
    return User.objects.filter(company="ACME", has_subscription=True)
```
**Problem**: Too specific to one project/company.

### Too Trivial
```python
# Just basic Python
def add_numbers(a, b):
    return a + b
```
**Problem**: Doesn't provide enough value to warrant a pattern.

### Incomplete
```python
# Missing error handling and edge cases
def parse_config(path):
    return json.load(open(path))
```
**Problem**: Not production-ready, would need significant expansion.

## Integration with Feedback Hooks

When you recognize a valuable pattern:

1. **Continue implementing** - Don't interrupt the user's workflow
2. **Note mentally** - The pattern will be captured at session end
3. **Be descriptive** - When discussing the implementation, explain why it's valuable

The Stop hook's Haiku analysis will detect patterns based on:
- Repeated implementations
- Best practice discussions
- "This could be reusable" mentions
- Template-like code structures

## What Becomes a Pattern

Captured patterns may become:

| Destination | When |
|-------------|------|
| **Skill** | Knowledge/guidelines that Claude applies |
| **Command** | User-invoked action or wizard |
| **Template** | Scaffolding for new projects/files |
| **Agent** | Specialized automated workflow |

## Notes

- This skill helps Claude recognize patterns, not explicitly mark them
- The feedback hooks capture patterns via AI analysis at session end
- Use `/sync-feedback` to review captured patterns
- Quality over quantity - only genuinely reusable patterns matter
