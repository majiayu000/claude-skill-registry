---
name: shared-patterns
description: 'Reference reusable patterns for validation, error handling, and test scaffolding. Use when: ensuring consistency across skills.'
version: 1.8.1
alwaysApply: false
category: meta-infrastructure
tags:
- patterns
- templates
- shared
- validation
- reusable
dependencies: []
estimated_tokens: 400
model_hint: standard
---
# Shared Patterns

Reusable patterns and templates for skill and hook development.

## Purpose

This skill provides shared patterns that are referenced by other skills in the abstract plugin. It follows DRY principles by centralizing common patterns.

## Pattern Categories

### Validation Patterns

See [modules/validation-patterns.md](modules/validation-patterns.md) for:
- Input validation templates
- Schema validation patterns
- Error reporting formats

### Error Handling

See [modules/error-handling.md](modules/error-handling.md) for:
- Exception hierarchies
- Error message formatting
- Recovery strategies

### Testing Templates

See [modules/testing-templates.md](modules/testing-templates.md) for:
- Unit test scaffolding
- Integration test patterns
- Mock fixtures

### Workflow Patterns

See [modules/workflow-patterns.md](modules/workflow-patterns.md) for:
- Checklist templates
- Feedback loop patterns
- Progressive disclosure structures

## Usage

Reference these patterns from other skills:

```markdown
For validation patterns, see the `shared-patterns` skill's
[validation-patterns](../shared-patterns/modules/validation-patterns.md) module.
```
**Verification:** Run the command with `--help` flag to verify availability.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
