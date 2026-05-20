---
name: bicep
description: |
  Use when writing Azure Bicep templates for infrastructure deployment. Covers resource declarations, modules, parameters, outputs, and deployment commands.
  USE FOR: Azure resource deployment, Bicep DSL modules, what-if previews, Azure-native IaC
  DO NOT USE FOR: AWS resources (use cloud-formation), multi-cloud infrastructure (use terraform or pulumi), raw ARM JSON (use arm)
license: MIT
metadata:
  displayName: "Azure Bicep"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Azure Bicep Documentation"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/"
  - title: "Bicep GitHub Repository"
    url: "https://github.com/Azure/bicep"
---

# Azure Bicep

## Overview
Bicep is Azure's domain-specific language for deploying Azure resources declaratively. It compiles to ARM JSON but provides a cleaner syntax with type safety, modules, and IDE support. Bicep is the recommended replacement for authoring ARM templates directly.

## Basic Template
```bicep
@description('The Azure region for all resources')
param location string = resourceGroup().location

@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${uniqueString(resourceGroup().id)}${environment}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-${environment}'
  location: location
  sku: {
    name: environment == 'prod' ? 'P1v3' : 'B1'
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'app-${environment}-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      minTlsVersion: '1.2'
    }
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output storageAccountId string = storageAccount.id
```

## Modules
Reusable components in separate `.bicep` files:
```bicep
// modules/storage.bicep
param name string
param location string
param sku string = 'Standard_LRS'

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  sku: { name: sku }
  kind: 'StorageV2'
}

output id string = storage.id
output name string = storage.name
```

Consume in the main template:
```bicep
module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'
  params: {
    name: 'stmyapp${environment}'
    location: location
    sku: environment == 'prod' ? 'Standard_GRS' : 'Standard_LRS'
  }
}
```

## Deployment
```bash
# Deploy to a resource group
az deployment group create \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters environment=prod

# What-if (preview changes)
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep

# Deploy to subscription scope
az deployment sub create \
  --location eastus \
  --template-file main.bicep
```

## Key Features
| Feature | Syntax |
|---------|--------|
| Parameters | `param name string` with decorators (`@allowed`, `@minLength`) |
| Variables | `var name = expression` |
| Resources | `resource sym 'type@version' = { ... }` |
| Modules | `module sym 'path.bicep' = { params: {} }` |
| Outputs | `output name type = value` |
| Loops | `[for item in list: { ... }]` |
| Conditions | `if (condition) { ... }` or ternary `condition ? a : b` |
| Existing resources | `resource sym 'type@version' existing = { name: '...' }` |

## Best Practices
- Always use `what-if` to preview changes before deploying.
- Use modules to break large templates into reusable, testable components.
- Use parameter decorators (`@allowed`, `@minLength`, `@description`) for validation and documentation.
- Reference existing resources with the `existing` keyword instead of hardcoding resource IDs.
- Use `uniqueString(resourceGroup().id)` for globally unique names (storage accounts, web apps).
- Pin API versions on resources for predictable behavior.
- Use Bicep instead of ARM JSON — it compiles to identical output with better readability.
