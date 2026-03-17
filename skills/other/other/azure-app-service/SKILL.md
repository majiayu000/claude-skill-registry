---
name: azure-app-service
description: Deploy and manage web apps using Azure App Service with auto-scaling, deployment slots, SSL/TLS, and monitoring. Use for hosting web applications on Azure.
---

# Azure App Service

## Overview

Azure App Service provides a fully managed platform for building and hosting web applications, REST APIs, and mobile backends. Support multiple programming languages with integrated DevOps, security, and high availability.

## When to Use

- Web applications (ASP.NET, Node.js, Python, Java)
- REST APIs and microservices
- Mobile app backends
- Static website hosting
- Production applications requiring scale
- Applications needing auto-scaling
- Multi-region deployments
- Containerized applications

## Implementation Examples

### 1. **App Service Creation with Azure CLI**

```bash
# Login to Azure
az login

# Create resource group
az group create --name myapp-rg --location eastus

# Create App Service Plan
az appservice plan create \
  --name myapp-plan \
  --resource-group myapp-rg \
  --sku P1V2 \
  --is-linux

# Create web app
az webapp create \
  --resource-group myapp-rg \
  --plan myapp-plan \
  --name myapp-web \
  --deployment-container-image-name nodejs:18

# Configure app settings
az webapp config appsettings set \
  --resource-group myapp-rg \
  --name myapp-web \
  --settings \
    NODE_ENV=production \
    PORT=8080 \
    DATABASE_URL=postgresql://... \
    REDIS_URL=redis://...

# Enable HTTPS only
az webapp update \
  --resource-group myapp-rg \
  --name myapp-web \
  --https-only true

# Configure custom domain
az webapp config hostname add \
  --resource-group myapp-rg \
  --webapp-name myapp-web \
  --hostname www.example.com

# Create deployment slot
az webapp deployment slot create \
  --resource-group myapp-rg \
  --name myapp-web \
  --slot staging

# Swap slots
az webapp deployment slot swap \
  --resource-group myapp-rg \
  --name myapp-web \
  --slot staging

# Get publish profile for deployment
az webapp deployment list-publish-profiles \
  --resource-group myapp-rg \
  --name myapp-web \
  --query "[0].publishUrl"
```

### 2. **Terraform App Service Configuration**

```hcl
# app-service.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "environment" {
  default = "prod"
}

variable "location" {
  default = "eastus"
}

# Resource group
resource "azurerm_resource_group" "main" {
  name     = "myapp-rg-${var.environment}"
  location = var.location
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "myapp-plan-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "P1V2"

  tags = {
    environment = var.environment
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

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "myapp-insights-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"

  retention_in_days      = 30
  workspace_id           = azurerm_log_analytics_workspace.main.id
}

# Web App
resource "azurerm_linux_web_app" "main" {
  name                = "myapp-web-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  https_only = true

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
    DOCKER_ENABLE_CI                    = true
    APPINSIGHTS_INSTRUMENTATIONKEY      = azurerm_application_insights.main.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.main.connection_string
    NODE_ENV                            = "production"
    PORT                                = "8080"
  }

  site_config {
    always_on                   = true
    http2_enabled               = true
    minimum_tls_version         = "1.2"
    websockets_enabled          = false
    application_stack {
      node_version = "18-lts"
    }

    cors {
      allowed_origins = ["https://example.com"]
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = var.environment
  }
}

# Deployment slot (staging)
resource "azurerm_linux_web_app_slot" "staging" {
  name            = "staging"
  app_service_id  = azurerm_linux_web_app.main.id
  service_plan_id = azurerm_service_plan.main.id

  https_only = true

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
    NODE_ENV                            = "staging"
    PORT                                = "8080"
  }

  site_config {
    always_on           = true
    http2_enabled       = true
    minimum_tls_version = "1.2"

    application_stack {
      node_version = "18-lts"
    }
  }

  identity {
    type = "SystemAssigned"
  }
}

# Autoscale settings
resource "azurerm_monitor_autoscale_setting" "app_service" {
  name                = "app-service-autoscale"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  target_resource_id  = azurerm_service_plan.main.id

  profile {
    name = "default"

    capacity {
      default = 2
      minimum = 1
      maximum = 5
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        operator           = "GreaterThan"
        threshold          = 75
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        operator           = "LessThan"
        threshold          = 25
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT5M"
      }
    }
  }
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "app_service" {
  name               = "app-service-logs"
  target_resource_id = azurerm_linux_web_app.main.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  enabled_log {
    category = "AppServiceHTTPLogs"
  }

  enabled_log {
    category = "AppServiceAntivirusScanAuditLogs"
  }

  metric {
    category = "AllMetrics"
  }
}

# Key Vault for secrets
resource "azurerm_key_vault" "main" {
  name                = "myappkv${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_linux_web_app.main.identity[0].principal_id

    secret_permissions = [
      "Get",
      "List"
    ]
  }

  tags = {
    environment = var.environment
  }
}

# Key Vault secrets
resource "azurerm_key_vault_secret" "database_url" {
  name         = "database-url"
  value        = "postgresql://user:pass@host/db"
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "api_key" {
  name         = "api-key"
  value        = "your-api-key-here"
  key_vault_id = azurerm_key_vault.main.id
}

data "azurerm_client_config" "current" {}

output "app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "app_insights_key" {
  value     = azurerm_application_insights.main.instrumentation_key
  sensitive = true
}
```

### 3. **Deployment Configuration**

```yaml
# .github/workflows/deploy.yml
name: Deploy to App Service

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: myapp-web-prod
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
          package: .

      - name: Swap slots
        uses: azure/CLI@v1
        with:
          azcliversion: 2.0.76
          inlineScript: |
            az webapp deployment slot swap \
              --resource-group myapp-rg-prod \
              --name myapp-web-prod \
              --slot staging
```

### 4. **Health Check Configuration**

```bash
# Enable health check
az webapp config set \
  --resource-group myapp-rg \
  --name myapp-web \
  --generic-configurations HEALTHCHECK_PATH=/health

# Monitor health
az monitor metrics list-definitions \
  --resource /subscriptions/{subscription}/resourceGroups/myapp-rg/providers/Microsoft.Web/sites/myapp-web
```

## Best Practices

### ✅ DO
- Use deployment slots for zero-downtime deployments
- Enable Application Insights
- Configure autoscaling based on metrics
- Use managed identity for Azure services
- Enable HTTPS only
- Store secrets in Key Vault
- Monitor performance metrics
- Implement health checks

### ❌ DON'T
- Store secrets in configuration
- Disable HTTPS
- Ignore Application Insights
- Use single instance for production
- Deploy directly to production
- Ignore autoscaling configuration

## Monitoring

- Application Insights for application metrics
- Azure Monitor for resource health
- Log Analytics for log analysis
- Custom metrics and events
- Performance counters and diagnostics

## Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [App Service Best Practices](https://docs.microsoft.com/en-us/azure/app-service/app-service-best-practices)
- [Application Insights Integration](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
