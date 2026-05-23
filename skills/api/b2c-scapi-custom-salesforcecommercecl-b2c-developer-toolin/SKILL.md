---
name: b2c-scapi-custom
description: Check Custom SCAPI endpoint registration status. Use when verifying custom API deployment, debugging "endpoint not found" errors, or checking if code activation registered new APIs. For creating new custom APIs, use b2c-custom-api-development instead.
---

# B2C SCAPI Custom APIs Skill

Use the `b2c` CLI plugin to manage SCAPI Custom API endpoints and check their registration status.

## Required: Tenant ID

The `--tenant-id` flag is **required** for all commands. The tenant ID identifies your B2C Commerce instance.

**Important:** The tenant ID is NOT the same as the organization ID:
- **Tenant ID**: `zzxy_prd` (used with commands that require `--tenant-id`)
- **Organization ID**: `f_ecom_zzxy_prd` (used in SCAPI URLs, has `f_ecom_` prefix)

### Deriving Tenant ID from Hostname

For sandbox instances, you can derive the tenant ID from the hostname by replacing hyphens with underscores:

| Hostname | Tenant ID |
|----------|-----------|
| `zzpq-013.dx.commercecloud.salesforce.com` | `zzpq_013` |
| `zzxy-001.dx.commercecloud.salesforce.com` | `zzxy_001` |
| `abcd-dev.dx.commercecloud.salesforce.com` | `abcd_dev` |

For production instances, use your realm and instance identifier (e.g., `zzxy_prd`).

## Examples

### Get Custom API Endpoint Status

```bash
# list all Custom API endpoints for an organization
b2c scapi custom status --tenant-id zzxy_prd

# list with JSON output
b2c scapi custom status --tenant-id zzxy_prd --json
```

### Filter by Status

```bash
# list only active endpoints
b2c scapi custom status --tenant-id zzxy_prd --status active

# list only endpoints that failed to register
b2c scapi custom status --tenant-id zzxy_prd --status not_registered
```

### Group by Type or Site

```bash
# group endpoints by API type (Admin vs Shopper)
b2c scapi custom status --tenant-id zzxy_prd --group-by type

# group endpoints by site
b2c scapi custom status --tenant-id zzxy_prd --group-by site
```

### Customize Output Columns

```bash
# show extended columns (includes error reasons, sites, etc.)
b2c scapi custom status --tenant-id zzxy_prd --extended

# select specific columns to display
b2c scapi custom status --tenant-id zzxy_prd --columns type,apiName,status,sites

# available columns: type, apiName, apiVersion, cartridgeName, endpointPath, httpMethod, status, sites, securityScheme, operationId, schemaFile, implementationScript, errorReason, id
```

### Debug Failed Registrations

```bash
# quickly find and diagnose failed Custom API registrations
b2c scapi custom status --tenant-id zzxy_prd --status not_registered --columns type,apiName,endpointPath,errorReason
```

### Configuration

The tenant ID and short code can be set via environment variables:
- `SFCC_TENANT_ID`: Tenant ID (e.g., `zzxy_prd`, not the organization ID)
- `SFCC_SHORTCODE`: SCAPI short code

### More Commands

See `b2c scapi custom --help` for a full list of available commands and options.

## Related Skills

- `b2c:b2c-custom-api-development` - Creating Custom API endpoints (schema, script, mapping)
- `b2c-cli:b2c-code` - Deploying and activating code versions (triggers registration)
