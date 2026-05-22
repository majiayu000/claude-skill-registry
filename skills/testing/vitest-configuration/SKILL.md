---
name: vitest-configuration
description: Use when vitest configuration, Vite integration, workspace setup, and test environment configuration for modern testing.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Vitest Configuration

Master Vitest configuration, Vite integration, workspace setup, and test environment configuration for modern testing. This skill covers comprehensive configuration strategies for Vitest, the blazing-fast unit test framework powered by Vite.

## Installation and Setup

### Basic Installation

```bash
npm install -D vitest
# or
yarn add -D vitest
# or
pnpm add -D vitest
```

### Additional Packages

```bash
# UI for vitest
npm install -D @vitest/ui

# Browser mode
npm install -D @vitest/browser playwright

# Coverage
npm install -D @vitest/coverage-v8
# or
npm install -D @vitest/coverage-istanbul
```

## Configuration Files

### vitest.config.ts (Recommended)

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Test environment
    environment: 'node', // 'node' | 'jsdom' | 'happy-dom' | 'edge-runtime'

    // Global test files
    globals: true,
    setupFiles: ['./vitest.setup.ts'],

    // Include/exclude patterns
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],

    // Coverage configuration
    coverage: {
      provider: 'v8', // 'v8' | 'istanbul'
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{js,ts,jsx,tsx}'],
      exclude: [
        'node_modules/',
        'src/**/*.test.{js,ts,jsx,tsx}',
        'src/**/*.spec.{js,ts,jsx,tsx}',
        'src/**/__tests__/**'
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    },

    // Performance
    pool: 'threads', // 'threads' | 'forks' | 'vmThreads'
    poolOptions: {
      threads: {
        singleThread: false,
        minThreads: 1,
        maxThreads: 4
      }
    },

    // Timeouts
    testTimeout: 10000,
    hookTimeout: 10000,

    // Watch options
    watch: false,
    watchExclude: ['**/node_modules/**', '**/dist/**'],

    // Reporters
    reporters: ['default'],

    // Mock options
    mockReset: true,
    restoreMocks: true,
    clearMocks: true
  }
});
```

### Extending Vite Config

```typescript
import { defineConfig, mergeConfig } from 'vitest/config';
import viteConfig from './vite.config';

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      // Vitest-specific configuration
    }
  })
);
```

### Workspace Configuration

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  // Multiple projects
  {
    extends: './vitest.config.ts',
    test: {
      name: 'unit',
      include: ['src/**/*.test.ts'],
      environment: 'node'
    }
  },
  {
    extends: './vitest.config.ts',
    test: {
      name: 'browser',
      include: ['src/**/*.browser.test.ts'],
      environment: 'jsdom'
    }
  },
  {
    extends: './vitest.config.ts',
    test: {
      name: 'integration',
      include: ['tests/integration/**/*.test.ts'],
      environment: 'node'
    }
  }
]);
```

## Environment Configuration

### Node Environment

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'node',
    environmentOptions: {
      // Node-specific options
    }
  }
});
```

### JSDOM Environment

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom',
    environmentOptions: {
      jsdom: {
        resources: 'usable',
        url: 'http://localhost:3000'
      }
    }
  }
});
```

### Happy DOM Environment

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'happy-dom',
    environmentOptions: {
      happyDOM: {
        width: 1024,
        height: 768
      }
    }
  }
});
```

### Custom Environment

```typescript
// custom-environment.ts
import type { Environment } from 'vitest';

export default <Environment>{
  name: 'custom',
  transformMode: 'ssr',
  setup() {
    // Setup custom environment
    return {
      teardown() {
        // Cleanup
      }
    };
  }
};

// vitest.config.ts
export default defineConfig({
  test: {
    environment: './custom-environment.ts'
  }
});
```

## Setup Files

### vitest.setup.ts

```typescript
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock global objects
global.fetch = vi.fn();

// Setup global test utilities
global.testUtils = {
  // Custom test utilities
};

// Configure test environment
beforeAll(() => {
  // Global setup
});

afterAll(() => {
  // Global teardown
});
```

### Setup for React Testing

```typescript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
});
```

## Coverage Configuration

### V8 Provider

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      include: ['src/**/*.ts'],
      exclude: [
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/types/**',
        '**/*.d.ts'
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
        perFile: true
      },
      all: true,
      clean: true,
      cleanOnRerun: true
    }
  }
});
```

### Istanbul Provider

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'istanbul',
      reporter: ['text', 'json', 'html'],
      watermarks: {
        lines: [80, 95],
        functions: [80, 95],
        branches: [80, 95],
        statements: [80, 95]
      }
    }
  }
});
```

## Module Resolution

### Path Aliases

```typescript
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services')
    }
  },
  test: {
    // Test configuration
  }
});
```

### External Dependencies

```typescript
export default defineConfig({
  test: {
    // Don't externalize these packages
    deps: {
      inline: ['package-to-inline']
    },
    // Externalize these packages
    server: {
      deps: {
        external: ['package-to-external']
      }
    }
  }
});
```

## Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest watch",
    "test:ci": "vitest run --coverage --reporter=json --reporter=default"
  }
}
```

## Advanced Configuration

### Browser Mode

```typescript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      name: 'chrome', // 'chrome' | 'firefox' | 'safari'
      provider: 'playwright', // 'playwright' | 'webdriverio'
      headless: true,
      screenshotFailures: true
    }
  }
});
```

### Performance Optimization

```typescript
export default defineConfig({
  test: {
    // Use threads for parallel execution
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
        minThreads: 1,
        maxThreads: 4,
        useAtomics: true
      }
    },

    // Isolate tests
    isolate: true,

    // Sequence tests
    sequence: {
      shuffle: false,
      concurrent: false
    },

    // File parallelism
    fileParallelism: true,

    // Max concurrency
    maxConcurrency: 5,

    // Bail on failure
    bail: 1
  }
});
```

### Type Checking

```typescript
export default defineConfig({
  test: {
    typecheck: {
      enabled: true,
      checker: 'tsc', // 'tsc' | 'vue-tsc'
      tsconfig: './tsconfig.json',
      include: ['**/*.{test,spec}-d.ts']
    }
  }
});
```

## Best Practices

1. **Use TypeScript configuration** - Leverage type safety in configuration files
2. **Configure appropriate environments** - Choose the right environment for your tests (node vs jsdom)
3. **Set up coverage thresholds** - Define realistic coverage goals
4. **Use workspace for monorepos** - Leverage workspace config for multiple projects
5. **Configure path aliases** - Match your application's import paths
6. **Optimize thread usage** - Balance parallelism with system resources
7. **Use globals sparingly** - Prefer explicit imports for better tree-shaking
8. **Configure appropriate timeouts** - Set realistic timeouts for async operations
9. **Enable coverage reporting** - Track test coverage consistently
10. **Use setup files effectively** - Centralize common setup logic

## Common Pitfalls

1. **Incorrect environment selection** - Using wrong environment causes undefined errors
2. **Missing path aliases** - Forgetting to configure aliases from vite.config
3. **Overly aggressive coverage thresholds** - Unrealistic goals discourage testing
4. **Not configuring globals** - Leads to verbose imports in every test file
5. **Incorrect thread configuration** - Too many threads overwhelm system
6. **Missing setup files** - Repetitive boilerplate in every test
7. **Wrong coverage provider** - V8 vs Istanbul have different capabilities
8. **Not cleaning mocks** - Shared mock state causes flaky tests
9. **Ignoring watch exclude** - Unnecessary file watching slows development
10. **Misconfigured module resolution** - Import errors in test files

## When to Use This Skill

- Setting up Vitest in a new Vite project
- Migrating from Jest to Vitest
- Configuring Vitest for TypeScript projects
- Setting up testing in monorepos with workspaces
- Optimizing test performance for large codebases
- Configuring browser testing with Playwright
- Setting up coverage reporting for CI/CD
- Debugging module resolution issues
- Implementing custom test environments
- Configuring type checking for tests
