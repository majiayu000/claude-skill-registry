---
name: deployment
description: Serverless deployment with zero-downtime, multi-environment strategies, and infrastructure validation. Use when deploying Lambda functions, managing environments, or troubleshooting deployment failures.
---

# Deployment Skill

**Tech Stack**: AWS Lambda, Docker, Terraform, GitHub Actions, Doppler (secrets)

**Source**: Extracted from CLAUDE.md deployment principles and production deployment patterns.

---

## When to Use This Skill

Use the deployment skill when:
- ✓ Deploying Lambda functions to AWS
- ✓ Managing multi-environment deployments (dev/staging/production)
- ✓ Implementing zero-downtime deployments
- ✓ Troubleshooting deployment failures
- ✓ Validating infrastructure configuration
- ✓ Setting up CI/CD pipelines
- ✓ Pre-deployment validation (see [lambda-deployment checklist](../../checklists/lambda-deployment.md))

**DO NOT use this skill for:**
- ✗ Local development setup (use project README instead)
- ✗ Running tests (use testing-workflow skill)
- ✗ Code refactoring (use refactor skill)

**Quick Links**:
- **Pre-deployment checklist**: [lambda-deployment.md](../../checklists/lambda-deployment.md) - Systematic verification before deploying Lambda
- **Error investigation**: [error-investigation skill](../error-investigation/) - AWS-specific troubleshooting
- **Testing workflow**: [testing-workflow skill](../testing-workflow/) - Docker-based testing for deployment fidelity

---

## Quick Deployment Decision Tree

```
What are you deploying?
├─ Lambda function update?
│  ├─ Code change only? → Update function code, wait for update
│  ├─ Config change (env vars, memory)? → Update configuration, wait
│  ├─ Zero-downtime required? → Use versioning + alias pattern
│  └─ Rollback needed? → Point alias to previous version
│
├─ New environment?
│  ├─ Branch-based (dev/staging/prod)? → Follow multi-env guide
│  ├─ Secrets setup? → Configure Doppler + GitHub secrets
│  └─ Infrastructure? → Terraform apply
│
├─ Deployment failed?
│  ├─ Check CloudWatch logs → Filter ERROR level
│  ├─ Validate secrets → Run validation script
│  ├─ Check resource state → AWS CLI describe commands
│  └─ Verify permissions → IAM policy validation
│
└─ CI/CD pipeline setup?
   ├─ Define environments → dev/staging/prod
   ├─ Configure artifact promotion → Immutable images
   ├─ Add validation gates → Pre-deploy checks
   └─ Setup monitoring → CloudWatch + smoke tests
```

---

## Core Deployment Patterns

### Pattern 1: Zero-Downtime Lambda Deployment

**Problem:** Updating Lambda function causes brief unavailability during deployment.

**Solution:** Version + Alias pattern

```
$LATEST (mutable, testing)
   ↓ publish version
Version N (immutable snapshot)
   ↓ update alias
live (production pointer) → Version N
```

**Benefits:**
- Zero downtime (alias swap is atomic)
- Instant rollback (point alias to previous version)
- Test before promotion ($LATEST → Version)

See [ZERO_DOWNTIME.md](ZERO_DOWNTIME.md) for detailed patterns.

### Pattern 2: Multi-Environment Strategy

**Branch-Based Deployment:**

```
dev branch → dev environment (~8 min)
    ↓ PR
main branch → staging environment (~10 min)
    ↓ Tag v*.*.*
production environment (~12 min)
```

**Artifact Promotion:**
- Build once in dev
- Same immutable Docker image promoted to staging/prod
- What you test is what you deploy

See [MULTI_ENV.md](MULTI_ENV.md) for environment separation patterns.

> **Note**: Deployment verification applies **Progressive Evidence Strengthening** (CLAUDE.md Principle #2). We verify from weak evidence (exit codes) to strong evidence (actual traffic metrics).

### Pattern 3: Deployment Validation

**Multi-Layer Verification (Deployment Application):**

1. **Status Code** (weakest signal)
   ```bash
   aws lambda invoke --function-name worker --payload '{}' /tmp/response.json
   # Exit code 0 only means "invocation succeeded", not "function worked"
   ```

2. **Response Payload** (stronger signal)
   ```bash
   if grep -q "errorMessage" /tmp/response.json; then
     echo "❌ Lambda returned error"
     exit 1
   fi
   ```

3. **CloudWatch Logs** (strongest signal)
   ```bash
   ERROR_COUNT=$(aws logs filter-log-events \
     --log-group-name /aws/lambda/worker \
     --filter-pattern "ERROR" \
     --query 'length(events)' --output text)

   if [ "$ERROR_COUNT" -gt 0 ]; then
     echo "❌ Found errors in logs"
     exit 1
   fi
   ```

**Principle:** AWS services returning 200 OK doesn't guarantee error-free execution. Always validate logs.

See [MONITORING.md](MONITORING.md) for comprehensive validation patterns.

### Pattern 4: Secret Management by Consumer

**Doppler (Runtime Secrets)**
- Who needs it: Lambda functions during execution
- Examples: `AURORA_HOST`, `OPENROUTER_API_KEY`
- Access: Doppler → Terraform → Lambda env vars

**GitHub Secrets (Deployment Secrets)**
- Who needs it: CI/CD pipeline during deployment
- Examples: `CLOUDFRONT_DISTRIBUTION_ID`, `AWS_ACCESS_KEY_ID`
- Access: `${{ secrets.SECRET_NAME }}` in workflows

**The Deciding Question:** "Does the Lambda function running in production need this value?"
- YES → Doppler (runtime secret)
- NO → GitHub Secrets (deployment secret)

See [MULTI_ENV.md#secret-management](MULTI_ENV.md#secret-management) for detailed patterns.

---

## Pre-Deployment Validation

**Principle:** Validate configuration BEFORE deployment, not during.

### Validation Script

```bash
# Run before every deployment
scripts/validate_deployment_ready.sh

# Checks:
# 1. Doppler configuration exists
# 2. Required environment variables set
# 3. AWS resources exist (S3 buckets, DynamoDB tables)
# 4. Lambda function dependencies available
```

**Why This Matters:**
- Distinguishes config failures from logic failures
- Fails fast (30 seconds vs 8 minute deploy)
- Prevents partial deployments

### Infrastructure-Deployment Contract Validation

**Pattern:** Query AWS infrastructure, validate secrets match reality.

```yaml
jobs:
  validate-deployment-config:
    runs-on: ubuntu-latest
    steps:
      - name: Validate CloudFront Distributions
        run: |
          # Query actual infrastructure
          ACTUAL=$(aws cloudfront list-distributions \
            --query 'DistributionList.Items[?Comment==`app-dev`].Id' \
            --output text)

          # Compare to GitHub secret
          if [ "$ACTUAL" != "${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}" ]; then
            echo "❌ Secret mismatch detected"
            exit 1
          fi

  build:
    needs: validate-deployment-config  # Won't run if validation fails
```

**Benefits:**
- Catches configuration drift automatically
- No manual checklist needed
- Single source of truth (AWS infrastructure is reality)

See [MONITORING.md#infrastructure-validation](MONITORING.md#infrastructure-validation).

---

## Common Deployment Scenarios

### Scenario 1: Deploy Code Change to Dev

```bash
# 1. Commit to dev branch
git add .
git commit -m "feat: Add new feature"
git push origin dev

# 2. GitHub Actions automatically:
#    - Builds Docker image
#    - Pushes to ECR
#    - Updates Lambda function code
#    - Waits for function update (no sleep!)
#    - Runs smoke tests
#    - Validates CloudWatch logs

# 3. Manual verification (optional)
just test-dev-api  # Test deployed function
```

**Time:** ~8 minutes

### Scenario 2: Promote Dev → Staging

```bash
# 1. Create PR from dev → main
gh pr create --base main --head dev --title "Release: v1.2.0"

# 2. Review and merge
gh pr merge --squash

# 3. GitHub Actions automatically:
#    - Uses SAME Docker image from dev (artifact promotion)
#    - Updates staging Lambda with promoted image
#    - Runs integration tests
#    - Validates staging environment
```

**Time:** ~10 minutes (faster because no rebuild)

### Scenario 3: Deploy to Production

```bash
# 1. Tag release on main branch
git tag v1.2.0
git push origin v1.2.0

# 2. GitHub Actions automatically:
#    - Uses SAME Docker image from staging
#    - Publishes new Lambda version (immutable)
#    - Updates 'live' alias to new version (zero-downtime)
#    - Runs smoke tests
#    - Validates production logs
```

**Time:** ~12 minutes

### Scenario 4: Rollback Production

```bash
# Find previous version
aws lambda list-versions-by-function \
  --function-name worker \
  --query 'Versions[-2].Version'  # Previous version

# Update alias to previous version (instant rollback)
aws lambda update-alias \
  --function-name worker \
  --name live \
  --function-version 42  # Previous working version

# Verify rollback
aws lambda get-alias --function-name worker --name live
```

**Time:** < 30 seconds (instant)

---

## Deployment Principles

**From CLAUDE.md global instructions:**
> "Deployment Philosophy: Serverless AWS Lambda with immutable container images, zero-downtime promotion via versioning."

### Core Principles

1. **Immutability**: Build once, promote same artifact through all environments
2. **Zero-Downtime**: Version + Alias pattern for atomic updates
3. **Fail Fast**: Validate before deployment, not during
4. **Multi-Layer Verification**: Status code + Payload + Logs
5. **Artifact Promotion**: Dev image → Staging image → Prod image (same hash)
6. **Secret Separation**: Runtime secrets (Doppler) vs Deployment secrets (GitHub)

### When NOT to Deploy

- ❌ Tests failing (run `just test-deploy` first)
- ❌ Secrets not configured (run validation script)
- ❌ Infrastructure not created (run `terraform apply` first)
- ❌ No PR review for staging/prod (require approval)

### AWS CLI Waiter Pattern

**DO:**
```bash
aws lambda update-function-code --function-name worker --image-uri $IMAGE
aws lambda wait function-updated --function-name worker  # Blocks until ready
```

**DON'T:**
```bash
aws lambda update-function-code --function-name worker --image-uri $IMAGE
sleep 30  # ❌ Arbitrary delay, might be too short or too long
```

**Why Waiters:**
- Precise timing (returns immediately when ready)
- Handles variability (cold start vs warm container)
- Prevents race conditions

---

## File Organization

```
.claude/skills/deployment/
├── SKILL.md                       # This file (entry point)
├── ZERO_DOWNTIME.md               # Lambda versioning patterns
├── MULTI_ENV.md                   # Environment strategy
├── MONITORING.md                  # Validation and monitoring
└── scripts/
    └── validate_deployment_ready.sh  # Pre-deployment validation
```

---

## Next Steps

- **For zero-downtime patterns**: See [ZERO_DOWNTIME.md](ZERO_DOWNTIME.md)
- **For multi-environment setup**: See [MULTI_ENV.md](MULTI_ENV.md)
- **For deployment monitoring**: See [MONITORING.md](MONITORING.md)
- **For complete runbook**: See `docs/deployment/TELEGRAM_DEPLOYMENT_RUNBOOK.md`

---

## References

- [AWS Lambda Versioning and Aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
- [AWS CLI Waiters](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-wait.html)
- [Doppler Documentation](https://docs.doppler.com/)
- [GitHub Actions: AWS Credentials](https://github.com/aws-actions/configure-aws-credentials)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
