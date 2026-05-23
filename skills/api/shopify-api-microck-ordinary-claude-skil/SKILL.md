---
name: shopify-api
description: Complete API integration guide for Shopify including GraphQL Admin API, REST Admin API, Storefront API, Ajax API, OAuth authentication, rate limiting, and webhooks. Use when making API calls to Shopify, authenticating apps, fetching product/order/customer data programmatically, implementing cart operations, handling webhooks, or working with API version 2025-10. Requires fetch or axios for JavaScript implementations.
---

# Shopify API Integration

Expert guidance for all Shopify APIs including GraphQL Admin API, REST Admin API, Storefront API, Ajax API, authentication, and webhooks.

## When to Use This Skill

Invoke this skill when:

- Making GraphQL or REST API calls to Shopify
- Implementing OAuth 2.0 authentication for apps
- Fetching product, collection, order, or customer data programmatically
- Using Storefront API for headless commerce
- Implementing Ajax cart operations in themes
- Setting up webhooks for event handling
- Working with API version 2025-10
- Handling rate limiting and API errors
- Building custom integrations with Shopify
- Using Shopify Admin API from Node.js, Python, or other languages

## Core Capabilities

### 1. GraphQL Admin API

Modern API for Shopify Admin operations with efficient data fetching.

**Endpoint:**
```
POST https://{store}.myshopify.com/admin/api/2025-10/graphql.json
```

**Headers:**
```javascript
{
  'X-Shopify-Access-Token': 'shpat_...',
  'Content-Type': 'application/json'
}
```

**Basic Query:**
```graphql
query GetProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        handle
        status
        vendor
        productType

        # Pricing
        priceRange {
          minVariantPrice { amount currencyCode }
          maxVariantPrice { amount currencyCode }
        }

        # Images
        images(first: 5) {
          edges {
            node {
              id
              url
              altText
            }
          }
        }

        # Variants
        variants(first: 10) {
          edges {
            node {
              id
              title
              sku
              price
              inventoryQuantity
              available: availableForSale
            }
          }
        }
      }
    }

    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```

**Variables:**
```json
{
  "first": 10
}
```

**JavaScript Example:**
```javascript
async function getProducts(accessToken, store, limit = 10) {
  const query = `
    query GetProducts($first: Int!) {
      products(first: $first) {
        edges {
          node {
            id
            title
            handle
            priceRange {
              minVariantPrice { amount currencyCode }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `;

  const response = await fetch(
    `https://${store}.myshopify.com/admin/api/2025-10/graphql.json`,
    {
      method: 'POST',
      headers: {
        'X-Shopify-Access-Token': accessToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables: { first: limit },
      }),
    }
  );

  const { data, errors } = await response.json();

  if (errors) {
    console.error('GraphQL Errors:', errors);
    throw new Error(errors[0].message);
  }

  return data.products;
}
```

**Common Mutations:**

Create product:
```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

Update product:
```graphql
mutation UpdateProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

Set metafield:
```graphql
mutation SetMetafield($input: MetafieldInput!) {
  metafieldSet(input: $input) {
    metafield {
      id
      namespace
      key
      value
      type
    }
    userErrors {
      field
      message
    }
  }
}
```

### 2. REST Admin API

Traditional REST API for Shopify Admin operations.

**Base URL:**
```
https://{store}.myshopify.com/admin/api/2025-10/
```

**Authentication:**
```javascript
headers: {
  'X-Shopify-Access-Token': 'shpat_...'
}
```

**Common Endpoints:**

Get products:
```javascript
GET /admin/api/2025-10/products.json?limit=50&status=active

// JavaScript
const response = await fetch(
  `https://${store}.myshopify.com/admin/api/2025-10/products.json?limit=50`,
  {
    headers: {
      'X-Shopify-Access-Token': accessToken,
    },
  }
);

const { products } = await response.json();
```

Get single product:
```javascript
GET /admin/api/2025-10/products/{product_id}.json
```

Create product:
```javascript
POST /admin/api/2025-10/products.json

// Body
{
  "product": {
    "title": "New Product",
    "body_html": "<p>Description</p>",
    "vendor": "My Vendor",
    "product_type": "Shoes",
    "status": "draft"
  }
}
```

Update product:
```javascript
PUT /admin/api/2025-10/products/{product_id}.json

// Body
{
  "product": {
    "id": 123456789,
    "title": "Updated Title"
  }
}
```

Get orders:
```javascript
GET /admin/api/2025-10/orders.json?status=any&limit=50
```

Get customers:
```javascript
GET /admin/api/2025-10/customers.json?limit=50
```

### 3. OAuth 2.0 Authentication

Complete OAuth flow for custom apps.

**Step 1: Authorization Request**
```
GET https://{shop}.myshopify.com/admin/oauth/authorize?
  client_id={api_key}&
  redirect_uri={redirect_uri}&
  scope={scopes}&
  state={random_state}
```

**Scopes:**
```javascript
const scopes = [
  'read_products',
  'write_products',
  'read_orders',
  'write_orders',
  'read_customers',
  'write_customers',
  'read_inventory',
  'write_inventory',
  'read_metafields',
  'write_metafields',
].join(',');
```

**Step 2: Handle Callback**
```javascript
// User approves, Shopify redirects to:
GET {redirect_uri}?code={auth_code}&state={state}&hmac={hmac}&shop={shop}

// Verify HMAC for security
function verifyHmac(query, secret) {
  const { hmac, ...params } = query;

  const message = Object.keys(params)
    .sort()
    .map(key => `${key}=${params[key]}`)
    .join('&');

  const hash = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');

  return hash === hmac;
}
```

**Step 3: Exchange Code for Token**
```javascript
POST https://{shop}.myshopify.com/admin/oauth/access_token

// Body
{
  "client_id": "{api_key}",
  "client_secret": "{api_secret}",
  "code": "{auth_code}"
}

// Response
{
  "access_token": "shpat_...",
  "scope": "write_products,read_orders"
}

// Node.js example
async function getAccessToken(shop, code, apiKey, apiSecret) {
  const response = await fetch(
    `https://${shop}/admin/oauth/access_token`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        client_id: apiKey,
        client_secret: apiSecret,
        code,
      }),
    }
  );

  const { access_token, scope } = await response.json();
  return { access_token, scope };
}
```

### 4. Rate Limiting

GraphQL uses points-based rate limiting.

**Rate Limits:**
- 50 cost points per second maximum
- Bucket refills at 50 points/second
- Each query has a calculated cost

**Check Rate Limit:**
```javascript
const response = await fetch(graphqlEndpoint, options);

const rateLimitHeader = response.headers.get('X-Shopify-GraphQL-Admin-Api-Call-Limit');
// Example: "42/50" (42 points used, 50 max)

const [used, limit] = rateLimitHeader.split('/').map(Number);

if (used > 40) {
  // Approaching limit, slow down
  await delay(1000);
}
```

**Implement Retry Logic:**
```javascript
async function fetchWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options);

    if (response.status === 429) {
      // Rate limited
      const retryAfter = response.headers.get('Retry-After') || 2;
      await delay(retryAfter * 1000 * Math.pow(2, i)); // Exponential backoff
      continue;
    }

    return response;
  }

  throw new Error('Max retries exceeded');
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### 5. Storefront API

Public API for headless/custom storefronts.

**Endpoint:**
```
POST https://{store}.myshopify.com/api/2025-10/graphql.json
```

**Headers (Public Access):**
```javascript
{
  'Content-Type': 'application/json',
  'X-Shopify-Storefront-Access-Token': '{public_token}' // Optional for public stores
}
```

**Query Products:**
```graphql
query GetProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        handle
        description
        priceRange {
          minVariantPrice { amount currencyCode }
          maxVariantPrice { amount currencyCode }
        }
        images(first: 3) {
          edges {
            node {
              url
              altText
            }
          }
        }
        variants(first: 10) {
          edges {
            node {
              id
              title
              price { amount currencyCode }
              availableForSale
              sku
            }
          }
        }
      }
    }
  }
}
```

**Cart Operations:**

Create cart:
```graphql
mutation CreateCart($input: CartInput!) {
  cartCreate(input: $input) {
    cart {
      id
      checkoutUrl
      lines(first: 10) {
        edges {
          node {
            id
            quantity
            merchandise {
              ... on ProductVariant {
                id
                title
                price { amount }
              }
            }
          }
        }
      }
      cost {
        totalAmount { amount currencyCode }
        subtotalAmount { amount }
        totalTaxAmount { amount }
      }
    }
  }
}
```

Add to cart:
```graphql
mutation AddToCart($cartId: ID!, $lines: [CartLineInput!]!) {
  cartLinesAdd(cartId: $cartId, lines: $lines) {
    cart {
      id
      lines(first: 10) {
        edges {
          node {
            id
            quantity
          }
        }
      }
    }
  }
}
```

### 6. Ajax API (Theme-Only)

JavaScript API for cart operations in themes.

**Get Cart:**
```javascript
fetch('/cart.js')
  .then(response => response.json())
  .then(cart => {
    console.log('Cart:', cart);
    console.log('Item count:', cart.item_count);
    console.log('Total:', cart.total_price);
    console.log('Items:', cart.items);
  });
```

**Add to Cart:**
```javascript
fetch('/cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: variantId,              // Required: variant ID
    quantity: 1,                 // Optional: default 1
    properties: {                // Optional: custom data
      'Gift wrap': 'Yes',
      'Note': 'Happy Birthday!'
    }
  })
})
  .then(response => response.json())
  .then(item => {
    console.log('Added to cart:', item);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

**Update Cart:**
```javascript
fetch('/cart/change.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    line: 1,          // Line item index (1-based)
    quantity: 2       // New quantity (0 = remove)
  })
})
  .then(response => response.json())
  .then(cart => console.log('Updated cart:', cart));
```

**Clear Cart:**
```javascript
fetch('/cart/clear.js', { method: 'POST' })
  .then(response => response.json())
  .then(cart => console.log('Cart cleared'));
```

**Update Cart Attributes:**
```javascript
fetch('/cart/update.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    attributes: {
      'gift_wrap': 'true',
      'gift_message': 'Happy Birthday!'
    },
    note: 'Please handle with care'
  })
})
  .then(response => response.json())
  .then(cart => console.log('Cart updated'));
```

### 7. Webhooks

Event-driven notifications for app integrations.

**Common Webhooks:**
```javascript
// Product events
'products/create'
'products/update'
'products/delete'

// Order events
'orders/create'
'orders/updated'
'orders/paid'
'orders/fulfilled'
'orders/cancelled'

// Customer events
'customers/create'
'customers/update'
'customers/delete'

// Cart events
'carts/create'
'carts/update'

// Inventory events
'inventory_levels/update'

// App events
'app/uninstalled'
```

**Register Webhook (GraphQL):**
```graphql
mutation CreateWebhook($input: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(input: $input) {
    webhookSubscription {
      id
      topic
      endpoint {
        __typename
        ... on WebhookHttpEndpoint {
          callbackUrl
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "topic": "ORDERS_CREATE",
    "webhookSubscription": {
      "callbackUrl": "https://your-app.com/webhooks/orders",
      "format": "JSON"
    }
  }
}
```

**Handle Webhook (Node.js/Express):**
```javascript
app.post('/webhooks/orders', async (req, res) => {
  // Verify webhook HMAC
  const hmac = req.headers['x-shopify-hmac-sha256'];
  const body = JSON.stringify(req.body);

  const hash = crypto
    .createHmac('sha256', SHOPIFY_WEBHOOK_SECRET)
    .update(body)
    .digest('base64');

  if (hash !== hmac) {
    return res.status(401).send('Invalid HMAC');
  }

  // Process order
  const order = req.body;
  console.log('New order:', order.id, order.email);

  // Respond quickly (within 5 seconds)
  res.status(200).send('OK');

  // Process in background
  await processOrder(order);
});
```

## Common Patterns

### Pagination (GraphQL)

```javascript
async function getAllProducts(accessToken, store) {
  let allProducts = [];
  let hasNextPage = true;
  let cursor = null;

  while (hasNextPage) {
    const query = `
      query GetProducts($first: Int!, $after: String) {
        products(first: $first, after: $after) {
          edges {
            node { id title }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    `;

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'X-Shopify-Access-Token': accessToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables: { first: 50, after: cursor },
      }),
    });

    const { data } = await response.json();
    allProducts.push(...data.products.edges.map(e => e.node));

    hasNextPage = data.products.pageInfo.hasNextPage;
    cursor = data.products.pageInfo.endCursor;
  }

  return allProducts;
}
```

### Error Handling

```javascript
async function safeApiCall(query, variables) {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'X-Shopify-Access-Token': accessToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, variables }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const { data, errors } = await response.json();

    if (errors) {
      console.error('GraphQL Errors:', errors);
      throw new Error(errors[0].message);
    }

    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

## Best Practices

1. **Always check API version** - Use latest stable (2025-10)
2. **Implement rate limit handling** - Use exponential backoff
3. **Verify webhook HMAC** - Security critical
4. **Use GraphQL over REST** when possible - More efficient
5. **Request only needed fields** - Reduce response size
6. **Handle errors gracefully** - Check `errors` and `userErrors`
7. **Store access tokens securely** - Never expose in client code
8. **Use minimum necessary scopes** - Security best practice
9. **Implement retry logic** - Handle transient failures
10. **Respond to webhooks quickly** - Within 5 seconds

## Detailed References

- **[references/graphql-queries.md](references/graphql-queries.md)** - Complete query examples
- **[references/rest-endpoints.md](references/rest-endpoints.md)** - All REST endpoints
- **[references/webhook-payloads.md](references/webhook-payloads.md)** - Webhook payload structures

## Integration with Other Skills

- **shopify-app-dev** - Use when building custom Shopify apps
- **shopify-liquid** - Use when displaying API data in theme templates
- **shopify-debugging** - Use when troubleshooting API errors
- **shopify-performance** - Use when optimizing API request patterns

## Quick Reference

```javascript
// GraphQL Admin API
POST https://{store}.myshopify.com/admin/api/2025-10/graphql.json
Headers: { 'X-Shopify-Access-Token': 'shpat_...' }

// REST Admin API
GET https://{store}.myshopify.com/admin/api/2025-10/products.json
Headers: { 'X-Shopify-Access-Token': 'shpat_...' }

// Storefront API
POST https://{store}.myshopify.com/api/2025-10/graphql.json
Headers: { 'X-Shopify-Storefront-Access-Token': 'token' }

// Ajax API (theme)
fetch('/cart.js')
fetch('/cart/add.js', { method: 'POST', body: ... })
fetch('/cart/change.js', { method: 'POST', body: ... })
```
