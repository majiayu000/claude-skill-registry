---
name: unit-test-starter
description: Generate starter unit tests for a small function or module. Use when a junior developer needs test scaffolding and edge cases.
---

# Unit Test Starter

## Purpose
Generate starter unit tests for a small function or module.

## Inputs to request
- Function signature and expected behavior.
- Test framework and language.
- Edge cases or error conditions.

## Workflow
1. Identify core behaviors and failure cases from the function signature.
2. Propose table-driven cases with inputs and expected outputs.
3. Highlight one edge case and one negative case.
4. Show how to run the tests.

## Output
- Test case list with rationale.
- Sample test code snippet for the project test framework.

## Quality bar
- Keep tests deterministic and isolated.
- Prefer clear assertions over broad snapshots.
