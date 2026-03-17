---
name: stagehand-automation
description: AI-powered browser automation using Stagehand v3 and Claude. Use when building self-healing tests, AI agents, dynamic web automation, or when traditional selectors break frequently due to UI changes.
---

# Stagehand Automation

## Overview

Stagehand v3 is the state-of-the-art AI browser automation framework that bridges brittle traditional automation with intelligent, self-healing capabilities. Built on Chrome DevTools Protocol (CDP), it's 44% faster than v2 and integrates seamlessly with Claude.

**Key Innovation**: When DOM changes, AI adapts instead of tests breaking.

**Core APIs**:
- `act()` - Perform actions using natural language
- `extract()` - Extract structured data from pages
- `observe()` - Identify elements and page state

---

## Quick Start (10 Minutes)

### 1. Install Stagehand

```bash
npm install @browserbase/stagehand zod
```

### 2. Configure Claude API

```bash
# Add to .env
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Write First Automation

```typescript
import { Stagehand } from "@browserbase/stagehand";
import { z } from "zod";

async function main() {
  const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "claude-sonnet-4-20250514",
    modelClientOptions: {
      apiKey: process.env.ANTHROPIC_API_KEY,
    },
  });

  await stagehand.init();
  await stagehand.page.goto("https://news.ycombinator.com");

  // AI-powered action - survives UI changes!
  await stagehand.act({ action: "click on the first story link" });

  // Extract structured data
  const data = await stagehand.extract({
    instruction: "extract the story title and author",
    schema: z.object({
      title: z.string(),
      author: z.string(),
    }),
  });

  console.log(data);
  await stagehand.close();
}

main();
```

### 4. Run

```bash
npx ts-node your-script.ts
```

---

## Core APIs

### act() - Perform Actions

Execute actions using natural language:

```typescript
// Click elements
await stagehand.act({ action: "click the login button" });

// Fill forms
await stagehand.act({ action: "fill in the email field with 'test@example.com'" });
await stagehand.act({ action: "enter password 'securepass123'" });

// Navigate
await stagehand.act({ action: "scroll down to the pricing section" });
await stagehand.act({ action: "click the 'Sign Up' button in the header" });

// Complex actions
await stagehand.act({
  action: "select 'Premium' from the plan dropdown and click Continue"
});
```

**Self-Healing**: If the button ID changes from `#login-btn` to `#auth-signin`, Stagehand adapts automatically.

### extract() - Get Structured Data

Extract data with schema validation:

```typescript
import { z } from "zod";

// Simple extraction
const title = await stagehand.extract({
  instruction: "get the main page title",
  schema: z.object({
    title: z.string(),
  }),
});

// Complex extraction
const products = await stagehand.extract({
  instruction: "extract all products with name, price, and availability",
  schema: z.object({
    products: z.array(z.object({
      name: z.string(),
      price: z.number(),
      inStock: z.boolean(),
    })),
  }),
});

// Extract from specific area
const cartItems = await stagehand.extract({
  instruction: "get items in the shopping cart",
  schema: z.object({
    items: z.array(z.object({
      name: z.string(),
      quantity: z.number(),
      price: z.number(),
    })),
    total: z.number(),
  }),
});
```

### observe() - Analyze Page State

Understand page elements and state:

```typescript
// Find elements
const elements = await stagehand.observe({
  instruction: "find all clickable buttons on this page"
});

// Check state
const loginState = await stagehand.observe({
  instruction: "is the user logged in? Look for profile icons or logout buttons"
});

// Identify form fields
const formFields = await stagehand.observe({
  instruction: "identify all form input fields and their labels"
});
```

---

## Self-Healing Patterns

### Traditional vs Stagehand

```typescript
// TRADITIONAL (Playwright) - Breaks when DOM changes
await page.click('#submit-btn-v2');  // Fails if ID changes
await page.click('.btn-primary:nth-child(2)');  // Fails if order changes

// STAGEHAND - Self-healing
await stagehand.act({ action: "click the submit button" });  // Always works
await stagehand.act({ action: "click the primary action button" });  // Adapts
```

### When Self-Healing Activates

1. **ID/Class Changes**: Button ID changes from `#old-id` to `#new-id`
2. **Structure Changes**: Element moves in DOM tree
3. **Text Changes**: Button text changes from "Submit" to "Send"
4. **Style Changes**: CSS classes reorganized

### Caching (Performance Optimization)

Stagehand v3 caches discovered elements:

```typescript
// First call: AI analyzes page, finds element (slow)
await stagehand.act({ action: "click login" });

// Second call: Uses cached selector (fast)
await stagehand.act({ action: "click login" });

// Cache invalidated when page changes significantly
```

---

## Hybrid Approach: Playwright + Stagehand

Combine traditional speed with AI resilience:

```typescript
import { Stagehand } from "@browserbase/stagehand";
import { test, expect } from "@playwright/test";

test('hybrid test', async () => {
  const stagehand = new Stagehand({ env: "LOCAL" });
  await stagehand.init();

  // Use Playwright for stable, fast operations
  await stagehand.page.goto('https://app.example.com');
  await stagehand.page.fill('[data-testid="email"]', 'test@example.com');

  // Use Stagehand for dynamic/fragile elements
  await stagehand.act({ action: "click the login button" });

  // Use Playwright for assertions
  await expect(stagehand.page).toHaveURL(/dashboard/);

  // Use Stagehand for complex extraction
  const dashboardData = await stagehand.extract({
    instruction: "get user stats from dashboard",
    schema: z.object({
      totalOrders: z.number(),
      accountBalance: z.number(),
    }),
  });

  expect(dashboardData.totalOrders).toBeGreaterThan(0);
});
```

---

## Claude Integration

### Model Selection

```typescript
// Claude Sonnet 4 (recommended - balance of speed/quality)
const stagehand = new Stagehand({
  modelName: "claude-sonnet-4-20250514",
  modelClientOptions: {
    apiKey: process.env.ANTHROPIC_API_KEY,
  },
});

// Claude Opus (highest quality, slower)
const stagehand = new Stagehand({
  modelName: "claude-opus-4-20250514",
});

// Claude Haiku (fastest, simpler tasks)
const stagehand = new Stagehand({
  modelName: "claude-3-5-haiku-20241022",
});
```

### Cost Optimization

```typescript
// Use Haiku for simple actions (cheaper)
const simpleStagehand = new Stagehand({
  modelName: "claude-3-5-haiku-20241022",
});
await simpleStagehand.act({ action: "click login" });

// Use Sonnet for complex extraction
const complexStagehand = new Stagehand({
  modelName: "claude-sonnet-4-20250514",
});
const data = await complexStagehand.extract({
  instruction: "extract all product details with nested specifications",
  schema: complexSchema,
});
```

### Estimated Costs

| Operation | Model | Est. Cost |
|-----------|-------|-----------|
| Simple act() | Haiku | ~$0.001 |
| Complex act() | Sonnet | ~$0.005 |
| Simple extract() | Haiku | ~$0.002 |
| Complex extract() | Sonnet | ~$0.01 |

---

## MCP Integration

Use Stagehand with Claude Desktop via Model Context Protocol:

```typescript
// Stagehand MCP server enables Claude to control browsers
// from Claude Desktop or any MCP-compatible client

import { StagehandMCPServer } from "@browserbase/stagehand/mcp";

const server = new StagehandMCPServer();
server.start();

// Now Claude can call:
// - stagehand.act({ action: "..." })
// - stagehand.extract({ instruction: "..." })
// - stagehand.observe({ instruction: "..." })
```

---

## Error Handling

```typescript
try {
  await stagehand.act({
    action: "click the non-existent button",
    timeout: 10000,  // 10 second timeout
  });
} catch (error) {
  if (error.message.includes('timeout')) {
    console.log('Element not found within timeout');
  } else if (error.message.includes('multiple')) {
    console.log('Multiple matching elements found - be more specific');
  } else {
    throw error;
  }
}

// Retry pattern
async function actWithRetry(stagehand, action, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await stagehand.act({ action });
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}
```

---

## Best Practices

### 1. Be Specific in Instructions

```typescript
// BAD - ambiguous
await stagehand.act({ action: "click button" });

// GOOD - specific
await stagehand.act({ action: "click the blue 'Add to Cart' button below the product image" });
```

### 2. Use Context

```typescript
// Provide context for better accuracy
await stagehand.act({
  action: "in the navigation menu, click on 'Settings'"
});

await stagehand.act({
  action: "in the user dropdown in the top right, click 'Logout'"
});
```

### 3. Combine with Playwright for Speed

```typescript
// Fast: Use Playwright for data-testid elements
await stagehand.page.click('[data-testid="submit"]');

// Resilient: Use Stagehand for dynamic elements
await stagehand.act({ action: "dismiss the cookie banner" });
```

### 4. Schema Validation

```typescript
// Always use Zod schemas for type safety
const schema = z.object({
  title: z.string().min(1),
  price: z.number().positive(),
  inStock: z.boolean(),
});

const data = await stagehand.extract({
  instruction: "get product details",
  schema,
});
// data is fully typed!
```

---

## Use Cases

1. **Self-Healing E2E Tests**: Tests that survive UI redesigns
2. **Web Scraping**: Extract data from any website
3. **Form Automation**: Fill complex forms automatically
4. **Testing AI Chatbots**: Interact with conversational UIs
5. **Cross-Site Workflows**: Automate multi-site processes

---

## References

- `references/stagehand-v3-guide.md` - Complete API reference
- `references/claude-integration.md` - API setup and model selection
- `references/self-healing-patterns.md` - Advanced patterns

---

**Stagehand v3 brings AI-powered self-healing to browser automation - tests that adapt instead of break.**
