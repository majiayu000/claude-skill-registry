---
name: quality-gates
description: "Definition of done, quality verification, tech-lead review pipeline, and CI/CD integration for git-review. Use when completing tasks, reviewing code, or preparing for commit."
---

# Quality Gates

## Definition of Done

- [ ] All tests pass (`cargo test`)
- [ ] No clippy warnings (`cargo clippy -- -D warnings`)
- [ ] Code formatted (`cargo fmt --check`)
- [ ] No hardcoded paths or credentials
- [ ] Public APIs have doc comments
- [ ] Error cases handled, not ignored

## Build & Test Commands

```bash
cargo build                # Build
cargo test                 # Run all tests
cargo clippy               # Lint
cargo fmt --check          # Format check
cargo check                # Type check only
```

- ALWAYS run `cargo test` after code changes
- ALWAYS run `cargo check` before committing
- ALWAYS run `cargo clippy` before opening PRs

## Hook Testing

- After modifying any hook script in `.claude/hooks/`, run `bash tests/hooks/run_hook_tests.sh`
- When creating test files, be aware that `protect-hooks.sh` may block writes to hook-adjacent paths — if blocked, report to team lead immediately
- Ensure git test environments have `user.email` and `user.name` configured

## Agent Output Schemas

When spawning agents, expect structured output:

- **coder**: `{ files_changed: [], tests_added: [], tests_passing: bool }`
- **tech-lead**: `{ status: APPROVED|BLOCKED, critical: [], warnings: [] }`
- **reviewer**: `{ issues: [], suggestions: [], approved: bool }`
- **qa**: `{ tests_run: int, tests_passed: int, edge_cases: [] }`

## Review Pipeline

1. Coder completes implementation
2. `cargo test` + `cargo clippy` runs (hook, deterministic)
3. Tech-lead reviews code (spawned as subagent)
4. If BLOCKED → coder fixes and re-submits
5. If APPROVED → orchestrator commits
6. User reviews via `git-review` (review gate hook)

## CI/CD Integration

- GitHub Actions should run: `cargo test`, `cargo clippy`, `cargo fmt --check`
- The review gate (`git-review gate check`) can run in CI as a required check
- Hook scripts in `.claude/hooks/` are for local Claude enforcement only — not CI
- CI checks are deterministic and repeatable; hook checks add agent-specific rules
