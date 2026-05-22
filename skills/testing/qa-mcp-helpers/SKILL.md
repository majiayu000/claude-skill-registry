---
name: qa-mcp-helpers
description: Shared helper patterns for Playwright MCP validation agents. Reuses Page Object patterns from E2E tests.
category: helper
---

# Playwright MCP Helper Patterns

> "Share code between E2E tests and MCP validation"

This skill provides common patterns for using Playwright MCP tools in validation agents. These patterns align with the Page Object Model used in automated E2E tests.

## Quick Reference

| E2E Test Pattern                      | MCP Equivalent                                                                               |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| `new GamePage(page)`                  | Use same selectors via `page.getByRole()`                                                   |
| `await gamePage.goto()`               | `await page.goto('http://localhost:{detected_port}')` // ALWAYS detect port first            |
| `await expect(element).toBeVisible()` | Check visibility, take screenshot                                                           |

## MANDATORY: Port Detection (BEFORE Navigation)

**⚠️ CRITICAL: Vite dev server may run on different ports (3000, 3001, 5173, etc.)**

**Before using Playwright MCP tools, ALWAYS detect the correct port:**

```bash
# Check which port is serving the Vite app
netstat -an | grep LISTEN | grep -E ":(3000|3001|5173|8080)"

# Alternative: Try curl to detect
curl -s http://localhost:3000 | grep -q "vite" && echo "PORT=3000" || \
curl -s http://localhost:3001 | grep -q "vite" && echo "PORT=3001" || \
curl -s http://localhost:5173 | grep -q "vite" && echo "PORT=5173"
```

**Store detected port in variable for subsequent MCP calls:**

```typescript
// After detecting port, use it in navigation
const detectedPort = 3001; // From bash detection above
await page.goto(`http://localhost:${detectedPort}`);
```

## Multi-Agent Playwright MCP Considerations

**⚠️ IMPORTANT: Standard Playwright MCP does NOT support parallel execution**

When multiple agents (Developer, QA, Tech Artist) may use Playwright MCP simultaneously:

1. **Issue:** Standard `@playwright/mcp` shares a single browser instance - agents interfere with each other
2. **Solution:** Use `playwright-parallel-mcp` for isolated browser sessions per agent

**To enable parallel Playwright instances, update MCP settings:**

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["playwright-parallel-mcp"],
      "env": {
        "MAX_SESSIONS": "5"
      }
    }
  }
}
```

**Usage with sessions:**
```javascript
// Create isolated session for this agent
[create_session] -> sessionId: "qa-session-{timestamp}"

// Use session ID in all subsequent calls
[navigate sessionId="qa-session-{timestamp}" url="http://localhost:3001"]
```

**Reference:** [playwright-parallel-mcp on LobeHub](https://lobehub.com/mcp/sumyapp-playwright-parallel-mcp)

## Common MCP Patterns

### Navigation

```typescript
// 1. FIRST: Detect port (see above)
const detectedPort = 3001; // From bash detection

// 2. Navigate to the application
await page.goto(`http://localhost:${detectedPort}`);

// 3. Wait for page to fully load
await page.waitForLoadState('networkidle');

// 4. Wait for canvas to be ready
await page.waitForSelector('canvas');
```

### Console Monitoring

```typescript
// Track console errors during validation
const errors: string[] = [];
const warnings: string[] = [];

page.on('console', (msg) => {
  if (msg.type() === 'error') {
    errors.push(msg.text());
  }
  if (msg.type() === 'warning') {
    warnings.push(msg.text());
  }
});

// After performing actions:
// Filter out known headless WebGL errors (expected, not application bugs)
const filteredErrors = errors.filter((error) => {
  const webglHeadlessPatterns = [
    /WebGL2RenderingContext/i,
    /Error creating WebGL context/i,
    /WebGL context could not be created/i,
    /Failed to create WebGL2RenderingContext/i,
    /WEBGL_debug_renderer_info/i,
    /ANGLE flag/i,
    /swiftshader/i,
  ];
  return !webglHeadlessPatterns.some((p) => p.test(error));
});

// Check that no actual application errors occurred
if (filteredErrors.length > 0) {
  console.error('Application errors found:', filteredErrors);
}
```

## WebGL / Three.js MCP Patterns

**⚠️ CRITICAL:** Three.js applications require specific patterns for MCP validation.

### Scene Readiness Detection

```typescript
// Wait for Three.js scene to be ready using data attribute
await page.waitForSelector('canvas[data-ready="1"]', { timeout: 15000 });

// Alternative: Wait for canvas and additional delay
await page.waitForSelector('canvas');
await page.waitForTimeout(2000); // Allow Three.js initialization
```

### WebGL Context Verification

```typescript
// Verify WebGL is working before proceeding
const webglStatus = await page.evaluate(() => {
  const canvas = document.querySelector('canvas');
  if (!canvas) return { exists: false, hasContext: false };

  const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
  if (!gl) return { exists: true, hasContext: false };

  return {
    exists: true,
    hasContext: true,
    version: gl.getParameter(gl.VERSION),
  };
});

if (!webglStatus.hasContext) {
  throw new Error('WebGL context not available - cannot validate 3D scene');
}
```

### Canvas Element Screenshot

```typescript
// For WebGL scenes, screenshot only the canvas element
const canvas = await page.locator('canvas').boundingBox();

if (canvas) {
  await page.screenshot({
    path: '.claude/session/qa-validation/canvas-render.png',
    clip: {
      x: canvas.x,
      y: canvas.y,
      width: canvas.width,
      height: canvas.height,
    },
  });
}
```

### Shader Error Detection

```typescript
// Track shader compilation errors separately
const shaderErrors: string[] = [];

page.on('console', (msg) => {
  const text = msg.text();
  const shaderErrorPatterns = [
    /THREE\.WebGLProgram/i,
    /shader error/i,
    /program info log/i,
    /WEBGL_WARNING/i,  // But NOT WEBGL_debug_renderer_info
  ];

  if (shaderErrorPatterns.some((p) => p.test(text))) {
    shaderErrors.push(text);
  }
});

if (shaderErrors.length > 0) {
  throw new Error(`Shader compilation errors: ${shaderErrors.join(', ')}`);
}
```

### Screenshot Evidence

```typescript
// Capture screenshot for validation evidence
await page.screenshot({
  path: '.claude/session/qa-validation/screenshot.png',
  fullPage: true,
});
```

### Using Page Object Selectors

When the E2E test uses specific selectors, use the same approach in MCP validation:

```typescript
// Character Selection Screen
// E2E test: page.locator('#characterName')
// MCP: page.locator('#characterName')

// Select Character Button
// E2E test: page.locator('button:has-text("Select Character")')
// MCP: page.locator('button:has-text("Select Character")')

// Lobby State
// E2E test: page.getByText('LOBBY')
// MCP: page.getByText('LOBBY')

// Connection State
// E2E test: page.getByText('Connected')
// MCP: page.getByText('Connected')
```

## Game-Specific Patterns

### Character Selection Flow

```typescript
// Navigate to game (detectedPort from port detection step above)
await page.goto(`http://localhost:${detectedPort}`);
await page.waitForLoadState('networkidle');

// Check if at Character Selection screen
const atCharacterSelection = await page.evaluate(() => {
  const bodyText = document.body.textContent || '';
  return bodyText.includes('Choose Your Character') || bodyText.includes('Character Selection');
});

if (atCharacterSelection) {
  // Enter character name
  await page.fill('#characterName', 'TestPlayer');

  // Wait for state update
  await page.waitForTimeout(500);

  // Click Select Character button
  const selectButton = page.locator('button:has-text("Select Character")').first();
  await selectButton.click();

  // Wait for Lobby screen
  await page.waitForFunction(
    () => {
      const bodyText = document.body.textContent || '';
      return bodyText.includes('LOBBY') || bodyText.includes('Connecting to server');
    },
    { timeout: 10000 }
  );
}
```

### Connection Verification

```typescript
// Wait for server connection
await page.waitForFunction(
  () => {
    const bodyText = document.body.textContent || '';
    // Must show "Connected" but not "Connecting to server"
    return bodyText.includes('Connected') && !bodyText.includes('Connecting to server');
  },
  { timeout: 25000 }
);

// Verify connection state
const isConnected = await page.evaluate(() => {
  const bodyText = document.body.textContent || '';
  return (
    bodyText.includes('Connected') &&
    bodyText.includes('Players in Lobby') &&
    !bodyText.includes('Connecting to server')
  );
});
```

## Input Testing Patterns

### Keyboard Input (Movement)

```typescript
// Continuous movement for gameplay testing
await page.keyboard.down('KeyW');
await page.waitForTimeout(1000); // Move for 1 second
await page.keyboard.up('KeyW');

// Individual key presses
await page.keyboard.press('KeyA');
await page.waitForTimeout(500);
```

### Mouse Input (Pointer Lock)

```typescript
// Click to activate pointer lock
await page.mouse.click(400, 300);
await page.waitForTimeout(500);

// Simulate mouse movement (movementX/Y only work when locked)
await page.mouse.move(100, 100);
await page.mouse.move(200, 150); // movementX: 100, movementY: 50

// Mouse click (shoot action)
await page.mouse.down();
await page.waitForTimeout(200);
await page.mouse.up();
```

### Escape Key (Pause/Unlock)

```typescript
// Press ESC to unlock pointer and show PAUSED
await page.keyboard.press('Escape');

// Verify pointer is unlocked
const isLocked = await page.evaluate(() => {
  return document.pointerLockElement === document.body;
});
expect(isLocked).toBe(false);
```

## Selector Best Practices

When writing MCP validation scripts, follow these selector priorities:

### Priority Order

1. **Role-based selectors** (Preferred - accessible)

   ```typescript
   page.getByRole('button', { name: 'Submit' });
   page.getByRole('textbox', { name: 'Username' });
   ```

2. **Label-based selectors** (Good - accessible)

   ```typescript
   page.getByLabel('Character Name');
   page.getByLabel('Email address');
   ```

3. **Test ID selectors** (When no accessible name)

   ```typescript
   page.getByTestId('submit-button');
   page.getByTestId('character-name-input');
   ```

4. **Text content** (For existing patterns)

   ```typescript
   page.getByText('LOBBY');
   page.locator('button:has-text("Select Character")');
   ```

5. **ID selectors** (For legacy/existing code)
   ```typescript
   page.locator('#characterName');
   ```

### Avoid

❌ **Brittle CSS selectors:**

```typescript
// Bad - breaks with CSS changes
page.locator('.btn-primary:first-child');
page.locator('div.container > div:nth-child(2)');

// Bad - fragile to DOM structure changes
page.locator('body > div > div > button');
```

## Anti-Patterns

### Don't Use Hard-coded Waits

```typescript
// Bad - arbitrary delay
await page.waitForTimeout(5000);

// Good - wait for specific condition
await page.waitForSelector('canvas');
await page.waitForFunction(() => {
  return document.body.textContent?.includes('Connected');
});
```

### Don't Skip Error Checking

```typescript
// Always check for console errors
const errors: string[] = [];
page.on('console', (msg) => {
  if (msg.type() === 'error') errors.push(msg.text());
});

// After validation, verify no errors
if (errors.length > 0) {
  console.error('Console errors found:', errors);
}
```

## Alignment with E2E Tests

MCP validation agents should:

1. **Use same selectors** as defined in `tests/pages/*.page.ts`
2. **Focus on NEW features** - don't duplicate regression tests
3. **Use Vision MCP** for visual validation when appropriate
4. **Take screenshots** as evidence for validation reports

### Example Alignment

```typescript
// E2E test (tests/pages/game.page.ts):
export class GamePage {
  readonly characterNameInput: Locator;
  constructor(page: Page) {
    this.characterNameInput = page.locator('#characterName');
  }
}

// MCP validation uses same selector:
await page.fill('#characterName', 'TestPlayer');
```

## Page Object Model Reference

**E2E tests and MCP agents share Page Objects from `tests/pages/`:**

| File                                                               | Purpose                                     |
| ------------------------------------------------------------------ | ------------------------------------------- |
| [tests/pages/base.page.ts](tests/pages/base.page.ts)               | Base page class (goto, console, screenshot) |
| [tests/pages/game.page.ts](tests/pages/game.page.ts)               | Character selection, lobby, connection      |
| [tests/pages/multiplayer.page.ts](tests/pages/multiplayer.page.ts) | Multi-client setup, connect, cleanup        |

**Selector priority:**

1. Role-based: `page.getByRole('button', { name: 'Submit' })`
2. Label-based: `page.getByLabel('Character Name')`
3. Test ID: `page.getByTestId('submit-button')`
4. Text content: `page.getByText('LOBBY')`
5. ID selector: `page.locator('#characterName')`

**Avoid:** Brittle CSS selectors like `.btn-primary:first-child`

---

## References

- [tests/pages/base.page.ts](tests/pages/base.page.ts) - Base page class
- [tests/pages/game.page.ts](tests/pages/game.page.ts) - Game-specific interactions
- [tests/pages/multiplayer.page.ts](tests/pages/multiplayer.page.ts) - Multiplayer test helpers
- [tests/e2e/multiplayer-suite.spec.ts](tests/e2e/multiplayer-suite.spec.ts) - Example E2E tests
- [.claude/skills/qa-browser-testing/SKILL.md](.claude/skills/qa-browser-testing/SKILL.md) - Browser testing skill
