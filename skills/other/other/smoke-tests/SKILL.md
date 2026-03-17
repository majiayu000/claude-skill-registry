---
name: smoke-tests
description: Use when running smoke tests, debugging smoke test failures, or verifying a deployed environment works correctly. Triggers on "run smoke tests", "smoke tests failing", "test against dev", "verify deployment".
---

## Prerequisites

1. **Login**: `hawk login` (stores OAuth2 tokens in keyring — shared across all environments, only need to do this once)
2. **AWS credentials**: Ensure credentials are configured for the target environment (e.g., set `AWS_PROFILE` if needed)
3. **Unset overrides**: `unset HAWK_MODEL_ACCESS_TOKEN_ISSUER` (if previously set)

**After any `tofu apply`**: You MUST regenerate the smoke env file. Terraform outputs change (image tags, URLs, etc.) and stale env files will cause confusing failures.

## Running Smoke Tests

### 1. Generate Environment File

For **dev environments** (dev1-4, using this repo's terraform):

```bash
unset HAWK_MODEL_ACCESS_TOKEN_ISSUER
scripts/dev/create-smoke-test-env.py env/smoke-dev2 --terraform-dir terraform
```

For **staging** (using the separate deploy repo):

```bash
unset HAWK_MODEL_ACCESS_TOKEN_ISSUER
scripts/dev/create-smoke-test-env.py env/smoke-staging --terraform-dir ../mp4-deploy/terraform_inspect
```

**Note:** `create-smoke-test-env.py` reads Terraform outputs, which may require AWS credentials.

### 2. Run Tests

```bash
# Using uv (outside virtual environment):
set -a && source env/smoke-<env> && set +a && \
  uv run pytest tests/smoke -m smoke --smoke -vv -n 5

# Already in virtual environment:
set -a && source env/smoke-<env> && set +a && \
  pytest tests/smoke -m smoke --smoke -vv -n 5
```

Or using `--env-file` (avoids polluting your shell):

```bash
uv run --env-file env/smoke-<env> pytest tests/smoke -m smoke --smoke -vv -n 5
```

- Use `-n 5` for dev environments (middleman can't handle more concurrent requests)
- Use `-n 10` for staging

**Important**: The hawk CLI reads `HAWK_API_URL` from the process environment — it does NOT auto-load `.env` files. You must either source the env file or use `--env-file`.

### 3. Run a Single Test

```bash
# Using uv:
set -a && source env/smoke-<env> && set +a && \
  uv run pytest tests/smoke/test_outcomes.py::test_model_roles --smoke -vv

# Already in virtual environment:
set -a && source env/smoke-<env> && set +a && \
  pytest tests/smoke/test_outcomes.py::test_model_roles --smoke -vv
```

## Auth Model

Smoke tests use **two separate auth mechanisms**:

- **API calls** (eval set submission, log viewer, sample edits): OAuth2 bearer tokens from keyring (`hawk login`)
- **Warehouse database**: IAM authentication via AWS credentials — this is why AWS access must be configured even though you already logged in

## Troubleshooting

### Before You Debug: Verify the Basics

When smoke tests fail, check these FIRST before investigating further:

1. **Env file regenerated?** If you ran `tofu apply` since the last env file generation, regenerate it now
2. **Correct environment sourced?** Run `echo $HAWK_API_URL` — does it point to the right environment?
3. **Network connectivity?** Ensure Tailscale is connected. If you're running in a different AWS VPC than the target environment (e.g., running in production VPC but targeting staging), you'll need to resolve network routing — ask for help
4. **Logged in?** `hawk auth access-token > /dev/null && echo OK` — if this fails, run `hawk login`

### Common Errors

| Issue | Cause | Fix |
|-------|-------|-----|
| `500 Internal Server Error` on `POST /eval_sets/` | Middleman timeout under concurrent load | Reduce workers (`-n 5`) or retry |
| `PAM authentication failed` for warehouse | Missing AWS credentials for IAM auth | Ensure correct AWS profile is active (e.g., `export AWS_PROFILE=staging`) |
| `RuntimeError: HAWK_API_URL not set` | Missing env file | Run `create-smoke-test-env.py` |
| All eval sets end in `error` status | Runner pods failing silently | `hawk logs <eval-set-id>` — read the actual error message |
| `Helm install failed: ... is forbidden` | k8s RBAC issue — service account missing permissions | Check ClusterRoleBinding exists for the runner service account |
| `TimeoutError` waiting for sample in warehouse | Eval-log-importer batch job failing | Check batch logs (see below) |
| `TimeoutError` waiting for eval set completion | Runner pod issue | `hawk logs <eval-set-id>` |
| `ValueError: refresh_token not found` | Not logged in | `hawk login` |
| Tests submit but API has zero logs | Smoke tests hitting wrong API endpoint | Verify `HAWK_API_URL` — env may not be sourced correctly |

### Debugging Approach

**ALWAYS find root cause before attempting fixes.** When investigating failures:

1. **Read error messages literally** — don't skip past errors to guess at causes. If Helm says "configmaps is forbidden", the issue IS permissions, not something else
2. **Gather evidence before forming hypotheses** — check logs, pod status, env vars before proposing a fix
3. **Verify one thing at a time** — don't change multiple things and re-test

### When Samples Don't Appear in Warehouse

This means the eval completed but the import pipeline failed. The investigation path is:

S3 → EventBridge → Lambda → Batch → DB

See `docs/solutions/smoke-test-failures/investigating-batch-import-failures.md` for the full debugging guide with commands for each stage.

## Related Skills and Docs

- **`deploy-dev`** skill: Deploy code changes to dev environments before running smoke tests
- **`db-migrations`** skill: Run migrations against dev warehouse DBs (often needed after deploying schema changes)
- **`docs/solutions/smoke-test-failures/`**: Detailed investigation writeups for specific failure patterns
