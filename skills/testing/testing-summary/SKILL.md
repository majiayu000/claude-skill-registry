---
name: testing-summary
description: Generate testing documentation from Linear issues and git commits. Use when the user requests test instructions, testing summary, or QA handover documentation for a completed feature or bug fix.
---

# Testing Summary

## Overview

Generate structured testing documentation by analyzing Linear issues and git commits. Produces markdown files with test scenarios, steps, and expected results formatted for QA handover.

**IMPORTANT:** Focus exclusively on QA/blackbox testing. Only include user-facing functionality, UI behavior, and observable outcomes. Exclude implementation details, code verification, component names, or technical internals.

## When to Use

Trigger this skill when users request:

- "Create test instructions for [Linear issue]"
- "Generate testing summary for the last commit"
- "Create QA handover documentation"
- "Write test scenarios for [feature/bug fix]"

## Workflow

### 1. Gather Context

Collect information from multiple sources:

**Linear Issue:**

```
Use: mcp__linear-server__get_issue
Extract: title, description, implementation steps, acceptance criteria
```

**Git Commit:**

```bash
git log -1 --stat          # Get commit summary
git show HEAD              # Get full diff
```

**Code Changes:**
Analyze the diff to understand:

- Which components were modified
- What functionality changed
- What edge cases might exist

### 2. Analyze Implementation

Map code changes to QA test scenarios (user-facing only):

- New features → Feature verification from user perspective
- Bug fixes → Regression tests for user workflows
- UI changes → Visual/interaction tests
- Form changes → Input validation and submission flows
- Data changes → Verify correct data displays to user

**Exclude:**

- Component names, file names, technical implementation
- Code structure verification
- Internal state management details
- API endpoints or backend logic

### 3. Generate Test Document

Use the template from `assets/test-template.md`:

**Structure:**

1. Summary section (issue link, commit hash, changes overview)
2. Test instructions header with:
   - Developer verification checklist
   - Environment details
   - Preconditions (data, feature flags, mock data)
3. Numbered test scenarios with:
   - Descriptive scenario title
   - Test steps (numbered list)
   - Expected results

**Scenario Guidelines:**

- Start with happy path scenarios
- Add edge cases based on user workflows
- Include negative test cases (error handling from user perspective)
- Cover all user-facing changes only
- Reference specific mock data when applicable
- Write from user perspective (no component/code references)
- Focus on "what user sees/does" not "how code works"

### 4. Fill Template Sections

**Environment:**

- Local dev, staging, or production
- Mock server if applicable

**Preconditions:**

- Required data setup
- Feature flags to enable
- Mock data created (list specific mock entities)
- User permissions needed

**Test Scenarios:**
Minimum 3-6 scenarios covering:

1. Primary functionality (happy path)
2. Alternative flows
3. Edge cases
4. Error handling
5. Integration points
6. Regression checks

## Resources

### assets/test-template.md

Standard template for test documentation. Contains the exact structure expected by QA:

```markdown
# {ISSUE-ID} - Testing Instructions

**Commit:** `{hash}` - {message}
**Issue:** {linear-url}

## Summary

{1-2 sentence overview of changes}

## Changes

- {bullet point list of modifications}

## Test Instructions

### Developer Verification before handover to QA:

- [ ] All scenarios tested & passed

**Environment:** {environment}

**Preconditions, data, feature flags:**

{list preconditions, mock data, feature flags}

---

### 1: {Scenario Title}

**Test steps:**

1. {step}
2. {step}

**Expected results:**

- {expected behavior}

---

### 2: {Scenario Title}

**Test steps:**

1. {step}

**Expected results:**

- {expected behavior}
```

## Example Usage

**User request:**

> "Create test instructions for LSTOCK-469"

**Skill execution:**

1. Fetch Linear issue `LSTOCK-469`
2. Get last commit: `git log -1 --stat` and `git show HEAD`
3. Analyze changes (renamed component, added department-specific logic)
4. Generate 6 test scenarios:
   - Email wholesaler fields visibility
   - ORDER_GW department toggle behavior
   - Mock data verification
5. Fill template with specific test steps
6. Save as `LSTOCK-469-testing.md`

## Best Practices

- **Be specific:** Reference exact component names, field names, mock data entities
- **Cover flows:** Happy path + edge cases + error states
- **Use preconditions:** List all mock data, feature flags, setup steps
- **Number everything:** Scenarios and test steps for easy reference
- **Expected results:** Be explicit about what QA should see/verify
