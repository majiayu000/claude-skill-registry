---
name: Visual Snapshot Skill
version: 1.1.0
description: Adds visual capabilities to the agent using Playwright MCP with Script Execution support.
mcpDependencies:
  - playwright
allowed-tools:
  - playwright_navigate
  - playwright_evaluate
  - playwright_evaluate
  - audit_a11y
  - compare_images
---

## Capabilities

This skill allows you to "see" the Shopify theme and interact with it programmatically. You can navigate, click, type, and execute complex JavaScript logic to verify your work.

## Dependencies

- **MCP Server**: `@modelcontextprotocol/server-playwright`
- **Shopify CLI**: Must be running `shopify theme dev` to serve the site (default: http://localhost:9292).

## Tools Usage Guide

### 1. `playwright_navigate`

Use this to open the local development URL.

- **Param** `url`: usually `http://localhost:9292`.

### 2. `playwright_screenshot`

Use this to capture the current state.

- **Param** `name`: filename prefix.
- **Param** `selector`: capture specific element.
- **Param** `width`/`height`: viewport dimensions.

### 3. `playwright_evaluate` (Advanced: Remote Code Execution)

**This is the most powerful tool.** It allows you to execute unlimited Playwright/JS code in the browser context in a SINGLE turn.

- **Param** `script`: The JavaScript code to run. Code runs inside the browser page context.
- **Usage**: Use this for complex interactions (loops, conditionals) or to batch multiple actions (Filling forms -> Clicking -> Waiting -> Returning data).
- **Example**:
  ```javascript
  // Agent sends this string to 'script' param
  const items = document.querySelectorAll(".product-card");
  const results = [];
  for (const item of items) {
    if (item.innerText.includes("Sale")) {
      item.querySelector("button").click(); // Add to cart
      results.push(item.id);
    }
  }
  return results; // Returns data to Agent
  ```

## Workflow: Visual Verification Loop

When asked to fix a UI bug or implement a design:

1.  **Analyze**: Understand the request.
2.  **Snapshot (Before)**:
    - Use `playwright_navigate`.
    - Use `playwright_screenshot`.
    - _Tip: Use `playwright_evaluate` to setup complex state (e.g., login, add item to cart) before screenshot._
    - **CRITICAL**: Use specific MCP tool to view the image file if not automatically shown.
3.  **Code**: Apply fixes to Liquid/CSS.
4.  **Snapshot (After)**: Verify changes.

## Advanced Pattern: "Code-as-Params"

Instead of calling `click` -> `wait` -> `click` (3 turns), just write a script:
`playwright_evaluate(script="document.getElementById('menu-toggle').click();")`
