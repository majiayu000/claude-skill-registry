---
name: deployment-workflow
description: Deployment workflow for gh-pr-linear-issue-linker. Use when deploying to GCP, verifying deployments, or running tests.
---

# Deployment Workflow

## Deployment Strategy

This service uses:
- **Terraform** for infrastructure (Cloud Run, Artifact Registry, Secret Manager)
- **Google Cloud Build** for container builds (triggered automatically by Terraform)
- **Cloud Run** for serverless container hosting

## Deployment Commands

**Check code quality before deployment:**

```bash
make check
```

This runs: `ruff format` + `ruff check` + `pytest`

**Deploy to GCP:**

```bash
make deploy
# or
make tf-apply
```

This will:
1. Initialize Terraform
2. Create/update infrastructure
3. Trigger Cloud Build to build and push Docker image (only if Dockerfile changed)
4. Deploy new image to Cloud Run
5. Configure public access for GitHub webhooks

## Terraform Operations

**Initialize Terraform:**

```bash
make tf-init
# or
cd infra && terraform init
```

**Plan changes:**

```bash
make tf-plan
# or
cd infra && terraform plan
```

**Apply changes:**

```bash
make tf-apply
# or
cd infra && terraform apply
```

**View outputs:**

```bash
make tf-output
# or
cd infra && terraform output
```

## Pre-Deployment Checklist

**Always run before deployment:**

1. Check code quality:
```bash
make check
```

2. Review Terraform plan:
```bash
make tf-plan
```

3. Ensure secrets are configured in `infra/terraform.tfvars`

## Test Execution

**Run all quality checks:**

```bash
make check
```

**Run tests only:**

```bash
make test
# or
pytest
```

**Run specific test file:**

```bash
pytest tests/test_webhook.py
```

**Run with coverage:**

```bash
pytest --cov=src --cov-report=term-missing
```

## Deployment Verification

**After deployment, verify:**

1. Check Cloud Run service status:
```bash
gcloud run services describe gh-pr-linear-issue-linker \
  --region=us-central1 \
  --format=yaml
```

2. Check recent logs:
```bash
gcloud logging tail "resource.type=cloud_run_revision" \
  --limit=50
```

3. Test webhook endpoint:
```bash
curl https://YOUR-SERVICE-URL/health
```

4. Check Logfire for traces

## Results Reporting Format

```
## Deployment Summary

**Service**: gh-pr-linear-issue-linker
**Platform**: Google Cloud Run
**Status**: Success | Failed

### Build Result
- Format: Pass/Fail (ruff)
- Lint: Pass/Fail (ruff)
- Tests: X passed, Y failed (pytest)

### Deployment Result
- Terraform: Applied successfully
- Cloud Build: Build ID {build-id}
- Cloud Run: Deployed revision {revision-name}
- URL: {service-url}

### Next Steps
- Monitor Cloud Logging for errors
- Check Logfire for webhook traces
- Verify GitHub webhook deliveries
```

## Failure Handling

### Build Failures

```bash
make check
```

Check output for:
- Formatting issues: `ruff format .`
- Linting errors: `ruff check . --fix`
- Test failures: `pytest -v`

### Terraform Failures

```bash
make tf-plan
```

Review plan output for issues:
- Resource conflicts
- Missing variables in `terraform.tfvars`
- State drift
- Permission issues

### Cloud Build Failures

Check build logs:
```bash
gcloud builds list --limit=5
gcloud builds log {build-id}
```

Common issues:
- Dockerfile syntax errors
- Missing dependencies in requirements.txt
- Build timeout (increase in `cloudbuild.yaml`)

### Runtime Failures

Check Cloud Run logs:
```bash
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=50
```

Use Logfire for detailed trace analysis.

## Critical Constraints

1. **Secrets management**: Never commit secrets - use `infra/terraform.tfvars` (gitignored)
2. **Always run `make check`** before deployment
3. **Use make commands** for consistency
4. **Monitor Logfire** after deployment for errors

## Available Commands

Run `make help` to see all available commands. Key commands:
- `make check` - Format + lint + tests (run before commits)
- `make test` - Run tests only
- `make deploy` or `make tf-apply` - Deploy to GCP
- `make tf-plan` - Preview infrastructure changes
- `make tf-output` - View Terraform outputs

## Environment Variables

Secrets are managed via Secret Manager and injected into Cloud Run:

| Variable               | Purpose                        | Source         |
|------------------------|--------------------------------|----------------|
| `GITHUB_APP_ID`        | GitHub App authentication      | Secret Manager |
| `GITHUB_PRIVATE_KEY`   | GitHub App private key         | Secret Manager |
| `LINEAR_API_KEY`       | Linear API access              | Secret Manager |
| `WEBHOOK_SECRET`       | GitHub webhook signature       | Secret Manager |
| `LOGFIRE_TOKEN`        | Logfire observability          | Secret Manager |
