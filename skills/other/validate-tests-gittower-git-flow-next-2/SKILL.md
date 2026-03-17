---
name: validate-tests
description: Validate and improve the test approach in an implementation plan
allowed-tools: Read, Grep, Glob, Edit
---

# Validate Test Approach

Review and improve the test plan in an implementation plan against TESTING_GUIDELINES.md.

## Instructions

1. **Find the Plan**
   - Detect current workflow folder from git branch
   - Read `.ai/<folder>/plan.md`
   - If no plan exists, suggest running `/create-plan` first

2. **Read Testing Guidelines**
   - Load TESTING_GUIDELINES.md for all test rules and conventions
   - Load GIT_TEST_SCENARIOS.md (required for setting up Git test scenarios)

3. **Validate Against Guidelines**
   - Check each test in the plan against TESTING_GUIDELINES.md requirements
   - Pay special attention to rules marked as CRITICAL in the guidelines

4. **Identify Missing Tests**
   - Check if all code paths have tests
   - Identify error conditions that need testing
   - Look for edge cases not covered

5. **Update the Plan**
   - Add missing tests to the Test Plan section
   - Improve test descriptions
   - Add specific test comments following the guidelines pattern
   - Note any testing challenges

6. **Generate Test Skeletons** (Optional)
   If requested, provide test function templates following the patterns in TESTING_GUIDELINES.md.

7. **Report Findings**
   Summarize:
   - Tests that pass validation
   - Issues found and fixes made
   - Tests added to the plan
   - Any concerns or recommendations
