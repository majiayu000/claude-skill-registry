---
name: test-gap-finder
description: Use when the user asks what to test next, where coverage is weak, or before a refactor of untested code. Maps source modules to existing tests, ranks untested modules by churn and size, and proposes the five highest-value tests with concrete names and cases, without writing them unasked.
---

# test-gap-finder

## Procedure
1. Detect test layout: `tests/`, `__tests__/`, `*_test.go`, `*.test.ts`, `test_*.py`, `spec/`. Detect the runner from config (`jest`, `vitest`, `pytest`, `go test`, `cargo test`).
2. Build the map: list source files (exclude generated, vendored, migrations). For each, find tests that import or name it (grep the module path/name inside test files). Result: `module | test files | test count (rough: count of test functions)`.
3. If a coverage report is cheap, run it: `pytest --cov --cov-report=term-missing -q`, `npx vitest run --coverage`, `go test -cover ./...`. Skip if it takes > 2 min or needs services.
4. Rank untested/under-tested modules by: recent churn (`git log --since=90.days --format='' --name-only | sort | uniq -c`), size (`wc -l`), and whether they sit on a critical path (auth, payments, data writes, public API).
5. For the top 5, propose tests: file path, test names, and 2 to 4 concrete cases each (happy path, boundary, failure). Reference the module's real function signatures (read the code).
6. Output a table plus the proposals. Ask before writing any test files; if approved, write them following the repo's existing test style and run them.

## Rules
- Do not claim a coverage percentage unless a coverage tool produced it.
- Do not propose tests for generated code, vendored code, or trivial getters.
- Proposed cases must be derivable from the code read in this session.

## Eval
`evals/test-gap-finder/`: fixture Python package with `auth.py` (untested, high churn), `utils.py` (tested), `payments.py` (untested); expected: auth.py and payments.py ranked top, utils.py not proposed, ≥2 concrete cases per proposal, no test files written.
