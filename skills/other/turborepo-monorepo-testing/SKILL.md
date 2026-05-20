---
name: "Turborepo Monorepo Testing"
description: "Testing patterns for Turborepo and pnpm monorepos covering workspace dependency testing, affected package detection, parallel test execution, and shared test utilities"
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [turborepo, monorepo, pnpm, workspace, parallel-testing, affected, caching, ci-cd, turbo-pipeline, shared-utils]
testingTypes: [unit, integration, e2e]
frameworks: [vitest, playwright, jest]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Turborepo Monorepo Testing Skill

You are an expert QA engineer specializing in testing Turborepo and pnpm monorepo projects. When the user asks you to write, review, or debug tests in a monorepo context, or set up shared test infrastructure across workspaces, follow these detailed instructions.

## Core Principles

1. **Workspace isolation** -- Each package should have self-contained tests that can run independently. Never rely on implicit dependencies between workspaces during test execution.
2. **Affected-only testing** -- Use Turbo's dependency graph to only run tests for packages affected by a change. Avoid running the full test suite on every commit.
3. **Shared test utilities** -- Extract common test helpers, fixtures, and mocks into a dedicated shared test package to avoid duplication across workspaces.
4. **Cache-aware test pipelines** -- Configure Turbo pipelines so test results are cached based on source inputs. A package whose code has not changed should never re-run its tests.
5. **Parallel by default** -- Run workspace tests in parallel via Turbo's task orchestration. Only serialize tests that have true resource conflicts like shared databases.
6. **Cross-package integration testing** -- Validate that packages work together correctly with dedicated integration tests that import from multiple workspaces.
7. **Consistent configuration** -- Use shared Vitest/Jest configs at the root to ensure all packages follow the same test conventions, coverage thresholds, and reporter settings.

## Project Structure

Always organize monorepo testing with this structure:

```
my-monorepo/
  turbo.json
  vitest.workspace.ts
  pnpm-workspace.yaml
  packages/
    shared/
      src/
        index.ts
        utils/
      __tests__/
        utils.test.ts
      vitest.config.ts
      package.json
    web/
      src/
        app/
        components/
      __tests__/
        unit/
        integration/
      e2e/
        home.spec.ts
      vitest.config.ts
      playwright.config.ts
      package.json
    api/
      src/
        routes/
        services/
      __tests__/
        unit/
        integration/
      vitest.config.ts
      package.json
    test-utils/
      src/
        fixtures/
          user.fixture.ts
          product.fixture.ts
        mocks/
          api-client.mock.ts
          database.mock.ts
        helpers/
          render.tsx
          setup-server.ts
        index.ts
      package.json
    config/
      vitest/
        base.config.ts
        react.config.ts
        node.config.ts
      tsconfig/
        base.json
        react.json
        node.json
      package.json
```

## Turbo Pipeline Configuration

### turbo.json with Test Pipelines

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "globalEnv": ["NODE_ENV", "CI"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "inputs": [
        "src/**",
        "__tests__/**",
        "vitest.config.*",
        "tsconfig.json"
      ],
      "env": ["DATABASE_URL", "TEST_DATABASE_URL"]
    },
    "test:unit": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "inputs": [
        "src/**",
        "__tests__/unit/**",
        "vitest.config.*"
      ]
    },
    "test:integration": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "inputs": [
        "src/**",
        "__tests__/integration/**",
        "vitest.config.*"
      ],
      "env": ["DATABASE_URL", "TEST_DATABASE_URL"]
    },
    "test:e2e": {
      "dependsOn": ["^build", "build"],
      "outputs": ["test-results/**", "playwright-report/**"],
      "inputs": [
        "e2e/**",
        "playwright.config.*",
        "src/**"
      ]
    },
    "lint": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**",
        "__tests__/**",
        "e2e/**",
        ".eslintrc.*",
        "eslint.config.*"
      ]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**",
        "__tests__/**",
        "tsconfig.json"
      ]
    }
  }
}
```

### Vitest Workspace Configuration

```typescript
// vitest.workspace.ts (root)
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/shared/vitest.config.ts',
  'packages/web/vitest.config.ts',
  'packages/api/vitest.config.ts',
]);
```

### Shared Base Vitest Config

```typescript
// packages/config/vitest/base.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    clearMocks: true,
    restoreMocks: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/index.ts',
        '**/__tests__/**',
        '**/test-utils/**',
      ],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
    reporters: process.env.CI
      ? ['default', 'junit']
      : ['default'],
    outputFile: process.env.CI
      ? { junit: './test-results/junit.xml' }
      : undefined,
  },
});
```

### Package-Level Vitest Config

```typescript
// packages/api/vitest.config.ts
import { defineConfig, mergeConfig } from 'vitest/config';
import baseConfig from '@repo/config/vitest/base.config';

export default mergeConfig(
  baseConfig,
  defineConfig({
    test: {
      environment: 'node',
      include: ['__tests__/**/*.test.ts'],
      setupFiles: ['__tests__/setup.ts'],
      testTimeout: 10000,
      pool: 'forks',
      poolOptions: {
        forks: {
          singleFork: false,
        },
      },
    },
  })
);
```

```typescript
// packages/web/vitest.config.ts
import { defineConfig, mergeConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import baseConfig from '@repo/config/vitest/base.config';

export default mergeConfig(
  baseConfig,
  defineConfig({
    plugins: [react()],
    test: {
      environment: 'jsdom',
      include: ['__tests__/**/*.test.{ts,tsx}'],
      setupFiles: ['__tests__/setup.ts'],
      css: true,
    },
  })
);
```

## Shared Test Utilities Package

### Package Configuration

```json
{
  "name": "@repo/test-utils",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./fixtures": "./src/fixtures/index.ts",
    "./mocks": "./src/mocks/index.ts",
    "./helpers": "./src/helpers/index.ts"
  },
  "dependencies": {
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "msw": "^2.0.0"
  },
  "peerDependencies": {
    "vitest": "^2.0.0"
  }
}
```

### Shared Fixtures

```typescript
// packages/test-utils/src/fixtures/user.fixture.ts
import { faker } from '@faker-js/faker';

export interface TestUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'editor';
  createdAt: Date;
}

export function createTestUser(overrides: Partial<TestUser> = {}): TestUser {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    createdAt: faker.date.recent(),
    ...overrides,
  };
}

export function createTestUsers(count: number, overrides: Partial<TestUser> = {}): TestUser[] {
  return Array.from({ length: count }, () => createTestUser(overrides));
}

export const adminUser = createTestUser({ role: 'admin', email: 'admin@test.com' });
export const regularUser = createTestUser({ role: 'user', email: 'user@test.com' });
```

```typescript
// packages/test-utils/src/fixtures/product.fixture.ts
import { faker } from '@faker-js/faker';

export interface TestProduct {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

export function createTestProduct(overrides: Partial<TestProduct> = {}): TestProduct {
  return {
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 1, max: 500 })),
    category: faker.commerce.department(),
    inStock: true,
    ...overrides,
  };
}
```

### Shared Mock Utilities

```typescript
// packages/test-utils/src/mocks/api-client.mock.ts
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { createTestUser, createTestProduct } from '../fixtures';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json({
      users: [createTestUser(), createTestUser()],
      total: 2,
    });
  }),

  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json(
      createTestUser({ id: params.id as string })
    );
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>;
    return HttpResponse.json(
      createTestUser(body),
      { status: 201 }
    );
  }),

  http.get('/api/products', () => {
    return HttpResponse.json({
      products: [createTestProduct(), createTestProduct()],
      total: 2,
    });
  }),
];

export const server = setupServer(...handlers);

export function setupMockServer() {
  beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());
}
```

### Shared React Testing Helpers

```typescript
// packages/test-utils/src/helpers/render.tsx
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Add your app-wide providers here
function AllProviders({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
    </>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  const user = userEvent.setup();
  return {
    user,
    ...render(ui, { wrapper: AllProviders, ...options }),
  };
}

export { render, screen, waitFor, within } from '@testing-library/react';
export { userEvent };
```

## Affected Package Testing

### Running Tests Only for Changed Packages

```bash
# Run tests only for packages affected by changes since main
pnpm turbo test --filter=...[origin/main]

# Run tests for a specific package and its dependents
pnpm turbo test --filter=@repo/shared...

# Run tests for packages affected by changes in the last commit
pnpm turbo test --filter=...[HEAD~1]

# Dry run to see what would be tested
pnpm turbo test --filter=...[origin/main] --dry-run
```

### CI Script for Affected Testing

```typescript
// scripts/run-affected-tests.ts
import { execSync } from 'child_process';

function getAffectedPackages(): string[] {
  const baseBranch = process.env.BASE_BRANCH || 'origin/main';

  try {
    const output = execSync(
      `pnpm turbo test --filter=...[${baseBranch}] --dry-run=json`,
      { encoding: 'utf-8' }
    );

    const result = JSON.parse(output);
    return result.packages || [];
  } catch {
    console.warn('Could not determine affected packages, running all tests');
    return ['*'];
  }
}

function runAffectedTests(): void {
  const affected = getAffectedPackages();

  if (affected.length === 0) {
    console.log('No packages affected, skipping tests');
    process.exit(0);
  }

  console.log(`Running tests for affected packages: ${affected.join(', ')}`);

  const filterArgs = affected
    .map((pkg) => `--filter=${pkg}`)
    .join(' ');

  try {
    execSync(`pnpm turbo test ${filterArgs}`, {
      stdio: 'inherit',
    });
  } catch {
    process.exit(1);
  }
}

runAffectedTests();
```

## Cross-Package Integration Testing

### Integration Test for Shared + API

```typescript
// packages/api/__tests__/integration/shared-integration.test.ts
import { describe, it, expect, beforeAll } from 'vitest';
import { parseSkillMd, serializeSkillMd } from '@repo/shared';
import { SkillService } from '../../src/services/skill-service';
import { createTestDatabase, cleanupDatabase } from '@repo/test-utils/helpers';

describe('Shared + API Integration', () => {
  let db: ReturnType<typeof createTestDatabase>;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await cleanupDatabase(db);
  });

  it('should parse SKILL.md and store in database via service', async () => {
    const markdown = `---
name: "Test Skill"
description: "A test skill for integration testing"
version: 1.0.0
author: test
tags: [testing]
testingTypes: [unit]
frameworks: [vitest]
languages: [typescript]
domains: [web]
agents: [claude-code]
---

# Test Skill

This is a test skill body.
`;

    // Uses @repo/shared parser
    const parsed = parseSkillMd(markdown);
    expect(parsed.frontmatter.name).toBe('Test Skill');

    // Uses API service to store
    const service = new SkillService(db);
    const stored = await service.createSkill(parsed);

    expect(stored.id).toBeDefined();
    expect(stored.name).toBe('Test Skill');

    // Round-trip: retrieve and serialize back
    const retrieved = await service.getSkill(stored.id);
    const serialized = serializeSkillMd(retrieved);

    expect(serialized).toContain('name: "Test Skill"');
    expect(serialized).toContain('# Test Skill');
  });

  it('should validate shared types are compatible with API endpoints', async () => {
    const service = new SkillService(db);

    const skills = await service.listSkills({
      testingTypes: ['unit'],
      languages: ['typescript'],
      page: 1,
      limit: 10,
    });

    // Verify the response matches the shared SkillSummary type
    for (const skill of skills.items) {
      expect(skill).toHaveProperty('id');
      expect(skill).toHaveProperty('name');
      expect(skill).toHaveProperty('description');
      expect(skill).toHaveProperty('version');
      expect(Array.isArray(skill.tags)).toBe(true);
      expect(Array.isArray(skill.testingTypes)).toBe(true);
    }
  });
});
```

### Integration Test for Web + API

```typescript
// packages/web/__tests__/integration/api-integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createTestUser, createTestProduct } from '@repo/test-utils/fixtures';
import { server } from '@repo/test-utils/mocks';

describe('Web + API Integration', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());

  it('should fetch and transform API data for UI rendering', async () => {
    const response = await fetch('/api/users');
    const data = await response.json();

    expect(data.users).toHaveLength(2);
    expect(data.users[0]).toHaveProperty('name');
    expect(data.users[0]).toHaveProperty('email');
  });

  it('should handle API error responses gracefully', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { error: 'Internal Server Error' },
          { status: 500 }
        );
      })
    );

    const response = await fetch('/api/users');
    expect(response.status).toBe(500);

    const data = await response.json();
    expect(data.error).toBe('Internal Server Error');
  });
});
```

## E2E Testing in a Monorepo

### Playwright Config with Monorepo Awareness

```typescript
// packages/web/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: path.join(__dirname, 'playwright-report') }],
    process.env.CI ? ['github'] : ['list'],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
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
      name: 'mobile-chrome',
      use: { ...devices['Pixel 7'] },
    },
  ],
  webServer: {
    command: 'pnpm turbo build --filter=@repo/web && pnpm turbo start --filter=@repo/web',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

## CI Configuration with Turbo Cache

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20]

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for affected detection

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # Turbo remote cache
      - name: Configure Turbo cache
        uses: actions/cache@v4
        with:
          path: node_modules/.cache/turbo
          key: turbo-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-${{ github.sha }}
          restore-keys: |
            turbo-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-
            turbo-${{ runner.os }}-

      # Run only affected unit and integration tests
      - name: Run affected tests
        run: pnpm turbo test:unit test:integration --filter=...[origin/main]

      # Always run full lint
      - name: Lint
        run: pnpm turbo lint

      # Type checking
      - name: Type check
        run: pnpm turbo typecheck

      # Upload coverage from all packages
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-reports
          path: packages/*/coverage/

  e2e:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright browsers
        run: pnpm --filter @repo/web exec playwright install --with-deps

      - name: Build all packages
        run: pnpm turbo build

      - name: Run E2E tests
        run: pnpm turbo test:e2e

      - name: Upload E2E report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: packages/web/playwright-report/
```

## Package Scripts Configuration

### Root package.json Scripts

```json
{
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "test": "turbo test",
    "test:unit": "turbo test:unit",
    "test:integration": "turbo test:integration",
    "test:e2e": "turbo test:e2e",
    "test:affected": "turbo test --filter=...[origin/main]",
    "test:watch": "vitest --workspace=vitest.workspace.ts",
    "test:coverage": "turbo test -- --coverage",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "clean": "turbo clean && rm -rf node_modules"
  }
}
```

### Individual Package Scripts

```json
{
  "name": "@repo/api",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsup src/index.ts",
    "test": "vitest run",
    "test:unit": "vitest run __tests__/unit",
    "test:integration": "vitest run __tests__/integration",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src __tests__",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf dist coverage"
  }
}
```

## Workspace Dependency Testing

### Verifying Internal Dependencies Resolve Correctly

```typescript
// packages/api/__tests__/unit/dependencies.test.ts
import { describe, it, expect } from 'vitest';

describe('Workspace Dependency Resolution', () => {
  it('should import shared types correctly', async () => {
    const shared = await import('@repo/shared');

    expect(shared).toHaveProperty('parseSkillMd');
    expect(shared).toHaveProperty('serializeSkillMd');
    expect(typeof shared.parseSkillMd).toBe('function');
  });

  it('should import test-utils fixtures', async () => {
    const { createTestUser } = await import('@repo/test-utils/fixtures');

    const user = createTestUser();
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('email');
    expect(user).toHaveProperty('name');
  });

  it('should verify shared constants are accessible', async () => {
    const { AGENTS, CATEGORIES } = await import('@repo/shared');

    expect(Array.isArray(AGENTS)).toBe(true);
    expect(AGENTS.length).toBeGreaterThan(0);
    expect(Array.isArray(CATEGORIES)).toBe(true);
  });

  it('should verify shared schemas validate correctly', async () => {
    const { skillFrontmatterSchema } = await import('@repo/shared');

    const validData = {
      name: 'Test Skill',
      description: 'A valid description that is long enough',
      version: '1.0.0',
      author: 'test',
      tags: ['testing'],
      testingTypes: ['unit'],
      frameworks: ['vitest'],
      languages: ['typescript'],
      domains: ['web'],
      agents: ['claude-code'],
    };

    const result = skillFrontmatterSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });
});
```

### Testing Build Output Compatibility

```typescript
// scripts/verify-build-outputs.test.ts
import { describe, it, expect } from 'vitest';
import { existsSync, readFileSync } from 'fs';
import path from 'path';

describe('Build Output Verification', () => {
  const packages = ['shared', 'cli', 'sdk', 'api'];

  for (const pkg of packages) {
    const distPath = path.join(__dirname, '..', 'packages', pkg, 'dist');

    it(`${pkg}: dist directory should exist after build`, () => {
      expect(existsSync(distPath)).toBe(true);
    });

    it(`${pkg}: should have a valid entry point`, () => {
      const pkgJsonPath = path.join(__dirname, '..', 'packages', pkg, 'package.json');
      const pkgJson = JSON.parse(readFileSync(pkgJsonPath, 'utf-8'));

      const mainEntry = pkgJson.main || pkgJson.exports?.['.'];
      expect(mainEntry).toBeDefined();

      const resolvedEntry = path.join(__dirname, '..', 'packages', pkg, mainEntry);
      expect(existsSync(resolvedEntry)).toBe(true);
    });

    it(`${pkg}: TypeScript declarations should be present`, () => {
      const dtsFiles = require('fast-glob').sync('**/*.d.ts', { cwd: distPath });
      expect(dtsFiles.length).toBeGreaterThan(0);
    });
  }
});
```

## Test Database Management for Integration Tests

```typescript
// packages/test-utils/src/helpers/setup-database.ts
import { execSync } from 'child_process';
import { randomUUID } from 'crypto';

interface TestDatabaseConfig {
  connectionString: string;
  databaseName: string;
  cleanup: () => Promise<void>;
}

export async function createTestDatabase(): Promise<TestDatabaseConfig> {
  const baseName = 'test_db';
  const databaseName = `${baseName}_${randomUUID().slice(0, 8)}`;
  const baseUrl = process.env.TEST_DATABASE_URL || 'postgresql://localhost:5432';

  // Create isolated test database
  execSync(`createdb ${databaseName}`, {
    env: { ...process.env, PGHOST: 'localhost' },
  });

  const connectionString = `${baseUrl}/${databaseName}`;

  // Run migrations
  execSync('pnpm drizzle-kit push', {
    env: { ...process.env, DATABASE_URL: connectionString },
    cwd: process.cwd(),
  });

  return {
    connectionString,
    databaseName,
    cleanup: async () => {
      execSync(`dropdb --if-exists ${databaseName}`, {
        env: { ...process.env, PGHOST: 'localhost' },
      });
    },
  };
}
```

## Parallel Test Execution Strategies

```typescript
// packages/api/__tests__/setup.ts
import { beforeAll, afterAll } from 'vitest';
import { server } from '@repo/test-utils/mocks';

// Each worker gets its own mock server
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'warn' });
});

afterAll(() => {
  server.close();
});
```

```typescript
// vitest.config.ts with parallel configuration
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Run test files in parallel (default)
    fileParallelism: true,

    // Each test file runs in its own worker thread
    pool: 'threads',
    poolOptions: {
      threads: {
        // Match CPU core count for optimal parallelism
        minThreads: 1,
        maxThreads: process.env.CI ? 4 : undefined,
      },
    },

    // Isolate each test file to prevent state leakage
    isolate: true,

    // Sequence configuration for deterministic order when needed
    sequence: {
      shuffle: true, // Randomize to detect order dependencies
    },
  },
});
```

## Coverage Aggregation Across Packages

```typescript
// scripts/merge-coverage.ts
import { execSync } from 'child_process';
import { existsSync, mkdirSync } from 'fs';
import path from 'path';

const rootDir = path.resolve(__dirname, '..');
const mergedDir = path.join(rootDir, 'coverage-merged');

if (!existsSync(mergedDir)) {
  mkdirSync(mergedDir, { recursive: true });
}

const packages = ['shared', 'web', 'api', 'cli', 'sdk'];

// Collect all coverage JSON files
const coverageFiles = packages
  .map((pkg) => path.join(rootDir, 'packages', pkg, 'coverage', 'coverage-final.json'))
  .filter((f) => existsSync(f));

if (coverageFiles.length === 0) {
  console.log('No coverage files found. Run tests with coverage first.');
  process.exit(0);
}

// Merge using nyc
const fileArgs = coverageFiles.map((f) => `--include="${f}"`).join(' ');
execSync(
  `npx nyc merge ${coverageFiles.map((f) => path.dirname(f)).join(' ')} ${mergedDir}/coverage.json`,
  { stdio: 'inherit' }
);

// Generate merged report
execSync(
  `npx nyc report --temp-dir=${mergedDir} --reporter=text --reporter=html --report-dir=${mergedDir}/html`,
  { stdio: 'inherit' }
);

console.log(`Merged coverage report generated at ${mergedDir}/html/index.html`);
```

## Best Practices

1. **Define explicit test inputs in turbo.json** -- Always list the `inputs` array for test tasks so Turbo can compute hashes correctly. Missing inputs cause stale cache hits.
2. **Use workspace protocol for internal dependencies** -- Use `"@repo/shared": "workspace:*"` in package.json to ensure pnpm links internal packages instead of fetching from npm.
3. **Create a dedicated test-utils package** -- Extract shared fixtures, mocks, and helpers into `@repo/test-utils` instead of duplicating across packages.
4. **Run affected tests in CI, full suite on main** -- Use `--filter=...[origin/main]` on PRs but run the full `pnpm turbo test` on main branch merges.
5. **Cache test results in CI** -- Store and restore `node_modules/.cache/turbo` between CI runs. Turbo will skip unchanged packages.
6. **Isolate integration tests with separate databases** -- Each integration test suite should create and destroy its own test database to enable parallel execution.
7. **Use Vitest workspace mode for development** -- Run `vitest --workspace=vitest.workspace.ts` in watch mode during development to get instant feedback across all packages.
8. **Set coverage thresholds per package** -- Different packages have different test priorities. Set appropriate thresholds in each package's vitest config rather than one global number.
9. **Type-check as a separate pipeline task** -- Run `tsc --noEmit` as a separate Turbo task (`typecheck`) instead of bundling it with tests. It catches different classes of errors.
10. **Pin exact versions of shared dev dependencies** -- Use the same versions of vitest, typescript, and eslint across all packages via a root `pnpm-workspace.yaml` catalog or `syncpack`.

## Anti-Patterns to Avoid

1. **Running all tests on every change** -- Without `--filter`, Turbo runs every package's tests. Always use affected detection for PRs.
2. **Importing from package dist instead of source** -- In a monorepo, internal packages should resolve to source (via `main: ./src/index.ts`), not compiled output, during development and testing.
3. **Sharing mutable test state across packages** -- Global test state that leaks across workspace boundaries causes flaky and order-dependent tests.
4. **Missing `dependsOn: ["^build"]` for test tasks** -- If test tasks don't depend on upstream builds, shared package changes won't be picked up, causing false positives.
5. **Duplicating test configuration in every package** -- Maintain base configs in a shared config package and use `mergeConfig` to extend per-package.
6. **Not specifying `inputs` for Turbo tasks** -- Without explicit inputs, Turbo hashes all files, causing unnecessary cache invalidation.
7. **Using a single global vitest config** -- A root-level vitest config without workspace mode runs all tests in a single process, losing parallelism benefits.
8. **Ignoring workspace dependency graph in E2E tests** -- E2E tests for the web app must `dependsOn: ["build"]` for the web package plus `["^build"]` for all dependencies.
9. **Hardcoding package paths in test scripts** -- Use workspace references (`@repo/shared`) instead of relative paths (`../../shared/src`) to avoid breakage when packages move.
10. **Not cleaning Turbo cache periodically** -- Stale cache entries accumulate over time. Add a `clean` script that removes `node_modules/.cache/turbo` and run it when debugging mysterious test failures.

## Running Tests

- Run all tests: `pnpm turbo test`
- Run affected tests: `pnpm turbo test --filter=...[origin/main]`
- Run tests for one package: `pnpm turbo test --filter=@repo/api`
- Run tests for a package and dependents: `pnpm turbo test --filter=@repo/shared...`
- Watch mode across workspace: `pnpm vitest --workspace=vitest.workspace.ts`
- View Turbo task graph: `pnpm turbo test --graph`
- Check cache status: `pnpm turbo test --dry-run`
- Force re-run (skip cache): `pnpm turbo test --force`
