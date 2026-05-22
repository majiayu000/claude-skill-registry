---
name: tdd-workflow
description: Test-Driven Development workflow for autonomous coding. Use when implementing features with TDD, writing tests first, following red-green-refactor, or ensuring test coverage.
version: 1.0.0
category: autonomous-coding
layer: orchestration
---

# TDD Workflow

Implements Test-Driven Development workflow for feature implementation.

## Quick Start

### Run TDD Cycle
```python
from scripts.tdd_workflow import TDDWorkflow

workflow = TDDWorkflow(project_dir)
result = await workflow.implement_feature(
    feature_id="auth-001",
    acceptance_criteria=criteria
)

if result.passed:
    print("Feature implemented and verified!")
```

### Individual Phases
```python
# Red: Write failing test
test_path = await workflow.write_test(feature_id)

# Green: Implement to pass
await workflow.implement_code(feature_id)

# Refactor: Clean up
await workflow.refactor(feature_id)
```

## TDD Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                      TDD CYCLE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│      ┌─────────────────────────────────────────┐           │
│      │                                         │           │
│      │            1. RED                       │           │
│      │     Write failing test                  │           │
│      │     Test must fail                      │           │
│      │                                         │           │
│      └───────────────────┬─────────────────────┘           │
│                          │                                  │
│                          ▼                                  │
│      ┌─────────────────────────────────────────┐           │
│      │                                         │           │
│      │            2. GREEN                     │           │
│      │     Write minimal code                  │           │
│      │     to pass test                        │           │
│      │                                         │           │
│      └───────────────────┬─────────────────────┘           │
│                          │                                  │
│                          ▼                                  │
│      ┌─────────────────────────────────────────┐           │
│      │                                         │           │
│      │            3. REFACTOR                  │           │
│      │     Improve code quality                │           │
│      │     Keep tests passing                  │           │
│      │                                         │           │
│      └───────────────────┬─────────────────────┘           │
│                          │                                  │
│                          ▼                                  │
│      ┌─────────────────────────────────────────┐           │
│      │                                         │           │
│      │         4. VERIFY (E2E)                 │           │
│      │     Run acceptance tests                │           │
│      │     Confirm feature works               │           │
│      │                                         │           │
│      └─────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## TDD Principles

| Principle | Description |
|-----------|-------------|
| **Tests First** | Always write tests before implementation |
| **Minimal Code** | Write only enough code to pass tests |
| **Small Steps** | Make incremental changes |
| **Fast Feedback** | Run tests frequently |
| **Refactor Often** | Keep code clean |

## Test Types

| Type | Purpose | When to Write |
|------|---------|---------------|
| **Unit** | Test individual functions | RED phase |
| **Integration** | Test component interaction | After GREEN |
| **E2E** | Test full feature flow | VERIFY phase |

## Integration Points

- **coding-agent**: Executes TDD workflow
- **browser-e2e-tester**: Runs E2E tests
- **error-recoverer**: Handle test failures
- **progress-tracker**: Track test metrics

## References

- `references/TDD-BEST-PRACTICES.md` - Best practices
- `references/TEST-PATTERNS.md` - Common patterns

## Scripts

- `scripts/tdd_workflow.py` - Main workflow
- `scripts/test_writer.py` - Generate tests
- `scripts/test_runner.py` - Run tests
- `scripts/refactor_helper.py` - Refactoring tools
