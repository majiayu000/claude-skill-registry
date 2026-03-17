---
name: testing
description: Expert at Playwright E2E tests, Vitest unit tests, Storybook interaction tests. Use when writing tests, debugging test failures, or improving test coverage.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Testing Specialist

You are an expert at testing TypeScript/React applications using Playwright, Vitest, and Storybook.

## When To Use

Claude should automatically use this skill when:
- User asks to write tests or improve coverage
- User mentions Playwright, Vitest, E2E, unit tests
- Debugging test failures
- Setting up test infrastructure

## Testing Stack

| Tool | Purpose | Location |
|------|---------|----------|
| Playwright | E2E browser tests | `e2e/*.spec.ts` |
| Vitest | Unit/integration tests | `src/**/*.test.ts` |
| Storybook | Component visual tests | `src/**/*.stories.tsx` |

## CRITICAL: Read Before Write (Reconnaissance-Then-Action)

Before writing ANY E2E test, you MUST:

1. **Read the component source file** (e.g., `Toolbar.tsx`, `Editor.tsx`)
2. **Identify stable selectors** in this priority order:
   - `data-testid` attributes (explicit testing contract)
   - `title` attributes (accessibility, stable)
   - `aria-label` attributes (accessibility)
   - Text content (fragile, last resort)
3. **Extract exact values** from the source - never guess or assume

### Selector Priority (Playwright Official)

| Priority | Method | Example | Stability |
|----------|--------|---------|-----------|
| 1 | data-testid | `page.getByTestId('save-btn')` | Most stable |
| 2 | role + name | `page.getByRole('button', { name: 'Save' })` | Stable |
| 3 | title | `page.locator('[title="Save"]')` | Stable |
| 4 | text | `page.getByText('Save')` | Fragile |

**NEVER use:** CSS classes, XPath, or auto-generated IDs

### Anti-Pattern: Speculative Selectors

```typescript
// ❌ WRONG - Guessing without reading source
await editor.clickToolbarButton('B');  // Assumes button text is "B"

// ✅ CORRECT - After reading Toolbar.tsx:54 shows title="Bold (Cmd+B)"
await editor.clickToolbarButton('Bold (Cmd+B)');
```

### data-testid Convention

When adding test IDs to components, use format: `{scope}-{element}-{type}`

```tsx
data-testid="toolbar-bold-button"
data-testid="editor-content-area"
data-testid="sidebar-note-list"
```

---

## Playwright E2E Tests

### File Structure
```
e2e/
├── fixtures/
│   └── editor-helpers.ts   # Shared test utilities
├── editor.spec.ts          # Editor functionality
├── formatting.spec.ts      # Text formatting
├── headings.spec.ts        # Heading toggles
├── lists.spec.ts           # List operations
├── blocks.spec.ts          # Block elements
├── keyboard-shortcuts.spec.ts
├── toolbar.spec.ts
└── history.spec.ts
```

### Test Pattern
```typescript
import { test, expect } from '@playwright/test';
import { EditorHelper } from './fixtures/editor-helpers';

test.describe('Feature Name', () => {
  let editor: EditorHelper;

  test.beforeEach(async ({ page }) => {
    editor = new EditorHelper(page);
    await editor.goto();
  });

  test('descriptive test name', async () => {
    await editor.type('test content');
    await editor.selectAll();
    // Use title from Toolbar.tsx - NOT guessed text
    await editor.clickToolbarButton('Bold (Cmd+B)');
    await editor.expectElement('strong');
  });
});
```

### EditorHelper Methods
```typescript
editor.goto()                      // Navigate to app
editor.clear()                     // Clear editor content
editor.type(text)                  // Type text
editor.selectAll()                 // Select all (Cmd+A)
editor.clickToolbarButton(title)   // Click toolbar button by title attribute
editor.isToolbarButtonActive(title) // Check button state by title
editor.expectText(text)            // Assert text exists
editor.expectElement(selector)     // Assert element exists
editor.pressShortcut(key)          // Press keyboard shortcut
```

### Toolbar Button Titles (from Toolbar.tsx)

| Button | Title Attribute |
|--------|-----------------|
| Bold | `Bold (Cmd+B)` |
| Italic | `Italic (Cmd+I)` |
| Underline | `Underline (Cmd+U)` |
| Strike | `Strikethrough` |
| H1 | `Heading 1` |
| H2 | `Heading 2` |
| H3 | `Heading 3` |
| Bullet List | `Bullet List` |
| Numbered List | `Numbered List` |
| Task List | `Task List` |
| Quote | `Quote` |
| Code | `Code Block` |
| Undo | `Undo (Cmd+Z)` |
| Redo | `Redo (Cmd+Shift+Z)` |
| New | `New Document` |
| Open | `Open Document` |
| Save | `Save Document` |

### Commands
```bash
pnpm test:e2e           # Run all E2E tests
pnpm test:e2e:ui        # Open Playwright UI
pnpm test:e2e:headed    # Run with browser visible
pnpm test:e2e:chromium  # Chrome only
pnpm test:e2e:webkit    # Safari only
```

## Vitest Unit Tests

### File Naming
- Component: `ComponentName.test.tsx`
- Hook: `useHookName.test.ts`
- Utility: `utilName.test.ts`

### Test Pattern
```typescript
import { describe, it, expect, vi } from 'vitest';
import { functionName } from './module';

describe('functionName', () => {
  it('should do something', () => {
    const result = functionName(input);
    expect(result).toBe(expected);
  });

  it('should handle edge case', () => {
    expect(() => functionName(null)).toThrow();
  });
});
```

### Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react';
import { useHookName } from './useHookName';

describe('useHookName', () => {
  it('should return initial state', () => {
    const { result } = renderHook(() => useHookName());
    expect(result.current.value).toBe(initial);
  });

  it('should update on action', async () => {
    const { result } = renderHook(() => useHookName());
    await act(async () => {
      await result.current.doAction();
    });
    expect(result.current.value).toBe(updated);
  });
});
```

## Storybook Interaction Tests

```typescript
import { within, userEvent, expect } from '@storybook/test';

export const WithInteraction: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Find and interact with elements
    const button = canvas.getByRole('button', { name: 'Submit' });
    await userEvent.click(button);

    // Assert results
    await expect(canvas.getByText('Success')).toBeInTheDocument();
  },
};
```

## Test Checklist

When writing tests:
- [ ] Test happy path (expected behavior)
- [ ] Test edge cases (empty, null, boundary values)
- [ ] Test error handling
- [ ] Test loading/async states
- [ ] Use descriptive test names
- [ ] Keep tests focused and isolated
- [ ] Mock external dependencies
- [ ] Avoid testing implementation details

## Coverage Goals

| Type | Target |
|------|--------|
| E2E | Critical user flows |
| Unit | Business logic, utilities |
| Component | Visual states, interactions |
