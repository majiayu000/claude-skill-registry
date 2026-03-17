# Azure Administration Skill

## Skill Metadata

```yaml
name: azure-admin
version: 1.0.0
category: cloud-infrastructure
auto_activate_keywords:
  - azure
  - az cli
  - azd
  - entra id
  - azure ad
  - rbac
  - azure resource
  - subscription
  - resource group
  - service principal
  - managed identity
  - azure devops
  - azure portal
  - arm template
  - bicep
  - azure policy
  - cost management
  - azure mcp
tags:
  - cloud
  - identity
  - access-management
  - devops
  - infrastructure
  - automation
prerequisites:
  - Azure subscription access
  - Azure CLI installed (az)
  - Basic understanding of cloud concepts
related_skills:
  - devops
  - security
  - infrastructure-as-code
```

## Overview

This skill provides comprehensive Azure administration capabilities, covering identity management, resource orchestration, CLI tooling, and DevOps automation. It integrates Microsoft's Azure ecosystem including Azure CLI (az), Azure Developer CLI (azd), Entra ID (formerly Azure AD), and Azure MCP (Model Context Protocol) for AI-powered workflows.

**Core Capabilities:**

- **Identity & Access Management**: User provisioning, RBAC, service principals, managed identities
- **Resource Management**: Subscriptions, resource groups, ARM templates, Bicep deployments
- **CLI & Tooling**: az CLI patterns, azd workflows, PowerShell integration
- **MCP Integration**: Azure MCP server for AI-driven Azure operations
- **DevOps Automation**: CI/CD pipelines, infrastructure as code, deployment strategies
- **Cost & Governance**: Budget management, policy enforcement, compliance

**Target Audience:**
- Cloud administrators managing Azure environments
- DevOps engineers automating Azure deployments
- Security teams implementing RBAC and compliance
- Developers using Azure services and MCP integration

**Philosophy Alignment:**
This skill follows amplihack principles: ruthless simplicity, working code only, clear module boundaries, and systematic workflows.

## Quick Reference Matrix

### Common Task Mapping

| Task | Primary Tool | Secondary Tools | Skill Doc Reference |
|------|--------------|----------------|---------------------|
| Create user account | az cli | Entra ID Portal | @docs/user-management.md |
| Assign RBAC role | az cli | Azure Portal | @docs/role-assignments.md |
| Deploy resource group | az cli, Bicep | ARM templates | @docs/resource-management.md |
| Setup service principal | az cli | Portal | @docs/user-management.md#service-principals |
| Enable managed identity | az cli | Portal | @docs/user-management.md#managed-identities |
| Create resource | az cli, azd | Portal, Terraform | @docs/resource-management.md |
| Query resources | az cli --query | JMESPath | @docs/cli-patterns.md#querying |
| Bulk user operations | az cli + bash | PowerShell | @examples/bulk-user-onboarding.md |
| Environment provisioning | azd | az cli, Bicep | @examples/environment-setup.md |
| Audit role assignments | az cli | Azure Policy | @examples/role-audit.md |
| Cost analysis | az cli, Portal | Cost Management API | @docs/cost-optimization.md |
| MCP integration | Azure MCP | az cli | @docs/mcp-integration.md |
| CI/CD pipeline | Azure DevOps | GitHub Actions | @docs/devops-automation.md |

### Command Pattern Reference

```bash
# Identity operations
az ad user create --display-name "Jane Doe" --user-principal-name jane@domain.com
az ad sp create-for-rbac --name myServicePrincipal --role Contributor

# Resource operations
az group create --name myResourceGroup --location eastus
az deployment group create --resource-group myRG --template-file main.bicep

# RBAC operations
az role assignment create --assignee user@domain.com --role Reader --scope /subscriptions/xxx
az role assignment list --assignee user@domain.com --all

# Query patterns
az vm list --query "[?powerState=='VM running'].{Name:name, RG:resourceGroup}"
az resource list --resource-type "Microsoft.Compute/virtualMachines" --query "[].{name:name, location:location}"

# Cost management
az consumption usage list --start-date 2025-01-01 --end-date 2025-01-31
az costmanagement query --type ActualCost --dataset-aggregation name=Cost,function=Sum

# Azure Developer CLI (azd)
azd init --template todo-nodejs-mongo
azd up  # provision + deploy
azd env list
azd down
```

## Topic 1: Identity & Access Management

Manage Azure identities through Entra ID: users, groups, service principals, managed identities, and RBAC.

**Common operations:** User creation, group management, role assignment, service principal setup, managed identity configuration, RBAC auditing

**See:** @docs/user-management.md and @docs/role-assignments.md for complete guides

**Quick example:**
```bash
# Create user
az ad user create --display-name "Jane Doe" --user-principal-name jane@contoso.com --password "SecureP@ssw0rd!"

# Create group and add member
az ad group create --display-name "Engineering Team" --mail-nickname "engineering"
az ad group member add --group "Engineering Team" --member-id $(az ad user show --id jane@contoso.com --query id -o tsv)

# Create service principal
az ad sp create-for-rbac --name "myAppSP" --role Contributor --scopes /subscriptions/{sub-id}

# Enable managed identity
az vm identity assign --name myVM --resource-group myRG

# Assign RBAC role
az role assignment create --assignee jane@contoso.com --role Reader --scope /subscriptions/{sub-id}
```

**Key concepts:**
- **Users & Groups**: Entra ID accounts, group-based permissions
- **Service Principals**: App authentication, certificate-based auth preferred
- **Managed Identities**: Azure-managed credentials, no secret rotation needed
- **RBAC**: Owner, Contributor, Reader, custom roles at multiple scopes
- **Security**: MFA enforcement, least privilege, regular access reviews

**Best practices:**
- Use groups for role assignments (not individual users)
- Prefer managed identities over service principals
- Rotate service principal credentials every 90 days
- Store credentials in Azure Key Vault
- Enable MFA for all administrative accounts

## Topic 2: Resource Management

Organize and deploy Azure resources through subscriptions, resource groups, and infrastructure as code.

**Common operations:** Resource group creation, tagging strategy, ARM/Bicep deployment, resource locks, multi-region management

**See:** @docs/resource-management.md for advanced patterns

**Quick example:**
```bash
# Create resource group with tags
az group create --name myResourceGroup --location eastus
az group update --name myResourceGroup --tags Environment=Production CostCenter=IT

# Deploy Bicep template with validation
az deployment group validate --resource-group myRG --template-file main.bicep
az deployment group create --resource-group myRG --template-file main.bicep --parameters vmName=myVM

# Lock resource group to prevent deletion
az lock create --name DontDelete --resource-group myResourceGroup --lock-type CanNotDelete

# Query resources by tag
az resource list --tag Environment=Production --query "[].{Name:name, Type:type}"
```

**Resource hierarchy:**
```
Management Groups (optional)
└── Subscriptions (billing boundary)
    └── Resource Groups (logical container)
        └── Resources (VMs, databases, storage, etc.)
```

**Bicep basics:** Declarative IaC with cleaner syntax than ARM templates, transpiles to ARM JSON, modular and reusable.

**Tagging strategy:** Environment, CostCenter, Owner, Application, Criticality, BackupPolicy

## Topic 3: CLI & Tooling

Master Azure CLI (az), Azure Developer CLI (azd), and query patterns for automation.

**Common operations:** Authentication, JMESPath queries, batch operations, azd workflows, PowerShell integration

**See:** @docs/cli-patterns.md for advanced scripting

**Quick example:**
```bash
# Azure CLI authentication
az login
az account set --subscription "My Subscription Name"
az account show

# JMESPath query patterns
az vm list --query "[?powerState=='VM running'].{Name:name, RG:resourceGroup}"
az resource list --query "[?contains(name, 'prod')]"
az vm list --query "sort_by([],&name)[0:5]"  # Top 5 by name

# Azure Developer CLI (azd)
azd init --template todo-nodejs-mongo
azd up  # provision + deploy in one command
azd env new development
azd monitor --logs
azd down  # cleanup
```

**JMESPath essentials:** Filter `[?condition]`, Project `[].{Name:name}`, Sort `sort_by([],&field)`, Contains `contains(name, 'str')`

**azd structure:** azure.yaml, infra/ (main.bicep), src/ (application code)

**PowerShell:** `Install-Module -Name Az`, `Connect-AzAccount`, `Get-AzVM`

## Topic 4: MCP Integration

Use Azure MCP (Model Context Protocol) to enable AI-powered Azure operations through Claude Code and other AI workflows.

**Common operations:** List resources via MCP, query resource properties, execute az commands through MCP, AI-driven automation

**See:** @docs/mcp-integration.md for complete tool reference

**Quick setup:**

Install and configure:
```bash
npm install -g @modelcontextprotocol/server-azure
```

Add to `~/.config/claude-code/mcp.json`:
```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-azure"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id"
      }
    }
  }
}
```

**Available MCP tools:**
- `azure_list_resources`: List resources by type/filter
- `azure_get_resource`: Get detailed resource info
- `azure_list_users`: List Entra ID users
- `azure_list_role_assignments`: List RBAC assignments
- `azure_query`: Execute Azure Resource Graph queries
- `azure_cli`: Execute arbitrary az CLI commands

**Usage example:**

Ask Claude Code: "Show me all running VMs in my subscription"

Claude Code uses MCP tool:
```json
{
  "tool": "azure_list_resources",
  "parameters": {
    "resourceType": "Microsoft.Compute/virtualMachines",
    "filter": "powerState eq 'VM running'"
  }
}
```

## Topic 5: DevOps Automation

Automate Azure deployments through CI/CD pipelines, infrastructure as code, and GitOps workflows.

**Common operations:** Azure DevOps pipelines, GitHub Actions integration, Bicep deployments, blue-green deployments, testing

**See:** @docs/devops-automation.md for advanced patterns

**Quick example - Azure DevOps YAML:**
```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureSubscription: 'myServiceConnection'

stages:
  - stage: Deploy
    jobs:
      - deployment: DeployInfra
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureResourceManagerTemplateDeployment@3
                  inputs:
                    azureResourceManagerConnection: $(azureSubscription)
                    resourceGroupName: myRG
                    templateLocation: Linked artifact
                    csmFile: main.bicep
```

**Quick example - GitHub Actions:**
```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy Bicep
        uses: azure/arm-deploy@v1
        with:
          resourceGroupName: myRG
          template: ./infra/main.bicep
```

**Best practices:**
- Version control all IaC in Git
- Create reusable Bicep modules
- Separate parameter files per environment
- Validate templates before deployment (what-if)
- Document architecture decisions

## Topic 6: Cost & Governance

Monitor and optimize Azure spending through cost management, budgets, and policy enforcement.

**Common operations:** Cost analysis, budget alerts, policy assignment, quota management, resource optimization

**See:** @docs/cost-optimization.md for detailed strategies

**Quick example:**
```bash
# View current month costs by resource group
az costmanagement query \
  --type ActualCost \
  --dataset-aggregation name=Cost,function=Sum \
  --dataset-grouping name=ResourceGroup,type=Dimension \
  --timeframe MonthToDate

# Get consumption usage details
az consumption usage list \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --query "[].{Date:usageStart, Service:meterName, Cost:pretaxCost}"

# Assign policy to enforce tagging
az policy assignment create \
  --name "require-tag-environment" \
  --policy "require-tag-on-resources" \
  --params '{"tagName":{"value":"Environment"}}' \
  --resource-group myRG

# Check VM quota usage
az vm list-usage --location eastus --output table
```

**Cost optimization strategies:**
1. Right-size resources (use appropriate VM sizes)
2. Reserved instances (30-70% savings for 1-3 year commits)
3. Spot instances for fault-tolerant workloads
4. Auto-shutdown schedules for non-production
5. Storage tiering (move cold data to Archive)
6. Regular cleanup of unused resources

**Azure Policy use cases:**
- Require tags on resources
- Restrict resource locations
- Limit allowed VM SKUs
- Enforce encryption at rest
- Audit compliance

## Troubleshooting

### Common Issues

**Authentication Errors:**
```bash
az logout && az login --use-device-code
az account show  # Verify tenant and subscription
```

**Permission Denied:**
- Check RBAC: `az role assignment list --assignee {user-or-sp}`
- Verify resource provider: `az provider list --query "[?registrationState=='NotRegistered']"`
- Confirm proper scope (subscription vs resource group)

**Resource Not Found:**
- Verify subscription context: `az account show`
- Check resource group exists: `az group exists --name {rg-name}`
- Search across subscriptions: `az resource list --name {resource-name}`

**Quota Exceeded:**
```bash
az vm list-usage --location eastus --output table
# Request quota increase through Azure Portal or support ticket
```

**CLI Tool Issues:**
- Update to latest: `az upgrade`
- Clear cache: `rm -rf ~/.azure/`
- Reinstall extensions: `az extension list-available`

**See:** @docs/troubleshooting.md for comprehensive debugging guide

## Certification Path

**Azure Administrator Associate (AZ-104):**
- Prerequisites: 6 months hands-on Azure experience
- Domains: Identity, governance, storage, compute, networking, monitoring
- Study Resources: @references/az-104-guide.md
- Practice: Azure free account, Microsoft Learn labs

**Next Steps:**
- Azure Solutions Architect Expert (AZ-305)
- Azure DevOps Engineer Expert (AZ-400)
- Azure Security Engineer Associate (AZ-500)

## Further Learning

**Documentation:**
- @docs/user-management.md - Complete user and identity operations
- @docs/role-assignments.md - RBAC patterns and custom roles
- @docs/resource-management.md - Advanced resource operations
- @docs/mcp-integration.md - MCP tools and workflows
- @docs/cli-patterns.md - Advanced CLI scripting
- @docs/devops-automation.md - CI/CD and GitOps
- @docs/cost-optimization.md - Cost management strategies
- @docs/troubleshooting.md - Debugging and resolution

**Examples:**
- @examples/bulk-user-onboarding.md - Automated user provisioning
- @examples/environment-setup.md - Complete environment deployment
- @examples/role-audit.md - RBAC compliance auditing
- @examples/mcp-workflow.md - AI-powered Azure operations

**References:**
- @references/microsoft-learn.md - Official learning paths
- @references/az-104-guide.md - Certification preparation
- @references/api-references.md - API and SDK documentation
