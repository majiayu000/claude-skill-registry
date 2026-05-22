---
name: shopify-remix-template
description: Guide for developing Shopify apps using the official Shopify Remix Template. Covers structure, authentication, API usage, and deployment.
---

# Shopify Remix Template Guide

This skill provides a guide for building Shopify apps using the official **Shopify Remix App Template**. This template is the recommended starting point for most new Shopify embedded apps (though React Router is the future direction, Remix is still widely used and supported).

## 🚀 Getting Started

To create a new app using the Remix template, run:

```bash
git clone https://github.com/Shopify/shopify-app-template-remix.git
```

## 📂 Project Structure

A typical Remix app structure:

*   `app/`
    *   `routes/`: File-system based routing.
        *   `app._index.tsx`: The main dashboard page.
        *   `app.tsx`: The root layout for the authenticated app.
        *   `webhooks.tsx`: Webhook handler.
    *   `shopify.server.ts`: **Critical**. Initializes the Shopify API client, authentication, and session storage (Redis).
    *   `db.server.ts`: Database connection (Mongoose).
    *   `models/`: Mongoose models (e.g., `Session.ts`, `Shop.ts`).
    *   `root.tsx`: The root component for the entire application.
*   `shopify.app.toml`: Main app configuration file.

## 🔐 Authentication & Sessions

The template uses `@shopify/shopify-app-remix` to handle authentication automatically.

### `shopify.server.ts`
This file exports an `authenticate` object used in loaders and actions. It is configured to use **Redis** for session storage.

```typescript
import { shopifyApp } from "@shopify/shopify-app-remix/server";
import { RedisSessionStorage } from "@shopify/shopify-app-session-storage-redis";

const sessionDb = new RedisSessionStorage(
  new URL(process.env.REDIS_URL!)
);

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  appUrl: process.env.SHOPIFY_APP_URL,
  scopes: process.env.SCOPES?.split(","),
  apiVersion: "2025-10",
  sessionStorage: sessionDb,
  isEmbeddedApp: true,
});

export const authenticate = shopify.authenticate;
export const apiVersion = "2025-10";
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
```

### Usage in Loaders (Data Fetching)
Protect routes and get the session context:

```typescript
import { json } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }) => {
  const { admin, session } = await authenticate.admin(request);
  
  // Use admin API
  const response = await admin.graphql(`...`);
  
  return json({ data: response });
};
```

## 📡 Webhooks

Webhooks are handled in `app/routes/webhooks.tsx` (or individual route files). The template automatically registers webhooks defined in `shopify.server.ts`.

To add a webhook:
1.  Add configuration in `shopify.server.ts`.
2.  Handle the topic in the `action` of `app/routes/webhooks.tsx`.

## 🗄️ Database (Mongoose/MongoDB)

Use **Mongoose** for persistent data storage (Shops, Settings, etc.).

### `app/db.server.ts`
Singleton connection to MongoDB.

```typescript
import mongoose from "mongoose";

let isConnected = false;

export const connectDb = async () => {
  if (isConnected) return;

  try {
    await mongoose.connect(process.env.MONGODB_URI!);
    isConnected = true;
    console.log("🚀 Connected to MongoDB");
  } catch (error) {
    console.error("❌ MongoDB connection error:", error);
  }
};
```

### `app/models/Shop.ts` (Example)

```typescript
import mongoose from "mongoose";

const ShopSchema = new mongoose.Schema({
  shop: { type: String, required: true, unique: true },
  accessToken: { type: String, required: true },
  isInstalled: { type: Boolean, default: true },
});

export const Shop = mongoose.models.Shop || mongoose.model("Shop", ShopSchema);
```

### Usage in Loaders
Connect to the DB before using models.

```typescript
import { connectDb } from "../db.server";
import { Shop } from "../models/Shop";

export const loader = async ({ request }) => {
  await connectDb();
  // ...
  const shopData = await Shop.findOne({ shop: session.shop });
  // ...
};
```

## 🎨 UI & Design (Polaris)

The template comes pre-configured with **Polaris**, Shopify's design system.
*   Wrap your pages in `<Page>` components.
*   Use `<Layout>`, `<Card>`, and other Polaris components for a native feel. 
*   App Bridge is initialized automatically in `app.tsx`.

## 🛠️ Common Tasks

### 1. Adding a Navigation Item
Update `app/routes/app.tsx`:
```typescript
<ui-nav-menu>
  <Link to="/app">Home</Link>
  <Link to="/app/settings">Settings</Link>
</ui-nav-menu>
```

### 2. Fetching Data from Shopify
Use the `admin` object from `authenticate.admin(request)` to make GraphQL calls.

### 3. Deploying
*   **Hosting:** Remix apps can be hosted on Vercel, Fly.io, Heroku, or Cloudflare.
*   **Database:** Ensure you have a persistent database (e.g., Postgres) for production.
*   **Environment Variables:** Set `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, `SCOPES`, `SHOPIFY_APP_URL`.

## 📚 References

*   [Shopify Remix App Template (GitHub)](https://github.com/Shopify/shopify-app-template-remix)
*   [@shopify/shopify-app-remix package](https://www.npmjs.com/package/@shopify/shopify-app-remix)
*   [Remix Documentation](https://remix.run/docs/en/main)
