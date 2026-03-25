---
name: bc-customers
description: Work with BigCommerce customers — Customer API, customer groups, addresses, stored instruments, attributes, Customer Login API (SSO), and customer segmentation. Use when building customer-facing features or integrating customer data.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Customer Management

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com rest customers` for Customers API reference
2. Fetch `https://developer.bigcommerce.com/docs/start/authentication/customer-login` for Customer Login API
3. Web-search `bigcommerce customer groups api` for customer group management

## Customer API (V3)

### Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v3/customers` | GET, POST, PUT, DELETE | Customer CRUD |
| `/v3/customers/addresses` | GET, POST, PUT, DELETE | Customer addresses |
| `/v3/customers/attributes` | GET, POST, PUT, DELETE | Custom attribute definitions |
| `/v3/customers/attribute-values` | GET, PUT, DELETE | Attribute values per customer |
| `/v3/customers/form-field-values` | GET, PUT | Form field values |
| `/v3/customers/settings` | GET, PUT | Customer settings |

### Customer Fields

Core fields:
- `id`, `email`, `first_name`, `last_name`, `company`
- `phone`, `date_created`, `date_modified`
- `customer_group_id` — assigned group
- `notes` — admin notes
- `registration_ip_address`
- `authentication` — password or external auth

### Creating Customers

```json
POST /v3/customers
[{
  "email": "customer@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "authentication": {
    "new_password": "SecurePassword123!"
  }
}]
```

Note: V3 accepts arrays — batch create/update multiple customers at once.

## Customer Groups

### What They Do

Segment customers for pricing, access, and promotions:
- **Price Lists** — group-specific pricing
- **Category Access** — restrict category visibility by group
- **Promotions** — group-specific discounts
- **Tax Exemptions** — tax-exempt groups

### Managing Groups

- `GET /v2/customer_groups` — list groups
- `POST /v2/customer_groups` — create group
- Assign customers via `customer_group_id` field on customer

### Default Groups

| Group | Description |
|-------|-------------|
| Guest | Non-logged-in visitors |
| Default | Default for new customers |
| Custom groups | Merchant-defined segments |

## Customer Addresses

### CRUD Operations

```json
POST /v3/customers/addresses
[{
  "customer_id": 123,
  "first_name": "Jane",
  "last_name": "Doe",
  "address1": "123 Main St",
  "city": "Austin",
  "state_or_province": "Texas",
  "postal_code": "78701",
  "country_code": "US",
  "address_type": "residential"
}]
```

## Custom Attributes

### Attribute Definitions

Create custom fields for customer profiles:
```json
POST /v3/customers/attributes
[{
  "name": "Loyalty Tier",
  "type": "string"
}]
```

Types: `string`, `number`, `date`, `dropdown`

### Attribute Values

Set per customer:
```json
PUT /v3/customers/attribute-values
[{
  "customer_id": 123,
  "attribute_id": 1,
  "value": "Gold"
}]
```

## Customer Login API (SSO)

### How It Works

Log customers into BigCommerce storefront from an external system:
1. Generate a JWT token on your server with customer info
2. Sign with your Client Secret
3. Redirect customer to `https://{store_url}/login/token/{jwt}`
4. BigCommerce validates the JWT and creates a session

### JWT Payload

```json
{
  "iss": "your_client_id",
  "iat": 1706140800,
  "jti": "unique-request-id",
  "operation": "customer_login",
  "store_hash": "abc123",
  "customer_id": 456,
  "redirect_to": "/account",
  "channel_id": 1
}
```

Sign with HMAC-SHA256 using your Client Secret.

### Use Cases

- Single Sign-On (SSO) from your own auth system
- Deep linking logged-in customers into their BigCommerce account
- Headless storefronts using external authentication

## Customer Impersonation (GraphQL)

For accessing customer-specific data in the GraphQL Storefront API:
- Create impersonation token: `POST /v3/storefront/api-token-customer-impersonation`
- Send with `X-Bc-Customer-Id: {customer_id}` header
- Access wishlists, order history, saved addresses in GraphQL

## Querying Customers

### V3 Filters

- `id:in=1,2,3` — by IDs
- `email:in=a@b.com,c@d.com` — by emails
- `name:like=Jane` — name search
- `customer_group_id:in=5,6` — by group
- `date_created:min=2024-01-01` — date range
- `include=addresses,attributes` — include sub-resources

## Best Practices

- Use V3 Customers API for all new development
- Batch operations — V3 accepts arrays for create/update
- Use customer groups for segmentation and pricing tiers
- Use custom attributes for integration data (not notes)
- Implement SSO via Customer Login API for seamless cross-platform auth
- Validate email addresses before creating customers
- Handle duplicate email addresses gracefully (BigCommerce enforces unique emails)
- Use customer impersonation tokens for personalized GraphQL queries

Fetch the BigCommerce Customers API reference and Customer Login API documentation for exact endpoints, JWT format, and attribute types before implementing.
