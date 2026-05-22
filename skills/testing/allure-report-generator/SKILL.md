---
name: Allure Report Generator
description: Configure and generate rich Allure test reports with test categorization, historical trends, environment details, and CI/CD integration for comprehensive test visibility
version: 1.0.0
author: Pramod
license: MIT
tags: [allure, test-reporting, test-results, ci-reporting, test-history, test-dashboard, reporting-framework]
testingTypes: [e2e, integration]
frameworks: [playwright, jest, pytest]
languages: [typescript, javascript, python, java]
domains: [devops]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Allure Report Generator

Allure is an open-source test reporting framework that produces rich, interactive HTML reports from test execution results. Unlike basic test reporters that show pass/fail summaries, Allure provides detailed test categorization, step-by-step execution breakdowns, attachment support for screenshots, logs, and videos, historical trend tracking across builds, and environment metadata. This skill guides AI coding agents through configuring Allure reporters for popular testing frameworks, annotating tests with meaningful metadata, integrating with CI/CD pipelines, and establishing report hosting strategies that give teams comprehensive test visibility.

## Core Principles

1. **Reports Serve Multiple Audiences**: A good test report provides quick pass/fail summaries for managers, detailed failure analysis for developers, trend data for QA leads, and categorized views for test strategists. Allure's multi-view design supports all these personas from a single report.

2. **Annotations Are Documentation**: Test step annotations, severity labels, and feature/story categorization serve as living documentation of test intent. Well-annotated tests in Allure reports communicate what is being tested and why without requiring code access.

3. **Attachments Accelerate Debugging**: Screenshots, DOM snapshots, network logs, and video recordings attached to test steps eliminate the need to reproduce failures locally. Every failure should carry sufficient attachments for diagnosis from the report alone.

4. **History Reveals Patterns**: A single test run is a snapshot. Historical trend data across builds reveals flaky tests that oscillate between pass and fail, degrading tests with gradually increasing failures, and regression patterns that correlate with specific changes.

5. **Categories Group Failures by Root Cause**: Allure categories classify failures by type (product defect, test defect, infrastructure issue) rather than by test name. This grouping accelerates triage by surfacing the most common failure modes across the entire suite.

6. **Environment Context Is Non-Negotiable**: Test results without environment information (browser version, OS, API version, deployment target) are incomplete. The same test can produce different results across environments, and the report must capture this context.

7. **Reports Must Be Accessible**: Test reports that exist only on a developer's local machine provide no team value. Reports must be published to a shared location where all stakeholders can access them without technical setup.

## Project Structure

```
project-root/
├── tests/
│   ├── e2e/
│   │   ├── checkout.spec.ts
│   │   ├── search.spec.ts
│   │   └── user-management.spec.ts
│   ├── integration/
│   │   ├── api-orders.test.ts
│   │   └── api-users.test.ts
│   └── fixtures/
│       └── allure-fixture.ts
├── allure-results/                    # Raw test results (JSON + attachments)
│   ├── *-result.json
│   ├── *-container.json
│   └── *-attachment.*
├── allure-report/                     # Generated HTML report
│   ├── index.html
│   ├── data/
│   └── widgets/
├── config/
│   ├── playwright.config.ts
│   ├── jest.config.ts
│   ├── allure-categories.json
│   └── allure-environment.properties
├── scripts/
│   ├── generate-report.sh
│   ├── publish-report.ts
│   └── setup-history.sh
├── .github/
│   └── workflows/
│       └── test-and-report.yml
└── package.json
```

## Allure Reporter Setup for Playwright

### Installation and Configuration

```bash
npm install --save-dev allure-playwright allure-commandline
```

```typescript
// config/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: 1,

  reporter: [
    // Console output for local development
    ['list'],

    // Allure reporter for rich reports
    [
      'allure-playwright',
      {
        detail: true,
        outputFolder: 'allure-results',
        suiteTitle: true,

        // Attach environment info
        environmentInfo: {
          'Node Version': process.version,
          OS: process.platform,
          'Test Environment': process.env.TEST_ENV || 'local',
          'Base URL': process.env.BASE_URL || 'http://localhost:3000',
          Browser: 'Chromium',
          'Playwright Version': require('@playwright/test/package.json').version,
        },

        // Categories for failure classification
        categories: [
          {
            name: 'Product Defects',
            matchedStatuses: ['failed'],
            messageRegex: '.*Expected.*to (be|have|contain).*',
          },
          {
            name: 'Test Infrastructure',
            matchedStatuses: ['broken'],
            messageRegex: '.*timeout|ECONNREFUSED|net::ERR.*',
          },
          {
            name: 'Flaky Tests',
            matchedStatuses: ['failed'],
            messageRegex: '.*flaky|intermittent.*',
            traceRegex: '.*retry.*',
          },
        ],
      },
    ],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
});
```

### Custom Step Annotations in Playwright

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test.describe('Checkout Flow', () => {
  test.beforeEach(async ({ page }) => {
    await allure.epic('E-Commerce');
    await allure.feature('Checkout');
    await allure.owner('team-payments');
  });

  test('should complete purchase with credit card', async ({ page }) => {
    await allure.severity('critical');
    await allure.story('Credit Card Payment');
    await allure.tag('smoke');
    await allure.tag('payments');

    // Add link to test case management system
    await allure.link('https://jira.example.com/browse/QA-100', 'Test Case', 'tms');
    await allure.issue('BUG-456', 'https://jira.example.com/browse/BUG-456');

    // Step 1: Add item to cart
    await allure.step('Add product to cart', async () => {
      await page.goto('/products/1');
      await page.click('[data-testid="add-to-cart"]');
      await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

      // Attach product page screenshot
      const screenshot = await page.screenshot();
      await allure.attachment('Product Page', screenshot, 'image/png');
    });

    // Step 2: Navigate to checkout
    await allure.step('Navigate to checkout page', async () => {
      await page.click('[data-testid="cart-icon"]');
      await page.click('[data-testid="proceed-to-checkout"]');
      await expect(page).toHaveURL('/checkout');
    });

    // Step 3: Fill payment details
    await allure.step('Enter payment information', async () => {
      await allure.step('Fill card number', async () => {
        await page.fill('[data-testid="card-number"]', '4242424242424242');
      });
      await allure.step('Fill expiry date', async () => {
        await page.fill('[data-testid="card-expiry"]', '12/28');
      });
      await allure.step('Fill CVV', async () => {
        await page.fill('[data-testid="card-cvv"]', '123');
      });
    });

    // Step 4: Submit order
    await allure.step('Place order', async () => {
      await page.click('[data-testid="place-order"]');
      await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible({
        timeout: 15000,
      });

      // Capture confirmation details
      const confirmationText = await page
        .locator('[data-testid="order-confirmation"]')
        .textContent();
      await allure.attachment('Order Confirmation', confirmationText || '', 'text/plain');
    });

    // Step 5: Verify order details
    await allure.step('Verify order details', async () => {
      const orderId = await page.locator('[data-testid="order-id"]').textContent();
      expect(orderId).toBeTruthy();

      // Attach full page screenshot
      const fullPage = await page.screenshot({ fullPage: true });
      await allure.attachment('Confirmation Page', fullPage, 'image/png');

      // Attach API response for debugging
      const orderDetails = await page.evaluate(async (id) => {
        const res = await fetch(`/api/orders/${id}`);
        return res.json();
      }, orderId);
      await allure.attachment(
        'Order API Response',
        JSON.stringify(orderDetails, null, 2),
        'application/json'
      );
    });
  });

  test('should show validation errors for invalid card', async ({ page }) => {
    await allure.severity('normal');
    await allure.story('Payment Validation');

    await page.goto('/checkout');

    await allure.step('Submit empty payment form', async () => {
      await page.click('[data-testid="place-order"]');
    });

    await allure.step('Verify validation errors displayed', async () => {
      await expect(page.locator('[data-testid="card-error"]')).toHaveText(
        'Card number is required'
      );
      await expect(page.locator('[data-testid="expiry-error"]')).toHaveText(
        'Expiry date is required'
      );
    });
  });
});
```

### Custom Allure Fixture for Reusable Annotations

```typescript
// tests/fixtures/allure-fixture.ts
import { test as base } from '@playwright/test';
import { allure } from 'allure-playwright';

interface AllureOptions {
  epic: string;
  feature: string;
  severity: 'blocker' | 'critical' | 'normal' | 'minor' | 'trivial';
}

export const test = base.extend<{ allureConfig: AllureOptions }>({
  allureConfig: [
    async ({}, use, testInfo) => {
      // Auto-derive categorization from test file path
      const filePath = testInfo.file;
      let epic = 'General';
      let feature = 'Uncategorized';

      if (filePath.includes('checkout')) {
        epic = 'E-Commerce';
        feature = 'Checkout';
      } else if (filePath.includes('search')) {
        epic = 'Discovery';
        feature = 'Search';
      } else if (filePath.includes('user')) {
        epic = 'Account';
        feature = 'User Management';
      }

      await allure.epic(epic);
      await allure.feature(feature);

      // Attach test metadata
      await allure.parameter('Browser', testInfo.project.name);
      await allure.parameter('Retry Attempt', String(testInfo.retry));

      const options: AllureOptions = {
        epic,
        feature,
        severity: 'normal',
      };

      await use(options);

      // After test: attach trace on failure
      if (testInfo.status !== 'passed') {
        const tracePath = testInfo.outputPath('trace.zip');
        try {
          const traceBuffer = require('fs').readFileSync(tracePath);
          await allure.attachment('Playwright Trace', traceBuffer, 'application/zip');
        } catch {
          // Trace not available
        }
      }
    },
    { auto: true },
  ],
});

export { expect } from '@playwright/test';
```

## Allure Reporter Setup for Jest

```bash
npm install --save-dev allure-jest allure-js-commons allure-commandline
```

```typescript
// config/jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'allure-jest/node',
  testEnvironmentOptions: {
    resultsDir: 'allure-results',
    environmentInfo: {
      'Node Version': process.version,
      OS: process.platform,
      'Test Environment': process.env.TEST_ENV || 'local',
    },
  },
  reporters: ['default'],
};

export default config;
```

### Jest Test with Allure Annotations

```typescript
// tests/integration/api-orders.test.ts
import { allure } from 'allure-js-commons';

describe('Orders API', () => {
  beforeAll(async () => {
    await allure.epic('API');
    await allure.feature('Orders');
  });

  it('should create a new order', async () => {
    await allure.severity('critical');
    await allure.story('Order Creation');
    await allure.owner('team-orders');
    await allure.tag('api');
    await allure.tag('smoke');

    await allure.step('Prepare order payload', async () => {
      const payload = {
        customerId: 42,
        items: [{ productId: 'prod-001', quantity: 2 }],
        shippingAddress: {
          street: '123 Main St',
          city: 'Portland',
          state: 'OR',
          zip: '97201',
        },
      };
      await allure.attachment(
        'Request Payload',
        JSON.stringify(payload, null, 2),
        'application/json'
      );

      await allure.step('Send POST request', async () => {
        const response = await fetch('http://localhost:3000/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        expect(response.status).toBe(201);

        const body = await response.json();
        await allure.attachment(
          'Response Body',
          JSON.stringify(body, null, 2),
          'application/json'
        );

        await allure.step('Verify order ID assigned', async () => {
          expect(body.id).toBeDefined();
          expect(typeof body.id).toBe('string');
        });

        await allure.step('Verify order total calculated', async () => {
          expect(body.total).toBeGreaterThan(0);
        });
      });
    });
  });

  it('should return 400 for invalid order', async () => {
    await allure.severity('normal');
    await allure.story('Order Validation');

    await allure.step('Send order without required fields', async () => {
      const response = await fetch('http://localhost:3000/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });

      expect(response.status).toBe(400);

      const body = await response.json();
      await allure.attachment(
        'Error Response',
        JSON.stringify(body, null, 2),
        'application/json'
      );

      await allure.step('Verify error details', async () => {
        expect(body.errors).toBeDefined();
        expect(body.errors.length).toBeGreaterThan(0);
      });
    });
  });
});
```

## Allure Reporter Setup for pytest

```bash
pip install allure-pytest
```

```ini
# pytest.ini
[pytest]
addopts = --alluredir=allure-results --clean-alluredir
```

### Python Test with Allure Annotations

```python
# tests/test_user_api.py
import allure
import pytest
import requests
import json

BASE_URL = "http://localhost:8000"


@allure.epic("API")
@allure.feature("User Management")
class TestUserAPI:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("User Registration")
    @allure.title("Register a new user with valid data")
    @allure.tag("api", "smoke", "registration")
    @allure.link("https://jira.example.com/browse/QA-200", name="Test Case")
    def test_register_user(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "SecureP@ss123",
        }

        with allure.step("Prepare registration payload"):
            allure.attach(
                json.dumps(payload, indent=2),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Send POST /api/users/register"):
            response = requests.post(
                f"{BASE_URL}/api/users/register", json=payload
            )

            allure.attach(
                json.dumps(response.json(), indent=2),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Verify registration succeeded"):
            assert response.status_code == 201
            body = response.json()
            assert "id" in body
            assert body["email"] == "jane@example.com"

        with allure.step("Verify user can authenticate"):
            login_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": "jane@example.com",
                    "password": "SecureP@ss123",
                },
            )
            assert login_response.status_code == 200
            assert "token" in login_response.json()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("User Registration")
    @allure.title("Reject registration with duplicate email")
    def test_register_duplicate_email(self):
        payload = {
            "name": "Duplicate",
            "email": "existing@example.com",
            "password": "Pass123!",
        }

        with allure.step("Register user with existing email"):
            response = requests.post(
                f"{BASE_URL}/api/users/register", json=payload
            )

        with allure.step("Verify conflict error returned"):
            assert response.status_code == 409
            assert "already exists" in response.json()["message"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("User Profile")
    @allure.title("Retrieve user profile with valid token")
    def test_get_user_profile(self, auth_token):
        with allure.step("Send GET /api/users/me with auth token"):
            response = requests.get(
                f"{BASE_URL}/api/users/me",
                headers={"Authorization": f"Bearer {auth_token}"},
            )

            allure.attach(
                json.dumps(response.json(), indent=2),
                name="Profile Response",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Verify profile data"):
            assert response.status_code == 200
            profile = response.json()
            assert "id" in profile
            assert "name" in profile
            assert "email" in profile
            assert "password" not in profile  # Verify password not exposed


@pytest.fixture
def auth_token():
    """Fixture that provides an authenticated user token."""
    with allure.step("Authenticate test user"):
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPass123!",
            },
        )
        return response.json()["token"]
```

## Environment Info Configuration

```properties
# config/allure-environment.properties
# This file is copied to allure-results/ before report generation
Browser=Chromium 120
OS=Ubuntu 22.04
Node.Version=20.10.0
Test.Environment=staging
API.Base.URL=https://staging-api.example.com
App.Version=2.5.0
Build.Number=${BUILD_NUMBER}
Git.Commit=${GIT_COMMIT}
Git.Branch=${GIT_BRANCH}
Deployment.Region=us-east-1
Database=PostgreSQL 16
```

### Dynamic Environment Properties Script

```typescript
// scripts/generate-environment.ts
import * as fs from 'fs';
import { execSync } from 'child_process';

const gitCommit = execSync('git rev-parse --short HEAD', { encoding: 'utf-8' }).trim();
const gitBranch = execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf-8' }).trim();

const properties = [
  `Browser=${process.env.BROWSER || 'Chromium'}`,
  `OS=${process.platform} ${process.arch}`,
  `Node.Version=${process.version}`,
  `Test.Environment=${process.env.TEST_ENV || 'local'}`,
  `Base.URL=${process.env.BASE_URL || 'http://localhost:3000'}`,
  `Git.Commit=${gitCommit}`,
  `Git.Branch=${gitBranch}`,
  `Build.Number=${process.env.BUILD_NUMBER || 'local'}`,
  `Timestamp=${new Date().toISOString()}`,
].join('\n');

fs.writeFileSync('allure-results/environment.properties', properties);
console.log('Environment properties written to allure-results/environment.properties');
```

## Categories and Severity Labeling

### Categories Configuration

```json
// config/allure-categories.json
[
  {
    "name": "Product Defects",
    "description": "Failures caused by actual application bugs",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*Expected .* (to be|to have|to contain|to equal).*"
  },
  {
    "name": "Test Infrastructure Issues",
    "description": "Failures caused by test environment problems",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*(timeout|ECONNREFUSED|ENOTFOUND|ETIMEDOUT|net::ERR|Navigation).*"
  },
  {
    "name": "Element Not Found",
    "description": "Failures where expected UI elements are missing",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*(locator|selector|element).*(not found|not visible|not attached).*"
  },
  {
    "name": "API Errors",
    "description": "Failures in API response validation",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*(status code|response|4\\d{2}|5\\d{2}).*"
  },
  {
    "name": "Data Setup Failures",
    "description": "Failures in test fixture or data preparation",
    "matchedStatuses": ["broken"],
    "traceRegex": ".*(beforeAll|beforeEach|fixture|setup).*"
  },
  {
    "name": "Outdated Tests",
    "description": "Tests that need updating due to application changes",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*(deprecated|removed|changed|no longer).*"
  }
]
```

### Copying Categories to Results

```bash
#!/bin/bash
# scripts/generate-report.sh

# Copy categories to allure-results (must be present before generation)
cp config/allure-categories.json allure-results/categories.json

# Generate environment properties
npx ts-node scripts/generate-environment.ts

# Copy history from previous report (for trends)
if [ -d "allure-report/history" ]; then
  cp -r allure-report/history allure-results/history
fi

# Generate the report
npx allure generate allure-results --clean -o allure-report

echo "Report generated at allure-report/index.html"
```

## Historical Trend Tracking

### Preserving History Across Builds

```bash
#!/bin/bash
# scripts/setup-history.sh
# Run before each test execution to preserve historical data

HISTORY_DIR="allure-results/history"
REPORT_HISTORY="allure-report/history"

# If a previous report exists, copy its history to the new results directory
if [ -d "$REPORT_HISTORY" ]; then
  mkdir -p "$HISTORY_DIR"
  cp -r "$REPORT_HISTORY/"* "$HISTORY_DIR/"
  echo "History preserved from previous report"
else
  echo "No previous history found (first run)"
fi
```

### CI History Preservation with Artifacts

```yaml
# In a GitHub Actions workflow, history is preserved via artifacts
- name: Download previous report history
  uses: actions/download-artifact@v4
  with:
    name: allure-report-history
    path: allure-results/history
  continue-on-error: true  # First run will not have history

# After report generation
- name: Save report history
  uses: actions/upload-artifact@v4
  with:
    name: allure-report-history
    path: allure-report/history
    retention-days: 30
```

## CI Integration

### GitHub Actions Complete Workflow

```yaml
# .github/workflows/test-and-report.yml
name: Test and Report
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps

      # Download previous Allure history for trends
      - name: Restore Allure history
        uses: actions/download-artifact@v4
        with:
          name: allure-history
          path: allure-results/history
        continue-on-error: true

      # Run tests
      - name: Run Playwright tests
        run: npx playwright test
        continue-on-error: true
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          TEST_ENV: ci

      # Generate environment properties
      - name: Generate environment info
        run: |
          cat > allure-results/environment.properties << EOF
          Browser=Chromium
          OS=Ubuntu (CI)
          Node.Version=$(node --version)
          Test.Environment=CI
          Git.Commit=${{ github.sha }}
          Git.Branch=${{ github.ref_name }}
          Build.Number=${{ github.run_number }}
          PR.Number=${{ github.event.pull_request.number || 'N/A' }}
          EOF

      # Copy categories
      - name: Setup Allure categories
        run: cp config/allure-categories.json allure-results/categories.json

      # Generate report
      - name: Generate Allure Report
        run: |
          npm install -g allure-commandline
          allure generate allure-results --clean -o allure-report

      # Save history for next run
      - name: Save Allure history
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-history
          path: allure-report/history
          retention-days: 60

      # Upload full report
      - name: Upload Allure Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-report
          path: allure-report/
          retention-days: 30

  # Deploy report to GitHub Pages
  deploy-report:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: allure-report
          path: allure-report

      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: allure-report
      - id: deployment
        uses: actions/deploy-pages@v4
```

### Jenkins Pipeline Integration

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'npm ci'
                sh 'npx playwright install --with-deps'
                sh 'npx playwright test || true'
            }
            post {
                always {
                    // Copy environment properties
                    sh '''
                        echo "Browser=Chromium" > allure-results/environment.properties
                        echo "Build.Number=${BUILD_NUMBER}" >> allure-results/environment.properties
                        echo "Git.Commit=${GIT_COMMIT}" >> allure-results/environment.properties
                        echo "Node.Version=$(node --version)" >> allure-results/environment.properties
                    '''

                    // Jenkins Allure plugin generates report and preserves history
                    allure([
                        includeProperties: true,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
    }
}
```

## Allure TestOps Overview

Allure TestOps is the commercial companion to Allure Report, providing centralized test management, real-time dashboards, and analytics across multiple projects.

```typescript
// Integration with Allure TestOps (if available)
// config/allure-testops.config.ts
export const testOpsConfig = {
  // TestOps server configuration
  endpoint: process.env.ALLURE_TESTOPS_URL || 'https://allure.example.com',
  token: process.env.ALLURE_TESTOPS_TOKEN,
  projectId: parseInt(process.env.ALLURE_PROJECT_ID || '1'),

  // Launch configuration
  launchName: `${process.env.GIT_BRANCH || 'local'} - ${new Date().toISOString()}`,
  launchTags: [process.env.TEST_ENV || 'local', process.env.GIT_BRANCH || 'unknown'],
};

// Upload results to TestOps after test execution:
// npx allurectl upload allure-results \
//   --endpoint $ALLURE_TESTOPS_URL \
//   --token $ALLURE_TESTOPS_TOKEN \
//   --project-id 1
```

## Custom Widgets

Allure reports support custom widgets that display aggregated data on the report overview page.

```json
// allure-results/widgets/summary.json (custom widget data)
{
  "reportName": "E-Commerce Test Suite",
  "testRuns": [
    {
      "name": "Smoke Tests",
      "total": 25,
      "passed": 24,
      "failed": 1,
      "broken": 0,
      "skipped": 0
    },
    {
      "name": "Regression Tests",
      "total": 150,
      "passed": 142,
      "failed": 5,
      "broken": 2,
      "skipped": 1
    }
  ],
  "environment": "Staging",
  "duration": "12m 34s"
}
```

## Report Hosting Strategies

### Strategy 1: GitHub Pages (Free, Public)

```bash
# Deploy to GitHub Pages using gh-pages package
npm install -g gh-pages

# Generate and deploy
allure generate allure-results -o allure-report
gh-pages -d allure-report -m "Allure Report $(date +%Y-%m-%d)"
```

### Strategy 2: S3 Static Hosting (Private, Scalable)

```typescript
// scripts/publish-report.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import * as fs from 'fs';
import * as path from 'path';
import * as mime from 'mime-types';

const s3 = new S3Client({ region: process.env.AWS_REGION || 'us-east-1' });
const BUCKET = process.env.REPORT_BUCKET || 'test-reports';
const PREFIX = `allure/${process.env.GIT_BRANCH || 'main'}/${Date.now()}`;

async function uploadDirectory(dirPath: string, s3Prefix: string): Promise<void> {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const s3Key = `${s3Prefix}/${entry.name}`;

    if (entry.isDirectory()) {
      await uploadDirectory(fullPath, s3Key);
    } else {
      const contentType = mime.lookup(entry.name) || 'application/octet-stream';
      await s3.send(
        new PutObjectCommand({
          Bucket: BUCKET,
          Key: s3Key,
          Body: fs.readFileSync(fullPath),
          ContentType: contentType,
        })
      );
    }
  }
}

async function main() {
  console.log(`Uploading report to s3://${BUCKET}/${PREFIX}/`);
  await uploadDirectory('allure-report', PREFIX);
  console.log(`Report available at: https://${BUCKET}.s3.amazonaws.com/${PREFIX}/index.html`);
}

main().catch(console.error);
```

### Strategy 3: Docker Container (Self-Hosted)

```yaml
# docker-compose.yml for self-hosted Allure report server
version: '3.8'
services:
  allure-server:
    image: frankescobar/allure-docker-service:latest
    ports:
      - "5050:5050"
    environment:
      CHECK_RESULTS_EVERY_SECONDS: 5
      KEEP_HISTORY: 25
    volumes:
      - ./allure-results:/app/allure-results
      - ./allure-reports:/app/default-reports
```

## Configuration

### Package.json Scripts

```json
{
  "scripts": {
    "test": "playwright test",
    "test:report": "playwright test && npm run allure:generate",
    "allure:generate": "bash scripts/generate-report.sh",
    "allure:open": "allure open allure-report",
    "allure:serve": "allure serve allure-results",
    "allure:clean": "rm -rf allure-results allure-report",
    "allure:history": "bash scripts/setup-history.sh",
    "allure:publish": "ts-node scripts/publish-report.ts"
  }
}
```

### Allure Commandline Installation

```bash
# Via npm (recommended for JavaScript projects)
npm install -g allure-commandline

# Via Homebrew (macOS)
brew install allure

# Via scoop (Windows)
scoop install allure

# Verify installation
allure --version
```

## Best Practices

1. **Annotate every test with severity.** Use Allure severity levels (blocker, critical, normal, minor, trivial) consistently. This enables filtering the report by severity during triage sessions.

2. **Organize tests with epic/feature/story hierarchy.** Map tests to the product feature hierarchy so the Allure Behaviors view reflects the actual product structure. This helps stakeholders navigate reports by business functionality.

3. **Attach screenshots and videos on failure only.** Recording screenshots and videos for all tests inflates report size without benefit. Configure `screenshot: 'only-on-failure'` and `video: 'retain-on-failure'`.

4. **Use meaningful step descriptions.** Steps should describe intent ("Add product to cart"), not implementation ("Click button with data-testid add-to-cart"). Report readers may not have code access.

5. **Configure categories to match your failure taxonomy.** Customize `categories.json` to classify failures into actionable groups. Default categories are too generic for effective triage.

6. **Preserve history across CI builds.** Without history, trend charts are empty and test retries lack context. Use CI artifacts or external storage to maintain history for at least 20-30 builds.

7. **Generate environment properties dynamically.** Hardcoded environment files become stale. Generate them from CI environment variables and git metadata at report generation time.

8. **Attach API request/response pairs for API tests.** When API tests fail, the request payload and response body attached to the report step eliminate the need to reproduce the failure locally.

9. **Include links to test case management and issue tracking.** Use `allure.link()` and `allure.issue()` to connect report entries to external systems. This creates bidirectional traceability between reports and project management tools.

10. **Host reports on a persistent URL.** Ephemeral reports in CI artifacts are hard to share. Deploy to GitHub Pages, S3, or a dedicated report server where stakeholders can always find the latest report.

11. **Set up Slack or email notifications for report availability.** After CI generates a report, notify the team with a direct link. Reports that nobody opens provide no value.

12. **Review report trends weekly.** Schedule a brief weekly review of the Allure trend view to catch increasing failure rates, growing test suite duration, or emerging flaky test patterns before they become systemic problems.

## Anti-Patterns to Avoid

1. **Generating reports without categories configuration.** Without categories, all failures appear in a single undifferentiated list. Categories enable meaningful failure classification that accelerates triage.

2. **Over-attaching large files to every test.** Attaching multi-megabyte videos or full HAR files to every test (including passing tests) creates enormous reports that are slow to generate, upload, and browse.

3. **Using generic step names.** Steps labeled "Step 1", "Step 2", or "Verification" provide no value. Each step name should clearly describe what is happening and why.

4. **Ignoring the Allure report trend view.** Running Allure without preserving history across builds discards the most valuable feature: the ability to see trends and identify degradation over time.

5. **Skipping environment configuration.** A report without environment details cannot be interpreted correctly. The same test result means different things on Chrome vs Firefox, or staging vs production.

6. **Treating report generation as an afterthought.** Report configuration should be established early in the project, not bolted on when stakeholders demand visibility. Retrofit is always harder than upfront setup.

7. **Not cleaning allure-results between runs.** If old results are not cleared before new test runs, the report will contain stale data from previous executions, creating confusion about current test status.

## Debugging Tips

1. **Check allure-results directory for raw data.** If the report looks wrong, inspect the JSON files in `allure-results/`. Each test produces a `-result.json` file containing all metadata, steps, and attachment references.

2. **Verify categories.json is in allure-results before generation.** The categories file must be present in the results directory when the report is generated. Placing it only in the config directory without copying produces a report with no category classifications.

3. **Validate environment.properties format.** The file must use `key=value` format with no quotes around values. Malformed properties are silently ignored, resulting in missing environment information in the report.

4. **Check attachment file references.** If attachments show as broken links in the report, verify that the attachment files exist in `allure-results/` and that the file names in the result JSON match the actual files on disk.

5. **Use allure serve for quick local preview.** The `allure serve allure-results` command generates a temporary report and opens it in a browser without creating the persistent `allure-report` directory. This is the fastest way to preview results during development.

6. **Verify allure-commandline version compatibility.** Allure Report and the framework reporters must use compatible versions. Check the compatibility matrix in the Allure documentation if reports appear empty or malformatted.

7. **Inspect the history directory structure.** Trend charts require a specific directory structure in `allure-results/history/`. If trends are not appearing, verify that `history.json` and `history-trend.json` from the previous report were correctly copied to the results directory.

8. **Check for conflicting reporters.** Running multiple reporters that write to the same output directory can cause data corruption. Ensure each reporter writes to a distinct directory or uses the framework's built-in multi-reporter support.

9. **Review CI artifact retention policies.** If history suddenly stops working in CI, check whether artifact retention policies expired. History artifacts need to persist across builds, so set retention days appropriately (30-60 days minimum).

10. **Test report generation locally before CI.** Always verify that `allure generate allure-results -o allure-report` works locally with representative test data before debugging CI-specific report issues.
