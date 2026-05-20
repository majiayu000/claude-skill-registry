---
name: azure-mcp
description: Comprehensive Azure cloud management skill using Azure CLI. Manage 40+ Azure services including storage, databases, containers, monitoring, security, AI services, messaging, and infrastructure. Use for any Azure resource management, configuration, troubleshooting, or deployment tasks.
---

# Azure MCP - Comprehensive Azure Management Skill

Manage Azure resources using Azure CLI across all major services.

## Triggers

Use this skill when you see:
- azure, az cli, azure resource
- azure storage, blob, cosmos, keyvault
- azure aks, kubernetes, container
- azure monitor, log analytics
- azure sql, postgres, mysql
- event grid, service bus, functions
- app service, resource group, subscription

## Instructions

### Authentication

```bash
# Login interactively
az login

# Login with service principal
az login --service-principal \
    --username <APP_ID> \
    --password <PASSWORD> \
    --tenant <TENANT_ID>

# Login with managed identity
az login --identity

# Set subscription
az account set --subscription "My Subscription"

# List subscriptions
az account list --output table
```

### Resource Groups

```bash
# Create resource group
az group create --name mygroup --location eastus

# List resource groups
az group list --output table

# Delete resource group
az group delete --name mygroup --yes --no-wait

# List resources in group
az resource list --resource-group mygroup --output table
```

### Storage Accounts

```bash
# Create storage account
az storage account create \
    --name mystorageaccount \
    --resource-group mygroup \
    --location eastus \
    --sku Standard_LRS \
    --kind StorageV2

# List storage accounts
az storage account list --resource-group mygroup --output table

# Get connection string
az storage account show-connection-string \
    --name mystorageaccount \
    --resource-group mygroup

# Create container
az storage container create \
    --name mycontainer \
    --account-name mystorageaccount

# Upload blob
az storage blob upload \
    --account-name mystorageaccount \
    --container-name mycontainer \
    --name myblob \
    --file ./localfile.txt

# List blobs
az storage blob list \
    --account-name mystorageaccount \
    --container-name mycontainer \
    --output table
```

### Key Vault

```bash
# Create Key Vault
az keyvault create \
    --name mykeyvault \
    --resource-group mygroup \
    --location eastus \
    --enable-rbac-authorization

# Set secret
az keyvault secret set \
    --vault-name mykeyvault \
    --name mysecret \
    --value "secret-value"

# Get secret
az keyvault secret show \
    --vault-name mykeyvault \
    --name mysecret

# List secrets
az keyvault secret list --vault-name mykeyvault --output table

# Create key
az keyvault key create \
    --vault-name mykeyvault \
    --name mykey \
    --kty RSA \
    --size 2048
```

### App Service

```bash
# Create App Service plan
az appservice plan create \
    --name myplan \
    --resource-group mygroup \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --name mywebapp \
    --resource-group mygroup \
    --plan myplan \
    --runtime "PYTHON:3.11"

# Configure settings
az webapp config appsettings set \
    --name mywebapp \
    --resource-group mygroup \
    --settings KEY=value

# Deploy from Git
az webapp deployment source config \
    --name mywebapp \
    --resource-group mygroup \
    --repo-url https://github.com/org/repo \
    --branch main

# View logs
az webapp log tail \
    --name mywebapp \
    --resource-group mygroup
```

### Azure SQL

```bash
# Create SQL server
az sql server create \
    --name mysqlserver \
    --resource-group mygroup \
    --location eastus \
    --admin-user sqladmin \
    --admin-password "Password123!"

# Create database
az sql db create \
    --name mydb \
    --resource-group mygroup \
    --server mysqlserver \
    --service-objective S0

# Configure firewall
az sql server firewall-rule create \
    --name AllowAzure \
    --resource-group mygroup \
    --server mysqlserver \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

# Get connection string
az sql db show-connection-string \
    --server mysqlserver \
    --name mydb \
    --client ado.net
```

### Azure PostgreSQL

```bash
# Create PostgreSQL Flexible Server
az postgres flexible-server create \
    --name mypostgres \
    --resource-group mygroup \
    --location eastus \
    --admin-user pgadmin \
    --admin-password "Password123!" \
    --sku-name Standard_D2s_v3 \
    --tier GeneralPurpose \
    --storage-size 32

# Create database
az postgres flexible-server db create \
    --resource-group mygroup \
    --server-name mypostgres \
    --database-name mydb

# Configure firewall
az postgres flexible-server firewall-rule create \
    --resource-group mygroup \
    --name mypostgres \
    --rule-name AllowAll \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 255.255.255.255
```

### Virtual Networks

```bash
# Create VNet
az network vnet create \
    --name myvnet \
    --resource-group mygroup \
    --location eastus \
    --address-prefix 10.0.0.0/16 \
    --subnet-name default \
    --subnet-prefix 10.0.1.0/24

# Create subnet
az network vnet subnet create \
    --name mysubnet \
    --resource-group mygroup \
    --vnet-name myvnet \
    --address-prefix 10.0.2.0/24

# Create NSG
az network nsg create \
    --name mynsg \
    --resource-group mygroup \
    --location eastus

# Add NSG rule
az network nsg rule create \
    --name AllowHTTP \
    --nsg-name mynsg \
    --resource-group mygroup \
    --priority 100 \
    --destination-port-ranges 80 443 \
    --access Allow \
    --protocol Tcp
```

### Monitoring

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
    --workspace-name myworkspace \
    --resource-group mygroup \
    --location eastus

# Create alert rule
az monitor metrics alert create \
    --name "High CPU Alert" \
    --resource-group mygroup \
    --scopes /subscriptions/.../resourceGroups/mygroup/providers/Microsoft.Compute/virtualMachines/myvm \
    --condition "avg Percentage CPU > 80" \
    --window-size 5m \
    --evaluation-frequency 1m

# Query logs
az monitor log-analytics query \
    --workspace /subscriptions/.../workspaces/myworkspace \
    --analytics-query "AzureActivity | take 10"

# Create Application Insights
az monitor app-insights component create \
    --app myappinsights \
    --resource-group mygroup \
    --location eastus \
    --workspace /subscriptions/.../workspaces/myworkspace
```

### Service Bus

```bash
# Create namespace
az servicebus namespace create \
    --name myservicebus \
    --resource-group mygroup \
    --location eastus \
    --sku Standard

# Create queue
az servicebus queue create \
    --name myqueue \
    --namespace-name myservicebus \
    --resource-group mygroup

# Create topic and subscription
az servicebus topic create \
    --name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup

az servicebus topic subscription create \
    --name mysubscription \
    --topic-name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup

# Get connection string
az servicebus namespace authorization-rule keys list \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --name RootManageSharedAccessKey
```

### Identity and RBAC

```bash
# Create managed identity
az identity create \
    --name myidentity \
    --resource-group mygroup

# Assign role
az role assignment create \
    --assignee <PRINCIPAL_ID> \
    --role "Storage Blob Data Contributor" \
    --scope /subscriptions/.../resourceGroups/mygroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount

# List role assignments
az role assignment list \
    --scope /subscriptions/.../resourceGroups/mygroup \
    --output table

# Create service principal
az ad sp create-for-rbac \
    --name myserviceprincipal \
    --role Contributor \
    --scopes /subscriptions/.../resourceGroups/mygroup
```

### Container Registry

```bash
# Create ACR
az acr create \
    --name myacr \
    --resource-group mygroup \
    --sku Standard \
    --admin-enabled true

# Login to ACR
az acr login --name myacr

# Build image
az acr build \
    --registry myacr \
    --image myapp:v1 \
    .

# List repositories
az acr repository list --name myacr --output table

# List tags
az acr repository show-tags --name myacr --repository myapp
```

## Best Practices

1. **Resource Groups**: Organize resources by lifecycle and management
2. **Tags**: Use tags for cost allocation and organization
3. **RBAC**: Follow least privilege principle
4. **Monitoring**: Enable diagnostics and alerts
5. **Networking**: Use private endpoints for sensitive resources

## Common Workflows

### Deploy Application Stack
1. Create resource group
2. Set up networking (VNet, subnets)
3. Deploy database services
4. Deploy application (App Service, Container Apps)
5. Configure monitoring and alerts

### Manage Resources
1. List resources: `az resource list`
2. View details: `az resource show`
3. Update settings: `az resource update`
4. Delete: `az resource delete`
5. Monitor: `az monitor`
