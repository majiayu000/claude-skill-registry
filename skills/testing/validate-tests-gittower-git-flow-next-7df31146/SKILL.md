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
   - Read `workflows/<folder>/plan.md`
   - If no plan exists, suggest running `/create-plan` first

2. **Read Testing Guidelines**
   - Load TESTING_GUIDELINES.md
   - Load GIT_TEST_SCENARIOS.md (required for setting up Git test scenarios)

3. **Validate Against Guidelines**

   Check each test in the plan against these requirements:

   ### Naming Convention
   - [ ] Descriptive names: `TestStartFeatureBranch`, `TestFinishWithMergeConflict`
   - [ ] Names indicate what is being tested

   ### One Test Case Per Function (CRITICAL)
   - [ ] NO table-driven tests for integration scenarios
   - [ ] Each test function tests exactly ONE scenario
   - [ ] Exception only for pure validation functions

   ### Required Test Comments
   - [ ] First line: Brief description
   - [ ] `Steps:` section with numbered list
   - [ ] Expected outcomes in steps

   ### Test Setup Pattern
   - [ ] Uses `testutil.SetupTestRepo(t)`
   - [ ] Uses `defer testutil.CleanupTestRepo(t, dir)`
   - [ ] Uses `testutil.RunGitFlow()` not direct exec
   - [ ] Uses `git flow init --defaults` for setup

   ### Working Directory (CRITICAL)
   - [ ] Uses testutil functions that set `cmd.Dir`
   - [ ] NO reliance on `os.Chdir()` unless unavoidable
   - [ ] If `os.Chdir()` needed, proper save/restore pattern

   ### Coverage Requirements
   - [ ] Success path tested
   - [ ] Error conditions tested
   - [ ] Edge cases identified and tested

4. **Identify Missing Tests**
   - Check if all code paths have tests
   - Identify error conditions that need testing
   - Look for edge cases not covered

5. **Update the Plan**
   - Add missing tests to the Test Plan section
   - Improve test descriptions
   - Add specific test comments following the pattern
   - Note any testing challenges

6. **Generate Test Skeletons** (Optional)
   If requested, provide test function templates:

   ```go
   // TestFeatureName tests <description>.
   // Steps:
   // 1. Sets up a test repository and initializes git-flow
   // 2. <Step 2>
   // 3. <Step 3>
   // 4. Verifies <expected outcome>
   func TestFeatureName(t *testing.T) {
       dir := testutil.SetupTestRepo(t)
       defer testutil.CleanupTestRepo(t, dir)

       // Initialize git-flow with defaults
       output, err := testutil.RunGitFlow(t, dir, "init", "--defaults")
       if err != nil {
           t.Fatalf("Failed to initialize git-flow: %v\nOutput: %s", err, output)
       }

       // TODO: Implement test
   }
   ```

7. **Report Findings**
   Summarize:
   - Tests that pass validation
   - Issues found and fixes made
   - Tests added to the plan
   - Any concerns or recommendations

## Checklist Output

After validation, add this checklist to the plan:

```markdown
## Test Validation Checklist
- [x] All tests follow naming conventions
- [x] One test case per function rule followed
- [x] Test comments include Steps section
- [x] Using testutil helpers correctly
- [x] Success and error paths covered
- [ ] <Any remaining issues>
```
