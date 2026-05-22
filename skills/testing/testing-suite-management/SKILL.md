---
name: testing-suite-management
description: Manage comprehensive testing strategy across unit, E2E, and mutation testing
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for testing-related tasks:
  - Creating new test files following project patterns
  - Updating test configurations for new modules
  - Running specific test suites with proper configs
  - Generating coverage reports and ensuring thresholds
  - Setting up CI/CD test pipelines
  
  Examples:
  "Create tests for new utility using the testing-suite-management skill"
  "Update test configuration using the testing-suite-management skill"
  "Set up E2E tests for new feature using the testing-suite-management skill"

# Testing Suite Management Skill

## Overview

This skill automates the comprehensive testing strategy used in Saberloop, covering Vitest unit tests, Playwright E2E tests, and Stryker mutation testing with proper configuration and reporting.

## Testing Stack Overview

| Tool | Purpose | Config File | Coverage Target |
|-------|----------|--------------|-----------------|
| Vitest | Unit testing | `vitest.config.js` | >90% |
| Playwright | E2E testing | `playwright.config.js` | Critical paths |
| Stryker | Mutation testing | `stryker.config.json` | >75% |
| Dependency Cruiser | Architecture testing | `.dependency-cruiser.cjs` | Zero violations |

## When to Use This Skill

Use this skill when ANY of these are true:
- [ ] Creating new module/service/utility
- [ ] Adding new views or components
- [ ] Updating test configurations
- [ ] Setting up CI/CD test pipelines
- [ ] Analyzing test coverage or quality
- [ ] Debugging test failures

## Test File Patterns

### Unit Test Structure

**File Location:** Co-located with source file
**Naming:** `filename.test.js`
**Framework:** Vitest with jsdom environment

```javascript
// src/utils/example.test.js
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { exampleFunction } from './example.js';

describe('Example Module', () => {
  beforeEach(() => {
    // Setup before each test
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Cleanup after each test
  });

  describe('exampleFunction', () => {
    it('should return correct result for valid input', () => {
      const result = exampleFunction('valid input');
      expect(result).toBe('expected output');
    });

    it('should handle edge cases', () => {
      expect(() => exampleFunction(null)).toThrow('Invalid input');
    });

    it('should work with different data types', () => {
      expect(exampleFunction(123)).toBe('number result');
      expect(exampleFunction('string')).toBe('string result');
    });
  });
});
```

### E2E Test Structure

**File Location:** `tests/e2e/`
**Naming:** `feature-description.spec.js`
**Framework:** Playwright with Chrome

```javascript
// tests/e2e/quiz-flow.spec.js
import { test, expect } from '@playwright/test';

test.describe('Quiz Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should complete quiz flow successfully', async ({ page }) => {
    // Navigate to quiz creation
    await page.click('[data-testid="start-quiz"]');
    
    // Fill topic
    await page.fill('[data-testid="topic-input"]', 'Science');
    await page.click('[data-testid="generate-quiz"]');
    
    // Wait for questions
    await expect(page.locator('[data-testid="question"]').first()).toBeVisible();
    
    // Answer questions
    const questions = await page.locator('[data-testid="question"]').all();
    for (const question of questions) {
      const firstAnswer = question.locator('[data-testid="answer"]').first();
      await firstAnswer.click();
    }
    
    // Submit and check results
    await page.click('[data-testid="submit-quiz"]');
    await expect(page.locator('[data-testid="results"]')).toBeVisible();
  });
});
```

## Configuration Templates

### Vitest Configuration

**File:** `vitest.config.js`

```javascript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Use jsdom to simulate browser environment
    environment: 'jsdom',

    // Enable global test functions
    globals: true,

    // Only include unit test files, exclude E2E tests
    include: ['**/*.test.js'],
    exclude: ['node_modules', 'dist', 'tests/e2e/**'],

    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '*.config.js',
        'sw.js',  // Service worker is hard to test in unit tests
        'tests/e2e/**'  // Exclude E2E from coverage
      ],
      thresholds: {
        global: {
          branches: 90,
          functions: 90,
          lines: 90,
          statements: 90
        }
      }
    }
  }
});
```

### Playwright Configuration

**File:** `playwright.config.js`

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 45000,
  retries: 1,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'on', // Record video for all tests
  },
  webServer: {
    command: 'npx cross-env VITE_USE_REAL_API=false vite --port 3000',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### Stryker Configuration

**File:** `stryker.config.json`

```javascript
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "_comment": "This config strykes JavaScript files for mutation testing",
  "packageManager": "npm",
  "reporters": [
    "html",
    "progress",
    "clear-text"
  ],
  "testRunner": "vitest",
  "coverageAnalysis": "off",
  "concurrency": 2,
  "mutate": [
    "src/utils/gradeProgression.js",
    "src/utils/shuffle.js",
    "src/utils/formatters.js"
  ],
  "timeoutMS": 60000,
  "tempDirName": ".stryker-tmp",
  "cleanTempDir": true,
  "types": {
    "javascript": {
      "mutator": "javascript"
    }
  }
}
```

## Test Creation Process

### Step 1: Analyze Code for Testing

```bash
# Find files without tests
find src -name "*.js" -not -name "*.test.js" | head -10

# Check current coverage
npm run test:coverage

# Identify mutation targets
npm run test:mutation
```

### Step 2: Create Unit Tests

#### Function Testing Template

```javascript
// For utility functions
describe('functionName', () => {
  describe('happy path', () => {
    it('should work with valid inputs', () => {
      const result = functionName(validInput, validOptions);
      expect(result).toEqual(expectedResult);
    });
  });

  describe('edge cases', () => {
    it('should handle null/undefined', () => {
      expect(() => functionName(null)).toThrow();
    });

    it('should handle empty inputs', () => {
      expect(functionName('')).toBe(defaultResult);
    });

    it('should handle boundary values', () => {
      expect(functionName(0)).toBe(minResult);
      expect(functionName(Number.MAX_VALUE)).toBe(maxResult);
    });
  });

  describe('error handling', () => {
    it('should throw specific error type', () => {
      expect(() => functionName(invalidInput)).toThrow('Specific error message');
    });
  });
});
```

#### Class Testing Template

```javascript
// For classes/services
describe('ClassName', () => {
  let instance;

  beforeEach(() => {
    instance = new ClassName(dependencies);
  });

  afterEach(() => {
    if (instance && typeof instance.destroy === 'function') {
      instance.destroy();
    }
  });

  describe('initialization', () => {
    it('should initialize with correct defaults', () => {
      expect(instance.property).toBe(defaultValue);
    });
  });

  describe('public methods', () => {
    it('should method name correctly', async () => {
      const result = await instance.methodName(parameters);
      expect(result).toBeDefined();
    });
  });

  describe('error handling', () => {
    it('should handle network failures', async () => {
      // Mock failure
      mockNetworkFailure();
      
      await expect(instance.methodName()).rejects.toThrow('Network error');
    });
  });
});
```

### Step 3: Create Integration Tests

```javascript
// Test interaction between modules
describe('Module Integration: Service + API', () => {
  beforeEach(async () => {
    // Setup test environment
    await setupTestDatabase();
    mockApiResponses();
  });

  afterEach(async () => {
    // Cleanup
    await cleanupTestDatabase();
    vi.clearAllMocks();
  });

  it('should successfully call API and save to database', async () => {
    const service = new TestService();
    
    const result = await service.createQuiz('Test Topic');
    
    expect(result).toBeDefined();
    expect(result.topic).toBe('Test Topic');
    
    // Verify database state
    const saved = await getQuizFromDatabase(result.id);
    expect(saved.topic).toBe('Test Topic');
  });
});
```

### Step 4: Create E2E Tests

#### Page Object Pattern

```javascript
// tests/e2e/pages/QuizPage.js
export class QuizPage {
  constructor(page) {
    this.page = page;
    
    // Define locators
    this.topicInput = page.locator('[data-testid="topic-input"]');
    this.generateButton = page.locator('[data-testid="generate-quiz"]');
    this.questions = page.locator('[data-testid="question"]');
    this.submitButton = page.locator('[data-testid="submit-quiz"]');
  }

  async navigate() {
    await this.page.goto('/topic-input');
  }

  async createQuiz(topic) {
    await this.topicInput.fill(topic);
    await this.generateButton.click();
    await this.questions.first().waitFor({ state: 'visible' });
  }

  async answerAllQuestions() {
    const questionCount = await this.questions.count();
    for (let i = 0; i < questionCount; i++) {
      const firstAnswer = this.questions.nth(i).locator('[data-testid="answer"]').first();
      await firstAnswer.click();
    }
  }

  async submitQuiz() {
    await this.submitButton.click();
  }
}
```

#### E2E Test with Page Objects

```javascript
// tests/e2e/quiz-complete.spec.js
import { test, expect } from '@playwright/test';
import { QuizPage } from './pages/QuizPage.js';

test.describe('Quiz Completion E2E', () => {
  let quizPage;

  test.beforeEach(async ({ page }) => {
    quizPage = new QuizPage(page);
  });

  test('should complete quiz from topic to results', async ({ page }) => {
    await quizPage.navigate();
    await quizPage.createQuiz('History');
    await quizPage.answerAllQuestions();
    await quizPage.submitQuiz();
    
    // Verify results page
    await expect(page.locator('[data-testid="results"]')).toBeVisible();
    await expect(page.locator('[data-testid="score-display"]')).toContainText('Your score');
  });
});
```

## Test Execution Strategies

### Running Specific Tests

```bash
# Single test file
npm test -- src/utils/example.test.js

# Single test
npm test -- --run -t "should return correct result"

# Watch mode for development
npm test -- src/utils/example.test.js

# Coverage for specific file
npm run test:coverage -- src/utils/
```

### E2E Test Execution

```bash
# All E2E tests
npm run test:e2e

# Single spec file
npm run test:e2e -- tests/e2e/quiz-flow.spec.js

# With UI for debugging
npm run test:e2e:ui

# Specific test
npm run test:e2e -- --grep "should complete quiz"
```

### Mutation Testing

```bash
# Full mutation testing
npm run test:mutation

# Specific file only
npx stryker run --mutate "src/utils/example.js"

# With incremental mode
npx stryker run --incremental

# With increased concurrency
npx stryker run --concurrency 4
```

## Quality Assurance

### Coverage Requirements

```javascript
// In vitest.config.js
coverage: {
  thresholds: {
    global: {
      branches: 90,    // 90% branch coverage
      functions: 90,   // 90% function coverage
      lines: 90,       // 90% line coverage
      statements: 90   // 90% statement coverage
    },
    // Per-file thresholds
    './src/utils/': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    }
  }
}
```

### Mutation Score Requirements

```javascript
// Target scores by importance
const mutationTargets = {
  critical: {    // Core functionality
    files: ['src/core/*.js'],
    target: 85
  },
  important: {   // Services and utilities
    files: ['src/services/*.js', 'src/utils/*.js'],
    target: 80
  },
  normal: {       // Less critical code
    files: ['src/components/*.js'],
    target: 75
  }
};
```

## CI/CD Integration

### GitHub Actions Test Workflow

**File:** `.github/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: ['**']
  pull_request:
    branches: ['**']

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm install

    - name: Run unit tests
      run: npm test -- --run

    - name: Run architecture tests
      run: npm run arch:test

    - name: Run type checking
      run: npm run typecheck

    - name: Install Playwright
      run: npx playwright install --with-deps

    - name: Run E2E tests
      run: npm run test:e2e

    - name: Upload test results
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: |
          test-results/
          playwright-report/
        retention-days: 7
```

## Troubleshooting

### Test Failures

#### Unit Test Issues

```bash
# Run with verbose output
npm test -- --reporter=verbose

# Debug specific test
npm test -- --run -t "failing test name"

# Update snapshots if needed
npm test -- --update-snapshots
```

#### E2E Test Failures

```bash
# Run with headed browser for debugging
npx playwright test --headed

# Run with slow mode
npx playwright test --slowmo

# Take screenshots on failure
npx playwright test --screenshot=only-on-failure

# Generate trace files
npx playwright test --trace on
```

#### Mutation Testing Issues

```bash
# Check timeout settings
"timeoutMS": 60000  // Increase for large codebases

# Limit concurrency for stability
"concurrency": 1  // Reduce if flaky

# Exclude problematic files
"mutate": [
  "src/utils/**/*.js",
  "!src/utils/problematic.js"
]
```

## Integration with Other Skills

This skill integrates with:
- **epic-hygiene-process** - For test validation during hygiene tasks
- **feature-flag-management** - For testing flagged functionality
- **pwa-feature-development** - For comprehensive feature testing
- **architecture-compliance** - For validating layer boundaries in tests

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+