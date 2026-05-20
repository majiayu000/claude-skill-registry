---
name: bc-channels
description: Work with BigCommerce multi-channel — channels, multi-storefront, channel-specific catalog, site routing, and channel management API. Use when building multi-storefront solutions or managing channel-specific content.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Multi-Channel & Multi-Storefront

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/storefront/multi-storefront` for multi-storefront guide
2. Web-search `site:developer.bigcommerce.com channels api` for Channels API reference
3. Web-search `bigcommerce multi-storefront setup` for configuration patterns

## Channel Architecture

### What Channels Are

Channels represent distinct sales surfaces connected to a single BigCommerce store:
- Each channel can have its own **domain**, **theme**, **currency**, and **locale**
- Products, categories, and content can be **assigned per channel**
- Shared backend: orders, customers, inventory are centralized
- Channel types: `storefront`, `marketplace`, `pos`, `marketing`

### Default Channel

Every BigCommerce store has a default Stencil storefront (Channel ID 1). Additional channels are created for:
- Additional storefronts (B2B + B2C, regional sites)
- Marketplace integrations (Amazon, eBay)
- POS integrations
- Headless storefronts (Catalyst, custom)

## Channels API

### Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v3/channels` | GET, POST, PUT | Channel CRUD |
| `/v3/channels/{id}/site` | GET, POST, PUT, DELETE | Channel site (domain) |
| `/v3/channels/{id}/active-theme` | GET, PUT | Active theme |
| `/v3/channels/{id}/currency-assignments` | GET, POST, PUT, DELETE | Currency config |
| `/v3/channels/{id}/listings` | GET, POST, PUT | Product listings |

### Creating a Channel

```json
POST /v3/channels
{
  "name": "B2B Storefront",
  "type": "storefront",
  "platform": "catalyst",
  "status": "active",
  "is_listable_from_ui": true,
  "is_visible": true
}
```

### Channel Site

Associate a domain with a channel:
```json
POST /v3/channels/{id}/site
{
  "url": "https://b2b.example.com"
}
```

## Product Channel Assignments

### Assigning Products to Channels

`PUT /v3/catalog/products/channel-assignments`:
```json
[
  {
    "product_id": 111,
    "channel_id": 2
  },
  {
    "product_id": 222,
    "channel_id": 2
  }
]
```

### Querying by Channel

`GET /v3/catalog/products?channel_id:in=2` — products assigned to a specific channel.

### Category Channel Assignments

`PUT /v3/catalog/categories/channel-assignments` — assign categories to channels.

## Channel-Aware APIs

### Storefront API Tokens

Storefront API tokens are **channel-scoped**:
```json
POST /v3/storefront/api-token
{
  "channel_id": 2,
  "expires_at": 1893456000,
  "allowed_cors_origins": ["https://b2b.example.com"]
}
```

### Price Lists

Different pricing per channel:
- Create a Price List with channel-specific prices
- Assign the Price List to a channel
- Customers on that channel see the assigned prices

### Channel-Specific Settings

- Currency per channel
- Theme per channel
- Locale per channel
- Tax settings per channel

## Multi-Storefront Patterns

### B2B + B2C

- Channel 1: B2C storefront (consumer-facing)
- Channel 2: B2B storefront (wholesale pricing, customer groups)
- Same product catalog with different pricing and category visibility

### Regional Storefronts

- Channel per region/country
- Different currencies, locales, and product assortments
- Shared inventory and order management

### Headless + Stencil

- Channel 1: Stencil-powered storefront
- Channel 2: Catalyst (Next.js) headless storefront
- Both pulling from the same catalog

## Best Practices

- Use channels for distinct sales surfaces — not for A/B testing
- Assign products explicitly to channels — don't rely on "all channels" visibility
- Use Price Lists for channel-specific pricing
- Create channel-scoped Storefront API tokens — don't share tokens across channels
- Use channel-aware webhook filters for per-channel event handling
- Plan your channel architecture before building — adding channels later requires product reassignment
- Test each channel independently

Fetch the BigCommerce Multi-Storefront documentation and Channels API reference for exact endpoints, configuration options, and current multi-storefront capabilities before implementing.
