---
name: scaffolding-marketplace-integrations
description: Generates boilerplate for e-commerce API integrations. Use when the user asks about WooCommerce, Shopify, Bol.com, or Etsy APIs, webhooks, product sync, or order handling.
---

# Marketplace Integration Helper

## When to use this skill

- User asks to integrate with WooCommerce or Shopify
- User needs webhook handlers for orders or products
- User mentions Bol.com, Etsy, or marketplace APIs
- User wants rate-limited API clients
- User asks about product synchronization

## Workflow

- [ ] Identify target marketplace(s)
- [ ] Generate API client with auth
- [ ] Add rate limiting and retry logic
- [ ] Create webhook handlers
- [ ] Add TypeScript types
- [ ] Implement error recovery

## Instructions

### Step 1: Identify Marketplace

| Platform    | Auth Type                    | Rate Limit           | Docs         |
| ----------- | ---------------------------- | -------------------- | ------------ |
| Shopify     | OAuth / Access Token         | 2 req/sec (burst 40) | Admin API    |
| WooCommerce | OAuth 1.0 / API Keys         | 25 req/sec           | REST API v3  |
| Bol.com     | OAuth 2.0 Client Credentials | 25 req/10sec         | Retailer API |
| Etsy        | OAuth 2.0 PKCE               | 10 req/sec           | Open API v3  |

### Step 2: Base API Client Structure

```typescript
// lib/marketplace/base-client.ts
interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
}

export abstract class BaseMarketplaceClient {
  protected baseUrl: string;
  protected rateLimitConfig: RateLimitConfig;
  protected retryConfig: RetryConfig;
  private requestQueue: Array<() => Promise<unknown>> = [];
  private processing = false;

  constructor(
    baseUrl: string,
    rateLimit: RateLimitConfig,
    retry: RetryConfig = {
      maxRetries: 3,
      baseDelayMs: 1000,
      maxDelayMs: 10000,
    },
  ) {
    this.baseUrl = baseUrl;
    this.rateLimitConfig = rateLimit;
    this.retryConfig = retry;
  }

  protected abstract getAuthHeaders(): Record<string, string>;

  protected async request<T>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    return this.enqueue(() => this.executeWithRetry<T>(method, path, body));
  }

  private async executeWithRetry<T>(
    method: string,
    path: string,
    body?: unknown,
    attempt = 0,
  ): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        method,
        headers: {
          "Content-Type": "application/json",
          ...this.getAuthHeaders(),
        },
        body: body ? JSON.stringify(body) : undefined,
      });

      if (response.status === 429) {
        const retryAfter = parseInt(response.headers.get("Retry-After") || "5");
        await this.delay(retryAfter * 1000);
        return this.executeWithRetry(method, path, body, attempt);
      }

      if (!response.ok) {
        throw new MarketplaceError(response.status, await response.text());
      }

      return response.json();
    } catch (error) {
      if (attempt < this.retryConfig.maxRetries && this.isRetryable(error)) {
        const delay = Math.min(
          this.retryConfig.baseDelayMs * Math.pow(2, attempt),
          this.retryConfig.maxDelayMs,
        );
        await this.delay(delay);
        return this.executeWithRetry(method, path, body, attempt + 1);
      }
      throw error;
    }
  }

  private isRetryable(error: unknown): boolean {
    if (error instanceof MarketplaceError) {
      return [408, 429, 500, 502, 503, 504].includes(error.status);
    }
    return error instanceof TypeError; // Network errors
  }

  private enqueue<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.requestQueue.push(async () => {
        try {
          resolve(await fn());
        } catch (e) {
          reject(e);
        }
      });
      this.processQueue();
    });
  }

  private async processQueue(): Promise<void> {
    if (this.processing) return;
    this.processing = true;

    while (this.requestQueue.length > 0) {
      const batch = this.requestQueue.splice(
        0,
        this.rateLimitConfig.maxRequests,
      );
      await Promise.all(batch.map((fn) => fn()));
      if (this.requestQueue.length > 0) {
        await this.delay(this.rateLimitConfig.windowMs);
      }
    }

    this.processing = false;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

export class MarketplaceError extends Error {
  constructor(
    public status: number,
    public body: string,
  ) {
    super(`Marketplace API error ${status}: ${body}`);
  }
}
```

### Step 3: Platform-Specific Clients

**Shopify Client:**

```typescript
// lib/marketplace/shopify-client.ts
import { BaseMarketplaceClient } from "./base-client";

interface ShopifyProduct {
  id: number;
  title: string;
  body_html: string;
  vendor: string;
  product_type: string;
  variants: ShopifyVariant[];
  images: ShopifyImage[];
  status: "active" | "archived" | "draft";
}

interface ShopifyVariant {
  id: number;
  product_id: number;
  title: string;
  price: string;
  sku: string;
  inventory_quantity: number;
}

interface ShopifyImage {
  id: number;
  src: string;
  alt: string | null;
}

interface ShopifyOrder {
  id: number;
  order_number: number;
  email: string;
  financial_status: string;
  fulfillment_status: string | null;
  line_items: ShopifyLineItem[];
  total_price: string;
  currency: string;
}

interface ShopifyLineItem {
  id: number;
  product_id: number;
  variant_id: number;
  quantity: number;
  price: string;
}

export class ShopifyClient extends BaseMarketplaceClient {
  private accessToken: string;

  constructor(shop: string, accessToken: string) {
    super(`https://${shop}.myshopify.com/admin/api/2024-01`, {
      maxRequests: 2,
      windowMs: 1000,
    });
    this.accessToken = accessToken;
  }

  protected getAuthHeaders(): Record<string, string> {
    return { "X-Shopify-Access-Token": this.accessToken };
  }

  // Products
  async getProducts(limit = 50): Promise<ShopifyProduct[]> {
    const data = await this.request<{ products: ShopifyProduct[] }>(
      "GET",
      `/products.json?limit=${limit}`,
    );
    return data.products;
  }

  async getProduct(id: number): Promise<ShopifyProduct> {
    const data = await this.request<{ product: ShopifyProduct }>(
      "GET",
      `/products/${id}.json`,
    );
    return data.product;
  }

  async createProduct(
    product: Partial<ShopifyProduct>,
  ): Promise<ShopifyProduct> {
    const data = await this.request<{ product: ShopifyProduct }>(
      "POST",
      "/products.json",
      { product },
    );
    return data.product;
  }

  async updateProduct(
    id: number,
    product: Partial<ShopifyProduct>,
  ): Promise<ShopifyProduct> {
    const data = await this.request<{ product: ShopifyProduct }>(
      "PUT",
      `/products/${id}.json`,
      { product },
    );
    return data.product;
  }

  // Inventory
  async updateInventory(
    inventoryItemId: number,
    locationId: number,
    quantity: number,
  ): Promise<void> {
    await this.request("POST", "/inventory_levels/set.json", {
      inventory_item_id: inventoryItemId,
      location_id: locationId,
      available: quantity,
    });
  }

  // Orders
  async getOrders(status = "any", limit = 50): Promise<ShopifyOrder[]> {
    const data = await this.request<{ orders: ShopifyOrder[] }>(
      "GET",
      `/orders.json?status=${status}&limit=${limit}`,
    );
    return data.orders;
  }

  async fulfillOrder(orderId: number, trackingNumber?: string): Promise<void> {
    await this.request("POST", `/orders/${orderId}/fulfillments.json`, {
      fulfillment: {
        tracking_number: trackingNumber,
        notify_customer: true,
      },
    });
  }
}
```

**WooCommerce Client:**

```typescript
// lib/marketplace/woocommerce-client.ts
import { BaseMarketplaceClient } from "./base-client";
import crypto from "crypto";

interface WooProduct {
  id: number;
  name: string;
  slug: string;
  type: "simple" | "variable" | "grouped";
  status: "publish" | "draft" | "pending";
  sku: string;
  price: string;
  regular_price: string;
  stock_quantity: number | null;
  images: { id: number; src: string; alt: string }[];
}

interface WooOrder {
  id: number;
  status: string;
  currency: string;
  total: string;
  billing: WooAddress;
  shipping: WooAddress;
  line_items: WooLineItem[];
}

interface WooAddress {
  first_name: string;
  last_name: string;
  address_1: string;
  city: string;
  postcode: string;
  country: string;
}

interface WooLineItem {
  id: number;
  product_id: number;
  quantity: number;
  total: string;
}

export class WooCommerceClient extends BaseMarketplaceClient {
  private consumerKey: string;
  private consumerSecret: string;

  constructor(siteUrl: string, consumerKey: string, consumerSecret: string) {
    super(`${siteUrl}/wp-json/wc/v3`, { maxRequests: 25, windowMs: 1000 });
    this.consumerKey = consumerKey;
    this.consumerSecret = consumerSecret;
  }

  protected getAuthHeaders(): Record<string, string> {
    const auth = Buffer.from(
      `${this.consumerKey}:${this.consumerSecret}`,
    ).toString("base64");
    return { Authorization: `Basic ${auth}` };
  }

  // Products
  async getProducts(page = 1, perPage = 100): Promise<WooProduct[]> {
    return this.request("GET", `/products?page=${page}&per_page=${perPage}`);
  }

  async getProduct(id: number): Promise<WooProduct> {
    return this.request("GET", `/products/${id}`);
  }

  async createProduct(product: Partial<WooProduct>): Promise<WooProduct> {
    return this.request("POST", "/products", product);
  }

  async updateProduct(
    id: number,
    product: Partial<WooProduct>,
  ): Promise<WooProduct> {
    return this.request("PUT", `/products/${id}`, product);
  }

  async updateStock(productId: number, quantity: number): Promise<WooProduct> {
    return this.updateProduct(productId, { stock_quantity: quantity });
  }

  // Orders
  async getOrders(status?: string, page = 1): Promise<WooOrder[]> {
    const query = status ? `&status=${status}` : "";
    return this.request("GET", `/orders?page=${page}${query}`);
  }

  async updateOrderStatus(orderId: number, status: string): Promise<WooOrder> {
    return this.request("PUT", `/orders/${orderId}`, { status });
  }
}
```

See [examples/bol-etsy-clients.md](examples/bol-etsy-clients.md) for Bol.com and Etsy implementations.

### Step 4: Webhook Handlers

**Webhook verification and routing:**

```typescript
// lib/marketplace/webhooks.ts
import crypto from "crypto";

interface WebhookHandler<T = unknown> {
  topic: string;
  handler: (payload: T) => Promise<void>;
}

// Shopify webhook verification
export function verifyShopifyWebhook(
  body: string,
  hmacHeader: string,
  secret: string,
): boolean {
  const hash = crypto
    .createHmac("sha256", secret)
    .update(body, "utf8")
    .digest("base64");
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(hmacHeader));
}

// WooCommerce webhook verification
export function verifyWooCommerceWebhook(
  body: string,
  signature: string,
  secret: string,
): boolean {
  const hash = crypto
    .createHmac("sha256", secret)
    .update(body, "utf8")
    .digest("base64");
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(signature));
}

// Generic webhook router
export class WebhookRouter {
  private handlers: Map<string, WebhookHandler["handler"]> = new Map();

  register<T>(topic: string, handler: (payload: T) => Promise<void>): void {
    this.handlers.set(topic, handler as WebhookHandler["handler"]);
  }

  async route(topic: string, payload: unknown): Promise<void> {
    const handler = this.handlers.get(topic);
    if (!handler) {
      console.warn(`No handler registered for topic: ${topic}`);
      return;
    }
    await handler(payload);
  }
}
```

**Next.js API route example:**

```typescript
// app/api/webhooks/shopify/route.ts
import { NextRequest, NextResponse } from "next/server";
import {
  verifyShopifyWebhook,
  WebhookRouter,
} from "@/lib/marketplace/webhooks";
import {
  handleOrderCreated,
  handleProductUpdated,
} from "@/lib/marketplace/handlers";

const router = new WebhookRouter();
router.register("orders/create", handleOrderCreated);
router.register("products/update", handleProductUpdated);

export async function POST(request: NextRequest) {
  const body = await request.text();
  const hmac = request.headers.get("X-Shopify-Hmac-Sha256") || "";
  const topic = request.headers.get("X-Shopify-Topic") || "";

  if (!verifyShopifyWebhook(body, hmac, process.env.SHOPIFY_WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: "Invalid signature" }, { status: 401 });
  }

  try {
    await router.route(topic, JSON.parse(body));
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Webhook processing error:", error);
    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }
}
```

**Webhook handler implementations:**

```typescript
// lib/marketplace/handlers.ts
import { db } from "@/lib/db";

interface ShopifyOrderPayload {
  id: number;
  order_number: number;
  email: string;
  line_items: Array<{
    product_id: number;
    variant_id: number;
    quantity: number;
  }>;
}

export async function handleOrderCreated(
  payload: ShopifyOrderPayload,
): Promise<void> {
  // Idempotency check
  const existing = await db.order.findUnique({
    where: { externalId: `shopify_${payload.id}` },
  });
  if (existing) return;

  // Create local order record
  await db.order.create({
    data: {
      externalId: `shopify_${payload.id}`,
      platform: "shopify",
      orderNumber: String(payload.order_number),
      customerEmail: payload.email,
      status: "pending",
      lineItems: {
        create: payload.line_items.map((item) => ({
          externalProductId: String(item.product_id),
          externalVariantId: String(item.variant_id),
          quantity: item.quantity,
        })),
      },
    },
  });

  // Sync inventory across platforms
  for (const item of payload.line_items) {
    await syncInventoryAcrossPlatforms(item.product_id, -item.quantity);
  }
}

export async function handleProductUpdated(payload: {
  id: number;
  title: string;
}): Promise<void> {
  await db.product.updateMany({
    where: { externalId: `shopify_${payload.id}` },
    data: { title: payload.title, updatedAt: new Date() },
  });
}
```

### Step 5: Product Sync Service

```typescript
// lib/marketplace/sync-service.ts
import { ShopifyClient } from "./shopify-client";
import { WooCommerceClient } from "./woocommerce-client";

interface NormalizedProduct {
  sku: string;
  title: string;
  description: string;
  price: number;
  quantity: number;
  images: string[];
}

export class ProductSyncService {
  constructor(
    private shopify: ShopifyClient,
    private woocommerce: WooCommerceClient,
  ) {}

  async syncProductToAll(product: NormalizedProduct): Promise<void> {
    const results = await Promise.allSettled([
      this.syncToShopify(product),
      this.syncToWooCommerce(product),
    ]);

    for (const result of results) {
      if (result.status === "rejected") {
        console.error("Sync failed:", result.reason);
      }
    }
  }

  private async syncToShopify(product: NormalizedProduct): Promise<void> {
    const existing = await this.findShopifyProductBySku(product.sku);

    if (existing) {
      await this.shopify.updateProduct(existing.id, {
        title: product.title,
        body_html: product.description,
        variants: [{ ...existing.variants[0], price: String(product.price) }],
      });
    } else {
      await this.shopify.createProduct({
        title: product.title,
        body_html: product.description,
        variants: [{ sku: product.sku, price: String(product.price) }] as any,
        images: product.images.map((src) => ({ src })) as any,
      });
    }
  }

  private async syncToWooCommerce(product: NormalizedProduct): Promise<void> {
    // Similar pattern for WooCommerce
  }

  private async findShopifyProductBySku(sku: string) {
    const products = await this.shopify.getProducts(250);
    return products.find((p) => p.variants.some((v) => v.sku === sku));
  }
}
```

## Environment Setup

```bash
# .env.local
SHOPIFY_SHOP=your-store
SHOPIFY_ACCESS_TOKEN=shpat_xxxxx
SHOPIFY_WEBHOOK_SECRET=xxxxx

WOOCOMMERCE_URL=https://your-store.com
WOOCOMMERCE_KEY=ck_xxxxx
WOOCOMMERCE_SECRET=cs_xxxxx

BOL_CLIENT_ID=xxxxx
BOL_CLIENT_SECRET=xxxxx

ETSY_API_KEY=xxxxx
ETSY_SHARED_SECRET=xxxxx
```

## Validation

Before completing:

- [ ] API client handles rate limits correctly
- [ ] Webhook signatures verified before processing
- [ ] Idempotency checks prevent duplicate processing
- [ ] Error recovery with exponential backoff works
- [ ] TypeScript types match API responses

## Error Handling

- **Rate limit exceeded**: Queue requests and respect Retry-After header.
- **Authentication failure**: Check token expiry; refresh OAuth tokens if needed.
- **Webhook signature mismatch**: Reject immediately; log for investigation.
- **Partial sync failure**: Use Promise.allSettled; continue with working platforms.
- **Network timeout**: Retry with exponential backoff up to max retries.

## Resources

- [Shopify Admin API](https://shopify.dev/docs/api/admin-rest)
- [WooCommerce REST API](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [Bol.com Retailer API](https://api.bol.com/retailer/public/Retailer-API/v10/introduction.html)
- [Etsy Open API v3](https://developers.etsy.com/documentation/)
