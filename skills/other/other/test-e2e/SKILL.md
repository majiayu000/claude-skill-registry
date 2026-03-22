---
name: test-e2e
description: "Executes E2E tests from definition files with Playwright browser automation. Triggers on keywords: test e2e, run e2e, execute e2e test, e2e test runner"
project-agnostic: true
allowed-tools:
  - Read
  - Bash
  - Glob
---

# E2E Test Runner

Execute E2E test steps from a test definition file.

**Test File:** $1
**Base URL:** $2 (default: `http://localhost:${DEFAULT_PORT:-5173}/`)

## Pre-Flight Checks

1. **Verify Test File Exists**
   - Read test file from `$1`
   - If not found: STOP with "Test file not found: $1"

2. **Verify playwright-cli Installed**
   - Run: `playwright-cli --help`
   - If not available: STOP with "playwright-cli not installed. Run: npm install -g @playwright/cli@latest"

3. **Parse Test Definition**
   - Extract: Test Name, User Story, Test Steps, Success Criteria
   - If parsing fails: STOP with parse error details

## Execution

1. **Initialize Test Session**
   - Record test start timestamp
   - Create screenshot directory: `{PROJECT_ROOT}/outputs/e2e/<test-name>/`

2. **Navigate to Base URL**
   - Run: `playwright-cli open <base_url>`
   - Run: `playwright-cli screenshot --output {PROJECT_ROOT}/outputs/e2e/<test-name>/01_initial.png`

3. **Execute Test Steps**
   - For each step in Test Steps section:
     a. Parse step action (Navigate, Verify, Click, Fill, Type, Screenshot)
     b. Execute action using appropriate playwright-cli command:
        - Navigate: `playwright-cli goto <url>`; Verify: `playwright-cli snapshot`; Click: `playwright-cli click "<selector>"`; Fill: `playwright-cli fill "<selector>" "<text>"`; Screenshot: `playwright-cli screenshot --output <path>`
     c. If step includes "screenshot": capture and save
     d. If step includes "verify": validate condition
     e. On failure: record error and continue to capture state

4. **Validate Success Criteria**
   - Check each criterion from Success Criteria section
   - Mark as passed/failed

5. **Generate Result JSON**
   - Output structured result to stdout

## Output Format

Return JSON result:
```json
{
  "test_name": "<name from test file>",
  "status": "passed|failed",
  "timestamp": "<ISO timestamp>",
  "duration_ms": <number>,
  "steps": [
    {"step": 1, "action": "navigate", "status": "passed"},
    {"step": 2, "action": "verify", "status": "passed"}
  ],
  "screenshots": [
    "{PROJECT_ROOT}/outputs/e2e/<test-name>/01_initial.png"
  ],
  "video": "{PROJECT_ROOT}/outputs/e2e/<timestamp>-<test-name>.webm",
  "error": null
}
```

## Error Handling

- On step failure: capture screenshot, continue remaining steps
- On critical failure (browser crash): return partial result with error
- Always close browser session on completion

## CLI Commands Used

- `playwright-cli open <url>` / `goto <url>` - Navigate to URLs
- `playwright-cli snapshot` - Get page accessibility tree
- `playwright-cli click "<selector>"` - Click elements
- `playwright-cli fill "<selector>" "<text>"` - Type into inputs
- `playwright-cli screenshot --output <path>` - Capture PNG screenshots
- `playwright-cli close` - End session
