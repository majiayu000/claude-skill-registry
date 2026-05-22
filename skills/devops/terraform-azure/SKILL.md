---
name: terraform-azure
description: Provision Azure infrastructure with Terraform including VNets, VMs, AKS, and managed identities
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 05-terraform-azure
bond_type: PRIMARY_BOND
---

# Terraform Azure Skill

Production patterns for Azure infrastructure provisioning with security best practices.

## Provider Setup

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}
```

## Resource Group

```hcl
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}
```

## Virtual Network

### Hub-Spoke Architecture
```hcl
resource "azurerm_virtual_network" "hub" {
  name                = "${var.project}-hub-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.0.0/27"]
}

resource "azurerm_virtual_network" "spoke" {
  name                = "${var.project}-spoke-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                      = "hub-to-spoke"
  resource_group_name       = azurerm_resource_group.main.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.spoke.id
  allow_gateway_transit     = true
}
```

### Network Security Group
```hcl
resource "azurerm_network_security_group" "web" {
  name                = "${var.project}-web-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_network_security_rule" "https" {
  name                        = "AllowHTTPS"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.web.name
}
```

## Managed Identity

```hcl
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.project}-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

## AKS Cluster

```hcl
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.project

  kubernetes_version        = "1.28"
  automatic_channel_upgrade = "stable"
  sku_tier                  = var.environment == "prod" ? "Standard" : "Free"

  default_node_pool {
    name                = "system"
    node_count          = 3
    vm_size             = "Standard_D4s_v3"
    vnet_subnet_id      = azurerm_subnet.aks.id
    zones               = ["1", "2", "3"]
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 5
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks.id]
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
  }

  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }
}
```

## Key Vault

```hcl
resource "azurerm_key_vault" "main" {
  name                        = "${var.project}kv"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 90
  purge_protection_enabled    = true
  enable_rbac_authorization   = true

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }
}
```

## Storage Account

```hcl
resource "azurerm_storage_account" "main" {
  name                     = "${var.project}storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = var.environment == "prod" ? "GRS" : "LRS"

  min_tls_version                 = "TLS1_2"
  enable_https_traffic_only       = true
  allow_nested_items_to_be_public = false

  blob_properties {
    versioning_enabled = true
  }
}
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthorizationFailed` | Missing RBAC | Add role assignment |
| `SubnetIsFull` | CIDR too small | Use larger subnet |
| `SkuNotAvailable` | Region limitation | Try different SKU/region |
| `QuotaExceeded` | Subscription limit | Request quota increase |

## Usage

```python
Skill("terraform-azure")
```

## Related

- **Agent**: 05-terraform-azure (PRIMARY_BOND)
