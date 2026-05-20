---
name: test:review
description: Review tests for quality - assertive checks, no hidden skips, proper coverage
---

# Test Review

Review test quality to ensure tests actually catch failures.

## When to Use

- After writing new tests (before committing)
- When reviewing a PR with test changes
- When tests pass but behavior seems wrong
- Periodic test suite health check

## Anti-Patterns to Catch

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `assert True` | Always passes, tests nothing | Assert specific values |
| `@pytest.mark.skip` without reason | Hides failures silently | Add reason or remove |
| `@pytest.mark.xfail` without ticket | Accepted failures without tracking | Link to issue |
| `try/except: pass` in test | Swallows errors | Let exceptions propagate |
| `assert response is not None` | Only checks existence, not correctness | Assert status code + content |
| `assert len(items) > 0` | Doesn't verify content | Assert specific items or properties |
| Empty test body | Test exists but does nothing | Implement or delete |
| Hardcoded timeouts `sleep(30)` | Flaky, slow | Use `wait_for` / retry pattern |

## Review Checklist

- [ ] **Assertive**: Every test asserts specific expected values
- [ ] **No silent skips**: `@skip` has a reason and linked issue
- [ ] **No xfail without tracking**: `@xfail` references a ticket
- [ ] **Error cases tested**: Not just happy path
- [ ] **Deterministic**: No flaky timing dependencies
- [ ] **Isolated**: Tests don't depend on execution order
- [ ] **Named clearly**: Test name describes what it verifies
- [ ] **Cleanup**: Resources created in test are cleaned up

## Review Command

Search for anti-patterns in test files:

```bash
grep -rn "assert True\|assert False\|@pytest.mark.skip\|@pytest.mark.xfail\|pass$" kagenti/tests/
```

Search for weak assertions:

```bash
grep -rn "is not None\|!= None\|assert .*>" kagenti/tests/ | grep -v "# ok"
```

## Related Skills

- `test:write` - Write new tests following standards
- `test:run-kind` - Run tests on Kind
- `test:run-hypershift` - Run tests on HyperShift
- `tdd:ci` - TDD workflow that includes test review
