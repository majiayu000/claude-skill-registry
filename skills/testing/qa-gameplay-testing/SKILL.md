---
name: qa-gameplay-testing
description: E2E gameplay testing patterns using Playwright API. Tests continuous movement, mouse control, and complete gameplay loops. Use when validating game controls, combat mechanics, and player interactions.
category: validation
---

# Gameplay Testing with E2E Tests

> "Game controls must be tested with continuous input patterns, not single keypresses."

## When to Use This Skill

Use for **every game feature validation** to create E2E tests for:

- Character movement (WASD, arrow keys)
- Mouse aiming and interaction
- Combat mechanics and combos
- Special actions (jump, crouch, interact)
- UI navigation (menus, inventory, map)
- Complete gameplay loops

## MANDATORY: Port Detection Before Browser Testing

**⚠️ CRITICAL: Vite dev server may run on different ports (3000, 3001, 5173, 8080, etc.)**

**Before ANY browser interaction, ALWAYS detect the correct port:**

```bash
# Method 1: Check listening ports
netstat -an | grep LISTEN | grep -E ":(3000|3001|5173|8080)"

# Method 2: Try curl to detect Vite
curl -s http://localhost:3000 | grep -q "vite" && echo "PORT=3000" || \
curl -s http://localhost:3001 | grep -q "vite" && echo "PORT=3001" || \
curl -s http://localhost:5173 | grep -q "vite" && echo "PORT=5173"
```

**NOTE:** E2E tests configured in `playwright.config.ts` use `baseURL: 'http://localhost:3000'` which works for most cases. The `webServer` configuration automatically starts the dev server on the correct port.

**For manual testing or MCP validation, detect the port first and use `http://localhost:{detectedPort}`.**

## Core Principle: Write Test Code, Don't Use MCP

**❌ OLD APPROACH (Do NOT do this):**

```typescript
// Interactive MCP - NO!
mcp__playwright__browser_navigate('http://localhost:3000');
mcp__playwright__browser_press_key({ key: 'KeyW' });
```

**✅ NEW APPROACH (Do this):**

```typescript
// Write E2E test - YES!
test('player can move forward', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');

  // Continuous movement - down, wait, up
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(1000);
  await page.keyboard.up('KeyW');

  // Verify position changed
  const position = await page.evaluate(() => (window as any).playerPosition);
  expect(position.z).not.toBe(0);
});
```

## E2E Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Gameplay - Movement', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForSelector('canvas');
    await page.click('canvas'); // Focus game
  });

  test('should move forward with W key', async ({ page }) => {
    // Test implementation
  });

  test('should strafe left with A key', async ({ page }) => {
    // Test implementation
  });
});
```

## Continuous Movement Patterns

### Critical Pattern: Key Down/Up

**Single `press()` only simulates a quick tap. Use `down()` + `waitForTimeout()` + `up()` for continuous movement.**

### Basic WASD Movement

```typescript
test.describe('WASD Movement', () => {
  test('should move forward', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    // Forward movement
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyW');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.z).toBeLessThan(initialPos.z); // Moved forward (negative Z)
  });

  test('should move backward', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    await page.keyboard.down('KeyS');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyS');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.z).toBeGreaterThan(initialPos.z); // Moved backward
  });

  test('should strafe left', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    await page.keyboard.down('KeyA');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyA');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.x).toBeLessThan(initialPos.x); // Moved left (negative X)
  });

  test('should strafe right', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    await page.keyboard.down('KeyD');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyD');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.x).toBeGreaterThan(initialPos.x); // Moved right
  });
});
```

### Diagonal Movement

```typescript
test.describe('Diagonal Movement', () => {
  test('should move forward-left diagonally', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    // Forward-left diagonal
    await page.keyboard.down('KeyW');
    await page.keyboard.down('KeyA');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyA');
    await page.keyboard.up('KeyW');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.x).toBeLessThan(initialPos.x); // Left
    expect(afterPos.z).toBeLessThan(initialPos.z); // Forward
  });

  test('should move forward-right diagonally', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    await page.keyboard.down('KeyW');
    await page.keyboard.down('KeyD');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyD');
    await page.keyboard.up('KeyW');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    expect(afterPos.x).toBeGreaterThan(initialPos.x); // Right
    expect(afterPos.z).toBeLessThan(initialPos.z); // Forward
  });
});
```

### Sprint/Run Combinations

```typescript
test.describe('Sprint Movement', () => {
  test('should sprint forward', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    // Sprint forward (Shift + W)
    await page.keyboard.down('ShiftLeft');
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyW');
    await page.keyboard.up('ShiftLeft');

    const afterPos = await page.evaluate(
      () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
    );

    // Sprint should cover more distance than walking
    expect(Math.abs(afterPos.z - initialPos.z)).toBeGreaterThan(5);
  });

  test('should sprint diagonally', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    await page.keyboard.down('ShiftLeft');
    await page.keyboard.down('KeyW');
    await page.keyboard.down('KeyD');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyD');
    await page.keyboard.up('KeyW');
    await page.keyboard.up('ShiftLeft');

    // Verify diagonal sprint worked
    const position = await page.evaluate(() => (window as any).playerPosition);
    expect(position.x).toBeGreaterThan(0);
    expect(position.z).toBeLessThan(0);
  });
});
```

### Crouch Movement

```typescript
test.describe('Crouch Movement', () => {
  test('should crouch forward', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialHeight = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Crouch while moving
    await page.keyboard.down('ControlLeft');
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyW');
    await page.keyboard.up('ControlLeft');

    const afterHeight = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Player should be lower when crouching
    expect(afterHeight).toBeLessThanOrEqual(initialHeight);
  });

  test('should crouch in place', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialHeight = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    await page.keyboard.down('ControlLeft');
    await page.waitForTimeout(500);
    await page.keyboard.up('ControlLeft');

    const afterHeight = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    expect(afterHeight).toBeLessThan(initialHeight);
  });
});
```

## Mouse Control Patterns

### Aiming

```typescript
test.describe('Mouse Aiming', () => {
  test('should aim with mouse movement', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Get initial camera rotation
    const initialRotation = await page.evaluate(() => (window as any).cameraRotation || { y: 0 });

    // Move mouse (simulates looking around)
    await page.mouse.move(500, 300);
    await page.waitForTimeout(100);

    // Check camera rotated
    const afterRotation = await page.evaluate(() => (window as any).cameraRotation || { y: 0 });

    expect(afterRotation.y).not.toBe(initialRotation.y);
  });

  test('should use pointer lock for camera control', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.waitForSelector('canvas');

    // Check pointer lock is active
    const isLocked = await page.evaluate(() => {
      return document.pointerLockElement === document.body;
    });

    expect(isLocked).toBe(true);

    // Movement should affect camera when locked
    const initialRotation = await page.evaluate(() => (window as any).cameraRotation?.y || 0);

    await page.mouse.move(500, 300);
    await page.waitForTimeout(100);

    const afterRotation = await page.evaluate(() => (window as any).cameraRotation?.y || 0);

    expect(afterRotation).not.toBe(initialRotation);
  });
});
```

### Clicking

```typescript
test.describe('Mouse Click Actions', () => {
  test('should shoot on left click', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialAmmo = await page.evaluate(() => (window as any).playerState?.ammo || 0);

    // Left click to shoot
    await page.mouse.click(400, 300, { button: 'left' });
    await page.waitForTimeout(100);

    const afterAmmo = await page.evaluate(() => (window as any).playerState?.ammo || 0);

    expect(afterAmmo).toBeLessThan(initialAmmo);
  });

  test('should perform alt action on right click', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Right click for secondary action
    await page.mouse.click(400, 300, { button: 'right' });

    // Verify secondary action occurred
    const actionState = await page.evaluate(
      () => (window as any).playerState?.secondaryActionActive || false
    );

    expect(actionState).toBe(true);
  });

  test('should handle charged attack', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Hold left button for charge
    await page.mouse.down({ button: 'left' });
    await page.waitForTimeout(1000); // Charge for 1 second
    await page.mouse.up({ button: 'left' });

    // Verify charged attack fired
    const attackType = await page.evaluate(() => (window as any).lastAttackType || 'none');

    expect(attackType).toBe('charged');
  });
});
```

## Special Keys

### Jump

```typescript
test.describe('Jump Actions', () => {
  test('should jump on space', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Press space to jump
    await page.keyboard.press('Space');
    await page.waitForTimeout(500);

    const peakY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    expect(peakY).toBeGreaterThan(initialY);
  });

  test('should vary jump height with hold duration', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Short tap = short jump
    await page.keyboard.press('Space');
    await page.waitForTimeout(300);
    const shortJumpY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Reset to ground
    await page.keyboard.press('KeyS');
    await page.waitForTimeout(500);
    await page.keyboard.up('KeyS');

    // Long hold = higher jump
    await page.keyboard.down('Space');
    await page.waitForTimeout(300);
    await page.keyboard.up('Space');
    await page.waitForTimeout(200);
    const longJumpY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Long jump should go higher
    expect(longJumpY).toBeGreaterThan(shortJumpY);
  });
});
```

### Interact Keys

```typescript
test.describe('Interaction Keys', () => {
  test('should interact with E key', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Move near interactable
    await page.click('canvas');
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(1000);
    await page.keyboard.up('KeyW');

    const beforeInteract = await page.evaluate(
      () => (window as any).nearbyInteractable?.activated || false
    );

    // Press E to interact
    await page.keyboard.press('KeyE');
    await page.waitForTimeout(100);

    const afterInteract = await page.evaluate(
      () => (window as any).nearbyInteractable?.activated || false
    );

    expect(afterInteract).toBe(true);
  });

  test('should hold interact for long actions', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Hold E for long interaction
    await page.keyboard.down('KeyE');
    await page.waitForTimeout(2000);
    await page.keyboard.up('KeyE');

    // Verify long interaction completed
    const interactionComplete = await page.evaluate(
      () => (window as any).longInteractionComplete || false
    );

    expect(interactionComplete).toBe(true);
  });
});
```

### Menu/UI Keys

```typescript
test.describe('Menu Keys', () => {
  test('should pause game on Escape', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Press Escape to pause
    await page.keyboard.press('Escape');

    // Check for paused state
    const isPaused = await page.evaluate(() => (window as any).gameState?.paused || false);

    expect(isPaused).toBe(true);

    // Check for PAUSED overlay
    const pausedText = await page.locator('text=PAUSED').isVisible();
    expect(pausedText).toBe(true);
  });

  test('should show scoreboard on Tab', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Press Tab for scoreboard
    await page.keyboard.down('Tab');
    await page.waitForTimeout(100);

    const scoreboardVisible = await page.getByTestId('scoreboard').isVisible();
    expect(scoreboardVisible).toBe(true);

    await page.keyboard.up('Tab');

    // Scoreboard should hide
    await page.waitForTimeout(100);
    const scoreboardHidden = await page.getByTestId('scoreboard').isHidden();
    expect(scoreboardHidden).toBe(true);
  });

  test('should toggle inventory on I', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Press I for inventory
    await page.keyboard.press('KeyI');

    const inventoryVisible = await page.getByTestId('inventory').isVisible();
    expect(inventoryVisible).toBe(true);

    // Press again to close
    await page.keyboard.press('KeyI');

    const inventoryClosed = await page.getByTestId('inventory').isHidden();
    expect(inventoryClosed).toBe(true);
  });
});
```

## Combo Sequences

### Melee Combo Pattern

```typescript
test.describe('Combat Combos', () => {
  test('should execute three-hit light combo', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Execute timed combo sequence
    const comboSequence = [
      { key: 'KeyJ', hold: 100 },
      { key: 'KeyJ', hold: 100 },
      { key: 'KeyJ', hold: 100 },
    ];

    for (const action of comboSequence) {
      await page.keyboard.down(action.key);
      await page.waitForTimeout(action.hold);
      await page.keyboard.up(action.key);
      await page.waitForTimeout(50); // Combo window
    }

    // Verify combo completed
    const comboCount = await page.evaluate(() => (window as any).playerState?.comboCount || 0);

    expect(comboCount).toBe(3);
  });

  test('should execute light-light-heavy finisher', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    // Light, Light, Heavy
    await page.keyboard.down('KeyJ');
    await page.waitForTimeout(100);
    await page.keyboard.up('KeyJ');
    await page.waitForTimeout(50);

    await page.keyboard.down('KeyJ');
    await page.waitForTimeout(100);
    await page.keyboard.up('KeyJ');
    await page.waitForTimeout(50);

    await page.keyboard.down('KeyK');
    await page.waitForTimeout(200);
    await page.keyboard.up('KeyK');

    // Verify finisher executed
    const lastAttack = await page.evaluate(() => (window as any).playerState?.lastAttack || 'none');

    expect(lastAttack).toBe('heavy_finisher');
  });
});
```

### Spell Cast Sequence

```typescript
test.describe('Spell Casting', () => {
  test('should cast spell with modifier key', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialMana = await page.evaluate(() => (window as any).playerState?.mana || 0);

    // Cast spell with Ctrl+Q
    await page.keyboard.down('ControlLeft');
    await page.keyboard.press('KeyQ');
    await page.keyboard.up('ControlLeft');

    const afterMana = await page.evaluate(() => (window as any).playerState?.mana || 0);

    expect(afterMana).toBeLessThan(initialMana);

    // Verify spell was cast
    const spellActive = await page.evaluate(() => (window as any).activeSpell?.type || 'none');

    expect(spellActive).not.toBe('none');
  });
});
```

### Modifier Combinations

```typescript
test.describe('Modifier Combinations', () => {
  test('should sprint jump', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Sprint jump (Shift + Space)
    await page.keyboard.down('ShiftLeft');
    await page.keyboard.press('Space');
    await page.keyboard.up('ShiftLeft');

    await page.waitForTimeout(500);
    const peakY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Sprint jump should go higher/further
    expect(peakY).toBeGreaterThan(initialY);
  });

  test('should crouch jump', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('canvas');

    const initialY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Crouch jump (Ctrl + Space)
    await page.keyboard.down('ControlLeft');
    await page.keyboard.press('Space');
    await page.keyboard.up('ControlLeft');

    await page.waitForTimeout(500);
    const afterY = await page.evaluate(() => (window as any).playerPosition?.y || 0);

    // Crouch jump has different properties
    expect(afterY).toBeGreaterThan(initialY);
  });
});
```

## Complete Gameplay Loop Tests

### Full Character Movement Test

```typescript
test('complete character movement test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas');

  const initialPos = await page.evaluate(
    () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
  );

  // Test all directions
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(500);
  await page.keyboard.up('KeyW');

  await page.keyboard.down('KeyA');
  await page.waitForTimeout(500);
  await page.keyboard.up('KeyA');

  await page.keyboard.down('KeyS');
  await page.waitForTimeout(500);
  await page.keyboard.up('KeyS');

  await page.keyboard.down('KeyD');
  await page.waitForTimeout(500);
  await page.keyboard.up('KeyD');

  // Jump
  await page.keyboard.press('Space');
  await page.waitForTimeout(500);

  const finalPos = await page.evaluate(
    () => (window as any).playerPosition || { x: 0, y: 0, z: 0 }
  );

  // Position should have changed
  expect(finalPos.x).not.toBe(initialPos.x);
  expect(finalPos.y).not.toBe(initialPos.y);
  expect(finalPos.z).not.toBe(initialPos.z);
});
```

### Complete Combat Test

```typescript
test('complete combat test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');

  const initialAmmo = await page.evaluate(() => (window as any).playerState?.ammo || 30);

  // Move into position
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(500);
  await page.keyboard.up('KeyW');

  // Aim
  await page.mouse.move(500, 300);
  await page.waitForTimeout(100);

  // Shoot
  await page.mouse.down({ button: 'left' });
  await page.waitForTimeout(500);
  await page.mouse.up({ button: 'left' });

  const finalAmmo = await page.evaluate(() => (window as any).playerState?.ammo || 30);

  // Ammo should have decreased
  expect(finalAmmo).toBeLessThan(initialAmmo);

  // Check for hit confirmation
  const hits = await page.evaluate(() => (window as any).playerState?.hits || 0);

  expect(hits).toBeGreaterThan(0);
});
```

### Performance During Gameplay

```typescript
test('maintains 60 FPS during gameplay', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.click('canvas');

  // Simulate gameplay actions
  const actions = [
    () => page.keyboard.down('KeyW'),
    () => page.waitForTimeout(200),
    () => page.mouse.move(500, 300),
    () => page.mouse.down({ button: 'left' }),
  ];

  // Collect FPS data
  const fpsData = await page.evaluate(async (actions) => {
    return new Promise((resolve) => {
      const fps = [];
      let lastTime = performance.now();
      let frames = 0;

      function measureFPS() {
        frames++;
        const now = performance.now();
        if (now >= lastTime + 1000) {
          fps.push(frames);
          frames = 0;
          lastTime = now;
          if (fps.length >= 10) {
            resolve(fps);
            return;
          }
        }
        requestAnimationFrame(measureFPS);
      }

      measureFPS();
    });
  }, []);

  // Calculate average FPS
  const avgFPS = fpsData.reduce((a, b) => a + b, 0) / fpsData.length;

  // Should maintain at least 55 FPS
  expect(avgFPS).toBeGreaterThanOrEqual(55);
});
```

## Helper Functions for Tests

### Movement Helper

```typescript
// In tests/helpers/gameplay.ts
export async function moveForward(page: Page, durationMs: number) {
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyW');
}

export async function moveBackward(page: Page, durationMs: number) {
  await page.keyboard.down('KeyS');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyS');
}

export async function strafeLeft(page: Page, durationMs: number) {
  await page.keyboard.down('KeyA');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyA');
}

export async function strafeRight(page: Page, durationMs: number) {
  await page.keyboard.down('KeyD');
  await page.waitForTimeout(durationMs);
  await page.keyboard.up('KeyD');
}

// Usage in tests
test('movement helpers work', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('canvas');

  await moveForward(page, 1000);
  await strafeLeft(page, 500);

  // Verify movement
  const position = await page.evaluate(() => (window as any).playerPosition);
  expect(position.z).toBeLessThan(0);
  expect(position.x).toBeLessThan(0);
});
```

## Testing Checklist

For each gameplay feature:

- [ ] Movement works in all 4 directions (WASD)
- [ ] Diagonal movement works correctly
- [ ] Sprint affects movement speed
- [ ] Jump/Space key triggers correct action
- [ ] Mouse aiming responds correctly
- [ ] Left click performs primary action
- [ ] Right click performs secondary action (if applicable)
- [ ] Interact key (E/F) works with objects
- [ ] Menu keys (Escape, Tab, I, M) open correct UI
- [ ] Combo sequences execute in order
- [ ] No input lag or delayed response
- [ ] Multiple keys can be pressed simultaneously

## Running Gameplay Tests

```bash
# Run all gameplay tests
npm run test:e2e -- tests/e2e/gameplay-suite.spec.ts

# Run specific test
npm run test:e2e -- -g "should move forward"

# Run in headed mode to see gameplay
npm run test:e2e -- --headed

# Run with debug mode
npm run test:e2e -- --debug
```

## Server Management

**⚠️ CRITICAL: Use `shared-lifecycle` skill for server management.**

### Server Detection (Before Gameplay Tests)

**⚠️ IMPORTANT: Playwright's `webServer` config manages servers for E2E tests automatically.**

When running `npm run test:e2e`, Playwright automatically starts:
- `npm run dev` (port 3000) with `reuseExistingServer: !process.env.CI`

**DO NOT manually start servers for E2E tests.**

### Server Check Pattern

```bash
# Check if dev server is running (port 3000)
netstat -an | grep :3000 || lsof -i :3000

# Alternative: Try curl to detect Vite
curl -s http://localhost:3000 | grep -q "vite" && echo "RUNNING" || echo "NOT_RUNNING"
```

### E2E Test Path (Standard Gameplay Validation)

```bash
# Playwright handles server lifecycle via webServer config
npm run test:e2e -- tests/e2e/gameplay-suite.spec.ts

# NO manual server start needed
# NO manual cleanup needed - Playwright handles it
```

### Manual MCP Validation Path (Only when explicitly needed)

```bash
# Only for manual MCP validation (NOT E2E tests)
# Check port 3000 first
if ! netstat -an | grep :3000; then
  # Start server in background
  Bash(command="npm run dev", run_in_background=true)
  # Capture shell_id for cleanup: { shell_id: "abc123" }
fi

# After validation completes:
TaskStop(task_id="abc123")  # MANDATORY cleanup
```

Before running gameplay E2E tests, always check/start the dev server using the patterns from `shared-lifecycle` skill.

**MANDATORY CLEANUP after all tests complete (pass OR fail):**

Use the cleanup patterns from `shared-lifecycle` skill to ensure:

- Dev server is stopped
- Ports are released
- No orphaned processes remain

**See also:** `shared-lifecycle` skill for complete process management patterns.

## References

- **[qa-e2e-test-creation/SKILL.md](../qa-e2e-test-creation/SKILL.md)** - Full E2E test patterns
- [Playwright Keyboard API](https://playwright.dev/docs/api/class-keyboard)
- [Playwright Mouse API](https://playwright.dev/docs/api/class-mouse)
- [tests/pages/game.page.ts](tests/pages/game.page.ts) - Game page object model
