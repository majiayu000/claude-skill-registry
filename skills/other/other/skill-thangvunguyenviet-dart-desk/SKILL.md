---
name: cms-qa-testing
description: Comprehensive QA automation for dart_desk using Marionette MCP. Run test suites or individual test files against a running Flutter app.
---

# CMS QA Testing Skill

Executes structured QA test cases against a running dart_desk app via Marionette MCP.

## Prerequisites

- Dart Desk app running in debug mode with the mock data source and test document types
- Marionette MCP server connected to the app's VM service URI
- The app should be on the studio screen with at least one document type visible in the sidebar

## Invocation

User says one of:
- "run the CMS test suite" -> run all test files 01-10
- "run test 04" or "run field types basic" -> run a specific test file
- "re-discover test 02" -> force re-run discovery even if replay exists

## Execution Flow

### Phase 1: Discovery Run

For each test file to execute:

1. **Read** the test file from `packages/dart_desk/test_automation/tests/`
2. **Check** if a replay file exists in `packages/dart_desk/test_automation/replays/` and is newer than the test file. If so, use Phase 2 instead.
3. **For each test case in the file:**
   a. Log the test case ID and title
   b. Execute each step using marionette tools:
      - `tap` for button/element interactions
      - `enter_text` for text input
      - `scroll_to` for scrolling to elements
   c. After each action, call `get_interactive_elements` to verify expected state
   d. Compare actual elements against the **Expected** section
   e. Take a screenshot and save to `results/screenshots/{test_case_id}.png`
   f. Record PASS if all expectations met, FAIL with notes if not
   g. Record the marionette commands (tap, enter_text, scroll_to only -- NOT get_interactive_elements or take_screenshots) into the replay action list
4. **After all test cases in a file pass**, write the replay JSON to `replays/{test_file_name}.json`
5. **Reset app state** by calling `mcp__dart__hot_restart` (requires DTD connection)
6. **Wait** 3 seconds after hot restart for the app to stabilize, then reconnect marionette

### Phase 2: Replay Run

1. **Read** the replay JSON from `packages/dart_desk/test_automation/replays/{test_file_name}.json`
2. **For each test case:**
   a. Execute the stored `actions` sequentially (tap, enter_text, scroll_to)
   b. At each `verify` checkpoint, call `get_interactive_elements` and check `expect_text`
   c. Take a screenshot at each verify point
   d. Record PASS/FAIL
3. If any verification fails, mark as FAIL and suggest re-running discovery

### Replay JSON Format

```json
{
  "test_file": "02_document_crud.md",
  "recorded": "2026-03-16T10:30:00",
  "test_cases": [
    {
      "id": "TC-02-01",
      "title": "Create a new document",
      "actions": [
        {"action": "tap", "params": {"text": "+"}}
      ],
      "verify": [
        {"action": "get_interactive_elements", "expect_text": ["My Test Document"]}
      ]
    }
  ]
}
```

### Results Report

After all test files complete, write a markdown report to `results/reports/YYYY-MM-DD-HHmm.md`:

```markdown
# CMS QA Test Report - {date}

## Summary
- **Total:** X test cases
- **Passed:** Y
- **Failed:** Z
- **Skipped:** W

## Results

### 01 - Sidebar Navigation
| ID | Title | Result | Notes |
|---|---|---|---|
| TC-01-01 | Select document type | PASS | |
| TC-01-02 | Selection indicator | PASS | |

### 02 - Document CRUD
...
```

## Interaction Rules

- **Always use `get_interactive_elements` after every action** to verify state
- **Use `text` parameter for tapping** -- never coordinates
- **Take screenshots** only at verification checkpoints, not after every action
- If an element cannot be found by text, check if it has a `Key` and use that
- If neither text nor key works, report the element as untestable and SKIP the test case
