---
name: test:run-hypershift
description: Run E2E tests on HyperShift cluster
---

# Run Tests on HyperShift

> **Auto-approved**: All test execution on hosted HyperShift clusters is auto-approved.

## When to Use

- Running full E2E tests including MLflow, Phoenix, auth
- Validating before merging to main
- Testing OpenShift-specific features

## Run All Tests

```bash
KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-$CLUSTER/auth/kubeconfig \
  ./.github/scripts/local-setup/hypershift-full-test.sh $CLUSTER --include-test
```

## Run Specific Tests

```bash
KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-$CLUSTER/auth/kubeconfig \
  ./.github/scripts/local-setup/hypershift-full-test.sh $CLUSTER \
  --include-test --pytest-filter "test_agent or test_mlflow"
```

## Run from Worktree

```bash
KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-$CLUSTER/auth/kubeconfig \
  .worktrees/$WORKTREE/.github/scripts/local-setup/hypershift-full-test.sh $CLUSTER \
  --include-test --pytest-filter "test_agent"
```

## Test Categories

| Filter | Tests | Notes |
|--------|-------|-------|
| `test_agent` | Agent conversation tests | Needs LLM (OpenAI) |
| `test_mlflow` | MLflow traces, auth | HyperShift only |
| `test_agent or test_mlflow` | Both (recommended) | Traces need fresh agent calls |

## Related Skills

- `test:run-kind` - Run on Kind (faster, no MLflow)
- `test:review` - Review test quality
- `tdd:hypershift` - Full TDD loop on HyperShift
- `hypershift:cluster` - Create cluster if needed
