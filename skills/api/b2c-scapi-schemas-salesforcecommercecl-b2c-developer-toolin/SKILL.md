---
name: b2c-scapi-schemas
description: Browse and retrieve SCAPI OpenAPI schemas. Use when exploring available SCAPI endpoints, checking API request/response formats, understanding SCAPI data models, or finding the right API for a task.
---

# B2C SCAPI Schemas Skill

Use the `b2c` CLI plugin to browse and retrieve SCAPI OpenAPI schema specifications.

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

### List Available Schemas

```bash
# list all available SCAPI schemas
b2c scapi schemas list --tenant-id zzxy_prd

# list with JSON output
b2c scapi schemas list --tenant-id zzxy_prd --json
```

### Filter Schemas

```bash
# filter by API family (e.g., product, checkout, search)
b2c scapi schemas list --tenant-id zzxy_prd --api-family product

# filter by API name
b2c scapi schemas list --tenant-id zzxy_prd --api-name shopper-products

# filter by status
b2c scapi schemas list --tenant-id zzxy_prd --status current
```

### Get Schema (Collapsed/Outline - Default)

By default, schemas are output in a collapsed format optimized for context efficiency. This is ideal for agentic use cases and LLM consumption.

```bash
# get collapsed schema (paths show methods, schemas show names only)
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd

# save to file
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd > schema.json
```

### Get Schema with Selective Expansion

Expand only the parts of the schema you need:

```bash
# expand specific paths
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --expand-paths /products,/products/{productId}

# expand specific schemas
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --expand-schemas Product,ProductResult

# combine expansions
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --expand-paths /products --expand-schemas Product
```

### Get Full Schema

```bash
# get full schema without any collapsing
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --expand-all
```

### List Available Paths/Schemas/Examples

Discover what's available in a schema before expanding:

```bash
# list all paths in the schema
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --list-paths

# list all schema names
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --list-schemas

# list all examples
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --list-examples
```

### Output Formats

```bash
# output as YAML
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --yaml

# output wrapped JSON with metadata (apiFamily, apiName, apiVersion, schema)
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --json
```

### Custom Properties

```bash
# include custom properties (default behavior)
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd

# exclude custom properties
b2c scapi schemas get product shopper-products v1 --tenant-id zzxy_prd --no-expand-custom-properties
```

### Configuration

The tenant ID and short code can be set via environment variables:
- `SFCC_TENANT_ID`: Tenant ID (e.g., `zzxy_prd`, not the organization ID)
- `SFCC_SHORTCODE`: SCAPI short code

### More Commands

See `b2c scapi schemas --help` for a full list of available commands and options.
