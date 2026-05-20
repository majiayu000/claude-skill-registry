---
name: cd-pipeline-generator
description: Generate GitHub Actions deployment workflows for automated deployment to staging and production environments on cloud platforms (AWS, GCP, Azure). Use when setting up continuous deployment pipelines, creating deployment automation, or configuring multi-environment deployment strategies. Includes templates for environment-specific deployments with approval gates, secrets management, and rollback capabilities.
---

# CD Pipeline Generator

## Overview

Generate production-ready GitHub Actions deployment workflows that automate deployments to staging and production environments with environment protection rules, approval gates, and secrets management.

## Workflow

### 1. Identify Deployment Target

Determine the cloud platform and deployment method:
- **AWS**: ECS, Elastic Beanstalk, EC2, Lambda
- **GCP**: Cloud Run, App Engine, Compute Engine, Cloud Functions
- **Azure**: App Service, Container Instances, Functions

### 2. Select Template

Use the appropriate template from `assets/` based on cloud platform:
- `deploy-aws.yml` - AWS deployments (ECS, Elastic Beanstalk, Lambda)
- `deploy-gcp.yml` - GCP deployments (Cloud Run, App Engine)
- `deploy-azure.yml` - Azure deployments (App Service, Container Instances)

### 3. Configure Environments

Set up GitHub environment protection rules for staging and production:

**Staging environment**:
- Auto-deploy on merge to main/master
- No approval required
- Use staging secrets and variables

**Production environment**:
- Manual approval required
- Deploy on workflow_dispatch or tag push
- Use production secrets and variables
- Optional: Restrict to specific branches

### 4. Configure Secrets

Add required secrets to GitHub repository settings (Settings → Secrets and variables → Actions):

**AWS**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

**GCP**:
- `GCP_PROJECT_ID`
- `GCP_SERVICE_ACCOUNT_KEY`

**Azure**:
- `AZURE_CREDENTIALS`
- `AZURE_SUBSCRIPTION_ID`

### 5. Customize Deployment Steps

Adapt the template to project-specific deployment needs:

**Build artifacts**: Add build steps before deployment
```yaml
- name: Build application
  run: npm run build  # or: python -m build, go build, cargo build
```

**Docker images**: Build and push container images
```yaml
- name: Build Docker image
  run: docker build -t $IMAGE_NAME:$TAG .

- name: Push to registry
  run: docker push $IMAGE_NAME:$TAG
```

**Database migrations**: Run migrations before deployment
```yaml
- name: Run migrations
  run: npm run migrate  # or: alembic upgrade head, rails db:migrate
```

**Health checks**: Verify deployment success
```yaml
- name: Health check
  run: curl -f https://$DEPLOYMENT_URL/health || exit 1
```

### 6. Set Deployment Triggers

Configure when deployments run:

**Staging**: Auto-deploy on push to main
```yaml
on:
  push:
    branches: [main]
```

**Production**: Manual trigger or tag-based
```yaml
on:
  workflow_dispatch:
  push:
    tags:
      - 'v*'
```

### 7. Place Workflow File

Create deployment workflow at `.github/workflows/deploy.yml`. If multiple deployment workflows are needed (e.g., separate staging and production), use descriptive names:
- `.github/workflows/deploy-staging.yml`
- `.github/workflows/deploy-production.yml`

## Template Features

All templates include:
- **Environment separation**: Distinct staging and production deployments
- **Approval gates**: Production deployments require manual approval
- **Secrets management**: Secure credential handling via GitHub secrets
- **Deployment status**: Clear success/failure reporting
- **Rollback support**: Easy revert to previous versions
- **Conditional execution**: Deploy only when tests pass

## Security Best Practices

- Never commit credentials or API keys to the repository
- Use GitHub environments to scope secrets appropriately
- Enable required reviewers for production deployments
- Use OIDC authentication instead of long-lived credentials when possible
- Implement deployment windows for production (e.g., business hours only)
- Add deployment notifications to Slack/email

## Customization Examples

**Add deployment notification**:
```yaml
- name: Notify deployment
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment to ${{ github.event.inputs.environment }} ${{ job.status }}'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

**Add rollback capability**:
```yaml
- name: Rollback on failure
  if: failure()
  run: |
    echo "Deployment failed, rolling back..."
    # Platform-specific rollback commands
```

**Restrict production deployment time**:
```yaml
- name: Check deployment window
  run: |
    HOUR=$(date +%H)
    if [ $HOUR -lt 9 ] || [ $HOUR -gt 17 ]; then
      echo "Deployments only allowed 9 AM - 5 PM"
      exit 1
    fi
```

## Tips

- Start with staging deployments to validate the workflow
- Use environment-specific configuration files (e.g., `config.staging.json`, `config.production.json`)
- Implement blue-green or canary deployments for zero-downtime updates
- Add deployment metrics and monitoring
- Document rollback procedures in the repository
- Test deployment workflows in a separate test environment first
