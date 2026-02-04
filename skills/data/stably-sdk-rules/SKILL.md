---
name: stably-sdk-rules
description: |
  AI rules and SDK reference for writing tests with Stably Playwright SDK.
  Use this skill when writing or modifying Playwright tests with Stably AI
  features. Triggers on tasks involving toMatchScreenshotPrompt, agent.act(),
  page.extract(), or when deciding between Playwright vs Stably SDK methods.
  Includes best practices for AI assertions, extraction, and autonomous agents.
license: MIT
metadata:
  author: stably
  version: '1.0.0'
---

# Stably SDK — AI Rules (Playwright‑compatible)

**Assumption:** Full Playwright parity unless noted below.

## Import

```ts
import { test, expect } from "@stablyai/playwright-test";

// Additional exports available:
import {
  defineConfig,       // Enhanced defineConfig with stably project support
  stablyReporter,     // Reporter for CI/cloud integration
  setApiKey,          // Programmatic API key configuration
  getDirname,         // ESM __dirname equivalent
  getFilename,        // ESM __filename equivalent
} from "@stablyai/playwright-test";
```

## Install & Setup

```bash
npm install @playwright/test @stablyai/playwright-test
export STABLY_API_KEY=YOUR_KEY
```

```ts
import { setApiKey } from "@stablyai/playwright-test";
setApiKey("YOUR_KEY");
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STABLY_API_KEY` | API key for authentication | (required) |
| `STABLY_PROJECT_ID` | Project ID for reporter | (required for reporter) |
| `STABLY_API_URL` | Custom API endpoint | `https://api.stably.ai` |
| `STABLY_WS_URL` | Custom WebSocket endpoint | `wss://api.stably.ai/reporter` |

## When to Use Stably SDK vs Playwright

**Prioritization:**
1. **Test accuracy and stability are the most important factors** - prioritize reliability over cost/speed.
2. **Otherwise, use Playwright whenever possible** since it's cheaper and faster.
3. **For interactions:** If the interaction will be hard to express as Playwright or will be too brittle that way (e.g., the scroll amount changes every time), then use `agent.act()`. **Any canvas-related operations, or any drag/click operations that require coordinates, must use `agent.act()`** (more semantic meaning, and less flaky).
4. **For assertions:** Use Playwright if it fulfills the purpose. But if the assertion is very visual-heavy, use Stably's `toMatchScreenshotPrompt`.
5. **Use Stably SDK methods if it helps your tests pass** - when Playwright methods are insufficient or unreliable.

## AI Assertions (intent‑based visuals)

```ts
await expect(page).toMatchScreenshotPrompt(
  "Shows revenue trend chart and spotlight card",
  { timeout: 30_000 }
);
await expect(page.locator(".header"))
  .toMatchScreenshotPrompt("Nav with avatar and bell icon");
```

**Signature:** `expect(page|locator).toMatchScreenshotPrompt(prompt: string, options?: ScreenshotOptions)`

* Use for **dynamic** UIs; keep prompts specific; scope with elements (using locators) when possible.
* **Consider whether you need `fullPage: true`**: Ask yourself if the assertion requires content beyond the visible viewport (e.g., long scrollable lists, full page layout checks). If only viewport content matters, omit `fullPage: true` — it's faster and cheaper. Use it only when you genuinely need to capture content outside the browser window's visible area.

## AI Extraction (visual → data)

```ts
// Extract from entire page
const txt = await page.extract("List revenue, active users, and churn rate");

// Extract from specific element (more focused, better results)
const headerText = await page.locator(".header").extract("Get the username displayed");
```

Typed with Zod:

```ts
import { z } from "zod";
const Metrics = z.object({ revenue: z.string(), activeUsers: z.number(), churnRate: z.number() });
const m = await page.extract("Return revenue (currency), active users, churn %", { schema: Metrics });

// Also works on locators
const UserSchema = z.object({ name: z.string(), role: z.string() });
const userData = await page.locator(".user-panel").extract("Get user info", { schema: UserSchema });
```

**Signatures:**

* `page.extract(prompt: string): Promise<string>`
* `page.extract<T extends z.AnyZodObject>(prompt, { schema: T }): Promise<z.output<T>>`
* `locator.extract(prompt: string): Promise<string>`
* `locator.extract<T extends z.AnyZodObject>(prompt, { schema: T }): Promise<z.output<T>>`

## AI Agent (autonomous workflows)

### When Test Generation Uses `agent.act()` vs Raw Playwright

Stably's test generation agent intelligently chooses between raw Playwright code and `agent.act()`:

- **For repeatable, stable actions**: The test generation agent will try to turn these into raw Playwright code when first generating tests. Raw Playwright is faster and more cost-effective.
- **For dynamic or unstable pages**: If the agent finds that the page changes frequently and it can't find stable Playwright selectors/code for an action, it will use `agent.act()` instead.

This means you may see a mix of both in generated tests—this is intentional and optimizes for reliability while keeping costs down where possible.

### Using the Agent Fixture

Use the `agent` fixture to execute complex, human-like workflows:

```ts
test("complex workflow", async ({ agent, page }) => {
  await page.goto("/orders");
  await agent.act("Find the first pending order and mark it as shipped", { page });
});

// Or create manually
const agent = context.newAgent();
await agent.act("Your task here", { page, maxCycles: 10 }); // split into smaller steps if possible
```

**Signature:** `agent.act(prompt: string, options: { page: Page, maxCycles?: number, model?: Model }): Promise<void>`

* Throws `Error` if the agent fails to complete the task (check `error.message` for the AI's failure reason)
* Default maxCycles: 30
* Supported models: `"anthropic/claude-sonnet-4-5-20250929"` (default), `"google/gemini-2.5-computer-use-preview-10-2025"`, or any custom model string

### Passing Variables to Prompts

You can use template literals to pass variables into your prompts:

```ts
const duration = 24 * 7 * 60;
await agent.act(`Enter the duration of ${duration} seconds`, { page });

const username = "john.doe@example.com";
await agent.act(`Login with username ${username}`, { page });
```

### Self-Contained Prompts

All prompts to Stably SDK AI methods (agent.act, toMatchScreenshotPrompt, extract) must be self-contained with all necessary information:

1. **No implicit references to outside context** - prompts cannot reference previous actions or state that the AI method doesn't have access to:
   - ❌ Bad: `agent.act("Verify the field you just filled in the form is 4", { page })`
   - ✅ Good: `agent.act("Verify the 'timeout' field in the form has value 4", { page })`
   - ❌ Bad: `agent.act("Pick something that's not in the previous step", { page })`
   - ✅ Good: `const selectedItem = "Option A"; await agent.act(\`Pick an option other than ${selectedItem}\`, { page })`

2. **Pass information between AI methods using explicit variables:**
   ```ts
   // Extract data, then use it in next action
   const orderId = await page.extract("Get the order ID from the first row");
   await agent.act(`Cancel order with ID ${orderId}`, { page });
   ```

3. **Include detailed instructions and domain knowledge** to help the AI perform the task successfully:
   - ❌ Bad: `agent.act("Fill in the form", { page })`
   - ✅ Good: `agent.act("Fill in the form with test data. On page 4 you might run into a popup asking for premium features - just click 'Skip' or 'Cancel' to ignore it", { page })`

### Optimizing Agent Performance

**IMPORTANT:** The fewer actions/cycles agent.act() needs to do, the better it performs. Offload work to Playwright code when possible:

1. If your prompt has work that could be done by Playwright code, use Playwright for that work, and only use agent.act() for actions that are hard for Playwright (canvas operations, dynamic decision making, etc.)
2. If your prompt has repetition (e.g., do it 5 times), calculations (e.g., type 24*7*60 seconds), or other code-suitable tasks, use code for those, and only have agent.act() perform the agent-suitable part.
3. If your prompt has an if/else condition that can be expressed in code, use code for the condition, and only have agent.act() perform the agent-suitable part.

**Examples:**
- ❌ Bad: `"Click the button 5 times"`
- ✅ Good: `"Click the button"` (and include this in a loop that runs 5 times)
- ❌ Bad: `"enter the duration of 24*7*60 seconds"`
- ✅ Good: Calculate in code (`const sum = 24*7*60`), then use `\`enter the duration of ${sum} seconds\``

## CI Reporter / Cloud

```bash
npm install @stablyai/playwright-test
```

```ts
// playwright.config.ts
import { defineConfig, stablyReporter } from "@stablyai/playwright-test";

export default defineConfig({
  reporter: [
    ["list"],
    stablyReporter({
      apiKey: process.env.STABLY_API_KEY,
      projectId: process.env.STABLY_PROJECT_ID,
      // Optional: Scrub sensitive values from traces before upload
      sensitiveValues: ["secret-password", process.env.API_SECRET].filter(Boolean),
    }),
  ],
  use: {
    trace: "on", // Required for trace uploads
  },
});
```

**Reporter Options:**
- `apiKey` (required): Your Stably API key
- `projectId` (required): Your Stably project ID
- `sensitiveValues` (optional): Array of strings to scrub from trace files
- `notificationConfigs` (optional): Per-project notification settings for Slack/email

## Notifications (Email/Slack)

Configure notifications per project via `stably` property in defineConfig:

```ts
import { defineConfig, stablyReporter } from "@stablyai/playwright-test";

export default defineConfig({
  reporter: [stablyReporter({ apiKey: "...", projectId: "..." })],
  projects: [
    {
      name: "smoke",
      stably: {
        notifications: {
          slack: {
            channelName: "#test-alerts",
            notifyOnStart: true,
            notifyOnResult: "failures-only", // "all" | "failures-only"
          },
          email: {
            to: ["team@example.com"],
            notifyOnResult: "all",
          },
        },
      },
    },
  ],
});
```

## Commands

```bash
# Recommended for Stably reporter + auto-heal
npx stably test

# Still supported (requires your reporter/config to be set up)
npx playwright test
# All Playwright CLI flags still work (headed, ui, project, file filters…)

# When running tests for debugging/getting stacktraces:
npx playwright test --reporter=list  # disable HTML reporter, shows terminal output directly
```

## ESM Utilities

For ESM projects needing `__dirname` or `__filename` equivalents:

```ts
import { getDirname, getFilename } from "@stablyai/playwright-test";

const __dirname = getDirname(import.meta.url);
const __filename = getFilename(import.meta.url);

// Use in tests for file paths
import path from "path";
await page.setInputFiles("input", path.join(__dirname, "fixtures", "file.pdf"));
```

## Best Practices

* **CRITICAL: All locators must use the `.describe()` method** for readability in trace views and test reports. Example: `page.getByRole('button', { name: 'Submit' }).describe('Submit button')` or `page.locator('table tbody tr').first().describe('First table row')`
* Scope visual checks with locators; keep prompts specific with labels/units.
* Use `toHaveScreenshot` for stable pixel‑perfect UIs; `toMatchScreenshotPrompt` for dynamic UIs.
* **Be deliberate with `fullPage: true`**: Default to viewport-only screenshots. Only use `fullPage: true` when your assertion genuinely requires content beyond the visible viewport (e.g., verifying footer content on a long page, checking full scrollable lists). Viewport captures are faster and more cost-effective.

## Troubleshooting

* **Slow assertions** → scope visuals; reduce viewport.
* **Agent stops early** → increase `maxCycles` or break task into smaller steps.

## Minimal Template

```ts
import { test, expect } from "@stablyai/playwright-test";

test("AI‑enhanced dashboard", async ({ page, agent }) => {
  await page.goto("/dashboard");

  // Use agent for complex workflows
  await agent.act("Navigate to settings and enable notifications", { page });

  // Use AI assertions for dynamic content
  await expect(page).toMatchScreenshotPrompt(
    "Dashboard shows revenue chart (>= 6 months) and account spotlight card"
  );
});
```

---

## Creating E2E Tests with Stably SDK

When creating end-to-end tests, follow these guidelines:

### 1. Understand Requirements
- Ask clarifying questions if the test scenario is unclear
- Identify the user flow, expected outcomes, and edge cases
- Determine which pages/components need testing

### 2. Choose the Right Tools

**Use Playwright when:**
- Simple, deterministic interactions (clicks, fills, selects)
- Static content that doesn't change
- Cost and speed are priorities

**Use Stably SDK when:**
- Visual assertions on dynamic UIs → `toMatchScreenshotPrompt()`
- Complex multi-step workflows → `agent.act()`
- Canvas interactions or coordinate-based operations → `agent.act()`
- Data extraction from UI → `page.extract()`
- Elements are hard to locate reliably

### 3. Structure the Test

```ts
import { test, expect } from "@stablyai/playwright-test";

test("descriptive test name", async ({ page, agent }) => {
  // 1. Setup & Navigation
  await page.goto("/your-page");

  // 2. Interactions (prefer Playwright, use agent for complex workflows)
  await page.getByRole('button', { name: 'Login' }).describe('Login button').click();

  // For complex workflows:
  await agent.act("Complete the multi-step checkout process", { page });

  // 3. Assertions (prefer Playwright, use AI assertions for dynamic content)
  await expect(page.getByText('Welcome')).toBeVisible();

  // For visual/dynamic assertions:
  await expect(page).toMatchScreenshotPrompt(
    "Dashboard shows revenue chart and user profile card"
  );
});
```

### 4. Best Practices

**CRITICAL:**
- **Always use `.describe()` on locators** for better traceability
  ```ts
  page.getByRole('button', { name: 'Submit' }).describe('Submit form button')
  ```

**General:**
- Write clear, descriptive test names
- Add comments explaining complex logic
- Use semantic locators (getByRole, getByLabel) over CSS selectors
- Keep prompts specific for AI assertions
- Scope visual checks with locators when possible
- Default to viewport screenshots (only use `fullPage: true` when needed)
- Handle async operations with proper waits
- Consider error states and edge cases

### 5. Example Patterns

**Login Flow:**
```ts
test("user can login successfully", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel('Email').describe('Email input').fill('user@example.com');
  await page.getByLabel('Password').describe('Password input').fill('password123');
  await page.getByRole('button', { name: 'Sign In' }).describe('Sign in button').click();

  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByText('Welcome back')).toBeVisible();
});
```

**Complex Workflow with AI:**
```ts
test("complete checkout process", async ({ page, agent }) => {
  await page.goto("/products");

  // Use agent for complex multi-step process
  await agent.act(
    "Add 2 items to cart, proceed to checkout, and fill shipping details",
    { page }
  );

  // Verify outcome
  await expect(page).toMatchScreenshotPrompt(
    "Order confirmation page with order number and thank you message"
  );
});
```

**Visual Regression:**
```ts
test("homepage matches design", async ({ page }) => {
  await page.goto("/");

  // AI-powered visual assertion for dynamic content
  await expect(page).toMatchScreenshotPrompt(
    "Hero section with call-to-action button, feature cards below, and navigation bar at top"
  );
});
```
