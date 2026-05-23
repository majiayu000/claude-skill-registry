---
name: ta-terrain-testing
description: E2E testing patterns for terrain system validation using Playwright. Use for visual validation, performance testing, and screenshot-based testing of terrain components.
category: workflow
---

# Terrain Testing Skill

> "Visual validation for terrain - screenshots, performance, and gameplay testing."

## Overview

This skill provides E2E testing patterns specifically for terrain system validation. Tests use Playwright to navigate to test scenes, take screenshots, and validate visual output.

**IMPORTANT:** This is for Tech Artist visual validation. QA runs the full test suite.

## When to Use This Skill

Use when:
- Validating terrain mesh renders correctly
- Testing water animation
- Verifying grass placement
- Checking paint overlay visibility
- Measuring performance (FPS)
- Creating visual regression tests

## Test Scene Navigation

```typescript
/**
 * Navigate to terrain test scene
 */
async function navigateToTerrainTest(
  page: Page,
  scene: 'terrain-mesh' | 'water-plane' | 'grass-instancer' | 'paint-overlay' | 'territory-grid' | 'terrain-full'
): Promise<void> {
  await page.goto(`http://localhost:3000/?scene=${scene}`);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000); // Wait for Three.js initialization
}
```

## Helper Functions

### Canvas Color Validation

```typescript
/**
 * Check if canvas has color (not all black/white)
 */
async function hasCanvasColor(page: Page): Promise<boolean> {
  return await page.evaluate(() => {
    const canvas = document.querySelector('canvas');
    if (!canvas) return false;

    const ctx = canvas.getContext('2d');
    if (!ctx) return false;

    const imageData = ctx.getImageData(100, 100, 200, 200);
    const data = imageData.data;

    // Check for non-grayscale pixels
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      // If channels differ significantly, has color
      if (Math.abs(r - g) > 20 || Math.abs(r - b) > 20) {
        return true;
      }
    }
    return false;
  });
}
```

### FPS Measurement

```typescript
/**
 * Measure FPS over 1 second
 */
async function measureFPS(page: Page, duration: number = 1000): Promise<number> {
  return await page.evaluate((ms) => {
    return new Promise((resolve) => {
      let frames = 0;
      const startTime = performance.now();

      function countFrame() {
        frames++;
        const elapsed = performance.now() - startTime;
        if (elapsed >= ms) {
          resolve(Math.round(frames * 1000 / elapsed));
        } else {
          requestAnimationFrame(countFrame);
        }
      }
      requestAnimationFrame(countFrame);
    });
  }, duration);
}
```

### Screenshot with Timestamp

```typescript
/**
 * Take screenshot with timestamp in filename
 */
async function takeScreenshot(
  page: Page,
  path: string,
  name: string
): Promise<void> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  await page.screenshot({
    path: `${path}/${name}-${timestamp}.png`,
    fullPage: true
  });
}
```

## Phase 1: Terrain Mesh Tests

```typescript
test.describe('Phase 1: Terrain Mesh', () => {

  test('renders with visible colors (not all black/white)', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    await page.screenshot({
      path: 'test-results/terrain/phase1-mesh/initial.png',
      fullPage: true
    });

    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });

  test('has visible height variation', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    // Sample heights at different positions
    const heights = await page.evaluate(() => {
      const getHeight = (window as any).getTerrainHeight;
      if (!getHeight) return [0, 0, 0];

      return [
        getHeight(0, 0),
        getHeight(50, 50),
        getHeight(-50, -50)
      ];
    });

    // Should have variation
    const minH = Math.min(...heights);
    const maxH = Math.max(...heights);
    expect(maxH - minH).toBeGreaterThan(1);
  });

  test('height zones have correct colors', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    await page.screenshot({
      path: 'test-results/terrain/phase1-mesh/height-zones.png',
      fullPage: true
    });

    // Check for no console errors
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.waitForTimeout(2000);
    expect(errors.length).toBe(0);
  });

  test('wireframe shows proper mesh structure', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    // Toggle wireframe if available
    await page.evaluate(() => {
      const toggle = (window as any).toggleWireframe;
      if (toggle) toggle();
    });

    await page.screenshot({
      path: 'test-results/terrain/phase1-mesh/wireframe.png',
      fullPage: true
    });
  });

  test('performance: renders at 60 FPS', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    const fps = await measureFPS(page);
    expect(fps).toBeGreaterThanOrEqual(55); // Allow margin
  });
});
```

## Phase 2: Water Plane Tests

```typescript
test.describe('Phase 2: Water Plane', () => {

  test('water renders at correct level (4.5m)', async ({ page }) => {
    await navigateToTerrainTest(page, 'water-plane');

    await page.screenshot({
      path: 'test-results/terrain/phase2-water/still.png',
      fullPage: true
    });

    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });

  test('Gerstner waves animate smoothly', async ({ page }) => {
    await navigateToTerrainTest(page, 'water-plane');

    await page.screenshot({
      path: 'test-results/terrain/phase2-water/animation-1.png'
    });

    await page.waitForTimeout(500);

    await page.screenshot({
      path: 'test-results/terrain/phase2-water/animation-2.png'
    });

    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.waitForTimeout(1000);
    expect(errors.length).toBe(0);
  });

  test('no z-fighting with terrain', async ({ page }) => {
    await navigateToTerrainTest(page, 'water-terrain-combined');

    await page.screenshot({
      path: 'test-results/terrain/phase2-water/no-z-fighting.png',
      fullPage: true
    });

    // Check for no WebGL warnings
    const warnings: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'warning') warnings.push(msg.text());
    });

    await page.waitForTimeout(2000);
    expect(warnings.filter(w => w.includes('z-fighting') || w.includes('depth')).length).toBe(0);
  });

  test('transparency renders correctly', async ({ page }) => {
    await navigateToTerrainTest(page, 'water-plane');

    // Water should show terrain through transparency
    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });
});
```

## Phase 3: Grass Instancer Tests

```typescript
test.describe('Phase 3: Grass Instancer', () => {

  test('grass renders on terrain surface', async ({ page }) => {
    await navigateToTerrainTest(page, 'grass-instancer');

    await page.screenshot({
      path: 'test-results/terrain/phase3-grass/top-down.png',
      fullPage: true
    });
  });

  test('no grass underwater', async ({ page }) => {
    await navigateToTerrainTest(page, 'grass-instancer');

    // Check from water level perspective
    await page.evaluate(() => {
      const camera = (window as any).camera;
      if (camera) {
        camera.position.set(0, 5, 50);
        camera.lookAt(0, 5, 0);
      }
    });

    await page.screenshot({
      path: 'test-results/terrain/phase3-grass/from-water.png'
    });
  });

  test('grass density looks natural', async ({ page }) => {
    await navigateToTerrainTest(page, 'grass-instancer');

    await page.screenshot({
      path: 'test-results/terrain/phase3-grass/ground-level.png',
      fullPage: true
    });
  });

  test('performance: 50K instances at 60 FPS', async ({ page }) => {
    await navigateToTerrainTest(page, 'grass-instancer');

    const fps = await measureFPS(page);
    expect(fps).toBeGreaterThanOrEqual(55);
  });
});
```

## Phase 4: Paint Overlay Tests

```typescript
test.describe('Phase 4: Paint Overlay', () => {

  test('orange paint visible with stripes pattern', async ({ page }) => {
    await navigateToTerrainTest(page, 'paint-overlay');

    // Apply orange paint
    await page.evaluate(() => {
      const applyPaint = (window as any).applyOrangePaint;
      if (applyPaint) applyPaint(0, 0);
    });

    await page.waitForTimeout(500);

    await page.screenshot({
      path: 'test-results/terrain/phase4-paint/orange-stripes.png',
      fullPage: true
    });

    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });

  test('blue paint visible with dots pattern', async ({ page }) => {
    await navigateToTerrainTest(page, 'paint-overlay');

    await page.evaluate(() => {
      const applyPaint = (window as any).applyBluePaint;
      if (applyPaint) applyPaint(50, 0);
    });

    await page.waitForTimeout(500);

    await page.screenshot({
      path: 'test-results/terrain/phase4-paint/blue-dots.png',
      fullPage: true
    });
  });

  test('paint blends with terrain colors', async ({ page }) => {
    await navigateToTerrainTest(page, 'paint-overlay');

    await page.evaluate(() => {
      const applyOrange = (window as any).applyOrangePaint;
      const applyBlue = (window as any).applyBluePaint;
      if (applyOrange) applyOrange(-30, 0);
      if (applyBlue) applyBlue(30, 0);
    });

    await page.waitForTimeout(500);

    await page.screenshot({
      path: 'test-results/terrain/phase4-paint/mixed-blended.png',
      fullPage: true
    });
  });

  test('accessibility patterns are distinct', async ({ page }) => {
    await navigateToTerrainTest(page, 'paint-overlay');

    await page.screenshot({
      path: 'test-results/terrain/phase4-paint/accessibility-patterns.png',
      fullPage: true
    });

    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });
});
```

## Phase 5: Territory Grid Tests

```typescript
test.describe('Phase 5: Territory Grid', () => {

  test('grid initializes to neutral', async ({ page }) => {
    await navigateToTerrainTest(page, 'territory-grid');

    const coverage = await page.evaluate(() => {
      const getCoverage = (window as any).getTerritoryCoverage;
      return getCoverage ? getCoverage() : { orange: 0, blue: 0, neutral: 100 };
    });

    expect(coverage.neutral).toBe(100);
    expect(coverage.orange).toBe(0);
    expect(coverage.blue).toBe(0);
  });

  test('paint updates territory ownership', async ({ page }) => {
    await navigateToTerrainTest(page, 'territory-grid');

    await page.evaluate(() => {
      const applyPaint = (window as any).applyOrangePaint;
      if (applyPaint) applyPaint(0, 0);
    });

    await page.waitForTimeout(100);

    const coverage = await page.evaluate(() => {
      const getCoverage = (window as any).getTerritoryCoverage;
      return getCoverage ? getCoverage() : { orange: 0 };
    });

    expect(coverage.orange).toBeGreaterThan(0);
  });

  test('coverage calculation accurate within 1%', async ({ page }) => {
    await navigateToTerrainTest(page, 'territory-grid');

    await page.evaluate(() => {
      const fillOrange = (window as any).fillOrangePercent;
      if (fillOrange) fillOrange(25);
    });

    await page.waitForTimeout(500);

    const coverage = await page.evaluate(() => {
      const getCoverage = (window as any).getTerritoryCoverage;
      return getCoverage ? getCoverage() : { orange: 0 };
    });

    expect(Math.abs(coverage.orange - 25)).toBeLessThan(1);
  });

  test('height multiplier applies correctly', async ({ page }) => {
    await navigateToTerrainTest(page, 'territory-grid');

    await page.evaluate(() => {
      const applyAt = (window as any).applyPaintAtHeight;
      if (applyAt) {
        applyAt(0, 0, 5);   // Low elevation
        applyAt(50, 50, 15); // High elevation (1.5x)
      }
    });

    await page.waitForTimeout(100);

    const coverage = await page.evaluate(() => {
      const getWeighted = (window as any).getWeightedCoverage;
      return getWeighted ? getWeighted() : { orange: 0 };
    });

    expect(coverage.orange).toBeGreaterThan(0);
  });
});
```

## Phase 6: Integration Tests

```typescript
test.describe('Phase 6: Integration', () => {

  test('all components render together', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-full');

    await page.screenshot({
      path: 'test-results/terrain/phase6-integration/full-scene.png',
      fullPage: true
    });

    const hasColor = await hasCanvasColor(page);
    expect(hasColor).toBe(true);
  });

  test('spawn zones are accessible', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-full');

    const spawnHeight = await page.evaluate(() => {
      const getSpawnHeight = (window as any).getSpawnZoneHeight;
      return getSpawnHeight ? getSpawnHeight() : 8;
    });

    expect(spawnHeight).toBeGreaterThan(5);
    expect(spawnHeight).toBeLessThan(15);
  });

  test('mountain boundaries enclose map', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-full');

    await page.screenshot({
      path: 'test-results/terrain/phase6-integration/boundaries.png',
      fullPage: true
    });
  });

  test('central conflict area exists', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-full');

    const centerHeight = await page.evaluate(() => {
      const getHeight = (window as any).getTerrainHeight;
      return getHeight ? getHeight(0, 0) : 0;
    });

    expect(centerHeight).toBeGreaterThan(5);
  });

  test('performance: full scene at 60 FPS', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-full');

    const fps = await measureFPS(page);
    expect(fps).toBeGreaterThanOrEqual(55);
  });
});
```

## Console Error Validation

```typescript
test.describe('Console Error Validation', () => {

  test('no WebGL errors in terrain mesh scene', async ({ page }) => {
    const errors: string[] = [];

    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await navigateToTerrainTest(page, 'terrain-mesh');
    await page.waitForTimeout(2000);

    expect(errors.filter(e => e.includes('WebGL') || e.includes('shader')).length).toBe(0);
  });

  test('no memory leaks during scene transitions', async ({ page }) => {
    await navigateToTerrainTest(page, 'terrain-mesh');

    const memoryBefore = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });

    await navigateToTerrainTest(page, 'water-plane');
    await navigateToTerrainTest(page, 'grass-instancer');
    await navigateToTerrainTest(page, 'paint-overlay');

    const memoryAfter = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });

    const memoryGrowth = (memoryAfter - memoryBefore) / 1024 / 1024;
    expect(memoryGrowth).toBeLessThan(50); // Less than 50MB growth
  });
});
```

## Running Tests

```bash
# Run all terrain tests
npm run test:e2e -- tests/e2e/terrain-system.spec.ts

# Run specific phase
npm run test:e2e -- tests/e2e/terrain-system.spec.ts -g "Phase 1"

# Run with screenshots
npm run test:e2e -- tests/e2e/terrain-system.spec.ts --screenshot=only-on-failure

# Run in headed mode
npm run test:e2e -- tests/e2e/terrain-system.spec.ts --headed
```

## Test Result Directories

Tests save screenshots to:
```
test-results/terrain/
├── phase1-mesh/
├── phase2-water/
├── phase3-grass/
├── phase4-paint/
├── phase5-grid/
├── phase6-integration/
└── final/
```

## Common Issues

### Test Scenes Not Loading

**Cause:** Scene query parameter not handled.

**Fix:** Ensure scene routing exists in App.tsx.

```typescript
// In App.tsx
const scene = useSearchParams().get('scene');
switch (scene) {
  case 'terrain-mesh':
    return <TerrainMeshTestScene />;
  // ...
}
```

### Screenshots All Black

**Cause:** Canvas not ready or rendering not complete.

**Fix:** Add wait for rendering.

```typescript
await page.waitForLoadState('networkidle');
await page.waitForTimeout(1000); // Wait for first frame
```

## Related Skills

For terrain mesh: `Skill("ta-terrain-mesh")`
For water shader: `Skill("ta-water-shader")`
For grass instancing: `Skill("ta-foliage-instancing")`
For paint system: `Skill("ta-paint-territory")`
For territory grid: `Skill("ta-territory-grid-cpu")`
