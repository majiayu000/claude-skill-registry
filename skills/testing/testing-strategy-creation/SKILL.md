---
name: testing-strategy-creation
description: "Generate testing strategy documentation following the TESTING-STRATEGY template. Use when planning test strategies, defining coverage targets, or when the user asks for a test plan."
event: testing-plan
auto_trigger: false
version: "1.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - feature_name
  - test_scope
  - coverage_targets
  - critical_paths
  - test_environment
output: testing_strategy_document
output_format: "Markdown testing doc (07-TESTING-STRATEGY-TEMPLATE.md)"
output_path: "docs/technical/*/testing/"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "testing-plan"
    - "feature-complete"
  conditions:
    - "user requests testing strategy"
    - "feature ready for QA"

# Validation
validation_rules:
  - "coverage targets defined"
  - "critical paths identified"
  - "test cases documented"
  - "environment requirements listed"

# Chaining
chain_after: []
chain_before: [doc-index-update]

# Agent Association
called_by: ["@QA"]
mcp_tools:
  - mcp_payment-syste_search_full_text
  - read_file
  - runTests
---

# Testing Strategy Creation Skill

> **Purpose:** Generate comprehensive testing strategy documentation. Ensures all features have proper test plans with coverage targets.

## Trigger

**When:** Feature is ready for QA OR user requests testing strategy
**Context Needed:** Feature requirements, critical paths, existing tests
**MCP Tools:** `mcp_payment-syste_search_full_text`, `read_file`, `runTests`

## Required Sections

```markdown
# [Feature] - Testing Strategy

## Scope

- In scope: ...
- Out of scope: ...

## Coverage Targets

| Component  | Target | Current |
| :--------- | :----- | :------ |
| Services   | 80%    | -       |
| Components | 70%    | -       |

## Test Types

- Unit tests
- Integration tests
- E2E tests

## Critical Paths

1. [Path description]
   - Tests: [test files]
   - Priority: High
```

## Test Case Format

```markdown
### TC-001: [Test Name]

**Type:** unit | integration | e2e
**Priority:** critical | high | medium | low

**Preconditions:**

- [condition]

**Steps:**

1. [action]
2. [action]

**Expected Result:**

- [outcome]

**Test File:** `path/to/test.spec.ts`
```

## Environment Requirements

````markdown
## Test Environment

**Dependencies:**

- PostgreSQL (test database)
- Redis (mock or real)

**Setup:**

```bash
bun run test:setup
```
````

````

**Teardown:**

```bash
bun run test:teardown
```

```

## Reference

- [07-TESTING-STRATEGY-TEMPLATE.md](/docs/templates/07-TESTING-STRATEGY-TEMPLATE.md)
- [testing.instructions.md](../instructions/testing.instructions.md)
```

```

````
