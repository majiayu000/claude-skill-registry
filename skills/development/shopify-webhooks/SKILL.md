---
name: shopify-webhooks
description: Guide for handling Shopify Webhooks, including configuration, verification, and processing. Use this skill when the user needs to set up webhook subscriptions, verify authentic requests, or handle event payloads.
---

# Shopify Webhooks Skill

Webhooks are the preferred way to stay in sync with Shopify data. They allow your app to receive real-time notifications when events occur in a shop (e.g., `orders/create`, `app/uninstalled`).

## 1. Verification (CRITICAL)

**ALL** webhook requests must be verified to ensure they came from Shopify.

### HMAC Verification

Shopify includes an `X-Shopify-Hmac-Sha256` header in every webhook request. This is a base64-encoded HMAC-SHA256 digest of the request body, using your **Client Secret** (API Secret Key) as the signing key.

> [!IMPORTANT]
> Always use the **raw request body** (Buffer) for verification. Parsed JSON bodies may have subtle differences that cause verification to fail.

#### Node.js Example (Generic)

```javascript
const crypto = require('crypto');

function verifyWebhook(rawBody, hmacHeader, apiSecret) {
  const digest = crypto
    .createHmac('sha256', apiSecret)
    .update(rawBody, 'utf8')
    .digest('base64');

  return crypto.timingSafeEqual(
    Buffer.from(digest),
    Buffer.from(hmacHeader)
  );
}
```

#### Remix / Shopify App Template (Recommended)

If using `@shopify/shopify-app-remix`, verification is handled automatically by the `authenticate.webhook` helper.

```typescript
/* app/routes/webhooks.tsx */
import { authenticate } from "../shopify.server";

export const action = async ({ request }) => {
  const { topic, shop, session, admin, payload } = await authenticate.webhook(request);

  if (!admin) {
    // The webhook request was not valid.
    return new Response();
  }

  switch (topic) {
    case "APP_UNINSTALLED":
      if (session) {
        await db.session.deleteMany({ where: { shop } });
      }
      break;
    case "ORDERS_CREATE":
      console.log(`Order created: ${payload.id}`);
      break;
  }

  return new Response();
};
```

## 2. Registration

### App-specific Webhooks (Recommended)
These are configured in `shopify.app.toml`. They are automatically registered when the app is deployed and are easier to manage. Best for topics that apply to the app in general (e.g., `app/uninstalled`).

```toml
[webhooks]
api_version = "2025-10"

  [[webhooks.subscriptions]]
  topics = [ "app/uninstalled", "orders/create" ]
  uri = "/webhooks"
```

### Shop-specific Webhooks (Advanced)
Use `webhookSubscriptionCreate` via the Admin API. Best for:
- Per-shop customization.
- Topics not supported by config.
- Dynamic runtime registration.

```graphql
mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
    userErrors {
      field
      message
    }
    webhookSubscription {
      id
    }
  }
}
```

## 3. Mandatory Compliance (GDPR)

Public apps **MUST** implement specific webhooks to comply with privacy laws. These are configured in the **Partner Dashboard** (App > Configuration > Privacy compliance), NOT in `shopify.app.toml` or via API.

-   `customers/data_request`: Request to export customer data.
-   `customers/redact`: Request to delete customer data.
-   `shop/redact`: Request to delete shop data (48 hours after uninstall).

> [!WARNING]
> Failure to handle these can result in app removal.

## 4. Best Practices

-   **Idempotency**: Webhooks can be delivered multiple times. Ensure your processing logic is idempotent (e.g., check if an order has already been processed before taking action).
-   **Response Time**: Respond with a `200 OK` **immediately** (within 5 seconds). Perform long-running tasks asynchronously (e.g., using a background queue).
-   **App Uninstalled**: ALWAYS handle `app/uninstalled` to clean up shop data and cancel subscriptions. This webhook acts as the "offboarding" signal.
-   **App Uninstalled**: ALWAYS handle `app/uninstalled` to clean up shop data and cancel subscriptions. This webhook acts as the "offboarding" signal.

## Common Topics

-   `APP_UNINSTALLED`: App removed. Cleanup required.
-   `ORDERS_CREATE`: New order placed.
-   `ORDERS_PAID`: Order payment status changed to paid.
-   `PRODUCTS_UPDATE`: Product details changed.
