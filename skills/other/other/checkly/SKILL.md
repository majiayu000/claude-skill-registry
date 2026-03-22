---
name: checkly
description: Expert guidance for Checkly, the synthetic monitoring platform that runs Playwright-based browser checks and API checks from locations worldwide. Helps developers implement monitoring-as-code (MaC) with the Checkly CLI, set up API and browser checks, configure alerting, and integrate monitoring into CI/CD pipelines.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
  - synthetic-monitoring
  - e2e-testing
  - api-monitoring
  - playwright
  - monitoring-as-code
---

# Checkly — Synthetic Monitoring and Testing


## Overview


Checkly, the synthetic monitoring platform that runs Playwright-based browser checks and API checks from locations worldwide. Helps developers implement monitoring-as-code (MaC) with the Checkly CLI, set up API and browser checks, configure alerting, and integrate monitoring into CI/CD pipelines.


## Instructions

### Monitoring as Code

```bash
# Install Checkly CLI
npm install -g checkly

# Initialize in your project
checkly init

# Project structure
# checkly.config.ts — Global configuration
# __checks__/
#   api/
#     health.check.ts
#     orders-api.check.ts
#   browser/
#     login-flow.check.ts
#     checkout.check.ts
```

```typescript
// checkly.config.ts — Global configuration
import { defineConfig } from "checkly";
import { EmailAlertChannel, SlackAlertChannel } from "checkly/constructs";

const slackAlert = new SlackAlertChannel("slack-alerts", {
  webhookUrl: process.env.SLACK_WEBHOOK_URL!,
  channel: "#alerts",
  sendFailure: true,
  sendRecovery: true,
  sendDegraded: true,
});

const emailAlert = new EmailAlertChannel("email-ops", {
  address: "ops@example.com",
  sendFailure: true,
  sendRecovery: true,
});

export default defineConfig({
  projectName: "My SaaS",
  logicalId: "my-saas-monitoring",
  repoUrl: "https://github.com/myorg/my-saas",
  checks: {
    locations: ["us-east-1", "eu-west-1", "ap-southeast-1"],
    frequency: 5,                        // Check every 5 minutes
    tags: ["production"],
    runtimeId: "2024.02",
    alertChannels: [slackAlert, emailAlert],
    browserChecks: {
      frequency: 10,                     // Browser checks every 10 min
      testMatch: "**/__checks__/browser/**/*.check.ts",
    },
    apiChecks: {
      frequency: 1,                      // API checks every 1 min
      testMatch: "**/__checks__/api/**/*.check.ts",
    },
  },
});
```

### API Checks

```typescript
// __checks__/api/orders-api.check.ts — API endpoint monitoring
import { ApiCheck, AssertionBuilder } from "checkly/constructs";

new ApiCheck("orders-api-health", {
  name: "Orders API — Health Check",
  request: {
    method: "GET",
    url: "https://api.example.com/v1/health",
    headers: [{ key: "Authorization", value: `Bearer {{MONITORING_API_KEY}}` }],
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody("$.status").equals("healthy"),
      AssertionBuilder.responseTime().lessThan(2000),   // Under 2 seconds
    ],
  },
  degradedResponseTime: 1000,          // Mark as degraded if > 1s
  maxResponseTime: 3000,               // Mark as failed if > 3s
});

new ApiCheck("orders-create", {
  name: "Orders API — Create Order Flow",
  request: {
    method: "POST",
    url: "https://api.example.com/v1/orders",
    headers: [
      { key: "Authorization", value: "Bearer {{MONITORING_API_KEY}}" },
      { key: "Content-Type", value: "application/json" },
    ],
    body: JSON.stringify({
      items: [{ productId: "test-product", quantity: 1 }],
      test: true,                       // Flag so backend doesn't charge
    }),
    assertions: [
      AssertionBuilder.statusCode().equals(201),
      AssertionBuilder.jsonBody("$.id").isNotEmpty(),
      AssertionBuilder.jsonBody("$.status").equals("pending"),
    ],
  },
  setupScript: {
    // Run before the request — generate dynamic data
    content: `
      const crypto = require('crypto');
      request.headers['X-Idempotency-Key'] = crypto.randomUUID();
    `,
  },
  teardownScript: {
    // Run after the request — clean up test data
    content: `
      if (response.statusCode === 201) {
        const orderId = JSON.parse(response.body).id;
        // Delete the test order
        await fetch(\`https://api.example.com/v1/orders/\${orderId}\`, {
          method: 'DELETE',
          headers: { 'Authorization': 'Bearer ' + process.env.MONITORING_API_KEY },
        });
      }
    `,
  },
});
```

### Browser Checks (Playwright)

```typescript
// __checks__/browser/checkout-flow.check.ts — E2E user flow monitoring
// Runs a real Playwright browser in Checkly's cloud every 10 minutes.
import { test, expect } from "@playwright/test";

test("Complete checkout flow", async ({ page }) => {
  // Step 1: Navigate to product page
  await page.goto("https://example.com/products/starter-plan");
  await expect(page.getByRole("heading", { name: "Starter Plan" })).toBeVisible();

  // Step 2: Add to cart
  await page.getByRole("button", { name: "Start Free Trial" }).click();
  await expect(page.getByText("Added to cart")).toBeVisible();

  // Step 3: Go to checkout
  await page.getByRole("link", { name: "Checkout" }).click();
  await expect(page).toHaveURL(/.*checkout/);

  // Step 4: Fill payment form (test card)
  await page.getByLabel("Email").fill("monitoring@example.com");
  await page.getByLabel("Card number").fill("4242424242424242");
  await page.getByLabel("Expiry").fill("12/28");
  await page.getByLabel("CVC").fill("123");

  // Step 5: Submit
  await page.getByRole("button", { name: "Subscribe" }).click();

  // Step 6: Verify success
  await expect(page.getByText("Welcome to Starter Plan")).toBeVisible({ timeout: 10000 });
});

test("Login flow works", async ({ page }) => {
  await page.goto("https://example.com/login");

  await page.getByLabel("Email").fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel("Password").fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole("button", { name: "Sign in" }).click();

  // Verify dashboard loads
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  await expect(page.getByText("Welcome back")).toBeVisible();
});
```

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml — Run checks after deployment
- name: Deploy to production
  run: npm run deploy

- name: Run Checkly checks
  uses: checkly/checkly-github-action@v1
  with:
    apiKey: ${{ secrets.CHECKLY_API_KEY }}
    accountId: ${{ secrets.CHECKLY_ACCOUNT_ID }}
    # Run all checks and fail the pipeline if any fail
    command: "checkly test --record"
```

```bash
# Deploy checks to Checkly (like deploying infrastructure)
checkly deploy

# Test locally before deploying
checkly test

# Dry run — show what would change
checkly deploy --preview
```

## Installation

```bash
npm install -g checkly
checkly login
checkly init
```


## Examples


### Example 1: Setting up Checkly for a microservices project

**User request:**

```
I have a Node.js API and a React frontend running in Docker. Set up Checkly for monitoring/deployment.
```

The agent creates the necessary configuration files based on patterns like `# Install Checkly CLI`, sets up the integration with the existing Docker setup, configures appropriate defaults for a Node.js + React stack, and provides verification commands to confirm everything is working.

### Example 2: Troubleshooting api checks issues

**User request:**

```
Checkly is showing errors in our api checks. Here are the logs: [error output]
```

The agent analyzes the error output, identifies the root cause by cross-referencing with common Checkly issues, applies the fix (updating configuration, adjusting resource limits, or correcting syntax), and verifies the resolution with appropriate health checks.


## Guidelines

1. **Monitoring as code** — Define checks in your repo alongside application code; version, review, and deploy together
2. **API + browser checks** — API checks catch backend issues fast (every 1 min); browser checks validate user flows (every 10 min)
3. **Multi-region** — Run checks from 3+ regions; catch regional outages and CDN issues
4. **Playwright for browser** — Checkly uses Playwright natively; reuse your E2E tests as production monitors
5. **Degraded vs failed** — Set degraded thresholds (e.g., > 1s) separate from failure (> 3s); catch slowdowns before they become outages
6. **Clean up test data** — Use teardown scripts to delete test orders/users created by monitoring checks
7. **CI/CD integration** — Run checks after every deployment; automatically catch regressions before users do
8. **Environment variables** — Store API keys and test credentials as Checkly environment variables, not in code
