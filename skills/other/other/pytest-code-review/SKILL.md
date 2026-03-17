---
name: pytest-code-review
description: Reviews pytest test code for async patterns, fixtures, parametrize, and mocking. Use when reviewing test_*.py files, checking async test functions, fixture usage, or mock patterns.
---

# Pytest Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| async def test_*, AsyncMock, await patterns | [references/async-testing.md](references/async-testing.md) |
| conftest.py, factory fixtures, scope, cleanup | [references/fixtures.md](references/fixtures.md) |
| @pytest.mark.parametrize, DRY patterns | [references/parametrize.md](references/parametrize.md) |
| AsyncMock tracking, patch patterns, when to mock | [references/mocking.md](references/mocking.md) |

## Review Checklist

- [ ] Test functions are `async def test_*` for async code under test
- [ ] AsyncMock used for async dependencies, not Mock
- [ ] All async mocks and coroutines are awaited
- [ ] Fixtures in conftest.py for shared setup
- [ ] Fixture scope appropriate (function, class, module, session)
- [ ] Yield fixtures have proper cleanup in finally block
- [ ] @pytest.mark.parametrize for similar test cases
- [ ] No duplicated test logic across multiple test functions
- [ ] Mocks track calls properly (assert_called_once_with)
- [ ] patch() targets correct location (where used, not defined)
- [ ] No mocking of internals that should be tested
- [ ] Test isolation (no shared mutable state between tests)

## When to Load References

- Reviewing async test functions → async-testing.md
- Reviewing fixtures or conftest.py → fixtures.md
- Reviewing similar test cases → parametrize.md
- Reviewing mocks and patches → mocking.md

## Review Questions

1. Are all async functions tested with async def test_*?
2. Are fixtures properly scoped with appropriate cleanup?
3. Can similar test cases be parametrized to reduce duplication?
4. Are mocks tracking calls and used at the right locations?
