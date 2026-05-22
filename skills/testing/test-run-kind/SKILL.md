---
name: test:run-kind
description: Run E2E tests on local Kind cluster
---

# Run Tests on Kind

> **Auto-approved**: All test execution on Kind is auto-approved.

## When to Use

- Running E2E tests locally on Kind
- Quick validation before pushing to CI
- Debugging test failures with live cluster

## Run All Tests

```bash
./.github/scripts/local-setup/kind-full-test.sh --include-test
```

## Run Specific Tests

```bash
./.github/scripts/local-setup/kind-full-test.sh --include-test --pytest-filter "test_agent"
```

## Run with pytest Directly

```bash
uv run pytest kagenti/tests/e2e/ -v -k "test_agent_simple_query"
```

## Run from Worktree

```bash
.worktrees/my-feature/.github/scripts/local-setup/kind-full-test.sh --include-test
```

## Environment

| Variable | Value |
|----------|-------|
| Agent URL | `http://localhost:8000` (port-forward) |
| Keycloak | `http://keycloak.localtest.me:8080` |
| MLflow | Disabled in Kind |

## Related Skills

- `test:run-hypershift` - Run on HyperShift (includes MLflow tests)
- `test:review` - Review test quality
- `tdd:kind` - Full TDD loop on Kind
- `kind:cluster` - Create/destroy Kind cluster
