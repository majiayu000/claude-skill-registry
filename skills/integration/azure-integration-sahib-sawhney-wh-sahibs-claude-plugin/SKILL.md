---
name: dapr-azure-integration
description: Configure Azure services as DAPR components with best practices. Supports Azure Cosmos DB, Service Bus, Key Vault, Blob Storage, Event Grid, and Container Apps. Automatically generates component YAML with managed identity support. Use when integrating Azure services or deploying to Azure.
allowed-tools: Read, Write, Grep, Glob, WebFetch
---

# DAPR Azure Integration

This skill helps configure Azure services as DAPR components with production-ready configurations and managed identity support.

## When to Use

Claude automatically uses this skill when:
- User mentions Azure services (Cosmos DB, Service Bus, etc.)
- Deploying DAPR apps to Azure Container Apps or AKS
- Setting up managed identity authentication
- Configuring Azure-specific DAPR components

## Azure Component Configurations

### Azure Cosmos DB (State Store)

**Best for:** Global distribution, strong consistency, document storage

```yaml
# components/statestore-cosmosdb.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.azure.cosmosdb
  version: v1
  metadata:
  # Connection
  - name: url
    value: https://{account}.documents.azure.com:443/
  - name: database
    value: daprdb
  - name: collection
    value: state

  # Authentication (Managed Identity - Recommended)
  - name: azureClientId
    value: "{managed-identity-client-id}"

  # OR Connection String (Development only)
  # - name: masterKey
  #   secretKeyRef:
  #     name: cosmos-secrets
  #     key: masterKey

  # Performance settings
  - name: actorStateStore
    value: "true"
  - name: partitionKey
    value: "/partitionKey"

  # Consistency
  - name: consistencyLevel
    value: "Strong"  # or Session, Eventual
```

**Prerequisites:**
```bash
# Create Cosmos DB account
az cosmosdb create \
  --name mycosmosaccount \
  --resource-group myapp-rg \
  --kind GlobalDocumentDB

# Create database and container
az cosmosdb sql database create \
  --account-name mycosmosaccount \
  --resource-group myapp-rg \
  --name daprdb

az cosmosdb sql container create \
  --account-name mycosmosaccount \
  --resource-group myapp-rg \
  --database-name daprdb \
  --name state \
  --partition-key-path /partitionKey
```

### Azure Service Bus (Pub/Sub)

**Best for:** Enterprise messaging, ordered delivery, dead-letter support

```yaml
# components/pubsub-servicebus.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.azure.servicebus.topics
  version: v1
  metadata:
  # Authentication (Managed Identity - Recommended)
  - name: namespaceName
    value: "{namespace}.servicebus.windows.net"
  - name: azureClientId
    value: "{managed-identity-client-id}"

  # OR Connection String
  # - name: connectionString
  #   secretKeyRef:
  #     name: servicebus-secrets
  #     key: connectionString

  # Consumer settings
  - name: consumerID
    value: "{app-id}"
  - name: maxActiveMessages
    value: "100"
  - name: maxConcurrentHandlers
    value: "10"
  - name: lockRenewalInSec
    value: "60"

  # Retry settings
  - name: maxRetriableErrorsPerSec
    value: "10"
  - name: maxDeliveryCount
    value: "10"
```

**Prerequisites:**
```bash
# Create Service Bus namespace
az servicebus namespace create \
  --name myservicebus \
  --resource-group myapp-rg \
  --sku Standard

# Create topic
az servicebus topic create \
  --namespace-name myservicebus \
  --resource-group myapp-rg \
  --name orders
```

### Azure Key Vault (Secret Store)

**Best for:** Centralized secret management, rotation, HSM support

```yaml
# components/secretstore-keyvault.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
spec:
  type: secretstores.azure.keyvault
  version: v1
  metadata:
  - name: vaultName
    value: "{vault-name}"

  # Authentication (Managed Identity - Recommended)
  - name: azureClientId
    value: "{managed-identity-client-id}"

  # OR Service Principal
  # - name: azureTenantId
  #   value: "{tenant-id}"
  # - name: azureClientId
  #   value: "{client-id}"
  # - name: azureClientSecret
  #   secretKeyRef:
  #     name: azure-sp
  #     key: client-secret
```

**Prerequisites:**
```bash
# Create Key Vault
az keyvault create \
  --name myvault \
  --resource-group myapp-rg \
  --location eastus

# Grant managed identity access
az keyvault set-policy \
  --name myvault \
  --object-id {managed-identity-object-id} \
  --secret-permissions get list
```

### Azure Blob Storage (Binding)

**Best for:** File storage, large objects, cold storage

```yaml
# components/binding-blobstorage.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: blobstore
spec:
  type: bindings.azure.blobstorage
  version: v1
  metadata:
  - name: accountName
    value: "{storage-account}"
  - name: containerName
    value: "{container-name}"

  # Authentication (Managed Identity - Recommended)
  - name: azureClientId
    value: "{managed-identity-client-id}"

  # OR Access Key
  # - name: accountKey
  #   secretKeyRef:
  #     name: storage-secrets
  #     key: accountKey

  # Settings
  - name: decodeBase64
    value: "false"
  - name: getBlobRetryCount
    value: "3"
```

### Azure Event Grid (Binding)

**Best for:** Event routing, serverless triggers, multi-subscriber

```yaml
# components/binding-eventgrid.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: eventgrid
spec:
  type: bindings.azure.eventgrid
  version: v1
  metadata:
  - name: tenantId
    value: "{tenant-id}"
  - name: subscriptionId
    value: "{subscription-id}"
  - name: resourceGroupName
    value: "{resource-group}"
  - name: subscriberEndpoint
    value: "https://{app-url}/eventgrid"
  - name: handshakePort
    value: "8080"
  - name: scope
    value: "/subscriptions/{sub}/resourceGroups/{rg}"

  # Authentication
  - name: azureClientId
    value: "{managed-identity-client-id}"
```

## Managed Identity Setup

### For Azure Container Apps

```bash
# 1. Create user-assigned managed identity
az identity create \
  --name dapr-identity \
  --resource-group myapp-rg

# 2. Get identity details
IDENTITY_ID=$(az identity show -n dapr-identity -g myapp-rg --query id -o tsv)
CLIENT_ID=$(az identity show -n dapr-identity -g myapp-rg --query clientId -o tsv)

# 3. Assign to Container App
az containerapp identity assign \
  --name myapp \
  --resource-group myapp-rg \
  --user-assigned $IDENTITY_ID

# 4. Grant permissions to Azure resources
# Cosmos DB
az cosmosdb sql role assignment create \
  --account-name mycosmosaccount \
  --resource-group myapp-rg \
  --principal-id $(az identity show -n dapr-identity -g myapp-rg --query principalId -o tsv) \
  --role-definition-id "00000000-0000-0000-0000-000000000002"

# Service Bus
az role assignment create \
  --assignee $CLIENT_ID \
  --role "Azure Service Bus Data Sender" \
  --scope /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ServiceBus/namespaces/{ns}

az role assignment create \
  --assignee $CLIENT_ID \
  --role "Azure Service Bus Data Receiver" \
  --scope /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ServiceBus/namespaces/{ns}

# Key Vault
az keyvault set-policy \
  --name myvault \
  --object-id $(az identity show -n dapr-identity -g myapp-rg --query principalId -o tsv) \
  --secret-permissions get list

# Storage
az role assignment create \
  --assignee $CLIENT_ID \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{sa}
```

### For AKS with Workload Identity

```bash
# 1. Enable OIDC and Workload Identity on AKS
az aks update \
  --resource-group myapp-rg \
  --name myaks \
  --enable-oidc-issuer \
  --enable-workload-identity

# 2. Get OIDC issuer
AKS_OIDC_ISSUER=$(az aks show -n myaks -g myapp-rg --query oidcIssuerProfile.issuerUrl -o tsv)

# 3. Create federated credential
az identity federated-credential create \
  --name myapp-federated \
  --identity-name dapr-identity \
  --resource-group myapp-rg \
  --issuer $AKS_OIDC_ISSUER \
  --subject system:serviceaccount:default:myapp-sa
```

## Container Apps DAPR Configuration

```bash
# Deploy with DAPR enabled
az containerapp create \
  --name order-service \
  --resource-group myapp-rg \
  --environment myenv \
  --image myregistry.azurecr.io/order-service:latest \
  --target-port 8000 \
  --ingress external \
  --dapr-enabled \
  --dapr-app-id order-service \
  --dapr-app-port 8000 \
  --user-assigned $IDENTITY_ID \
  --env-vars "AZURE_CLIENT_ID=$CLIENT_ID"

# Add DAPR component
az containerapp env dapr-component set \
  --name myenv \
  --resource-group myapp-rg \
  --dapr-component-name statestore \
  --yaml ./components/statestore-cosmosdb.yaml
```

## Best Practices

1. **Always use Managed Identity** in production - never connection strings
2. **Scope components** to specific apps when they contain sensitive data
3. **Use private endpoints** for Azure services in production
4. **Enable diagnostic logging** on all Azure resources
5. **Set appropriate consistency levels** based on requirements
6. **Configure auto-scaling** based on KEDA scalers
7. **Enable zone redundancy** for high availability

## Troubleshooting

### Common Issues

**"Unauthorized" errors:**
- Check managed identity has correct RBAC roles
- Verify identity is assigned to the container app
- Ensure AZURE_CLIENT_ID env var is set

**"Resource not found":**
- Verify Azure resource exists
- Check resource names in component YAML
- Ensure correct subscription/resource group

**Connection timeouts:**
- Check VNet/firewall rules
- Verify private endpoint configuration
- Check DNS resolution
