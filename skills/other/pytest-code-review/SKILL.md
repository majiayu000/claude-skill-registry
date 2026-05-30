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

## Review gates

Work in order. Do not assert pytest-specific problems until each applicable gate passes.

1. **Scoped files** — **Pass when:** You list every `test_*.py` and any `conftest.py` you will cite; no findings for files outside that list.
2. **Async vs sync** — **Pass when:** Per scoped file, you note whether it uses `async def test_*` / `await`; if yes, open [references/async-testing.md](references/async-testing.md) before criticizing async usage.
3. **Fixtures** — **Pass when:** If shared setup matters, you name the `conftest.py` path(s) or state none; for yield fixtures, confirm cleanup exists before claiming resource leaks.
4. **patch / mocks** — **Pass when:** For any `patch` or mock critique, you give the import path where the symbol is **used** (call site), or mark N/A; open [references/mocking.md](references/mocking.md) when mocking is central to the review.
5. **Findings** — **Pass when:** Each finding includes a file path and line(s) or test node id, not a generic rule restatement.

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
