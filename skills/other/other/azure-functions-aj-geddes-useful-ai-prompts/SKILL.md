---
name: azure-functions
description: Create serverless functions on Azure with triggers, bindings, authentication, and monitoring. Use for event-driven computing without managing infrastructure.
---

# Azure Functions

## Overview

Azure Functions enables serverless computing on Microsoft Azure. Build event-driven applications with automatic scaling, flexible bindings to various Azure services, and integrated monitoring through Application Insights.

## When to Use

- HTTP APIs and webhooks
- Message-driven processing (Service Bus, Event Hub)
- Scheduled jobs and CRON expressions
- File and blob processing
- Queue-based workflows
- Real-time data processing
- Microservices and backend logic
- Integration with Azure ecosystem services

## Implementation Examples

### 1. **Azure Function Creation with Azure CLI**

```bash
# Install Azure Functions Core Tools
curl https://aka.ms/install-artifacts-ubuntu.sh | bash

# Login to Azure
az login

# Create resource group
az group create --name myapp-rg --location eastus

# Create storage account (required for Functions)
az storage account create \
  --name myappstore \
  --location eastus \
  --resource-group myapp-rg \
  --sku Standard_LRS

# Create Function App
az functionapp create \
  --resource-group myapp-rg \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 18 \
  --functions-version 4 \
  --name myapp-function \
  --storage-account myappstore

# Create function in app
func new --name HttpTrigger --template "HTTP trigger"

# Configure authentication
az functionapp auth update \
  --resource-group myapp-rg \
  --name myapp-function \
  --enabled true \
  --action RedirectToLoginPage \
  --default-provider AzureActiveDirectory

# Deploy function
func azure functionapp publish myapp-function

# Check deployment
az functionapp list --output table

# Get function details
az functionapp function show \
  --resource-group myapp-rg \
  --name myapp-function \
  --function-name HttpTrigger
```

### 2. **Azure Function Implementation (Node.js)**

```javascript
// HttpTrigger/index.js
module.exports = async function (context, req) {
  context.log('HTTP trigger function processed request.');

  // Extract request data
  const name = req.query.name || (req.body && req.body.name);
  const requestId = context.traceContext.traceparent;

  try {
    // Validate input
    if (!name) {
      return {
        status: 400,
        body: { error: 'Name parameter is required' }
      };
    }

    // Business logic
    const response = {
      message: `Hello ${name}!`,
      timestamp: new Date().toISOString(),
      requestId: requestId
    };

    // Log to Application Insights
    context.log({
      level: 'info',
      message: 'Request processed successfully',
      name: name,
      requestId: requestId
    });

    return {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': requestId
      },
      body: response
    };
  } catch (error) {
    context.log.error('Error processing request:', error);

    return {
      status: 500,
      body: { error: 'Internal server error' }
    };
  }
};

// TimerTrigger/index.js
module.exports = async function (context, myTimer) {
  const timeStamp = new Date().toISOString();

  if (myTimer.isPastDue) {
    context.log('Timer function is running late!');
  }

  // Process scheduled job
  context.log(`Timer trigger function ran at ${timeStamp}`);
  context.log('Processing batch job...');

  // Simulate work
  await new Promise(resolve => setTimeout(resolve, 1000));

  context.log('Batch job completed');
};

// ServiceBusQueueTrigger/index.js
module.exports = async function (context, mySbMsg) {
  context.log('ServiceBus queue trigger function processed message:', mySbMsg);

  try {
    const messageBody = typeof mySbMsg === 'string' ? JSON.parse(mySbMsg) : mySbMsg;

    // Process message
    await processMessage(messageBody);

    context.log('Message processed successfully');
  } catch (error) {
    context.log.error('Error processing message:', error);
    throw error; // Re-queue message
  }
};

async function processMessage(messageBody) {
  // Business logic here
  return true;
}
```

### 3. **Azure Functions with Terraform**

```hcl
# functions.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    virtual_machine {
      delete_os_disk_on_delete            = true
      graceful_shutdown                   = false
      skip_shutdown_and_force_delete       = false
    }
  }
}

variable "environment" {
  default = "dev"
}

variable "location" {
  default = "eastus"
}

# Resource group
resource "azurerm_resource_group" "main" {
  name     = "myapp-rg-${var.environment}"
  location = var.location
}

# Storage account for Function App
resource "azurerm_storage_account" "function_storage" {
  name                     = "myappstore${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = var.environment
  }
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "myapp-insights-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"

  retention_in_days = 30
}

# App Service Plan
resource "azurerm_service_plan" "function_plan" {
  name                = "myapp-plan-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption plan

  tags = {
    environment = var.environment
  }
}

# Function App
resource "azurerm_linux_function_app" "main" {
  name                = "myapp-function-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.function_plan.id

  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key

  app_settings = {
    APPINSIGHTS_INSTRUMENTATIONKEY             = azurerm_application_insights.main.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING      = azurerm_application_insights.main.connection_string
    AzureWebJobsStorage                        = azurerm_storage_account.function_storage.primary_blob_connection_string
    WEBSITE_NODE_DEFAULT_VERSION               = "~18"
    FUNCTIONS_EXTENSION_VERSION                = "~4"
    FUNCTIONS_WORKER_RUNTIME                   = "node"
    ENABLE_INIT_LOGGING                        = true
    WEBSITE_RUN_FROM_PACKAGE                   = 1
  }

  site_config {
    application_insights_key             = azurerm_application_insights.main.instrumentation_key
    application_insights_connection_string = azurerm_application_insights.main.connection_string

    cors {
      allowed_origins = ["https://example.com"]
    }

    http2_enabled = true
  }

  https_only = true
  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = var.environment
  }
}

# Key Vault for secrets
resource "azurerm_key_vault" "function_secrets" {
  name                = "myappkv${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_linux_function_app.main.identity[0].principal_id

    secret_permissions = [
      "Get",
      "List"
    ]
  }

  tags = {
    environment = var.environment
  }
}

# Store database password in Key Vault
resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = "MySecurePassword123!"
  key_vault_id = azurerm_key_vault.function_secrets.id
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "function_logs" {
  name               = "function-logs"
  target_resource_id = azurerm_linux_function_app.main.id

  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  enabled_log {
    category = "FunctionAppLogs"
  }

  metric {
    category = "AllMetrics"
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "myapp-logs-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"

  retention_in_days = 30
}

data "azurerm_client_config" "current" {}

output "function_app_url" {
  value = "https://${azurerm_linux_function_app.main.default_hostname}"
}

output "app_insights_key" {
  value     = azurerm_application_insights.main.instrumentation_key
  sensitive = true
}
```

### 4. **Function Bindings Configuration**

```json
{
  "scriptFile": "index.js",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"],
      "route": "api/{*route}"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    },
    {
      "type": "queue",
      "direction": "out",
      "name": "myQueueItem",
      "queueName": "myqueue",
      "connection": "AzureWebJobsStorage"
    },
    {
      "type": "serviceBus",
      "direction": "in",
      "name": "mySbMsg",
      "queueName": "myqueue",
      "connection": "ServiceBusConnection",
      "cardinality": "one"
    },
    {
      "type": "blob",
      "direction": "in",
      "name": "inputBlob",
      "path": "input/{name}",
      "connection": "AzureWebJobsStorage"
    },
    {
      "type": "blob",
      "direction": "out",
      "name": "outputBlob",
      "path": "output/{name}",
      "connection": "AzureWebJobsStorage"
    }
  ]
}
```

## Best Practices

### ✅ DO
- Use managed identity for Azure services
- Store secrets in Key Vault
- Enable Application Insights
- Implement idempotent functions
- Use durable functions for long-running operations
- Handle exceptions and failures
- Monitor function execution
- Use bindings instead of SDK calls

### ❌ DON'T
- Store secrets in code or configuration
- Ignore Application Insights
- Create functions without error handling
- Use blocking operations
- Create long-running functions without Durable Functions
- Ignore monitoring and logging

## Monitoring

- Application Insights for tracing and metrics
- Azure Monitor for overall health
- Log Analytics for log analysis
- Function metrics (execution count, duration)
- Custom telemetry and events

## Resources

- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Azure Functions Best Practices](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices)
- [Azure Key Vault Integration](https://docs.microsoft.com/en-us/azure/azure-functions/security-concepts)
