---
name: preview-testing
description: Comprehensive E2E + Security Tests for Vercel Preview Deployments. Combines Playwright automation with Claude-in-Chrome MCP for interactive debugging. Activate on PR creation, before merge, or manual /preview-test.
---

# Preview Testing

> Comprehensive E2E + Security Tests for Vercel Preview Deployments

## Trigger

This skill activates on:

- `/preview-test` - Manual invocation
- After PR creation against `main` or `develop`
- Before merge for production approval

## Features

| Feature            | Duration | Description                                     |
| ------------------ | -------- | ----------------------------------------------- |
| Smoke Tests        | <2min    | Critical user flows (Login, Upload, Analysis)   |
| Visual Regression  | <3min    | Screenshot comparison with 1% tolerance         |
| Security Tests     | <5min    | OWASP LLM01, Quota Bypass, Stripe Webhook       |
| DSGVO Region Check | <30s     | Verifies Frankfurt (fra1) region                |
| npm audit          | <1min    | Dependency vulnerability scan                   |

## Usage

```bash
# Standard: Smoke + Visual + Security
/preview-test

# Security tests only
/preview-test --security

# With AI Exploratory Testing (optional)
/preview-test --ai
```

## Security Tests (OWASP LLM Top 10 2025)

### Prompt Injection (LLM01) - CRITICAL

- Direct Injection (Jailbreaks, DAN, Role Manipulation)
- System Prompt Extraction Prevention
- Context Hijacking via Fake History
- Indirect Injection via File Upload
- Multi-Language Bypass Attempts

**File:** `tests/security/prompt-injection.spec.ts`

### Quota Bypass - CRITICAL (Cost Risk)

- API Authentication Bypass
- Email Spoofing Prevention
- Demo Mode Abuse
- Race Condition in Quota Check
- Test User Email Discovery

**File:** `tests/security/quota-bypass.spec.ts`

### Stripe Webhook Security (PCI-DSS)

- Signature Validation
- Replay Attack Prevention
- Payload Manipulation Detection
- Subscription Fraud Prevention

**File:** `tests/security/stripe-webhook.spec.ts`

## Workflow

```
1. PRE-DEPLOY GATES (quality-gate.yml)
   └── TypeScript Check
   └── Unit Tests
   └── Build Validation

2. PREVIEW DEPLOYMENT
   └── Generate Vercel Preview URL
   └── Wait 30s warmup

3. SMOKE TESTS (Playwright, <2min)
   └── Homepage loads
   └── Login flow works
   └── Critical Path: Upload → Analysis

4. VISUAL REGRESSION (Playwright, <3min)
   └── Screenshot comparison with baseline
   └── Mobile + Desktop breakpoints

5. SECURITY TESTS (Playwright, <5min) [CRITICAL]
   └── Quota Bypass Tests
   └── Prompt Injection Tests
   └── Stripe Webhook Security

6. GDPR REGION CHECK
   └── Verifies fra1 (Frankfurt) region

7. APPROVAL GATE
   └── All tests green → PR comment "Ready to merge"
   └── Security failures → BLOCK MERGE
```

## Claude-in-Chrome MCP Integration

In addition to automated Playwright tests, interactive browser tools are available via MCP. These are ideal for:

- **Visual debugging** during development
- **Ad-hoc testing** without test scripts
- **GIF recordings** for PR documentation
- **Live console/network inspection**

### When to Use Which Tool?

| Situation                   | Tool                                     | Reason                              |
| --------------------------- | ---------------------------------------- | ----------------------------------- |
| Automated CI/CD tests       | Playwright `npm run test:e2e`            | Fast, headless, reproducible        |
| Visual inspection           | Claude-in-Chrome `read_page`             | Accessibility tree, structured      |
| Screenshot for PR           | Claude-in-Chrome `computer`              | Saves locally, real Chrome          |
| Document user flow          | Claude-in-Chrome `gif_creator`           | Animated GIF                        |
| Debug console errors        | Claude-in-Chrome `read_console_messages` | Live JS errors                      |
| Inspect API calls           | Claude-in-Chrome `read_network_requests` | XHR/Fetch debugging                 |

### Interactive Preview Testing (Claude-in-Chrome)

```typescript
// 1. Initialize browser tab context
mcp__claude-in-chrome__tabs_context_mcp({ createIfEmpty: true })

// 2. Create new tab for preview
mcp__claude-in-chrome__tabs_create_mcp()

// 3. Navigate to preview URL
mcp__claude-in-chrome__navigate({
  url: "https://your-app-xyz.vercel.app",
  tabId: <id>
})

// 4. Accessibility snapshot (better than screenshot for structure)
mcp__claude-in-chrome__read_page({ tabId: <id> })

// 5. Find interactive elements
mcp__claude-in-chrome__find({
  query: "login button",
  tabId: <id>
})

// 6. Click element
mcp__claude-in-chrome__computer({
  action: "left_click",
  ref: "ref_123",  // from find result
  tabId: <id>
})

// 7. Save screenshot
mcp__claude-in-chrome__computer({
  action: "screenshot",
  tabId: <id>
})
```

### GIF Recording for PR Documentation

```typescript
// 1. Start recording
mcp__claude-in-chrome__gif_creator({
  action: "start_recording",
  tabId: <id>
})

// 2. Screenshot for first frame
mcp__claude-in-chrome__computer({ action: "screenshot", tabId: <id> })

// 3. Perform user flow (login, upload, etc.)
mcp__claude-in-chrome__computer({
  action: "left_click",
  coordinate: [x, y],
  tabId: <id>
})

// 4. Wait for page transition
mcp__claude-in-chrome__browser_wait_for({
  text: "Welcome",
  tabId: <id>
})

// 5. Screenshot for last frame
mcp__claude-in-chrome__computer({ action: "screenshot", tabId: <id> })

// 6. Stop recording
mcp__claude-in-chrome__gif_creator({
  action: "stop_recording",
  tabId: <id>
})

// 7. Export GIF
mcp__claude-in-chrome__gif_creator({
  action: "export",
  tabId: <id>,
  filename: "login-flow-preview.gif",
  download: true,
  options: { quality: 15 }  // 1-30, lower = smaller file
})
```

### Debugging: Console & Network

```typescript
// Check JavaScript errors in console
mcp__claude-in-chrome__read_console_messages({
  tabId: <id>,
  onlyErrors: true,
  pattern: "error|exception"
})

// Inspect API requests
mcp__claude-in-chrome__read_network_requests({
  tabId: <id>,
  urlPattern: "/api/"  // Backend calls only
})
```

### Example: Complete Interactive Preview Test

```
User: "Test the preview https://your-app-abc123.vercel.app"

Claude executes:
1. tabs_context_mcp → Get tab IDs
2. tabs_create_mcp → Create new tab
3. navigate → Open preview URL
4. read_page → Check accessibility snapshot
5. find → Search for "login button"
6. computer(screenshot) → Baseline screenshot
7. computer(left_click) → Click login button
8. read_console_messages → Check for JS errors
9. Report: "Landing page correct, no console errors"
```

## Local Execution

```bash
# All preview tests (against local dev server)
npm run test:e2e

# Security tests only
npx playwright test tests/security/ --project=chromium

# Against Vercel Preview URL
BASE_URL=https://preview-xxx.vercel.app npx playwright test tests/security/
```

## CI/CD Integration

The workflow is defined in `.github/workflows/preview-test.yml` and runs automatically on PRs against `main` or `develop`.

### PR Comment (automatic)

After each run, a comment with test results is created:

```markdown
## Preview Deployment Test Results

| Test Suite             | Status     |
| ---------------------- | ---------- |
| Smoke Tests            | ✅ success |
| Visual Regression      | ✅ success |
| Security Tests (OWASP) | ✅ success |
| GDPR Region (fra1)     | ✅ success |
| npm audit              | ⚠️ failure |
```

### Blocking Logic

- **Smoke Tests**: Must pass
- **Security Tests**: Must pass (CRITICAL)
- **Visual Regression**: Warning on failure, doesn't block
- **npm audit**: Warning on failure, doesn't block

## GDPR Compliance

- **EU Data Residency**: All tests verify Frankfurt (fra1) region
- **No Real User Data**: Synthetic test data (faker.js)
- **Screenshots in EU**: Playwright reports stored in GitHub Actions (EU region)
- **Audit Trail**: 30-day retention for security test reports

## Expected Output

After running `/preview-test`:

```
Preview Testing Complete

RESULTS:
✅ Smoke Tests: 8/8 passed
✅ Visual Regression: 0 diffs
✅ Security Tests: 45/45 passed
  - Prompt Injection: 15 tests
  - Quota Bypass: 18 tests
  - Stripe Webhook: 12 tests
✅ GDPR Region: fra1 verified
⚠️ npm audit: 2 moderate vulnerabilities

RECOMMENDATION: Ready to merge to main
```

## Troubleshooting

### Security Tests Are Skipped

Tests use `test.skip(!isVercelDeployment, ...)` and only run against production-like Vercel Preview. Locally they're skipped because some tests (e.g., rate limiting) require a real serverless environment.

**Solution:**
```bash
# Test against Vercel Preview
BASE_URL=https://your-preview-url.vercel.app npx playwright test tests/security/
```

### Visual Regression Baseline Missing

On first run, baseline screenshots are created. Changes are marked as diffs.

**Solution:**
```bash
# Update baseline
npx playwright test tests/e2e/visual-regression.spec.ts --update-snapshots
```

## Sources

- [OWASP LLM Top 10 2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Stripe Webhook Security](https://stripe.com/docs/webhooks/signatures)
- [Vercel Preview URL Polling](https://github.com/marketplace/actions/vercel-preview-url-with-status-polling)
