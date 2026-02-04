---
name: mistral-ci-integration
description: |
  Configure Mistral AI CI/CD integration with GitHub Actions and testing.
  Use when setting up automated testing, configuring CI pipelines,
  or integrating Mistral AI tests into your build process.
  Trigger with phrases like "mistral CI", "mistral GitHub Actions",
  "mistral automated tests", "CI mistral".
allowed-tools: Read, Write, Edit, Bash(gh:*)
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI CI Integration

## Overview
Set up CI/CD pipelines for Mistral AI integrations with automated testing.

## Prerequisites
- GitHub repository with Actions enabled
- Mistral AI test API key
- npm/pnpm project configured

## Instructions

### Step 1: Create GitHub Actions Workflow

Create `.github/workflows/mistral-integration.yml`:

```yaml
name: Mistral AI Integration Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  lint-and-type:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci

      - name: Type Check
        run: npm run typecheck

      - name: Lint
        run: npm run lint

  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci

      - name: Run Unit Tests
        run: npm test -- --coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [lint-and-type, unit-tests]
    # Only run on main branch or manual trigger
    if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
    env:
      MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci

      - name: Run Integration Tests
        run: npm run test:integration
        timeout-minutes: 10

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
```

### Step 2: Configure Secrets

```bash
# Add API key to repository secrets
gh secret set MISTRAL_API_KEY --body "your-test-api-key"

# Verify secret is set
gh secret list
```

### Step 3: Create Integration Test File

```typescript
// tests/integration/mistral.integration.test.ts
import { describe, it, expect, beforeAll } from 'vitest';
import Mistral from '@mistralai/mistralai';

describe('Mistral AI Integration', () => {
  let client: Mistral;

  beforeAll(() => {
    const apiKey = process.env.MISTRAL_API_KEY;
    if (!apiKey) {
      throw new Error('MISTRAL_API_KEY required for integration tests');
    }
    client = new Mistral({ apiKey });
  });

  it('should list available models', async () => {
    const models = await client.models.list();

    expect(models.data).toBeDefined();
    expect(models.data?.length).toBeGreaterThan(0);

    const modelIds = models.data?.map(m => m.id) || [];
    expect(modelIds).toContain('mistral-small-latest');
  });

  it('should complete a chat request', async () => {
    const response = await client.chat.complete({
      model: 'mistral-small-latest',
      messages: [
        { role: 'user', content: 'Reply with exactly: Integration test passed' }
      ],
      maxTokens: 20,
    });

    expect(response.choices).toBeDefined();
    expect(response.choices?.[0]?.message?.content).toContain('Integration test');
    expect(response.usage?.totalTokens).toBeGreaterThan(0);
  });

  it('should handle streaming responses', async () => {
    const stream = await client.chat.stream({
      model: 'mistral-small-latest',
      messages: [
        { role: 'user', content: 'Count from 1 to 3' }
      ],
      maxTokens: 20,
    });

    const chunks: string[] = [];
    for await (const event of stream) {
      const content = event.data?.choices?.[0]?.delta?.content;
      if (content) {
        chunks.push(content);
      }
    }

    expect(chunks.length).toBeGreaterThan(0);
    expect(chunks.join('')).toBeTruthy();
  });

  it('should generate embeddings', async () => {
    const response = await client.embeddings.create({
      model: 'mistral-embed',
      inputs: ['Hello world'],
    });

    expect(response.data).toBeDefined();
    expect(response.data[0].embedding.length).toBe(1024);
  });
});
```

### Step 4: Create Vitest Integration Config

```typescript
// vitest.integration.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/integration/**/*.test.ts'],
    testTimeout: 60000, // 60s for API calls
    hookTimeout: 30000,
    retry: 2, // Retry flaky tests
    reporters: ['verbose', 'junit'],
    outputFile: {
      junit: 'test-results/junit.xml',
    },
  },
});
```

### Step 5: Add Package Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:integration": "vitest run --config vitest.integration.config.ts",
    "test:coverage": "vitest run --coverage",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src tests --ext .ts"
  }
}
```

## Output
- Automated test pipeline
- PR checks configured
- Coverage reports uploaded
- Integration tests on main branch

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Secret not found | Missing configuration | Add secret via `gh secret set` |
| Tests timeout | Slow API | Increase timeout or mock |
| Auth failures | Invalid key | Check secret value |
| Rate limiting | Too many tests | Add delays or reduce test count |

## Examples

### Release Workflow with Mistral Validation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  validate:
    runs-on: ubuntu-latest
    env:
      MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY_PROD }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci

      - name: Verify Mistral Integration
        run: npm run test:integration

      - name: Build
        run: npm run build

      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### PR Comment with Test Results

```yaml
- name: Comment PR with Results
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const coverage = fs.readFileSync('coverage/coverage-summary.json', 'utf8');
      const data = JSON.parse(coverage);

      github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body: `## Test Results

        | Metric | Coverage |
        |--------|----------|
        | Lines | ${data.total.lines.pct}% |
        | Functions | ${data.total.functions.pct}% |
        | Branches | ${data.total.branches.pct}% |
        `
      });
```

### Branch Protection Rules

```yaml
# Configure via GitHub UI or API
required_status_checks:
  strict: true
  contexts:
    - "Lint & Type Check"
    - "Unit Tests"
    - "Integration Tests"
```

## Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vitest Documentation](https://vitest.dev/)
- [Mistral AI API Reference](https://docs.mistral.ai/api/)

## Next Steps
For deployment patterns, see `mistral-deploy-integration`.
