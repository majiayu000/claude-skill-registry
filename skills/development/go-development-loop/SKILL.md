---
name: go-development-loop
description: Follow an opinionated Go feedback loop with targeted tests, linting, local CI, security scans, dependency audits, coverage, benchmarking, generation, and migrations. Use when Codex is modifying Go code, setting up repeatable repo scripts, or tightening validation after a Go change.
---

# Go Development Loop

Run the helper scripts from the target repo root. They live under this skill's `scripts/` directory and can either be executed in place or copied into the target repo if the user wants a permanent local workflow.

## Defaults

- Prefer small, compilable changes.
- Write table-driven tests for behavior changes.
- Keep interfaces narrow.
- Use context-aware APIs and explicit error wrapping.

## Core Loop

1. Bootstrap tools if needed with `scripts/bootstrap-go-tools.sh`.
2. Run the fast loop with `scripts/test-fast.sh [base-ref]`.
3. Run the standard loop with `scripts/lint.sh`.
4. Run the full loop with `scripts/ci-local.sh`.

If a targeted test fails, isolate one failing test and switch to `$go-debug-breakpoints` or `scripts/debug-test.sh`.

## Extended Loops

- Security: `scripts/security-scan.sh` and `scripts/gosec-scan.sh`
- Dependencies: `scripts/deps-check.sh` and `scripts/deps-upgrade.sh`
- Coverage: `scripts/coverage-report.sh [threshold]`
- Performance: `scripts/bench-run.sh` and `scripts/bench-profile.sh`
- Generation: `scripts/generate.sh [path]`
- Migrations: `scripts/migrate.sh ...`
- Failure triage: `scripts/triage-failure.sh <logfile>`

## Review Rubric

Check for:

- correctness under edge cases
- concurrency safety
- error clarity and observability
- regression coverage for the changed path

## Notes

- `scripts/test-fast.sh` falls back to `./...` when it cannot find changed packages.
- `scripts/ci-local.sh` layers lint, race, coverage, and vulnerability checks.
- Use `references/command-mapping.md` to translate the original Claude plugin commands into Codex usage.
