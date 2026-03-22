---
name: reconcile-tests
description: Add, update, or delete tests for changes in the current commit
disable-model-invocation: true
---

Add, update, or delete tests for changes made in the current `jj` commit.

Before starting, read: `../authoring-tests/SKILL.md`

# Goals

- Delete no longer applicable tests
- Update outdated test expectations
- Add tests for new behaviors

# Recently changed files

!`jj diff --summary`

If no files are changed, the consider all files in the current directory.

# Workflow

1. Explore each deleted, updated, or added file:
   1. Read the file if it still exists
   2. Run `jj diff <file>` to view changes
   3. Identify:
      - Deleted logic
      - Modified logic (new branches, edge cases, changed behavior)
      - New logic
2. Find the test files that import or reference the changed code. Create them if
   missing
3. Run the relevant tests
4. Examine failing tests and update them as necessary:
   1. Delete if no longer applicable
   2. Update if expectations are outdated
   3. Flag regressions to the user. Describe the changed behavior, the failing
      test, and your hypothesis about why it's a bug. Ask how to proceed Go back
      to step 3 after making updates until all tests pass
5. Add tests for new behaviors
6. Run the new tests
7. Examine failing tests and update them as necessary:
   1. Update if there's a bug in the test
   2. Flag to the user if the tests caught a bug, Describe the behavior, the
      failing test, and your hypothesis about why it's a bug. Ask how to proceed
      Go back to step 7 after making updates
8. Run tests with coverage if possible. If _new_ logic is not covered, then go
   back to step 5
