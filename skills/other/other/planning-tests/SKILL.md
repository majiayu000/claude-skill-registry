---
name: planning-tests
description: |
  Creates a complete test plan from a project folder by detecting the ticket
  type, writing test plan sections, reviewing coverage, and publishing to
  Confluence. Use when a QA engineer wants to plan tests, create a test plan,
  write a test plan, or start test planning for a project.
disable-model-invocation: true
tools:
  - mcp-atlassian:confluence_create_page
  - mcp-atlassian:confluence_get_page
---

# planning-tests

Creates a complete test plan from a project folder by detecting the ticket type, writing sections, and publishing to Confluence.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Validate prerequisites
- [ ] Step 2: Detect ticket type and route
- [ ] Step 3: Write test plan to test_plan/
- [ ] Step 4: Review coverage (matrix + diagrams)
- [ ] Validate: Scenario count + coverage assessment
- [ ] Step 5: Create Confluence test plan pages
- [ ] Validate: Confluence URL + page count
- [ ] Step 6: Review Confluence for formatting issues
```

## Steps

### Step 1: Validate Prerequisites

Check that `00_Main_Task_*.md` exists in the current project folder.

If missing: "Please run `/receiving-tickets [TICKET]` first to gather all documentation."

### Step 2: Detect Ticket Type and Route

Run `/tw-plan-init` to detect the ticket type and route to the appropriate planning command:
- **Type A (Feature):** → `/tw-plan-feature`
- **Type B (Bug Fix):** → `/tw-plan-bugfix`
- **Type C (Enhancement):** → `/tw-plan-enhance`

### Step 3: Write Test Plan

Execute the routed planning command from Step 2. It writes test plan sections to `test_plan/README.md` and `test_plan/sections/` based on the detected type:
- Feature: 5-8 scenarios, comprehensive coverage
- Bug Fix: 2-4 scenarios, focused on defect verification + regression
- Enhancement: 4-6 scenarios, hybrid new + regression

### Step 4: Review Plan

Run `/tw-plan-review` to analyze coverage and generate:
- Coverage matrix (ASCII table)
- Gap and overlap analysis

Run `/tw-diagrams` to generate diagrams for 5+ scenarios (configuration flow, data flow, modular design).

### Validate

Report:
- Total scenario count
- Estimated test case count
- Coverage assessment: **READY FOR TEST CASES** or **NEEDS REVISION**

### Step 5: Create Confluence Pages

Run `/cf-create-page` to create the test plan hierarchy in Confluence.

#### Page Naming Convention

##### Feature (Type A)

| Source File | Page Title Format |
|-------------|-------------------|
| `README.md` | `[PROJECT_ID]: Test Plan - [Feature Name]` |
| `sections/01_Project_Business_Context.md` | `[PROJECT_ID]: 1. Project & Business Context` |
| `sections/02_Feature_Definition.md` | `[PROJECT_ID]: 2. Feature Definition` |
| `sections/03_Scope_Boundaries.md` | `[PROJECT_ID]: 3. Scope & Boundaries` |
| `sections/04_Test_Strategy.md` | `[PROJECT_ID]: 4. Test Strategy` |
| `sections/05_References_Resources.md` | `[PROJECT_ID]: 5. References & Resources` |
| `sections/06_Revision_History.md` | `[PROJECT_ID]: 6. Document Revision History` |

##### Bug Fix (Type B)

| Source File | Page Title Format |
|-------------|-------------------|
| `README.md` | `[PROJECT_ID]: Test Plan - [Bug Description]` |
| `sections/01_Problem_Context.md` | `[PROJECT_ID]: 1. Problem Context` |
| `sections/02_Test_Scope.md` | `[PROJECT_ID]: 2. Test Scope` |
| `sections/03_Test_Strategy.md` | `[PROJECT_ID]: 3. Test Strategy` |
| `sections/04_References_Resources.md` | `[PROJECT_ID]: 4. References & Resources` |
| `sections/05_Revision_History.md` | `[PROJECT_ID]: 5. Document Revision History` |

##### Enhancement (Type C)

| Source File | Page Title Format |
|-------------|-------------------|
| `README.md` | `[PROJECT_ID]: Test Plan - [Enhancement Name]` |
| `sections/01_Enhancement_Context.md` | `[PROJECT_ID]: 1. Enhancement Context` |
| `sections/02_Enhancement_Definition.md` | `[PROJECT_ID]: 2. Enhancement Definition` |
| `sections/03_Test_Scope.md` | `[PROJECT_ID]: 3. Test Scope` |
| `sections/04_Test_Strategy.md` | `[PROJECT_ID]: 4. Test Strategy` |
| `sections/05_References_Resources.md` | `[PROJECT_ID]: 5. References & Resources` |
| `sections/06_Revision_History.md` | `[PROJECT_ID]: 6. Document Revision History` |

Create parent page first, then child pages for each section. Parent page ID is provided by the user.

**MCP tool:** `mcp-atlassian:confluence_create_page`

### Validate

Report:
- Confluence parent page URL
- Number of pages created

### Step 6: Review Confluence

Run `/cf-review-page` to fetch each created page and check for markdown conversion issues (lists rendering as plain text, missing tables, etc.).

**MCP tool:** `mcp-atlassian:confluence_get_page` with `convert_to_markdown: false`

## Expected Input

Path to project folder containing `00_Main_Task_*.md` and optional Confluence docs.

## Next Step

After planning tests, run `/designing-cases` to create detailed test cases.
