---
description: Deploy Azure infrastructure, BFF API, and configure App Service settings
tags: [deploy, azure, infrastructure, bicep, api, app-service]
techStack: [azure, bicep, dotnet, app-service]
appliesTo: ["infrastructure/**", "deploy to azure", "deploy api", "azure deployment"]
alwaysApply: false
---

# Azure Deploy

> **Category**: Operations
> **Last Updated**: January 2026

---

## Quick Reference

| Deployment Type | Tool | Skill/Guide |
|-----------------|------|-------------|
| Azure Infrastructure | Azure CLI + Bicep | This skill |
| BFF API | Azure CLI / GitHub Actions | This skill |
| Dataverse/PCF | PAC CLI | Use `dataverse-deploy` skill |
| Solution Import | PAC CLI | Use `dataverse-deploy` skill |

**For Dataverse deployments (PCF, solutions, web resources)**: Use the `dataverse-deploy` skill instead.

---

## Prerequisites

### Required Tools

```powershell
# Verify installations
az --version          # Azure CLI 2.50+
az bicep version      # Bicep CLI 0.39+
dotnet --version      # .NET SDK 8.0+
```

### Required Access

| Resource | Access Level |
|----------|--------------|
| Azure Subscription | Contributor role |
| Azure AD | Application Administrator (for app registrations) |

### Authentication

```powershell
# Login to Azure
az login

# Set subscription
az account set --subscription "Spaarke SPE Subscription 1"

# Verify
az account show --query "{Name:name, Id:id}" -o table
```

---

## Environment Reference

### Subscriptions & Resource Groups

| Environment | Subscription | Resource Group |
|-------------|--------------|----------------|
| Dev | Spaarke SPE Subscription 1 | `spe-infrastructure-westus2` |
| Prod | (TBD) | `rg-spaarke-{customer}-prod` |

### Azure Resource Endpoints (Dev)

| Service | Endpoint |
|---------|----------|
| BFF API | `https://spe-api-dev-67e2xz.azurewebsites.net` |
| Azure OpenAI | `https://spaarke-openai-dev.openai.azure.com/` |
| AI Search | `https://spaarke-search-dev.search.windows.net/` |
| Document Intelligence | `https://westus2.api.cognitive.microsoft.com/` |
| Key Vault | `https://sprkspaarkedev-aif-kv.vault.azure.net/` |
| AI Foundry Hub | `sprkspaarkedev-aif-hub` |
| AI Foundry Project | `sprkspaarkedev-aif-proj` |

### Key Vault Secrets

| Secret Name | Purpose |
|-------------|---------|
| `openai-api-key` | Azure OpenAI API key |
| `search-admin-key` | AI Search admin key |
| `docintel-api-key` | Document Intelligence key |
| `redis-connection` | Redis connection string |
| `appinsights-key` | Application Insights key |

**Full environment reference**: See `docs/guides/AZURE-DEPLOYMENT-GUIDE.md` → Environment Configuration

---

## Deployment Type 1: Azure Infrastructure (Bicep)

### When to Use

- Creating new Azure resources
- Deploying AI Foundry stack
- Setting up customer environments

### Bicep Stack Locations

| Stack | Path | Purpose |
|-------|------|---------|
| AI Foundry | `infrastructure/bicep/stacks/ai-foundry-stack.bicep` | AI Hub, Project, Storage, KV |
| Model 1 Shared | `infrastructure/bicep/stacks/model1-shared.bicep` | Shared infrastructure |
| Model 2 Full | `infrastructure/bicep/stacks/model2-full.bicep` | Full customer deployment |

### Deploy Infrastructure

```powershell
# Navigate to infrastructure directory
cd infrastructure/bicep

# Deploy AI Foundry stack
az deployment group create `
  --resource-group spe-infrastructure-westus2 `
  --template-file stacks/ai-foundry-stack.bicep `
  --parameters customerId=spaarke environment=dev location=westus2
```

### Verify Deployment

```powershell
# List deployed resources
az resource list `
  --resource-group spe-infrastructure-westus2 `
  --output table
```

### Expected Resources (AI Foundry Stack)

| Resource Type | Name Pattern | Purpose |
|---------------|--------------|---------|
| Storage Account | `sprk{customer}{env}aifsa` | AI Foundry storage |
| Key Vault | `sprk{customer}{env}-aif-kv` | Secrets |
| Log Analytics | `sprk{customer}{env}-aif-logs` | Monitoring |
| App Insights | `sprk{customer}{env}-aif-insights` | APM |
| ML Workspace (Hub) | `sprk{customer}{env}-aif-hub` | AI Foundry Hub |
| ML Workspace (Project) | `sprk{customer}{env}-aif-proj` | AI Foundry Project |

---

## Deployment Type 2: BFF API (App Service)

### When to Use

- Deploying API code changes
- Updating App Service configuration
- Publishing new API version

### Build API

```powershell
# Build release
cd src/server/api/Sprk.Bff.Api
dotnet publish -c Release -o ./publish

# Or use publish profile
dotnet publish -c Release /p:PublishProfile=Azure
```

### Deploy to App Service

#### Option A: Azure CLI (Primary for Dev)

**Use for dev iteration** - quick deployments without committing:

```powershell
# Build and package
cd src/server/api/Sprk.Bff.Api
dotnet publish -c Release -o ./publish
Compress-Archive -Path './publish/*' -DestinationPath './publish.zip' -Force

# Deploy
az webapp deploy `
  --resource-group spe-infrastructure-westus2 `
  --name spe-api-dev-67e2xz `
  --src-path ./publish.zip `
  --type zip

# Verify deployment took effect
curl https://spe-api-dev-67e2xz.azurewebsites.net/healthz
```

#### Option B: GitHub Actions (Production Releases)

**Use for production deployments** - push to master triggers automated deployment:

```powershell
# Merge to master triggers deploy-staging.yml
git push origin master

# Monitor deployment
gh run list --workflow=deploy-staging.yml --limit 3
gh run watch
```

See `.github/workflows/deploy-staging.yml` for configuration.

#### Option C: Kudu Zip Push Deploy (Troubleshooting Fallback)

**Use when CLI deploy reports success but app still runs old code:**

1. Go to **Azure Portal** → **App Services** → `spe-api-dev-67e2xz`
2. Click **Advanced Tools** → **Go** (opens Kudu)
3. Click **Tools** → **Zip Push Deploy**
4. Drag and drop `publish.zip` onto the page
5. Verify new entry appears in **Deployment Center** logs

> **Note**: This is a rare fallback. If CLI deploys consistently fail to update the app, check Deployment Center logs first.

### Configure App Settings

```powershell
# Set individual setting
az webapp config appsettings set `
  --resource-group spe-infrastructure-westus2 `
  --name spe-api-dev-67e2xz `
  --settings Ai__Enabled=true

# Set multiple settings from file
az webapp config appsettings set `
  --resource-group spe-infrastructure-westus2 `
  --name spe-api-dev-67e2xz `
  --settings @appsettings.json
```

### Required App Settings

| Setting | Example Value |
|---------|---------------|
| `Ai__Enabled` | `true` |
| `Ai__OpenAiEndpoint` | `https://spaarke-openai-dev.openai.azure.com/` |
| `Ai__OpenAiKey` | `@Microsoft.KeyVault(...)` |
| `Ai__SummarizeModel` | `gpt-4o-mini` |
| `DocumentIntelligence__Enabled` | `true` |
| `DocumentIntelligence__AiSearchEndpoint` | `https://spaarke-search-dev.search.windows.net` |

**Full settings reference**: See `docs/guides/AZURE-DEPLOYMENT-GUIDE.md` → BFF API App Settings

---

## Deployment Type 3: Key Vault Secrets

### Store Secrets

```powershell
# Store OpenAI API key
az keyvault secret set `
  --vault-name sprkspaarkedev-aif-kv `
  --name openai-api-key `
  --value "YOUR-API-KEY"

# Store from Azure resource (auto-retrieve)
az keyvault secret set `
  --vault-name sprkspaarkedev-aif-kv `
  --name openai-api-key `
  --value "$(az cognitiveservices account keys list --name spaarke-openai-dev --resource-group spe-infrastructure-westus2 --query key1 -o tsv)"
```

### Retrieve Secrets

```powershell
# Get secret value
az keyvault secret show `
  --vault-name sprkspaarkedev-aif-kv `
  --name openai-api-key `
  --query value -o tsv
```

---

## Verification Procedures

### API Health Check

```powershell
# Check API is running
curl https://spe-api-dev-67e2xz.azurewebsites.net/healthz
# Expected: "Healthy"

curl https://spe-api-dev-67e2xz.azurewebsites.net/ping
# Expected: "pong"
```

### Azure Resource Verification

```powershell
# List resources in resource group
az resource list --resource-group spe-infrastructure-westus2 -o table

# Check specific resource
az webapp show --name spe-api-dev-67e2xz --resource-group spe-infrastructure-westus2 --query state
```

### AI Services Verification

```powershell
# Check OpenAI deployments
az cognitiveservices account deployment list `
  --name spaarke-openai-dev `
  --resource-group spe-infrastructure-westus2 `
  -o table

# Check AI Search index
az search index list `
  --service-name spaarke-search-dev `
  --resource-group spe-infrastructure-westus2 `
  -o table
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthorizationFailed` | Insufficient permissions | Verify Contributor role on subscription |
| `ResourceNotFound` | Wrong resource group or name | Check resource names in Environment Reference |
| `DeploymentFailed` | Bicep template error | Check `az deployment group show --name {deployment}` for details |
| `KeyVault access denied` | Missing Key Vault policy | Add access policy for your identity |
| `App Service 503` | API not started | Check Application Insights logs |
| `App Service 500` after deploy | DI scope mismatch or startup error | Check `/healthz` response body for error details |
| CLI deploy succeeds but old code runs | Deployment didn't register | Check Deployment Center logs; use Kudu as fallback |

### Deployment Not Taking Effect (Rare)

**Symptom**: `az webapp deploy` reports success, but the API still runs old code.

**Diagnosis**:
1. Check **Deployment Center** → **Logs** in Azure Portal
2. If no new entry with current timestamp, deployment didn't register

**Solution** (in order of preference):
1. **Restart the App Service** - sometimes forces reload of new deployment
2. **Try alternative CLI command**: `az webapp deployment source config-zip`
3. **Use Kudu Zip Push Deploy** as manual fallback (see Option C above)
4. After any method, verify with `curl https://{app}.azurewebsites.net/healthz`

**Root Cause**: This is rare and may indicate Azure-side caching or deployment slot issues. For consistent deployments, use GitHub Actions (Option A).

### Check Deployment Logs

```powershell
# API logs (streaming)
az webapp log tail --name spe-api-dev-67e2xz --resource-group spe-infrastructure-westus2

# Deployment logs
az webapp log deployment show --name spe-api-dev-67e2xz --resource-group spe-infrastructure-westus2
```

---

## Naming Conventions

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Resource Group | `rg-spaarke-{customer}-{env}` | `rg-spaarke-contoso-prod` |
| App Service | `sprk-{app}-{env}` | `sprk-bff-dev` |
| Key Vault | `sprk{customer}{env}-{purpose}-kv` | `sprkspaarkedev-aif-kv` |
| Storage Account | `sprk{customer}{env}sa` | `sprkspaarkedevsa` |
| Azure OpenAI | `spaarke-openai-{env}` | `spaarke-openai-dev` |
| AI Search | `spaarke-search-{env}` | `spaarke-search-dev` |

**Full naming conventions**: See `docs/architecture/AZURE-RESOURCE-NAMING-CONVENTION.md`

---

## Related Skills

| Skill | Use For |
|-------|---------|
| `dataverse-deploy` | Dataverse solutions, PCF controls, web resources |
| `ribbon-edit` | Ribbon customizations (uses solution export/import) |
| `ci-cd` | CI/CD pipeline status and automated deployment workflows |

---

## CI/CD Integration

### Automated Deployments via GitHub Actions

This skill documents **manual** Azure deployments. For automated deployments, see the GitHub Actions workflows:

| Workflow | Trigger | What It Deploys |
|----------|---------|-----------------|
| `deploy-staging.yml` | Auto (after CI passes on master) | API to staging App Service |
| `deploy-to-azure.yml` | Manual trigger | Infrastructure (Bicep) + API to production |

### When to Use Manual vs Automated

| Scenario | Use |
|----------|-----|
| Regular code deployments | Automated (`deploy-staging.yml` after merge to master) |
| Production deployment | Automated (`deploy-to-azure.yml` manual trigger) |
| Emergency hotfix | Manual deployment (this skill) |
| Infrastructure changes only | Manual deployment (this skill) |
| Debugging deployment issues | Manual deployment (this skill) |

### Trigger Automated Deployment

```powershell
# Trigger production deployment manually
gh workflow run deploy-to-azure.yml

# Monitor deployment progress
gh run watch

# View deployment status
gh run list --workflow=deploy-to-azure.yml --limit 5
```

### Check Deployment Status

```powershell
# View recent deployments
gh run list --workflow=deploy-to-azure.yml

# View specific run details
gh run view {run-id}

# Download deployment artifacts
gh run download {run-id}
```

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `docs/guides/AZURE-DEPLOYMENT-GUIDE.md` | Comprehensive deployment reference |
| `docs/guides/CUSTOMER-DEPLOYMENT-GUIDE.md` | Customer-facing setup guide |
| `docs/architecture/AZURE-RESOURCE-NAMING-CONVENTION.md` | Naming standards |

---

## Tips for AI

- **Avoid discovery queries** - Use endpoint values from Environment Reference above
- **Operational commands OK** - Deployments, secret management, configuration are permitted
- **For Dataverse** - Always use `dataverse-deploy` skill instead of this one
- **Check health first** - Before troubleshooting, verify `/healthz` endpoint
- **Key Vault references** - Use `@Microsoft.KeyVault(SecretUri=...)` syntax in App Settings
- **Dev deploys** - Use Azure CLI for quick dev iteration; GitHub Actions for production releases
- **Verify deployments** - After manual deploy, check `/healthz` and Deployment Center logs
- **If CLI deploy fails silently** - Try restart first, then Kudu as last resort
- **500 errors after deploy** - Check `/healthz` response body for DI scope or startup errors
