---
name: component-screenshot-testing
description: Screenshot testing for React components with Playwright. Captures component pixels and compares to baselines. Auto-apply when editing React component stories or *.visual.spec.ts files that test UI components.
---

# Component Screenshot Testing Skill

Captures **React component screenshots** and compares them to baseline PNGs. Tests that UI components render correctly at the pixel level.

This is about **component appearance**, not data or canvas rendering. It catches:

- Color/style changes in React components
- Layout shifts and alignment issues
- Missing or misplaced UI elements
- Theme/styling regressions

For canvas-based filmstrip testing (matrix progressions), see `canvas-filmstrip-testing`.

## When to Use This

- Testing React components (buttons, controls, panels, etc.)
- UI styling changes
- Theme/dark mode appearance
- Component layout verification

## Architecture

```
stories/
  components/                    → Shared React components for stories
    StripViewer.tsx
    ProgressionStrip.tsx
  ui-components/                 → UI component stories (if present)
    Button.visual.spec.ts
    Panel.visual.spec.ts
```

## Commands

```bash
# Run visual tests
npm run test:visual:headless        # CI/agents
npm run test:visual:headed          # Debugging with browser UI

# Update baselines after intentional changes
npm run test:visual:update:headless
npm run test:visual:update:headed

# Clear test artifacts
npm run reset:visual                # Clear results/reports only
npm run reset:visual:all            # Clear results + colocated baselines

# Verify stories compile (fast check)
npm run stories:build
```

## Test Structure

```typescript
// Example: stories/ui-components/Button.visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button Component', () => {
  test('primary button', async ({ page }) => {
    await page.goto('http://localhost:3001/?page=ui-button');

    const button = page.getByTestId('button-primary');
    await expect(button).toHaveScreenshot('button-primary.png');
  });

  test('disabled button', async ({ page }) => {
    await page.goto('http://localhost:3001/?page=ui-button');

    const button = page.getByTestId('button-disabled');
    await expect(button).toHaveScreenshot('button-disabled.png');
  });
});
```

## Best Practices

1. **Target specific elements** - Use `data-testid` to capture just the component
2. **Test states** - Hover, focus, disabled, active states
3. **Consistent viewport** - Set fixed dimensions to avoid flaky tests
4. **Wait for render** - Ensure component is fully rendered before screenshot

```typescript
// Wait for component to be ready
await page.waitForSelector('[data-testid="my-component"]');
await page.waitForLoadState('networkidle');

// Screenshot just the component
const element = page.getByTestId('my-component');
await expect(element).toHaveScreenshot('my-component.png');
```

## Debugging with Chrome DevTools MCP

When a visual test fails:

```typescript
// Start dev server
npm run stories

// Open in browser
mcp__chrome-devtools__new_page({ url: "http://localhost:3001/?page=ui-button" })

// Take snapshot to find element UIDs
mcp__chrome-devtools__take_snapshot()

// Screenshot specific element
mcp__chrome-devtools__take_screenshot({ uid: "<element-uid>" })

// After fixing, reload and re-check
mcp__chrome-devtools__navigate_page({ type: "reload" })
```

## Related Skills

- **canvas-filmstrip-testing** - For matrix-to-canvas rendered progressions
- **visual-regression** - Shared infrastructure and orchestration
- **react-ui** - React component development patterns
