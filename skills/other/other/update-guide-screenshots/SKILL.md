---
name: update-guide-screenshots
description: Verify NiFi custom UI tabs via Chrome and update doc/guides screenshots and guides
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__claude-in-chrome__*
---

# Update Guide Screenshots Skill

Verifies the NiFi custom UI against existing documentation, takes fresh screenshots, and updates `doc/guides/` content to match the current UI.

## Parameters

Optional argument selects the workflow:
- `/update-guide-screenshots` — Full workflow: verify UI via Chrome, take screenshots, update docs
- `/update-guide-screenshots verify` — Chrome-only: browse UI tabs and report differences (no file changes)
- `/update-guide-screenshots screenshots` — Take screenshots only (Playwright headless, no Chrome needed)
- `/update-guide-screenshots docs` — Update documentation text only (assumes screenshots are current)

## Prerequisites

- NiFi and Keycloak containers must be running. Use `/deploy start` if not.
- For `verify` mode: Chrome browser with Claude-in-Chrome extension connected.
- For `screenshots` and default mode: Playwright installed in `e-2-e-playwright/`.

## Workflow

### Step 1: Verify Containers Running

```bash
./integration-testing/src/main/docker/check-status.sh --quiet
```

If not healthy, instruct the user to run `/deploy start` first. Do NOT start containers from this skill.

### Step 2: Read Current Documentation

Read these files to understand the current documented state:
- `doc/guides/QuickStart.adoc` — Main guide with processor and gateway documentation
- `doc/guides/IssuerConfigPropertiesGuide.adoc` — Detailed issuer configuration walkthrough

Also read all existing screenshot PNGs in `doc/guides/` to compare against the live UI.

### Step 3: Verify UI via Chrome (for `verify` and default mode)

Use Chrome browser automation to navigate the live NiFi UI and compare against documentation.

#### 3a. Log in to NiFi

1. Navigate to `https://localhost:9095/nifi/`
2. Enter credentials: `testUser` / `drowssap`
3. Click Log in
4. Wait for canvas to load (URL contains `/process-groups/`)

#### 3b. Inspect JWT Processor Custom UI

1. From root canvas, double-click the **JWT Auth Pipeline** process group
2. Right-click the **MultiIssuerJWTTokenAuthenticator** processor → click **Advanced**
3. Wait for custom UI to load
4. Verify and screenshot each tab:
   - **Configuration** — Issuer form with Name, JWKS Source Type, Issuer URI, JWKS URL, Audience, Client ID
   - **Token Verification** — Token input textarea, Verify Token / Clear buttons, Verification Results area
   - **Metrics** — Shows "Metrics Not Available" message for JWT processor
   - **Help** — Accordion sections: Getting Started, Issuer Configuration, Authorization Rules, Token Verification, Troubleshooting, Additional Resources
5. Click **Back to Processor** to return

#### 3c. Inspect REST API Gateway Custom UI

1. Navigate to root canvas, double-click the **REST API Gateway** process group
2. Right-click the **RestApiGateway** processor → click **Advanced**
3. Wait for custom UI to load
4. Verify and screenshot each tab:
   - **Endpoint Configuration** — Global Settings table + route table with Name, Path, Methods, Enabled, Actions columns
   - **Endpoint Tester** — Route dropdown, Method dropdown, Authorization Token textarea, Send Request button
   - **Issuer Configuration** — Issuer table with Name, JWKS Source, Type, Issuer URI, Actions columns
   - **Token Verification** — Same as JWT processor Token Verification
   - **Metrics** — Gateway Metrics with Token Validation, HTTP Security, Gateway Events sections
   - **Help** — REST API Gateway accordion with Key Features, Tabs listing, Troubleshooting, Additional Resources

Also capture the **Route Editor** by clicking Edit on a route from the Endpoint Configuration tab.

#### 3d. Report Differences

Compare what was seen in Chrome against the existing screenshots and documentation text. Report:
- New tabs not documented
- Removed tabs still documented
- Changed content/layout within tabs
- Incorrect text descriptions

### Step 4: Take Fresh Screenshots (for `screenshots` and default mode)

Write a temporary Playwright script to `e-2-e-playwright/take-screenshots.mjs` and run it. The script must:

1. Use `@playwright/test` (installed in `e-2-e-playwright/node_modules`)
2. Launch headless Chromium with `--ignore-certificate-errors`, `ignoreHTTPSErrors: true`, and `locale: 'en-US'` to force English UI
3. Set viewport to `1456 x 816` for consistent screenshot dimensions
4. Log in via the NiFi login form (`testUser` / `drowssap`)
5. Use the NiFi REST API (`/nifi-api/flow/process-groups/root`) to discover processor IDs
6. Navigate to each processor's advanced UI via URL: `https://localhost:9095/nifi/#/process-groups/{pgId}/Processor/{procId}/advanced`
7. Wait for the iframe to load and locate it with `page.waitForSelector('iframe')` + `contentFrame()`
8. Click tabs WITHIN THE IFRAME using `frame.locator('a:visible').filter({ hasText: /^Tab Name$/ })`
   - IMPORTANT: Use `:visible` filter — some tabs have hidden duplicates with class "hidden"
9. Take `page.screenshot({ fullPage: true })` for each tab (captures the full NiFi shell including iframe)
10. Save screenshots to `doc/guides/` with these exact filenames

**JWT Processor screenshots:**

| Filename | Tab | Notes |
|----------|-----|-------|
| `ui-configuration-tab.png` | Configuration | Default tab, shows issuer form |
| `ui-token-verification-tab.png` | Token Verification | Empty token input state |

**Gateway Processor screenshots:**

| Filename | Tab | Notes |
|----------|-----|-------|
| `ui-gateway-endpoint-configuration.png` | Endpoint Configuration | Default tab, shows routes table |
| `ui-gateway-route-editor.png` | Endpoint Configuration | After clicking Edit on first route |
| `ui-gateway-endpoint-tester.png` | Endpoint Tester | Empty state |
| `ui-gateway-endpoint-tester-response.png` | Endpoint Tester | After clicking Send Request |
| `ui-gateway-issuer-configuration.png` | Issuer Configuration | Shows issuers table |
| `ui-gateway-token-verification.png` | Token Verification | Empty token input state |
| `ui-gateway-metrics.png` | Metrics | Shows Gateway Metrics sections |
| `ui-gateway-help.png` | Help | Shows Component Help accordion |

After the script runs successfully, delete the temporary `take-screenshots.mjs` file.

### Step 5: Update Guide Documentation (for `docs` and default mode)

Update `doc/guides/QuickStart.adoc` and `doc/guides/IssuerConfigPropertiesGuide.adoc` based on differences found:

Common things to check and update:
- **Tab counts and names** in gateway description (e.g., "four tabs" → "six tabs")
- **Tab list** in gateway introduction paragraph
- **New sections** for any tabs not yet documented (with `image::` directive and description)
- **Removed sections** for tabs that no longer exist
- **Screenshot references** — ensure every `image::` directive matches an actual file in `doc/guides/`
- **Login credentials** — must be `testUser` / `drowssap` (not `admin/adminadminadmin`)
- **Cross-reference anchors** — verify `link:` targets resolve correctly

Do NOT change sections about tabs whose UI has not changed. Only update what is actually different.

### Step 6: Report Summary

Output a summary table showing:
- Which screenshots were updated/added/unchanged
- Which documentation sections were modified
- Any issues found that require manual attention

## Key Paths

| Path | Purpose |
|------|---------|
| `doc/guides/QuickStart.adoc` | Main quick start guide |
| `doc/guides/IssuerConfigPropertiesGuide.adoc` | Detailed issuer configuration guide |
| `doc/guides/*.png` | Guide screenshots |
| `e-2-e-playwright/` | Playwright project root (has `node_modules/`) |
| `e-2-e-playwright/utils/constants.js` | Processor type names for API lookups |

## Critical Rules

- NEVER start or stop Docker containers — this skill only reads the running UI
- ALWAYS delete the temporary `take-screenshots.mjs` after use
- ALWAYS use `:visible` selector when clicking tabs in iframes (hidden duplicates exist)
- Screenshots MUST use `fullPage: true` to capture the complete NiFi shell
- The Playwright script MUST run from the `e-2-e-playwright/` directory (for `node_modules` resolution)
- Do NOT update screenshots that haven't visually changed — compare before overwriting
- NiFi custom UI loads inside an iframe on the `/advanced` URL — all tab interactions must target the iframe's `contentFrame()`
- Screenshots MUST always be in English — the UI auto-detects browser language via `navigator.language`, so Playwright must launch with `locale: 'en-US'` to prevent German or other translations from appearing
