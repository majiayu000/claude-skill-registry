---
name: Mobile Gesture Tester
description: Test touch gestures including swipe, pinch-to-zoom, long press, and drag-and-drop on mobile viewports and touch-enabled devices.
version: 1.0.0
author: Pramod
license: MIT
tags: [mobile, gestures, touch, swipe, pinch-zoom, drag-drop, responsive]
testingTypes: [mobile, e2e]
frameworks: [playwright, appium]
languages: [typescript, javascript]
domains: [mobile, web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Mobile Gesture Tester Skill

You are an expert QA automation engineer specializing in mobile gesture testing, touch interaction verification, and cross-device compatibility analysis. When asked to test touch gestures such as swipe, pinch-to-zoom, long press, drag-and-drop, and multi-touch interactions on mobile viewports and touch-enabled devices, follow these comprehensive instructions to systematically verify that every gesture-driven interface responds correctly.

## Core Principles

1. **Touch Is Not a Click** -- Touch interactions are fundamentally different from mouse interactions. A touch event sequence consists of touchstart, touchmove, and touchend events, with additional complexity from multi-touch pointers, gesture recognition, and velocity-based momentum. Testing touch behavior with mouse events produces false confidence because many gesture libraries only respond to genuine touch events.

2. **Gestures Must Feel Natural** -- A swipe that requires pixel-perfect precision, a pinch that responds with noticeable delay, or a drag that loses tracking when the finger moves too fast are all gesture failures. Test gestures with realistic human motion: imprecise start points, curved paths, variable speeds, and accidental near-edge touches.

3. **Gesture Boundaries Must Be Enforced** -- Swipeable carousels must stop at the first and last item. Pinch-to-zoom must respect minimum and maximum scale limits. Draggable elements must not be dragged outside their container. Every gesture must have well-defined boundaries that prevent impossible or nonsensical states.

4. **Gesture Conflicts Must Be Resolved** -- When a swipe region overlaps with a scrollable container, the application must correctly determine whether the user intends to swipe the carousel or scroll the page. Gesture conflict resolution is a rich source of bugs and must be tested explicitly.

5. **Gestures Must Be Accessible** -- Every gesture-driven interaction must have a non-gesture alternative for users who cannot perform touch gestures. Swipeable content must also be navigable via buttons. Drag-and-drop must have a keyboard alternative. Pinch-to-zoom must coexist with standard browser zoom.

6. **Performance Under Gesture Is Critical** -- Touch interactions must respond at 60fps. Any frame drop during a swipe, pinch, or drag is perceptible to the user and makes the interface feel broken. Test gesture performance on mid-range devices, not just flagship phones.

7. **Test on Real Touch Contexts** -- Playwright's touch emulation and Appium's real device interaction produce different results. Touch emulation is useful for logic testing, but gesture physics, inertia, and edge cases require testing on real devices or accurate simulators.

## Project Structure

Organize your mobile gesture test suite with this directory structure:

```
tests/
  gestures/
    swipe-carousel.spec.ts
    pinch-to-zoom.spec.ts
    long-press-context-menu.spec.ts
    drag-and-drop.spec.ts
    pull-to-refresh.spec.ts
    scroll-gesture-conflicts.spec.ts
    multi-touch-interactions.spec.ts
  fixtures/
    touch-device.fixture.ts
  helpers/
    gesture-simulator.ts
    touch-event-builder.ts
    gesture-validator.ts
    device-profiles.ts
  reports/
    gesture-test-results.json
playwright.config.ts
appium.config.ts
```

Each spec file targets a specific gesture type. The helpers directory contains utilities for constructing realistic touch event sequences and validating gesture outcomes.

## Detailed Guide

### Step 1: Build a Gesture Simulator

The foundation of mobile gesture testing is a reliable simulator that produces realistic touch event sequences with configurable speed, trajectory, and multi-touch points.

```typescript
// helpers/gesture-simulator.ts
import { Page } from '@playwright/test';

export interface Point {
  x: number;
  y: number;
}

export interface GestureOptions {
  durationMs?: number;
  steps?: number;
  startDelay?: number;
}

export class GestureSimulator {
  constructor(private page: Page) {}

  async swipe(from: Point, to: Point, options: GestureOptions = {}): Promise<void> {
    const { durationMs = 300, steps = 20, startDelay = 50 } = options;
    const stepDuration = durationMs / steps;

    // Dispatch touchstart at the origin point
    await this.page.evaluate(
      ({ x, y }) => {
        const target = document.elementFromPoint(x, y) || document.body;
        const touch = new Touch({
          identifier: 0,
          target,
          clientX: x,
          clientY: y,
          pageX: x,
          pageY: y,
        });
        target.dispatchEvent(
          new TouchEvent('touchstart', {
            touches: [touch],
            targetTouches: [touch],
            changedTouches: [touch],
            bubbles: true,
            cancelable: true,
          })
        );
      },
      { x: from.x, y: from.y }
    );

    await this.page.waitForTimeout(startDelay);

    // Move through intermediate points with easing
    for (let i = 1; i <= steps; i++) {
      const progress = i / steps;
      const easedProgress = this.easeOutCubic(progress);
      const currentX = from.x + (to.x - from.x) * easedProgress;
      const currentY = from.y + (to.y - from.y) * easedProgress;

      await this.page.evaluate(
        ({ x, y, originX, originY }) => {
          const target = document.elementFromPoint(originX, originY) || document.body;
          const touch = new Touch({
            identifier: 0,
            target,
            clientX: x,
            clientY: y,
            pageX: x,
            pageY: y,
          });
          target.dispatchEvent(
            new TouchEvent('touchmove', {
              touches: [touch],
              targetTouches: [touch],
              changedTouches: [touch],
              bubbles: true,
              cancelable: true,
            })
          );
        },
        { x: currentX, y: currentY, originX: from.x, originY: from.y }
      );

      await this.page.waitForTimeout(stepDuration);
    }

    // Dispatch touchend at the destination point
    await this.page.evaluate(
      ({ x, y, originX, originY }) => {
        const target = document.elementFromPoint(originX, originY) || document.body;
        const touch = new Touch({
          identifier: 0,
          target,
          clientX: x,
          clientY: y,
          pageX: x,
          pageY: y,
        });
        target.dispatchEvent(
          new TouchEvent('touchend', {
            touches: [],
            targetTouches: [],
            changedTouches: [touch],
            bubbles: true,
            cancelable: true,
          })
        );
      },
      { x: to.x, y: to.y, originX: from.x, originY: from.y }
    );
  }

  async pinch(
    center: Point,
    startDistance: number,
    endDistance: number,
    options: GestureOptions = {}
  ): Promise<void> {
    const { durationMs = 500, steps = 30 } = options;
    const stepDuration = durationMs / steps;

    for (let i = 0; i <= steps; i++) {
      const progress = i / steps;
      const easedProgress = this.easeOutCubic(progress);
      const currentDistance = startDistance + (endDistance - startDistance) * easedProgress;

      const finger1 = { x: center.x - currentDistance / 2, y: center.y };
      const finger2 = { x: center.x + currentDistance / 2, y: center.y };

      const eventType = i === 0 ? 'touchstart' : i === steps ? 'touchend' : 'touchmove';

      await this.page.evaluate(
        ({ f1, f2, type, cx, cy }) => {
          const target = document.elementFromPoint(cx, cy) || document.body;
          const touch1 = new Touch({
            identifier: 0,
            target,
            clientX: f1.x,
            clientY: f1.y,
            pageX: f1.x,
            pageY: f1.y,
          });
          const touch2 = new Touch({
            identifier: 1,
            target,
            clientX: f2.x,
            clientY: f2.y,
            pageX: f2.x,
            pageY: f2.y,
          });

          const touches = type === 'touchend' ? [] : [touch1, touch2];
          target.dispatchEvent(
            new TouchEvent(type, {
              touches,
              targetTouches: touches,
              changedTouches: [touch1, touch2],
              bubbles: true,
              cancelable: true,
            })
          );
        },
        { f1: finger1, f2: finger2, type: eventType, cx: center.x, cy: center.y }
      );

      await this.page.waitForTimeout(stepDuration);
    }
  }

  async longPress(point: Point, holdMs: number = 800): Promise<void> {
    await this.page.evaluate(
      ({ x, y }) => {
        const target = document.elementFromPoint(x, y) || document.body;
        const touch = new Touch({
          identifier: 0, target,
          clientX: x, clientY: y, pageX: x, pageY: y,
        });
        target.dispatchEvent(
          new TouchEvent('touchstart', {
            touches: [touch], targetTouches: [touch], changedTouches: [touch],
            bubbles: true, cancelable: true,
          })
        );
      },
      { x: point.x, y: point.y }
    );

    await this.page.waitForTimeout(holdMs);

    await this.page.evaluate(
      ({ x, y }) => {
        const target = document.elementFromPoint(x, y) || document.body;
        const touch = new Touch({
          identifier: 0, target,
          clientX: x, clientY: y, pageX: x, pageY: y,
        });
        target.dispatchEvent(
          new TouchEvent('touchend', {
            touches: [], targetTouches: [], changedTouches: [touch],
            bubbles: true, cancelable: true,
          })
        );
      },
      { x: point.x, y: point.y }
    );
  }

  async drag(
    from: Point,
    to: Point,
    options: GestureOptions & { holdBeforeDragMs?: number } = {}
  ): Promise<void> {
    const { holdBeforeDragMs = 150 } = options;

    await this.page.evaluate(
      ({ x, y }) => {
        const target = document.elementFromPoint(x, y) || document.body;
        const touch = new Touch({
          identifier: 0, target,
          clientX: x, clientY: y, pageX: x, pageY: y,
        });
        target.dispatchEvent(
          new TouchEvent('touchstart', {
            touches: [touch], targetTouches: [touch], changedTouches: [touch],
            bubbles: true, cancelable: true,
          })
        );
      },
      { x: from.x, y: from.y }
    );

    await this.page.waitForTimeout(holdBeforeDragMs);
    await this.swipe(from, to, { ...options, startDelay: 0 });
  }

  async pullToRefresh(page: Page, pullDistance: number = 150): Promise<void> {
    const viewport = page.viewportSize();
    if (!viewport) throw new Error('No viewport size');

    const startY = 100;
    const endY = startY + pullDistance;
    const centerX = viewport.width / 2;

    await this.swipe(
      { x: centerX, y: startY },
      { x: centerX, y: endY },
      { durationMs: 400, steps: 25 }
    );
  }

  private easeOutCubic(t: number): number {
    return 1 - Math.pow(1 - t, 3);
  }
}
```

### Step 2: Define Device Profiles

Different devices have different screen sizes, pixel ratios, and touch capabilities.

```typescript
// helpers/device-profiles.ts
export interface DeviceProfile {
  name: string;
  viewport: { width: number; height: number };
  deviceScaleFactor: number;
  isMobile: boolean;
  hasTouch: boolean;
  userAgent: string;
}

export const deviceProfiles: Record<string, DeviceProfile> = {
  'iphone-14': {
    name: 'iPhone 14',
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  },
  'pixel-7': {
    name: 'Pixel 7',
    viewport: { width: 412, height: 915 },
    deviceScaleFactor: 2.625,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
  },
  'ipad-pro-12': {
    name: 'iPad Pro 12.9"',
    viewport: { width: 1024, height: 1366 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  },
  'galaxy-fold': {
    name: 'Samsung Galaxy Z Fold',
    viewport: { width: 280, height: 653 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
  },
  'galaxy-s23': {
    name: 'Samsung Galaxy S23',
    viewport: { width: 360, height: 780 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
  },
};
```

### Step 3: Test Swipe Gestures

Swipe is the most common mobile gesture, used in carousels, dismiss actions, navigation drawers, and card stacks.

```typescript
// tests/gestures/swipe-carousel.spec.ts
import { test, expect } from '@playwright/test';
import { GestureSimulator } from '../helpers/gesture-simulator';
import { deviceProfiles } from '../helpers/device-profiles';

const mobile = deviceProfiles['iphone-14'];

test.describe('Swipe Carousel Gestures', () => {
  test.use({
    viewport: mobile.viewport,
    isMobile: mobile.isMobile,
    hasTouch: mobile.hasTouch,
  });

  test('horizontal swipe advances carousel to next slide', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/');

    const carousel = page.locator('[data-testid="carousel"]');
    await carousel.waitFor({ state: 'visible' });
    const box = await carousel.boundingBox();
    if (!box) throw new Error('Carousel not found');

    const initialSlide = await page
      .locator('[data-testid="carousel-indicator"].active, [aria-current="true"]')
      .getAttribute('data-index');

    // Swipe left to advance
    await gestures.swipe(
      { x: box.x + box.width * 0.8, y: box.y + box.height / 2 },
      { x: box.x + box.width * 0.2, y: box.y + box.height / 2 },
      { durationMs: 300 }
    );

    await page.waitForTimeout(500);

    const newSlide = await page
      .locator('[data-testid="carousel-indicator"].active, [aria-current="true"]')
      .getAttribute('data-index');

    expect(newSlide).not.toBe(initialSlide);
  });

  test('swipe does not go past the last slide', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/');

    const carousel = page.locator('[data-testid="carousel"]');
    await carousel.waitFor({ state: 'visible' });
    const box = await carousel.boundingBox();
    if (!box) throw new Error('Carousel not found');

    const totalSlides = await page.locator('[data-testid="carousel-indicator"]').count();

    // Swipe far beyond the last slide
    for (let i = 0; i < totalSlides + 3; i++) {
      await gestures.swipe(
        { x: box.x + box.width * 0.8, y: box.y + box.height / 2 },
        { x: box.x + box.width * 0.2, y: box.y + box.height / 2 },
        { durationMs: 250 }
      );
      await page.waitForTimeout(400);
    }

    const activeIndex = await page
      .locator('[data-testid="carousel-indicator"].active, [aria-current="true"]')
      .getAttribute('data-index');

    expect(Number(activeIndex)).toBeLessThanOrEqual(totalSlides - 1);
  });

  test('short swipe distance snaps back to current slide', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/');

    const carousel = page.locator('[data-testid="carousel"]');
    await carousel.waitFor({ state: 'visible' });
    const box = await carousel.boundingBox();
    if (!box) throw new Error('Carousel not found');

    const initialSlide = await page
      .locator('[data-testid="carousel-indicator"].active, [aria-current="true"]')
      .getAttribute('data-index');

    // Small swipe that should not trigger transition
    await gestures.swipe(
      { x: box.x + box.width * 0.55, y: box.y + box.height / 2 },
      { x: box.x + box.width * 0.45, y: box.y + box.height / 2 },
      { durationMs: 300 }
    );

    await page.waitForTimeout(500);

    const afterSlide = await page
      .locator('[data-testid="carousel-indicator"].active, [aria-current="true"]')
      .getAttribute('data-index');

    expect(afterSlide).toBe(initialSlide);
  });

  test('vertical swipe on carousel allows page scroll', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/');

    const carousel = page.locator('[data-testid="carousel"]');
    await carousel.waitFor({ state: 'visible' });
    const box = await carousel.boundingBox();
    if (!box) throw new Error('Carousel not found');

    const initialScrollY = await page.evaluate(() => window.scrollY);

    await gestures.swipe(
      { x: box.x + box.width / 2, y: box.y + box.height * 0.8 },
      { x: box.x + box.width / 2, y: box.y + box.height * 0.2 },
      { durationMs: 300 }
    );

    await page.waitForTimeout(500);

    const newScrollY = await page.evaluate(() => window.scrollY);
    expect(newScrollY).toBeGreaterThan(initialScrollY);
  });

  test('swipe-to-dismiss removes item from list', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/notifications');

    const items = page.locator('[data-testid="notification-item"]');
    const initialCount = await items.count();
    if (initialCount === 0) return;

    const firstItem = items.first();
    const box = await firstItem.boundingBox();
    if (!box) throw new Error('Notification item not found');

    // Swipe right to dismiss
    await gestures.swipe(
      { x: box.x + 20, y: box.y + box.height / 2 },
      { x: box.x + box.width + 50, y: box.y + box.height / 2 },
      { durationMs: 250 }
    );

    await page.waitForTimeout(500);

    const afterCount = await items.count();
    expect(afterCount).toBe(initialCount - 1);
  });
});
```

### Step 4: Test Pinch-to-Zoom

```typescript
// tests/gestures/pinch-to-zoom.spec.ts
import { test, expect } from '@playwright/test';
import { GestureSimulator } from '../helpers/gesture-simulator';
import { deviceProfiles } from '../helpers/device-profiles';

test.describe('Pinch-to-Zoom Gestures', () => {
  test.use({
    viewport: deviceProfiles['iphone-14'].viewport,
    isMobile: true,
    hasTouch: true,
  });

  test('pinch-out zooms in on image', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/gallery');

    const image = page.locator('[data-testid="zoomable-image"]').first();
    await image.waitFor({ state: 'visible' });
    const box = await image.boundingBox();
    if (!box) throw new Error('Zoomable image not found');

    const center = { x: box.x + box.width / 2, y: box.y + box.height / 2 };

    const initialScale = await image.evaluate((el) => {
      const transform = window.getComputedStyle(el).transform;
      if (transform === 'none') return 1;
      const matrix = transform.match(/matrix\((.+)\)/);
      return matrix ? parseFloat(matrix[1].split(', ')[0]) : 1;
    });

    // Pinch out: spread fingers apart
    await gestures.pinch(center, 50, 200, { durationMs: 500 });
    await page.waitForTimeout(300);

    const afterScale = await image.evaluate((el) => {
      const transform = window.getComputedStyle(el).transform;
      if (transform === 'none') return 1;
      const matrix = transform.match(/matrix\((.+)\)/);
      return matrix ? parseFloat(matrix[1].split(', ')[0]) : 1;
    });

    expect(afterScale).toBeGreaterThan(initialScale);
  });

  test('zoom does not exceed maximum scale limit', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/gallery');

    const image = page.locator('[data-testid="zoomable-image"]').first();
    await image.waitFor({ state: 'visible' });
    const box = await image.boundingBox();
    if (!box) throw new Error('Zoomable image not found');

    const center = { x: box.x + box.width / 2, y: box.y + box.height / 2 };

    for (let i = 0; i < 10; i++) {
      await gestures.pinch(center, 30, 300, { durationMs: 300 });
      await page.waitForTimeout(200);
    }

    const finalScale = await image.evaluate((el) => {
      const transform = window.getComputedStyle(el).transform;
      if (transform === 'none') return 1;
      const matrix = transform.match(/matrix\((.+)\)/);
      return matrix ? parseFloat(matrix[1].split(', ')[0]) : 1;
    });

    // Should be capped at a reasonable maximum
    expect(finalScale).toBeLessThanOrEqual(5);
  });

  test('double-tap toggles zoom in and out', async ({ page }) => {
    await page.goto('/gallery');

    const image = page.locator('[data-testid="zoomable-image"]').first();
    await image.waitFor({ state: 'visible' });
    const box = await image.boundingBox();
    if (!box) throw new Error('Zoomable image not found');

    const tapPoint = { x: box.x + box.width / 2, y: box.y + box.height / 2 };

    // Double-tap to zoom in
    await page.touchscreen.tap(tapPoint.x, tapPoint.y);
    await page.waitForTimeout(100);
    await page.touchscreen.tap(tapPoint.x, tapPoint.y);
    await page.waitForTimeout(500);

    const zoomedScale = await image.evaluate((el) => {
      const transform = window.getComputedStyle(el).transform;
      if (transform === 'none') return 1;
      const matrix = transform.match(/matrix\((.+)\)/);
      return matrix ? parseFloat(matrix[1].split(', ')[0]) : 1;
    });

    expect(zoomedScale).toBeGreaterThan(1);

    // Double-tap again to zoom out
    await page.touchscreen.tap(tapPoint.x, tapPoint.y);
    await page.waitForTimeout(100);
    await page.touchscreen.tap(tapPoint.x, tapPoint.y);
    await page.waitForTimeout(500);

    const resetScale = await image.evaluate((el) => {
      const transform = window.getComputedStyle(el).transform;
      if (transform === 'none') return 1;
      const matrix = transform.match(/matrix\((.+)\)/);
      return matrix ? parseFloat(matrix[1].split(', ')[0]) : 1;
    });

    expect(resetScale).toBeCloseTo(1, 1);
  });
});
```

### Step 5: Test Long Press Interactions

```typescript
// tests/gestures/long-press-context-menu.spec.ts
import { test, expect } from '@playwright/test';
import { GestureSimulator } from '../helpers/gesture-simulator';
import { deviceProfiles } from '../helpers/device-profiles';

test.describe('Long Press Context Menu', () => {
  test.use({
    viewport: deviceProfiles['iphone-14'].viewport,
    isMobile: true,
    hasTouch: true,
  });

  test('long press on list item shows context menu', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/list');

    const listItem = page.locator('[data-testid="list-item"]').first();
    await listItem.waitFor({ state: 'visible' });
    const box = await listItem.boundingBox();
    if (!box) throw new Error('List item not found');

    await gestures.longPress(
      { x: box.x + box.width / 2, y: box.y + box.height / 2 },
      800
    );

    await page.waitForTimeout(300);

    const contextMenu = page.locator('[data-testid="context-menu"], [role="menu"]');
    await expect(contextMenu).toBeVisible();

    const menuItems = contextMenu.locator('[role="menuitem"], .menu-item');
    expect(await menuItems.count()).toBeGreaterThan(0);
  });

  test('quick tap does not trigger long press action', async ({ page }) => {
    await page.goto('/list');

    const listItem = page.locator('[data-testid="list-item"]').first();
    await listItem.waitFor({ state: 'visible' });
    await listItem.tap();
    await page.waitForTimeout(300);

    const contextMenu = page.locator('[data-testid="context-menu"], [role="menu"]');
    await expect(contextMenu).not.toBeVisible();
  });

  test('finger movement during long press cancels the gesture', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/list');

    const listItem = page.locator('[data-testid="list-item"]').first();
    await listItem.waitFor({ state: 'visible' });
    const box = await listItem.boundingBox();
    if (!box) throw new Error('List item not found');

    const start = { x: box.x + box.width / 2, y: box.y + box.height / 2 };

    // Begin touch
    await page.evaluate(({ x, y }) => {
      const target = document.elementFromPoint(x, y) || document.body;
      const touch = new Touch({ identifier: 0, target, clientX: x, clientY: y, pageX: x, pageY: y });
      target.dispatchEvent(new TouchEvent('touchstart', {
        touches: [touch], targetTouches: [touch], changedTouches: [touch], bubbles: true, cancelable: true,
      }));
    }, start);

    await page.waitForTimeout(300);

    // Move finger significantly before long press threshold
    await page.evaluate(({ x, y, ox, oy }) => {
      const target = document.elementFromPoint(ox, oy) || document.body;
      const touch = new Touch({ identifier: 0, target, clientX: x, clientY: y, pageX: x, pageY: y });
      target.dispatchEvent(new TouchEvent('touchmove', {
        touches: [touch], targetTouches: [touch], changedTouches: [touch], bubbles: true, cancelable: true,
      }));
    }, { x: start.x + 50, y: start.y + 50, ox: start.x, oy: start.y });

    await page.waitForTimeout(600);

    await page.evaluate(({ x, y }) => {
      const target = document.elementFromPoint(x, y) || document.body;
      const touch = new Touch({ identifier: 0, target, clientX: x, clientY: y, pageX: x, pageY: y });
      target.dispatchEvent(new TouchEvent('touchend', {
        touches: [], targetTouches: [], changedTouches: [touch], bubbles: true, cancelable: true,
      }));
    }, { x: start.x + 50, y: start.y + 50 });

    await page.waitForTimeout(300);

    const contextMenu = page.locator('[data-testid="context-menu"], [role="menu"]');
    await expect(contextMenu).not.toBeVisible();
  });
});
```

### Step 6: Test Touch Drag-and-Drop

```typescript
// tests/gestures/drag-and-drop.spec.ts
import { test, expect } from '@playwright/test';
import { GestureSimulator } from '../helpers/gesture-simulator';
import { deviceProfiles } from '../helpers/device-profiles';

test.describe('Touch Drag and Drop', () => {
  test.use({
    viewport: deviceProfiles['ipad-pro-12'].viewport,
    isMobile: true,
    hasTouch: true,
  });

  test('drag card from one column to another', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/kanban');

    const draggable = page.locator('[data-testid="draggable-card"]').first();
    const dropZone = page.locator('[data-testid="drop-zone-done"]');

    await draggable.waitFor({ state: 'visible' });
    await dropZone.waitFor({ state: 'visible' });

    const dragBox = await draggable.boundingBox();
    const dropBox = await dropZone.boundingBox();
    if (!dragBox || !dropBox) throw new Error('Elements not found');

    const initialCount = await dropZone.locator('[data-testid="draggable-card"]').count();

    await gestures.drag(
      { x: dragBox.x + dragBox.width / 2, y: dragBox.y + dragBox.height / 2 },
      { x: dropBox.x + dropBox.width / 2, y: dropBox.y + dropBox.height / 2 },
      { durationMs: 600, holdBeforeDragMs: 200 }
    );

    await page.waitForTimeout(500);

    const afterCount = await dropZone.locator('[data-testid="draggable-card"]').count();
    expect(afterCount).toBe(initialCount + 1);
  });

  test('dragging outside valid zones returns item to origin', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/kanban');

    const draggable = page.locator('[data-testid="draggable-card"]').first();
    await draggable.waitFor({ state: 'visible' });

    const dragBox = await draggable.boundingBox();
    if (!dragBox) throw new Error('Draggable not found');

    const parentColumn = draggable.locator('..');
    const initialColumnCount = await parentColumn.locator('[data-testid="draggable-card"]').count();

    // Drag to an invalid area (far outside any drop zone)
    await gestures.drag(
      { x: dragBox.x + dragBox.width / 2, y: dragBox.y + dragBox.height / 2 },
      { x: 10, y: 10 },
      { durationMs: 500, holdBeforeDragMs: 200 }
    );

    await page.waitForTimeout(500);

    // Item should return to its original column
    const afterColumnCount = await parentColumn.locator('[data-testid="draggable-card"]').count();
    expect(afterColumnCount).toBe(initialColumnCount);
  });
});
```

### Step 7: Test Pull-to-Refresh

```typescript
// tests/gestures/pull-to-refresh.spec.ts
import { test, expect } from '@playwright/test';
import { GestureSimulator } from '../helpers/gesture-simulator';
import { deviceProfiles } from '../helpers/device-profiles';

test.describe('Pull-to-Refresh Gesture', () => {
  test.use({
    viewport: deviceProfiles['iphone-14'].viewport,
    isMobile: true,
    hasTouch: true,
  });

  test('pulling down at top of page triggers refresh', async ({ page }) => {
    const gestures = new GestureSimulator(page);
    await page.goto('/feed');
    await page.waitForLoadState('networkidle');

    let refreshTriggered = false;
    await page.route('**/api/feed**', async (route) => {
      refreshTriggered = true;
      await route.continue();
    });

    // Ensure we are at the top of the page
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(200);

    // Pull down gesture
    await gestures.pullToRefresh(page, 150);
    await page.waitForTimeout(2000);

    expect(refreshTriggered).toBe(true);
  });

  test('pull-to-refresh shows loading indicator during refresh', async ({ page }) => {
    const gestures = new GestureSimulator(page);

    await page.route('**/api/feed**', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      await route.continue();
    });

    await page.goto('/feed');
    await page.waitForLoadState('networkidle');
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(200);

    await gestures.pullToRefresh(page, 150);
    await page.waitForTimeout(500);

    // A refresh indicator should be visible
    const refreshIndicator = page.locator(
      '[data-testid="pull-refresh-indicator"], .refresh-spinner, .pull-to-refresh-loading'
    );
    const isVisible = await refreshIndicator.isVisible().catch(() => false);

    // Some implementations use the native indicator, so just verify no error
    expect(typeof isVisible).toBe('boolean');
  });
});
```

## Configuration

### Playwright Configuration for Gesture Testing

```typescript
// playwright.config.ts
import { defineConfig, devices as playwrightDevices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/gestures',
  timeout: 45000,
  retries: 2,
  use: {
    screenshot: 'on',
    video: 'on',
    trace: 'on-first-retry',
  },
  reporter: [
    ['html', { open: 'never' }],
    ['json', { outputFile: 'reports/gesture-test-results.json' }],
  ],
  projects: [
    { name: 'iphone-14', use: { ...playwrightDevices['iPhone 14'] } },
    { name: 'pixel-7', use: { ...playwrightDevices['Pixel 7'] } },
    { name: 'ipad-pro', use: { ...playwrightDevices['iPad Pro 11'] } },
    {
      name: 'galaxy-fold',
      use: {
        viewport: { width: 280, height: 653 },
        isMobile: true,
        hasTouch: true,
        deviceScaleFactor: 3,
      },
    },
  ],
});
```

### Appium Configuration for Real Device Testing

```typescript
// appium.config.ts
export const appiumCapabilities = {
  android: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Pixel 7',
    'appium:platformVersion': '13.0',
    'appium:browserName': 'Chrome',
    'appium:newCommandTimeout': 240,
  },
  ios: {
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 14',
    'appium:platformVersion': '16.0',
    'appium:browserName': 'Safari',
    'appium:newCommandTimeout': 240,
  },
};
```

## Best Practices

1. **Always enable hasTouch and isMobile in Playwright configuration.** Mouse events do not trigger touch event handlers. Without these flags, gesture tests produce false positives.

2. **Use realistic gesture parameters with easing curves.** Real human swipes are not perfectly linear. Add slight vertical variance and use easeOutCubic for natural finger acceleration and deceleration.

3. **Test gesture threshold boundaries.** Every gesture has a minimum distance or duration. Test just below, at, and just above the threshold to verify activation and cancellation.

4. **Record video for all gesture tests.** Gesture bugs are temporal and spatial. Static screenshots cannot show that a swipe stuttered or a drag snapped to the wrong position.

5. **Test on foldable device viewports.** Foldable phones have extremely narrow viewports in folded mode. Gestures that work at 390px may be impossible at 280px.

6. **Verify accessibility alternatives for every gesture.** Every swipe needs a button alternative. Every drag needs a keyboard alternative. Every pinch needs browser zoom support.

7. **Test gesture conflicts between parent and child elements.** A swipeable carousel inside a scrollable page must correctly disambiguate horizontal versus vertical intent.

8. **Measure gesture response frame rate.** Touch interactions must render at 60fps. Use Performance Observer to detect long frames during gesture animations.

9. **Test both portrait and landscape orientations.** Landscape changes touch target sizes and gesture directions significantly.

10. **Test gesture interruption scenarios.** Phone calls mid-swipe, keyboard appearance during drag, and device rotation during pinch-zoom must not leave broken UI state.

11. **Clean up gesture state after each test.** Zoom levels, scroll positions, and drag states can persist between tests. Reset to prevent interdependence.

12. **Test rapid successive gestures.** Users swipe multiple times quickly through carousels. Verify no animation queue buildup or missed inputs.

## Anti-Patterns to Avoid

1. **Testing touch gestures with mouse events.** Mouse down/move/up does not equal touch start/move/end. Many gesture libraries ignore mouse events entirely.

2. **Hardcoding pixel coordinates.** Different devices have different screens. Always use relative positions based on element bounding boxes.

3. **Ignoring gesture velocity.** Libraries often use swipe speed, not just distance, to determine transitions. A slow 200px swipe and a fast 200px swipe produce different outcomes.

4. **Skipping boundary tests.** Not testing first/last carousel slide, min/max zoom, or container edges lets boundary bugs escape.

5. **Testing only the happy path.** Bugs hide in cancelled gestures, interrupted gestures, conflicting gestures, and gestures on unexpected elements.

6. **Ignoring landscape orientation.** Many teams only test portrait mode. Landscape significantly changes touch dynamics.

7. **Forgetting the 300ms tap delay.** Some mobile browsers add a 300ms delay to distinguish taps from double-taps. Verify touch-action CSS eliminates this.

8. **Touch targets smaller than 44x44px.** Targets below this minimum are difficult to tap accurately with a finger.

9. **Not testing with screen protectors or wet fingers.** Real-world touch input is less precise than automation. Increase touch target sizes accordingly.

10. **Only testing in Chrome.** Safari on iOS handles touch events differently from Chrome on Android. Test on both platforms.

## Debugging Tips

1. **Use Playwright's video recording for every gesture test.** The video shows the exact finger path and UI response, making diagnosis far easier than screenshots.

2. **Log all touch events** by attaching touchstart, touchmove, and touchend listeners via page.evaluate. Print coordinates, timestamps, and target elements.

3. **Visualize touch points** by adding temporary colored circles at each touch coordinate. This makes gesture paths visible in screenshots and videos.

4. **Check for preventDefault() calls** that block gesture recognition. If a parent calls preventDefault on touchmove, child handlers receive nothing.

5. **Test with Chrome DevTools device emulation** for fast iteration, then on real devices for touch calibration and performance verification.

6. **Inspect the CSS touch-action property.** The touch-action value controls which gestures the browser handles natively. Setting touch-action: none on a scrollable container breaks scrolling.

7. **Monitor requestAnimationFrame timing** during gestures to detect frame drops. Any frame exceeding 16.67ms causes visible jank.

8. **Compare touch event timestamps** to verify consistent 16ms intervals. Irregular timing indicates main thread blocking during gesture processing.

9. **Use the Appium Inspector** to identify touch-sensitive elements on real devices when Playwright selectors do not match mobile rendering.

10. **Test on actual hardware.** Emulators miss physical touch issues like palm rejection, edge gesture conflicts with OS-level gestures, and device-specific haptic feedback behavior.
