---
name: testing-guidelines
description: How tests should be structured, named, and prioritized in this codebase.
---

# Testing Guidelines

## Test Types

- **Unit tests**
  - Fast, isolated, no network or DB.
  - Test one behavior per test.

- **Integration tests**
  - Exercise real integrations (DB, queue, external service stubs).
  - Focus on critical paths and failure modes.

- **End-to-end (E2E) tests**
  - Cover full user journeys.
  - More expensive; keep the set small but meaningful.

## Naming & Structure

- Test files:
  - Mirror source structure: `src/foo/bar.py` → `tests/foo/test_bar.py`
- Test names:
  - Use descriptive names reflecting behavior, e.g.:
    - `def test_rejects_requests_without_authentication():`

## Coverage Expectations

- Core domain logic: ≥ 80% line coverage
- Peripheral or legacy code: best-effort; prioritize stability
- Do not chase metrics blindly; focus on risk and impact.

## Fixtures & Data

- Prefer factory functions over static fixtures.
- Make fixtures explicit and readable; avoid hidden magic.

## Testing Conventions

- Arrange-Act-Assert structure where possible.
- Avoid brittle tests that depend on:
  - Exact error messages
  - Implementation details that can change safely

## CI Requirements

- All tests must pass before merge.
- E2E tests may run on a separate pipeline if slow; document behavior.
