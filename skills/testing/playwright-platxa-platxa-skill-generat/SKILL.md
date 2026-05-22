---
name: playwright
description: >-
  Use when the task requires automating a real browser from the terminal
  via playwright-cli: navigation, form filling, snapshots, screenshots,
  data extraction, tracing, and UI-flow debugging. Prefer the bundled
  wrapper script so the CLI works without a global install. Treat this
  skill as CLI-first automation; do not pivot to @playwright/test unless
  the user explicitly asks for test files.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - browser-automation
    - playwright
    - testing
    - scraping
  provenance:
    upstream_source: "playwright"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T18:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.8
---

# Playwright CLI Browser Automation

Drive a real browser from the terminal using `playwright-cli`. Navigate pages, fill forms, capture screenshots, extract data, and debug UI flows without writing test files.

## Overview

Playwright CLI provides headless and headed browser control through a single command-line interface. Every interaction follows a snapshot-first pattern: open a page, take an accessibility snapshot to obtain stable element references (`e1`, `e2`, ...), then interact using those refs.

**What you will learn:**

- Setting up the wrapper script and verifying prerequisites
- The snapshot-interact-snapshot core loop
- Form filling, data extraction, and multi-tab workflows
- Tracing and debugging production UI issues
- Session isolation for parallel workstreams

**Prerequisites:**

- Node.js >= 18 and npm/npx on `PATH`
- The bundled `scripts/playwright_cli.sh` wrapper (avoids global install)

## Learning Path

### Level 1: Setup and First Snapshot

**Verify Node.js and npx are available:**

```bash
node --version   # must be >= 18
npm --version
command -v npx >/dev/null 2>&1 && echo "npx ready"
```

If npx is missing, install Node.js first. Once available, set the wrapper path:

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PWCLI="$SKILL_DIR/scripts/playwright_cli.sh"
```

**Open a page and take the first snapshot:**

```bash
"$PWCLI" open https://playwright.dev
"$PWCLI" snapshot
```

The snapshot returns an accessibility tree with stable refs like `e1`, `e3`, `e15`. Use these refs for all subsequent interactions.

**Key point:** Always snapshot before interacting. Stale refs cause `ElementNotFound` errors.

### Level 2: Core Interaction Loop

The fundamental pattern is open-snapshot-interact-snapshot:

```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot          # get initial refs
"$PWCLI" click e3          # interact with ref from snapshot
"$PWCLI" snapshot          # refresh refs after DOM change
```

**When to re-snapshot:**

- After any navigation (`click` on a link, `go-back`, `go-forward`)
- After modal open/close, dropdown expand, or tab switch
- After `fill`/`type` if it triggers dynamic content
- Whenever a command returns `ElementNotFound`

**Common interactions:**

```bash
"$PWCLI" click e5                    # click element
"$PWCLI" dblclick e7                 # double-click
"$PWCLI" fill e1 "user@test.io"     # fill input field
"$PWCLI" type "search query"        # type into focused element
"$PWCLI" press Enter                # press keyboard key
"$PWCLI" select e9 "option-value"   # select dropdown option
"$PWCLI" hover e4                   # hover for tooltips
"$PWCLI" check e12                  # check checkbox
"$PWCLI" uncheck e12                # uncheck checkbox
"$PWCLI" upload ./document.pdf      # upload file
"$PWCLI" drag e2 e8                 # drag and drop
```

**Capture artifacts:**

```bash
"$PWCLI" screenshot                  # full viewport PNG
"$PWCLI" screenshot e5               # element-specific screenshot
"$PWCLI" pdf                         # save page as PDF
```

### Level 3: Advanced Patterns

**Form submission workflow:**

```bash
"$PWCLI" open https://app.example.com/login --headed
"$PWCLI" snapshot
"$PWCLI" fill e1 "admin@company.io"
"$PWCLI" fill e2 "securePass!42"
"$PWCLI" click e3                    # submit button
"$PWCLI" snapshot                    # verify post-login state
"$PWCLI" screenshot                  # capture dashboard
```

**Data extraction with eval:**

```bash
"$PWCLI" eval "document.title"
"$PWCLI" eval "el => el.textContent" e12
"$PWCLI" eval "JSON.stringify([...document.querySelectorAll('table tr')].map(r => [...r.cells].map(c => c.textContent)))"
```

**Multi-tab workflows:**

```bash
"$PWCLI" tab-new https://docs.example.com
"$PWCLI" tab-list                    # see all open tabs
"$PWCLI" tab-select 0               # switch to first tab
"$PWCLI" snapshot                    # always snapshot after tab switch
"$PWCLI" tab-close 1                # close second tab
```

**Debug with tracing:**

```bash
"$PWCLI" open https://app.example.com --headed
"$PWCLI" tracing-start
"$PWCLI" snapshot
"$PWCLI" click e5
"$PWCLI" fill e8 "test data"
"$PWCLI" click e10
"$PWCLI" tracing-stop               # saves trace.zip
```

The trace file can be viewed at `trace.playwright.dev` for timeline, network, and DOM inspection.

**Session isolation:**

```bash
"$PWCLI" --session checkout open https://shop.example.com/cart
"$PWCLI" --session checkout snapshot
"$PWCLI" --session admin open https://admin.example.com
"$PWCLI" --session admin snapshot
```

Or set once per shell:

```bash
export PLAYWRIGHT_CLI_SESSION=checkout
"$PWCLI" open https://shop.example.com/cart
```

**Console and network inspection:**

```bash
"$PWCLI" console                     # all console messages
"$PWCLI" console warning             # warnings and errors only
"$PWCLI" network                     # all network requests
```

**Browser window control:**

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" resize 1920 1080
```

## Best Practices

### Do

- Snapshot before every interaction sequence
- Re-snapshot immediately after navigation or significant DOM mutations
- Use `--headed` when visual confirmation helps debugging
- Use `--session` to isolate parallel workflows
- Capture screenshots as evidence after completing multi-step flows
- Store artifacts under `output/playwright/<label>/` to keep them organized
- Use `eval` for targeted data extraction rather than scraping full HTML
- Set `PWCLI` once at session start and reference it everywhere

### Avoid

- Referencing element IDs (`e3`, `e12`) without a recent snapshot
- Using `run-code` or `eval` to bypass the snapshot-ref pattern
- Running `@playwright/test` specs unless the user specifically requests it
- Assuming refs survive across navigation or modal open/close
- Hardcoding element refs in scripts (they change between page loads)
- Skipping the npx prerequisite check

## Common Questions

### Q: Element ref `e5` not found after clicking a link?

**A**: Navigation invalidates all refs. Run `"$PWCLI" snapshot` after the click completes, then use the new refs from the fresh snapshot.

### Q: How do I handle authentication cookies across sessions?

**A**: Named sessions (`--session myapp`) maintain separate browser contexts with independent cookie jars. Cookies persist within a session until the browser closes.

### Q: Can I run playwright-cli without Node.js?

**A**: No. The CLI depends on npx to resolve `@playwright/mcp`. Verify with `command -v npx` before starting. The wrapper script exits with an error if npx is missing.

### Q: How do I configure viewport size or headless mode by default?

**A**: Create a `playwright-cli.json` configuration file:

```json
{
  "browser": {
    "launchOptions": { "headless": false },
    "contextOptions": {
      "viewport": { "width": 1280, "height": 720 }
    }
  }
}
```

Place it in the working directory or pass `--config path/to/config.json`.

## Examples

### Example 1: Scrape a Table

```
User: Extract the pricing table from https://example.com/pricing
Assistant:
  1. "$PWCLI" open https://example.com/pricing
  2. "$PWCLI" snapshot  →  identifies table at e14
  3. "$PWCLI" eval "JSON.stringify([...document.querySelectorAll('#pricing tr')].map(r => [...r.cells].map(c => c.textContent)))"
  4. "$PWCLI" screenshot  →  saves visual evidence
  Result: Returns JSON array of row/cell text content
```

### Example 2: Fill and Submit a Login Form

```
User: Log into https://app.example.com with test credentials
Assistant:
  1. "$PWCLI" open https://app.example.com/login --headed
  2. "$PWCLI" snapshot  →  e1=email, e2=password, e3=submit
  3. "$PWCLI" fill e1 "test@example.com"
  4. "$PWCLI" fill e2 "TestPass123!"
  5. "$PWCLI" click e3
  6. "$PWCLI" snapshot  →  verify redirect to dashboard
  7. "$PWCLI" screenshot  →  capture logged-in state
```

### Example 3: Debug a Broken Checkout Flow

```
User: The checkout button does nothing on our staging site
Assistant:
  1. "$PWCLI" open https://staging.shop.example.com/cart --headed
  2. "$PWCLI" tracing-start
  3. "$PWCLI" snapshot  →  locate checkout button at e22
  4. "$PWCLI" click e22
  5. "$PWCLI" console warning  →  check for JavaScript errors
  6. "$PWCLI" network  →  inspect failed API requests
  7. "$PWCLI" tracing-stop  →  save trace for detailed analysis
  Result: Trace reveals 403 on POST /api/checkout (expired CSRF token)
```

## Guardrails

- Always verify npx availability before running any playwright-cli command
- Always snapshot before referencing element IDs like `e12`
- Re-snapshot when refs seem stale or after `ElementNotFound` errors
- Prefer explicit CLI commands over `eval` and `run-code` unless data extraction requires JavaScript
- When you lack a fresh snapshot, use placeholder refs like `eX` and explain why
- Use `--headed` when a visual check adds value
- Default to CLI commands and workflows, not Playwright test specifications
- Store output artifacts under `output/playwright/<label>/` in the project directory

## References

Load these on demand when deeper detail is needed:

- **CLI command reference**: `references/cli-reference.md` -- full command listing with arguments
- **Workflow patterns**: `references/workflow-patterns.md` -- step-by-step recipes for common scenarios
