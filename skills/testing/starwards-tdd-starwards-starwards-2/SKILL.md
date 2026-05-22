---
name: starwards-tdd
description: Test-driven development for Starwards - write the test first, watch it fail, write minimal code to pass; includes Jest unit tests, Playwright E2E tests, Colyseus state sync, @gameField decorators, Tweakpane UI, and multiplayer scenarios
version: 2025-11-04
related_skills:
  - starwards-debugging (when tests fail unexpectedly)
  - starwards-verification (verify all tests pass before completion)
  - starwards-monorepo (understand build workflow)
  - starwards-colyseus (test state sync patterns)
  - using-superpowers (announce skill usage)
---

# Test-Driven Development for Starwards

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** "If you didn't watch the test fail, you don't know if it tests the right thing."

**Starwards-specific:** Test state sync, decorators, multiplayer scenarios, and UI interactions.

## When to Use

**Always:**
- New ship systems (@gameField decorators)
- New space objects (Spaceship, Projectile, etc.)
- Bug fixes in game logic
- UI widget changes (Tweakpane panels)
- Multiplayer scenarios (Colyseus state sync)
- Command handlers (JSON Pointer or typed commands)

**Exceptions (ask first):**
- Throwaway prototypes
- Configuration files
- Static assets

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

**Violating the letter of the rules is violating the spirit of the rules.**

## Starwards Test Types

### 1. Unit Tests (Jest) - `modules/*/test/*.spec.ts`

**For:** Game logic, state managers, utility functions

**Run:** `npm test` (all) or `npm test -- modules/core/test/specific.spec.ts`

**Pattern:**
```typescript
// modules/core/test/shield.spec.ts
import { Shield } from '../src/ship/shield';

describe('Shield', () => {
  test('recharges at design rate', () => {
    const shield = new Shield();
    shield.strength = 500;
    shield.design.rechargeRate = 100;

    // Simulate 1 second update
    shield.strength += shield.design.rechargeRate * 1.0;

    expect(shield.strength).toBeCloseTo(600, 1);
  });
});
```

### 2. Integration Tests (Jest + Test Harness) - `modules/*/test/*.spec.ts`

**For:** Ship systems interaction, multiplayer scenarios, state sync

**Use:** `ShipTestHarness` or `MultiClientDriver` from `docs/testing/UTILITIES.md`

**Pattern:**
```typescript
// modules/core/test/shield-sync.spec.ts
import { ShipTestHarness } from './ship-test-harness';

describe('Shield state sync', () => {
  test('strength syncs to all clients', async () => {
    const harness = new ShipTestHarness();
    await harness.connect();

    // Change shield strength server-side
    harness.shipManager.state.shield.strength = 750;

    // Wait for sync
    await harness.waitForSync();

    // Verify client received update
    expect(harness.shipDriver.state.shield.strength).toBe(750);

    await harness.cleanup();
  });
});
```

### 3. E2E Tests (Playwright) - `modules/e2e/test/*.spec.ts`

**For:** UI interactions, Tweakpane panels, visual verification

**Run:** `npm run test:e2e` or `npm run test:e2e -- --headed`

**Pattern:**
```typescript
// modules/e2e/test/shield-panel.spec.ts
import { test, expect } from '@playwright/test';
import { createTestClient } from './test-infrastructure';

test('shield power slider updates strength', async ({ page }) => {
  const client = await createTestClient(page);

  // Locate shield panel by data-id
  const shieldPanel = page.locator('[data-id="Shield Status"]');
  await expect(shieldPanel).toBeVisible();

  // Get initial strength
  const initialStrength = await getPropertyValue(page, 'strength', 'Shield Status');

  // Adjust power slider
  await shieldPanel.locator('.tp-slider').fill('0.5');

  // Wait for state update
  await page.waitForTimeout(100);

  // Verify strength changed
  const newStrength = await getPropertyValue(page, 'strength', 'Shield Status');
  expect(newStrength).not.toBe(initialStrength);

  await client.cleanup();
});
```

## Red-Green-Refactor: Starwards Examples

### Example 1: New Ship System with @gameField

**RED - Write Failing Test:**
```typescript
// modules/core/test/shield.spec.ts
import { Shield } from '../src/ship/shield';

describe('Shield', () => {
  test('has max strength from design', () => {
    const shield = new Shield();
    shield.design.maxStrength = 1000;

    expect(shield.strength).toBeLessThanOrEqual(shield.design.maxStrength);
  });
});
```

**Verify RED:**
```bash
$ npm test -- modules/core/test/shield.spec.ts
FAIL: Cannot find module '../src/ship/shield'
```
Good! Test fails because Shield doesn't exist.

**GREEN - Minimal Code:**
```typescript
// modules/core/src/ship/shield.ts
import { SystemState, DesignState } from './system';
import { gameField } from '../game-field';
import { range } from '../range';

class ShieldDesign extends DesignState {
  @gameField('float32') maxStrength = 1000;
}

export class Shield extends SystemState {
  @gameField(ShieldDesign) design = new ShieldDesign();
  @gameField('float32')
  @range((t: Shield) => [0, t.design.maxStrength])
  strength = 1000;
}
```

**Verify GREEN:**
```bash
$ npm test -- modules/core/test/shield.spec.ts
PASS ✓ Shield > has max strength from design
```

**REFACTOR:** Extract common system patterns if needed.

### Example 2: Multiplayer State Sync

**RED - Write Failing Test:**
```typescript
// modules/core/test/shield-command.spec.ts
import { ShipTestHarness } from './ship-test-harness';

describe('Shield power command', () => {
  test('syncs shield power to clients', async () => {
    const harness = new ShipTestHarness();
    await harness.connect();

    // Send command from client
    harness.shipDriver.room.send({
      type: '/Spaceship/ship-0/shield/power',
      value: 0.5
    });

    await harness.waitForSync();

    // Verify server received update
    expect(harness.shipManager.state.shield.power).toBe(0.5);

    await harness.cleanup();
  });
});
```

**Verify RED:**
```bash
$ npm test -- modules/core/test/shield-command.spec.ts
FAIL: Property 'shield' does not exist on ShipState
```

**GREEN - Add to ShipState:**
```typescript
// modules/core/src/ship/ship-state.ts
@gameField(Shield) shield!: Shield;
```

**Verify GREEN:**
```bash
$ npm test -- modules/core/test/shield-command.spec.ts
PASS ✓ Shield power command > syncs shield power to clients
```

### Example 3: Tweakpane UI Widget

**RED - Write E2E Test:**
```typescript
// modules/e2e/test/shield-widget.spec.ts
import { test, expect } from '@playwright/test';
import { createTestClient } from './test-infrastructure';

test('shield widget displays current strength', async ({ page }) => {
  const client = await createTestClient(page);

  // Navigate to ship screen with shield widget
  await page.goto('http://localhost:3000/#/ship/ship-0');

  // Find shield panel by data-id
  const shieldPanel = page.locator('[data-id="Shield Status"]');
  await expect(shieldPanel).toBeVisible();

  // Check strength label exists
  await expect(shieldPanel.locator('label:has-text("strength")')).toBeVisible();

  await client.cleanup();
});
```

**Verify RED:**
```bash
$ npm run test:e2e -- shield-widget.spec.ts
FAIL: Locator not found: [data-id="Shield Status"]
```

**GREEN - Create Widget:**
```typescript
// modules/browser/src/widgets/shield.ts
import { createPane } from '../panel/blades';
import { ShipDriver } from '@starwards/core';

export function renderShield(ship: ShipDriver, container: HTMLElement) {
  const pane = createPane({
    title: 'Shield Status',
    container
  });

  const shield = ship.state.shield;

  pane.addBinding(shield, 'strength', {
    readonly: true,
    label: 'strength'
  });

  return container;
}
```

**Register widget in Dashboard, rebuild, verify GREEN.**

## Starwards-Specific Patterns

### Testing @gameField Decorators

```typescript
test('@gameField syncs float32 values', () => {
  const shield = new Shield();
  shield.strength = 123.456789;

  // Float32 precision loss expected
  expect(shield.strength).toBeCloseTo(123.46, 1);
});
```

### Testing @range Constraints

```typescript
test('@range clamps shield strength to design max', () => {
  const shield = new Shield();
  shield.design.maxStrength = 1000;
  shield.strength = 1500; // Exceeds max

  // @range decorator should clamp
  expect(shield.strength).toBe(1000);
});
```

### Testing Multiplayer with MultiClientDriver

```typescript
import { MultiClientDriver } from '@starwards/server/test/multi-client-driver';

test('multiple clients see same shield state', async () => {
  const driver = new MultiClientDriver();
  await driver.start();

  const [client1, client2] = await Promise.all([
    driver.joinShip('ship-1'),
    driver.joinShip('ship-1')
  ]);

  // Change shield on server
  driver.getShipManager('ship-1').state.shield.strength = 800;

  await driver.waitForSync();

  // Both clients see update
  expect(client1.state.shield.strength).toBe(800);
  expect(client2.state.shield.strength).toBe(800);

  await driver.cleanup();
});
```

### Testing UI with Page Object Pattern

```typescript
class ShieldPanelPage {
  constructor(private page: Page) {}

  async setPower(value: number) {
    const slider = this.page.locator('[data-id="Shield Status"] .tp-slider');
    await slider.fill(value.toString());
  }

  async getStrength(): Promise<number> {
    return getPropertyValue(this.page, 'strength', 'Shield Status');
  }
}

test('adjusting shield power affects strength', async ({ page }) => {
  const client = await createTestClient(page);
  const shieldPanel = new ShieldPanelPage(page);

  await shieldPanel.setPower(0.5);
  await page.waitForTimeout(100);

  const strength = await shieldPanel.getStrength();
  expect(strength).toBeGreaterThan(0);

  await client.cleanup();
});
```

## Verification Commands

**Unit tests:**
```bash
npm test                                           # All tests
npm test -- modules/core/test/shield.spec.ts      # Specific file
npm test -- --testNamePattern="shield recharge"   # Specific test
npm test -- --watch                               # Watch mode
```

**E2E tests:**
```bash
npm run test:e2e                                   # Headless
npm run test:e2e -- --headed                       # With browser
npm run test:e2e -- shield-widget.spec.ts          # Specific file
npm run test:e2e -- --update-snapshots             # Update screenshots
```

**Full verification:**
```bash
npm run test:types    # TypeScript check
npm run test:format   # ESLint + Prettier
npm test              # Unit tests
npm run test:e2e      # E2E tests
```

## Common Starwards Test Patterns

### Float Precision
```typescript
// WRONG
expect(state.speed).toBe(123.456789);

// CORRECT
expect(state.speed).toBeCloseTo(123.46, 1);
```

### Angle Wrapping
```typescript
test('angle wraps at 360°', () => {
  ship.angle = 370;
  expect(ship.angle).toBe(10); // toPositiveDegreesDelta
});
```

### Velocity Zero Check
```typescript
// WRONG
expect(ship.velocity.x === 0 && ship.velocity.y === 0).toBe(true);

// CORRECT
expect(XY.isZero(ship.velocity, 0.01)).toBe(true);
```

### System Effectiveness
```typescript
test('broken system has 0 effectiveness', () => {
  shield.broken = true;
  expect(shield.effectiveness).toBe(0);
});

test('hacked system reduces effectiveness', () => {
  shield.hacked = 0.3;
  shield.power = 1.0;

  const expected = 1.0 * (1 - 0.3); // power × (1 - hacked)
  expect(shield.effectiveness).toBeCloseTo(expected, 2);
});
```

## Monorepo Testing Considerations

**Run tests from root:**
```bash
npm test                    # Runs all module tests
npm test -- --projects=core # Only core module
```

**Module-specific:**
```bash
cd modules/core && npm test
cd modules/server && npm test
```

**Watch during development:**
```bash
# Terminal 1: Build core on change
cd modules/core && npm run build:watch

# Terminal 2: Run tests on change
npm test -- --watch
```

## Integration with Other Skills

- **systematic-debugging** - Use when tests fail unexpectedly
- **verification-before-completion** - Run full test suite before claiming done
- **starwards-monorepo** - Understand workspace test organization

## Common Rationalizations - STOP

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately (didn't watch it fail)
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- Skipping Playwright tests for UI changes
- Not using ShipTestHarness for multiplayer tests
- Mocking Colyseus state sync instead of testing it
- "I'll add E2E tests later" for new widgets

**All of these mean: Delete code. Start over with TDD.**

## Final Rule

```
Production code → test exists and failed first
UI widget → E2E test exists and failed first
Multiplayer feature → integration test with harness exists and failed first
Otherwise → not TDD
```

No exceptions.
