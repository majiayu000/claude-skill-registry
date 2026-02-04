---
name: bicep
description: Expert assistance for Azure Bicep infrastructure-as-code. Provides best practices for authoring Bicep templates, Azure resource type discovery with API versions, resource schema retrieval, and Azure Verified Modules (AVM) guidance. Use when writing Bicep files, deploying Azure resources, looking up resource types/schemas, or working with AVM modules.
---

# Bicep Expert Assistant

Expert guidance for Azure Bicep infrastructure-as-code development, including best practices, resource type discovery, schema retrieval, and Azure Verified Modules.

## Triggers

Use this skill when you see:
- bicep, azure bicep, arm template
- infrastructure as code, iac, azure deployment
- avm, azure verified modules
- resource type, api version, bicep module

## Instructions

### Resource Type Discovery

```bash
# List resource types for a provider
az provider show --namespace Microsoft.Storage --query "resourceTypes[].{Type:resourceType,ApiVersions:apiVersions[0]}" -o table

# Common providers
az provider show --namespace Microsoft.Compute
az provider show --namespace Microsoft.Network
az provider show --namespace Microsoft.KeyVault
```

### Parameters Best Practices

```bicep
// Use descriptive names with descriptions
@description('The name of the storage account. Must be globally unique.')
param storageAccountName string

// Set safe defaults with constraints
@description('The SKU for the storage account')
@allowed(['Standard_LRS', 'Standard_GRS', 'Standard_ZRS', 'Premium_LRS'])
param storageAccountSku string = 'Standard_LRS'

// Apply length constraints
@minLength(3)
@maxLength(24)
param storageAccountName string

// Secure sensitive parameters
@secure()
param adminPassword string
```

### Variables

```bicep
// Use for computed values
var storageAccountName = '${prefix}${uniqueString(resourceGroup().id)}'

// Use for repeated values
var commonTags = {
  environment: environment
  project: projectName
  deployedBy: 'Bicep'
}

// Typed variables (Bicep 0.26+)
var instanceCount int = environment == 'prod' ? 5 : 2
```

### Resources

```bicep
// Use symbolic names without 'name' suffix
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}

// Use existing keyword for references
resource existingVnet 'Microsoft.Network/virtualNetworks@2023-09-01' existing = {
  name: vnetName
}
```

### Child Resources

```bicep
// Nested declaration (preferred)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  // ...

  resource blobService 'blobServices' = {
    name: 'default'
  }
}

// Or use parent property
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}
```

### Modules

```bicep
// Local module
module storageModule 'modules/storage.bicep' = {
  name: 'storageDeployment'
  params: {
    storageAccountName: storageAccountName
    location: location
  }
}

// Azure Verified Module from Registry
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: storageAccountName
    location: location
  }
}
```

### Outputs

```bicep
// Expose essential values
output storageAccountId string = storageAccount.id
output primaryEndpoints object = storageAccount.properties.primaryEndpoints

// NEVER output secrets
// WRONG - Never do this:
// output connectionString string = storageAccount.listKeys().keys[0].value
```

### Common Resource Examples

#### Storage Account

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}
```

#### Virtual Network

```bicep
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'default'
        properties: {
          addressPrefix: '10.0.1.0/24'
        }
      }
    ]
  }
}
```

#### Key Vault

```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
  }
}
```

### Azure Verified Modules (AVM)

#### Using AVM Modules

```bicep
// Reference from Bicep Public Registry
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: 'mystorageaccount'
    location: location
  }
}
```

#### Module Types
- **Resource Modules (`avm/res/`)**: Single Azure resource with all configurations
- **Pattern Modules (`avm/ptn/`)**: Multi-resource patterns for common scenarios
- **Utility Modules (`avm/utl/`)**: Helper types and functions

#### Finding AVM Modules
- Browse: https://azure.github.io/Azure-Verified-Modules/indexes/bicep/
- GitHub: https://github.com/Azure/bicep-registry-modules

### File Organization

```
project/
├── main.bicep           # Entry point
├── main.bicepparam      # Parameters file
├── modules/
│   ├── networking.bicep
│   ├── storage.bicep
│   └── compute.bicep
└── tests/
    └── main.tests.bicep
```

### Order of Elements

1. Target scope (if not resourceGroup)
2. Parameters
3. Variables
4. Resources
5. Modules
6. Outputs

## Best Practices

1. **Naming**: Use camelCase for parameters, variables, and symbolic names
2. **Uniqueness**: Use `uniqueString()` for globally unique names
3. **API Versions**: Use latest stable API versions
4. **Security**: Use managed identities, enable HTTPS/TLS, use private endpoints
5. **Modules**: Version your modules, use AVM when available

## Common Workflows

### New Bicep Template
1. Define parameters with descriptions and constraints
2. Create variables for computed values
3. Define resources with proper dependencies
4. Use modules for reusability
5. Output essential values (never secrets)
6. Test with `bicep build` and what-if deployment
