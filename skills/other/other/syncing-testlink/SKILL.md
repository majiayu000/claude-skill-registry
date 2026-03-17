---
name: syncing-testlink
description: |
  Syncs test cases from a project folder into TestLink by creating test suites,
  importing test cases with HTML formatting, building a test plan, and assigning
  cases. Use when a QA engineer wants to sync TestLink, import to TestLink,
  upload test cases, or push test cases to TestLink.
disable-model-invocation: true
tools:
  - testlink-mcp:list_projects
  - testlink-mcp:create_test_suite
  - testlink-mcp:create_test_case
  - testlink-mcp:update_test_case
  - testlink-mcp:list_test_cases_in_suite
  - testlink-mcp:create_test_plan
  - testlink-mcp:add_test_case_to_test_plan
  - testlink-mcp:get_test_cases_for_test_plan
---

# syncing-testlink

Syncs test cases from a project folder into TestLink: creates suites, imports cases with HTML formatting, builds a test plan, and assigns cases.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Validate prerequisites
- [ ] Step 2: List TestLink projects, confirm target
- [ ] Step 3: Create test suite + child suites per scenario
- [ ] Validate: Suite IDs and names
- [ ] Step 4: Sync test cases (diff: skip/update/create)
- [ ] Validate: Created/updated/skipped counts per suite
- [ ] Step 5: Create test plan, add all cases
- [ ] Step 6: Verify count matches local
- [ ] Validate: Count match (PASS/FAIL) + test plan ID
```

## Steps

### Step 1: Validate Prerequisites

Check that:
- `test_cases/README.md` exists
- At least one `test_cases/TS-XX_*.md` file exists

### Step 2: List Projects and Confirm Target

Use `testlink-mcp:list_projects` to show available projects. Ask user to confirm the target project.

### Step 3: Create Test Suites

Run `/tl-create-suite` to create a parent test suite named after the project, then create child suites for each TS-XX scenario.

**MCP tool:** `testlink-mcp:create_test_suite`

### Validate

List all created suite IDs and names. Confirm the hierarchy is correct.

### Step 4: Sync Test Cases

Run `/tl-create-case` for each TS-XX file. Use `/tl-format` for HTML formatting rules.

Before creating, compare local test cases against TestLink using diff logic:
- **MATCHING** (all fields same) → Skip
- **DIFFERS** (name matches but fields differ) → Update only differing fields
- **NEW** (name not found in TestLink) → Create with HTML formatting

Comparison fields: `name`, `summary`, `preconditions`, `steps.actions`, `steps.expected_results`.

After creation, verify preconditions were applied — update if empty.

**MCP tools:** `testlink-mcp:create_test_case`, `testlink-mcp:update_test_case`, `testlink-mcp:list_test_cases_in_suite`

### Validate

Report per suite:
- Created: N
- Updated: N
- Skipped (already matching): N

### Step 5: Create Test Plan and Assign Cases

Run `/tl-create-plan` to create a test plan using plain text (no HTML in notes field).

Run `/tl-add-case-to-plan` to add all created/existing test cases to the plan.

**MCP tools:** `testlink-mcp:create_test_plan`, `testlink-mcp:add_test_case_to_test_plan`

### Step 6: Verify Count

Use `testlink-mcp:get_test_cases_for_test_plan` to count cases in the plan.
Compare against local test case count.

### Validate

Report:
- Local test case count vs TestLink count
- Count match: **PASS** or **FAIL**
- Test Plan ID for future execution

## Expected Input

Path to project folder containing `test_cases/` with TS-XX files.

## Next Step

After syncing TestLink, run `/executing-tests` to execute the test plan.
