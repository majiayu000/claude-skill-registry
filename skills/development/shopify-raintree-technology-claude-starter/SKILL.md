---
name: shopify-expert
description: Comprehensive Shopify development expert with access to 24 official documentation files covering APIs (GraphQL Admin, Storefront, REST), app development, themes, Liquid, Hydrogen, checkout, extensions, webhooks, Functions, CLI, subscriptions, payments, and all platform features. Invoke when user mentions Shopify, e-commerce, online store, product management, orders, checkout, themes, or headless commerce.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
---

# Shopify Development Expert

## Purpose

Provide comprehensive, accurate guidance for building on Shopify's platform based on 24+ official documentation files. Cover all aspects of app development, theme customization, API integration, checkout extensions, and e-commerce features.

## Documentation Coverage

**Full access to official Shopify documentation (when available):**
- **Location:** `docs/shopify/`
- **Files:** 25 markdown files
- **Coverage:** Complete API reference, guides, best practices, and implementation patterns

**Note:** Documentation must be pulled separately:
```bash
pipx install docpull
docpull https://shopify.dev/docs -o .claude/skills/shopify/docs
```

**Major Areas:**
- GraphQL Admin API (products, orders, customers, inventory)
- Storefront API (cart, checkout, customer accounts)
- REST Admin API (legacy support)
- App development (authentication, webhooks, extensions)
- Theme development (Liquid, sections, blocks)
- Headless commerce (Hydrogen, Oxygen)
- Checkout customization (UI extensions, validation)
- Shopify Functions (discounts, delivery, payments)
- POS extensions (in-person sales)
- Subscriptions and selling plans
- Metafields and custom data
- Shopify Flow automation
- CLI and development tools
- Privacy and compliance
- Performance optimization

## When to Use

Invoke when user mentions:
- **Platform:** Shopify, e-commerce, online store, merchant
- **APIs:** GraphQL, REST, Storefront API, Admin API
- **Products:** product management, collections, variants, inventory
- **Orders:** order processing, fulfillment, shipping
- **Customers:** customer data, accounts, authentication
- **Checkout:** checkout customization, payment methods, delivery options
- **Themes:** Liquid templates, theme development, sections, blocks
- **Apps:** app development, extensions, webhooks, OAuth
- **Headless:** Hydrogen, React, headless commerce, Oxygen
- **Functions:** Shopify Functions, custom logic, discounts
- **Subscriptions:** recurring billing, selling plans, subscriptions
- **Tools:** Shopify CLI, development workflow
- **POS:** point of sale, retail, in-person payments

## How to Use Documentation

When answering questions:

1. **Search for specific topics:**
   ```bash
   # Use Grep to find relevant docs
   grep -r "checkout" .claude/skills/shopify/docs/ --include="*.md"
   ```

2. **Read specific documentation:**
   ```bash
   # API docs
   cat .claude/skills/shopify/docs/shopify/api-admin-graphql.md
   cat .claude/skills/shopify/docs/shopify/api-storefront.md
   ```

3. **Find implementation guides:**
   ```bash
   # List all guides
   ls .claude/skills/shopify/docs/shopify/
   ```

## Core Authentication

### OAuth 2.0 Flow

```javascript
// Redirect to Shopify OAuth
const authUrl = `https://${shop}/admin/oauth/authorize?` +
  `client_id=${process.env.SHOPIFY_API_KEY}&` +
  `scope=read_products,write_products&` +
  `redirect_uri=${redirectUri}&` +
  `state=${nonce}`;

// Exchange code for access token
const response = await fetch(
  `https://${shop}/admin/oauth/access_token`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: process.env.SHOPIFY_API_KEY,
      client_secret: process.env.SHOPIFY_API_SECRET,
      code
    })
  }
);

const { access_token } = await response.json();
```

### Session Tokens (Modern Embedded Apps)

```javascript
import { shopifyApi } from '@shopify/shopify-api';

const shopify = shopifyApi({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  scopes: ['read_products', 'write_products'],
  hostName: process.env.HOST,
  isEmbeddedApp: true,
});
```

## GraphQL Admin API

### Query Products

```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        handle
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
        variants(first: 5) {
          edges {
            node {
              id
              sku
              inventoryQuantity
            }
          }
        }
      }
    }
  }
}
```

### Create Product

```graphql
mutation {
  productCreate(input: {
    title: "New Product"
    vendor: "My Store"
    productType: "Apparel"
    variants: [{
      price: "29.99"
      sku: "PROD-001"
    }]
  }) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

### Fetch Orders

```graphql
query {
  orders(first: 25, query: "fulfillment_status:unfulfilled") {
    edges {
      node {
        id
        name
        createdAt
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          email
        }
        lineItems(first: 10) {
          edges {
            node {
              title
              quantity
            }
          }
        }
      }
    }
  }
}
```

## Storefront API

### Create Cart

```graphql
mutation {
  cartCreate(input: {
    lines: [{
      merchandiseId: "gid://shopify/ProductVariant/123"
      quantity: 1
    }]
  }) {
    cart {
      id
      checkoutUrl
      cost {
        totalAmount {
          amount
          currencyCode
        }
      }
    }
  }
}
```

### Update Cart

```graphql
mutation {
  cartLinesUpdate(
    cartId: "gid://shopify/Cart/xyz"
    lines: [{
      id: "gid://shopify/CartLine/abc"
      quantity: 2
    }]
  ) {
    cart {
      id
      lines(first: 10) {
        edges {
          node {
            quantity
          }
        }
      }
    }
  }
}
```

## Webhooks

### Setup Webhook

```javascript
// Register webhook via API
const webhook = await shopify.webhooks.register({
  topic: 'ORDERS_CREATE',
  address: 'https://your-app.com/webhooks/orders-create',
  format: 'json'
});
```

### Verify Webhook

```javascript
import crypto from 'crypto';

function verifyWebhook(body, hmacHeader, secret) {
  const hash = crypto
    .createHmac('sha256', secret)
    .update(body, 'utf8')
    .digest('base64');

  return hash === hmacHeader;
}

// In webhook handler
app.post('/webhooks/orders-create', async (req, res) => {
  const hmac = req.headers['x-shopify-hmac-sha256'];
  const body = await req.text();

  if (!verifyWebhook(body, hmac, process.env.SHOPIFY_API_SECRET)) {
    return res.status(401).send('Invalid HMAC');
  }

  const order = JSON.parse(body);
  // Process order...

  res.status(200).send('OK');
});
```

## Liquid Templates

### Basic Liquid

```liquid
<!-- Output product title -->
{{ product.title }}

<!-- Conditional logic -->
{% if product.available %}
  <button>Add to Cart</button>
{% else %}
  <span>Sold Out</span>
{% endif %}

<!-- Loop through variants -->
{% for variant in product.variants %}
  <option value="{{ variant.id }}">
    {{ variant.title }} - {{ variant.price | money }}
  </option>
{% endfor %}
```

### Custom Section

```liquid
{% schema %}
{
  "name": "Featured Product",
  "settings": [
    {
      "type": "product",
      "id": "product",
      "label": "Product"
    }
  ]
}
{% endschema %}

{% if section.settings.product %}
  {% assign product = section.settings.product %}
  <div class="featured-product">
    <img src="{{ product.featured_image | img_url: '500x' }}" alt="{{ product.title }}">
    <h2>{{ product.title }}</h2>
    <p>{{ product.price | money }}</p>
  </div>
{% endif %}
```

## Shopify Functions

### Discount Function

```javascript
// Function to apply volume discount
export default (input) => {
  const quantity = input.cart.lines.reduce((sum, line) => sum + line.quantity, 0);

  let discountPercentage = 0;
  if (quantity >= 10) discountPercentage = 20;
  else if (quantity >= 5) discountPercentage = 10;

  if (discountPercentage > 0) {
    return {
      discounts: [{
        message: `${discountPercentage}% volume discount`,
        targets: [{
          orderSubtotal: {
            excludedVariantIds: []
          }
        }],
        value: {
          percentage: {
            value: discountPercentage.toString()
          }
        }
      }]
    };
  }

  return { discounts: [] };
};
```

### Delivery Customization

```javascript
// Hide specific delivery options
export default (input) => {
  const operations = [];

  // Hide express shipping for orders under $100
  const cartTotal = parseFloat(input.cart.cost.subtotalAmount.amount);

  if (cartTotal < 100) {
    const expressOptions = input.cart.deliveryGroups[0].deliveryOptions
      .filter(option => option.title.toLowerCase().includes('express'));

    expressOptions.forEach(option => {
      operations.push({
        hide: {
          deliveryOptionHandle: option.handle
        }
      });
    });
  }

  return { operations };
};
```

## Hydrogen (Headless Commerce)

### Product Page

```typescript
// app/routes/products.$handle.tsx
import {json, LoaderFunctionArgs} from '@shopify/remix-oxygen';
import {useLoaderData} from '@remix-run/react';

export async function loader({params, context}: LoaderFunctionArgs) {
  const {product} = await context.storefront.query(PRODUCT_QUERY, {
    variables: {handle: params.handle},
  });

  return json({product});
}

export default function Product() {
  const {product} = useLoaderData<typeof loader>();

  return (
    <div>
      <h1>{product.title}</h1>
      <img src={product.featuredImage.url} alt={product.title} />
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  );
}

const PRODUCT_QUERY = `#graphql
  query Product($handle: String!) {
    product(handle: $handle) {
      id
      title
      description
      featuredImage {
        url
        altText
      }
      variants(first: 10) {
        nodes {
          id
          price {
            amount
            currencyCode
          }
        }
      }
    }
  }
`;
```

## Shopify CLI

### Common Commands

```bash
# Create new app
shopify app init

# Start development server
shopify app dev

# Deploy app
shopify app deploy

# Create extension
shopify app generate extension

# Create theme
shopify theme init

# Serve theme locally
shopify theme dev --store=your-store.myshopify.com

# Push theme
shopify theme push

# Pull theme
shopify theme pull
```

## Testing

### Test Stores

1. Create Partner account: https://partners.shopify.com
2. Create development store
3. Install your app
4. Test features

### Test Data

```javascript
// Create test product
const product = await shopify.rest.Product.save({
  session,
  title: "Test Product",
  body_html: "<strong>Test description</strong>",
  vendor: "Test Vendor",
  product_type: "Test Type",
  variants: [{
    price: "19.99",
    sku: "TEST-001"
  }]
});

// Create test order
const order = await shopify.rest.Order.save({
  session,
  line_items: [{
    variant_id: 123456789,
    quantity: 1
  }],
  customer: {
    email: "test@example.com"
  }
});
```

## Security Best Practices

1. **API Keys:**
   - Store in environment variables
   - Never commit to version control
   - Use separate keys per environment
   - Rotate if compromised

2. **Webhooks:**
   - ALWAYS verify HMAC signatures
   - Use HTTPS endpoints only
   - Return 200 immediately
   - Process async

3. **Access Scopes:**
   - Request minimal scopes
   - Document why each scope is needed
   - Review periodically

4. **Rate Limits:**
   - Respect API rate limits
   - Implement exponential backoff
   - Monitor API usage

## Common Errors

### API Authentication

- `Invalid access token` - Check token is valid and has correct scopes
- `Shop not found` - Verify shop domain format
- `Missing access token` - Include X-Shopify-Access-Token header

### GraphQL Errors

- `User errors` - Check `userErrors` field in response
- `Throttled` - Reduce request rate
- `Field not found` - Verify API version supports field

### Webhook Issues

- `Invalid HMAC` - Check webhook secret and verification logic
- `Delivery failed` - Ensure endpoint returns 200 within timeout
- `Not receiving webhooks` - Check webhook registration and endpoint URL

## Resources

- **Dashboard:** https://partners.shopify.com
- **Documentation:** https://shopify.dev
- **GraphiQL Admin:** https://shopify.dev/docs/apps/tools/graphiql-admin-api
- **Community:** https://community.shopify.com
- **Status:** https://www.shopifystatus.com

## Documentation Quick Reference

**Need to find something specific?**

```bash
# Search all docs
grep -r "search term" .claude/skills/shopify/docs/

# Find specific topics
ls .claude/skills/shopify/docs/shopify/

# Read specific guide
cat .claude/skills/shopify/docs/shopify/webhooks.md
```

**Common doc files:**
- `api-admin-graphql.md` - GraphQL Admin API
- `api-storefront.md` - Storefront API
- `authentication.md` - OAuth and auth flows
- `webhooks.md` - Webhook handling
- `apps.md` - App development
- `themes.md` - Theme development
- `liquid.md` - Liquid reference
- `hydrogen.md` - Headless commerce
- `checkout.md` - Checkout customization
- `functions.md` - Shopify Functions
- `cli.md` - CLI commands
