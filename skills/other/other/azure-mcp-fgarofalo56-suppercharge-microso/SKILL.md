---
name: azure-mcp
description: Comprehensive Azure cloud management skill using Azure CLI. Manage 40+ Azure services including storage, databases, containers, monitoring, security, AI services, messaging, and infrastructure. Triggers on Azure, cloud, blob, cosmos, keyvault, AKS, kubernetes, monitor, SQL, postgres, mysql, event grid, service bus, functions, app service, resource group, subscription.
---

# Azure Cloud Management Skill

Comprehensive skill for managing Azure cloud services using Azure CLI (`az`). This skill provides natural language interaction with 40+ Azure services - no additional setup beyond Azure CLI required.

## Prerequisites

- **Azure CLI installed**: Install via `winget install Microsoft.AzureCLI` or `brew install azure-cli`
- **Authenticated**: Run `az login` before using Azure commands
- **Subscription set**: Use `az account set --subscription <name-or-id>` to set default

## Quick Authentication Check

Before running Azure commands, verify authentication:
```bash
az account show --query "{name:name, id:id, user:user.name}" -o table
```

## Core Patterns

### Output Formats
Always use `-o table` for human-readable output, `-o json` for parsing, `-o tsv` for scripting:
```bash
az <command> -o table    # Human readable
az <command> -o json     # Full details, parseable
az <command> -o tsv      # Tab-separated for scripts
```

### Common Query Patterns
Use `--query` with JMESPath to filter output:
```bash
az vm list --query "[].{Name:name, RG:resourceGroup, State:powerState}" -o table
```

---

## Resource Management

### Subscriptions
```bash
# List all subscriptions
az account list -o table

# Show current subscription
az account show -o table

# Set active subscription
az account set --subscription "<name-or-id>"

# List available locations/regions
az account list-locations -o table --query "[].{Name:name, DisplayName:displayName}"
```

### Resource Groups
```bash
# List all resource groups
az group list -o table

# List resources in a group
az resource list --resource-group <rg-name> -o table

# Create resource group
az group create --name <name> --location <region>

# Delete resource group
az group delete --name <name> --yes --no-wait

# Show resource group details
az group show --name <name>
```

### Generic Resource Operations
```bash
# List all resources in subscription
az resource list -o table

# Get resource by ID
az resource show --ids <resource-id>

# Delete resource by ID
az resource delete --ids <resource-id>

# List resource providers
az provider list -o table

# Show resource tags
az resource show --ids <resource-id> --query "tags"
```

---

## Storage

### Storage Accounts
```bash
# List storage accounts
az storage account list -o table

# List in resource group
az storage account list --resource-group <rg> -o table

# Create storage account
az storage account create \
  --name <account-name> \
  --resource-group <rg> \
  --location <region> \
  --sku Standard_LRS \
  --kind StorageV2

# Show storage account
az storage account show --name <account> --resource-group <rg>

# Get connection string
az storage account show-connection-string --name <account> --resource-group <rg> -o tsv

# Get storage account keys
az storage account keys list --account-name <account> --resource-group <rg> -o table

# Delete storage account
az storage account delete --name <account> --resource-group <rg> --yes
```

### Blob Containers
```bash
# List containers (with account key)
az storage container list --account-name <account> --account-key <key> -o table

# List containers (with connection string)
az storage container list --connection-string "<conn-string>" -o table

# Create container
az storage container create --name <container> --account-name <account> --account-key <key>

# Delete container
az storage container delete --name <container> --account-name <account> --account-key <key>

# Show container properties
az storage container show --name <container> --account-name <account> --account-key <key>

# Set container access level
az storage container set-permission --name <container> --public-access blob --account-name <account>
```

### Blobs
```bash
# List blobs in container
az storage blob list --container-name <container> --account-name <account> --account-key <key> -o table

# Upload blob
az storage blob upload \
  --container-name <container> \
  --name <blob-name> \
  --file <local-path> \
  --account-name <account> \
  --account-key <key>

# Upload directory
az storage blob upload-batch \
  --destination <container> \
  --source <local-dir> \
  --account-name <account> \
  --account-key <key>

# Download blob
az storage blob download \
  --container-name <container> \
  --name <blob-name> \
  --file <local-path> \
  --account-name <account> \
  --account-key <key>

# Delete blob
az storage blob delete --container-name <container> --name <blob-name> --account-name <account>

# Get blob URL
az storage blob url --container-name <container> --name <blob-name> --account-name <account>

# Generate SAS token for blob
az storage blob generate-sas \
  --container-name <container> \
  --name <blob-name> \
  --account-name <account> \
  --permissions r \
  --expiry <datetime> \
  --https-only
```

### File Shares
```bash
# List file shares
az storage share list --account-name <account> --account-key <key> -o table

# Create file share
az storage share create --name <share-name> --account-name <account> --account-key <key>

# List files in share
az storage file list --share-name <share> --account-name <account> -o table

# Upload file
az storage file upload --share-name <share> --source <local-file> --account-name <account>

# Download file
az storage file download --share-name <share> --path <remote-path> --dest <local-path> --account-name <account>
```

### Tables & Queues
```bash
# List tables
az storage table list --account-name <account> --account-key <key> -o table

# Create table
az storage table create --name <table-name> --account-name <account>

# List queues
az storage queue list --account-name <account> --account-key <key> -o table

# Create queue
az storage queue create --name <queue-name> --account-name <account>
```

---

## Databases

### Azure SQL
```bash
# List SQL servers
az sql server list -o table

# List SQL servers in resource group
az sql server list --resource-group <rg> -o table

# Create SQL server
az sql server create \
  --name <server-name> \
  --resource-group <rg> \
  --location <region> \
  --admin-user <username> \
  --admin-password <password>

# Show server details
az sql server show --name <server> --resource-group <rg>

# Delete SQL server
az sql server delete --name <server> --resource-group <rg> --yes

# List databases on server
az sql db list --server <server> --resource-group <rg> -o table

# Create database
az sql db create \
  --server <server> \
  --resource-group <rg> \
  --name <db-name> \
  --service-objective S0

# Show database details
az sql db show --server <server> --resource-group <rg> --name <db-name>

# Delete database
az sql db delete --server <server> --resource-group <rg> --name <db-name> --yes

# List elastic pools
az sql elastic-pool list --server <server> --resource-group <rg> -o table

# Configure firewall rule
az sql server firewall-rule create \
  --server <server> \
  --resource-group <rg> \
  --name <rule-name> \
  --start-ip-address <start-ip> \
  --end-ip-address <end-ip>

# Allow Azure services
az sql server firewall-rule create \
  --server <server> \
  --resource-group <rg> \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# List firewall rules
az sql server firewall-rule list --server <server> --resource-group <rg> -o table

# Delete firewall rule
az sql server firewall-rule delete --server <server> --resource-group <rg> --name <rule-name>

# Get connection string
az sql db show-connection-string --server <server> --name <db-name> --client ado.net
```

### Azure Cosmos DB
```bash
# List Cosmos DB accounts
az cosmosdb list -o table

# List in resource group
az cosmosdb list --resource-group <rg> -o table

# Create Cosmos DB account (SQL API)
az cosmosdb create \
  --name <account-name> \
  --resource-group <rg> \
  --kind GlobalDocumentDB \
  --locations regionName=<region> failoverPriority=0

# Show account details
az cosmosdb show --name <account> --resource-group <rg>

# Get connection strings
az cosmosdb keys list --name <account> --resource-group <rg> --type connection-strings

# Get keys
az cosmosdb keys list --name <account> --resource-group <rg>

# List SQL databases
az cosmosdb sql database list --account-name <account> --resource-group <rg> -o table

# Create SQL database
az cosmosdb sql database create \
  --account-name <account> \
  --resource-group <rg> \
  --name <db-name>

# Delete SQL database
az cosmosdb sql database delete --account-name <account> --resource-group <rg> --name <db-name> --yes

# List containers in database
az cosmosdb sql container list \
  --account-name <account> \
  --resource-group <rg> \
  --database-name <db-name> \
  -o table

# Create container
az cosmosdb sql container create \
  --account-name <account> \
  --resource-group <rg> \
  --database-name <db-name> \
  --name <container-name> \
  --partition-key-path "/partitionKey"

# Show container details
az cosmosdb sql container show \
  --account-name <account> \
  --resource-group <rg> \
  --database-name <db-name> \
  --name <container-name>

# Delete container
az cosmosdb sql container delete \
  --account-name <account> \
  --resource-group <rg> \
  --database-name <db-name> \
  --name <container-name> \
  --yes
```

### Azure Database for PostgreSQL
```bash
# List PostgreSQL servers (flexible)
az postgres flexible-server list -o table

# List in resource group
az postgres flexible-server list --resource-group <rg> -o table

# Create PostgreSQL server
az postgres flexible-server create \
  --name <server-name> \
  --resource-group <rg> \
  --location <region> \
  --admin-user <username> \
  --admin-password <password> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Show server details
az postgres flexible-server show --name <server> --resource-group <rg>

# Delete server
az postgres flexible-server delete --name <server> --resource-group <rg> --yes

# List databases
az postgres flexible-server db list --server-name <server> --resource-group <rg> -o table

# Create database
az postgres flexible-server db create \
  --server-name <server> \
  --resource-group <rg> \
  --database-name <db-name>

# Delete database
az postgres flexible-server db delete \
  --server-name <server> \
  --resource-group <rg> \
  --database-name <db-name> \
  --yes

# Configure firewall rule
az postgres flexible-server firewall-rule create \
  --server-name <server> \
  --resource-group <rg> \
  --name <rule-name> \
  --start-ip-address <ip> \
  --end-ip-address <ip>

# List firewall rules
az postgres flexible-server firewall-rule list --server-name <server> --resource-group <rg> -o table

# Show server configuration
az postgres flexible-server parameter list --server-name <server> --resource-group <rg> -o table

# Update configuration parameter
az postgres flexible-server parameter set \
  --server-name <server> \
  --resource-group <rg> \
  --name <param-name> \
  --value <value>

# Connect and run query (requires psql)
# az postgres flexible-server connect -n <server> -u <user> -p <password> -d <database>
```

### Azure Database for MySQL
```bash
# List MySQL servers (flexible)
az mysql flexible-server list -o table

# List in resource group
az mysql flexible-server list --resource-group <rg> -o table

# Create MySQL server
az mysql flexible-server create \
  --name <server-name> \
  --resource-group <rg> \
  --location <region> \
  --admin-user <username> \
  --admin-password <password> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Show server details
az mysql flexible-server show --name <server> --resource-group <rg>

# Delete server
az mysql flexible-server delete --name <server> --resource-group <rg> --yes

# List databases
az mysql flexible-server db list --server-name <server> --resource-group <rg> -o table

# Create database
az mysql flexible-server db create \
  --server-name <server> \
  --resource-group <rg> \
  --database-name <db-name>

# Configure firewall
az mysql flexible-server firewall-rule create \
  --server-name <server> \
  --resource-group <rg> \
  --name <rule-name> \
  --start-ip-address <ip> \
  --end-ip-address <ip>

# List firewall rules
az mysql flexible-server firewall-rule list --server-name <server> --resource-group <rg> -o table

# Show configuration
az mysql flexible-server parameter list --server-name <server> --resource-group <rg> -o table
```

### Azure Cache for Redis
```bash
# List Redis caches
az redis list -o table

# List in resource group
az redis list --resource-group <rg> -o table

# Create Redis cache
az redis create \
  --name <cache-name> \
  --resource-group <rg> \
  --location <region> \
  --sku Basic \
  --vm-size c0

# Show cache details
az redis show --name <cache> --resource-group <rg>

# Get access keys
az redis list-keys --name <cache> --resource-group <rg>

# Delete cache
az redis delete --name <cache> --resource-group <rg> --yes

# Regenerate key
az redis regenerate-keys --name <cache> --resource-group <rg> --key-type Primary
```

---

## Containers & Compute

### Azure Kubernetes Service (AKS)
```bash
# List AKS clusters
az aks list -o table

# List in resource group
az aks list --resource-group <rg> -o table

# Create AKS cluster
az aks create \
  --name <cluster-name> \
  --resource-group <rg> \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2 \
  --generate-ssh-keys

# Show cluster details
az aks show --name <cluster> --resource-group <rg>

# Get credentials (configure kubectl)
az aks get-credentials --name <cluster> --resource-group <rg>

# Delete cluster
az aks delete --name <cluster> --resource-group <rg> --yes --no-wait

# Scale cluster
az aks scale --name <cluster> --resource-group <rg> --node-count 5

# Upgrade cluster
az aks upgrade --name <cluster> --resource-group <rg> --kubernetes-version <version>

# List available Kubernetes versions
az aks get-versions --location <region> -o table

# Show nodepool details
az aks nodepool list --cluster-name <cluster> --resource-group <rg> -o table

# Add nodepool
az aks nodepool add \
  --cluster-name <cluster> \
  --resource-group <rg> \
  --name <pool-name> \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2

# Scale nodepool
az aks nodepool scale \
  --cluster-name <cluster> \
  --resource-group <rg> \
  --name <pool-name> \
  --node-count 5

# Delete nodepool
az aks nodepool delete --cluster-name <cluster> --resource-group <rg> --name <pool-name>

# Browse dashboard
az aks browse --name <cluster> --resource-group <rg>
```

### Azure Container Registry (ACR)
```bash
# List container registries
az acr list -o table

# List in resource group
az acr list --resource-group <rg> -o table

# Create container registry
az acr create \
  --name <registry-name> \
  --resource-group <rg> \
  --sku Basic \
  --admin-enabled true

# Show registry details
az acr show --name <registry> --resource-group <rg>

# Get login credentials
az acr credential show --name <registry>

# Login to registry
az acr login --name <registry>

# List repositories
az acr repository list --name <registry> -o table

# List tags in repository
az acr repository show-tags --name <registry> --repository <repo-name> -o table

# Delete repository
az acr repository delete --name <registry> --repository <repo-name> --yes

# Delete specific image tag
az acr repository delete --name <registry> --image <repo>:<tag> --yes

# Import image from Docker Hub
az acr import --name <registry> --source docker.io/library/nginx:latest --image nginx:latest

# Build image in ACR
az acr build --registry <registry> --image <image-name>:<tag> .

# Show repository manifests
az acr repository show-manifests --name <registry> --repository <repo-name>
```

### Azure Container Instances (ACI)
```bash
# List container instances
az container list -o table

# List in resource group
az container list --resource-group <rg> -o table

# Create container instance
az container create \
  --name <container-name> \
  --resource-group <rg> \
  --image <image> \
  --cpu 1 \
  --memory 1.5 \
  --ports 80

# Show container details
az container show --name <container> --resource-group <rg>

# Get container logs
az container logs --name <container> --resource-group <rg>

# Stream logs
az container logs --name <container> --resource-group <rg> --follow

# Execute command in container
az container exec --name <container> --resource-group <rg> --exec-command "/bin/bash"

# Delete container
az container delete --name <container> --resource-group <rg> --yes

# Restart container
az container restart --name <container> --resource-group <rg>

# Stop container
az container stop --name <container> --resource-group <rg>

# Start container
az container start --name <container> --resource-group <rg>
```

### Azure Container Apps
```bash
# List Container Apps environments
az containerapp env list -o table

# Create Container Apps environment
az containerapp env create \
  --name <env-name> \
  --resource-group <rg> \
  --location <region>

# List Container Apps
az containerapp list -o table

# Create Container App
az containerapp create \
  --name <app-name> \
  --resource-group <rg> \
  --environment <env-name> \
  --image <image> \
  --target-port 80 \
  --ingress external

# Show Container App
az containerapp show --name <app> --resource-group <rg>

# Update Container App
az containerapp update \
  --name <app> \
  --resource-group <rg> \
  --image <new-image>

# Delete Container App
az containerapp delete --name <app> --resource-group <rg> --yes

# Get logs
az containerapp logs show --name <app> --resource-group <rg>

# Scale Container App
az containerapp update --name <app> --resource-group <rg> --min-replicas 1 --max-replicas 10
```

---

## Web & Functions

### Azure App Service
```bash
# List App Service plans
az appservice plan list -o table

# Create App Service plan
az appservice plan create \
  --name <plan-name> \
  --resource-group <rg> \
  --sku B1 \
  --is-linux

# List web apps
az webapp list -o table

# List web apps in resource group
az webapp list --resource-group <rg> -o table

# Create web app
az webapp create \
  --name <app-name> \
  --resource-group <rg> \
  --plan <plan-name> \
  --runtime "PYTHON:3.9"

# Show web app details
az webapp show --name <app> --resource-group <rg>

# Delete web app
az webapp delete --name <app> --resource-group <rg>

# Get web app URL
az webapp show --name <app> --resource-group <rg> --query "defaultHostName" -o tsv

# Browse web app
az webapp browse --name <app> --resource-group <rg>

# Restart web app
az webapp restart --name <app> --resource-group <rg>

# Stop web app
az webapp stop --name <app> --resource-group <rg>

# Start web app
az webapp start --name <app> --resource-group <rg>

# Deploy from zip
az webapp deployment source config-zip \
  --name <app> \
  --resource-group <rg> \
  --src <file.zip>

# Configure app settings
az webapp config appsettings set \
  --name <app> \
  --resource-group <rg> \
  --settings KEY1=VALUE1 KEY2=VALUE2

# List app settings
az webapp config appsettings list --name <app> --resource-group <rg> -o table

# Delete app setting
az webapp config appsettings delete --name <app> --resource-group <rg> --setting-names KEY1

# Configure connection strings
az webapp config connection-string set \
  --name <app> \
  --resource-group <rg> \
  --connection-string-type SQLAzure \
  --settings MyDb="<connection-string>"

# Get logs
az webapp log tail --name <app> --resource-group <rg>

# Download logs
az webapp log download --name <app> --resource-group <rg>

# List deployment slots
az webapp deployment slot list --name <app> --resource-group <rg> -o table

# Create deployment slot
az webapp deployment slot create --name <app> --resource-group <rg> --slot staging

# Swap slots
az webapp deployment slot swap --name <app> --resource-group <rg> --slot staging

# Enable continuous deployment
az webapp deployment container config \
  --name <app> \
  --resource-group <rg> \
  --enable-cd true
```

### Azure Functions
```bash
# List function apps
az functionapp list -o table

# List in resource group
az functionapp list --resource-group <rg> -o table

# Create function app (consumption plan)
az functionapp create \
  --name <app-name> \
  --resource-group <rg> \
  --storage-account <storage-account> \
  --consumption-plan-location <region> \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4

# Create function app (dedicated plan)
az functionapp create \
  --name <app-name> \
  --resource-group <rg> \
  --storage-account <storage-account> \
  --plan <app-service-plan> \
  --runtime node \
  --runtime-version 18

# Show function app details
az functionapp show --name <app> --resource-group <rg>

# Delete function app
az functionapp delete --name <app> --resource-group <rg>

# Restart function app
az functionapp restart --name <app> --resource-group <rg>

# Stop function app
az functionapp stop --name <app> --resource-group <rg>

# Start function app
az functionapp start --name <app> --resource-group <rg>

# List functions in app
az functionapp function list --name <app> --resource-group <rg> -o table

# Show function details
az functionapp function show --name <app> --resource-group <rg> --function-name <func>

# Get function app settings
az functionapp config appsettings list --name <app> --resource-group <rg> -o table

# Set function app settings
az functionapp config appsettings set \
  --name <app> \
  --resource-group <rg> \
  --settings KEY1=VALUE1

# Deploy function app
az functionapp deployment source config-zip \
  --name <app> \
  --resource-group <rg> \
  --src <function.zip>

# Get deployment credentials
az functionapp deployment list-publishing-credentials --name <app> --resource-group <rg>
```

---

## Security

### Azure Key Vault
```bash
# List key vaults
az keyvault list -o table

# List in resource group
az keyvault list --resource-group <rg> -o table

# Create key vault
az keyvault create \
  --name <vault-name> \
  --resource-group <rg> \
  --location <region>

# Show key vault details
az keyvault show --name <vault>

# Delete key vault
az keyvault delete --name <vault> --resource-group <rg>

# Purge deleted vault (if soft-delete enabled)
az keyvault purge --name <vault>

# List deleted vaults
az keyvault list-deleted -o table

### Secrets ###

# List secrets
az keyvault secret list --vault-name <vault> -o table

# Set secret
az keyvault secret set --vault-name <vault> --name <secret-name> --value "<value>"

# Get secret value
az keyvault secret show --vault-name <vault> --name <secret-name> --query "value" -o tsv

# Delete secret
az keyvault secret delete --vault-name <vault> --name <secret-name>

# List secret versions
az keyvault secret list-versions --vault-name <vault> --name <secret-name> -o table

# Recover deleted secret
az keyvault secret recover --vault-name <vault> --name <secret-name>

### Keys ###

# List keys
az keyvault key list --vault-name <vault> -o table

# Create key
az keyvault key create --vault-name <vault> --name <key-name> --kty RSA --size 2048

# Show key
az keyvault key show --vault-name <vault> --name <key-name>

# Delete key
az keyvault key delete --vault-name <vault> --name <key-name>

# Backup key
az keyvault key backup --vault-name <vault> --name <key-name> --file <backup-file>

### Certificates ###

# List certificates
az keyvault certificate list --vault-name <vault> -o table

# Create self-signed certificate
az keyvault certificate create \
  --vault-name <vault> \
  --name <cert-name> \
  --policy "$(az keyvault certificate get-default-policy)"

# Import certificate
az keyvault certificate import \
  --vault-name <vault> \
  --name <cert-name> \
  --file <cert-file.pfx> \
  --password <pfx-password>

# Download certificate
az keyvault certificate download \
  --vault-name <vault> \
  --name <cert-name> \
  --file <output-file>

# Delete certificate
az keyvault certificate delete --vault-name <vault> --name <cert-name>

### Access Policies ###

# Set access policy for user/service principal
az keyvault set-policy \
  --name <vault> \
  --object-id <object-id> \
  --secret-permissions get list set delete \
  --key-permissions get list create delete \
  --certificate-permissions get list create delete

# Remove access policy
az keyvault delete-policy --name <vault> --object-id <object-id>
```

### Role-Based Access Control (RBAC)
```bash
# List role assignments for resource group
az role assignment list --resource-group <rg> -o table

# List role assignments for subscription
az role assignment list --all -o table

# List role assignments for user
az role assignment list --assignee <user-email> -o table

# List available role definitions
az role definition list -o table --query "[].{Name:roleName, Description:description}"

# Create role assignment
az role assignment create \
  --assignee <user-email-or-object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>

# Delete role assignment
az role assignment delete \
  --assignee <user-email-or-object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>

# Show role definition
az role definition list --name "Contributor"
```

### Microsoft Entra ID (Azure AD)
```bash
# Get current user info
az ad signed-in-user show

# List users
az ad user list -o table --query "[].{Name:displayName, UPN:userPrincipalName, Id:id}"

# Show user details
az ad user show --id <user-id-or-upn>

# List groups
az ad group list -o table --query "[].{Name:displayName, Id:id}"

# List group members
az ad group member list --group <group-name-or-id> -o table

# List service principals
az ad sp list --all -o table --query "[].{Name:displayName, AppId:appId, Id:id}"

# Create service principal
az ad sp create-for-rbac --name <sp-name> --role Contributor --scopes /subscriptions/<sub-id>

# Show service principal
az ad sp show --id <app-id>

# Delete service principal
az ad sp delete --id <app-id>

# Reset service principal credentials
az ad sp credential reset --id <app-id>

# List app registrations
az ad app list -o table --query "[].{Name:displayName, AppId:appId}"
```

---

## Monitoring & Diagnostics

### Azure Monitor
```bash
# List Log Analytics workspaces
az monitor log-analytics workspace list -o table

# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --workspace-name <name> \
  --resource-group <rg> \
  --location <region>

# Show workspace details
az monitor log-analytics workspace show --workspace-name <name> --resource-group <rg>

# Get workspace ID
az monitor log-analytics workspace show --workspace-name <name> --resource-group <rg> --query "customerId" -o tsv

# Get workspace key
az monitor log-analytics workspace get-shared-keys --workspace-name <name> --resource-group <rg>

# Delete workspace
az monitor log-analytics workspace delete --workspace-name <name> --resource-group <rg> --yes

# Query logs (requires workspace ID)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AzureActivity | take 10" \
  -o table

# List tables in workspace
az monitor log-analytics workspace table list \
  --workspace-name <name> \
  --resource-group <rg> \
  -o table
```

### Metrics
```bash
# List metric definitions for a resource
az monitor metrics list-definitions \
  --resource <resource-id> \
  -o table

# Query metrics
az monitor metrics list \
  --resource <resource-id> \
  --metric "Percentage CPU" \
  --interval PT1H \
  --start-time <start-datetime> \
  --end-time <end-datetime>

# Query multiple metrics
az monitor metrics list \
  --resource <resource-id> \
  --metric "Percentage CPU" "Network In" "Network Out" \
  --interval PT5M
```

### Activity Logs
```bash
# List activity logs
az monitor activity-log list -o table

# List activity logs for resource group
az monitor activity-log list --resource-group <rg> -o table

# List activity logs for time range
az monitor activity-log list \
  --start-time <datetime> \
  --end-time <datetime> \
  -o table

# List activity logs for specific resource
az monitor activity-log list \
  --resource-id <resource-id> \
  -o table
```

### Alerts
```bash
# List metric alerts
az monitor metrics alert list -o table

# Create metric alert
az monitor metrics alert create \
  --name <alert-name> \
  --resource-group <rg> \
  --scopes <resource-id> \
  --condition "avg Percentage CPU > 80" \
  --description "CPU usage alert"

# Delete metric alert
az monitor metrics alert delete --name <alert-name> --resource-group <rg>

# List action groups
az monitor action-group list -o table

# Create action group
az monitor action-group create \
  --name <group-name> \
  --resource-group <rg> \
  --short-name <short-name> \
  --action email <email-name> <email@example.com>
```

### Application Insights
```bash
# List Application Insights components
az monitor app-insights component list -o table

# Create Application Insights
az monitor app-insights component create \
  --app <name> \
  --resource-group <rg> \
  --location <region>

# Show Application Insights details
az monitor app-insights component show --app <name> --resource-group <rg>

# Get instrumentation key
az monitor app-insights component show --app <name> --resource-group <rg> --query "instrumentationKey" -o tsv

# Get connection string
az monitor app-insights component show --app <name> --resource-group <rg> --query "connectionString" -o tsv

# Query Application Insights
az monitor app-insights query \
  --app <name> \
  --resource-group <rg> \
  --analytics-query "requests | take 10"

# Delete Application Insights
az monitor app-insights component delete --app <name> --resource-group <rg>
```

### Resource Health
```bash
# Get resource health
az resource show \
  --ids <resource-id> \
  --query "properties.provisioningState"

# List resources with health status (via REST API pattern)
az rest --method get \
  --url "https://management.azure.com/subscriptions/{sub-id}/providers/Microsoft.ResourceHealth/availabilityStatuses?api-version=2020-05-01"
```

---

## Messaging & Integration

### Azure Event Grid
```bash
# List Event Grid topics
az eventgrid topic list -o table

# List in resource group
az eventgrid topic list --resource-group <rg> -o table

# Create Event Grid topic
az eventgrid topic create \
  --name <topic-name> \
  --resource-group <rg> \
  --location <region>

# Show topic details
az eventgrid topic show --name <topic> --resource-group <rg>

# Get topic endpoint
az eventgrid topic show --name <topic> --resource-group <rg> --query "endpoint" -o tsv

# Get topic key
az eventgrid topic key list --name <topic> --resource-group <rg>

# Delete topic
az eventgrid topic delete --name <topic> --resource-group <rg>

# List event subscriptions for topic
az eventgrid event-subscription list --source-resource-id <topic-resource-id> -o table

# Create event subscription
az eventgrid event-subscription create \
  --name <subscription-name> \
  --source-resource-id <topic-resource-id> \
  --endpoint <webhook-url>

# Delete event subscription
az eventgrid event-subscription delete \
  --name <subscription-name> \
  --source-resource-id <topic-resource-id>

# List system topics
az eventgrid system-topic list -o table

# Create system topic for storage
az eventgrid system-topic create \
  --name <topic-name> \
  --resource-group <rg> \
  --source <storage-account-resource-id> \
  --topic-type Microsoft.Storage.StorageAccounts \
  --location <region>
```

### Azure Event Hubs
```bash
# List Event Hubs namespaces
az eventhubs namespace list -o table

# Create Event Hubs namespace
az eventhubs namespace create \
  --name <namespace-name> \
  --resource-group <rg> \
  --location <region> \
  --sku Standard

# Show namespace details
az eventhubs namespace show --name <namespace> --resource-group <rg>

# Get connection string
az eventhubs namespace authorization-rule keys list \
  --namespace-name <namespace> \
  --resource-group <rg> \
  --name RootManageSharedAccessKey

# Delete namespace
az eventhubs namespace delete --name <namespace> --resource-group <rg>

# List event hubs in namespace
az eventhubs eventhub list --namespace-name <namespace> --resource-group <rg> -o table

# Create event hub
az eventhubs eventhub create \
  --name <hub-name> \
  --namespace-name <namespace> \
  --resource-group <rg> \
  --partition-count 4

# Show event hub details
az eventhubs eventhub show --name <hub> --namespace-name <namespace> --resource-group <rg>

# Delete event hub
az eventhubs eventhub delete --name <hub> --namespace-name <namespace> --resource-group <rg>

# List consumer groups
az eventhubs eventhub consumer-group list \
  --eventhub-name <hub> \
  --namespace-name <namespace> \
  --resource-group <rg> \
  -o table

# Create consumer group
az eventhubs eventhub consumer-group create \
  --name <group-name> \
  --eventhub-name <hub> \
  --namespace-name <namespace> \
  --resource-group <rg>
```

### Azure Service Bus
```bash
# List Service Bus namespaces
az servicebus namespace list -o table

# Create Service Bus namespace
az servicebus namespace create \
  --name <namespace-name> \
  --resource-group <rg> \
  --location <region> \
  --sku Standard

# Show namespace details
az servicebus namespace show --name <namespace> --resource-group <rg>

# Get connection string
az servicebus namespace authorization-rule keys list \
  --namespace-name <namespace> \
  --resource-group <rg> \
  --name RootManageSharedAccessKey

# Delete namespace
az servicebus namespace delete --name <namespace> --resource-group <rg>

### Queues ###

# List queues
az servicebus queue list --namespace-name <namespace> --resource-group <rg> -o table

# Create queue
az servicebus queue create \
  --name <queue-name> \
  --namespace-name <namespace> \
  --resource-group <rg>

# Show queue details
az servicebus queue show --name <queue> --namespace-name <namespace> --resource-group <rg>

# Delete queue
az servicebus queue delete --name <queue> --namespace-name <namespace> --resource-group <rg>

### Topics ###

# List topics
az servicebus topic list --namespace-name <namespace> --resource-group <rg> -o table

# Create topic
az servicebus topic create \
  --name <topic-name> \
  --namespace-name <namespace> \
  --resource-group <rg>

# Show topic details
az servicebus topic show --name <topic> --namespace-name <namespace> --resource-group <rg>

# Delete topic
az servicebus topic delete --name <topic> --namespace-name <namespace> --resource-group <rg>

# List subscriptions for topic
az servicebus topic subscription list \
  --topic-name <topic> \
  --namespace-name <namespace> \
  --resource-group <rg> \
  -o table

# Create subscription
az servicebus topic subscription create \
  --name <subscription-name> \
  --topic-name <topic> \
  --namespace-name <namespace> \
  --resource-group <rg>

# Delete subscription
az servicebus topic subscription delete \
  --name <subscription-name> \
  --topic-name <topic> \
  --namespace-name <namespace> \
  --resource-group <rg>
```

---

## AI & Cognitive Services

### Azure Cognitive Services
```bash
# List Cognitive Services accounts
az cognitiveservices account list -o table

# Create Cognitive Services account
az cognitiveservices account create \
  --name <account-name> \
  --resource-group <rg> \
  --kind CognitiveServices \
  --sku S0 \
  --location <region>

# Show account details
az cognitiveservices account show --name <account> --resource-group <rg>

# Get keys
az cognitiveservices account keys list --name <account> --resource-group <rg>

# Get endpoint
az cognitiveservices account show --name <account> --resource-group <rg> --query "properties.endpoint" -o tsv

# Delete account
az cognitiveservices account delete --name <account> --resource-group <rg>

# List available kinds
az cognitiveservices account list-kinds -o table

# List SKUs for a kind
az cognitiveservices account list-skus --kind OpenAI --location <region> -o table
```

### Azure OpenAI
```bash
# Create Azure OpenAI resource
az cognitiveservices account create \
  --name <account-name> \
  --resource-group <rg> \
  --kind OpenAI \
  --sku S0 \
  --location <region>

# List deployments
az cognitiveservices account deployment list \
  --name <account> \
  --resource-group <rg> \
  -o table

# Create deployment
az cognitiveservices account deployment create \
  --name <account> \
  --resource-group <rg> \
  --deployment-name <deployment-name> \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard

# Show deployment
az cognitiveservices account deployment show \
  --name <account> \
  --resource-group <rg> \
  --deployment-name <deployment>

# Delete deployment
az cognitiveservices account deployment delete \
  --name <account> \
  --resource-group <rg> \
  --deployment-name <deployment>

# List available models
az cognitiveservices account list-models --name <account> --resource-group <rg> -o table
```

### Azure AI Search (Cognitive Search)
```bash
# List search services
az search service list -o table

# Create search service
az search service create \
  --name <service-name> \
  --resource-group <rg> \
  --sku basic \
  --location <region>

# Show search service
az search service show --name <service> --resource-group <rg>

# Get admin keys
az search admin-key show --service-name <service> --resource-group <rg>

# Get query keys
az search query-key list --service-name <service> --resource-group <rg> -o table

# Delete search service
az search service delete --name <service> --resource-group <rg> --yes
```

---

## Networking

### Virtual Networks
```bash
# List virtual networks
az network vnet list -o table

# Create virtual network
az network vnet create \
  --name <vnet-name> \
  --resource-group <rg> \
  --location <region> \
  --address-prefixes 10.0.0.0/16

# Show virtual network
az network vnet show --name <vnet> --resource-group <rg>

# Delete virtual network
az network vnet delete --name <vnet> --resource-group <rg>

# List subnets
az network vnet subnet list --vnet-name <vnet> --resource-group <rg> -o table

# Create subnet
az network vnet subnet create \
  --name <subnet-name> \
  --vnet-name <vnet> \
  --resource-group <rg> \
  --address-prefixes 10.0.1.0/24

# Delete subnet
az network vnet subnet delete --name <subnet> --vnet-name <vnet> --resource-group <rg>
```

### Network Security Groups (NSG)
```bash
# List NSGs
az network nsg list -o table

# Create NSG
az network nsg create --name <nsg-name> --resource-group <rg> --location <region>

# Show NSG
az network nsg show --name <nsg> --resource-group <rg>

# List NSG rules
az network nsg rule list --nsg-name <nsg> --resource-group <rg> -o table

# Create NSG rule
az network nsg rule create \
  --nsg-name <nsg> \
  --resource-group <rg> \
  --name Allow-HTTP \
  --priority 100 \
  --access Allow \
  --direction Inbound \
  --protocol Tcp \
  --destination-port-ranges 80

# Delete NSG rule
az network nsg rule delete --nsg-name <nsg> --resource-group <rg> --name <rule-name>

# Delete NSG
az network nsg delete --name <nsg> --resource-group <rg>
```

### Public IP Addresses
```bash
# List public IPs
az network public-ip list -o table

# Create public IP
az network public-ip create \
  --name <ip-name> \
  --resource-group <rg> \
  --sku Standard \
  --allocation-method Static

# Show public IP
az network public-ip show --name <ip> --resource-group <rg>

# Get IP address value
az network public-ip show --name <ip> --resource-group <rg> --query "ipAddress" -o tsv

# Delete public IP
az network public-ip delete --name <ip> --resource-group <rg>
```

### Load Balancers
```bash
# List load balancers
az network lb list -o table

# Create load balancer
az network lb create \
  --name <lb-name> \
  --resource-group <rg> \
  --sku Standard \
  --frontend-ip-name <frontend-name> \
  --backend-pool-name <backend-pool-name> \
  --public-ip-address <public-ip-name>

# Show load balancer
az network lb show --name <lb> --resource-group <rg>

# Delete load balancer
az network lb delete --name <lb> --resource-group <rg>

# List backend pools
az network lb address-pool list --lb-name <lb> --resource-group <rg> -o table
```

### DNS Zones
```bash
# List DNS zones
az network dns zone list -o table

# Create DNS zone
az network dns zone create --name <zone-name> --resource-group <rg>

# Show DNS zone
az network dns zone show --name <zone> --resource-group <rg>

# List DNS records
az network dns record-set list --zone-name <zone> --resource-group <rg> -o table

# Create A record
az network dns record-set a add-record \
  --zone-name <zone> \
  --resource-group <rg> \
  --record-set-name <record-name> \
  --ipv4-address <ip-address>

# Delete DNS zone
az network dns zone delete --name <zone> --resource-group <rg> --yes
```

### Private Endpoints
```bash
# List private endpoints
az network private-endpoint list -o table

# Create private endpoint
az network private-endpoint create \
  --name <endpoint-name> \
  --resource-group <rg> \
  --vnet-name <vnet> \
  --subnet <subnet> \
  --private-connection-resource-id <resource-id> \
  --group-id <group-id> \
  --connection-name <connection-name>

# Show private endpoint
az network private-endpoint show --name <endpoint> --resource-group <rg>

# Delete private endpoint
az network private-endpoint delete --name <endpoint> --resource-group <rg>
```

---

## Virtual Machines

### VM Operations
```bash
# List VMs
az vm list -o table

# List VMs in resource group
az vm list --resource-group <rg> -o table

# List VMs with status
az vm list --resource-group <rg> --show-details -o table

# Create VM
az vm create \
  --name <vm-name> \
  --resource-group <rg> \
  --image Ubuntu2204 \
  --size Standard_DS2_v2 \
  --admin-username azureuser \
  --generate-ssh-keys

# Show VM details
az vm show --name <vm> --resource-group <rg>

# Get VM instance view (power state)
az vm get-instance-view --name <vm> --resource-group <rg> --query "instanceView.statuses[1].displayStatus" -o tsv

# Start VM
az vm start --name <vm> --resource-group <rg>

# Stop VM (deallocate)
az vm deallocate --name <vm> --resource-group <rg>

# Restart VM
az vm restart --name <vm> --resource-group <rg>

# Delete VM
az vm delete --name <vm> --resource-group <rg> --yes

# Resize VM
az vm resize --name <vm> --resource-group <rg> --size Standard_DS3_v2

# List available VM sizes
az vm list-sizes --location <region> -o table

# List available VM images
az vm image list --all --offer Ubuntu -o table

# Run command on VM
az vm run-command invoke \
  --name <vm> \
  --resource-group <rg> \
  --command-id RunShellScript \
  --scripts "hostname && uptime"
```

### VM Scale Sets
```bash
# List VM scale sets
az vmss list -o table

# Create VM scale set
az vmss create \
  --name <vmss-name> \
  --resource-group <rg> \
  --image Ubuntu2204 \
  --instance-count 3 \
  --vm-sku Standard_DS2_v2 \
  --admin-username azureuser \
  --generate-ssh-keys

# Show VM scale set
az vmss show --name <vmss> --resource-group <rg>

# Scale out/in
az vmss scale --name <vmss> --resource-group <rg> --new-capacity 5

# List instances
az vmss list-instances --name <vmss> --resource-group <rg> -o table

# Delete VM scale set
az vmss delete --name <vmss> --resource-group <rg>
```

### Managed Disks
```bash
# List managed disks
az disk list -o table

# Create managed disk
az disk create \
  --name <disk-name> \
  --resource-group <rg> \
  --size-gb 128 \
  --sku Premium_LRS

# Show disk
az disk show --name <disk> --resource-group <rg>

# Delete disk
az disk delete --name <disk> --resource-group <rg> --yes

# Attach disk to VM
az vm disk attach --vm-name <vm> --resource-group <rg> --name <disk-name>

# Detach disk from VM
az vm disk detach --vm-name <vm> --resource-group <rg> --name <disk-name>
```

---

## DevOps & Infrastructure as Code

### ARM/Bicep Deployments
```bash
# Deploy ARM template
az deployment group create \
  --resource-group <rg> \
  --template-file <template.json> \
  --parameters <parameters.json>

# Deploy Bicep template
az deployment group create \
  --resource-group <rg> \
  --template-file <template.bicep> \
  --parameters param1=value1

# Validate template
az deployment group validate \
  --resource-group <rg> \
  --template-file <template.json>

# List deployments
az deployment group list --resource-group <rg> -o table

# Show deployment
az deployment group show --resource-group <rg> --name <deployment-name>

# Delete deployment
az deployment group delete --resource-group <rg> --name <deployment-name>

# What-if deployment
az deployment group what-if \
  --resource-group <rg> \
  --template-file <template.bicep>

# Export resource group as template
az group export --name <rg> > template.json

# Deploy at subscription level
az deployment sub create \
  --location <region> \
  --template-file <template.bicep>
```

### Azure DevOps
```bash
# Configure Azure DevOps CLI
az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>

# List projects
az devops project list -o table

# List repos
az repos list -o table

# List pipelines
az pipelines list -o table

# Run pipeline
az pipelines run --name <pipeline-name>

# List pipeline runs
az pipelines runs list -o table
```

---

## Cost Management

### Cost Analysis
```bash
# Show current usage/spending (requires Cost Management Reader role)
az consumption usage list \
  --start-date <start> \
  --end-date <end> \
  -o table

# List budgets
az consumption budget list -o table

# Create budget
az consumption budget create \
  --budget-name <name> \
  --amount 1000 \
  --category Cost \
  --time-grain Monthly \
  --start-date <start-date> \
  --end-date <end-date>
```

### Reservations
```bash
# List reservations
az reservations reservation list --reservation-order-id <order-id> -o table

# List reservation orders
az reservations reservation-order list -o table
```

---

## Tips & Best Practices

### Performance Tips
```bash
# Use --no-wait for async operations
az vm create --name myvm --resource-group myrg --image Ubuntu2204 --no-wait

# Use --query to reduce output
az vm list --query "[].{name:name, rg:resourceGroup}" -o table

# Use --only-show-errors to reduce noise
az vm list --only-show-errors
```

### Common Patterns
```bash
# Get resource ID
RESOURCE_ID=$(az <resource> show --name <name> --resource-group <rg> --query id -o tsv)

# Loop through resources
for vm in $(az vm list --query "[].name" -o tsv); do
  echo "Processing $vm"
done

# Check if resource exists
if az group show --name <rg> &>/dev/null; then
  echo "Resource group exists"
fi
```

### Useful Aliases
```bash
# Add to shell profile
alias azls='az account list -o table'
alias azrg='az group list -o table'
alias azvm='az vm list --show-details -o table'
```

---

## External Resources

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure CLI Command Reference](https://learn.microsoft.com/en-us/cli/azure/reference-index)
- [JMESPath Query Tutorial](https://jmespath.org/tutorial.html)
- [Azure Quickstart Templates](https://github.com/Azure/azure-quickstart-templates)
