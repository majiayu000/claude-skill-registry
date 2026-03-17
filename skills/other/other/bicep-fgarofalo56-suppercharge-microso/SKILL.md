---
name: bicep
description: Expert assistance for Azure Bicep infrastructure-as-code. Provides best practices for authoring Bicep templates, Azure resource type discovery with API versions, resource schema retrieval, and Azure Verified Modules (AVM) guidance. Use when writing Bicep files, deploying Azure resources, looking up resource types/schemas, or working with AVM modules.
---

# Bicep Expert Assistant

Expert guidance for Azure Bicep infrastructure-as-code development, including best practices, resource type discovery, schema retrieval, and Azure Verified Modules.

## Core Capabilities

This skill provides four main functions equivalent to the Bicep MCP Server:

1. **Best Practices** - Comprehensive Bicep authoring guidelines
2. **Resource Type Discovery** - List Azure resource types with API versions
3. **Schema Retrieval** - Get detailed schemas for resource types
4. **AVM Metadata** - Azure Verified Modules information

## Instructions

### When User Asks About Bicep Best Practices

Provide guidance from the comprehensive best practices below. Focus on the specific area they're asking about (parameters, variables, resources, modules, naming, security, etc.).

### When User Needs Resource Types for a Provider

Run the helper script to list resource types:

```bash
# PowerShell
./scripts/get-resource-types.ps1 -Provider "Microsoft.Storage"

# Bash
./scripts/get-resource-types.sh "Microsoft.Storage"
```

Or use Azure CLI directly:
```bash
az provider show --namespace Microsoft.Storage --query "resourceTypes[].{Type:resourceType,ApiVersions:apiVersions[0]}" -o table
```

### When User Needs a Resource Schema

Use Bicep CLI to get the schema:
```bash
bicep build-params --stdout <<< "param resourceType string = 'Microsoft.Storage/storageAccounts@2023-05-01'"
```

Or reference the helper script in `scripts/get-resource-schema.ps1`

### When User Asks About Azure Verified Modules

Provide AVM guidance and help them find appropriate modules from the Bicep Public Registry.

---

## Bicep Best Practices Reference

### Parameters

1. **Use descriptive names**: Parameters should have clear, meaningful names that indicate their purpose
   ```bicep
   // Good
   param storageAccountName string
   param enableHttpsTrafficOnly bool = true

   // Avoid
   param san string
   param flag bool
   ```

2. **Provide descriptions**: Always add `@description()` decorator
   ```bicep
   @description('The name of the storage account. Must be globally unique.')
   param storageAccountName string
   ```

3. **Set safe defaults**: Default values should be secure and cost-effective
   ```bicep
   @description('The SKU for the storage account')
   @allowed(['Standard_LRS', 'Standard_GRS', 'Standard_ZRS', 'Premium_LRS'])
   param storageAccountSku string = 'Standard_LRS'
   ```

4. **Use constraints wisely**: Apply `@minLength()`, `@maxLength()`, `@minValue()`, `@maxValue()`
   ```bicep
   @minLength(3)
   @maxLength(24)
   param storageAccountName string
   ```

5. **Use `@allowed` sparingly**: Overly restrictive lists block valid deployments as Azure adds new SKUs

6. **Secure sensitive parameters**: Use `@secure()` for secrets
   ```bicep
   @secure()
   param adminPassword string
   ```

### Variables

1. **Use for computed values**: Variables simplify complex expressions
   ```bicep
   var storageAccountName = '${prefix}${uniqueString(resourceGroup().id)}'
   ```

2. **Use for repeated values**: Define once, use multiple times
   ```bicep
   var commonTags = {
     environment: environment
     project: projectName
     deployedBy: 'Bicep'
   }
   ```

3. **Typed variables** (Bicep 0.26+): Add types for clarity
   ```bicep
   var instanceCount int = environment == 'prod' ? 5 : 2
   ```

### Resources

1. **Use symbolic names without 'name' suffix**:
   ```bicep
   // Good
   resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {

   // Avoid
   resource storageAccountName 'Microsoft.Storage/storageAccounts@2023-05-01' = {
   ```

2. **Use latest stable API versions**: Check for the most recent stable API version

3. **Leverage implicit dependencies**: Bicep automatically handles dependencies when you reference resources
   ```bicep
   resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
     name: storageAccountName
     // ...
   }

   resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
     parent: storageAccount  // Implicit dependency
     name: 'default'
   }
   ```

4. **Use `existing` keyword for references**:
   ```bicep
   resource existingVnet 'Microsoft.Network/virtualNetworks@2023-09-01' existing = {
     name: vnetName
   }
   ```

### Child Resources

1. **Use nested declaration** (preferred):
   ```bicep
   resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
     name: storageAccountName
     // ...

     resource blobService 'blobServices' = {
       name: 'default'
     }
   }
   ```

2. **Or use parent property**:
   ```bicep
   resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
     parent: storageAccount
     name: 'default'
   }
   ```

### Modules

1. **Use modules for reusability**: Break large templates into focused modules
   ```bicep
   module storageModule 'modules/storage.bicep' = {
     name: 'storageDeployment'
     params: {
       storageAccountName: storageAccountName
       location: location
     }
   }
   ```

2. **Use Azure Verified Modules**: Leverage pre-built, tested modules from the Bicep Registry
   ```bicep
   module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
     name: 'storageDeployment'
     params: {
       name: storageAccountName
       location: location
     }
   }
   ```

3. **Version your modules**: Always pin to specific versions

### Naming Conventions

1. **Use camelCase** for parameters, variables, and symbolic names
2. **Use `uniqueString()` for unique names**:
   ```bicep
   var storageAccountName = 'st${uniqueString(resourceGroup().id)}'
   ```
3. **Add prefixes for context**: Include environment, project, or region prefixes
4. **Follow Azure naming constraints**: Check character limits and allowed characters

### Outputs

1. **Expose essential values**: Output what consumers need
   ```bicep
   output storageAccountId string = storageAccount.id
   output primaryEndpoints object = storageAccount.properties.primaryEndpoints
   ```

2. **Never output secrets**: Use Key Vault references instead
   ```bicep
   // WRONG - Never do this
   output connectionString string = storageAccount.listKeys().keys[0].value
   ```

### Security Best Practices

1. **Use managed identities** instead of credentials where possible
2. **Enable HTTPS/TLS** for all services
3. **Use private endpoints** for sensitive resources
4. **Apply least privilege** with RBAC assignments
5. **Enable diagnostic logging** and monitoring
6. **Use Key Vault** for secrets management
7. **Enable encryption** at rest and in transit

### Code Organization

1. **File structure**:
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

2. **Order of elements in files**:
   - Target scope (if not resourceGroup)
   - Parameters
   - Variables
   - Resources
   - Modules
   - Outputs

3. **Comments**: Use `//` for single-line, `/* */` for multi-line

---

## Azure Verified Modules (AVM)

### What is AVM?

Azure Verified Modules are pre-built, tested Bicep modules maintained by Microsoft that follow best practices and the Well-Architected Framework.

### Using AVM Modules

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

### Finding AVM Modules

1. Browse: https://azure.github.io/Azure-Verified-Modules/indexes/bicep/
2. GitHub: https://github.com/Azure/bicep-registry-modules
3. Registry: `mcr.microsoft.com` for container images

### Module Types

- **Resource Modules (`avm/res/`)**: Single Azure resource with all configurations
- **Pattern Modules (`avm/ptn/`)**: Multi-resource patterns for common scenarios
- **Utility Modules (`avm/utl/`)**: Helper types and functions

---

## Common Resource Type Examples

### Storage Account
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
    minimumTls  }
}
```

### Virtual Network
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

### Key Vault
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

---

## When to Use This Skill

- Writing or reviewing Bicep templates
- Looking up Azure resource types and API versions
- Finding the correct schema for a resource type
- Using Azure Verified Modules
- Applying Bicep best practices
- Deploying Azure infrastructure with IaC

## Keywords

bicep, azure, arm, infrastructure as code, iac, resource manager, deployment, template, module, avm, azure verified modules, resource type, schema, api version, storage account, virtual network, key vault, best practices
