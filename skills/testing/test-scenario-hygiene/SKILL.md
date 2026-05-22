---
name: test-scenario-hygiene
description: Use after TDD is finished, to review and clean the testing additions
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Review git changes to find test scenarios added this session
2. Use Task tool with general-purpose subagent to categorize tests
3. Present categorization to user via AskUserQuestion
4. Execute user's choice (remove selected tests)
5. Run formatters/linters
6. Present cleanup summary
</required>

# Overview

After TDD completes, many test scenarios may be temporary scaffolding,
useful during development but adding little long-term value.
You must review and clean up these tests.

**Announce at start:** "I'm using the Test Scenario Hygiene skill to review and clean up test scenarios from this session."

### Core Principles

<good-example> Integration test hitting real boundaries </good-example>
<good-example> Unit test for pure utility function </good-example>
<good-example> Durable end-to-end test for user workflow </good-example>
<good-example> Edge case that risks application failure </good-example>

<bad-example> Test that exclusively exercises mocks </bad-example>
<bad-example> Test for stdlib/builtin/library behavior </bad-example>
<bad-example> Brittle test checking internal state </bad-example>
<bad-example> Duplicate coverage for already-tested behavior </bad-example>

## Red Flags

Signs a test should likely be discarded:

- Test name includes "temp", "scaffold", "wip", "todo"
- Test only calls mocked functions and asserts on mock call counts
- Test duplicates coverage from an integration test
- Test asserts on implementation details (private methods, internal state)
- Test was added just to verify a single line of code works
- Test has `skip` or `xfail` markers with no clear reason

## Cleanup Steps

### Step 1: Gather Test Changes

Review all changes from this session to identify added test scenarios.

```bash
# Check staged and unstaged changes
git diff --name-only
git diff --cached --name-only

# If no current changes, check recent commits from this session
git log --oneline -20
git diff HEAD~N..HEAD --name-only  # where N = commits from this session
```

Create a list of all test files that were modified or created.
For each test file, identify the specific test scenarios (functions/methods) that were added.

**If no test changes are found:** Report this to the user and skip to Step 5 (formatters/linters).

### Step 2: Delegate Review to Subagent

Use the Task tool with `subagent_type=general-purpose` to review test quality.

Pass the list of tests with this prompt:

```
Review each of these test cases. For each test, determine:

- Is this test durable and likely useful over time? (Tests real behavior, good coverage, not overly specific to implementation details)
- OR is this test temporary/scaffolding? (Maybe useful during TDD, but brittle, testing a builtin or library, adds little long-term value)

Return a structured list categorizing each test as 'keep' or 'discard' with a brief reason.

Tests to review:
<list of test file paths and test function names>
```

### Step 3: Present Results to User

Summarize the results to the user:

<example>
The following test scenarios have been reviewed:

**Recommended to KEEP:**
- `path/to/test.ts:42` - test_name: [reason]
- `path/to/test.ts:58` - other_test: [reason]

**Recommended to DISCARD:**
- `path/to/test.ts:87` - scaffolding_test: [reason]
- `path/to/test.ts:102` - mock_only_test: [reason]

Would you like to:
1. Accept all recommendations
2. Review each test individually
3. Keep all tests
4. Discard all recommended tests
</example>

Use AskUserQuestion to determine the choice from the four options.

### Step 4: Execute User's Choice

Based on user selection:

- Accept all: Remove tests marked for discard
- Review each: Present each discard candidate one at a time, ask keep/discard
- Keep all: Skip removal, proceed to Step 5
- Discard all: Remove all tests marked for discard

When removing tests, edit the test files to delete the specific test functions/methods. Do not delete entire files unless all tests in the file are being removed.

### Step 5: Run Formatters and Linters

Check if the project has formatting/linting configured:

```bash
# Look for common config files
ls package.json pyproject.toml Cargo.toml setup.cfg .eslintrc* .prettierrc* Makefile justfile 2>/dev/null
```

**If NO formatters/linters are configured:** Ask the user if something was missed. Do not fail - just note it and proceed.

Use the Task tool to run any formatters and fix issues in a subagent.
Provide this prompt the subagent:

```
Run the project's formatters and linters. Fix any issues that arise.

Look for:
- npm run lint / npm run format
- yarn lint / yarn format  
- just fmt / just fix
- make lint / make format
- ruff / black / isort (Python)
- eslint --fix / prettier --write (JavaScript/TypeScript)
- cargo fmt / cargo clippy
```

### Step 6: Present Cleanup Summary

Present the final summary to the user:

<example>
**Test Scenario Hygiene Complete**

**Temporary tests removed:**
- `path/to/test.ts:87` - scaffolding_test
- `path/to/test.ts:102` - mock_only_test

These tests were used to keep development on track with requirements and have now been cleaned up.

**Tests retained:** N tests across M files

**Formatters/linters:** [Ran successfully / No issues / Fixed N issues / Not configured]
</example>

