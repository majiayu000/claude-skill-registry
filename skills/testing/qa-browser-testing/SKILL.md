---
name: qa-browser-testing
description: E2E test creation and execution for QA. Validates implementations using Playwright API tests that become persistent artifacts for regression.
category: validation
---

# Browser Testing for QA

> "Validate implementations with E2E tests that become regression tests for the project."

## Three.js / WebGL Testing Best Practices (2025-2026)

**CRITICAL**: Testing Three.js applications requires specific configuration for WebGL context support.

### Playwright Configuration Requirements

The `playwright.config.ts` **MUST** include these GPU acceleration flags for headless WebGL support:

```typescript
// playwright.config.ts - Required for Three.js testing
projects: [
  {
    name: 'chromium-webgl',
    use: {
      ...devices['Desktop Chrome'],
      channel: 'chrome',
      launchOptions: {
        args: [
          '--use-gl=desktop',        // Desktop OpenGL (Windows/macOS/Linux)
          '--enable-webgl',
          '--enable-webgl2',
          '--ignore-gpu-blocklist',
          '--enable-gpu-rasterization',
          '--enable-zero-copy',
          '--disable-gpu-vsync',
        ],
      },
    },
  },
]
```

### Headless vs Headed Mode for WebGL

| Browser   | Headless WebGL | Solution |
|-----------|----------------|----------|
| Chromium  | Yes (with flags) | Use `--use-gl=desktop` flags |
| Chrome     | Yes (with flags) | Best WebGL support |
| Firefox   | **No** | Set `headless: false` or use Xvfb in CI |
| WebKit    | **No** | Set `headless: false` |

**Firefox Testing Pattern** (requires headed mode):
```bash
# Local development - use headed mode
npm run test:e2e -- --project=firefox-webgl

# CI environment - use Xvfb for virtual display
xvfb-run --auto-servernum npx playwright test --project=firefox-webgl
```

### WebGL Console Error Filtering

**Headless browsers may produce expected WebGL warnings**. Always filter these out:

```typescript
// Filter out known headless WebGL errors
const filteredErrors = errors.filter(
  (error) =>
    !error.includes('WebGL2RenderingContext') &&
    !error.includes('Error creating WebGL context') &&
    !error.includes('WebGL context could not be created') &&
    !error.includes('WEBGL_debug_renderer_info')
);
```

### Scene Readiness Pattern

**Always wait for scene initialization** using a data attribute:

```typescript
// In your app code (Scene.tsx or main component)
useEffect(() => {
  // Mark scene as ready when Three.js has initialized
  const canvas = canvasRef.current;
  if (canvas) {
    canvas.dataset.ready = '1';
  }
}, []);

// In your test
await page.locator('canvas[data-ready="1"]').waitFor({ timeout: 15000 });
```

### GPU Acceleration Verification Test

Include this test to verify GPU acceleration is working:

```typescript
test('GPU hardware acceleration is enabled', async ({ page }) => {
  // This test verifies WebGL context is properly initialized
  await page.goto('/');

  const canvas = await page.locator('canvas').first();
  await expect(canvas).toBeVisible();

  const webglInfo = await page.evaluate(() => {
    const canvas = document.querySelector('canvas');
    if (!canvas) return { hasContext: false };

    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!gl) return { hasContext: false };

    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');

    return {
      hasContext: true,
      version: gl.getParameter(gl.VERSION),
      vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'unknown',
      renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'unknown',
    };
  });

  expect(webglInfo.hasContext).toBe(true);
  console.log('WebGL Info:', webglInfo);
});
```

### Canvas-Only Screenshots

For visual regression of WebGL scenes, screenshot only the canvas:

```typescript
test('canvas visual regression', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('canvas[data-ready="1"]');

  const canvas = page.locator('canvas');

  // Screenshot just the canvas element
  await expect(canvas).toHaveScreenshot('canvas-render.png', {
    animations: 'allow',
    // Anti-aliasing tolerance is set in playwright.config.ts
    // threshold: 0.2, maxDiffPixelRatio: 0.02
  });
});
```

---

## When to Use This Skill

Use for **every validation** after automated checks pass:

- Validating Developer implementation
- Verifying Tech Artist visual assets
- Testing gameplay mechanics
- Checking UI components
- Before marking PRD items as passed

## Quick Start

```bash
# 1. MANDATORY: Detect dev server port (Vite may use 3000, 3001, 5173, etc.)
netstat -an | grep LISTEN | grep -E ":(3000|3001|5173|8080)"
# OR try: curl -s http://localhost:3000 | grep -q "vite" && echo "3000" || curl -s http://localhost:3001 | grep -q "vite" && echo "3001"

# 2. Check if E2E test exists for the feature
ls tests/e2e/{feature}-suite.spec.ts

# 3. If missing, create using qa-e2e-test-creation patterns
# Use Skill("qa-e2e-test-creation")

# 4. Run E2E tests to validate implementation
npm run test:e2e

# 5. Review test output for acceptance criteria verification
```

## MANDATORY: Port Detection

**⚠️ CRITICAL: Vite dev server may run on different ports (3000, 3001, 5173, etc.)**

**Before ANY browser interaction, ALWAYS detect the correct port:**

```bash
# Method 1: Check listening ports
netstat -an | grep LISTEN | grep -E ":(3000|3001|5173|8080)"

# Method 2: Try curl to detect Vite
curl -s http://localhost:3000 | grep -q "vite" && echo "PORT=3000" || \
curl -s http://localhost:3001 | grep -q "vite" && echo "PORT=3001" || \
curl -s http://localhost:5173 | grep -q "vite" && echo "PORT=5173"

# Method 3: Check Vite output when running `npm run dev`
# Look for "Local: http://localhost:XXXX" in the output
```

**E2E tests automatically detect the port from `playwright.config.ts`.**
**Manual MCP validation requires you to use the detected port.**

## Multi-Agent Playwright Considerations

**⚠️ IMPORTANT: When multiple agents use Playwright MCP simultaneously**

Standard `@playwright/mcp` shares a single browser instance. For parallel agent execution:

1. **Use `playwright-parallel-mcp`** - Isolated browser sessions per agent
2. **Configuration in MCP settings:**
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["playwright-parallel-mcp"],
         "env": { "MAX_SESSIONS": "5" }
       }
     }
   }
   ```
3. **Usage:** Create session per agent, use sessionId in all calls

**Reference:** See `qa-mcp-helpers` skill for full details on parallel Playwright setup.

## Core Principle: Run Tests, Don't Use MCP

**❌ OLD APPROACH (Do NOT do this):**

```typescript
// Interactive MCP validation - NO!
mcp__playwright__browser_navigate('http://localhost:3000');
mcp__playwright__browser_take_screenshot({ filename: 'validation.png' });
```

**✅ NEW APPROACH (Do this):**

```typescript
// Write or run E2E test - YES!
npm run test:e2e -- tests/e2e/{feature}-suite.spec.ts
```

## Validation Workflow

### Level 0: Test Coverage Check (BEFORE Validation)

**⚠️ CRITICAL: Ensure tests exist before validation**

1. **Check if E2E test exists** for the validated feature:

   ```bash
   # Look for test file
   ls tests/e2e/{feature}-suite.spec.ts

   # Or search for task/feature in tests
   grep -r "taskId" tests/e2e/
   ```

2. **If test is missing:**
   - Load `qa-e2e-test-creation` skill
   - Create test covering acceptance criteria
   - Verify test runs successfully

### Level 1: Run E2E Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run specific test file
npm run test:e2e -- tests/e2e/{feature}-suite.spec.ts

# Run specific test by name
npm run test:e2e -- -g "test-name"

# Run in headed mode (see browser)
npm run test:e2e -- --headed

# Run with debug mode
npm run test:e2e -- --debug
```

### Level 2: Verify Acceptance Criteria

For each acceptance criterion in `current-task-qa.json` (acceptanceCriteria array):

```markdown
## Acceptance Criteria Verification

### Criterion 1: "Feature does X"

- **Test**: `npm run test:e2e -- -g "feature does X"`
- **Result**: ✅ PASS / ❌ FAIL
- **Evidence**: Test output shows expected behavior
```

### Level 3: Report Results

**If ALL tests pass:**

```json
{
  "id": "{taskId}",
  "passes": true,
  "status": "passed",
  "validatedAt": "{ISO_TIMESTAMP}",
  "testResults": {
    "e2eTests": "passed",
    "testFile": "tests/e2e/{feature}-suite.spec.ts"
  }
}
```

**If ANY test fails:**

```json
{
  "id": "{taskId}",
  "status": "needs_fixes",
  "bugNotes": "Test failure details...",
  "retryCount": 1,
  "testResults": {
    "e2eTests": "failed",
    "failureReason": "Test output excerpt"
  }
}
```

## Test Categories

| Category        | What to Check              | Test Pattern              |
| --------------- | -------------------------- | ------------------------- |
| **Load**        | Page loads, canvas renders | `test('page loads', ...)` |
| **Console**     | No errors or warnings      | Console listener test     |
| **Functional**  | Features work as specified | Acceptance criteria tests |
| **Visual**      | UI appears correctly       | Screenshot comparison     |
| **Performance** | 60 FPS, no stuttering      | FPS monitoring test       |
| **Input**       | Controls respond correctly | WASD/mouse tests          |

## Creating Tests for Missing Coverage

When Developer/Tech Artist didn't create tests:

```typescript
// tests/e2e/{feature}-suite.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Feature Name - {taskId}', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should meet acceptance criterion 1', async ({ page }) => {
    // Test implementation
  });

  test('should meet acceptance criterion 2', async ({ page }) => {
    // Test implementation
  });
});
```

**Then verify:**

```bash
npm run test:e2e -- tests/e2e/{feature}-suite.spec.ts
```

## Common Test Patterns for Validation

### Basic Load Test

```typescript
test('page loads correctly', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Wait for canvas
  const canvas = page.locator('canvas');
  await expect(canvas).toBeVisible();

  // Check for console errors
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(msg.text());
  });

  await page.waitForTimeout(5000); // Wait for initial load
  expect(errors).toHaveLength(0);
});
```

### Input Testing

```typescript
test('keyboard controls work', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Focus canvas
  await page.click('canvas');

  // Press WASD keys
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'test-results/after-w.png' });
  await page.keyboard.up('KeyW');
});
```

### Visual Comparison

```typescript
test('visual appearance matches', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');
  await page.waitForTimeout(2000); // Wait for scene to stabilize

  // Compare with baseline
  await expect(page).toHaveScreenshot('baseline.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

### Pointer Lock Testing (FPS/TPS)

```typescript
test('pointer lock activates on game start', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForSelector('canvas');

  // Wait for auto-lock timeout (typically 100ms)
  await page.waitForTimeout(200);

  // Check if pointer lock is active
  const isLocked = await page.evaluate(() => {
    return document.pointerLockElement === document.body;
  });

  expect(isLocked).toBe(true);
});
```

### Performance Metrics

```typescript
test('performance is acceptable', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Get performance metrics
  const metrics = await page.evaluate(() => {
    const entries = performance.getEntriesByType('navigation');
    const nav = entries[0] as PerformanceNavigationTiming;
    return {
      loadTime: nav.loadEventEnd - nav.startTime,
      domContentLoaded: nav.domContentLoadedEventEnd - nav.startTime,
    };
  });

  expect(metrics.loadTime).toBeLessThan(3000);
  expect(metrics.domContentLoaded).toBeLessThan(2000);
});
```

## Console Error Monitoring

Every validation should include console error checking **with WebGL-specific filtering**:

```typescript
test.describe('Console Error Check', () => {
  test('should have no application console errors', async ({ page }) => {
    const errors: string[] = [];
    const warnings: string[] = [];

    page.on('console', (msg) => {
      if (msg.type() === 'error') errors.push(msg.text());
      if (msg.type() === 'warning') warnings.push(msg.text());
    });

    await page.goto('http://localhost:3000');
    await page.waitForSelector('canvas[data-ready="1"]');
    await page.waitForTimeout(3000);

    // Filter out known headless WebGL/browser errors that are not app bugs
    const filteredErrors = errors.filter((error) => {
      // WebGL context errors in headless mode (expected, not app bugs)
      const webglContextPatterns = [
        /WebGL2RenderingContext/i,
        /Error creating WebGL context/i,
        /WebGL context could not be created/i,
        /Failed to create WebGL2RenderingContext/i,
        /WEBGL_debug_renderer_info/i,
      ];

      // ANGLE/GPU driver warnings (platform-specific, not app bugs)
      const gpuDriverPatterns = [
        /ANGLE flag/,
        /GPU process/,
        /swiftshader/i,
      ];

      // Filter if matches any known non-bug pattern
      return !webglContextPatterns.some((p) => p.test(error)) &&
             !gpuDriverPatterns.some((p) => p.test(error));
    });

    // Report actual application errors
    expect(filteredErrors).toHaveLength(0);

    // Log warnings for review (non-failing)
    if (warnings.length > 0) {
      console.warn('Console warnings found:', warnings);
    }
  });
});
```

### WebGL Error Filter Patterns

| Pattern | Type | Action |
|---------|------|--------|
| `WebGL2RenderingContext` | Headless limitation | Filter out |
| `Error creating WebGL context` | Headless limitation | Filter out |
| `Failed to create WebGL2RenderingContext` | Headless limitation | Filter out |
| `WEBGL_debug_renderer_info` | Extension not available | Filter out |
| `ANGLE flag` | GPU driver info | Filter out |
| `swiftshader` | Software renderer | Filter out |
| `THREE.WebGLProgram` | **Shader compilation** | **FAIL - This is a bug** |
| `shader error` | **Shader compilation** | **FAIL - This is a bug** |
| `program info log` | **Shader compilation** | **FAIL - This is a bug** |

### Load State Decision Tree

**CRITICAL: Choose correct load state to avoid flaky timeouts**

Based on retrospective findings (bugfix-e2e-001, 2026-01-26), `domcontentloaded` is more reliable than `networkidle` for most E2E tests.

```
                    What does your test need?
                            |
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   HTML/DOM only?    All resources?     No network activity?
        │                   │                   │
        ▼                   ▼                   ▼
   domcontentloaded        load          networkidle (rare)
        │                   │
        │             Use when:         Use when:
        │             - Images           - SPA with
        │             - Styles           background
   Use when:             - Scripts          polling
   - Page structure       - Fonts
   - Element visibility   - Media
   - Fast test execution
```

**Default Choice**: `domcontentloaded`

**Why `domcontentloaded` is preferred:**

- Fires when HTML is parsed and DOM is ready
- Much faster than waiting for all network requests
- Sufficient for most UI interactions (after waiting for specific elements)
- `networkidle` can timeout on pages with continuous background activity

**When to use `load`:**

- Testing image loading
- Need fonts fully applied
- Media elements (video/audio)
- Critical styles depend on external resources

**When to use `networkidle`:**

- SPA with continuous background polling
- Analytics/tracking scripts running
- WebSocket connections active
- Rare - only when explicitly justified

**Learned from bugfix-e2e-001 (2026-01-26):**

- Changed `waitForLoadState('networkidle')` to `waitForLoadState('domcontentloaded')`
- 23/23 accessibility tests now passing (was timing out before)
- Tests complete within 60 seconds (was timing out)

### Load State Usage Examples

```typescript
// Default: domcontentloaded (fastest, most reliable)
await page.goto('http://localhost:3000');
await page.waitForLoadState('domcontentloaded');

// For element-specific waits (even better than load state)
await page.waitForSelector('canvas', { state: 'attached' });

// Only use load when you need all resources
await page.waitForLoadState('load'); // For images, fonts, styles

// Rarely use networkidle (only for background activity)
await page.waitForLoadState('networkidle'); // Last resort
```

### E2E Server Lifecycle Management

**CRITICAL: Multiplayer E2E tests require explicit port cleanup**

Based on retrospective findings (bugfix-e2e-002, 2026-01-26), Colyseus server tests need proper lifecycle management to avoid EADDRINUSE errors.

```typescript
// tests/e2e/multiplayer-suite.spec.ts
import { test, expect } from '@playwright/test';

let serverProcess: ReturnType<typeof spawn> | null = null;
const TEST_PORT = 2577; // Different from default 2567

test.beforeAll(async () => {
  // Start server for E2E tests
  serverProcess = spawn('npm', ['run', 'server'], {
    env: { ...process.env, PORT: String(TEST_PORT) },
    stdio: 'pipe',
  });

  // Wait for server to be ready
  await waitForServerReady(TEST_PORT);
});

test.afterAll(async () => {
  // EXPLICIT cleanup required
  if (serverProcess) {
    serverProcess.kill('SIGTERM');
    serverProcess = null;

    // Additional: verify port is released
    await waitForPortRelease(TEST_PORT);
  }
});
```

**Port Management Checklist:**

- [ ] Use unique port for E2E tests (different from development)
- [ ] Set port via environment variable
- [ ] Explicitly kill server process in afterAll
- [ ] Verify port is released before next test
- [ ] Handle cleanup even if test fails (try/finally)

**Learned from bugfix-e2e-002 (2026-01-26):**

- Fixed EADDRINUSE errors with proper port cleanup
- 65/65 E2E tests passing (100% success rate)
- Server availability detection added

### Shader-Specific Error Detection

**CRITICAL for Shader/TSL Tasks**: Add pattern matching for shader errors:

```typescript
test.describe('Shader Error Detection', () => {
  test('should have no shader compilation errors', async ({ page }) => {
    const shaderErrors: string[] = [];

    page.on('console', (msg) => {
      const text = msg.text();

      // Three.js shader error patterns
      const shaderErrorPatterns = [
        /THREE\.WebGLProgram/i,
        /shader error/i,
        /program info log/i,
        /WEBGL_WARNING/i,
        // TSL-specific patterns
        /Cannot read properties.*undefined.*replace/i,
        /VaryingProperty/i,
        /NodeBuilder/i,
        /assign.*null/i,
      ];

      if (shaderErrorPatterns.some((pattern) => pattern.test(text))) {
        shaderErrors.push(text);
      }
    });

    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');

    // Trigger shader-heavy interactions
    await page.mouse.click(400, 300);
    await page.waitForTimeout(2000);

    expect(shaderErrors).toHaveLength(0);
  });
});
```

### Color Mode / Shader Task Validation Pattern

For P1-005 (Color Blind Modes) and similar shader tasks:

```typescript
test.describe('Shader Task Validation Checklist', () => {
  test('should validate all color modes without errors', async ({ page }) => {
    const allErrors: string[] = [];

    page.on('console', (msg) => {
      if (msg.type() === 'error') allErrors.push(msg.text());
    });

    const colorModes = ['default', 'protanopia', 'deuteranopia', 'tritanopia', 'high_contrast'];

    for (const mode of colorModes) {
      // Set mode via localStorage or UI
      await page.evaluate((m) => {
        localStorage.setItem(
          'project-chroma-accessibility',
          JSON.stringify({
            hasCompletedFirstLaunch: true,
            colorMode: m,
          })
        );
      }, mode);
      await page.reload();
      await page.waitForTimeout(1000);
    }

    // Verify no shader errors across all modes
    const shaderErrors = allErrors.filter((e) => /shader|THREE|TSL|WebGL/i.test(e));
    expect(shaderErrors).toHaveLength(0);
  });
});
```

## Runtime Error Detection

### Problem: Pre-existing Runtime Errors Block Validation

Runtime TypeErrors like "Cannot read properties of undefined" can exist in the codebase before a task starts, blocking browser validation for unrelated features. QA needs to detect and report these blockers early.

### Runtime Error Monitoring Pattern

```typescript
// tests/e2e/runtime-error-check.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Runtime Error Detection', () => {
  test('should have no runtime TypeErrors', async ({ page }) => {
    const runtimeErrors: Array<{
      message: string;
      stack?: string;
      timestamp: number;
    }> = [];

    // Capture all unhandled errors
    page.on('pageerror', (error) => {
      runtimeErrors.push({
        message: error.message,
        stack: error.stack,
        timestamp: Date.now(),
      });
    });

    // Also capture console errors
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        runtimeErrors.push({
          message: msg.text(),
          timestamp: Date.now(),
        });
      }
    });

    await page.goto('http://localhost:3000');
    await page.waitForSelector('canvas');
    await page.waitForTimeout(5000); // Wait for initial load

    // Check for specific runtime error patterns
    const blockingErrors = runtimeErrors.filter((error) => {
      const blockingPatterns = [
        /Cannot read properties.*undefined/,
        /Cannot read.*property.*undefined/,
        /undefined is not.*object/,
        /null is not.*object/,
        /is not a function/,
        /Unexpected token/,
      ];
      return blockingPatterns.some((pattern) => pattern.test(error.message));
    });

    if (blockingErrors.length > 0) {
      console.error('BLOCKING RUNTIME ERRORS FOUND:', blockingErrors);
      throw new Error(
        `Found ${blockingErrors.length} blocking runtime error(s):\n` +
          blockingErrors.map((e) => `  - ${e.message}`).join('\n') +
          `\n\nThese errors must be fixed before validation can proceed.`
      );
    }

    // Also check for any runtime errors (not just blocking)
    if (runtimeErrors.length > 0) {
      console.warn('Non-blocking runtime errors:', runtimeErrors);
    }
  });

  test('should report all runtime errors for debugging', async ({ page }) => {
    const allErrors: string[] = [];

    page.on('pageerror', (error) => {
      allErrors.push(`[${error.name}] ${error.message}`);
    });

    await page.goto('http://localhost:3000');
    await page.waitForSelector('canvas');
    await page.waitForTimeout(3000);

    if (allErrors.length > 0) {
      // Log all errors for debugging, even if non-blocking
      console.log('All Runtime Errors:', allErrors);
    }
  });
});
```

### Error Blocking Decision Tree

```
                    Runtime Error Found?
                            |
            ┌───────────────┴───────────────┐
            │                               │
      Error in CHANGED files?         Error in UNCHANGED files?
            │                               │
            ▼                               ▼
       RETURN to Developer          CREATE BLOCKER TASK
       (Task's code has bug)        (Pre-existing issue)
```

### Runtime Error Report Format

When blocking runtime errors are found:

```json
{
  "status": "blocked",
  "blocker": "Pre-existing runtime TypeError",
  "errors": [
    {
      "message": "Cannot read properties of undefined (reading 'position')",
      "location": "src/components/game/player/index.ts:42",
      "isNew": false,
      "relatedToTask": false
    }
  ],
  "action": "Create separate bugfix task for pre-existing error",
  "recommendation": "Developer should fix pre-existing error before validating new features"
}
```

### Pre-Existing Error Detection

```typescript
// Check if error exists before task changes
test.beforeEach(async ({ page }) => {
  // Record baseline errors before any task interactions
  const baselineErrors: string[] = [];

  page.on('pageerror', (error) => {
    baselineErrors.push(error.message);
  });

  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);

  // Store baseline for comparison
  (page as any).__baselineErrors = baselineErrors;
});
```

### Validation Blocking Rules

| Error Type                   | Is Blocking? | Action                |
| ---------------------------- | ------------ | --------------------- |
| TypeError in changed files   | YES          | Return to Developer   |
| TypeError in unchanged files | YES          | Create blocker task   |
| ReferenceError               | YES          | Return to Developer   |
| Console warnings             | NO           | Note in report        |
| Asset load errors (404)      | MAYBE        | Check if task-related |

**Learned from bugfix-tps-001 retrospective (2026-01-25)**:

- "Cannot read properties of undefined" runtime error blocked browser validation for feat-tps-005
- Pre-existing errors need separate bugfix tasks, not to block current task indefinitely
- QA must distinguish between task-caused errors and pre-existing issues

## Page Object Model Usage

For complex validations, use Page Objects from `tests/pages/`:

```typescript
import { test, expect } from '@playwright/test';
import { GamePage } from '@/pages/game.page';
import { MultiplayerPage } from '@/pages/multiplayer.page';

test('complete gameplay loop', async ({ page }) => {
  const gamePage = new GamePage(page);

  await gamePage.goto();
  await gamePage.selectCharacter('TestPlayer');
  await gamePage.waitForLobby();

  expect(await gamePage.isConnected()).toBe(true);
});

test('multiplayer state sync', async ({ browser }) => {
  const multiplayerPage = new MultiplayerPage(page);
  const players = await multiplayerPage.setupMultiPlayerTest(browser, 2);

  try {
    await multiplayerPage.connectPlayersToGame(players);
    expect(await multiplayerPage.verifyAllConnected(players)).toBe(true);
  } finally {
    await multiplayerPage.cleanupPlayers(players);
  }
});
```

## Cross-Browser Testing for WebGL

| Browser         | Headless WebGL | GPU Acceleration | Priority | Notes |
| --------------- | -------------- | ----------------- | -------- | ------ |
| Chrome          | Yes (with flags) | Yes (with flags) | **Primary** | Best WebGL support |
| Chromium        | Yes (with flags) | Yes (with flags) | **Primary** | CI/CD standard |
| Firefox         | **No** | Yes (headed only) | Optional | Use `headless: false` or Xvfb |
| WebKit/Safari   | **No** | Yes (headed only) | If iOS target | Use `headless: false` |
| Edge            | Yes (with flags) | Yes (with flags) | Optional | Uses Chromium |

### Running Tests by Browser

```bash
# Chrome/Chromium (primary - works in headless)
npm run test:e2e -- --project=chromium-webgl

# Firefox (requires headed mode or Xvfb)
npm run test:e2e -- --project=firefox-webgl --headed

# Firefox with Xvfb (CI/CD)
xvfb-run --auto-servernum npm run test:e2e -- --project=firefox-webgl

# All browsers
npm run test:e2e
```

### Firefox WebGL Testing Setup

**Firefox doesn't support WebGL in headless mode.** Configure project in `playwright.config.ts`:

```typescript
{
  name: 'firefox-webgl',
  use: {
    ...devices['Desktop Firefox'],
    headless: false,  // Required for WebGL support
  },
}
```

**For CI/CD with Firefox**, use Xvfb (virtual display):

```yaml
# GitHub Actions example
- name: Install Xvfb
  run: sudo apt-get install -y xvfb

- name: Run Firefox WebGL tests
  run: xvfb-run --auto-servernum npx playwright test --project=firefox-webgl
```

## Hybrid Model: Tests Serve Dual Purpose

**New Feature Validation → Regression Tests**

```
Developer/Tech Artist writes E2E test
                ↓
           QA validates feature
                ↓
          Test passes
                ↓
    Feature merged to main
                ↓
    Test becomes regression check in CI/CD
```

## Decision Framework

| Test Result        | Action                             |
| ------------------ | ---------------------------------- |
| All E2E tests pass | Mark as PASSED                     |
| Some tests fail    | Mark as NEEDS_FIXES with bug notes |
| Console errors     | Mark as NEEDS_FIXES                |
| No test exists     | Create test first, then validate   |

## Anti-Patterns

❌ **DON'T:**

- Use Playwright MCP directly for validation
- Skip E2E tests because automated checks passed
- Mark as passed without running tests
- Assume "it works on my machine"

✅ **DO:**

- Always run E2E tests for validation
- Create tests if missing
- Verify all acceptance criteria with tests
- Document failures with test output

## Validation Checklist

For each validation:

- [ ] E2E test file exists in `tests/e2e/`
- [ ] `npm run test:e2e` runs without errors
- [ ] All acceptance criteria covered by tests
- [ ] No console errors during tests
- [ ] Performance acceptable (60 FPS target)
- [ ] Screenshot comparison passes (for visual features)
- [ ] Tests committed to repository

## Bug Report Format

When tests fail, include in bug notes:

```markdown
## Test Failure

**Test File**: tests/e2e/{feature}-suite.spec.ts
**Test Name**: "{test-name}"
**Error Message**: {error from test output}

**Steps to Reproduce**:

1. npm run test:e2e -- -g "{test-name}"
2. Observe failure

**Expected**: {expected behavior}
**Actual**: {actual behavior from test output}
```

## Server Management

**⚠️ CRITICAL: Use `shared-lifecycle` skill for server management.**

### Server Detection (Before Any Browser Interaction)

**⚠️ IMPORTANT: Playwright's `webServer` config manages servers for E2E tests automatically.**

When running `npm run test:e2e`, Playwright automatically starts:
- `npm run dev` (port 3000) with `reuseExistingServer: !process.env.CI`
- `npm run server` (port 2567) with `reuseExistingServer: false` (for multiplayer)

**DO NOT manually start servers for E2E tests.**

### Decision Tree

```
                    Running E2E tests?
                            |
            ┌───────────────┴───────────────┐
            │                               │
       YES (npm run test:e2e)        NO (Manual MCP validation)
            │                               │
            ▼                               ▼
   DO NOT start servers         Check if servers running
   Playwright manages them       If YES: use existing
   Cleanup is automatic          If NO: start and track
```

### Server Check Pattern

```bash
# Check if dev server is running (port 3000)
netstat -an | grep :3000 || lsof -i :3000

# Alternative: Try curl to detect Vite
curl -s http://localhost:3000 | grep -q "vite" && echo "RUNNING" || echo "NOT_RUNNING"
```

### E2E Test Path (Standard Validation)

```bash
# Playwright handles server lifecycle via webServer config
npm run test:e2e

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

**MANDATORY CLEANUP after all tests complete (pass OR fail):**

Use the cleanup patterns from `shared-lifecycle` skill to ensure:

- Dev server is stopped
- Ports are released
- No orphaned processes remain

**See also:** `shared-lifecycle` skill for complete process management patterns.

## References

- **[qa-e2e-test-creation/SKILL.md](../qa-e2e-test-creation/SKILL.md)** - Full E2E test patterns
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [tests/pages/](tests/pages/) - Page Object Model classes

## Camera Validation Pattern (feat-tps-004, 2026-01-27)

**⚠️ CRITICAL: Camera validation requires E2E tests with exact value verification.**

When validating camera features (TPS, orbital, etc.), use systematic E2E test coverage:

```typescript
// tests/e2e/camera-suite.spec.ts
test.describe('TPS Camera Validation - feat-tps-004', () => {
  test('should validate shoulder offset values match acceptance criteria', async ({ page }) => {
    await page.goto('http://localhost:3000/?scene=controls');
    await page.waitForSelector('canvas');

    // Access camera test state (exposed by test scene)
    const cameraState = await page.evaluate(() => {
      return (window as any).__cameraTestState;
    });

    // Verify EXACT values from acceptance criteria
    expect(cameraState.shoulderOffsetRight).toBe(0.75);
    expect(cameraState.shoulderOffsetLeft).toBe(-0.75);

    // Common bug: wrong values (0.85 instead of 0.75)
    if (cameraState.shoulderOffsetRight !== 0.75) {
      throw new Error(
        `shoulderOffsetRight mismatch: expected 0.75, got ${cameraState.shoulderOffsetRight}`
      );
    }
  });

  test('should validate look-at offset is applied', async ({ page }) => {
    await page.goto('http://localhost:3000/?scene=controls');
    await page.waitForSelector('canvas');

    // Screenshot validation for visual composition
    await page.screenshot({
      path: 'test-results/camera/shoulder-offset.png',
    });

    // Verify look-at direction
    const lookAtOffset = await page.evaluate(() => {
      const camera = (window as any).__testCamera;
      return camera ? camera.userData.lookAtOffset : null;
    });

    expect(lookAtOffset).toBeDefined();
    expect(Math.abs(lookAtOffset)).toBe(0.75);
  });
});
```

**Learned from feat-tps-004 retrospective:**

1. **Value mismatch detection**: Implementation had 0.85, acceptance criteria specified 0.75
   - Solution: E2E tests verify EXACT numerical values from acceptance criteria

2. **Missing look-at offset**: Camera position was offset but looked at center
   - Solution: E2E tests verify BOTH position and look-at are offset

3. **Scene routing test**: URL-based scene loading must be tested
   - Solution: Test `?scene=controls` actually loads correct scene

**Camera E2E test checklist:**
- [ ] Position offset values match acceptance criteria exactly
- [ ] Look-at offset is applied (same as position offset)
- [ ] Shoulder swap functionality tested (X key)
- [ ] Screenshot validation for visual composition
- [ ] Scene routing tested (URL parameters work)

**URL Scene Routing Pattern:**
```typescript
// main.tsx - useState/useEffect sync for URL-based routing
const [sceneParam, setSceneParam] = useState<string | null>(null);

useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const scene = params.get('scene');
  if (scene) {
    setSceneParam(scene);
    // Sync to gameStore
    gameStore.setPhase(scene as any);
  }
}, []);
```
