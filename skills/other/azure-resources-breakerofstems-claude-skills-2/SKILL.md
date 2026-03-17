---
name: azure-resources
description: Query Azure resources and configurations (read-only)
---

# Azure Resources Skill (Read-Only)

Query and inspect Azure resources without making changes.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Search, list, and inspect Azure resources to understand infrastructure.

## Commands

```bash
az account show -o json
az account list -o json
az group list -o json
az group show --name <name> -o json
az resource list -o json
az resource list --resource-group <rg> -o json
az resource list --resource-type <type> -o json
az resource show --ids <resource-id> -o json
```

## Output Format

**Always use `-o json`** for consistent, parseable output.

## Workflow Examples

### Get Current Subscription

```bash
az account show -o json
```

### List All Resource Groups

```bash
az group list -o json
```

### Find Resources by Type

```bash
# All VMs
az resource list --resource-type "Microsoft.Compute/virtualMachines" -o json

# All storage accounts
az resource list --resource-type "Microsoft.Storage/storageAccounts" -o json

# All App Services
az resource list --resource-type "Microsoft.Web/sites" -o json
```

### Inspect Specific Resource

```bash
az resource show --ids "/subscriptions/xxx/resourceGroups/yyy/providers/..." -o json
```

### Find Resources in a Resource Group

```bash
az resource list --resource-group my-rg -o json
```

## Common Resource Types

| Resource | Type String |
|----------|-------------|
| VM | `Microsoft.Compute/virtualMachines` |
| Storage | `Microsoft.Storage/storageAccounts` |
| App Service | `Microsoft.Web/sites` |
| SQL Database | `Microsoft.Sql/servers/databases` |
| Key Vault | `Microsoft.KeyVault/vaults` |
| AKS | `Microsoft.ContainerService/managedClusters` |

## Policies

- **Read-only only** - no create, update, delete, or set commands
- **Always use JSON output** for consistent parsing
- If asked to modify resources: stop, explain read-only scope, show what command would be needed, require explicit confirmation
