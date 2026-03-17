---
name: "Bicep AVM Mastery"
description: "Azure Verified Modules (AVM), Bicep best practices, and MCP-powered infrastructure as code for Azure"
---

# Skill: Bicep AVM Mastery

> Azure Verified Modules (AVM), Bicep best practices, and MCP-powered infrastructure as code for Azure.

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | bicep-avm-mastery |
| **Version** | 1.1.0 |
| **Category** | Cloud/Infrastructure |
| **Difficulty** | Advanced |
| **Prerequisites** | Basic Azure, infrastructure-as-code |
| **Related Skills** | azure-architecture-patterns, infrastructure-as-code |
| **Last Validated** | Feb 2026 |

> ⚠️ **Staleness Watch**: The AVM registry grows monthly — module counts and version numbers change frequently. Always use [`mcp_bicep_list_avm_metadata`](https://azure.github.io/Azure-Verified-Modules/) to enumerate current modules rather than relying on hardcoded counts. Watch for new module categories and `avm/res` vs `avm/ptn` naming changes.

---

## Overview

Bicep is Azure's domain-specific language for infrastructure as code. This skill covers Bicep best practices, Azure Verified Modules (AVM), and MCP tool integration for high-quality, production-ready deployments.

### Why Bicep?

| Feature | Bicep | ARM JSON | Terraform |
|---------|-------|----------|-----------|
| Syntax | Clean, readable | Verbose | HCL |
| Azure Integration | Native | Native | Provider |
| State Management | Azure-managed | Azure-managed | External |
| Learning Curve | Low | High | Medium |
| Tooling | VS Code, MCP | Limited | Extensive |

---

## Module 1: Bicep Best Practices

### General Rules

1. **Avoid setting `name` for module statements** — no longer required
2. **Use user-defined types** for grouped param/output values instead of multiple params
3. **Prefer `.bicepparam` files** over JSON parameters files

### Resource Patterns

```bicep
// ✅ CORRECT: Use parent property
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2023-09-01' = {
  parent: vnet  // Reference parent symbolically
  name: 'default'
  properties: {
    addressPrefix: '10.0.0.0/24'
  }
}

// ❌ AVOID: Slash in name property
resource subnetBad 'Microsoft.Network/virtualNetworks/subnets@2023-09-01' = {
  name: '${vnetName}/default'  // Don't do this
}
```

### Type Safety

```bicep
// ✅ CORRECT: Typed user-defined type
@export()
type storageAccountConfig = {
  @description('Storage account name')
  name: string
  @description('SKU for the storage account')
  sku: 'Standard_LRS' | 'Standard_GRS' | 'Premium_LRS'
  @description('Enable public access')
  allowPublicAccess: bool
}

// ❌ AVOID: Open types
param config object  // Too broad
```

### Symbolic References

```bicep
// ✅ CORRECT: Use symbolic references
output storageId string = storageAccount.id
output storageName string = storageAccount.name

// ❌ AVOID: resourceId() and reference()
output storageIdBad string = resourceId('Microsoft.Storage/storageAccounts', storageAccountName)
```

### Security

```bicep
// ✅ ALWAYS use @secure() for sensitive data
@secure()
param adminPassword string

@secure()
param connectionString string
```

### Null Handling

```bicep
// ✅ CORRECT: Safe dereference with coalesce
var subnetId = vnet.properties.subnets[?0].?id ?? 'default'

// ❌ AVOID: Non-null assertion or verbose ternary
var subnetIdBad = vnet!.properties.subnets[0].id
```

---

## Module 2: Azure Verified Modules (AVM)

### What is AVM?

Azure Verified Modules are **Microsoft-supported, production-ready Bicep modules** covering 328+ Azure resources. They follow best practices, are tested, and receive updates.

### AVM Categories

| Category | Count | Examples |
|----------|-------|----------|
| Compute | 50+ | VMs, AKS, App Service, Functions |
| Networking | 40+ | VNets, NSGs, Load Balancers, Front Door |
| Storage | 30+ | Storage Accounts, Cosmos DB, SQL |
| Security | 25+ | Key Vault, Managed Identities, WAF |
| Integration | 20+ | Service Bus, Event Grid, Logic Apps |
| AI/ML | 15+ | Cognitive Services, OpenAI, ML Workspaces |

### Using AVM in Bicep

```bicep
// Module from Bicep Registry (AVM)
module storageAccount 'br/public:avm/res/storage/storage-account:0.14.3' = {
  name: 'storageAccountDeployment'
  params: {
    name: 'st${uniqueString(resourceGroup().id)}'
    location: location
    skuName: 'Standard_LRS'
    kind: 'StorageV2'
    managedIdentities: {
      systemAssigned: true
    }
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}
```

### Finding AVM Modules

Use the MCP tool to discover available modules:

```
mcp_bicep_list_avm_metadata → 328 modules with:
  - Module name and description
  - Latest version
  - Required/optional parameters
  - Usage examples
```

---

## Module 3: MCP Tool Integration

### Required Extensions & MCP Servers

| Component | ID / Name | Purpose |
|-----------|-----------|--------|
| **VS Code Extension** | `ms-azuretools.vscode-bicep` | Bicep language support, IntelliSense |
| **VS Code Extension** | `ms-azuretools.vscode-azure-github-copilot` | Azure Copilot integration |
| **VS Code Extension** | `ms-vscode.azure-account` | Azure authentication |
| **MCP Server** | `bicep-mcp` | AVM lookup, schema, validation, best practices |

**Installation**:
```bash
# VS Code Extensions (required for Bicep authoring)
code --install-extension ms-azuretools.vscode-bicep
code --install-extension ms-azuretools.vscode-azure-github-copilot
code --install-extension ms-vscode.azure-account

# MCP Server enabled via VS Code MCP gallery
# Settings: chat.mcp.gallery.enabled = true
```

### Fallback Patterns (When MCP Unavailable)

If Bicep MCP tools are not available, use these alternatives:

| MCP Tool | Fallback Approach |
|----------|-------------------|
| `list_avm_metadata` | Browse https://aka.ms/avm/modules |
| `get_az_resource_type_schema` | Use `bicep list-api-types` CLI or ARM reference docs |
| `get_bicep_best_practices` | Reference https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices |
| `get_bicep_file_diagnostics` | VS Code Bicep extension shows diagnostics automatically |
| `format_bicep_file` | Run `bicep format <file>` CLI |
| `decompile_arm_template_file` | Run `az bicep decompile --file <file>` CLI |

**Manual AVM Module Discovery**:
```bash
# Search Bicep Registry for modules
az bicep registry list --resource-group bicep-registry

# Or browse AVM directly
# https://github.com/Azure/bicep-registry-modules
```

### Available Bicep MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_bicep_list_avm_metadata` | Browse 328 Azure Verified Modules |
| `mcp_bicep_get_az_resource_type_schema` | Get resource type properties |
| `mcp_bicep_get_bicep_best_practices` | Current best practices |
| `mcp_bicep_get_bicep_file_diagnostics` | Validate Bicep files |
| `mcp_bicep_format_bicep_file` | Auto-format code |
| `mcp_bicep_decompile_arm_template_file` | Convert ARM JSON → Bicep |
| `mcp_bicep_get_file_references` | Find file dependencies |
| `mcp_bicep_get_deployment_snapshot` | Preview deployment changes |

### Common Workflows

#### Find the Right AVM Module

```
User: "I need to deploy a storage account with private endpoints"

Alex → mcp_bicep_list_avm_metadata 
  Filter: storage
  Returns: avm/res/storage/storage-account (v0.14.3)
    - Supports privateEndpoints parameter
    - Supports networkAcls
    - Includes diagnosticSettings
```

#### Get Resource Schema

```
User: "What properties does App Service support?"

Alex → mcp_bicep_get_az_resource_type_schema
  provider: Microsoft.Web
  resourceType: sites
  Returns: Full property schema with descriptions
```

#### Validate Before Deploy

```
User: "Check my Bicep file for errors"

Alex → mcp_bicep_get_bicep_file_diagnostics
  filePath: main.bicep
  Returns: BCP036 errors, warnings, suggestions
```

#### Convert Legacy ARM

```
User: "Convert this ARM template to Bicep"

Alex → mcp_bicep_decompile_arm_template_file
  filePath: azuredeploy.json
  Returns: Clean Bicep code
```

---

## Module 4: Project Patterns

### Recommended Structure

```text
infrastructure/
├── main.bicep              # Entry point
├── main.bicepparam         # Parameters (env-specific)
├── modules/
│   ├── networking.bicep    # Custom modules
│   ├── compute.bicep
│   └── data.bicep
├── types/
│   └── shared.bicep        # Shared user-defined types
└── bicepconfig.json        # Bicep configuration
```

### bicepconfig.json

```json
{
  "analyzers": {
    "core": {
      "rules": {
        "no-hardcoded-location": {
          "level": "error"
        },
        "secure-parameter-default": {
          "level": "error"
        },
        "prefer-interpolation": {
          "level": "warning"
        }
      }
    }
  },
  "moduleAliases": {
    "br": {
      "public": {
        "registry": "mcr.microsoft.com/bicep"
      }
    }
  }
}
```

### Environment-Specific Parameters

```bicep
// main.bicepparam (for dev)
using './main.bicep'

param environment = 'dev'
param skuName = 'Standard_LRS'
param instanceCount = 1
```

```bicep
// main.bicepparam (for prod)  
using './main.bicep'

param environment = 'prod'
param skuName = 'Standard_GRS'
param instanceCount = 3
```

---

## Module 5: Deployment Patterns

### Azure CLI

```bash
# What-if preview
az deployment group what-if \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters main.bicepparam

# Deploy
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters main.bicepparam
```

### GitHub Actions

```yaml
- name: Deploy Bicep
  uses: azure/arm-deploy@v2
  with:
    resourceGroupName: ${{ env.RESOURCE_GROUP }}
    template: ./infrastructure/main.bicep
    parameters: ./infrastructure/main.bicepparam
    deploymentMode: Incremental
```

### Azure DevOps

```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: 'AzureConnection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      az deployment group create \
        --resource-group $(resourceGroup) \
        --template-file infrastructure/main.bicep \
        --parameters infrastructure/main.bicepparam
```

---

## Common Diagnostic Codes

| Code | Meaning | Fix |
|------|---------|-----|
| BCP036 | Invalid property | Check resource schema |
| BCP037 | Invalid property value | Verify allowed values |
| BCP081 | Hallucinated resource/property | Use schema lookup |
| BCP035 | Missing required property | Add required params |
| BCP334 | Expected literal value | Use string/number directly |

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "Bicep", "infrastructure as code Azure" | Full skill activation |
| "AVM", "Azure Verified Modules" | Module 2 |
| "Bicep MCP", "validate Bicep" | Module 3 |
| "Bicep project structure" | Module 4 |
| "deploy Bicep", "CI/CD Bicep" | Module 5 |
| "BCP error", "Bicep diagnostic" | Common Diagnostic Codes |

---

*Skill created: 2026-02-14 | Category: Cloud/Infrastructure | Status: Active | MCP-Enhanced: Yes*

---

## Synapses

- [.github/skills/infrastructure-as-code/SKILL.md] (High, Extends, Bidirectional) - "Bicep is an IaC tool covered in depth here"
- [.github/skills/azure-architecture-patterns/SKILL.md] (High, Implements, Bidirectional) - "Bicep deploys architectures designed with WAF"
- [.github/skills/azure-devops-automation/SKILL.md] (Medium, Uses, Forward) - "CI/CD pipelines deploy Bicep code"
