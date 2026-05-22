---
name: deployment-stacks-2025
description: Azure Deployment Stacks GA 2025 features for unified resource management, deny settings, and lifecycle management
---

# Azure Deployment Stacks - 2025 GA Features

Complete knowledge base for Azure Deployment Stacks, the successor to Azure Blueprints (GA 2024, best practices 2025).

## Overview

Azure Deployment Stacks is a resource type for managing a collection of Azure resources as a single, atomic unit. It provides unified lifecycle management, resource protection, and automatic cleanup capabilities.

## Key Features

### 1. Unified Resource Management
- Manage multiple resources as a single entity
- Update, export, and delete operations on the entire stack
- Track all managed resources in one place
- Consistent deployment across environments

### 2. Deny Settings (Resource Protection)
Prevent unauthorized modifications to managed resources:
- **None**: No restrictions (default)
- **DenyDelete**: Prevent resource deletion
- **DenyWriteAndDelete**: Prevent updates and deletions

### 3. ActionOnUnmanage (Cleanup Policies)
Control what happens to resources no longer in template:
- **detachAll**: Remove from stack management, keep resources
- **deleteAll**: Delete resources not in template
- **deleteResources**: Delete unmanaged resources, keep resource groups

### 4. Scope Flexibility
Deploy stacks at:
- Resource group scope
- Subscription scope
- Management group scope

### 5. Replaces Azure Blueprints
Azure Blueprints will be deprecated in **July 2026**. Deployment Stacks is the recommended replacement.

## Prerequisites

### Azure CLI Version
```bash
# Requires Azure CLI 2.61.0 or later
az version

# Upgrade if needed
az upgrade
```

### Azure PowerShell Version
```bash
# Requires Azure PowerShell 12.0.0 or later
Get-InstalledModule -Name Az
Update-Module -Name Az
```

## Creating Deployment Stacks

### Subscription Scope Stack

```bash
# Create deployment stack at subscription level
az stack sub create \
  --name MyProductionStack \
  --location eastus \
  --template-file main.bicep \
  --parameters @parameters.json \
  --deny-settings-mode DenyWriteAndDelete \
  --deny-settings-excluded-principals <devops-service-principal-id> <admin-group-id> \
  --action-on-unmanage deleteAll \
  --description "Production infrastructure managed by deployment stack" \
  --tags Environment=Production ManagedBy=DeploymentStack CostCenter=Engineering

# What-if analysis before deployment
az stack sub what-if \
  --name MyProductionStack \
  --location eastus \
  --template-file main.bicep \
  --parameters @parameters.json

# Create with confirmation prompt disabled
az stack sub create \
  --name MyDevStack \
  --location eastus \
  --template-file main.bicep \
  --deny-settings-mode None \
  --action-on-unmanage detachAll \
  --yes
```

### Resource Group Scope Stack

```bash
# Create resource group
az group create \
  --name MyRG \
  --location eastus \
  --tags Environment=Production

# Create deployment stack
az stack group create \
  --name MyAppStack \
  --resource-group MyRG \
  --template-file main.bicep \
  --parameters environment=production \
  --deny-settings-mode DenyDelete \
  --action-on-unmanage deleteAll \
  --description "Application infrastructure stack"
```

### Management Group Scope Stack

```bash
# Create stack at management group level
az stack mg create \
  --name MyEnterpriseStack \
  --management-group-id MyMgmtGroup \
  --location eastus \
  --template-file main.bicep \
  --deny-settings-mode DenyWriteAndDelete \
  --action-on-unmanage detachAll
```

## Bicep Template for Deployment Stack

### Production Stack Template

```bicep
// main.bicep
targetScope = 'subscription'

@description('Environment name')
@allowed([
  'dev'
  'staging'
  'production'
])
param environment string = 'production'

@description('Primary location')
param location string = 'eastus'

@description('Secondary location for geo-replication')
param secondaryLocation string = 'westus'

// Resource naming
var namingPrefix = 'myapp-${environment}'

// Resource Group for core infrastructure
resource coreRG 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: '${namingPrefix}-core-rg'
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'DeploymentStack'
    Purpose: 'Core Infrastructure'
  }
}

// Resource Group for data services
resource dataRG 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: '${namingPrefix}-data-rg'
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'DeploymentStack'
    Purpose: 'Data Services'
  }
}

// Log Analytics Workspace
module logAnalytics 'modules/log-analytics.bicep' = {
  name: 'logAnalyticsDeploy'
  scope: coreRG
  params: {
    name: '${namingPrefix}-logs'
    location: location
    retentionInDays: environment == 'production' ? 90 : 30
  }
}

// AKS Automatic Cluster
module aksCluster 'modules/aks-automatic.bicep' = {
  name: 'aksClusterDeploy'
  scope: coreRG
  params: {
    name: '${namingPrefix}-aks'
    location: location
    kubernetesVersion: '1.34'
    workspaceId: logAnalytics.outputs.workspaceId
    enableZoneRedundancy: environment == 'production'
  }
}

// Container Apps Environment
module containerEnv 'modules/container-env.bicep' = {
  name: 'containerEnvDeploy'
  scope: coreRG
  params: {
    name: '${namingPrefix}-containerenv'
    location: location
    workspaceId: logAnalytics.outputs.workspaceId
    zoneRedundant: environment == 'production'
  }
}

// Azure OpenAI
module openAI 'modules/openai.bicep' = {
  name: 'openAIDeploy'
  scope: dataRG
  params: {
    name: '${namingPrefix}-openai'
    location: location
    deployGPT5: environment == 'production'
  }
}

// Cosmos DB with geo-replication
module cosmosDB 'modules/cosmos-db.bicep' = {
  name: 'cosmosDBDeploy'
  scope: dataRG
  params: {
    name: '${namingPrefix}-cosmos'
    primaryLocation: location
    secondaryLocation: secondaryLocation
    enableAutomaticFailover: environment == 'production'
  }
}

// Key Vault
module keyVault 'modules/key-vault.bicep' = {
  name: 'keyVaultDeploy'
  scope: coreRG
  params: {
    name: '${namingPrefix}-kv'
    location: location
    enablePurgeProtection: environment == 'production'
  }
}

// Outputs
output aksClusterName string = aksCluster.outputs.clusterName
output containerEnvId string = containerEnv.outputs.environmentId
output openAIEndpoint string = openAI.outputs.endpoint
output cosmosDBEndpoint string = cosmosDB.outputs.endpoint
output keyVaultUri string = keyVault.outputs.vaultUri
```

### AKS Automatic Module

```bicep
// modules/aks-automatic.bicep
@description('Cluster name')
param name string

@description('Location')
param location string

@description('Kubernetes version')
param kubernetesVersion string = '1.34'

@description('Log Analytics workspace ID')
param workspaceId string

@description('Enable zone redundancy')
param enableZoneRedundancy bool = true

resource aksCluster 'Microsoft.ContainerService/managedClusters@2025-01-01' = {
  name: name
  location: location
  sku: {
    name: 'Automatic'
    tier: 'Standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    kubernetesVersion: kubernetesVersion
    dnsPrefix: '${name}-dns'
    enableRBAC: true
    aadProfile: {
      managed: true
      enableAzureRBAC: true
    }
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'
      networkDataplane: 'cilium'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
    }
    autoScalerProfile: {
      'balance-similar-node-groups': 'true'
      expander: 'least-waste'
    }
    autoUpgradeProfile: {
      upgradeChannel: 'stable'
      nodeOSUpgradeChannel: 'NodeImage'
    }
    securityProfile: {
      defender: {
        securityMonitoring: {
          enabled: true
        }
      }
      workloadIdentity: {
        enabled: true
      }
    }
    oidcIssuerProfile: {
      enabled: true
    }
    addonProfiles: {
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: workspaceId
        }
      }
      azurePolicy: {
        enabled: true
      }
    }
  }
  zones: enableZoneRedundancy ? ['1', '2', '3'] : null
}

output clusterName string = aksCluster.name
output clusterId string = aksCluster.id
output oidcIssuerUrl string = aksCluster.properties.oidcIssuerProfile.issuerUrl
output kubeletIdentity string = aksCluster.properties.identityProfile.kubeletidentity.objectId
```

## Managing Deployment Stacks

### Update Stack

```bash
# Update with new template version
az stack sub update \
  --name MyProductionStack \
  --template-file main.bicep \
  --parameters @parameters.json \
  --action-on-unmanage deleteAll

# Update deny settings
az stack sub update \
  --name MyProductionStack \
  --deny-settings-mode DenyWriteAndDelete \
  --deny-settings-excluded-principals <new-principal-id>
```

### View Stack Details

```bash
# Show stack information
az stack sub show \
  --name MyProductionStack \
  --output json

# List all stacks in subscription
az stack sub list --output table

# List stacks in resource group
az stack group list \
  --resource-group MyRG \
  --output table
```

### Export Stack Template

```bash
# Export template from deployed stack
az stack sub export \
  --name MyProductionStack \
  --output-file exported-stack.json

# Export and save parameters
az stack sub show \
  --name MyProductionStack \
  --query "parameters" \
  --output json > parameters-backup.json
```

### Delete Stack

```bash
# Delete stack and all managed resources
az stack sub delete \
  --name MyProductionStack \
  --action-on-unmanage deleteAll \
  --yes

# Delete stack but keep resources
az stack sub delete \
  --name MyProductionStack \
  --action-on-unmanage detachAll \
  --yes

# Delete with confirmation prompt
az stack sub delete --name MyProductionStack
```

## Deny Settings in Detail

### DenyDelete Mode

Prevents deletion but allows updates:

```bash
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --deny-settings-mode DenyDelete \
  --deny-settings-excluded-principals \
    <emergency-access-principal-id> \
    <devops-service-principal-id>
```

**Use cases:**
- Protect production databases
- Prevent accidental resource deletion
- Allow configuration updates

### DenyWriteAndDelete Mode

Prevents both updates and deletions:

```bash
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --deny-settings-mode DenyWriteAndDelete \
  --deny-settings-excluded-principals <break-glass-principal-id>
```

**Use cases:**
- Immutable infrastructure
- Compliance requirements
- Critical production workloads

### Excluded Principals

Bypass deny settings for specific identities:

```bash
# Get principal IDs
SERVICE_PRINCIPAL_ID=$(az ad sp show --id <app-id> --query id -o tsv)
ADMIN_GROUP_ID=$(az ad group show --group "Cloud Admins" --query id -o tsv)

# Apply with exclusions
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --deny-settings-mode DenyWriteAndDelete \
  --deny-settings-excluded-principals $SERVICE_PRINCIPAL_ID $ADMIN_GROUP_ID
```

## ActionOnUnmanage Policies

### detachAll

Resources are removed from stack management but not deleted:

```bash
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --action-on-unmanage detachAll
```

**Use when:**
- Testing deployment changes
- Migrating resources to another stack
- Temporary stack management

### deleteAll

All unmanaged resources are deleted:

```bash
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --action-on-unmanage deleteAll
```

**Use when:**
- Ephemeral environments (dev, test)
- Clean slate deployments
- Strict infrastructure-as-code enforcement

### deleteResources

Delete resources but keep resource groups:

```bash
az stack sub create \
  --name MyStack \
  --location eastus \
  --template-file main.bicep \
  --action-on-unmanage deleteResources
```

## RBAC for Deployment Stacks

### Built-in Roles

**Azure Deployment Stack Contributor**
- Manage deployment stacks
- Cannot create or delete deny-assignments

**Azure Deployment Stack Owner**
- Full stack management
- Can create and delete deny-assignments

### Assign Roles

```bash
# Assign Stack Contributor role
az role assignment create \
  --assignee <user-or-service-principal-id> \
  --role "Azure Deployment Stack Contributor" \
  --scope /subscriptions/<subscription-id>

# Assign Stack Owner role
az role assignment create \
  --assignee <admin-principal-id> \
  --role "Azure Deployment Stack Owner" \
  --scope /subscriptions/<subscription-id>
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Deployment Stack

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: What-if Analysis
        run: |
          az stack sub what-if \
            --name MyProductionStack \
            --location eastus \
            --template-file main.bicep \
            --parameters @parameters.json

      - name: Deploy Stack
        run: |
          az stack sub create \
            --name MyProductionStack \
            --location eastus \
            --template-file main.bicep \
            --parameters @parameters.json \
            --deny-settings-mode DenyWriteAndDelete \
            --deny-settings-excluded-principals ${{ secrets.DEVOPS_PRINCIPAL_ID }} \
            --action-on-unmanage deleteAll \
            --yes
```

### Azure DevOps Pipeline

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureSubscription: 'MyAzureConnection'
  stackName: 'MyProductionStack'
  location: 'eastus'

steps:
  - task: AzureCLI@2
    displayName: 'What-if Analysis'
    inputs:
      azureSubscription: $(azureSubscription)
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az stack sub what-if \
          --name $(stackName) \
          --location $(location) \
          --template-file main.bicep \
          --parameters @parameters.json

  - task: AzureCLI@2
    displayName: 'Deploy Stack'
    inputs:
      azureSubscription: $(azureSubscription)
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az stack sub create \
          --name $(stackName) \
          --location $(location) \
          --template-file main.bicep \
          --parameters @parameters.json \
          --deny-settings-mode DenyWriteAndDelete \
          --action-on-unmanage deleteAll \
          --yes
```

## Monitoring and Auditing

### View Stack Events

```bash
# Get deployment operations
az stack sub show \
  --name MyProductionStack \
  --query "deploymentId" \
  --output tsv | \
  xargs -I {} az deployment sub show --name {}

# List managed resources
az stack sub show \
  --name MyProductionStack \
  --query "resources[].id" \
  --output table
```

### Activity Logs

```bash
# Query stack operations
az monitor activity-log list \
  --resource-group MyRG \
  --namespace Microsoft.Resources \
  --start-time 2025-01-01T00:00:00Z \
  --query "[?contains(authorization.action, 'Microsoft.Resources/deploymentStacks')]" \
  --output table
```

## Migration from Azure Blueprints

### Assessment

1. **Inventory Blueprints**: List all blueprints and assignments
2. **Document Parameters**: Export parameters and configurations
3. **Plan Conversion**: Map blueprints to deployment stacks
4. **Test in Dev**: Validate converted templates

### Conversion Steps

```bash
# 1. Export Blueprint as ARM template
# (Use Azure Portal or PowerShell)

# 2. Convert ARM to Bicep
az bicep decompile --file blueprint-template.json

# 3. Create Deployment Stack
az stack sub create \
  --name ConvertedFromBlueprint \
  --location eastus \
  --template-file converted.bicep \
  --parameters @blueprint-parameters.json \
  --deny-settings-mode DenyWriteAndDelete \
  --action-on-unmanage detachAll

# 4. Validate resources
az stack sub show --name ConvertedFromBlueprint

# 5. Delete Blueprint assignment (after validation)
# Remove-AzBlueprintAssignment -Name MyBlueprintAssignment
```

## Best Practices

✓ **Use Deployment Stacks for all new infrastructure**
✓ **Always run what-if analysis before deployment**
✓ **Use DenyWriteAndDelete for production stacks**
✓ **Exclude break-glass principals from deny settings**
✓ **Tag stacks with Environment, CostCenter, Owner**
✓ **Use deleteAll for ephemeral environments**
✓ **Use detachAll for migration scenarios**
✓ **Implement CI/CD pipelines for stack deployment**
✓ **Monitor stack operations via activity logs**
✓ **Document stack architecture and dependencies**

## Troubleshooting

### Stack Creation Fails

```bash
# Check deployment errors
az stack sub show \
  --name MyStack \
  --query "error" \
  --output json

# Validate template
az deployment sub validate \
  --location eastus \
  --template-file main.bicep \
  --parameters @parameters.json
```

### Deny Settings Blocking Operations

```bash
# Check deny assignments
az role assignment list \
  --scope /subscriptions/<subscription-id> \
  --include-inherited \
  --query "[?type=='Microsoft.Authorization/denyAssignments']"

# Add principal to exclusions
az stack sub update \
  --name MyStack \
  --deny-settings-excluded-principals <new-principal-id>
```

### Resources Not Deleted

```bash
# Check action-on-unmanage setting
az stack sub show \
  --name MyStack \
  --query "actionOnUnmanage" \
  --output tsv

# Update to deleteAll
az stack sub update \
  --name MyStack \
  --action-on-unmanage deleteAll
```

## References

- [Deployment Stacks Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks)
- [Deployment Stacks Quickstart](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/quickstart-create-deployment-stacks)
- [Migrate from Blueprints](https://learn.microsoft.com/en-us/azure/governance/blueprints/how-to/migrate-to-deployment-stacks)

Deployment Stacks represents the future of Azure infrastructure lifecycle management!
