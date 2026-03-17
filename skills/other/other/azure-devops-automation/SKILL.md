---
name: "Azure DevOps Automation"
description: "CI/CD pipelines, infrastructure as code, and deployment automation for Azure workloads"
---

# Skill: Azure DevOps Automation

> CI/CD pipelines, infrastructure as code, and deployment automation for Azure workloads.

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | azure-devops-automation |
| **Version** | 1.0.0 |
| **Category** | Cloud/Infrastructure |
| **Difficulty** | Advanced |
| **Prerequisites** | azure-architecture-patterns |
| **Related Skills** | azure-architecture-patterns, code-review |

---

## Overview

DevOps automation bridges development and operations, enabling rapid, reliable deployments. This skill covers Azure DevOps Services, GitHub Actions, and infrastructure as code patterns.

### Core Principles

| Principle | Meaning |
|-----------|---------|
| **Automate everything** | Manual steps = errors and delays |
| **Version everything** | Code, config, infrastructure—all in Git |
| **Test continuously** | Feedback at every stage |
| **Deploy frequently** | Small batches, fast recovery |
| **Monitor always** | Know before users complain |

---

## Module 1: CI/CD Pipeline Fundamentals

### Pipeline Anatomy

```yaml
# Azure DevOps YAML Pipeline
trigger:
  branches:
    include:
      - main
      - release/*

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'build'
              
  - stage: Test
    dependsOn: Build
    jobs:
      - job: TestJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'test'
              
  - stage: Deploy
    dependsOn: Test
    condition: succeeded()
    jobs:
      - deployment: DeployToDev
        environment: 'dev'
```

### Key Concepts

| Concept | Purpose |
|---------|---------|
| **Trigger** | What starts the pipeline |
| **Stage** | Major phase (Build, Test, Deploy) |
| **Job** | Unit of work on an agent |
| **Step/Task** | Individual action |
| **Environment** | Target deployment context |
| **Artifact** | Output passed between stages |

### Trigger Types

| Trigger | Use Case |
|---------|----------|
| `push` | On code push to branch |
| `pr` | On pull request |
| `schedule` | Cron-based execution |
| `pipeline` | After another pipeline completes |
| `manual` | User-initiated |

---

## Module 2: GitHub Actions

### Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run tests
        run: npm test
        
      - name: Build
        run: npm run build
```

### Useful Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout` | Clone repository |
| `actions/setup-node` | Configure Node.js |
| `actions/cache` | Cache dependencies |
| `azure/login` | Azure authentication |
| `azure/webapps-deploy` | Deploy to App Service |

### Secrets and Variables

```yaml
env:
  AZURE_WEBAPP_NAME: my-app
  
steps:
  - name: Deploy to Azure
    uses: azure/webapps-deploy@v2
    with:
      app-name: ${{ env.AZURE_WEBAPP_NAME }}
      publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

---

## Module 3: Infrastructure as Code

### Bicep Fundamentals

```bicep
// main.bicep
targetScope = 'resourceGroup'

@description('The environment name')
@allowed(['dev', 'staging', 'prod'])
param environment string

@description('The Azure region')
param location string = resourceGroup().location

var appServicePlanName = 'asp-${environment}'
var webAppName = 'app-${environment}-${uniqueString(resourceGroup().id)}'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: environment == 'prod' ? 'P1v3' : 'B1'
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
```

### Bicep Best Practices

| Practice | Rationale |
|----------|-----------|
| Use modules | Reusability, maintainability |
| Parameterize environments | Same code, different configs |
| Use `@secure()` for secrets | Prevent logging |
| Deploy with what-if | Preview changes before applying |
| Store in repo | Version control, review |

### Deployment Command

```powershell
# What-if preview
az deployment group what-if `
  --resource-group rg-myapp-dev `
  --template-file main.bicep `
  --parameters environment=dev

# Actual deployment
az deployment group create `
  --resource-group rg-myapp-dev `
  --template-file main.bicep `
  --parameters environment=dev
```

---

## Module 4: Environment Strategy

### Environment Progression

```
Dev → Staging → Production
 ↓       ↓          ↓
Auto   Manual    Approval
Deploy  Deploy    Required
```

### Azure DevOps Environments

```yaml
# With approval gates
- stage: DeployProd
  jobs:
    - deployment: DeployProduction
      environment: 'production'  # Configured with approvers
      strategy:
        runOnce:
          deploy:
            steps:
              - script: echo Deploying to production
```

### Feature Flags

Decouple deployment from release:

```csharp
// Azure App Configuration feature flags
if (await _featureManager.IsEnabledAsync("NewFeature"))
{
    // New code path
}
else
{
    // Existing behavior
}
```

---

## Module 5: Testing in Pipelines

### Test Pyramid

```
        /   E2E   \      (Few, slow, expensive)
       /───────────\
      /  Integration \   (Some, medium speed)
     /─────────────────\
    /     Unit Tests    \  (Many, fast, cheap)
   /─────────────────────\
```

### Test Tasks

```yaml
# .NET test with coverage
- task: DotNetCoreCLI@2
  inputs:
    command: 'test'
    arguments: '--collect:"XPlat Code Coverage"'
    
- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: '$(Agent.TempDirectory)/**/coverage.cobertura.xml'
```

### Quality Gates

| Gate | Threshold |
|------|-----------|
| Code coverage | ≥80% |
| Test pass rate | 100% |
| Security scan | 0 critical/high |
| Lint errors | 0 |

---

## Module 6: Secrets and Security

### Secret Management

| Method | Use Case |
|--------|----------|
| **Azure Key Vault** | Production secrets |
| **Pipeline Variables** | Build-time values |
| **GitHub Secrets** | Action credentials |
| **Azure App Configuration** | Feature flags, config |

### Key Vault Integration

```yaml
# Azure DevOps
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'Production'
    KeyVaultName: 'kv-myapp-prod'
    SecretsFilter: 'DatabaseConnectionString,ApiKey'

- script: |
    echo "Using secret from Key Vault"
    # Secret available as $(DatabaseConnectionString)
```

### Security Scanning

```yaml
# GitHub CodeQL
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: csharp, javascript

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

---

## Module 7: Monitoring and Rollback

### Deployment Monitoring

```yaml
# Health check after deployment
- script: |
    for i in {1..30}; do
      response=$(curl -s -o /dev/null -w "%{http_code}" https://myapp.azurewebsites.net/health)
      if [ "$response" = "200" ]; then
        echo "Health check passed"
        exit 0
      fi
      sleep 10
    done
    echo "Health check failed"
    exit 1
```

### Rollback Strategies

| Strategy | Implementation |
|----------|----------------|
| **Redeploy previous** | Trigger previous successful pipeline |
| **Slot swap back** | Swap staging back to production |
| **Feature flag off** | Disable problematic feature |
| **Database rollback** | Apply reverse migration |

### Blue-Green Deployment

```yaml
# Deploy to staging slot
- task: AzureWebApp@1
  inputs:
    appName: 'my-app'
    slotName: 'staging'
    
# Swap slots after validation
- task: AzureAppServiceManage@0
  inputs:
    Action: 'Swap Slots'
    SourceSlot: 'staging'
```

---

## Quick Reference

### Pipeline Checklist

- [ ] Triggers configured (push, PR, schedule)
- [ ] Build artifacts created
- [ ] Unit tests run with coverage
- [ ] Integration tests included
- [ ] Security scanning enabled
- [ ] Environment approvals configured
- [ ] Secrets in Key Vault (not pipeline)
- [ ] Health checks post-deployment
- [ ] Rollback plan documented

### Common Commands

```powershell
# Azure CLI
az login
az account set --subscription "Production"
az deployment group create --resource-group rg --template-file main.bicep

# Azure DevOps CLI
az pipelines run --name "CI-Pipeline" --branch main
az pipelines build list --top 5

# GitHub CLI
gh workflow run ci.yml
gh run list --limit 5
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not available | Check agent pool, add agents |
| Secret not found | Verify Key Vault access policy |
| Deployment timeout | Increase timeout, check health |
| Test flakiness | Isolate tests, add retries |
| Permission denied | Check service connection, RBAC |

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "CI/CD", "pipeline", "DevOps" | Full skill activation |
| "GitHub Actions", "workflow" | Module 2 |
| "Bicep", "IaC", "infrastructure as code" | Module 3 |
| "deploy", "release", "environment" | Module 4 |
| "rollback", "health check" | Module 7 |

---

*Skill created: 2026-02-10 | Category: Cloud/Infrastructure | Status: Active*
