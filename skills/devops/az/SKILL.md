---
name: az
description: Use az CLI for Azure cloud resource management, Azure DevOps operations, VMs, storage, networking, AKS, and Key Vault with comprehensive authentication and output control.
---
# Azure CLI (az) Skill

You are an Azure CLI specialist. This skill provides comprehensive guidance for managing Azure resources, Azure DevOps, and cloud infrastructure using the `az` command-line tool.

## Core Principles

### Authentication

Always ensure proper authentication before running Azure commands:
- Use `az login` for interactive authentication
- Use `az account show` to verify current subscription
- Use `az account set` to switch subscriptions
- Service principal authentication for automation

### Output Formats

Azure CLI supports multiple output formats:
- `--output table` - Human-readable table (default for many commands)
- `--output json` - Full JSON output for scripting
- `--output tsv` - Tab-separated values for parsing
- `--output yaml` - YAML format
- `--output jsonc` - Colorized JSON
- `-o` - Short form for `--output`

### Query and Filtering

Use JMESPath queries with `--query` to filter results:
```bash
az vm list --query "[?location=='eastus'].name" -o table
az resource list --query "[?type=='Microsoft.Compute/virtualMachines']"
```

## Authentication and Account Management

### Login and Authentication

```bash
# Interactive login
az login

# Login with specific tenant
az login --tenant <tenant-id>

# Login with service principal
az login --service-principal -u <app-id> -p <password-or-cert> --tenant <tenant-id>

# Login with managed identity
az login --identity

# Check authentication status
az account show

# List all accessible subscriptions
az account list -o table
```

### Subscription Management

```bash
# Show current subscription
az account show

# List all subscriptions
az account list -o table

# Set active subscription
az account set --subscription <subscription-id-or-name>

# Show subscription details
az account show --query "{SubscriptionName:name, SubscriptionId:id, TenantId:tenantId}"
```

### Service Principal Management

```bash
# Create service principal
az ad sp create-for-rbac --name <name>

# Create with specific role
az ad sp create-for-rbac --name <name> --role contributor --scopes /subscriptions/<subscription-id>

# List service principals
az ad sp list --display-name <name>

# Delete service principal
az ad sp delete --id <app-id>

# Reset credentials
az ad sp credential reset --id <app-id>
```

## Resource Management

### Resource Groups

```bash
# List resource groups
az group list -o table

# Create resource group
az group create --name <name> --location <location>

# Show resource group
az group show --name <name>

# Delete resource group
az group delete --name <name> --yes --no-wait

# Update tags
az group update --name <name> --tags Environment=Dev Project=MyApp

# List resources in group
az resource list --resource-group <name> -o table

# Export resource group template
az group export --name <name>
```

### Generic Resource Operations

```bash
# List all resources
az resource list -o table

# List resources by type
az resource list --resource-type Microsoft.Compute/virtualMachines -o table

# Show resource
az resource show --ids <resource-id>
az resource show --resource-group <group> --name <name> --resource-type <type>

# Update resource tags
az resource tag --tags Environment=Prod --ids <resource-id>

# Delete resource
az resource delete --ids <resource-id>

# Move resources
az resource move --destination-group <dest-group> --ids <resource-id1> <resource-id2>
```

### Locations and Providers

```bash
# List available locations
az account list-locations -o table

# List resource providers
az provider list -o table

# Show provider
az provider show --namespace Microsoft.Compute

# Register provider
az provider register --namespace Microsoft.Compute

# Check registration status
az provider show --namespace Microsoft.Compute --query "registrationState"
```

## Azure DevOps

### DevOps Configuration

```bash
# Configure default organization and project
az devops configure --defaults organization=https://dev.azure.com/myorg project=MyProject

# Show current defaults
az devops configure --list

# Login to Azure DevOps
az devops login --organization https://dev.azure.com/myorg
```

### Projects

```bash
# List projects
az devops project list --organization https://dev.azure.com/myorg -o table

# Create project
az devops project create --name <name>

# Show project
az devops project show --project <name>

# Delete project
az devops project delete --id <project-id> --yes
```

### Repositories

```bash
# List repositories
az repos list --organization https://dev.azure.com/myorg --project <project> -o table

# Show repository
az repos show --repository <repo-name>

# Create repository
az repos create --name <name> --project <project>

# Delete repository
az repos delete --id <repo-id> --yes

# Import repository
az repos import create --git-source-url <url> --repository <repo-name>

# List branches
az repos ref list --repository <repo-name>

# List pull requests
az repos pr list --repository <repo-name> -o table
```

### Pipelines

```bash
# List pipelines
az pipelines list --organization https://dev.azure.com/myorg --project <project> -o table

# Show pipeline
az pipelines show --name <pipeline-name>

# Run pipeline
az pipelines run --name <pipeline-name>

# List pipeline runs
az pipelines runs list -o table

# Show run details
az pipelines runs show --id <run-id>

# List build definitions
az pipelines build list -o table

# Queue build
az pipelines build queue --definition-name <name>
```

## Virtual Machines

### VM Management

```bash
# List VMs
az vm list -o table
az vm list --resource-group <group> -o table

# Show VM
az vm show --resource-group <group> --name <vm-name>

# Create VM (basic)
az vm create \
  --resource-group <group> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys

# Create VM (detailed)
az vm create \
  --resource-group <group> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_DS2_v2 \
  --admin-username azureuser \
  --ssh-key-values @~/.ssh/id_rsa.pub \
  --vnet-name myVnet \
  --subnet mySubnet \
  --public-ip-address myPublicIP \
  --nsg myNSG

# Start VM
az vm start --resource-group <group> --name <vm-name>

# Stop VM (deallocate)
az vm deallocate --resource-group <group> --name <vm-name>

# Stop VM (without deallocate)
az vm stop --resource-group <group> --name <vm-name>

# Restart VM
az vm restart --resource-group <group> --name <vm-name>

# Delete VM
az vm delete --resource-group <group> --name <vm-name> --yes

# Resize VM
az vm resize --resource-group <group> --name <vm-name> --size Standard_DS3_v2

# List available sizes
az vm list-sizes --location eastus -o table
```

### VM Images

```bash
# List popular images
az vm image list -o table

# List all images from publisher
az vm image list --publisher Canonical --all -o table

# Show image details
az vm image show --urn Canonical:Ubuntu2204:latest

# List VM SKUs
az vm list-skus --location eastus --size Standard_D -o table
```

### VM Extensions

```bash
# List extensions on VM
az vm extension list --resource-group <group> --vm-name <vm-name>

# Install extension
az vm extension set \
  --resource-group <group> \
  --vm-name <vm-name> \
  --name customScript \
  --publisher Microsoft.Azure.Extensions

# Delete extension
az vm extension delete --resource-group <group> --vm-name <vm-name> --name <extension-name>
```

## Storage

### Storage Accounts

```bash
# List storage accounts
az storage account list -o table

# Create storage account
az storage account create \
  --name <account-name> \
  --resource-group <group> \
  --location eastus \
  --sku Standard_LRS

# Show storage account
az storage account show --name <account-name>

# Get connection string
az storage account show-connection-string --name <account-name>

# Get access keys
az storage account keys list --account-name <account-name>

# Delete storage account
az storage account delete --name <account-name> --yes
```

### Blob Storage

```bash
# List containers
az storage container list --account-name <account-name> -o table

# Create container
az storage container create --name <container-name> --account-name <account-name>

# Upload blob
az storage blob upload \
  --account-name <account-name> \
  --container-name <container-name> \
  --name <blob-name> \
  --file <local-file-path>

# Download blob
az storage blob download \
  --account-name <account-name> \
  --container-name <container-name> \
  --name <blob-name> \
  --file <local-file-path>

# List blobs
az storage blob list --account-name <account-name> --container-name <container-name> -o table

# Delete blob
az storage blob delete --account-name <account-name> --container-name <container-name> --name <blob-name>

# Copy blob
az storage blob copy start \
  --account-name <dest-account> \
  --destination-container <dest-container> \
  --destination-blob <dest-blob> \
  --source-uri <source-blob-url>
```

## Networking

### Virtual Networks

```bash
# List vnets
az network vnet list -o table

# Create vnet
az network vnet create \
  --resource-group <group> \
  --name <vnet-name> \
  --address-prefix 10.0.0.0/16 \
  --subnet-name <subnet-name> \
  --subnet-prefix 10.0.1.0/24

# Show vnet
az network vnet show --resource-group <group> --name <vnet-name>

# Delete vnet
az network vnet delete --resource-group <group> --name <vnet-name>

# List subnets
az network vnet subnet list --resource-group <group> --vnet-name <vnet-name> -o table

# Create subnet
az network vnet subnet create \
  --resource-group <group> \
  --vnet-name <vnet-name> \
  --name <subnet-name> \
  --address-prefix 10.0.2.0/24
```

### Network Security Groups (NSGs)

```bash
# List NSGs
az network nsg list -o table

# Create NSG
az network nsg create --resource-group <group> --name <nsg-name>

# List NSG rules
az network nsg rule list --resource-group <group> --nsg-name <nsg-name> -o table

# Create NSG rule
az network nsg rule create \
  --resource-group <group> \
  --nsg-name <nsg-name> \
  --name <rule-name> \
  --priority 100 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 80 \
  --access Allow \
  --protocol Tcp \
  --description "Allow HTTP"

# Delete NSG rule
az network nsg rule delete --resource-group <group> --nsg-name <nsg-name> --name <rule-name>
```

### Public IPs and Load Balancers

```bash
# List public IPs
az network public-ip list -o table

# Create public IP
az network public-ip create --resource-group <group> --name <ip-name>

# Show public IP address
az network public-ip show --resource-group <group> --name <ip-name> --query "ipAddress"

# List load balancers
az network lb list -o table

# Create load balancer
az network lb create \
  --resource-group <group> \
  --name <lb-name> \
  --sku Standard \
  --public-ip-address <ip-name>
```

## App Services

### Web Apps

```bash
# List app service plans
az appservice plan list -o table

# Create app service plan
az appservice plan create \
  --name <plan-name> \
  --resource-group <group> \
  --sku B1 \
  --is-linux

# List web apps
az webapp list -o table

# Create web app
az webapp create \
  --resource-group <group> \
  --plan <plan-name> \
  --name <app-name> \
  --runtime "NODE:18-lts"

# Show web app
az webapp show --resource-group <group> --name <app-name>

# Deploy from Git
az webapp deployment source config \
  --name <app-name> \
  --resource-group <group> \
  --repo-url <git-url> \
  --branch main \
  --manual-integration

# Deploy ZIP file
az webapp deployment source config-zip \
  --resource-group <group> \
  --name <app-name> \
  --src <zip-file-path>

# Start/stop/restart web app
az webapp start --resource-group <group> --name <app-name>
az webapp stop --resource-group <group> --name <app-name>
az webapp restart --resource-group <group> --name <app-name>

# View logs
az webapp log tail --resource-group <group> --name <app-name>

# Delete web app
az webapp delete --resource-group <group> --name <app-name>
```

### App Settings and Configuration

```bash
# List app settings
az webapp config appsettings list --name <app-name> --resource-group <group>

# Set app settings
az webapp config appsettings set \
  --name <app-name> \
  --resource-group <group> \
  --settings KEY1=value1 KEY2=value2

# Delete app setting
az webapp config appsettings delete \
  --name <app-name> \
  --resource-group <group> \
  --setting-names KEY1

# Set connection strings
az webapp config connection-string set \
  --name <app-name> \
  --resource-group <group> \
  --connection-string-type SQLAzure \
  --settings DefaultConnection="connection-string-value"
```

## Container Services (AKS)

### AKS Cluster Management

```bash
# List AKS clusters
az aks list -o table

# Create AKS cluster
az aks create \
  --resource-group <group> \
  --name <cluster-name> \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get AKS credentials
az aks get-credentials --resource-group <group> --name <cluster-name>

# Show AKS cluster
az aks show --resource-group <group> --name <cluster-name>

# Scale AKS cluster
az aks scale --resource-group <group> --name <cluster-name> --node-count 5

# Upgrade AKS cluster
az aks upgrade --resource-group <group> --name <cluster-name> --kubernetes-version 1.28.0

# Stop AKS cluster
az aks stop --resource-group <group> --name <cluster-name>

# Start AKS cluster
az aks start --resource-group <group> --name <cluster-name>

# Delete AKS cluster
az aks delete --resource-group <group> --name <cluster-name> --yes
```

### Container Registry (ACR)

```bash
# List container registries
az acr list -o table

# Create container registry
az acr create --resource-group <group> --name <registry-name> --sku Basic

# Login to registry
az acr login --name <registry-name>

# List repositories
az acr repository list --name <registry-name> -o table

# Show repository tags
az acr repository show-tags --name <registry-name> --repository <repo-name>

# Delete image
az acr repository delete --name <registry-name> --image <repo-name>:<tag> --yes

# Import image
az acr import \
  --name <registry-name> \
  --source docker.io/library/nginx:latest \
  --image nginx:latest
```

## Databases

### SQL Databases

```bash
# List SQL servers
az sql server list -o table

# Create SQL server
az sql server create \
  --name <server-name> \
  --resource-group <group> \
  --location eastus \
  --admin-user <admin-user> \
  --admin-password <admin-password>

# List databases
az sql db list --resource-group <group> --server <server-name> -o table

# Create database
az sql db create \
  --resource-group <group> \
  --server <server-name> \
  --name <db-name> \
  --service-objective S0

# Show connection string
az sql db show-connection-string \
  --client ado.net \
  --name <db-name> \
  --server <server-name>

# Configure firewall rule
az sql server firewall-rule create \
  --resource-group <group> \
  --server <server-name> \
  --name AllowMyIP \
  --start-ip-address <ip> \
  --end-ip-address <ip>
```

### Cosmos DB

```bash
# List Cosmos DB accounts
az cosmosdb list -o table

# Create Cosmos DB account
az cosmosdb create \
  --name <account-name> \
  --resource-group <group> \
  --kind GlobalDocumentDB

# List databases
az cosmosdb sql database list \
  --account-name <account-name> \
  --resource-group <group>

# Create database
az cosmosdb sql database create \
  --account-name <account-name> \
  --resource-group <group> \
  --name <db-name>

# Get connection strings
az cosmosdb keys list \
  --name <account-name> \
  --resource-group <group> \
  --type connection-strings
```

## Monitoring and Logs

### Activity Logs

```bash
# List activity logs
az monitor activity-log list -o table

# List activity logs for resource group
az monitor activity-log list --resource-group <group> -o table

# List recent activity logs
az monitor activity-log list --start-time 2024-01-01T00:00:00Z -o table

# Query specific operations
az monitor activity-log list --filters "eventName eq 'Create or Update Virtual Machine'"
```

### Metrics

```bash
# List available metrics
az monitor metrics list-definitions --resource <resource-id>

# Get metric values
az monitor metrics list \
  --resource <resource-id> \
  --metric "Percentage CPU" \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z

# List metric alerts
az monitor metrics alert list -o table

# Create metric alert
az monitor metrics alert create \
  --name <alert-name> \
  --resource-group <group> \
  --scopes <resource-id> \
  --condition "avg Percentage CPU > 80" \
  --description "Alert when CPU exceeds 80%"
```

### Log Analytics

```bash
# List workspaces
az monitor log-analytics workspace list -o table

# Create workspace
az monitor log-analytics workspace create \
  --resource-group <group> \
  --workspace-name <workspace-name>

# Query logs
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AzureActivity | limit 10"

# List tables
az monitor log-analytics workspace table list \
  --resource-group <group> \
  --workspace-name <workspace-name>
```

## Azure Functions

### Function Apps

```bash
# List function apps
az functionapp list -o table

# Create function app
az functionapp create \
  --resource-group <group> \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 18 \
  --functions-version 4 \
  --name <function-app-name> \
  --storage-account <storage-account-name>

# Deploy function
az functionapp deployment source config-zip \
  --resource-group <group> \
  --name <function-app-name> \
  --src <zip-file-path>

# List functions
az functionapp function list --resource-group <group> --name <function-app-name>

# Show function
az functionapp function show \
  --resource-group <group> \
  --name <function-app-name> \
  --function-name <function-name>

# Start/stop function app
az functionapp start --resource-group <group> --name <function-app-name>
az functionapp stop --resource-group <group> --name <function-app-name>

# View logs
az functionapp log tail --resource-group <group> --name <function-app-name>
```

## Key Vault

### Key Vault Management

```bash
# List key vaults
az keyvault list -o table

# Create key vault
az keyvault create \
  --name <vault-name> \
  --resource-group <group> \
  --location eastus

# Show key vault
az keyvault show --name <vault-name>

# Delete key vault
az keyvault delete --name <vault-name>

# Purge deleted vault
az keyvault purge --name <vault-name>
```

### Secrets Management

```bash
# List secrets
az keyvault secret list --vault-name <vault-name> -o table

# Set secret
az keyvault secret set --vault-name <vault-name> --name <secret-name> --value <secret-value>

# Get secret
az keyvault secret show --vault-name <vault-name> --name <secret-name>

# Get secret value only
az keyvault secret show --vault-name <vault-name> --name <secret-name> --query "value" -o tsv

# Delete secret
az keyvault secret delete --vault-name <vault-name> --name <secret-name>

# List secret versions
az keyvault secret list-versions --vault-name <vault-name> --name <secret-name>
```

### Keys and Certificates

```bash
# List keys
az keyvault key list --vault-name <vault-name> -o table

# Create key
az keyvault key create --vault-name <vault-name> --name <key-name> --protection software

# List certificates
az keyvault certificate list --vault-name <vault-name> -o table

# Import certificate
az keyvault certificate import \
  --vault-name <vault-name> \
  --name <cert-name> \
  --file <cert-file-path>
```

## Role-Based Access Control (RBAC)

### Role Assignments

```bash
# List role assignments
az role assignment list -o table

# List role assignments for resource group
az role assignment list --resource-group <group> -o table

# Create role assignment
az role assignment create \
  --assignee <user-email-or-sp-id> \
  --role "Contributor" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<group>

# Create role assignment for subscription
az role assignment create \
  --assignee <user-email-or-sp-id> \
  --role "Reader" \
  --subscription <subscription-id>

# Delete role assignment
az role assignment delete \
  --assignee <user-email-or-sp-id> \
  --role "Contributor" \
  --resource-group <group>
```

### Role Definitions

```bash
# List role definitions
az role definition list -o table

# List built-in roles
az role definition list --query "[?type=='BuiltInRole'].{Name:roleName}" -o table

# Show role definition
az role definition list --name "Contributor"

# Create custom role
az role definition create --role-definition <json-file-path>

# Update custom role
az role definition update --role-definition <json-file-path>

# Delete custom role
az role definition delete --name <role-name>
```

## Complete Workflows

### Workflow 1: Deploy Web Application

```bash
# 1. Create resource group
az group create --name myapp-rg --location eastus

# 2. Create app service plan
az appservice plan create --name myapp-plan --resource-group myapp-rg --sku B1 --is-linux

# 3. Create web app
az webapp create --resource-group myapp-rg --plan myapp-plan --name myapp-webapp --runtime "NODE:18-lts"

# 4. Configure app settings
az webapp config appsettings set --name myapp-webapp --resource-group myapp-rg --settings NODE_ENV=production

# 5. Deploy application
az webapp deployment source config-zip --resource-group myapp-rg --name myapp-webapp --src app.zip

# 6. Verify deployment
az webapp show --resource-group myapp-rg --name myapp-webapp --query "defaultHostName" -o tsv
```

### Workflow 2: Create AKS Cluster with ACR

```bash
# 1. Create resource group
az group create --name k8s-rg --location eastus

# 2. Create container registry
az acr create --resource-group k8s-rg --name myacr --sku Basic

# 3. Create AKS cluster
az aks create --resource-group k8s-rg --name myk8s --node-count 2 --generate-ssh-keys --attach-acr myacr

# 4. Get cluster credentials
az aks get-credentials --resource-group k8s-rg --name myk8s

# 5. Verify cluster
kubectl get nodes
```

### Workflow 3: Mirror Azure DevOps Repository to GitHub

```bash
# 1. Set DevOps defaults
az devops configure --defaults organization=https://dev.azure.com/myorg project=MyProject

# 2. List repositories
az repos list -o table

# 3. Get repository clone URL
REPO_URL=$(az repos show --repository MyRepo --query "remoteUrl" -o tsv)

# 4. Clone repository (mirror)
git clone --mirror "$REPO_URL"

# 5. Add GitHub remote
cd MyRepo.git
git remote add github git@github.com:myuser/myrepo.git

# 6. Push to GitHub
git push --mirror github
```

### Workflow 4: Setup Virtual Machine with Storage

```bash
# 1. Create resource group
az group create --name vm-rg --location eastus

# 2. Create storage account
az storage account create --name vmstorage --resource-group vm-rg --sku Standard_LRS

# 3. Create virtual network
az network vnet create --resource-group vm-rg --name myVnet --subnet-name mySubnet

# 4. Create public IP
az network public-ip create --resource-group vm-rg --name myPublicIP

# 5. Create NSG with SSH rule
az network nsg create --resource-group vm-rg --name myNSG
az network nsg rule create --resource-group vm-rg --nsg-name myNSG --name AllowSSH --priority 1000 --destination-port-ranges 22 --protocol Tcp --access Allow

# 6. Create VM
az vm create \
  --resource-group vm-rg \
  --name myVM \
  --image Ubuntu2204 \
  --vnet-name myVnet \
  --subnet mySubnet \
  --public-ip-address myPublicIP \
  --nsg myNSG \
  --admin-username azureuser \
  --generate-ssh-keys

# 7. Get public IP address
az vm show --resource-group vm-rg --name myVM --show-details --query "publicIps" -o tsv
```

### Workflow 5: Deploy Function App with Key Vault Integration

```bash
# 1. Create resource group
az group create --name func-rg --location eastus

# 2. Create storage account for function
az storage account create --name funcstorage --resource-group func-rg --sku Standard_LRS

# 3. Create Key Vault
az keyvault create --name myfuncvault --resource-group func-rg --location eastus

# 4. Add secret to Key Vault
az keyvault secret set --vault-name myfuncvault --name DatabasePassword --value "SuperSecret123!"

# 5. Create function app
az functionapp create \
  --resource-group func-rg \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 18 \
  --functions-version 4 \
  --name myfuncapp \
  --storage-account funcstorage

# 6. Enable managed identity for function app
az functionapp identity assign --name myfuncapp --resource-group func-rg

# 7. Get function app identity
FUNC_IDENTITY=$(az functionapp identity show --name myfuncapp --resource-group func-rg --query "principalId" -o tsv)

# 8. Grant function app access to Key Vault
az keyvault set-policy --name myfuncvault --object-id $FUNC_IDENTITY --secret-permissions get list

# 9. Configure function app to reference Key Vault secret
az functionapp config appsettings set \
  --name myfuncapp \
  --resource-group func-rg \
  --settings DatabasePassword="@Microsoft.KeyVault(SecretUri=https://myfuncvault.vault.azure.net/secrets/DatabasePassword/)"
```

## Best Practices

### Output and Querying

1. **Use appropriate output format for context**:
   - `--output table` for human review
   - `--output json` for scripting and automation
   - `--output tsv` for simple parsing

2. **Master JMESPath queries**:
   - Filter results: `--query "[?location=='eastus']"`
   - Select fields: `--query "[].{Name:name, Location:location}"`
   - First element: `--query "[0]"`

3. **Use --query with -o tsv for clean scripting**:
   ```bash
   RESOURCE_ID=$(az resource show --name myapp --resource-group myrg --query "id" -o tsv)
   ```

### Resource Management

1. **Tag resources consistently**:
   ```bash
   az group create --name myrg --location eastus --tags Environment=Production Owner=TeamA CostCenter=12345
   ```

2. **Use resource groups for lifecycle management**:
   - Group related resources together
   - Delete entire environments by deleting resource group

3. **Check resource limits and quotas**:
   ```bash
   az vm list-usage --location eastus -o table
   ```

### Security

1. **Use managed identities when possible** instead of service principals
2. **Store secrets in Key Vault** instead of app settings
3. **Enable soft delete on Key Vaults** for production
4. **Use Azure RBAC** for fine-grained access control
5. **Regularly rotate credentials** for service principals

### Performance

1. **Use --no-wait for long-running operations**:
   ```bash
   az vm create --resource-group myrg --name myvm --image Ubuntu2204 --no-wait
   ```

2. **Batch operations when possible**:
   ```bash
   az vm start --ids $(az vm list -g myrg --query "[].id" -o tsv)
   ```

3. **Use parallel execution for multiple operations**:
   ```bash
   # In shell scripts, use xargs or parallel
   az vm list --query "[].name" -o tsv | xargs -P 5 -I {} az vm start --name {} --resource-group myrg
   ```

### Cost Management

1. **Stop/deallocate VMs when not in use**:
   ```bash
   az vm deallocate --resource-group myrg --name myvm
   ```

2. **Use appropriate SKUs** - don't over-provision
3. **Clean up unused resources** regularly
4. **Set up budgets and alerts**:
   ```bash
   az consumption budget list
   ```

## Common Patterns

### Pattern 1: List Resources with Custom Output

```bash
# List VMs with custom columns
az vm list --query "[].{Name:name, ResourceGroup:resourceGroup, Location:location, PowerState:powerState}" -o table

# List web apps with URLs
az webapp list --query "[].{Name:name, URL:defaultHostName, State:state}" -o table
```

### Pattern 2: Bulk Operations

```bash
# Start all VMs in resource group
az vm start --ids $(az vm list -g myrg --query "[].id" -o tsv)

# Stop all VMs in subscription
az vm deallocate --ids $(az vm list --query "[].id" -o tsv)

# Delete all resource groups with specific tag
az group list --tag Environment=Dev --query "[].name" -o tsv | xargs -I {} az group delete --name {} --yes --no-wait
```

### Pattern 3: Resource Creation with Dependencies

```bash
# Create resources in order, capturing IDs
VNET_ID=$(az network vnet create --name myVnet --resource-group myrg --query "newVNet.id" -o tsv)
SUBNET_ID=$(az network vnet subnet create --name mySubnet --vnet-name myVnet --resource-group myrg --query "id" -o tsv)
VM_ID=$(az vm create --name myVM --resource-group myrg --image Ubuntu2204 --subnet $SUBNET_ID --query "id" -o tsv)
```

### Pattern 4: Configuration Backup

```bash
# Export resource group template
az group export --name myrg > myrg-template.json

# Export individual resource
az resource show --ids <resource-id> > resource-config.json

# Export all resource groups
az group list --query "[].name" -o tsv | while read rg; do
  az group export --name "$rg" > "${rg}-template.json"
done
```

### Pattern 5: Health Checks and Monitoring

```bash
# Check VM power state
az vm get-instance-view --resource-group myrg --name myvm --query "instanceView.statuses[?starts_with(code, 'PowerState/')].displayStatus" -o tsv

# Check web app status
az webapp show --resource-group myrg --name myapp --query "state" -o tsv

# Monitor activity log for errors
az monitor activity-log list --start-time $(date -u -d '1 hour ago' '+%Y-%m-%dT%H:%M:%SZ') --query "[?level=='Error']" -o table
```

## Troubleshooting

### Issue: Authentication Failures

```bash
# Solution 1: Re-login
az logout
az login

# Solution 2: Clear token cache
rm -rf ~/.azure

# Solution 3: Login with specific tenant
az login --tenant <tenant-id>

# Verify authentication
az account show
```

### Issue: Subscription Not Found

```bash
# List all accessible subscriptions
az account list -o table

# Set correct subscription
az account set --subscription <subscription-id>

# Verify current subscription
az account show --query "{Name:name, ID:id}" -o table
```

### Issue: Resource Already Exists

```bash
# Check if resource exists
az resource show --name <resource-name> --resource-group <group> --resource-type <type>

# List resources with same name
az resource list --name <resource-name> -o table

# Use unique names or clean up existing resources
az resource delete --ids <resource-id>
```

### Issue: Insufficient Permissions

```bash
# Check your role assignments
az role assignment list --assignee $(az account show --query "user.name" -o tsv) -o table

# Check required permissions for operation
# Azure documentation provides required permissions for each operation

# Request access from administrator if needed
```

### Issue: Quota or Limit Exceeded

```bash
# Check current usage
az vm list-usage --location eastus -o table

# Request quota increase through Azure Portal or support ticket

# Use different region if available
az account list-locations -o table
```

### Issue: Long-Running Operation Timeout

```bash
# Use --no-wait to avoid timeout
az vm create --resource-group myrg --name myvm --image Ubuntu2204 --no-wait

# Check operation status
az vm show --resource-group myrg --name myvm --query "provisioningState"

# Monitor with polling
while true; do
  STATE=$(az vm show --resource-group myrg --name myvm --query "provisioningState" -o tsv 2>/dev/null)
  echo "Current state: $STATE"
  [[ "$STATE" == "Succeeded" ]] && break
  sleep 10
done
```

## Quick Reference

```bash
# Authentication
az login
az account show
az account set --subscription <id>

# Resource Groups
az group create --name <name> --location <location>
az group list -o table
az group delete --name <name> --yes

# Virtual Machines
az vm list -o table
az vm create --resource-group <rg> --name <name> --image Ubuntu2204
az vm start/stop/restart --resource-group <rg> --name <name>

# Storage
az storage account create --name <name> --resource-group <rg>
az storage blob upload --account-name <account> --container <container> --name <blob> --file <file>

# Web Apps
az webapp create --resource-group <rg> --plan <plan> --name <name> --runtime "NODE:18-lts"
az webapp deployment source config-zip --resource-group <rg> --name <name> --src <zip>

# Azure DevOps
az repos list -o table
az pipelines list -o table
az pipelines run --name <pipeline>

# Networking
az network vnet create --resource-group <rg> --name <vnet>
az network nsg create --resource-group <rg> --name <nsg>

# Container Services
az aks create --resource-group <rg> --name <cluster>
az aks get-credentials --resource-group <rg> --name <cluster>
az acr create --resource-group <rg> --name <registry>

# Key Vault
az keyvault create --name <vault> --resource-group <rg>
az keyvault secret set --vault-name <vault> --name <secret> --value <value>
az keyvault secret show --vault-name <vault> --name <secret> --query "value" -o tsv

# Monitoring
az monitor activity-log list -o table
az monitor metrics list --resource <id> --metric <metric>

# Useful query patterns
--query "[].{Name:name, Location:location}" -o table
--query "[?location=='eastus'].name" -o tsv
--query "[0].id" -o tsv
```

## Integration with Other Tools

### Working with Git

After Azure DevOps repository operations, integrate with git workflow:
```bash
# Clone Azure DevOps repo
REPO_URL=$(az repos show --repository MyRepo --query "remoteUrl" -o tsv)
git clone "$REPO_URL"

# Use git skill for commit and push operations
```

### Working with Kubernetes

After AKS operations, use kubectl:
```bash
# Get credentials
az aks get-credentials --resource-group myrg --name myk8s

# Then use kubectl
kubectl get nodes
kubectl apply -f deployment.yaml
```

### Working with Docker

After ACR operations, use docker:
```bash
# Login to ACR
az acr login --name myacr

# Then use docker
docker build -t myacr.azurecr.io/myapp:v1 .
docker push myacr.azurecr.io/myapp:v1
```

## Summary

**Primary directives:**
1. **Always authenticate** before running commands
2. **Use appropriate output formats** for context (table for humans, json/tsv for scripts)
3. **Master --query for filtering** results
4. **Tag resources consistently** for organization
5. **Use --no-wait for long operations** to avoid timeouts
6. **Store secrets in Key Vault**, not in app settings
7. **Use managed identities** when possible
8. **Clean up resources** to avoid unnecessary costs

**Most common commands:**
- `az login` - Authenticate
- `az account set --subscription <id>` - Set subscription
- `az group create/delete` - Manage resource groups
- `az <service> list -o table` - List resources
- `az <service> show --query "<path>" -o tsv` - Get specific values
- `az devops configure --defaults` - Set DevOps defaults
- `az repos list` - List repositories
- `az pipelines run` - Run pipelines
