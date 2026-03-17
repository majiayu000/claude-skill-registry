---
name: azure-expert
version: 1.0.0
description: Expert-level Microsoft Azure cloud platform, services, and architecture
category: cloud
tags: [azure, cloud, microsoft, azure-functions, cosmos-db]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(az:*)
---

# Microsoft Azure Expert

Expert guidance for Microsoft Azure cloud platform, services, and cloud-native architecture.

## Core Concepts

- Azure Resource Manager (ARM)
- Virtual Machines and App Services
- Azure Functions (serverless)
- Azure Storage (Blob, Queue, Table)
- Azure SQL Database
- Cosmos DB
- Azure Kubernetes Service (AKS)
- Azure Active Directory

## Azure CLI

```bash
# Login
az login

# Create resource group
az group create --name myResourceGroup --location eastus

# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys

# Create App Service
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name myWebApp \
  --runtime "NODE|14-lts"

# Create storage account
az storage account create \
  --name mystorageaccount \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard_LRS
```

## Azure Functions

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="HttpTrigger")
@app.route(route="hello")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name",
            status_code=400
        )

@app.function_name(name="QueueTrigger")
@app.queue_trigger(arg_name="msg", queue_name="myqueue",
                   connection="AzureWebJobsStorage")
def queue_trigger(msg: func.QueueMessage):
    logging.info(f'Python queue trigger function processed: {msg.get_body().decode("utf-8")}')
```

## Cosmos DB

```python
from azure.cosmos import CosmosClient, PartitionKey

endpoint = "https://myaccount.documents.azure.com:443/"
key = "YOUR_KEY"

client = CosmosClient(endpoint, key)
database = client.create_database_if_not_exists(id="myDatabase")
container = database.create_container_if_not_exists(
    id="myContainer",
    partition_key=PartitionKey(path="/userId")
)

# Create item
item = {
    "id": "1",
    "userId": "user123",
    "name": "John Doe"
}
container.create_item(body=item)

# Query items
query = "SELECT * FROM c WHERE c.userId = @userId"
items = container.query_items(
    query=query,
    parameters=[{"name": "@userId", "value": "user123"}],
    enable_cross_partition_query=True
)

for item in items:
    print(item)
```

## ARM Templates

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-02-01",
      "name": "[parameters('webAppName')]",
      "location": "[parameters('location')]",
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', parameters('appServicePlanName'))]"
      }
    }
  ]
}
```

## Best Practices

- Use managed identities
- Implement Azure Key Vault
- Tag resources properly
- Use ARM templates or Bicep
- Monitor with Azure Monitor
- Implement auto-scaling
- Use availability zones

## Anti-Patterns

❌ Hardcoded credentials
❌ No resource tagging
❌ Single region deployment
❌ No backup strategy
❌ Ignoring cost optimization
❌ Not using managed services

## Resources

- Azure Documentation: https://docs.microsoft.com/azure/
- Azure CLI: https://docs.microsoft.com/cli/azure/
