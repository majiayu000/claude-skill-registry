---
name: adf-master
description: Comprehensive Azure Data Factory knowledge base with official documentation sources, CI/CD methods, deployment patterns, and troubleshooting resources
---

# Azure Data Factory Master Knowledge Base

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation



---

This skill provides comprehensive reference information about Azure Data Factory, including official documentation sources, CI/CD deployment methods, and troubleshooting resources. Use this to access detailed ADF knowledge on-demand.

## 🚨 CRITICAL 2025 UPDATE: Deprecated Features### Apache Airflow Workflow Orchestration Manager - DEPRECATED**Status:** Available only for existing customers as of early 2025**Retirement Date:** Not yet announced, but feature is officially deprecated**Impact:** New customers cannot provision Apache Airflow in Azure Data Factory**Official Deprecation Notice:**- Apache Airflow Workflow Orchestration Manager is deprecated with no retirement date set- Only existing deployments can continue using this feature- No new Airflow integrations can be created in ADF**Migration Path:**- **Recommended:** Migrate to Fabric Data Factory with native Airflow support- **Alternative:** Use standalone Apache Airflow deployments (Azure Container Instances, AKS, or VM-based)- **Alternative:** Migrate orchestration logic to native ADF pipelines with control flow activities**Why Deprecated:**- Microsoft focus shifted to Fabric Data Factory as the unified data integration platform- Fabric provides modern orchestration capabilities superseding Airflow integration- Limited adoption and maintenance burden for standalone Airflow feature in ADF**Action Required:**- If using Airflow in ADF: Plan migration within 12-18 months- For new projects: Do NOT use Airflow in ADF - use Fabric or native ADF patterns- Monitor Microsoft announcements for official retirement timeline**Reference:**- Microsoft Roadmap: https://www.directionsonmicrosoft.com/roadmaps/ref/azure-data-factory-roadmap/## 🆕 2025 Feature Updates### Microsoft Fabric Integration (GA June 2025)**ADF Mounting in Fabric:**- Bring existing ADF pipelines into Fabric workspaces without rebuilding- General Availability as of June 2025- Seamless integration enables hybrid ADF + Fabric workflows**Cross-Workspace Pipeline Orchestration:**- New **Invoke Pipeline** activity supports cross-platform calls- Invoke pipelines across Fabric, Azure Data Factory, and Synapse- Managed VNet support for secure cross-workspace communication**Variable Libraries:**- Environment-specific variables for CI/CD automation- Automatic value substitution during workspace promotion- Eliminates separate parameter files per environment**Connector Enhancements:**- ServiceNow V2 (V1 End of Support)- Enhanced PostgreSQL and Snowflake connectors- Native OneLake connectivity for zero-copy integration### Node.js 20.x Requirement for CI/CD**CRITICAL:** As of 2025, npm package `@microsoft/azure-data-factory-utilities` requires Node.js 20.x**Breaking Change:**- Older Node.js versions (14.x, 16.x, 18.x) may cause package incompatibility errors- Update CI/CD pipelines to use Node.js 20.x or compatible versions**GitHub Actions:**```yaml- name: Setup Node.js  uses: actions/setup-node@v4  with:    node-version: '20.x'```**Azure DevOps:**```yaml- task: UseNode@1  inputs:    version: '20.x'```

## 🚨 CRITICAL 2025 UPDATE: Deprecated Features

### Apache Airflow Workflow Orchestration Manager - DEPRECATED

**Status:** Available only for existing customers as of early 2025
**Retirement Date:** Not yet announced, but feature is officially deprecated
**Impact:** New customers cannot provision Apache Airflow in Azure Data Factory

**Official Deprecation Notice:**
- Apache Airflow Workflow Orchestration Manager is deprecated with no retirement date set
- Only existing deployments can continue using this feature
- No new Airflow integrations can be created in ADF

**Migration Path:**
- **Recommended:** Migrate to Fabric Data Factory with native Airflow support
- **Alternative:** Use standalone Apache Airflow deployments (Azure Container Instances, AKS, or VM-based)
- **Alternative:** Migrate orchestration logic to native ADF pipelines with control flow activities

**Why Deprecated:**
- Microsoft focus shifted to Fabric Data Factory as the unified data integration platform
- Fabric provides modern orchestration capabilities superseding Airflow integration
- Limited adoption and maintenance burden for standalone Airflow feature in ADF

**Action Required:**
- If using Airflow in ADF: Plan migration within 12-18 months
- For new projects: Do NOT use Airflow in ADF - use Fabric or native ADF patterns
- Monitor Microsoft announcements for official retirement timeline

**Reference:**
- Microsoft Roadmap: https://www.directionsonmicrosoft.com/roadmaps/ref/azure-data-factory-roadmap/

## 🆕 2025 Feature Updates

### Microsoft Fabric Integration (GA June 2025)

**ADF Mounting in Fabric:**
- Bring existing ADF pipelines into Fabric workspaces without rebuilding
- General Availability as of June 2025
- Seamless integration enables hybrid ADF + Fabric workflows

**Cross-Workspace Pipeline Orchestration:**
- New **Invoke Pipeline** activity supports cross-platform calls
- Invoke pipelines across Fabric, Azure Data Factory, and Synapse
- Managed VNet support for secure cross-workspace communication

**Variable Libraries:**
- Environment-specific variables for CI/CD automation
- Automatic value substitution during workspace promotion
- Eliminates separate parameter files per environment

**Connector Enhancements:**
- ServiceNow V2 (V1 End of Support)
- Enhanced PostgreSQL and Snowflake connectors
- Native OneLake connectivity for zero-copy integration

### Node.js 20.x Requirement for CI/CD

**CRITICAL:** As of 2025, npm package `@microsoft/azure-data-factory-utilities` requires Node.js 20.x

**Breaking Change:**
- Older Node.js versions (14.x, 16.x, 18.x) may cause package incompatibility errors
- Update CI/CD pipelines to use Node.js 20.x or compatible versions

**GitHub Actions:**
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20.x'
```

**Azure DevOps:**
```yaml
- task: UseNode@1
  inputs:
    version: '20.x'
```

## Official Documentation Sources

### Primary Microsoft Learn Resources

**Main Documentation Hub:**
- URL: https://learn.microsoft.com/en-us/azure/data-factory/
- Last Updated: February 2025
- Coverage: Complete ADF documentation including tutorials, concepts, how-to guides, and reference materials
- Key Topics: Pipelines, datasets, triggers, linked services, data flows, integration runtimes, monitoring

**Introduction to Azure Data Factory:**
- URL: https://learn.microsoft.com/en-us/azure/data-factory/introduction
- Summary: Managed cloud service for complex hybrid ETL, ELT, and data integration projects
- Key Features: 90+ built-in connectors, serverless architecture, code-free UI, single-pane monitoring

### Context7 Library Documentation

**Library ID:** `/websites/learn_microsoft_en-us_azure_data-factory`
- Trust Score: 7.5
- Code Snippets: 10,839
- Topics: CI/CD, ARM templates, pipeline patterns, data flows, monitoring, troubleshooting

**How to Access:**
```
Use Context7 MCP tool to fetch latest documentation:
mcp__context7__get-library-docs:
  - context7CompatibleLibraryID: /websites/learn_microsoft_en-us_azure_data-factory
  - topic: "CI/CD continuous integration deployment pipelines ARM templates"
  - tokens: 8000
```

## CI/CD Deployment Methods

### Modern Automated Approach (Recommended)

**npm Package:** `@microsoft/azure-data-factory-utilities`
- **Latest Version:** 1.0.3+ (check npm for current version)
- **npm URL:** https://www.npmjs.com/package/@microsoft/azure-data-factory-utilities
- **Node.js Requirement:** Version 20.x or compatible

**Key Features:**
- Validates ADF resources independently of service
- Generates ARM templates programmatically
- Enables true CI/CD without manual publish button
- Supports preview mode for selective trigger management

**package.json Configuration:**
```json
{
  "scripts": {
    "build": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index",
    "build-preview": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index --preview"
  },
  "dependencies": {
    "@microsoft/azure-data-factory-utilities": "^1.0.3"
  }
}
```

**Commands:**
```bash
# Validate resources
npm run build validate <rootFolder> <factoryId>

# Generate ARM templates
npm run build export <rootFolder> <factoryId> [outputFolder]

# Preview mode (only stop/start modified triggers)
npm run build-preview export <rootFolder> <factoryId> [outputFolder]
```

**Official Documentation:**
- URL: https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery-improvements
- Last Updated: January 2025
- Topics: Setup, configuration, build commands, CI/CD integration

### Traditional Manual Approach (Legacy)

**Method:** Git integration + Publish button

**Process:**
1. Configure Git integration in ADF UI (Dev environment only)
2. Make changes in ADF Studio
3. Click "Publish" button to generate ARM templates
4. Templates saved to `adf_publish` branch
5. Release pipelines deploy from `adf_publish` branch

**When to Use:**
- Migrating from existing setup
- No build pipeline infrastructure
- Simple deployments without validation

**Limitations:**
- Requires manual publish action
- No validation until publish
- Not true CI/CD (manual step required)
- Can't validate on pull requests

**Migration Path:** Modern approach recommended for new implementations

## ARM Template Deployment

### PowerShell Deployment

**Primary Command:** `New-AzResourceGroupDeployment`

**Syntax:**
```powershell
New-AzResourceGroupDeployment `
  -ResourceGroupName "<resource-group-name>" `
  -TemplateFile "ARMTemplateForFactory.json" `
  -TemplateParameterFile "ARMTemplateParametersForFactory.<environment>.json" `
  -factoryName "<factory-name>" `
  -Mode Incremental `
  -Verbose
```

**Validation:**
```powershell
Test-AzResourceGroupDeployment `
  -ResourceGroupName "<resource-group-name>" `
  -TemplateFile "ARMTemplateForFactory.json" `
  -TemplateParameterFile "ARMTemplateParametersForFactory.<environment>.json" `
  -factoryName "<factory-name>"
```

**What-If Analysis:**
```powershell
New-AzResourceGroupDeployment `
  -ResourceGroupName "<resource-group-name>" `
  -TemplateFile "ARMTemplateForFactory.json" `
  -TemplateParameterFile "ARMTemplateParametersForFactory.<environment>.json" `
  -factoryName "<factory-name>" `
  -WhatIf
```

### Azure CLI Deployment

**Primary Command:** `az deployment group create`

**Syntax:**
```bash
az deployment group create \
  --resource-group <resource-group-name> \
  --template-file ARMTemplateForFactory.json \
  --parameters ARMTemplateParametersForFactory.<environment>.json \
  --parameters factoryName=<factory-name> \
  --mode Incremental
```

**Validation:**
```bash
az deployment group validate \
  --resource-group <resource-group-name> \
  --template-file ARMTemplateForFactory.json \
  --parameters ARMTemplateParametersForFactory.<environment>.json \
  --parameters factoryName=<factory-name>
```

**What-If Analysis:**
```bash
az deployment group what-if \
  --resource-group <resource-group-name> \
  --template-file ARMTemplateForFactory.json \
  --parameters ARMTemplateParametersForFactory.<environment>.json \
  --parameters factoryName=<factory-name>
```

## PrePostDeploymentScript

### Current Version: Ver2

**Location:** https://github.com/Azure/Azure-DataFactory/blob/main/SamplesV2/ContinuousIntegrationAndDelivery/PrePostDeploymentScript.Ver2.ps1

**Key Improvement in Ver2:**
- Turns off/on ONLY triggers that have been modified
- Ver1 stopped/started ALL triggers (slower, more disruptive)
- Compares trigger payloads to determine changes

**Download Command:**
```bash
# Linux/macOS/Git Bash
curl -o PrePostDeploymentScript.Ver2.ps1 https://raw.githubusercontent.com/Azure/Azure-DataFactory/main/SamplesV2/ContinuousIntegrationAndDelivery/PrePostDeploymentScript.Ver2.ps1

# PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Azure/Azure-DataFactory/main/SamplesV2/ContinuousIntegrationAndDelivery/PrePostDeploymentScript.Ver2.ps1" -OutFile "PrePostDeploymentScript.Ver2.ps1"
```

### Parameters

**Pre-Deployment (Stop Triggers):**
```powershell
./PrePostDeploymentScript.Ver2.ps1 `
  -armTemplate "<path-to-ARMTemplateForFactory.json>" `
  -ResourceGroupName "<resource-group-name>" `
  -DataFactoryName "<factory-name>" `
  -predeployment $true `
  -deleteDeployment $false
```

**Post-Deployment (Start Triggers & Cleanup):**
```powershell
./PrePostDeploymentScript.Ver2.ps1 `
  -armTemplate "<path-to-ARMTemplateForFactory.json>" `
  -ResourceGroupName "<resource-group-name>" `
  -DataFactoryName "<factory-name>" `
  -predeployment $false `
  -deleteDeployment $true
```

### PowerShell Requirements

**Version:** PowerShell Core (7.0+) recommended
- Azure DevOps: Use `pwsh: true` in AzurePowerShell@5 task
- Locally: Use `pwsh` command, not `powershell`

**Modules Required:**
- Az.DataFactory
- Az.Resources

**Official Documentation:**
- URL: https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery-sample-script
- Last Updated: January 2025

## GitHub Actions CI/CD

### Official Resources

**Medium Article (Recent 2025):**
- URL: https://medium.com/microsoftazure/azure-data-factory-build-and-deploy-with-new-ci-cd-flow-using-github-actions-cd46c95054e0
- Author: Jared Zagelbaum (Microsoft Azure)
- Topics: Modern CI/CD flow, npm package usage, GitHub Actions setup

**Microsoft Community Hub:**
- URL: https://techcommunity.microsoft.com/blog/fasttrackforazureblog/azure-data-factory-cicd-with-github-actions/3768493
- Topics: End-to-end GitHub Actions setup, workload identity federation

**Community Blog (February 2025):**
- URL: https://linusdata.blog/2025/03/14/automating-azure-data-factory-deployments-with-github-actions/
- Topics: Practical implementation guide, troubleshooting tips

### Key GitHub Actions

**Essential Actions:**
- `actions/checkout@v4` - Checkout repository
- `actions/setup-node@v4` - Setup Node.js
- `actions/upload-artifact@v4` - Publish ARM templates
- `actions/download-artifact@v4` - Download ARM templates in deploy workflow
- `azure/login@v2` - Authenticate to Azure
- `azure/arm-deploy@v2` - Deploy ARM templates
- `azure/powershell@v2` - Run PrePostDeploymentScript

### Authentication Methods

**Service Principal (JSON credentials):**
```json
{
  "clientId": "<GUID>",
  "clientSecret": "<STRING>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>"
}
```
Store in GitHub secret: `AZURE_CREDENTIALS`

**Workload Identity Federation (More secure):**
- No secrets stored
- Uses OIDC (OpenID Connect)
- Recommended for production
- Setup: https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure

## Azure DevOps CI/CD

### Official Resources

**Microsoft Learn:**
- URL: https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery-automate-azure-pipelines
- Topics: Build pipeline, release pipeline, service connections, variable groups

**Community Guides:**
- Adam Marczak Blog: https://marczak.io/posts/2023/02/quick-cicd-for-data-factory/
- Topics: Quick setup, best practices, folder structure

**Towards Data Science:**
- URL: https://towardsdatascience.com/azure-data-factory-ci-cd-made-simple-building-and-deploying-your-arm-templates-with-azure-devops-30c30595afa5
- Topics: ARM template build and deployment workflow

### Key Azure DevOps Tasks

**Build Pipeline Tasks:**
- `UseNode@1` - Install Node.js
- `Npm@1` - Install packages, run build commands
- `PublishPipelineArtifact@1` - Publish ARM templates

**Release Pipeline Tasks:**
- `DownloadPipelineArtifact@2` - Download ARM templates
- `AzurePowerShell@5` - Run PrePostDeploymentScript
- `AzureResourceManagerTemplateDeployment@3` - Deploy ARM template

### Service Connection Requirements

**Permissions Needed:**
- Data Factory Contributor (on all Data Factories)
- Contributor (on Resource Groups)
- Key Vault access policies (if using secrets)

**Configuration:**
- Project Settings → Service connections → New service connection
- Type: Azure Resource Manager
- Authentication: Service Principal (recommended) or Managed Identity

## Troubleshooting Resources

### Official Troubleshooting Guide

**URL:** https://learn.microsoft.com/en-us/azure/data-factory/ci-cd-github-troubleshoot-guide
**Last Updated:** January 2025

**Common Issues Covered:**
1. Template parameter validation errors
2. Integration Runtime type cannot be changed
3. ARM template size exceeds 4MB limit
4. Git connection problems
5. Authentication failures
6. Deployment errors

### Diagnostic Logs

**Enable Diagnostic Settings:**
```
Azure Portal → Data Factory → Diagnostic settings → Add diagnostic setting
Send to: Log Analytics workspace

Logs to Enable:
- PipelineRuns
- TriggerRuns
- ActivityRuns
- SandboxPipelineRuns
- SandboxActivityRuns
```

**Kusto Queries for Troubleshooting:**

```kusto
// Failed pipeline runs in last 24 hours
ADFPipelineRun
| where Status == "Failed"
| where TimeGenerated > ago(24h)
| project TimeGenerated, PipelineName, RunId, Status, ErrorMessage, Parameters
| order by TimeGenerated desc

// Failed CI/CD deployments
ADFActivityRun
| where ActivityType == "ExecutePipeline"
| where Status == "Failed"
| where TimeGenerated > ago(7d)
| project TimeGenerated, PipelineName, ActivityName, ErrorCode, ErrorMessage
| order by TimeGenerated desc

// Performance analysis
ADFActivityRun
| where TimeGenerated > ago(7d)
| extend DurationMinutes = datetime_diff('minute', End, Start)
| summarize AvgDuration = avg(DurationMinutes) by ActivityType, ActivityName
| where AvgDuration > 10
| order by AvgDuration desc
```

### Common Error Patterns

**Error: "Template parameters are not valid"**
- Cause: Deleted triggers still referenced in parameters
- Solution: Regenerate ARM template or use PrePostDeploymentScript cleanup

**Error: "Updating property type is not supported"**
- Cause: Trying to change Integration Runtime type
- Solution: Delete and recreate IR (not in-place update)

**Error: "Operation timed out"**
- Cause: Network connectivity, large data volume, insufficient compute
- Solution: Increase timeout, optimize query, increase DIUs

**Error: "Authentication failed"**
- Cause: Service principal expired, missing permissions, wrong credentials
- Solution: Verify credentials, check role assignments, renew if expired

## Best Practices

### Repository Structure

**Recommended Folder Layout:**
```
repository-root/
├── adf-resources/          # ADF JSON files (if using npm approach)
│   ├── dataset/
│   ├── pipeline/
│   ├── trigger/
│   ├── linkedService/
│   └── integrationRuntime/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── adf-build.yml
│       └── adf-deploy.yml
├── azure-pipelines/        # Azure DevOps pipelines
│   ├── build.yml
│   └── release.yml
├── parameters/             # Environment-specific parameters
│   ├── ARMTemplateParametersForFactory.dev.json
│   ├── ARMTemplateParametersForFactory.test.json
│   └── ARMTemplateParametersForFactory.prod.json
├── package.json            # npm configuration
└── README.md
```

### Git Configuration

**Only Configure Git on Development ADF:**
- Development: Git-integrated for source control
- Test: CI/CD deployment only (no Git)
- Production: CI/CD deployment only (no Git)

**Rationale:** Prevents accidental manual changes in higher environments

### Multi-Environment Strategy

```
Environment Flow:
Dev (Git) → Build → Test → Approval → Production
            ↓
        ARM Templates
```

**Parameter Management:**
- Separate parameter file per environment
- Store secrets in Azure Key Vault
- Reference Key Vault in parameter files
- Never commit secrets to source control

### Monitoring and Alerting

**Set up alerts for:**
- Build pipeline failures
- Deployment failures
- Pipeline run failures
- Performance degradation
- Cost anomalies

**Recommended Tools:**
- Azure Monitor (Metrics and Alerts)
- Log Analytics (Kusto queries)
- Application Insights (for custom logging)
- Azure Advisor (optimization recommendations)

## Additional Resources

### GitHub Repositories

**Official Azure Data Factory Samples:**
- URL: https://github.com/Azure/Azure-DataFactory
- Path: SamplesV2/ContinuousIntegrationAndDelivery/
- Contents: PrePostDeploymentScript.Ver2.ps1, example pipelines, documentation

**Community Examples:**
- Search GitHub for "azure-data-factory-cicd" for real-world examples
- Many organizations publish their CI/CD patterns as reference

### Community Support

**Microsoft Q&A:**
- URL: https://learn.microsoft.com/en-us/answers/tags/130/azure-data-factory
- Active community, Microsoft employees respond

**Stack Overflow:**
- Tag: `azure-data-factory`
- Large knowledge base of resolved issues

**Azure Status:**
- URL: https://status.azure.com
- Check for service outages and incidents

## When to Fetch Latest Information

**Situations requiring current documentation:**
1. npm package version updates
2. New ADF features or activities
3. Changes to ARM template schema
4. Updates to PrePostDeploymentScript
5. New GitHub Actions or Azure DevOps tasks
6. Breaking changes or deprecations

**How to Fetch:**
- Use WebFetch for Microsoft Learn articles
- Check npm for latest package version
- Use Context7 for comprehensive topic coverage
- Review Azure Data Factory GitHub for script updates

This knowledge base should be your starting point for all Azure Data Factory questions. Always verify critical information with the latest official documentation when making production decisions.

## Progressive Disclosure References

For detailed JSON schemas and complete reference materials, see:

- **Activity Types**: `references/activity-types.md` - Complete JSON schemas for all activity types (Copy, ForEach, IfCondition, Switch, Until, Lookup, ExecutePipeline, WebActivity, DatabricksJob, SetVariable, AppendVariable, Wait, Fail, GetMetadata)
- **Expression Functions**: `references/expression-functions.md` - Complete reference for all ADF expression functions (string, collection, logical, conversion, math, date/time, pipeline/activity references)
- **Linked Services**: `references/linked-services.md` - Complete JSON configurations for all connector types (Blob Storage, ADLS Gen2, Azure SQL, Synapse, Fabric Lakehouse/Warehouse, Databricks, Key Vault, REST, SFTP, Snowflake, PostgreSQL)
- **Triggers**: `references/triggers.md` - Complete JSON schemas for schedule, tumbling window, and event triggers
- **Datasets**: `references/datasets.md` - Complete JSON schemas for all dataset types with parameterization patterns
