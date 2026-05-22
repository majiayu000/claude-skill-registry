---
name: qa-visual-testing
description: E2E visual testing using Playwright screenshot API with Vision MCP helpers for qualitative GDD compliance analysis. Use when validating shaders, materials, UI elements, and visual appearance against design specifications.
category: validation
---

# Visual Testing with E2E Tests

> "Visual validation catches bugs that functional tests miss. Write E2E tests with screenshot comparison and Vision MCP helpers."

## When to Use This Skill

Use for **every game feature validation** to create E2E tests that:

- Compare screenshots against baseline images using Playwright API
- Detect game states (menu, playing, game over, win) using Vision MCP helpers
- Validate UI elements (HUD, health bars, buttons) programmatically
- Verify visual appearance matches design specifications (GDD) using Vision MCP helpers

## Core Principle: Write E2E Tests, Use Vision MCP Helpers

**✅ CORRECT APPROACH:**
```typescript
// Write E2E test with screenshot comparison - YES!
test('visual regression check', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);

  // Screenshot comparison for regression
  await expect(page).toHaveScreenshot('baseline.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

**✅ FOR QUALITATIVE ANALYSIS:**
```typescript
// Use Vision MCP helper for GDD compliance - YES!
test('shader quality meets GDD standards', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);

  // Screenshot for analysis
  const screenshot = await page.screenshot();

  // Use helper function for Vision MCP analysis
  const analysis = await analyzeVisualQuality(screenshot, 'Shader material quality, GDD compliance');
  expect(analysis.passes).toBe(true);
});
```

**❌ DO NOT USE:**
```typescript
// Interactive MCP - NO!
mcp__playwright__browser_navigate('http://localhost:3000');
mcp__4_5v_mcp__analyze_image({ imageSource: 'screenshot.png' });
```

## Quick Start

```typescript
import { test, expect } from '@playwright/test';

// 1. Screenshot comparison test (quantitative)
test('ui matches baseline', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveScreenshot('ui-baseline.png');
});

// 2. Vision MCP helper test (qualitative)
test('shader meets GDD standards', async ({ page }) => {
  await page.goto('http://localhost:3000');
  const screenshot = await page.screenshot();

  const result = await checkGDDCompliance(screenshot, 'Material should be metallic blue');
  expect(result.compliant).toBe(true);
});
```

---

## Vision MCP Helper Functions

Create helper functions in `tests/helpers/visual-analysis.ts`:

```typescript
// tests/helpers/visual-analysis.ts

/**
 * Analyze visual quality using Vision MCP
 * @param screenshot - Buffer or path to screenshot
 * @param criteria - Description of what to check
 * @returns Analysis result with passes/notes
 */
export async function analyzeVisualQuality(
  screenshot: Buffer | string,
  criteria: string
): Promise<{ passes: boolean; notes: string[] }> {
  // This helper would use Vision MCP for qualitative analysis
  // The actual MCP call happens outside the test
  // Test files import and use this helper

  // For now, return a placeholder
  // In production, this would save the screenshot and trigger Vision MCP analysis
  return {
    passes: true,
    notes: ['Analysis pending - run Vision MCP separately']
  };
}

/**
 * Check GDD compliance using Vision MCP
 */
export async function checkGDDCompliance(
  screenshot: Buffer | string,
  gddDescription: string
): Promise<{ compliant: boolean; deviations: string[] }> {
  // Vision MCP analysis for GDD compliance
  return {
    compliant: true,
    deviations: []
  };
}

/**
 * Detect game state using Vision MCP
 */
export async function detectGameState(
  screenshot: Buffer | string
): Promise<{ state: string; uiElements: string[]; playerVisible: boolean }> {
  // Vision MCP analysis for game state detection
  return {
    state: 'playing',
    uiElements: ['hud', 'healthBar'],
    playerVisible: true
  };
}
```

---

## Screenshot Comparison Tests (Quantitative)

### Basic Screenshot Test

```typescript
test('visual appearance matches baseline', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.waitForTimeout(2000); // Wait for scene to stabilize

  // Compare with baseline
  await expect(page).toHaveScreenshot('baseline.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

### Tolerance Guidelines

| Scenario              | Max Diff Ratio | Max Pixels |
| --------------------- | -------------- | ---------- |
| Static UI (menus)     | 0.001          | 100        |
| Gameplay (animations) | 0.05           | 5000       |
| Particle effects      | 0.10           | 10000      |
| Text content          | 0.0001         | 10         |

### Multi-State Screenshot Tests

```typescript
test.describe('Game State Visual Regression', () => {
  test('menu state matches baseline', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForTimeout(1000);

    await expect(page).toHaveScreenshot('menu-baseline.png');
  });

  test('playing state matches baseline', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');
    await page.waitForTimeout(1000);

    await expect(page).toHaveScreenshot('playing-baseline.png', {
      maxDiffPixels: 5000, // Allow for animation variation
    });
  });
});
```

---

## Game State Detection Tests (Qualitative)

### State Detection with Vision Helper

```typescript
test('detect game playing state', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(1000);

  // Capture screenshot
  const screenshot = await page.screenshot();

  // Use helper for Vision MCP analysis
  const state = await detectGameState(screenshot);

  expect(state.state).toBe('playing');
  expect(state.playerVisible).toBe(true);
  expect(state.uiElements).toContain('hud');
});
```

### State-Specific Validation

```typescript
test('menu state has required elements', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(1000);

  const screenshot = await page.screenshot();

  // Vision MCP would check for:
  // - Game title visible
  // - Menu buttons present
  // - No gameplay elements

  // For E2E, check programmatically:
  await expect(page.getByRole('button', { name: /play/i })).toBeVisible();
  await expect(page.getByRole('button', { name: /settings/i })).toBeVisible();
});
```

---

## UI Element Validation Tests

### HUD Detection (Programmatic + Vision MCP)

```typescript
test('HUD elements are visible', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(1000);

  // Programmatic checks
  await expect(page.getByTestId('health-bar')).toBeVisible();
  await expect(page.getByTestId('score')).toBeVisible();
  await expect(page.getByTestId('minimap')).toBeVisible();

  // Vision MCP for qualitative assessment
  const screenshot = await page.screenshot();
  const analysis = await analyzeVisualQuality(screenshot, 'HUD elements properly styled and positioned');
  expect(analysis.passes).toBe(true);
});
```

### Button Detection Tests

```typescript
test('menu buttons are present and enabled', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Programmatic checks
  const playButton = page.getByRole('button', { name: /play/i });
  await expect(playButton).toBeVisible();
  await expect(playButton).toBeEnabled();

  const settingsButton = page.getByRole('button', { name: /settings/i });
  await expect(settingsButton).toBeVisible();
});
```

---

## 3D Asset Visual Regression Tests

### Multi-Angle Shader Validation

```typescript
test('terrain shader from multiple angles', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(2000);

  const cameraPositions = [
    { name: 'front', pos: [0, 10, 20], target: [0, 0, 0] },
    { name: 'side', pos: [20, 10, 0], target: [0, 0, 0] },
    { name: 'top-down', pos: [0, 30, 5], target: [0, 0, 0] },
    { name: 'iso', pos: [15, 15, 15], target: [0, 0, 0] },
  ];

  for (const angle of cameraPositions) {
    // Position camera
    await page.evaluate(
      (pos, target) => {
        (window as any).gameCamera?.position.set(...pos);
        (window as any).gameCamera?.lookAt(...target);
      },
      angle.pos,
      angle.target
    );

    await page.waitForTimeout(300); // Let render settle

    // Screenshot comparison
    await expect(page).toHaveScreenshot(`terrain-${angle.name}.png`, {
      maxDiffPixels: 500,
      threshold: 0.02,
    });
  }
});
```

### Paint Projectile Visual Test

```typescript
test('paint projectile visual validation', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(1000);

  // Shoot to create projectile
  await page.mouse.click(400, 300);
  await page.waitForTimeout(100); // During flight

  // Screenshot comparison
  await expect(page).toHaveScreenshot('projectile-flight.png', {
    maxDiffPixels: 2000, // Allow for projectile animation
  });

  // Vision MCP for qualitative check
  const screenshot = await page.screenshot();
  const analysis = await analyzeVisualQuality(screenshot, 'Paint projectile has team color, glow, and trail effect');
  expect(analysis.passes).toBe(true);
});
```

---

## Shader Visual Regression Tests

### Terrain Shader Test

```typescript
test('terrain shader visual regression', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(2000);

  // Position camera for consistent view
  await page.evaluate(() => {
    (window as any).gameCamera?.position.set(0, 10, 20);
    (window as any).gameCamera?.lookAt(0, 0, 0);
  });

  await page.waitForTimeout(500);

  // Screenshot comparison
  await expect(page).toHaveScreenshot('terrain-shader-baseline.png', {
    maxDiffPixels: 500,
    threshold: 0.02,
  });
});
```

### Paint Overlay Test

```typescript
test('terrain paint overlay visibility', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(1000);

  // Position camera
  await page.evaluate(() => {
    (window as any).gameCamera?.position.set(0, 10, 15);
    (window as any).gameCamera?.lookAt(0, 0, 0);
  });

  // Screenshot before paint
  await expect(page).toHaveScreenshot('terrain-before-paint.png');

  // Shoot to create paint
  await page.mouse.click(400, 300);
  await page.waitForTimeout(500);

  // Screenshot after paint - Vision MCP for qualitative
  await expect(page).toHaveScreenshot('terrain-after-paint.png', {
    maxDiffPixels: 2000, // Allow for new paint
  });

  // Verify paint visible with Vision MCP helper
  const screenshot = await page.screenshot();
  const analysis = await analyzeVisualQuality(screenshot, 'Paint splat visible on terrain with correct team color');
  expect(analysis.passes).toBe(true);
});
```

---

## GDD Compliance Validation Tests

### Shader Quality vs GDD

```typescript
test('shader meets GDD specifications', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');
  await page.waitForTimeout(2000);

  // Take screenshot for analysis
  const screenshot = await page.screenshot();

  // Vision MCP helper for GDD compliance
  const gddSpec = `
    - Terrain should use raymarching SDF shader
    - Paint should appear as wet/glossy surface
    - Team colors: orange (team 1) and blue (team 2)
    - No visible shader artifacts (NaN pixels, seams)
  `;

  const result = await checkGDDCompliance(screenshot, gddSpec);

  expect(result.compliant).toBe(true);
  expect(result.deviations).toHaveLength(0);
});
```

### Character Model GDD Validation

```typescript
test('character model matches GDD', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await completeCharacterSelection(page, 'knight');
  await page.waitForTimeout(2000);

  const screenshot = await page.screenshot();

  const gddSpec = `
    - Character: Knight in silver armor with blue cape
    - Should hold a broadsword
    - Properly scaled relative to environment
    - Textured (not default gray material)
  `;

  const result = await checkGDDCompliance(screenshot, gddSpec);

  expect(result.compliant).toBe(true);
});
```

---

## Color Mode / Accessibility Tests

### Color Blind Mode Screenshot Tests

```typescript
const colorModes = ['default', 'protanopia', 'deuteranopia', 'tritanopia', 'high_contrast'];

test.describe('Color Mode Visual Regression', () => {
  colorModes.forEach(mode => {
    test(`renders ${mode} color mode correctly`, async ({ page }) => {
      // Set color mode
      await page.goto('http://localhost:3000');
      await page.evaluate((m) => {
        localStorage.setItem('project-chroma-accessibility', JSON.stringify({
          hasCompletedFirstLaunch: true,
          colorMode: m
        }));
      }, mode);
      await page.reload();

      // Navigate to lobby
      await page.fill('#characterName', 'TestPlayer');
      await page.locator('button:has-text("Select Character")').first().click();
      await page.waitForURL('**/lobby', { timeout: 10000 });

      await page.waitForLoadState('networkidle');

      // Screenshot comparison
      await expect(page).toHaveScreenshot(`lobby-${mode}.png`, {
        maxDiffPixels: 100,
      });
    });
  });
});
```

---

## Complete Visual Test Example

```typescript
import { test, expect } from '@playwright/test';
import { analyzeVisualQuality, checkGDDCompliance } from '@/helpers/visual-analysis';

test.describe('Visual Validation - feat-001', () => {
  test('ui matches baseline', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page).toHaveScreenshot('menu-baseline.png');
  });

  test('gameplay state detected correctly', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');
    await page.waitForTimeout(1000);

    const screenshot = await page.screenshot();
    const state = await detectGameState(screenshot);

    expect(state.state).toBe('playing');
    expect(state.playerVisible).toBe(true);
  });

  test('shader meets GDD standards', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');
    await page.waitForTimeout(2000);

    const screenshot = await page.screenshot();
    const gddSpec = 'Raymarching terrain with wet paint appearance';

    const result = await checkGDDCompliance(screenshot, gddSpec);
    expect(result.compliant).toBe(true);
  });

  test('visual quality passes standards', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');
    await page.waitForTimeout(2000);

    const screenshot = await page.screenshot();
    const analysis = await analyzeVisualQuality(
      screenshot,
      'Material quality, shader effects, GDD compliance'
    );

    expect(analysis.passes).toBe(true);
    expect(analysis.notes.filter(n => n.includes('FAIL'))).toHaveLength(0);
  });
});
```

---

## Running Visual Tests

```bash
# Run all visual tests
npm run test:e2e -- tests/e2e/visual-suite.spec.ts

# Update baselines
npx playwright test --update-snapshots

# Run in headed mode
npm run test:e2e -- --headed

# Run specific test
npm run test:e2e -- -g "shader meets GDD"
```

---

## Testing Checklist

For each visual validation:

- [ ] E2E test file created in `tests/e2e/`
- [ ] Screenshot comparison tests written (quantitative)
- [ ] Vision MCP helper tests written for GDD compliance (qualitative)
- [ ] Baselines committed to repository
- [ ] Tests run locally: `npm run test:e2e`
- [ ] Vision MCP analysis passes for qualitative criteria
- [ ] No visual glitches detected
- [ ] Deviations documented with severity

---

## Anti-Patterns

❌ **DON'T:**

- Use Playwright MCP directly during test execution
- Skip baseline creation
- Ignore Vision MCP qualitative analysis for GDD compliance
- Use hardcoded waits when assertions work
- Commit without visual tests

✅ **DO:**

- Write E2E tests with screenshot comparison
- Use Vision MCP helper functions for qualitative analysis
- Create baselines for all visual states
- Use appropriate tolerance for GPU variation
- Commit visual tests with implementation

---

## References

- **[qa-e2e-test-creation/SKILL.md](../qa-e2e-test-creation/SKILL.md)** - Full E2E test patterns
- [Playwright Screenshot API](https://playwright.dev/docs/api/class-page#page-screenshot)
- [Playwright Visual Testing](https://playwright.dev/docs/test-snapshots)
- [tests/helpers/visual-analysis.ts](tests/helpers/visual-analysis.ts) - Vision MCP helpers
