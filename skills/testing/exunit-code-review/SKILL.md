---
name: exunit-code-review
description: Reviews ExUnit test code for proper patterns, boundary mocking with Mox, and test adapter usage. Use when reviewing _test.exs files or test helper configurations.
---

# ExUnit Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Async tests, setup, describe, tags | [references/exunit-patterns.md](references/exunit-patterns.md) |
| Behavior-based mocking, expectations | [references/mox-boundaries.md](references/mox-boundaries.md) |
| Bypass, Swoosh, Oban testing | [references/test-adapters.md](references/test-adapters.md) |
| What to mock vs real, Ecto sandbox | [references/integration-tests.md](references/integration-tests.md) |

## Mock Boundary Philosophy

**Mock at external boundaries:**
- HTTP clients, external APIs, third-party services
- Slow resources: file system, email, job queues
- Non-deterministic: DateTime.utc_now(), :rand

**DO NOT mock internal code:**
- Contexts, schemas, GenServers
- Internal modules, PubSub
- Anything you wrote

## Review Checklist

### Test Structure
- [ ] Tests are `async: true` unless sharing database state
- [ ] Describe-blocks group related tests
- [ ] Setup extracts common test data
- [ ] Tests have clear arrange/act/assert structure

### Mocking
- [ ] Mox used for external boundaries (HTTP, APIs)
- [ ] Behaviors defined for mockable interfaces
- [ ] No mocking of internal modules
- [ ] verify_on_exit! in setup for strict mocking

### Test Adapters
- [ ] Bypass for HTTP endpoint mocking
- [ ] Swoosh.TestAdapter for email testing
- [ ] Oban.Testing for background job assertions

### Database
- [ ] Ecto.Adapters.SQL.Sandbox for isolation
- [ ] Async tests don't share database state
- [ ] Fixtures/factories used consistently

## Valid Patterns (Do NOT Flag)

- **Mock in unit test, real in integration** - Different test levels have different needs
- **Not mocking database in integration tests** - Database is internal
- **Simple inline test data** - Not everything needs factories
- **Testing private functions via public API** - Correct approach

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| Not async | Test actually needs shared state |
| Missing mock | External call exists AND no mock/bypass |
| Mock internal | Module being mocked is internal code |

## Before Submitting Findings

Use the issue format: `[FILE:LINE] ISSUE_TITLE` for each finding.

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
