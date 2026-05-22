---
name: tauri-e2e-testing
description: "This skill should be used when setting up, writing, debugging, or maintaining end-to-end tests for Tauri v2 desktop applications. Triggers on: 'tauri test', 'e2e tauri', 'playwright tauri', 'test tauri app', 'tauri testing', 'test desktop app'. Provides Playwright + Vitest + Rust test configuration, Tauri API mocking patterns, CI/CD workflows, and debugging utilities for Vue 3 + TypeScript + Vite + Tauri v2 stacks."
---

# Tauri E2E Testing Skill

End-to-end testing guide for Tauri v2 applications with Vue 3 + TypeScript + Vite + Playwright.

## Purpose

Set up, write, debug, and maintain comprehensive test suites for Tauri v2 desktop applications using a 3-tier testing pyramid approach.

## When to Use

- Setting up testing infrastructure for a new Tauri app
- Writing E2E tests that interact with Tauri IPC commands
- Mocking Tauri APIs (file system, dialogs, system tray)
- Configuring CI/CD for multi-platform testing
- Debugging flaky or failing Playwright tests
- Testing Rust backend commands

## Framework Recommendation

| Layer | Framework | Purpose |
|-------|-----------|---------|
| E2E | **Playwright** | UI workflows, mocked Tauri commands |
| Unit | **Vitest** | Vue components, composables, utilities |
| Backend | **cargo test** | Rust command logic, permissions |

**Why Playwright over WebDriver:**
- Superior TypeScript support and IDE integration
- TraceViewer for post-mortem debugging
- Auto-waiting eliminates flakiness
- Faster execution (~1-2s per test)
- Vue 3 semantic queries work perfectly

**Use WebDriver only if:** Testing actual system tray or native file dialogs is critical.

## Quick Start

### 1. Install Dependencies

```bash
npm install -D @playwright/test vitest @vitest/ui @vue/test-utils jsdom
npm install -D @testing-library/vue @testing-library/user-event
npx playwright install --with-deps
```

### 2. Copy Configuration Files

Copy templates from `assets/` directory:
- `playwright.config.ts` → project root
- `vitest.config.ts` → project root
- `mock-tauri.ts` → `src/tests/e2e/fixtures/`

### 3. Add npm Scripts

```json
{
  "scripts": {
    "test": "npm run test:unit && npm run test:e2e",
    "test:unit": "vitest",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:report": "playwright show-report"
  }
}
```

### 4. Create Test Directory Structure

```
src/tests/
├── e2e/
│   ├── fixtures/
│   │   └── mock-tauri.ts
│   ├── pages/           # Page Object classes
│   ├── app.spec.ts
│   └── global-setup.ts
├── unit/
│   ├── setup.ts
│   ├── components/
│   └── composables/
└── __snapshots__/
```

## Core Patterns

### Mocking Tauri IPC Commands

```typescript
// In Playwright test
test('invoke tauri command', async ({ page }) => {
  await page.addInitScript(() => {
    window.__TAURI_CORE__ = {
      invoke: async (cmd: string, args?: any) => {
        const mocks: Record<string, (args: any) => any> = {
          'greet': (args) => `Hello, ${args.name}!`,
          'save_config': () => ({ success: true }),
        };
        const handler = mocks[cmd];
        if (!handler) throw new Error(`Unknown command: ${cmd}`);
        return handler(args);
      },
    };
  });

  await page.goto('/');
  // Test continues...
});
```

### Mocking File System

```typescript
await page.addInitScript(() => {
  window.__TAURI_FS__ = {
    readTextFile: async (path: string) => 'mocked content',
    writeTextFile: async (path: string, content: string) => {},
    readDir: async (path: string) => [],
  };
});
```

### Mocking Native Dialogs

```typescript
await page.addInitScript(() => {
  window.__TAURI_DIALOG__ = {
    open: async () => '/path/to/selected/file.pdf',
    save: async () => '/path/to/save/location.json',
  };
});
```

### Page Object Pattern

```typescript
// src/tests/e2e/pages/TaskPage.ts
export class TaskPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/tasks');
    await this.page.waitForSelector('[data-testid="task-list"]');
  }

  async addTask(title: string) {
    await this.page.fill('input[placeholder="Enter task"]', title);
    await this.page.click('button:has-text("Add")');
  }

  async completeTask(title: string) {
    const task = this.page.locator(`[data-testid="task"]:has-text("${title}")`);
    await task.getByRole('button', { name: /complete/i }).click();
  }
}
```

### Keyboard Shortcuts Testing

```typescript
test('ctrl+s saves document', async ({ page }) => {
  await page.goto('/');
  await page.fill('textarea', 'content');
  await page.keyboard.press('Control+S');
  await expect(page.getByText(/saved/i)).toBeVisible();
});
```

## Vitest Unit Test Setup

```typescript
// src/tests/unit/setup.ts
import { vi } from 'vitest';

vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
  convertFileSrc: vi.fn(),
}));

vi.mock('@tauri-apps/api/fs', () => ({
  readTextFile: vi.fn(),
  writeTextFile: vi.fn(),
}));

vi.mock('@tauri-apps/api/dialog', () => ({
  open: vi.fn(),
  save: vi.fn(),
}));

beforeEach(() => {
  localStorage.clear();
  vi.clearAllMocks();
});
```

## Rust Backend Testing

```rust
#[tauri::command]
pub fn add_task(state: tauri::State<TaskState>, title: String) -> Result<Task, String> {
  if title.trim().is_empty() {
    return Err("Task title cannot be empty".to_string());
  }
  // ... implementation
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn test_add_task_empty_title() {
    let state = TaskState::default();
    let result = add_task(tauri::State::new(state), "".to_string());
    assert!(result.is_err());
  }
}
```

## CI/CD Setup

Copy `assets/test.yml` to `.github/workflows/test.yml` for:
- Multi-platform testing (Ubuntu, Windows, macOS)
- Parallel unit/Rust tests, sequential E2E
- Playwright artifact upload on failure
- Rust caching with swatinem/rust-cache

### Linux Dependencies (Ubuntu)

```bash
sudo apt-get install -y \
  libwebkit2gtk-4.1-dev \
  libgtk-3-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev
```

## Debugging

### Commands

```bash
npm run test:e2e:debug    # Opens Playwright Inspector
npm run test:e2e:ui       # Interactive UI mode
npm run test:e2e:report   # View HTML report
npx playwright show-trace trace.zip  # Post-mortem analysis
```

### Debug Utilities

```typescript
export async function debugPage(page: Page) {
  console.log('URL:', page.url());
  await page.screenshot({ path: 'debug.png' });
  await page.pause();  // Opens inspector
}
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Element not visible | Use `page.getByRole('button').isVisible()` |
| Timeout waiting | Add `await page.waitForLoadState('networkidle')` |
| Flaky tests | Replace `waitForTimeout` with explicit conditions |
| Can't find element | Use semantic selectors: `getByRole`, `getByLabel` |

## Best Practices 2025

### Do

- Use semantic selectors: `getByRole('button', { name: /save/i })`
- Auto-wait for conditions: `await expect(element).toBeVisible()`
- Use Page Object pattern for maintainable tests
- Mock Tauri APIs with `page.addInitScript()`
- Test error cases and edge conditions
- Run tests in CI on multiple platforms

### Don't

- Use `waitForTimeout()` with hardcoded delays
- Use fragile CSS selectors: `div > div:nth-child(3)`
- Test implementation details
- Skip platform-specific testing in CI
- Ignore flaky tests

## Security Testing

```typescript
test('restricted command fails without permission', async ({ page }) => {
  const error = await page.evaluate(async () => {
    try {
      await window.__TAURI_CORE__.invoke('restricted_command');
      return null;
    } catch (e: any) {
      return e.message;
    }
  });
  expect(error).toContain('Permission denied');
});
```

## Performance Testing

```typescript
test('app startup under 3 seconds', async ({ page }) => {
  const start = Date.now();
  await page.goto('/', { waitUntil: 'networkidle' });
  expect(Date.now() - start).toBeLessThan(3000);
});
```

## Asset Files

| File | Purpose | Location |
|------|---------|----------|
| `playwright.config.ts` | Playwright configuration | Project root |
| `vitest.config.ts` | Vitest configuration | Project root |
| `mock-tauri.ts` | Tauri API mocking helpers | `src/tests/e2e/fixtures/` |
| `test.yml` | GitHub Actions workflow | `.github/workflows/` |

## WebKitGTK UI Compatibility (Linux)

### The Problem

On Linux, Tauri uses **WebKitGTK** as its webview engine. Unlike Chromium (Windows/macOS), WebKitGTK renders certain UI elements using **GTK native widgets** instead of CSS:

| Element | Chromium | WebKitGTK |
|---------|----------|-----------|
| `<select>` | CSS-styled | GTK native widget |
| `<input type="date">` | CSS-styled | GTK native widget |
| `<input type="color">` | CSS-styled | GTK native widget |
| Scrollbars | CSS-styled | Often GTK native |

**CSS cannot fully style these native elements** - they inherit from the system GTK theme.

### Known Issues

- [Tauri #11755](https://github.com/tauri-apps/tauri/issues/11755): Select element not styled correctly
- [Tauri #1126](https://github.com/tauri-apps/tauri/issues/1126): background-color for `<select>` ignored

### The Solution: Use Custom Components

**Replace native form elements with custom Vue components:**

```vue
<!-- ❌ WRONG - Native select won't style in WebKitGTK -->
<select v-model="value">
  <option value="a">Option A</option>
  <option value="b">Option B</option>
</select>

<!-- ✅ CORRECT - Custom component with full CSS control -->
<CustomSelect
  v-model="value"
  :options="[
    { label: 'Option A', value: 'a' },
    { label: 'Option B', value: 'b' }
  ]"
/>
```

### Quick CSS Fixes (Partial)

Add to your main CSS file:

```css
/* Signal dark mode to browser */
:root {
  color-scheme: dark;
}

/* Reset native appearance (helps with trigger button only) */
select {
  -webkit-appearance: none;
  appearance: none;
  background-color: #1e1e28;
  color: #e0e0e0;
}
```

**Note:** This only affects the closed select trigger, NOT the dropdown options list.

### Files That Need Migration

When fixing a Tauri app, search for native `<select>` usage:

```bash
grep -rn "<select" src/components/ --include="*.vue" | grep -v CustomSelect
```

Common locations in Pomo-Flow:
- `src/components/base/FilterControls.vue` ✅ Fixed
- `src/components/sync/BackupSettings.vue`
- `src/components/kanban/KanbanSwimlane.vue`
- `src/components/common/GroupModal.vue`
- `src/components/projects/ProjectModal.vue`
- `src/components/canvas/UnifiedGroupModal.vue`
- `src/components/tasks/HierarchicalTaskRow.vue`
- `src/components/tasks/TaskTable.vue`
- `src/components/tasks/BatchEditModal.vue`
- `src/components/canvas/GroupSettingsMenu.vue`
- `src/components/recurrence/RecurrencePatternSelector.vue`

### Migration Pattern

1. **Import CustomSelect:**
   ```typescript
   import CustomSelect from '@/components/common/CustomSelect.vue'
   ```

2. **Create options array:**
   ```typescript
   const options = [
     { label: 'All Items', value: '' },
     { label: 'Option 1', value: 'opt1' },
     { label: 'Option 2', value: 'opt2' }
   ]
   ```

3. **Replace template:**
   ```vue
   <CustomSelect
     :model-value="selectedValue"
     :options="options"
     placeholder="Select..."
     @update:model-value="handleChange"
   />
   ```

### Tauri Environment Detection

Detect Tauri to apply conditional styling:

```typescript
// In main.ts - run early before CSS loads
const isTauri = ('isTauri' in window && window.isTauri) ||
                ('__TAURI__' in window) ||
                ('__TAURI_INTERNALS__' in window)

if (isTauri) {
  document.documentElement.classList.add('tauri-app')
}
```

Then in CSS:
```css
.tauri-app .some-element {
  /* Tauri-specific overrides */
  backdrop-filter: none;
  background: rgba(25, 25, 30, 0.98);
}
```

### Backdrop-Filter Limitations

WebKitGTK has limited `backdrop-filter` support. Add fallbacks:

```css
/* Glass morphism fallback for Tauri */
.tauri-app .glass,
.tauri-app [class*="backdrop-blur"] {
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  background-color: rgba(25, 25, 30, 0.98) !important;
}
```

## References

For detailed patterns and examples, see:
- `references/testing-patterns.md` - Common test patterns
- `references/troubleshooting.md` - Debugging guide
- `references/webkitgtk-compatibility.md` - Full WebKitGTK UI guide
