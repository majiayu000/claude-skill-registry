---
name: b2c-slas
description: Using the b2c CLI for SLAS (Shopper Login and API Access Service) client management
---

# B2C SLAS Skill

Use the `b2c` CLI plugin to manage SLAS (Shopper Login and API Access Service) API clients and credentials.

## When to Use This Skill

Common scenarios requiring SLAS client management:

- **Testing Custom APIs**: Create a client with custom scopes (e.g., `c_loyalty`) to test your Custom API endpoints
- **PWA/Headless Development**: Configure clients for composable storefronts
- **Integration Testing**: Create dedicated test clients with specific scope sets

## Examples

### List SLAS Clients

```bash
# list all SLAS clients for a tenant
b2c slas client list --tenant-id abcd_123

# list with JSON output
b2c slas client list --tenant-id abcd_123 --json
```

### Get SLAS Client Details

```bash
# get details for a specific SLAS client
b2c slas client get --tenant-id abcd_123 --client-id my-client-id
```

### Create SLAS Client

```bash
# create a new SLAS client with default scopes (auto-generates UUID client ID)
b2c slas client create --tenant-id abcd_123 --channels RefArch --default-scopes --redirect-uri http://localhost:3000/callback

# create with a specific client ID and custom scopes
b2c slas client create my-client-id --tenant-id abcd_123 --channels RefArch --scopes sfcc.shopper-products,sfcc.shopper-search --redirect-uri http://localhost:3000/callback

# create a public client
b2c slas client create --tenant-id abcd_123 --channels RefArch --default-scopes --redirect-uri http://localhost:3000/callback --public

# create client without auto-creating tenant (if you manage tenants separately)
b2c slas client create --tenant-id abcd_123 --channels RefArch --default-scopes --redirect-uri http://localhost:3000/callback --no-create-tenant

# output as JSON (useful for capturing the generated secret)
b2c slas client create --tenant-id abcd_123 --channels RefArch --default-scopes --redirect-uri http://localhost:3000/callback --json
```

Note: By default, the tenant is automatically created if it doesn't exist.

**Warning:** Use `--scopes` (plural) for client scopes, NOT `--scope` (singular). The `--scope` flag is a global authentication option and will cause errors if used here.

### Create Client for Custom API Testing

When testing a Custom API that requires custom scopes:

```bash
# Create a private client with custom scope for testing
# Replace c_my_scope with your API's custom scope from schema.yaml
b2c slas client create \
  --tenant-id zzpq_013 \
  --channels RefArch \
  --default-scopes \
  --scopes "c_my_scope" \
  --redirect-uri http://localhost:3000/callback \
  --json

# Output includes client_id and client_secret - save these for token requests
```

**Important:** The custom scope in your SLAS client must match the scope defined in your Custom API's `schema.yaml` security section.

### Get a Token for Testing

After creating a SLAS client, obtain a token for API testing:

```bash
# Set credentials from client creation output
# Find your shortcode in Business Manager: Administration > Site Development > Salesforce Commerce API Settings
SHORTCODE="kv7kzm78"  # Example shortcode - yours will be different
ORG="f_ecom_zzpq_013"
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"
SITE="RefArch"

# Get access token
curl -s "https://$SHORTCODE.api.commercecloud.salesforce.com/shopper/auth/v1/organizations/$ORG/oauth2/token" \
  -u "$CLIENT_ID:$CLIENT_SECRET" \
  -d "grant_type=client_credentials&channel_id=$SITE"
```

### Update SLAS Client

```bash
# update an existing SLAS client
b2c slas client update --tenant-id abcd_123 --client-id my-client-id
```

### Delete SLAS Client

```bash
# delete a SLAS client
b2c slas client delete --tenant-id abcd_123 --client-id my-client-id
```

### Configuration

The tenant ID can be set via environment variable:
- `SFCC_TENANT_ID`: SLAS tenant ID (organization ID)

### More Commands

See `b2c slas --help` for a full list of available commands and options in the `slas` topic.

## Related Skills

- `b2c:b2c-custom-api-development` - Creating Custom APIs that require SLAS authentication
- `b2c-cli:b2c-scapi-custom` - Checking Custom API registration status
