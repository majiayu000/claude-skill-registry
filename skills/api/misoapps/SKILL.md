---
name: misoapps
description: Guide for using Miso Apps SDKs (@misoapps/mail-sdk and @misoapps/shop-sdk) in Shopify apps. Use this skill when the user needs to send emails via SMTP or AWS SES, manage SMTP configurations, retrieve email logs, manage shop installations, or access shop/app data through Miso Apps services.
---

# Miso Apps SDK

SDKs for email services and shop management in Shopify applications.

## Installation

```bash
npm install @misoapps/mail-sdk @misoapps/shop-sdk
```

## Mail SDK (`@misoapps/mail-sdk`)

### Setup

```typescript
import { createMailClient } from '@misoapps/mail-sdk';

const mailClient = createMailClient({
  endpoint: 'https://mail-service.example.com',
  shopDomain: 'my-shop.myshopify.com', // Required for User SMTP APIs
});
```

### Send Email (User SMTP)

```typescript
const result = await mailClient.sendEmail({
  to: 'customer@example.com',
  fromEmail: 'shop@example.com',
  fromName: 'My Shop',        // optional
  replyTo: ['support@example.com'], // optional
  subject: 'Hello!',
  html: '<h1>Welcome!</h1>',
  text: 'Welcome!',           // optional
});
// { success: true, messageId: '...', logId: '...' }
```

### Send Email (System SMTP - AWS SES)

`fromEmail` is fixed from server's `AWS_SMTP_FROM_EMAIL` env:

```typescript
const result = await mailClient.sendSystemEmail({
  to: 'customer@example.com',
  fromName: 'Miso Apps',      // optional
  replyTo: ['support@example.com'], // optional
  subject: 'Hello!',
  html: '<h1>Welcome!</h1>',
  text: 'Welcome!',           // optional
});
```

### Get Email Logs

```typescript
const logs = await mailClient.getEmailLogs({
  status: 'sent',   // optional: 'pending' | 'sent' | 'failed'
  type: 'user',     // optional: 'user' | 'system'
  page: 1,          // optional
  limit: 20,        // optional
});
// { logs: [...], total: 100, page: 1, pages: 5 }
```

### SMTP Configuration

```typescript
// Create/Update (upsert)
const config = await mailClient.upsertSmtpConfig({
  host: 'smtp.gmail.com',
  port: 587,        // optional, default: 587
  secure: false,    // optional, default: false
  username: 'user@gmail.com',
  password: 'app-password',
});

// Get
const config = await mailClient.getSmtpConfig(); // SmtpConfig | null

// Update (partial)
await mailClient.updateSmtpConfig({
  port: 465,
  secure: true,
  isActive: true,
});

// Delete
await mailClient.deleteSmtpConfig();
// { success: true, message: '...' }

// Test connection
const result = await mailClient.testSmtpConnection();
// { success: true, message: 'SMTP connection successful' }
// or { success: false, message: '...', error: '...' }
```

### Mail SDK Types

```typescript
import type {
  MailClientConfig, MailClient,
  SendEmailRequest, SendSystemEmailRequest, SendEmailResponse,
  EmailLog, GetEmailLogsParams, GetEmailLogsResponse,
  EmailStatus, EmailType,
  SmtpConfig, CreateSmtpConfigRequest, UpdateSmtpConfigRequest, TestSmtpResponse,
} from '@misoapps/mail-sdk';
```

## Shop SDK (`@misoapps/shop-sdk`)

### Setup

```typescript
import { createShopServices, Platform, AppID } from '@misoapps/shop-sdk';

const shopService = createShopServices(
  'http://localhost:5000',
  'shopify'  // Platform: 'shopify' | 'shopline'
);
```

### Install App

```typescript
const result = await shopService.installApp({
  shop: 'example.myshopify.com',
  shopName: 'Example Shop',
  contactEmail: 'contact@example.com',
  themeId: 'theme-123',       // optional
  app: {
    appId: 'llmstxt',         // AppID
    plan: 'basic',
    accessToken: 'token',     // optional
  },
});
// { message: 'App installed successfully', status: 'NEW' | 'INSTALLED' | 'REINSTALLED', shop: IShop }
```

### Uninstall App

```typescript
const result = await shopService.uninstallApp({
  shop: 'example.myshopify.com',
  appId: 'llmstxt',
});
// { message: 'App uninstalled successfully', shop: IShop }
```

### Get App

```typescript
const { shop, app } = await shopService.getApp('example.myshopify.com', 'llmstxt');
// shop: IShop (without apps array), app: IAppInfo
```

### Update App

```typescript
const { shop, app } = await shopService.updateApp(
  'example.myshopify.com',
  'llmstxt',
  {
    plan: 'premium',          // optional
    isReviewed: true,         // optional
    accessToken: 'new-token', // optional
  }
);
```

### Shop Queries

```typescript
// Get single shop
const { shop } = await shopService.getShop('example.myshopify.com');

// Get shop's apps
const { apps } = await shopService.getShopApps('example.myshopify.com');

// List shops (paginated)
const { shops, total, page, pages } = await shopService.listShops({
  page: 1,          // default: 1
  limit: 10,        // default: 10
  platform: 'shopify', // optional filter
});

// Find recently uninstalled (last 10 days)
const { shops } = await shopService.findUninstalledShops('llmstxt');

// Get stats
const stats = await shopService.getStats();
// { totalShops, totalInstalls, activeInstalls }
```

### Shop SDK Types

```typescript
import type {
  Platform, AppID, Shop, AppInfo,
  InstallAppPayload, InstallAppResponse,
  UninstallAppPayload, UninstallAppResponse,
  UpdateAppPayload, UpdateAppResponse,
  GetAppResponse, GetShopResponse, GetShopAppsResponse,
  ListShopsResponse, FindUninstalledShopsResponse, GetStatsResponse,
} from '@misoapps/shop-sdk';
```

## Environment Variables

```env
MAIL_SERVICE_ENDPOINT=https://mail-api.misoapps.com
SHOP_SERVICE_ENDPOINT=https://shop-api.misoapps.com
```

## Integration with Remix

See `references/remix-integration.md` for Remix loader/action patterns.
