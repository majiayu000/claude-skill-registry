---
name: wix-app-validation
description: Validates Wix CLI applications are ready and working by running a sequential workflow of TypeScript check, build, preview, and e2e tests using Playwright MCP. Use when testing app readiness, verifying runtime errors, checking UI rendering, or before releases. Triggers include validate, test, e2e, check, verify, ready, working, runtime errors, UI check, preview test, build test, smoke test, tsc, typescript.
---

# Wix App Validation

Validates Wix CLI applications through a five-step sequential workflow: TypeScript compilation check, package installation, build, preview, and e2e testing.

## Non-Matching Intents

Do NOT use this skill for:

- **Creating new extensions** → Use `wix-dashboard-page`, `wix-embedded-script`, etc.
- **Deploying to production** → This is for validation/testing only
- **Unit testing** → This skill performs e2e/integration testing

## Validation Workflow

Execute these steps sequentially. Stop and report errors if any step fails.

### Step 1: TypeScript Compilation Check

Run TypeScript compiler to check for type errors before proceeding with any other steps:

```bash
npx tsc --noEmit
```

**Success criteria:**
- Exit code 0
- No TypeScript compilation errors
- All type checks pass

**On failure:** Report the specific TypeScript errors and stop validation. Common issues:
- Type mismatches between expected and actual types
- Missing type declarations for imported modules
- Incorrect generic type parameters
- Properties not existing on declared types
- Incompatible function signatures

**Example error output:**
```
src/dashboard/pages/offers/page.tsx:45:23 - error TS2339: Property 'id' does not exist on type 'undefined'.
src/components/OfferForm.tsx:12:5 - error TS2322: Type 'string' is not assignable to type 'number'.
```

### Step 2: Package Installation

Ensure all dependencies are installed before proceeding with the build.

**Detect package manager:**
- Check for `package-lock.json` → use `npm`
- Check for `yarn.lock` → use `yarn`
- Check for `pnpm-lock.yaml` → use `pnpm`
- Default to `npm` if no lock file is found

**Run installation command:**

```bash
# For npm
npm install

# For yarn
yarn install

# For pnpm
pnpm install
```

**Success criteria:**
- Exit code 0
- All dependencies installed successfully
- No missing peer dependencies warnings (unless expected)
- `node_modules` directory exists and contains expected packages

**On failure:** Report the installation errors and stop validation. Common issues:
- Network connectivity problems
- Corrupted lock files
- Version conflicts
- Missing Node.js or package manager

### Step 3: Build Validation

Run the build command and check for compilation errors:

```bash
npx wix build
```

**Success criteria:**
- Exit code 0
- No TypeScript errors
- No missing dependencies

**On failure:** Report the specific compilation errors and stop validation.

### Step 4: Preview Deployment

Start the preview server:

```bash
npx wix preview
```

**Success criteria:**
- Preview server starts successfully
- Preview URLs are generated (both site and dashboard)

**URL extraction:** Parse the terminal output to find both preview URLs. Look for patterns like:
- Site preview: `Site preview: https://...` or `Site URL: https://...`
- Dashboard preview: `Dashboard preview: https://...` or `Preview URL: https://...` or `Your app is available at: https://...`

Extract both URLs as they will be used in Step 5 for testing.

**On failure:** Report the preview startup errors and stop validation.

### Step 5: E2E Testing with Playwright MCP

Once the preview URL is available, use Playwright MCP tools to validate the application.

See [Playwright MCP Reference](references/PLAYWRIGHT_MCP.md) for complete tool documentation.

#### Pre-Flight Checklist

Before starting Playwright testing, create a test plan for each dashboard page extension:

**For each dashboard page extension, identify:**
1. **Primary user action**: What's the main button/action? (e.g., "Create Offer", "New Item", "Save")
2. **Secondary actions**: What other interactive elements exist? (filters, tabs, edit buttons)
3. **Empty states**: What buttons appear when no data exists?
4. **Form fields**: What inputs need testing?

**Create a mental testing checklist for each page:**
- [ ] Page loads without app-specific errors
- [ ] Primary action button exists and is clickable
- [ ] Console remains clean after button click
- [ ] No backend 5xx errors from YOUR app's APIs
- [ ] UI responds correctly to interaction

#### 5.1 Test Site Preview and All Extensions

Test both the site preview and all dashboard page extensions. Parse the preview output to identify:
- **Site preview URL**: The main site URL (typically shown as "Site preview" or similar)
- **Dashboard preview URL**: The base URL for dashboard pages

**A. Test Site Preview**

1. **Navigate to the site preview URL:**
   ```
   Tool: playwright__browser-navigate
   Args: { "url": "<site-preview-url>" }
   ```

2. **Wait for the page to load completely** before proceeding to validation steps (4.2-4.7).

3. **Run validation steps 5.2-5.7** to validate the site preview.

**B. Test All Dashboard Page Extensions**

Discover all dashboard page extensions from `src/extensions.ts` and test each one. For each extension:

1. **Navigate to the extension URL:**
   - Base dashboard preview URL: `<dashboard-preview-url>`
   - Extension routePath: from `routePath` property in each extension definition
   - Full URL: `<dashboard-preview-url>/<routePath>`
   - Example: If dashboard preview URL is `https://preview.wix.com/...` and routePath is `"offers"`, navigate to `https://preview.wix.com/.../offers`

   ```
   Tool: playwright__browser-navigate
   Args: { "url": "<dashboard-preview-url>/<routePath>" }
   ```

2. **Wait for the page to load completely** before proceeding to validation steps (5.2-5.7).

3. **Run validation steps 5.2-5.7** for each extension to ensure all dashboard pages are validated.

**Common dashboard page extensions to test:**
- Root page (routePath: `""` or `"/"`)
- Dashboard pages with any routePath value
- Nested routes with multiple path segments

**Note:** Only test dashboard page extensions (`extensions.dashboardPage`). Skip data extensions and embedded scripts for this validation step.

#### 5.2 Check for Runtime Errors

Check console errors at **THREE** critical moments:
1. **On initial page load** (wait 3-5 seconds for page to settle)
2. **After EACH button click or interaction**
3. **After any navigation or tab change**

```
Tool: playwright__browser-console-messages
Args: { "level": "error" }
```

**Distinguish between error types:**

✗ **CRITICAL - App Errors (FAIL validation):**
- Errors with stack traces pointing to YOUR source code
- Paths include: `/src/`, `/dashboard/`, `/extensions/`, your component files
- Example: `TypeError at /src/dashboard/pages/offers/page.tsx:45`
- Example: `ReferenceError: variable is not defined at components/OfferForm.tsx`

✓ **OK - Third-party Warnings:**
- Google Maps async loading warnings
- react-i18next warnings
- Sentry initialization logs

**Action on errors:**
- If CRITICAL app errors found → Mark page validation as **FAILED**
- Document all errors in the validation report with full messages

#### 5.3 Validate Backend API Calls

Check that all backend API calls are successful and not returning error status codes.

```
Tool: playwright__browser-network-requests
Args: {}
```

**Validate API responses:**
- Check all network requests for status codes
- **Critical failures:** Any 500 (Internal Server Error) responses from backend APIs
- **Warning:** 4xx responses (client errors) - note but may be expected in some cases
- **Success:** 200-299 status codes are acceptable
- Filter requests to only check API endpoints (typically `/api/` or backend service URLs)

**Check for:**
- No 500 errors from backend APIs
- No 502 (Bad Gateway) or 503 (Service Unavailable) errors
- Failed requests to Wix backend services
- Timeout errors on API calls

**On failure:** Report:
- Which API endpoint(s) failed
- HTTP status code(s) received
- Request URL and method
- Response body if available (may contain error details)

**Note:** This validation should be performed after the page has fully loaded and all API calls have completed. Wait for network activity to settle before checking.

#### 5.4 Interactive Testing

**CRITICAL**: Pages may load successfully but fail when users interact with them. You **MUST** test primary actions on every page.

**⚠️ VALIDATION REQUIREMENT**: Do NOT mark any page as validated until you have clicked at least one primary action button and verified no app errors occurred.

---

**For EACH dashboard page, perform these steps:**

**Step 1: Identify Interactive Elements**

Capture an accessibility snapshot to identify buttons and interactive elements:

```
Tool: playwright__browser-snapshot
Args: {}
```

**Step 2: Test Primary Action Button**

You **MUST** click at least one primary action button on each page:

```
Tool: playwright__browser-click
Args: { "element": "Primary action button name", "ref": "element-ref-from-snapshot" }
```

**Step 3: Check Console Errors After EACH Click**

Immediately after clicking, check for errors:

```
Tool: playwright__browser-wait-for
Args: { "time": 2 }  # Wait for action to complete

Tool: playwright__browser-console-messages
Args: { "level": "error" }
```

**Analyze the errors:**
- ✗ **App errors** (from YOUR code) → **FAIL** the page validation
- ⚠️ Platform errors → Note but continue
- ✓ No errors → **PASS**

**Step 4: Test Additional Interactions**

**Form inputs:**
```
Tool: playwright__browser-type
Args: { "element": "Input field", "ref": "input-ref", "text": "test value" }
```

**Navigation flows:**
- Click list items to navigate to detail views
- Click tabs to switch between sections
- Test back navigation

**Step 5: Document Results**

For each interaction tested, document:
- ✓ Button: "[Button Name]" - Clicked successfully, no errors
- ✗ Button: "[Button Name]" - ERROR: [full error message with stack trace]
- ⚠️ Button: "[Button Name]" - Warning: [platform error message]

---

**Success criteria:**
- At least ONE primary action button clicked per page
- Console checked for errors after EACH click
- No app-specific errors found (platform errors are OK)
- Results documented for validation report

**Failure criteria:**
- Primary action button not tested
- App errors found after button click
- Errors not checked after interaction

**On failure:** Report:
- Page name and route
- Button that was clicked
- Full error message from console
- Stack trace showing source file
- Mark validation as FAILED for that page

#### 5.5 Capture Accessibility Snapshot

```
Tool: playwright__browser-snapshot
Args: {}
```

**Validate:**
- Expected UI elements are present
- Page structure is correct
- No broken or missing components

#### 5.6 Take Screenshot (Optional)

```
Tool: playwright__browser-take-screenshot
Args: { "fullPage": true }
```

Capture visual evidence of the rendered page state.

#### 5.7 Execute Custom Validations (If Needed)

```
Tool: playwright__browser-evaluate
Args: { "function": "() => { /* validation code */ }" }
```

Use for custom runtime checks like:
- Verifying specific DOM elements exist
- Checking application state
- Validating data loading

## Validation Report

After completing all steps, provide a summary:

**Pass:**
- TypeScript: ✓ No compilation errors
- Dependencies: ✓ All packages installed successfully
- Build: ✓ Compiled successfully
- Preview: ✓ Running at [URL]
- E2E: ✓ All previews tested successfully
  - Site Preview: ✓ No runtime errors, UI renders correctly, all API calls successful, interactions work correctly
  - Dashboard Extensions:
    - [Extension 1]: ✓ No runtime errors, UI renders correctly, all API calls successful, interactions work correctly
    - [Extension 2]: ✓ No runtime errors, UI renders correctly, all API calls successful, interactions work correctly
    - [Extension N]: ✓ No runtime errors, UI renders correctly, all API calls successful, interactions work correctly

**Fail:**
- Identify which step failed
- Identify which preview/extension(s) failed (if applicable)
- Provide specific error messages
- Suggest remediation steps

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| TypeScript compilation fails | Type mismatches, missing declarations, or incorrect types | Fix TypeScript errors shown in `npx tsc --noEmit` output |
| Package installation fails | Missing lock file, network issues, or corrupted node_modules | Delete `node_modules` and lock file, then reinstall |
| Build fails with TS errors | Type mismatches | Fix TypeScript errors in source |
| Preview fails to start | Port conflict or config issue | Check `wix.config.json` |
| Console errors in preview | Runtime exceptions | Check browser console output |
| Backend API 500 errors | Server-side errors in API routes | Check API route handlers, server logs, and error handling |
| UI not rendering | Component errors | Review component code and imports |
| Button click fails | Missing onClick handler, disabled state, or element not found | Verify button has proper event handlers and is interactive |
| Form submission errors | Validation failures, missing required fields, or API errors | Check form validation logic and API endpoint handling |
| Navigation not working | Broken links, missing routes, or state management issues | Verify route configuration and navigation handlers |
