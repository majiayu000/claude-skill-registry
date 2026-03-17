---
name: azure-architecture
description: "Microsoft Azure architecture patterns and best practices. Use when designing, deploying, or reviewing Azure infrastructure including AKS, App Service, Functions, CosmosDB, and Entra ID."
---

# Microsoft Azure Architecture

Comprehensive guide for building secure, scalable infrastructure on Microsoft Azure.

## When to Use

- Designing Azure architecture for new projects
- Deploying applications to Azure services
- Setting up networking (VNet, NSGs)
- Configuring Azure AD/Entra ID and RBAC
- Working with AKS (Azure Kubernetes Service)
- Integrating with Microsoft 365 ecosystem

## Core Services Overview

### Compute

| Service | Use Case | Key Features |
|---------|----------|--------------|
| Virtual Machines | Full control | Any OS, any workload |
| AKS | Managed Kubernetes | Azure-integrated K8s |
| App Service | PaaS web apps | Managed platform |
| Functions | Serverless | Event-driven, consumption |
| Container Apps | Serverless containers | Dapr, KEDA built-in |
| Container Instances | Simple containers | Quick deployment |

### Storage

| Service | Use Case | Key Features |
|---------|----------|--------------|
| Blob Storage | Object storage | Hot/Cool/Archive tiers |
| Azure Files | SMB/NFS shares | Cloud file storage |
| Managed Disks | Block storage (VMs) | SSD/HDD options |
| Queue Storage | Message queuing | Simple queues |
| Table Storage | NoSQL key-value | Structured data |

### Database

| Service | Use Case | Key Features |
|---------|----------|--------------|
| Azure SQL | Managed SQL Server | Hyperscale, serverless |
| PostgreSQL Flexible | Managed PostgreSQL | Zone redundant |
| CosmosDB | Multi-model NoSQL | Global distribution |
| Cache for Redis | In-memory cache | Managed Redis |

### Networking

| Service | Use Case | Key Features |
|---------|----------|--------------|
| VNet | Virtual network | Private networking |
| Application Gateway | Layer 7 LB | WAF, SSL termination |
| Load Balancer | Layer 4 LB | Regional/Global |
| Front Door | Global CDN + LB | WAF, routing |
| Private Endpoint | Private connectivity | PaaS over VNet |

## VNet Architecture

### Hub-Spoke Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                          Hub VNet                               │
│                        10.0.0.0/16                              │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │ Gateway Subnet  │  │ Firewall Subnet │  │ Bastion Subnet │  │
│  │ 10.0.0.0/24     │  │ 10.0.1.0/24     │  │ 10.0.2.0/24    │  │
│  │                 │  │                 │  │                │  │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌────────────┐ │  │
│  │ │ VPN Gateway │ │  │ │ Azure       │ │  │ │ Bastion    │ │  │
│  │ └─────────────┘ │  │ │ Firewall    │ │  │ └────────────┘ │  │
│  └─────────────────┘  │ └─────────────┘ │  └────────────────┘  │
│                       └─────────────────┘                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Peering
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Spoke: Prod   │    │ Spoke: Dev    │    │ Spoke: Shared │
│ 10.1.0.0/16   │    │ 10.2.0.0/16   │    │ 10.3.0.0/16   │
│               │    │               │    │               │
│ App + Data    │    │ App + Data    │    │ DNS, AD DS    │
│ Subnets       │    │ Subnets       │    │ Monitoring    │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Terraform VNet

```hcl
# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = var.location
  tags     = local.common_tags
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${var.project}-${var.environment}-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

# Subnets
resource "azurerm_subnet" "app" {
  name                 = "app-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "app-service-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "data" {
  name                 = "data-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]

  service_endpoints = [
    "Microsoft.Sql",
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.10.0/22"]
}

# Network Security Group
resource "azurerm_network_security_group" "app" {
  name                = "${var.project}-app-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = local.common_tags
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}
```

## Azure AD / Entra ID

### Managed Identity

```hcl
# User Assigned Managed Identity
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.project}-app-identity"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

# Role Assignment - Storage
resource "azurerm_role_assignment" "storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

# Role Assignment - Key Vault
resource "azurerm_role_assignment" "keyvault" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

# Role Assignment - SQL
resource "azurerm_role_assignment" "sql" {
  scope                = azurerm_mssql_server.main.id
  role_definition_name = "SQL DB Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

### Service Principal (CI/CD)

```hcl
# For CI/CD pipelines
resource "azuread_application" "cicd" {
  display_name = "${var.project}-cicd"
}

resource "azuread_service_principal" "cicd" {
  client_id = azuread_application.cicd.client_id
}

resource "azuread_service_principal_password" "cicd" {
  service_principal_id = azuread_service_principal.cicd.id
  end_date_relative    = "8760h"  # 1 year
}

# Grant Contributor to Resource Group
resource "azurerm_role_assignment" "cicd" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.cicd.object_id
}
```

## AKS (Azure Kubernetes Service)

### Production AKS Cluster

```hcl
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.project
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "system"
    node_count          = 3
    vm_size             = "Standard_D4s_v3"
    vnet_subnet_id      = azurerm_subnet.aks.id
    zones               = ["1", "2", "3"]
    enable_auto_scaling = true
    min_count           = 3
    max_count           = 10

    node_labels = {
      "nodepool" = "system"
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks.id]
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    load_balancer_sku = "standard"
    outbound_type     = "loadBalancer"
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  azure_active_directory_role_based_access_control {
    managed                = true
    azure_rbac_enabled     = true
    admin_group_object_ids = [var.aks_admin_group_id]
  }

  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  microsoft_defender {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  tags = local.common_tags
}

# User Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "user" {
  name                  = "user"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D8s_v3"
  zones                 = ["1", "2", "3"]
  enable_auto_scaling   = true
  min_count             = 2
  max_count             = 20
  vnet_subnet_id        = azurerm_subnet.aks.id

  node_labels = {
    "nodepool" = "user"
  }

  node_taints = []

  tags = local.common_tags
}
```

## App Service

### Web App with Slots

```hcl
resource "azurerm_service_plan" "main" {
  name                = "${var.project}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.environment == "prod" ? "P2v3" : "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.project}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  site_config {
    always_on                = var.environment == "prod"
    http2_enabled            = true
    minimum_tls_version      = "1.2"
    ftps_state               = "Disabled"
    vnet_route_all_enabled   = true

    application_stack {
      node_version = "20-lts"
    }

    health_check_path = "/health"
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    NODE_ENV                            = "production"
    KEY_VAULT_URI                       = azurerm_key_vault.main.vault_uri
  }

  connection_string {
    name  = "Database"
    type  = "SQLAzure"
    value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_connection.id})"
  }

  virtual_network_subnet_id = azurerm_subnet.app.id

  logs {
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  tags = local.common_tags
}

# Deployment Slot
resource "azurerm_linux_web_app_slot" "staging" {
  name           = "staging"
  app_service_id = azurerm_linux_web_app.main.id

  site_config {
    always_on           = false
    http2_enabled       = true
    minimum_tls_version = "1.2"

    application_stack {
      node_version = "20-lts"
    }
  }

  app_settings = azurerm_linux_web_app.main.app_settings

  tags = local.common_tags
}
```

## Azure SQL

### SQL Database

```hcl
resource "azurerm_mssql_server" "main" {
  name                         = "${var.project}-sql"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = random_password.sql.result
  minimum_tls_version          = "1.2"
  public_network_access_enabled = false

  azuread_administrator {
    login_username              = "AzureAD Admin"
    object_id                   = var.sql_aad_admin_object_id
    azuread_authentication_only = var.environment == "prod"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = local.common_tags
}

resource "azurerm_mssql_database" "main" {
  name                 = var.database_name
  server_id            = azurerm_mssql_server.main.id
  collation            = "SQL_Latin1_General_CP1_CI_AS"
  max_size_gb          = 100
  sku_name             = var.environment == "prod" ? "GP_S_Gen5_4" : "Basic"
  zone_redundant       = var.environment == "prod"
  storage_account_type = "Zone"

  short_term_retention_policy {
    retention_days           = 7
    backup_interval_in_hours = 12
  }

  long_term_retention_policy {
    weekly_retention  = var.environment == "prod" ? "P4W" : null
    monthly_retention = var.environment == "prod" ? "P12M" : null
  }

  threat_detection_policy {
    state                      = "Enabled"
    email_account_admins       = "Enabled"
    retention_days             = 30
  }

  tags = local.common_tags
}

# Private Endpoint
resource "azurerm_private_endpoint" "sql" {
  name                = "${var.project}-sql-pe"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.data.id

  private_service_connection {
    name                           = "${var.project}-sql-psc"
    private_connection_resource_id = azurerm_mssql_server.main.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }

  private_dns_zone_group {
    name                 = "sql-dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.sql.id]
  }
}
```

## Key Vault

### Secure Secrets Management

```hcl
resource "azurerm_key_vault" "main" {
  name                        = "${var.project}-kv"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 90
  purge_protection_enabled    = var.environment == "prod"
  enable_rbac_authorization   = true
  public_network_access_enabled = false

  network_acls {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    virtual_network_subnet_ids = [azurerm_subnet.app.id]
  }

  tags = local.common_tags
}

resource "azurerm_key_vault_secret" "db_connection" {
  name         = "db-connection-string"
  value        = "Server=tcp:${azurerm_mssql_server.main.fully_qualified_domain_name};Database=${var.database_name};..."
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_role_assignment.kv_admin]
}
```

## Storage Account

### Secure Blob Storage

```hcl
resource "azurerm_storage_account" "main" {
  name                            = "${replace(var.project, "-", "")}storage"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = var.environment == "prod" ? "GRS" : "LRS"
  account_kind                    = "StorageV2"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = false

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 30
    }

    container_delete_retention_policy {
      days = 30
    }
  }

  network_rules {
    default_action             = "Deny"
    bypass                     = ["AzureServices"]
    virtual_network_subnet_ids = [azurerm_subnet.app.id]
  }

  identity {
    type = "SystemAssigned"
  }

  tags = local.common_tags
}

resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Lifecycle Management
resource "azurerm_storage_management_policy" "main" {
  storage_account_id = azurerm_storage_account.main.id

  rule {
    name    = "archive-old-blobs"
    enabled = true

    filters {
      blob_types   = ["blockBlob"]
      prefix_match = ["data/"]
    }

    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than    = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
        delete_after_days_since_modification_greater_than          = 365
      }
    }
  }
}
```

## CLI Reference

```bash
# Auth
az login
az account set --subscription "SUBSCRIPTION_NAME"
az account show

# Resource Groups
az group list
az group create --name mygroup --location eastus

# AKS
az aks get-credentials --resource-group mygroup --name mycluster
az aks list
az aks scale --resource-group mygroup --name mycluster --node-count 5

# App Service
az webapp list
az webapp deployment source config-zip --resource-group mygroup --name myapp --src app.zip
az webapp deployment slot swap --resource-group mygroup --name myapp --slot staging

# SQL
az sql db list --resource-group mygroup --server myserver
az sql db show-connection-string --server myserver --name mydb --client ado.net

# Storage
az storage blob list --container-name mycontainer --account-name mystorage
az storage blob upload --container-name mycontainer --file local.txt --name remote.txt

# Key Vault
az keyvault secret list --vault-name myvault
az keyvault secret show --vault-name myvault --name mysecret
az keyvault secret set --vault-name myvault --name mysecret --value "value"
```

## Security Checklist

- [ ] Managed Identity instead of service principals
- [ ] RBAC with least privilege
- [ ] Private Endpoints for PaaS services
- [ ] Network Security Groups configured
- [ ] Key Vault for all secrets
- [ ] Diagnostic settings enabled
- [ ] Azure Defender/Security Center enabled
- [ ] Azure Policy for compliance
- [ ] TLS 1.2+ enforced everywhere

## Integration

Works with:
- `/terraform` - Azure provider configuration
- `/k8s` - AKS deployments
- `/devops` - Azure DevOps pipelines
- `/security` - Azure security review
