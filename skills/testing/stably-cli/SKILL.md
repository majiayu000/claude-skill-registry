---
name: stably-cli
description: |
  Expert assistant for the Stably CLI tool. Use this skill when working with
  stably commands for creating, running, and fixing Playwright tests using AI.
  Triggers on tasks like "create tests with stably", "fix failing tests",
  "run stably test", or "use stably cli".
license: MIT
metadata:
  author: stably
  version: '1.0.0'
---

# Stably CLI Assistant

You are an expert assistant for the Stably CLI, a command-line tool that enables developers to create, run, and maintain Playwright tests through AI assistance. Your goal is to help users effectively use the Stably CLI for test automation.

## Overview

The Stably CLI provides both interactive and automated workflows for test management:

- **Interactive Mode**: Conversational AI agent for creating and debugging tests
- **Automated Mode**: Headless commands for CI/CD integration

## Prerequisites

Before using Stably CLI, ensure the user has:

1. **Node.js 20+** and npm installed
2. **Playwright** configured in their project
3. A **Stably account** (https://app.stably.ai) or API key

## Installation

The Stably CLI can be installed globally or used via npx:

```bash
# Global installation
npm install -g stably

# Or use without installation
npx stably
```

Verify installation:
```bash
stably --version
```

---

## Core Commands Reference

### Authentication Commands

#### `stably login`
Browser-based authentication for the CLI.

```bash
stably login
```

Opens a browser for authentication. Credentials are stored locally for future use.

#### `stably logout`
Clear stored credentials.

```bash
stably logout
```

#### `stably whoami`
Display current authentication status.

```bash
stably whoami
```

Shows the currently logged-in user and organization.

---

### Project Setup

#### `stably init`
Initialize Playwright and Stably SDK in a project. This handles login automatically if needed.

```bash
stably init
```

This command will:
- Set up Playwright if not already installed
- Configure the Stably SDK
- Set up necessary configuration files

---

### Interactive Agent

#### `stably`
Launch the interactive agent for conversational test work.

```bash
stably
```

The interactive agent allows you to:
- Describe desired tests and receive generated Playwright code
- Paste error output for AI-powered debugging and fixes
- Query test suite coverage and structure
- Receive guidance on testing best practices

**Example session:**
```
$ stably
> Create a test that logs into my app and verifies the dashboard loads

[Agent generates test code and explains it]

> The login button selector is failing, here's the error: [paste error]

[Agent diagnoses and fixes the selector]
```

---

### Test Creation

#### `stably create <prompt>`
Create tests with AI in headless mode (for automation).

```bash
stably create "test user login flow with email and password"
```

**Options:**
- `--output <dir>` - Specify output directory for generated tests

**Auto-detection:**
The command automatically detects output location by:
1. Checking `playwright.config.ts` for `testDir` setting
2. Searching for `tests/`, `e2e/`, `__tests__/`, or `test/` directories

**Examples:**

```bash
# Basic test creation
stably create "test the checkout flow"

# Specify output directory
stably create "test user registration" --output ./e2e

# Create multiple related tests
stably create "test all CRUD operations on the users API"
```

**Best practices for prompts:**
- Be specific about user flows and expected outcomes
- Mention specific UI elements if known
- Include authentication requirements if needed
- Describe error states to test

---

### Test Execution

#### `stably test`
Execute Playwright tests with the integrated Stably reporter.

```bash
stably test
```

This is the recommended method for running tests as it automatically configures the Stably reporter.

**All standard Playwright CLI options are supported:**

```bash
# Run in headed mode
stably test --headed

# Run specific project
stably test --project=chromium

# Control parallelism
stably test --workers=4

# Run with retries
stably test --retries=2

# Filter tests by name
stably test --grep="login"

# Run specific test file
stably test tests/login.spec.ts
```

**Alternative method:**
You can also run tests directly with Playwright if the reporter is configured in `playwright.config.ts`:

```bash
npx playwright test
```

---

### Test Repair

#### `stably fix [runId]`
Diagnose failures and apply AI fixes automatically.

```bash
# In local environment (requires run ID)
stably fix abc123

# In CI environment (auto-detects run ID)
stably fix
```

The fix command:
- Analyzes test failures using captured context (screenshots, logs, DOM traces)
- Applies AI-generated corrections automatically
- Exits after applying fixes, enabling pipeline chaining

**Common fixes applied:**
- Selector changes (when UI elements move or rename)
- Assertion mismatches
- Timing issues and race conditions
- API response changes

**Typical workflow:**
```bash
# Run tests
stably test

# If failures occur, get the run ID from output
# Then fix the failing tests
stably fix run_abc123
```

---

### Browser Management

#### `stably install`
Install browser dependencies required by Playwright.

```bash
stably install
```

This is equivalent to `npx playwright install` but integrated into the Stably workflow.

---

## Configuration

### Environment Variables

Tests require these environment variables:

```bash
STABLY_API_KEY=your_api_key_here
STABLY_PROJECT_ID=your_project_id_here
```

**Getting credentials:**
1. Go to https://auth.stably.ai/org/api_keys/
2. Create or copy your API key
3. Get your project ID from the dashboard

**Setting up .env file:**
```bash
# .env
STABLY_API_KEY=sk_live_xxxxx
STABLY_PROJECT_ID=proj_xxxxx
```

### Playwright Configuration

For full debugging context, enable tracing in `playwright.config.ts`:

```typescript
import { defineConfig } from '@playwright/test';
import { stablyReporter } from '@stablyai/playwright-test';

export default defineConfig({
  use: {
    trace: 'on', // Required for stably fix to work properly
  },
  reporter: [
    ['list'],
    stablyReporter({
      apiKey: process.env.STABLY_API_KEY,
      projectId: process.env.STABLY_PROJECT_ID,
    }),
  ],
});
```

---

## CI/CD Integration

### GitHub Actions Example

Self-healing pipeline that automatically detects failures, applies fixes, and commits corrections:

```yaml
name: E2E Tests with Auto-Fix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run tests
        run: npx stably test
        env:
          STABLY_API_KEY: ${{ secrets.STABLY_API_KEY }}
          STABLY_PROJECT_ID: ${{ secrets.STABLY_PROJECT_ID }}
        continue-on-error: true
        id: test

      - name: Auto-fix failing tests
        if: steps.test.outcome == 'failure'
        run: npx stably fix
        env:
          STABLY_API_KEY: ${{ secrets.STABLY_API_KEY }}
          STABLY_PROJECT_ID: ${{ secrets.STABLY_PROJECT_ID }}

      - name: Commit fixes
        if: steps.test.outcome == 'failure'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --staged --quiet || git commit -m "fix: auto-repair failing tests"
          git push
```

### Auto-generating Tests in PRs

```yaml
name: Generate Tests for New Features

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Generate tests for changes
        run: |
          npx stably create "test the new features in this PR"
        env:
          STABLY_API_KEY: ${{ secrets.STABLY_API_KEY }}
          STABLY_PROJECT_ID: ${{ secrets.STABLY_PROJECT_ID }}

      - name: Commit generated tests
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --staged --quiet || git commit -m "test: add auto-generated tests"
          git push
```

---

## Common Workflows

### New Project Setup

```bash
# 1. Initialize project with Stably
stably init

# 2. Create initial tests
stably create "test the main user flows"

# 3. Run tests to verify
stably test
```

### Daily Development

```bash
# Start interactive session for creating/debugging tests
stably

# Or create specific tests
stably create "test the new feature I just built"

# Run all tests
stably test

# Fix any failures
stably fix <runId>
```

### Debugging Failing Tests

```bash
# 1. Run tests and note the run ID
stably test

# 2. If tests fail, use fix command with the run ID
stably fix run_abc123

# 3. Or start interactive session for manual debugging
stably
> Here's the error I'm seeing: [paste error]
```

---

## Troubleshooting

### Authentication Issues

**Problem:** "Not authenticated" error
```bash
# Solution: Re-authenticate
stably login
```

**Problem:** API key not recognized
```bash
# Verify your credentials
stably whoami

# Check environment variables are set
echo $STABLY_API_KEY
```

### Test Creation Issues

**Problem:** Tests generated in wrong directory
```bash
# Solution: Specify output directory explicitly
stably create "test login" --output ./tests/e2e
```

**Problem:** Generated tests don't match project patterns
```bash
# Solution: Use interactive mode for more control
stably
> Generate a test for login following the patterns in my existing tests
```

### Test Execution Issues

**Problem:** Tests fail with missing browser
```bash
# Solution: Install browsers
stably install
# Or
npx playwright install
```

**Problem:** Traces not uploading
```bash
# Solution: Enable tracing in playwright.config.ts
# Set: trace: 'on' in the use section
```

### Fix Command Issues

**Problem:** "Run ID not found" error
```bash
# Solution: Get run ID from test output
stably test
# Look for "Run ID: xxx" in output
stably fix xxx
```

**Problem:** Fix command not finding issues
```bash
# Solution: Ensure tracing is enabled
# Check playwright.config.ts has trace: 'on'
```

---

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `stably` | Launch interactive agent |
| `stably init` | Initialize project with Stably |
| `stably create <prompt>` | Create tests headlessly |
| `stably test` | Run tests with Stably reporter |
| `stably fix [runId]` | Auto-fix failing tests |
| `stably login` | Authenticate via browser |
| `stably logout` | Clear credentials |
| `stably whoami` | Show auth status |
| `stably install` | Install browser dependencies |
| `stably --version` | Show CLI version |

---

## Best Practices

1. **Use interactive mode for exploration** - Start with `stably` to understand your app before creating automated tests

2. **Be specific in prompts** - The more detail you provide to `stably create`, the better the generated tests

3. **Enable tracing** - Always set `trace: 'on'` in your Playwright config for best fix command results

4. **Commit generated tests** - Review and commit AI-generated tests to version control

5. **Run tests frequently** - Use `stably test` as part of your development workflow

6. **Fix tests promptly** - Address failing tests with `stably fix` before they accumulate

---

## Links

- [Stably Documentation](https://docs.stably.ai)
- [CLI Quickstart](https://docs.stably.ai/stably2/cli-quickstart)
- [Stably Dashboard](https://app.stably.ai)
- [Get API Key](https://auth.stably.ai/org/api_keys/)
