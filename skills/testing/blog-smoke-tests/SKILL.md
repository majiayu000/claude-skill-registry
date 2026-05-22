---
name: blog-smoke-tests
description: Run Playwright smoke tests for Denser blog application. Executes 15 tests (SMOKE-01 to SMOKE-15) against configurable environment (production, dev, or localhost) with retry support (max 3 attempts per failing test). Supports headed (visible browser) and headless modes. Collects artifacts (screenshots, trace.zip) on failures and generates HTML report. Use when testing blog functionality, verifying deployments, checking UI/API consistency, or when user requests smoke tests, playwright tests, or blog testing.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Blog Smoke Tests Skill

Run Playwright smoke tests against the Denser blog application.

## Features

- **15 smoke tests** organized by priority (P0-P4)
- **Retry logic** - max 3 attempts per failing test
- **Headed/headless modes** - choose visible or background execution
- **Artifact collection** - screenshots and trace.zip on failures
- **HTML report** - comprehensive test results report
- **Tracing** - Playwright traces for debugging failures

## Workflow

### Step 1: Ask User Preferences

Before running tests, ask user:

1. **Target environment**:
   - **Production** (default) - https://blog.openhive.network
   - **Dev** - https://blog.dev.openhive.network
   - **Localhost** - http://localhost:3000

2. **Browser mode**:
   - **Headed** (default) - visible browser, good for debugging
   - **Headless** - faster, for CI/CD

3. **Test scope**:
   - **All** - run all 15 tests
   - **P0** - critical tests only (SMOKE-01, 04, 08)
   - **P1** - important tests (SMOKE-05, 06, 07)
   - **P2** - tooltip tests (SMOKE-02, 03, 09)
   - **P3** - navigation tests (SMOKE-10, 11, 12)
   - **P4** - additional tests (SMOKE-13, 14, 15)

### Step 2: Prepare Directories

```bash
# Create temp and report directories
mkdir -p /storage1/denser/apps/blog/playwright/temp_ai_script_tests
mkdir -p /storage1/denser/apps/blog/playwright/temp_ai_report_tests

# Copy test scripts
cp /storage1/denser/.claude/skills/blog-smoke-tests/scripts/smoke-*.mjs /storage1/denser/apps/blog/playwright/temp_ai_script_tests/
```

### Step 3: Run Tests with Retry Logic

For each test:
1. Run test script with `REPORT_DIR` set
2. If FAIL, retry up to 2 more times (max 3 attempts total)
3. Wait 2 seconds between retries
4. Collect JSON result from output (line starting with `__RESULT__`)
5. On failure: artifacts saved automatically (screenshot + trace.zip)

**Command to run single test:**
```bash
cd /storage1/denser/apps/blog
BASE_URL=https://blog.openhive.network HEADLESS=false REPORT_DIR=./playwright/temp_ai_report_tests pnpm exec node playwright/temp_ai_script_tests/smoke-XX-name.mjs
```

Replace:
- `BASE_URL=https://blog.openhive.network` with chosen environment URL
- `HEADLESS=false` with `HEADLESS=true` for headless mode

**Parsing JSON result:**
Each test outputs a JSON line prefixed with `__RESULT__`:
```
__RESULT__{"id":"SMOKE-01","name":"Homepage Posts","priority":"P0","passed":true,"error":null,"artifacts":[]}
```

### Step 4: Generate HTML Report

After running all tests, collect results and generate HTML report:

```bash
# Option 1: Using generate-report.mjs script
cd /storage1/denser/apps/blog
pnpm exec node /storage1/denser/.claude/skills/blog-smoke-tests/scripts/generate-report.mjs '[results-json-array]'
```

Alternatively, create report manually based on collected results.

**Report location:** `./playwright/temp_ai_report_tests/report.html`

### Step 5: Cleanup

After all tests complete:
```bash
rm -f /storage1/denser/apps/blog/playwright/temp_ai_script_tests/smoke-*.mjs
```

Keep report directory with:
- `report.html` - HTML test report
- `SMOKE-XX-failure.png` - screenshots of failures
- `SMOKE-XX-trace.zip` - Playwright traces for failures

### Step 6: Summary

Present results:

```
========================================
SMOKE TEST SUMMARY: X/Y PASSED
========================================
✓ [P0] SMOKE-01: Homepage Posts
✓ [P0] SMOKE-04: Post Navigation
✓ [P0] SMOKE-08: User Profile
✓ [P1] SMOKE-05: Votes API
...
✗ [P3] SMOKE-11: Categories (3 attempts)
...
========================================

HTML Report: ./playwright/temp_ai_report_tests/report.html
Artifacts: ./playwright/temp_ai_report_tests/

To view traces: npx playwright show-trace ./playwright/temp_ai_report_tests/SMOKE-XX-trace.zip
```

## Artifacts on Failure

When a test fails, the following artifacts are saved:

| Artifact | Description | Location |
|----------|-------------|----------|
| Screenshot | Full page screenshot at failure | `SMOKE-XX-failure.png` |
| Trace | Playwright trace with snapshots | `SMOKE-XX-trace.zip` |

**Viewing Traces:**
```bash
cd /storage1/denser/apps/blog
npx playwright show-trace ./playwright/temp_ai_report_tests/SMOKE-04-trace.zip
```

## Test Catalog

| Priority | ID | Name | Script |
|----------|-----|------|--------|
| P0 | SMOKE-01 | Homepage Posts | smoke-01-homepage-posts.mjs |
| P0 | SMOKE-04 | Post Navigation | smoke-04-post-navigation.mjs |
| P0 | SMOKE-08 | User Profile | smoke-08-profile.mjs |
| P1 | SMOKE-05 | Votes API | smoke-05-votes-api.mjs |
| P1 | SMOKE-06 | Comments | smoke-06-comments.mjs |
| P1 | SMOKE-07 | Payout | smoke-07-payout.mjs |
| P2 | SMOKE-02 | Votes Tooltip | smoke-02-votes-tooltip.mjs |
| P2 | SMOKE-03 | Payout Tooltip | smoke-03-payout-tooltip.mjs |
| P2 | SMOKE-09 | Followers | smoke-09-followers.mjs |
| P3 | SMOKE-10 | Tags | smoke-10-tags.mjs |
| P3 | SMOKE-11 | Categories | smoke-11-categories.mjs |
| P3 | SMOKE-12 | Communities | smoke-12-communities.mjs |
| P4 | SMOKE-13 | Static Pages | smoke-13-static-pages.mjs |
| P4 | SMOKE-14 | Theme Toggle | smoke-14-theme.mjs |
| P4 | SMOKE-15 | Login Button | smoke-15-login.mjs |

## Retry Logic Pattern

```javascript
const MAX_RETRIES = 3;
const results = [];

for (const test of tests) {
  let passed = false;
  let attempts = 0;
  let lastError = null;
  let artifacts = [];

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    attempts = attempt;
    const output = await runTest(test);

    // Parse __RESULT__ from output
    const resultLine = output.match(/__RESULT__(.+)/);
    if (resultLine) {
      const result = JSON.parse(resultLine[1]);
      passed = result.passed;
      lastError = result.error;
      artifacts = result.artifacts;
    }

    if (passed) break;

    if (attempt < MAX_RETRIES) {
      console.log(`Retry ${attempt + 1}/${MAX_RETRIES} in 2 seconds...`);
      await sleep(2000);
    }
  }

  results.push({
    id: test.id,
    name: test.name,
    priority: test.priority,
    passed,
    attempts,
    error: lastError,
    artifacts
  });
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Target environment URL | `https://blog.openhive.network` |
| `HEADLESS` | Run browser in headless mode | `false` (headed) |
| `REPORT_DIR` | Directory for artifacts and report | `./playwright/temp_ai_report_tests` |

### Available Environments

| Environment | URL |
|-------------|-----|
| Production | `https://blog.openhive.network` |
| Dev | `https://blog.dev.openhive.network` |
| Localhost | `http://localhost:3000` |

## Reference Documentation

- **Test patterns and selectors**: See [references/test-selectors.md](references/test-selectors.md)
- **Full documentation**: `/storage1/denser/docs/playwright-testing-notes.md`
- **Blog architecture**: `/storage1/denser/docs/denser-blog-architecture.md`

## Directories

| Path | Purpose |
|------|---------|
| Production URL | https://blog.openhive.network |
| Dev URL | https://blog.dev.openhive.network |
| Localhost URL | http://localhost:3000 |
| API URL | https://api.hive.blog |
| Working directory | /storage1/denser/apps/blog |
| Temp scripts | playwright/temp_ai_script_tests/ |
| Reports & artifacts | playwright/temp_ai_report_tests/ |
| Skill scripts | /storage1/denser/.claude/skills/blog-smoke-tests/scripts/ |
