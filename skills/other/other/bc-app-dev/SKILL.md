---
name: bc-app-dev
description: Build BigCommerce apps — single-click apps, OAuth flow, app callbacks, connector apps, control panel integration, and App Marketplace submission. Use when creating integrations that install via the BigCommerce App Marketplace.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce App Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/integrations/apps` for the apps guide
2. Web-search `site:developer.bigcommerce.com apps guide auth` for OAuth patterns
3. Web-search `bigcommerce single-click app tutorial` for step-by-step implementation

## App Types

### Single-Click Apps

Apps installed from the BigCommerce App Marketplace:
- User clicks "Install" in the marketplace or admin panel
- BigCommerce initiates OAuth flow with your server
- Your app receives a permanent API token for that store
- Load your app UI in an iframe within BigCommerce admin

### Connector Apps

Simplified apps that don't embed UI in BigCommerce:
- OAuth install flow only — get an API token
- No admin panel iframe
- Typically background data sync services (ERP, shipping, marketing)

### Scripts-Only Apps

Inject JavaScript into the storefront without a full app:
- Use the Script Manager API after OAuth install
- No admin panel UI
- For analytics, chat widgets, A/B testing, etc.

## OAuth Flow

### Installation Flow

1. Merchant clicks "Install" — BigCommerce sends GET to your **Auth Callback URL** with `code`, `scope`, `context`
2. Your server exchanges `code` for a permanent `access_token` via POST to `https://login.bigcommerce.com/oauth2/token`
3. Store the `access_token`, `store_hash`, and `scope` for future API calls
4. Return HTML that BigCommerce renders in the admin iframe

### Load Callback

When the merchant opens your app in BigCommerce admin:
- BigCommerce sends GET to your **Load Callback URL** with a signed JWT
- Verify JWT signature using your Client Secret
- Extract `store_hash` and `user` from the JWT payload
- Return your app's UI HTML

### Uninstall Callback

When the merchant uninstalls:
- BigCommerce sends GET to your **Uninstall Callback URL** with a signed JWT
- Clean up stored tokens and data for that store

### Remove User Callback

When a specific user is removed from a multi-user store:
- Clean up user-specific data

## OAuth Token Exchange

### Request

POST to `https://login.bigcommerce.com/oauth2/token`:
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "code": "temporary_auth_code",
  "scope": "store_v2_products store_v2_orders",
  "grant_type": "authorization_code",
  "redirect_uri": "https://your-app.com/auth/callback",
  "context": "stores/{store_hash}"
}
```

### Response

```json
{
  "access_token": "permanent_token",
  "scope": "store_v2_products store_v2_orders",
  "user": { "id": 123, "email": "merchant@example.com" },
  "context": "stores/abc123",
  "account_uuid": "..."
}
```

## App Scopes

| Scope | Access |
|-------|--------|
| `store_v2_products` | Products, categories, brands |
| `store_v2_orders` | Orders, shipments |
| `store_v2_customers` | Customer data |
| `store_v2_content` | Pages, blog, redirects |
| `store_v2_marketing` | Coupons, gift certificates |
| `store_v2_information` | Store metadata |
| `store_channel_settings` | Channel/multi-storefront |
| `store_cart` | Cart operations |
| `store_checkout` | Checkout operations |
| `store_payments` | Payment processing |
| `store_themes_manage` | Theme operations |

Request minimum scopes necessary — principle of least privilege.

## Control Panel Integration

### Embedding in Admin

Your app loads in an iframe within the BigCommerce admin panel:
- Set `Content-Security-Policy` headers to allow framing by `*.bigcommerce.com`
- Handle the Load callback JWT to authenticate the session
- Use the BigCommerce admin design patterns for consistent UX

### BigDesign Component Library

BigCommerce provides a React component library for admin UIs:
- `@bigcommerce/big-design` — buttons, forms, tables, modals
- Matches the BigCommerce admin panel design language
- Install: `npm install @bigcommerce/big-design`

## App Marketplace Submission

### Requirements

- Valid OAuth flow (install, load, uninstall callbacks)
- HTTPS for all endpoints
- Privacy policy and terms of service
- App description, screenshots, icon
- Handle multi-user stores (different users on same store)
- Rate limit compliance

## Best Practices

- Store tokens securely — encrypted at rest
- Handle rate limits gracefully with exponential backoff
- Verify JWT signatures on all callbacks using your Client Secret
- Request minimum OAuth scopes
- Handle the uninstall callback — clean up data
- Support multi-user stores (multiple admin users)
- Use BigDesign components for admin panel UIs
- Never hardcode store hashes or tokens

Fetch the BigCommerce apps guide and OAuth documentation for exact callback parameters, JWT structure, and submission requirements before implementing.
