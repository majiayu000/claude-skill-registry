# CI/CD Automation Skill

**Purpose:** Design and implement continuous integration and continuous deployment pipelines using GitHub Actions for Azure deployments.

**When to use:** Creating deployment automation, setting up build pipelines, implementing deployment strategies.

**Agents who use this:** DevOps/Platform Engineering Agent

---

## GitHub Actions Workflow Patterns

### 1. Continuous Integration (CI) - Build, Test, Scan

**`.github/workflows/ci.yml`:**
```yaml
name: CI - Build, Test, Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
          isort --check-only .
      
      - name: Run tests with coverage
        env:
          DJANGO_SETTINGS_MODULE: config.settings.test
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Semgrep security scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            p/django
      
      - name: Run dependency security scan
        run: |
          pip install safety pip-audit
          safety check --json || true
          pip-audit --desc || true
      
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
```

### 2. Deploy to Staging (Automatic on Merge to Main)

**`.github/workflows/deploy-staging.yml`:**
```yaml
name: Deploy to Staging

on:
  push:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'
  AZURE_WEBAPP_NAME: 'app-myapp-staging'
  RESOURCE_GROUP: 'rg-myapp-staging-swedencentral'

jobs:
  deploy-infrastructure:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy Bicep template
        uses: azure/arm-deploy@v1
        with:
          subscriptionId: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          resourceGroupName: ${{ env.RESOURCE_GROUP }}
          template: ./infrastructure/bicep/main.bicep
          parameters: ./infrastructure/bicep/parameters/parameters.staging.json
          failOnStdErr: false
      
      - name: Get infrastructure outputs
        id: infra
        run: |
          APP_NAME=$(az deployment group show \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --name main \
            --query properties.outputs.appServiceName.value \
            --output tsv)
          echo "app_name=$APP_NAME" >> $GITHUB_OUTPUT

  deploy-database:
    needs: deploy-infrastructure
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run database migrations
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
          DJANGO_SETTINGS_MODULE: config.settings.staging
        run: |
          python manage.py migrate --noinput

  deploy-application:
    needs: [deploy-infrastructure, deploy-database]
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          package: .
      
      - name: Run smoke tests
        run: |
          curl -f https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net/health || exit 1
      
      - name: Notify on success
        if: success()
        run: |
          echo "✅ Staging deployment successful!"
      
      - name: Notify on failure
        if: failure()
        run: |
          echo "❌ Staging deployment failed!"
```

### 3. Deploy to Production (Manual Approval)

**`.github/workflows/deploy-production.yml`:**
```yaml
name: Deploy to Production

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy (e.g., v1.2.3)'
        required: true

env:
  PYTHON_VERSION: '3.11'
  AZURE_WEBAPP_NAME: 'app-myapp-prod'
  RESOURCE_GROUP: 'rg-myapp-prod-swedencentral'

jobs:
  approval:
    runs-on: ubuntu-latest
    environment: production  # Requires approval in GitHub Settings
    
    steps:
      - name: Waiting for approval
        run: echo "Waiting for production deployment approval..."

  backup-database:
    needs: approval
    runs-on: ubuntu-latest
    
    steps:
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Create database backup
        run: |
          az postgres flexible-server backup create \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --server-name psql-myapp-prod \
            --backup-name "pre-deploy-${{ github.inputs.version }}"

  deploy-to-slot:
    needs: [approval, backup-database]
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.inputs.version }}
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to staging slot
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: staging
          package: .
      
      - name: Run database migrations on staging slot
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
          DJANGO_SETTINGS_MODULE: config.settings.production
        run: |
          python manage.py migrate --noinput
      
      - name: Smoke test staging slot
        run: |
          curl -f https://${{ env.AZURE_WEBAPP_NAME }}-staging.azurewebsites.net/health || exit 1
          sleep 30  # Wait for warmup
          curl -f https://${{ env.AZURE_WEBAPP_NAME }}-staging.azurewebsites.net/api/v1/health || exit 1

  swap-slots:
    needs: deploy-to-slot
    runs-on: ubuntu-latest
    
    steps:
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Swap staging to production
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --slot staging \
            --target-slot production
      
      - name: Verify production
        run: |
          sleep 10
          curl -f https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net/health || exit 1
      
      - name: Notify on success
        if: success()
        run: |
          echo "✅ Production deployment successful! Version: ${{ github.inputs.version }}"
      
      - name: Rollback on failure
        if: failure()
        run: |
          echo "❌ Production deployment failed! Rolling back..."
          az webapp deployment slot swap \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --slot production \
            --target-slot staging
```

---

## GitHub Secrets Configuration

### Required Secrets

Configure in GitHub: **Settings > Secrets and variables > Actions**

```yaml
# Azure credentials (service principal)
AZURE_CREDENTIALS:
  {
    "clientId": "<service-principal-app-id>",
    "clientSecret": "<service-principal-password>",
    "subscriptionId": "<azure-subscription-id>",
    "tenantId": "<azure-tenant-id>"
  }

AZURE_SUBSCRIPTION_ID: <subscription-id>

# Database connection strings (per environment)
STAGING_DATABASE_URL: postgresql://user:pass@server/db
PROD_DATABASE_URL: postgresql://user:pass@server/db

# Django secret keys (per environment)
STAGING_DJANGO_SECRET_KEY: <random-key>
PROD_DJANGO_SECRET_KEY: <random-key>

# Optional: Semgrep token for enhanced scanning
SEMGREP_APP_TOKEN: <semgrep-token>
```

### Creating Azure Service Principal

```bash
# Create service principal with Contributor role
az ad sp create-for-rbac \
  --name "github-actions-myapp" \
  --role Contributor \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth

# Output (copy to AZURE_CREDENTIALS secret):
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "...",
  "resourceManagerEndpointUrl": "...",
  "activeDirectoryGraphResourceId": "...",
  "sqlManagementEndpointUrl": "...",
  "galleryEndpointUrl": "...",
  "managementEndpointUrl": "..."
}
```

---

## Deployment Strategies

### 1. Blue-Green Deployment (Using Deployment Slots)

```yaml
# Deploy to staging slot (green)
- name: Deploy to staging slot
  uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ env.AZURE_WEBAPP_NAME }}
    slot-name: staging
    package: .

# Test staging slot
- name: Test staging slot
  run: |
    curl -f https://${APP_NAME}-staging.azurewebsites.net/health

# Swap staging to production (instant cutover)
- name: Swap to production
  run: |
    az webapp deployment slot swap \
      --resource-group ${{ env.RESOURCE_GROUP }} \
      --name ${{ env.AZURE_WEBAPP_NAME }} \
      --slot staging \
      --target-slot production
```

**Benefits:**
- Zero downtime
- Instant rollback (swap back)
- Test in production-like environment

### 2. Canary Deployment (Traffic Routing)

```yaml
# Deploy to staging slot
# Route 10% of traffic to staging slot
- name: Route 10% traffic to staging
  run: |
    az webapp traffic-routing set \
      --resource-group ${{ env.RESOURCE_GROUP }} \
      --name ${{ env.AZURE_WEBAPP_NAME }} \
      --distribution staging=10

# Monitor for 30 minutes
- name: Monitor canary
  run: |
    sleep 1800  # 30 minutes
    # Check error rates, latency, etc.

# If successful, route 100% traffic
- name: Complete canary rollout
  run: |
    az webapp deployment slot swap \
      --resource-group ${{ env.RESOURCE_GROUP }} \
      --name ${{ env.AZURE_WEBAPP_NAME }} \
      --slot staging
```

### 3. Rolling Deployment (Multiple Instances)

```yaml
# For apps with multiple instances
# Azure automatically does rolling updates
- name: Deploy with rolling update
  uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ env.AZURE_WEBAPP_NAME }}
    package: .
    # Azure deploys to instances one at a time
```

---

## Testing in CI/CD

### Unit and Integration Tests

```yaml
- name: Run tests
  env:
    DJANGO_SETTINGS_MODULE: config.settings.test
    DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
  run: |
    pytest \
      --cov=. \
      --cov-report=xml \
      --cov-report=term \
      --junit-xml=test-results.xml \
      -v

- name: Publish test results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: test-results.xml
```

### Smoke Tests

```yaml
- name: Smoke test deployment
  run: |
    # Health check
    curl -f https://${APP_URL}/health || exit 1
    
    # API availability
    curl -f https://${APP_URL}/api/v1/health || exit 1
    
    # Database connectivity (via API)
    curl -f https://${APP_URL}/api/v1/db-check || exit 1
```

### Load Testing (Optional)

```yaml
- name: Run load tests
  run: |
    pip install locust
    locust -f loadtest.py --headless --users 100 --spawn-rate 10 --run-time 2m --host https://${APP_URL}
```

---

## Rollback Procedures

### Automated Rollback on Failure

```yaml
- name: Deploy to production
  id: deploy
  uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ env.AZURE_WEBAPP_NAME }}
    package: .

- name: Verify deployment
  id: verify
  run: |
    sleep 30
    curl -f https://${APP_URL}/health || exit 1

- name: Rollback on failure
  if: failure() && steps.deploy.outcome == 'success'
  run: |
    echo "Deployment verification failed, rolling back..."
    az webapp deployment slot swap \
      --resource-group ${{ env.RESOURCE_GROUP }} \
      --name ${{ env.AZURE_WEBAPP_NAME }} \
      --slot production \
      --target-slot staging
```

### Manual Rollback Workflow

**`.github/workflows/rollback-production.yml`:**
```yaml
name: Rollback Production

on:
  workflow_dispatch:
    inputs:
      target_version:
        description: 'Version to rollback to (e.g., v1.2.2)'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.inputs.target_version }}
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy previous version
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: staging
          package: .
      
      - name: Swap to production
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --slot staging
```

---

## Best Practices

### 1. Secrets Management
- ✅ Store secrets in GitHub Secrets, not in code
- ✅ Use separate secrets per environment
- ✅ Rotate secrets regularly
- ✅ Use Azure Key Vault for production secrets

### 2. Environment Separation
- ✅ Separate workflows for staging and production
- ✅ Require manual approval for production deployments
- ✅ Use GitHub Environments for protection rules

### 3. Testing
- ✅ Run tests on every push
- ✅ Block merges if tests fail
- ✅ Require code review before merging
- ✅ Run security scans (Semgrep, dependency scanning)

### 4. Deployment Safety
- ✅ Always backup database before production deployment
- ✅ Use deployment slots for zero-downtime deployments
- ✅ Run smoke tests after deployment
- ✅ Have automated rollback on failure

### 5. Monitoring
- ✅ Monitor deployment success/failure
- ✅ Alert on failed deployments
- ✅ Track deployment frequency and lead time
- ✅ Monitor application health after deployment

### 6. Documentation
- ✅ Document deployment process in README
- ✅ Include rollback procedures
- ✅ Maintain changelog (CHANGELOG.md)
- ✅ Tag releases in Git

---

## Troubleshooting

### Issue: Azure Login Fails

```
Error: Authentication failed
Solution: Verify service principal has correct permissions
```

```bash
# Check service principal
az ad sp show --id <client-id>

# Grant Contributor role
az role assignment create \
  --assignee <client-id> \
  --role Contributor \
  --scope /subscriptions/<subscription-id>
```

### Issue: Deployment Fails with "Package not found"

```
Solution: Ensure all required files are in repository
Check: .gitignore is not excluding necessary files
```

### Issue: Database Migration Fails

```
Solution: Verify DATABASE_URL secret is correct
Check: Database allows connections from GitHub Actions IP
```

---

## CI/CD Checklist

Before merging CI/CD workflows:

- [ ] GitHub Secrets configured
- [ ] Azure service principal created with correct permissions
- [ ] Bicep templates validated
- [ ] Parameter files created for all environments
- [ ] Tests passing locally
- [ ] Security scans configured (Semgrep)
- [ ] Deployment slots created (for production)
- [ ] Database backup configured
- [ ] Smoke tests implemented
- [ ] Rollback procedures tested
- [ ] Documentation updated
- [ ] Team notified of deployment process

---

**Remember:** CI/CD is about **confidence** and **speed**. Automate everything, test thoroughly, and always have a rollback plan.
