---
name: deploy-dev
description: Use when deploying code changes to dev environments (dev1-4), running terraform apply against dev, or verifying changes end-to-end. Triggers on "deploy to dev", "apply to dev2", "test in dev", "update dev environment".
---

## Dev Environment Architecture

Dev environments (dev1-4) run in the **staging** AWS account.

**Shared resources** (when `create_*` flags are `false` in tfvars):
- S3 bucket: `staging-metr-inspect-data`
- EventBridge bus: `staging-inspect-ai-api`
- EKS cluster: `staging-eks-cluster`
- ALB, VPC, subnets

**Dedicated per environment:**
- Warehouse DB: `{env_name}-inspect-ai-warehouse`
- API service: `{env_name}-inspect-ai-api`
- Lambda functions: `{env_name}-inspect-ai-*`
- ECR repos: `{env_name}/inspect-ai/*`
- CloudWatch logs

Config lives in `terraform/terraform.tfvars` (gitignored — set to your target environment before deploying).

**Note:** Commands below may require AWS credentials for the staging account. Set `AWS_PROFILE` or configure credentials as appropriate for your environment.

## Targeted Deploy

When you only changed one component:

```bash
tofu -chdir=terraform apply \
  -var-file="terraform.tfvars" -target=module.<target> -auto-approve
```

Common targets:

| Target | What It Deploys |
|--------|----------------|
| `module.eval_log_importer` | Batch job for importing eval logs to warehouse |
| `module.job_status_updated` | Lambda processing S3 events |
| `module.api` | API server (ECS Fargate) |
| `module.scan_importer` | Lambda for scan imports |
| `module.eval_log_reader` | Lambda for S3 Object Lambda access |
| `module.warehouse` | PostgreSQL Aurora database |

## Full Deploy

```bash
# Preview changes
tofu -chdir=terraform plan -var-file="terraform.tfvars"

# Apply all changes
tofu -chdir=terraform apply -var-file="terraform.tfvars"
```

### Runner Image Rebuilds

Terraform automatically tracks `uv.lock`, `pyproject.toml`, and Python source files to determine when the runner Docker image needs rebuilding (see `terraform/modules/runner/ecr.tf`). **`tofu apply` is the correct way to rebuild runner images** — it produces deterministic `sha256.<hash>` image tags.

Do NOT use `scripts/dev/build-and-push-runner-image.sh` for deploying to dev environments. That script is only for local `hawk local` testing.

### Docker Registry Authentication

Before `tofu apply` can build and push images, you must be logged into:

1. **ECR**: Install the `docker-credential-ecr-login` helper and configure Docker to use it
2. **DHI (hardened images) registry**: `docker login dhi.io`

### Lambda Lock Files

After changing Python dependencies (`pyproject.toml` or `uv.lock`), run `./scripts/dev/uv-lock-all.sh` to update lock files in ALL terraform modules. Terraform modules have their own lock files that must stay in sync with the root.

## Database Migrations

See the **`db-migrations`** skill for full details.

Quick command:

```bash
DATABASE_URL=$(tofu -chdir=terraform output \
  -var-file="terraform.tfvars" -raw warehouse_database_url_admin) \
  alembic upgrade head
```

## Verify with Smoke Tests

See the **`smoke-tests`** skill for full details.

Quick command:

```bash
unset HAWK_MODEL_ACCESS_TOKEN_ISSUER
scripts/dev/create-smoke-test-env.py env/smoke-dev2 --terraform-dir terraform
set -a && source env/smoke-dev2 && set +a && \
  pytest tests/smoke -m smoke --smoke -vv -n 5
```

## Complete Workflow

The typical deploy-and-verify loop:

1. Make code changes
2. Run local tests: `pytest tests/{package} -n auto -vv`
3. Run quality checks: `ruff check . && ruff format . --check && basedpyright .`
4. Deploy to dev: `tofu apply -target=module.X`
5. Run migrations if needed (see Database Migrations section above)
6. Run smoke tests to verify
7. Commit and push

## Choosing Between Shared and Dedicated Infrastructure

Dev environments default to reusing staging infra. To create dedicated resources, change these flags in your tfvars:

```hcl
# Shared (default for dev environments)
create_s3_bucket       = false
create_eventbridge_bus = false
create_eks_resources   = false

# Dedicated (set to true + provide unique names)
create_s3_bucket       = true
s3_bucket_name         = "dev5-metr-inspect-data"
create_eventbridge_bus = true
eventbridge_bus_name   = "dev5-inspect-ai-api"
create_eks_resources   = true
```

**Use shared** (recommended): Cheaper, simpler, sufficient for most dev work.

**Use dedicated**: When testing infrastructure changes, or when you need full isolation from other devs.

### Shared Mode Implications (create_eks_resources=false)

When using shared infrastructure, dev environments reuse staging's k8s namespace, ClusterRole, and ClusterRoleBinding. This means:

- Runner pods use the staging k8s service account and RBAC bindings
- Changes to k8s auth patterns (e.g., in-cluster config, service account permissions) must be tested in shared mode — they may work on staging (which has its own dedicated ClusterRoleBinding) but fail on dev environments that rely on staging's bindings
- The Helm chart creates a RoleBinding in the sandbox namespace only — ClusterRoleBinding for the runner namespace comes from terraform (only when `create_eks_resources=true`)

## Useful Log Groups

| Component | Log Group |
|-----------|-----------|
| API server | `{env_name}/inspect-ai/api` |
| Batch importer | `/{env_name}/inspect-ai/eval-log-importer/batch` |
| Job status Lambda | `/aws/lambda/{env_name}-inspect-ai-job-status-updated` |
| Runner pods | Use `hawk logs <eval-set-id>` |

Tail logs: `aws logs tail <log-group> --since 30m --format short`

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `tofu apply` fails with dependency cycle | Deposed resources from previous module refactors | `tofu state rm` on the orphaned resource, then re-apply |
| `exec format error` during Docker build | Building wrong architecture (e.g., arm64 instead of amd64) | Terraform handles this correctly; if building manually, specify `--platform linux/amd64` |
| Lambda can't find Docker image after apply | Docker build failed silently | Check ECR for the expected image tag; verify registry auth |
| Connection refused / timeout to dev resources | VPC routing issue — may be running in a different VPC | Check Tailscale is connected; if in a different AWS VPC, need user assistance for networking |
| `tofu apply` succeeds but runner image is stale | Using manual build script instead of terraform | Use `tofu apply` — it tracks `uv.lock` and rebuilds automatically |
