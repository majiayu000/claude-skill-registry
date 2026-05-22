---
name: azure-rbac
description: Query Azure RBAC role assignments and definitions (read-only)
---

# Azure RBAC Skill (Read-Only)

Inspect role-based access control assignments and definitions.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Query who has access to what in Azure without making changes.

## Commands

```bash
az role assignment list -o json
az role assignment list --assignee <principal> -o json
az role assignment list --scope <scope> -o json
az role assignment list --resource-group <rg> -o json
az role definition list -o json
az role definition show --name <role-name> -o json
```

## Output Format

**Always use `-o json`** for consistent, parseable output.

## Workflow Examples

### List All Role Assignments

```bash
az role assignment list -o json
```

### Check User's Permissions

```bash
az role assignment list --assignee "user@example.com" -o json
```

### Check Service Principal Access

```bash
az role assignment list --assignee <app-id-or-object-id> -o json
```

### List Assignments at Scope

```bash
# Resource group scope
az role assignment list --resource-group my-rg -o json

# Subscription scope
az role assignment list --scope "/subscriptions/<sub-id>" -o json

# Resource scope
az role assignment list --scope "/subscriptions/.../resourceGroups/.../providers/..." -o json
```

### Inspect Role Definition

```bash
# Built-in role
az role definition show --name "Contributor" -o json

# List all role definitions
az role definition list -o json

# Custom roles only
az role definition list --custom-role-only true -o json
```

## Common Built-in Roles

| Role | Description |
|------|-------------|
| Owner | Full access including RBAC |
| Contributor | Full access except RBAC |
| Reader | Read-only access |
| User Access Administrator | Manage RBAC only |

## Understanding Output

Role assignment includes:
- `principalId` - who has access
- `roleDefinitionName` - what role
- `scope` - where it applies

## Policies

- **Read-only only** - no role assignment create/delete
- **Always use JSON output**
- If asked to grant/revoke access: stop, explain read-only scope, show required command, require explicit confirmation
