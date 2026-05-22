---
name: playwright-bdd-configuration
description: Use when configuring Playwright BDD projects, setting up defineBddConfig(), configuring feature and step file paths, and integrating with Playwright config.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Playwright BDD Configuration

Expert knowledge of Playwright BDD configuration, project setup, and integration with Playwright's testing framework for behavior-driven development.

## Overview

Playwright BDD enables running Gherkin-syntax BDD tests with Playwright Test. Configuration is done through the `playwright.config.ts` file using the `defineBddConfig()` function, which generates Playwright test files from your `.feature` files.

## Installation

```bash
# Install playwright-bdd
npm install -D playwright-bdd

# Or with specific Playwright version
npm install -D playwright-bdd @playwright/test
```

## Basic Configuration

### Minimal Setup

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
});

export default defineConfig({
  testDir,
});
```

### Generated Test Directory

The `defineBddConfig()` function returns a path to the generated test directory. By default, this is `.features-gen` in your project root:

```typescript
const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
});

// testDir = '.features-gen/features'
```

### Custom Output Directory

```typescript
const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  outputDir: '.generated-tests', // Custom output directory
});
```

## Configuration Options

### Feature Files

Configure where to find feature files:

```typescript
defineBddConfig({
  // Single pattern
  features: 'features/**/*.feature',

  // Multiple patterns
  features: [
    'features/**/*.feature',
    'specs/**/*.feature',
  ],

  // Exclude patterns
  features: {
    include: 'features/**/*.feature',
    exclude: 'features/**/skip-*.feature',
  },
});
```

### Step Definitions

Configure step definition locations:

```typescript
defineBddConfig({
  // Single pattern
  steps: 'steps/**/*.ts',

  // Multiple patterns
  steps: [
    'steps/**/*.ts',
    'features/**/*.steps.ts',
  ],

  // Mixed JavaScript and TypeScript
  steps: [
    'steps/**/*.ts',
    'steps/**/*.js',
  ],
});
```

### Import Test Instance

When using custom fixtures, import the test instance:

```typescript
defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  importTestFrom: 'steps/fixtures.ts', // Path to your custom test instance
});
```

The fixtures file should export the test instance:

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';

export const test = base.extend<{
  todoPage: TodoPage;
}>({
  todoPage: async ({ page }, use) => {
    const todoPage = new TodoPage(page);
    await use(todoPage);
  },
});

export const { Given, When, Then } = createBdd(test);
```

## Advanced Configuration

### Multiple Feature Sets

Configure different feature sets for different test projects:

```typescript
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const coreTestDir = defineBddConfig({
  features: 'features/core/**/*.feature',
  steps: 'steps/core/**/*.ts',
  outputDir: '.features-gen/core',
});

const adminTestDir = defineBddConfig({
  features: 'features/admin/**/*.feature',
  steps: 'steps/admin/**/*.ts',
  outputDir: '.features-gen/admin',
});

export default defineConfig({
  projects: [
    {
      name: 'core',
      testDir: coreTestDir,
    },
    {
      name: 'admin',
      testDir: adminTestDir,
    },
  ],
});
```

### Language Configuration

Configure the Gherkin language:

```typescript
defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  language: 'de', // German keywords (Gegeben, Wenn, Dann)
});
```

Supported languages follow the Gherkin specification:

- `en` (English - default)
- `de` (German)
- `fr` (French)
- `es` (Spanish)
- `ru` (Russian)
- And many more...

### Quote Style

Configure quote style in generated test files:

```typescript
defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  quotes: 'single', // 'single' | 'double' | 'backtick'
});
```

### Verbose Mode

Enable verbose output during generation:

```typescript
defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  verbose: true,
});
```

## Integration with Playwright Config

### Full Configuration Example

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  importTestFrom: 'steps/fixtures.ts',
});

export default defineConfig({
  testDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
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
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Environment-Specific Configuration

```typescript
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const isCI = !!process.env.CI;

const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  verbose: !isCI,
});

export default defineConfig({
  testDir,
  timeout: isCI ? 60000 : 30000,
  retries: isCI ? 2 : 0,
  workers: isCI ? 4 : undefined,
});
```

## Running Tests

### Generate and Run

```bash
# Generate test files from features
npx bddgen

# Run Playwright tests
npx playwright test

# Or combine both
npx bddgen && npx playwright test
```

### Watch Mode

For development, regenerate on file changes:

```bash
# Watch feature and step files
npx bddgen --watch

# In another terminal, run tests
npx playwright test --watch
```

### Export Step Definitions

Export all step definitions for documentation:

```bash
npx bddgen export
```

## Directory Structure

Recommended project structure:

```
project/
├── playwright.config.ts
├── features/
│   ├── auth/
│   │   ├── login.feature
│   │   └── logout.feature
│   └── products/
│       └── catalog.feature
├── steps/
│   ├── auth/
│   │   ├── login.steps.ts
│   │   └── logout.steps.ts
│   ├── products/
│   │   └── catalog.steps.ts
│   └── fixtures.ts
└── .features-gen/          # Generated (gitignore this)
    └── features/
        ├── auth/
        │   ├── login.feature.spec.js
        │   └── logout.feature.spec.js
        └── products/
            └── catalog.feature.spec.js
```

### Gitignore Generated Files

Add to `.gitignore`:

```
# Playwright BDD generated files
.features-gen/
```

## Common Configuration Patterns

### Monorepo Setup

```typescript
// packages/e2e/playwright.config.ts
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const testDir = defineBddConfig({
  features: 'features/**/*.feature',
  steps: 'steps/**/*.ts',
  importTestFrom: 'steps/fixtures.ts',
});

export default defineConfig({
  testDir,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
  },
});
```

### Component Testing

```typescript
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const testDir = defineBddConfig({
  features: 'features/components/**/*.feature',
  steps: 'steps/components/**/*.ts',
});

export default defineConfig({
  testDir,
  use: {
    ctPort: 3100,
  },
});
```

### API Testing

```typescript
import { defineConfig } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const testDir = defineBddConfig({
  features: 'features/api/**/*.feature',
  steps: 'steps/api/**/*.ts',
});

export default defineConfig({
  testDir,
  use: {
    baseURL: 'https://api.example.com',
  },
});
```

## Troubleshooting

### Steps Not Found

If steps are not being matched:

1. Verify step patterns match your directory structure
2. Check for typos in step definition text
3. Ensure step files are included in the `steps` config
4. Run `npx bddgen export` to see all registered steps

### Import Errors

If imports fail in generated files:

1. Verify `importTestFrom` path is correct
2. Ensure the file exports `test` and step functions
3. Check TypeScript configuration includes step files

### Generation Errors

If `bddgen` fails:

1. Validate feature file syntax
2. Check for missing step definitions
3. Run with `verbose: true` for details
4. Verify all imports in step files

## Best Practices

1. **Organize by Feature** - Group features and steps by domain
2. **Use Fixtures** - Share setup logic via Playwright fixtures
3. **Keep Steps Simple** - One action per step definition
4. **Reuse Steps** - Write generic steps that work across features
5. **Version Generated Files** - Optionally commit for debugging
6. **CI Integration** - Run `bddgen` before tests in CI
7. **Type Safety** - Use TypeScript for step definitions
8. **Documentation** - Export steps for team reference
9. **Parallel Execution** - Let Playwright handle parallelism
10. **Clean Output** - Gitignore generated directory

## When to Use This Skill

- Setting up a new Playwright BDD project
- Configuring multiple feature sets
- Integrating custom fixtures with BDD
- Troubleshooting configuration issues
- Optimizing test generation
- Setting up monorepo testing
- Configuring language/i18n support
