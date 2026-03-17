---
name: desktop-e2e-testing
description: Generate end-to-end tests for the complete Desktop Ethereal application, including UI interactions, system integration, and user workflows. Triggers on E2E testing, Playwright, system testing, or complete application testing requests.
---

# Desktop E2E Testing Skill

This skill enables Claude to generate comprehensive end-to-end tests for the complete Desktop Ethereal application, covering UI interactions, system integration, and user workflows.

## When to Apply This Skill

Apply this skill when the user:

- Asks to **write E2E tests** for the complete application
- Asks to **test user workflows** or **complete user journeys**
- Mentions **Playwright**, **system testing**, or **desktop application testing**
- Requests **UI interaction testing** or **integration testing**
- Wants to improve **test coverage** for end-to-end scenarios

**Do NOT apply** when:

- User is asking about unit tests (frontend or backend)
- User is asking about specific component testing
- User is only asking conceptual questions without code context

## Quick Reference

### Tech Stack

| Tool | Version | Purpose |
| ------ | --------- | --------- |
| Playwright | 1.40+ | E2E testing framework |
| TypeScript | 5.9+ | Test scripting |
| Node.js | 18+ | Runtime environment |

### Key Commands

```bash
# Run all E2E tests
pnpm test:e2e

# Run tests in headed mode
pnpm test:e2e --headed

# Run specific test file
pnpm test:e2e tests/e2e/basic-workflow.spec.ts

# Generate test report
pnpm test:e2e --reporter=html
```

## Test Structure Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Desktop Ethereal E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Setup test environment
    await page.goto('/');
    // Wait for application to load
    await page.waitForSelector('[data-testid="ethereal-window"]');
  });

  test.afterEach(async ({ page }) => {
    // Cleanup test environment
    await page.close();
  });

  // User workflow tests (REQUIRED)
  test.describe('Basic User Workflow', () => {
    test('should display ethereal window on startup', async ({ page }) => {
      // Arrange - Application started in beforeEach

      // Act - No action needed, just observing initial state

      // Assert
      await expect(page.locator('[data-testid="ethereal-window"]')).toBeVisible();
      await expect(page.locator('[data-testid="status-display"]')).toContainText('IDLE');
    });

    test('should toggle click-through mode', async ({ page }) => {
      // Arrange
      const enableButton = page.locator('[data-testid="enable-click-through"]');
      const disableButton = page.locator('[data-testid="disable-click-through"]');

      // Act
      await enableButton.click();

      // Assert
      await expect(disableButton).toBeVisible();
      await expect(enableButton).not.toBeVisible();

      // Act
      await disableButton.click();

      // Assert
      await expect(enableButton).toBeVisible();
      await expect(disableButton).not.toBeVisible();
    });
  });

  // System integration tests
  test.describe('System Integration', () => {
    test('should respond to GPU temperature changes', async ({ page }) => {
      // Arrange
      const statusDisplay = page.locator('[data-testid="status-display"]');

      // Act - Simulate GPU temperature event
      await page.evaluate(() => {
        window.dispatchEvent(new CustomEvent('gpu-update', {
          detail: { temperature: 85, utilization: 50 }
        }));
      });

      // Assert
      await expect(statusDisplay).toContainText('OVERHEATING');
      await expect(statusDisplay).toContainText('85°C');
    });
  });

  // UI interaction tests
  test.describe('UI Interactions', () => {
    test('should drag window when not in click-through mode', async ({ page }) => {
      // Arrange
      const windowElement = page.locator('[data-testid="ethereal-window"]');

      // Act
      await windowElement.dragTo(windowElement, {
        targetPosition: { x: 100, y: 100 }
      });

      // Assert
      // Verify window position changed (implementation dependent)
    });
  });
});
```

## Testing Workflow (CRITICAL)

### ⚠️ Incremental Approach Required

**NEVER generate all test files at once.** For complex workflows or multi-scenario testing:

1. **Analyze & Plan**: List all user workflows, order by complexity (simple → complex)
1. **Process ONE at a time**: Write test → Run test → Fix if needed → Next
1. **Verify before proceeding**: Do NOT continue to next workflow until current passes

```
For each workflow:
  ┌────────────────────────────────────────┐
  │ 1. Write test                          │
  │ 2. Run: pnpm test:e2e test-file.spec.ts│
  │ 3. PASS? → Mark complete, next workflow│
  │    FAIL? → Fix first, then continue    │
  │ 4. Check coverage                      │
  └────────────────────────────────────────┘
```

### Complexity-Based Order

Process in this order for multi-workflow testing:

1. 🟢 Basic application startup and visibility
1. 🟢 Simple UI interactions (clicking buttons)
1. 🟡 System event responses
1. 🟡 State transitions
1. 🔴 Complex user workflows
1. 🔴 Cross-feature integration scenarios

## Core Principles

### 1. User-Centric Testing

- Test from the user's perspective
- Focus on complete workflows, not individual components
- Verify observable behavior and user experience

### 2. Realistic Test Scenarios

- Use realistic data and inputs
- Simulate actual user interactions
- Test common and edge case scenarios

### 3. Deterministic Tests

- Ensure tests produce consistent results
- Use proper waits and assertions
- Avoid flaky test conditions

### 4. Descriptive Test Naming

Use `should <behavior> when <condition>`:

```typescript
test('should display overheating state when GPU temperature exceeds 80°C')
test('should enable click-through mode when Ctrl+Shift+D is pressed')
test('should animate ethereal when system activity changes')
```

## Required Test Scenarios

### Always Required (Core Functionality)

1. **Application Startup**: Window appears, initial state is correct
1. **Basic UI Interaction**: Buttons respond to clicks
1. **Mode Toggling**: Click-through mode can be enabled/disabled
1. **Window Movement**: Window can be dragged when not in click-through mode

### Conditional (When Present)

| Feature | Test Focus |
| --------- | ------------ |
| System Monitoring | Response to GPU/CPU events |
| State Transitions | Correct state changes based on system activity |
| Sprite Animation | Animations play correctly for each state |
| LLM Integration | Chat functionality works |
| Clipboard Monitoring | Response to clipboard changes |
| Hotkey Support | Global hotkeys function |

## Coverage Goals (Per Workflow)

For each test workflow generated, aim for:

- ✅ **100%** workflow coverage
- ✅ **100%** user interaction coverage
- ✅ **>95%** scenario coverage
- ✅ **>95%** edge case coverage

## Desktop-Specific Considerations

### Window Management Testing

Test window-specific behaviors:

```typescript
test('should maintain always-on-top behavior', async ({ page }) => {
  // Test that the window stays on top of other applications
});

test('should respect transparent window properties', async ({ page }) => {
  // Test that transparency works correctly
});
```

### System Integration Testing

Test system-level integrations:

```typescript
test('should respond to system GPU monitoring events', async ({ page }) => {
  // Simulate GPU temperature events and verify response
  await page.evaluate(() => {
    window.dispatchEvent(new CustomEvent('gpu-update', {
      detail: { temperature: 85, utilization: 75 }
    }));
  });

  await expect(page.locator('[data-testid="status"]')).toContainText('OVERHEATING');
});
```

### Input Method Testing

Test various input methods:

```typescript
test('should respond to global hotkey Ctrl+Shift+D', async ({ page }) => {
  // Test global hotkey functionality
  await page.keyboard.press('Control+Shift+D');
  // Verify mode changed
});

test('should respond to mouse drag when not click-through', async ({ page }) => {
  // Test window dragging functionality
});
```

## Playwright-Specific Patterns

### Page Object Model

Use page objects for maintainable tests:

```typescript
// tests/e2e/page-objects/EtherealWindow.ts
export class EtherealWindow {
  constructor(private page: Page) {}

  async toggleClickThrough() {
    const enableButton = this.page.locator('[data-testid="enable-click-through"]');
    const disableButton = this.page.locator('[data-testid="disable-click-through"]');

    if (await enableButton.isVisible()) {
      await enableButton.click();
    } else {
      await disableButton.click();
    }
  }

  async getStatus() {
    return await this.page.locator('[data-testid="status-display"]').textContent();
  }
}

// In test file
test('should toggle click-through mode', async ({ page }) => {
  const etherealWindow = new EtherealWindow(page);

  await etherealWindow.toggleClickThrough();
  // ... assertions
});
```

### Custom Assertions

Create custom assertions for complex verifications:

```typescript
// tests/e2e/utils/assertions.ts
export async function expectEtherealState(page: Page, expectedState: string) {
  const status = await page.locator('[data-testid="status-display"]').textContent();
  expect(status).toContain(expectedState);
}

// In test file
import { expectEtherealState } from '../utils/assertions';

test('should enter overheating state when GPU temp exceeds 80°C', async ({ page }) => {
  // ... trigger GPU event
  await expectEtherealState(page, 'OVERHEATING');
});
```

## Test Data Management

### Fixture Data

Use fixtures for consistent test data:

```typescript
// tests/e2e/fixtures/gpu-events.ts
export const gpuEvents = {
  normal: { temperature: 65, utilization: 30 },
  hot: { temperature: 85, utilization: 75 },
  critical: { temperature: 95, utilization: 90 }
};

// In test file
import { gpuEvents } from '../fixtures/gpu-events';

test('should respond to GPU temperature events', async ({ page }) => {
  await page.evaluate((event) => {
    window.dispatchEvent(new CustomEvent('gpu-update', { detail: event }));
  }, gpuEvents.hot);

  // ... assertions
});
```

## Detailed Guides

For more detailed information, refer to:

- `references/workflow.md` - **Incremental testing workflow** (MUST READ for multi-workflow testing)
- `references/playwright-patterns.md` - Playwright testing patterns and best practices
- `references/system-integration.md` - System integration testing approaches
- `references/ui-interactions.md` - UI interaction testing techniques
- `references/test-organization.md` - Test file organization and structure

## Authoritative References

### Primary Specification (MUST follow)

- **`docs/e2e-testing.md`** - The canonical testing specification for Desktop Ethereal E2E tests.

### Reference Examples in Codebase

- `tests/e2e/` - E2E test directory (to be created)
- `playwright.config.ts` - Playwright configuration
- `package.json` - Test scripts and dependencies

### Project Configuration

- `playwright.config.ts` - Playwright configuration
- `tests/e2e/` - E2E test files
