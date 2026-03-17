---
name: "Infrastructure as Code Skill"
description: "**Domain**: DevOps & Cloud Engineering"
---

# Infrastructure as Code Skill

> **Domain**: DevOps & Cloud Engineering
> **Inheritance**: inheritable
> **Version**: 1.0.0
> **Last Updated**: 2026-02-01

---

## Overview

Comprehensive patterns for defining, provisioning, and managing cloud infrastructure through declarative code. Covers major IaC tools (Terraform, Bicep, Pulumi, CloudFormation), best practices for modularity, state management, testing, and GitOps workflows.

---

## IaC Fundamentals

### Why Infrastructure as Code?

```text
Manual Infrastructure          Infrastructure as Code
┌─────────────────────┐       ┌─────────────────────┐
│  Click in Console   │       │  Write Code         │
│  Document Steps     │       │  Version Control    │
│  Hope It's Repeated │       │  Review & Approve   │
│  Drift Over Time    │       │  Automated Deploy   │
│  Unclear State      │       │  Consistent State   │
└─────────────────────┘       └─────────────────────┘
```

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Repeatability** | Same code = same infrastructure, every time |
| **Version Control** | Track changes, rollback, audit history |
| **Collaboration** | Code review, PRs, shared ownership |
| **Documentation** | Code IS the documentation |
| **Testing** | Validate before deploy |
| **Speed** | Provision environments in minutes |

### Declarative vs Imperative

| Approach | Description | Tools |
|----------|-------------|-------|
| **Declarative** | Describe desired end state | Terraform, Bicep, CloudFormation |
| **Imperative** | Describe steps to reach state | Scripts, Ansible, Pulumi (optional) |

**Prefer declarative** — let the tool figure out how to reach the desired state.

---

## Tool Comparison

| Tool | Provider | Language | State | Best For |
|------|----------|----------|-------|----------|
| **Terraform** | HashiCorp | HCL | Remote/Local | Multi-cloud, mature ecosystem |
| **Bicep** | Microsoft | Bicep DSL | Azure-managed | Azure-native, simple syntax |
| **Pulumi** | Pulumi | TS/Python/Go/C# | Managed/Self | Developers who prefer real languages |
| **CloudFormation** | AWS | YAML/JSON | AWS-managed | AWS-only, deep integration |
| **ARM Templates** | Microsoft | JSON | Azure-managed | Legacy Azure (prefer Bicep) |
| **CDK** | AWS | TS/Python/Java | AWS-managed | Developers on AWS |

---

## Terraform Patterns

### Project Structure

```text
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   └── database/
└── shared/
    └── providers.tf
```

### Basic Resource Pattern

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  type        = string
  default     = "eastus2"
  description = "Azure region for resources"
}

# main.tf
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project
  }
}

# outputs.tf
output "resource_group_id" {
  value       = azurerm_resource_group.main.id
  description = "The ID of the resource group"
}
```

### Module Pattern

```hcl
# modules/app-service/variables.tf
variable "name" {
  type        = string
  description = "Name of the App Service"
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "sku" {
  type = object({
    tier = string
    size = string
  })
  default = {
    tier = "Standard"
    size = "S1"
  }
}

# modules/app-service/main.tf
resource "azurerm_service_plan" "main" {
  name                = "asp-${var.name}"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = var.sku.size
}

resource "azurerm_linux_web_app" "main" {
  name                = "app-${var.name}"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = var.sku.tier != "Free"
  }
}

# Usage in environment
module "api" {
  source = "../../modules/app-service"

  name                = "myapi-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku = {
    tier = var.environment == "prod" ? "Premium" : "Standard"
    size = var.environment == "prod" ? "P1v3" : "S1"
  }
}
```

### State Management

```hcl
# backend.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate"
    container_name       = "tfstate"
    key                  = "myproject/dev/terraform.tfstate"
  }
}
```

**State Best Practices:**
- ✅ Use remote state (never local for teams)
- ✅ Enable state locking
- ✅ Encrypt state at rest
- ✅ Separate state per environment
- ❌ Never commit `.tfstate` files
- ❌ Never manually edit state

### Data Sources

```hcl
# Reference existing resources
data "azurerm_key_vault" "shared" {
  name                = "kv-shared-${var.environment}"
  resource_group_name = "rg-shared-${var.environment}"
}

data "azurerm_key_vault_secret" "db_password" {
  name         = "db-admin-password"
  key_vault_id = data.azurerm_key_vault.shared.id
}

# Use in resource
resource "azurerm_mssql_server" "main" {
  name                         = "sql-${var.project}-${var.environment}"
  administrator_login          = "sqladmin"
  administrator_login_password = data.azurerm_key_vault_secret.db_password.value
  # ...
}
```

---

## Bicep Patterns (Azure)

### Basic Structure

```bicep
// main.bicep
targetScope = 'subscription'

@allowed(['dev', 'staging', 'prod'])
param environment string

param location string = 'eastus2'

var resourceGroupName = 'rg-myproject-${environment}'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

module appService 'modules/app-service.bicep' = {
  scope: rg
  name: 'appServiceDeployment'
  params: {
    appName: 'app-myproject-${environment}'
    location: location
    sku: environment == 'prod' ? 'P1v3' : 'S1'
  }
}

output resourceGroupId string = rg.id
output appServiceUrl string = appService.outputs.defaultHostName
```

### Module Pattern

```bicep
// modules/app-service.bicep
@description('Name of the App Service')
param appName string

param location string = resourceGroup().location

@allowed(['F1', 'S1', 'P1v3'])
param sku string = 'S1'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-${appName}'
  location: location
  sku: {
    name: sku
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      alwaysOn: sku != 'F1'
    }
  }
}

output defaultHostName string = webApp.properties.defaultHostName
output appServiceId string = webApp.id
```

### Bicep vs Terraform for Azure

| Aspect | Bicep | Terraform |
|--------|-------|-----------|
| Azure Support | Day-0 | Day-1 to Day-N |
| Multi-cloud | ❌ | ✅ |
| State Management | Azure-managed | Self-managed |
| Learning Curve | Lower | Moderate |
| Community Modules | Limited | Extensive |
| Type Safety | Strong | Moderate |

**Recommendation**: Bicep for Azure-only; Terraform for multi-cloud or complex scenarios.

---

## Pulumi Patterns

### TypeScript Example

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as azure from "@pulumi/azure-native";

const config = new pulumi.Config();
const environment = config.require("environment");

// Resource Group
const resourceGroup = new azure.resources.ResourceGroup("rg", {
  resourceGroupName: `rg-myproject-${environment}`,
  location: "eastus2",
  tags: {
    Environment: environment,
    ManagedBy: "Pulumi",
  },
});

// App Service Plan
const appServicePlan = new azure.web.AppServicePlan("asp", {
  resourceGroupName: resourceGroup.name,
  kind: "Linux",
  reserved: true,
  sku: {
    name: environment === "prod" ? "P1v3" : "S1",
    tier: environment === "prod" ? "Premium" : "Standard",
  },
});

// Web App
const webApp = new azure.web.WebApp("app", {
  resourceGroupName: resourceGroup.name,
  serverFarmId: appServicePlan.id,
  siteConfig: {
    linuxFxVersion: "NODE|20-lts",
    alwaysOn: true,
  },
});

export const endpoint = pulumi.interpolate`https://${webApp.defaultHostName}`;
```

### When to Use Pulumi

✅ **Good fit:**
- Team prefers TypeScript/Python/Go over HCL
- Need complex logic (loops, conditionals, API calls)
- Want type checking and IDE support
- Building reusable libraries

❌ **Consider alternatives:**
- Simple infrastructure needs
- Team experienced with Terraform
- Need maximum community resources

---

## Best Practices

### Naming Conventions

```text
Pattern: {resource-type}-{project}-{environment}-{region}-{instance}

Examples:
  rg-myproject-prod-eus2           (Resource Group)
  app-myproject-prod-eus2          (App Service)
  sql-myproject-prod-eus2          (SQL Server)
  kv-myproject-prod-eus2           (Key Vault)
  st-myproject-prod-eus2           (Storage - no hyphens)
```

### Tagging Strategy

```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "Terraform"
    CostCenter  = var.cost_center
    Owner       = var.owner_email
    CreatedDate = timestamp()
  }
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project}-${var.environment}"
  location = var.location
  tags     = local.common_tags
}
```

### Secrets Management

```text
❌ DON'T: Hard-code secrets in IaC
❌ DON'T: Store secrets in tfvars files
❌ DON'T: Commit secrets to version control

✅ DO: Use Key Vault / Secrets Manager
✅ DO: Reference secrets via data sources
✅ DO: Use CI/CD pipeline secrets
✅ DO: Use managed identities where possible
```

### Environment Parity

```text
┌─────────────────────────────────────────────────────────┐
│                    Same Code Base                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   dev.tfvars      staging.tfvars      prod.tfvars      │
│   ┌─────────┐     ┌─────────┐        ┌─────────┐       │
│   │ SKU: S1 │     │ SKU: S1 │        │ SKU: P1v3│      │
│   │ Count:1 │     │ Count:2 │        │ Count:3  │      │
│   └─────────┘     └─────────┘        └─────────┘       │
│        │               │                  │             │
│        ▼               ▼                  ▼             │
│   ┌─────────┐     ┌─────────┐        ┌─────────┐       │
│   │   DEV   │     │ STAGING │        │  PROD   │       │
│   └─────────┘     └─────────┘        └─────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Testing IaC

### Static Analysis

```bash
# Terraform
terraform fmt -check
terraform validate
tflint
tfsec  # Security scanning
checkov  # Policy as code

# Bicep
az bicep build --file main.bicep  # Syntax check
```

### Unit Testing (Terraform)

```hcl
# tests/app_service_test.tftest.hcl
run "app_service_creates_correctly" {
  command = plan

  variables {
    environment = "dev"
    project     = "test"
  }

  assert {
    condition     = azurerm_linux_web_app.main.site_config[0].always_on == true
    error_message = "Always-on should be enabled"
  }
}
```

### Integration Testing

```bash
# Deploy to ephemeral environment
terraform apply -auto-approve -var="environment=test-${BUILD_ID}"

# Run integration tests
npm test

# Destroy ephemeral environment
terraform destroy -auto-approve -var="environment=test-${BUILD_ID}"
```

---

## CI/CD Patterns

### GitHub Actions Workflow

```yaml
name: Infrastructure

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    paths: ['infrastructure/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.0

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/environments/prod
        env:
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_USE_OIDC: true

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: infrastructure/environments/prod

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: infrastructure/environments/prod/tfplan

  apply:
    needs: plan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: infrastructure/environments/prod

      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
        working-directory: infrastructure/environments/prod
```

### GitOps Flow

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Feature    │     │    Pull      │     │    Main      │
│   Branch     │ ──► │   Request    │ ──► │   Branch     │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  terraform plan      terraform plan       terraform apply
  (local preview)     (CI check)           (automated)
```

---

## Common Patterns

### Conditional Resources

```hcl
# Terraform
resource "azurerm_application_insights" "main" {
  count = var.enable_monitoring ? 1 : 0

  name                = "appi-${var.project}-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  application_type    = "web"
}
```

### Dynamic Blocks

```hcl
resource "azurerm_network_security_group" "main" {
  name                = "nsg-${var.project}-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location

  dynamic "security_rule" {
    for_each = var.security_rules
    content {
      name                       = security_rule.value.name
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }
}
```

### Resource Dependencies

```hcl
# Implicit (recommended)
resource "azurerm_linux_web_app" "main" {
  service_plan_id = azurerm_service_plan.main.id  # Implicit dependency
}

# Explicit (when needed)
resource "azurerm_linux_web_app" "main" {
  depends_on = [azurerm_private_endpoint.sql]  # Wait for private endpoint
}
```

---

## Anti-Patterns

### ❌ Monolithic Configuration

**Problem**: Single massive `.tf` file
**Solution**: Split into logical modules and files

### ❌ Hard-coded Values

**Problem**: Values embedded in resources
**Solution**: Use variables with defaults and tfvars

### ❌ No State Locking

**Problem**: Concurrent applies corrupt state
**Solution**: Enable state locking (DynamoDB for S3, built-in for Azure)

### ❌ Manual Changes

**Problem**: Drift between code and reality
**Solution**: Always change through code, use `terraform import` for existing resources

### ❌ Overly Generic Modules

**Problem**: Modules that try to do everything
**Solution**: Purpose-built modules with sensible defaults

---

## MCP Tool Integration

### Required Extensions & MCP Servers

| Component | ID / Name | Purpose |
|-----------|-----------|--------|
| **VS Code Extension** | `ms-azuretools.vscode-bicep` | Bicep language support |
| **VS Code Extension** | `hashicorp.terraform` | Terraform language support |
| **VS Code Extension** | `ms-azuretools.vscode-azure-github-copilot` | Azure Copilot integration |
| **MCP Server** | `bicep-mcp` | Bicep tools (AVM, schema, validation) |
| **MCP Server** | `azure-mcp` | Azure architecture and deployment tools |

**Installation**:
```bash
# VS Code Extensions
code --install-extension ms-azuretools.vscode-bicep
code --install-extension hashicorp.terraform
code --install-extension ms-azuretools.vscode-azure-github-copilot

# MCP Servers enabled via VS Code MCP gallery
# Settings: chat.mcp.gallery.enabled = true
```

### Fallback Patterns (When MCP Unavailable)

| MCP Tool | Fallback Approach |
|----------|-------------------|
| `list_avm_metadata` | Browse https://aka.ms/avm/modules |
| `get_az_resource_type_schema` | ARM template reference or `az rest` API |
| `get_bicep_best_practices` | https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices |
| `get_bicep_file_diagnostics` | VS Code Bicep extension or `bicep build` CLI |
| `cloudarchitect` | Azure Architecture Center + WAF Assessment (https://aka.ms/waf-assessment) |
| `documentation` | https://learn.microsoft.com/azure/architecture |

**Terraform Fallbacks** (no MCP yet):
```bash
# Terraform validation
terraform validate
terraform fmt -check

# Provider docs
terraform providers schema -json

# Static analysis
tflint
tfsec
checkov -d .
```

### Available IaC MCP Tools

Alex has access to Bicep MCP tools for enhanced infrastructure as code capabilities:

| Tool | Purpose |
|------|---------|
| `mcp_bicep_list_avm_metadata` | Browse 328 Azure Verified Modules |
| `mcp_bicep_get_az_resource_type_schema` | Get resource type properties and schema |
| `mcp_bicep_get_bicep_best_practices` | Current Bicep coding best practices |
| `mcp_bicep_get_bicep_file_diagnostics` | Validate Bicep files, find errors |
| `mcp_bicep_format_bicep_file` | Auto-format Bicep code |
| `mcp_bicep_decompile_arm_template_file` | Convert ARM JSON → Bicep |
| `mcp_bicep_decompile_arm_parameters_file` | Convert parameters.json → .bicepparam |

### Azure Architecture Tools

| Tool | Purpose |
|------|---------|
| `mcp_azure_mcp_cloudarchitect` | Interactive architecture design aligned with WAF |
| `mcp_azure_mcp_documentation` | Search Azure docs and best practices |
| `mcp_azure_mcp_get_bestpractices` | Code generation and deployment patterns |

### Workflow: MCP-Enhanced IaC

```text
1. Architecture Design
   └─ mcp_azure_mcp_cloudarchitect → Requirements → Component design

2. Module Discovery
   └─ mcp_bicep_list_avm_metadata → Find production-ready modules

3. Schema Lookup
   └─ mcp_bicep_get_az_resource_type_schema → Exact properties

4. Code Generation
   └─ mcp_bicep_get_bicep_best_practices → Write clean code

5. Validation
   └─ mcp_bicep_get_bicep_file_diagnostics → Fix errors early

6. Deployment
   └─ mcp_azure_mcp_deploy → Automated deployment
```

### When to Use MCP Tools

| Scenario | Tool |
|----------|------|
| "What modules exist for X?" | `list_avm_metadata` |
| "What properties does X support?" | `get_az_resource_type_schema` |
| "Review my Bicep file" | `get_bicep_file_diagnostics` |
| "Convert ARM to Bicep" | `decompile_arm_template_file` |
| "Design infrastructure from scratch" | `cloudarchitect` |

**Related Skill**: See `bicep-avm-mastery` for deep Bicep patterns and AVM guidance.

---

## Activation Triggers

- "infrastructure as code", "IaC"
- "Terraform", "Bicep", "Pulumi", "CloudFormation"
- "provision infrastructure", "deploy infrastructure"
- "HCL", "tfvars", "terraform.tfstate"
- "ARM template", "CDK"
- "GitOps", "infrastructure pipeline"
- "MCP Bicep", "AVM modules", "Azure Verified Modules"
- "convert ARM to Bicep", "validate Bicep"

---

## Quick Reference

### IaC Checklist

- [ ] Use remote state with locking
- [ ] Implement consistent naming conventions
- [ ] Apply tagging strategy for all resources
- [ ] Store secrets in Key Vault / Secrets Manager
- [ ] Use modules for reusable components
- [ ] Run static analysis (tflint, tfsec)
- [ ] Set up CI/CD pipeline with plan/apply
- [ ] Document module inputs and outputs
- [ ] Test with ephemeral environments
- [ ] Enable drift detection

### Command Reference

```bash
# Terraform
terraform init          # Initialize backend and providers
terraform plan          # Preview changes
terraform apply         # Apply changes
terraform destroy       # Tear down infrastructure
terraform import        # Import existing resource
terraform state list    # List resources in state
terraform fmt           # Format code

# Bicep
az bicep build          # Compile to ARM
az deployment sub create --location eastus2 --template-file main.bicep
az deployment group create --resource-group rg-name --template-file main.bicep
```

---

*Infrastructure as Code skill — Reliable, repeatable infrastructure through code | MCP-Enhanced: Yes | Updated: 2026-02-14*

---

## Synapses

- [.github/skills/bicep-avm-mastery/SKILL.md] (High, Contains, Forward) - "Deep Bicep and AVM patterns"
- [.github/skills/azure-architecture-patterns/SKILL.md] (High, Uses, Forward) - "IaC implements cloud architectures"
- [.github/skills/azure-devops-automation/SKILL.md] (Medium, Uses, Forward) - "CI/CD deploys IaC code"
