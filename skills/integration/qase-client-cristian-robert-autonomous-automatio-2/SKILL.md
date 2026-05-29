---
name: qase-client
description: Qase.io test management integration for creating suites, test cases, and reporting results. Use when syncing test cases to Qase, creating test suites, reporting automation results, or managing test documentation in Qase. Triggers on "Qase", "test management", "create suite", "create test case", "sync to Qase", "report results".
---

# Qase.io Client

Integrate with Qase.io to manage test suites, cases, and report automation results.

## Setup Requirements

```bash
# Required environment variables
QASE_API_TOKEN=your_api_token_here
QASE_PROJECT_CODE=PROJ  # Your project code in Qase
```

Get your API token: Qase → User Settings → API Tokens → Create

## Usage

The `qase_client.py` script provides all Qase operations:

```bash
# List projects
python scripts/qase_client.py projects

# List suites in a project
python scripts/qase_client.py suites PROJ

# List cases in a project
python scripts/qase_client.py cases PROJ

# Search for existing cases by keyword (ALWAYS DO THIS FIRST!)
python scripts/qase_client.py search-cases PROJ "login"
python scripts/qase_client.py search-cases PROJ "checkout"

# Get full details of a specific case
python scripts/qase_client.py get-case PROJ 42

# Create a suite
python scripts/qase_client.py create-suite PROJ '{"title": "Authentication Tests", "description": "Login and registration tests"}'

# Create a test case
python scripts/qase_client.py create-case PROJ '{"title": "Valid login redirects to dashboard", "suite_id": 1, "severity": 2, "priority": 1}'

# Create a test run
python scripts/qase_client.py create-run PROJ '{"title": "Smoke Test Run"}'

# Report a result
python scripts/qase_client.py report-result PROJ 1 '{"case_id": 1, "status": "passed", "time_ms": 1500}'
```

## MANDATORY: Check for Existing Cases First

**Before creating any test cases, ALWAYS search Qase for existing cases:**

```bash
# Search for cases related to your feature
python scripts/qase_client.py search-cases PROJ "feature_keyword"

# If cases exist, get their full details
python scripts/qase_client.py get-case PROJ <case_id>
```

This prevents duplicate test cases and ensures you build on existing test documentation.

### Decision Flow

```
1. SEARCH for existing cases matching your feature
2. IF cases exist:
   - Review existing coverage
   - Identify gaps
   - Only create NEW cases for uncovered scenarios
3. IF no cases exist:
   - Create new suite (if needed)
   - Create new cases
4. Record all case IDs (existing + new) for automation
```

## Workflow Integration

### Before Creating Test Cases (MANDATORY)
```
1. Search for existing cases: search-cases PROJ "feature"
2. List existing suites: suites PROJ
3. Review what's already documented
4. Only create what's missing
```

### After Test Design
```
1. Create suites for each feature area (if not exists)
2. Create cases within each suite (only new ones)
3. Record Qase case IDs for automation mapping
```

### After Test Execution
```
1. Create a test run
2. Report results for each case
3. Complete the run
```

## Test Case Structure

```json
{
  "title": "Valid login should redirect to dashboard",
  "suite_id": 1,
  "severity": 2,
  "priority": 1,
  "preconditions": "User exists in system",
  "steps": [
    {
      "action": "Navigate to /login",
      "expected_result": "Login form is visible"
    },
    {
      "action": "Enter valid email and password",
      "expected_result": "Fields are populated"
    },
    {
      "action": "Click Sign In button",
      "expected_result": "User is redirected to /dashboard"
    }
  ]
}
```

## Severity & Priority Mapping

| Our Priority | Qase Severity | Qase Priority |
|--------------|---------------|---------------|
| P0 | 1 (blocker) | 1 (high) |
| P1 | 2 (critical) | 2 (medium) |
| P2 | 3 (major) | 3 (low) |

## Playwright Integration

### Install Reporter

```bash
npm install playwright-qase-reporter dotenv --save-dev
```

### Environment Setup

Create `.env` file (copy from `.env.example`):

```bash
QASE_TESTOPS_API_TOKEN=your_api_token_here
QASE_TESTOPS_PROJECT=ATP
QASE_MODE=testops
```

### Playwright Config

Add to `playwright.config.ts`:

```typescript
import dotenv from 'dotenv';
import path from 'path';
dotenv.config({ path: path.resolve(__dirname, '.env') });

export default defineConfig({
  reporter: [
    ['list'],
    ['playwright-qase-reporter', {
      mode: process.env.QASE_MODE || 'off',
      testops: {
        api: { token: process.env.QASE_TESTOPS_API_TOKEN },
        project: process.env.QASE_TESTOPS_PROJECT || 'ATP',
        uploadAttachments: true,
        run: { complete: true, title: 'Playwright Test Run' },
      },
    }],
  ],
});
```

### Link Tests to Qase Cases

```typescript
import { test, expect } from '@playwright/test';
import { qase } from 'playwright-qase-reporter';

// qase(CASE_ID, 'test title')
test(qase(1, 'Page loads successfully'), async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/App/);
});
```

### Run Tests

```bash
# With Qase reporting
npx playwright test

# Without Qase (local only)
QASE_MODE=off npx playwright test
```

## References

- **API documentation**: See [references/qase-api.md](references/qase-api.md)
- **Config example**: See [references/qase-config.example.json](references/qase-config.example.json)
