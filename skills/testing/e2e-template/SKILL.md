---
name: e2e-template
description: "Template generator for E2E test definitions. Creates structured test files for use with test-e2e skill. Triggers on keywords: e2e template, test template, create test definition"
project-agnostic: true
allowed-tools:
  - Read
  - Write
---

# E2E Test: <Test Name>

<!--
Template for E2E test definitions.
Copy this file and fill in the sections below.
Usage: /test-e2e <path-to-your-test>.md
-->

## User Story

As a <user type>
I want to <action>
So that <benefit>

## Pre-Conditions

- Application is running at base URL
- <any specific state requirements>

## Test Steps

1. **Navigate** to `<path>`
2. **Verify** page title contains "<expected text>"
3. **Screenshot** "initial_state"
4. **Click** "<button text or selector>"
5. **Verify** "<expected result>"
6. **Type** "<text>" into "<input selector>"
7. **Screenshot** "after_action"
8. **Verify** <final condition>

## Success Criteria

- [ ] Page loads without errors
- [ ] <specific criterion 1>
- [ ] <specific criterion 2>
- [ ] All screenshots captured successfully

## Expected Output

```json
{
  "test_name": "<Test Name>",
  "status": "passed",
  "screenshots": [
    "{PROJECT_ROOT}/outputs/e2e/<test-name>/01_initial_state.png",
    "{PROJECT_ROOT}/outputs/e2e/<test-name>/02_after_action.png"
  ],
  "error": null
}
```

## Notes

- Video recording is explicit: use `playwright-cli video-start` before and `video-stop` after the test flow. Output saved to `{PROJECT_ROOT}/outputs/e2e/`
- Screenshots saved to `{PROJECT_ROOT}/outputs/e2e/<test-name>/`
- Use descriptive screenshot names for clarity
