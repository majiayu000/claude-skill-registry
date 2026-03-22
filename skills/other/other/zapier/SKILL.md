---
name: zapier
description: >-
  Automate workflows between apps with Zapier. Use when a user asks to connect
  apps without code, automate repetitive tasks, sync data between services, or
  build no-code integrations between SaaS tools.
license: Apache-2.0
compatibility: '6000+ app integrations (cloud service)'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: automation
  tags:
    - zapier
    - automation
    - integration
    - no-code
    - workflow
---

# Zapier

## Overview

Zapier connects 6000+ apps with automated workflows (Zaps). Trigger → Action chains: when something happens in one app, do something in another. No code required for basic automation; supports code steps for complex logic.

## Instructions

### Step 1: Common Zap Patterns

```text
Trigger → Action examples:
1. New Stripe payment → Add row to Google Sheets → Send Slack notification
2. New form submission (Typeform) → Create contact in HubSpot → Send welcome email
3. New GitHub issue → Create Trello card → Notify on Discord
4. New email (Gmail) with attachment → Save to Google Drive → Notify on Slack
5. Scheduled (every day 9 AM) → Pull data from API → Post summary to Slack
```

### Step 2: Webhooks (Custom Triggers)

```typescript
// Trigger a Zap from your app via webhook
await fetch('https://hooks.zapier.com/hooks/catch/123456/abcdef/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    event: 'order_completed',
    customer_email: 'john@example.com',
    order_total: 99.99,
    product: 'Premium Plan',
  }),
})
// Zapier receives this and runs the connected workflow
```

### Step 3: Code Steps (JavaScript)

```javascript
// Zapier Code step — transform data between apps
const inputData = inputData    // data from previous step

// Parse and transform
const fullName = `${inputData.firstName} ${inputData.lastName}`
const isVIP = parseFloat(inputData.totalSpent) > 1000

output = [{
  fullName,
  email: inputData.email.toLowerCase(),
  isVIP,
  segment: isVIP ? 'vip' : 'regular',
}]
```

### Step 4: Build a Zapier Integration

```typescript
// If you want YOUR app to appear in Zapier's directory
// Use Zapier Platform CLI to build a custom integration

// index.ts — Define triggers and actions for your app
const App = {
  triggers: {
    newOrder: {
      display: { label: 'New Order', description: 'Triggers when a new order is created' },
      operation: {
        perform: async (z, bundle) => {
          const response = await z.request('https://api.myapp.com/orders?since=' + bundle.meta.page)
          return response.data
        },
      },
    },
  },
  actions: {
    createContact: {
      display: { label: 'Create Contact' },
      operation: {
        perform: async (z, bundle) => {
          return z.request({
            method: 'POST',
            url: 'https://api.myapp.com/contacts',
            body: { email: bundle.inputData.email, name: bundle.inputData.name },
          })
        },
      },
    },
  },
}
```

## Guidelines

- Free tier: 100 tasks/month, 5 Zaps. Starter ($19.99/mo): 750 tasks, 20 Zaps.
- "Tasks" = each action step that runs. A 5-step Zap uses 5 tasks per trigger.
- For self-hosted alternative, use n8n (free, unlimited) or Activepieces.
- Use Paths (branching) for conditional logic — different actions based on data.
