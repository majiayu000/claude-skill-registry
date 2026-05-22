---
name: ralph-test
description: Use this skill when writing tests, especially when working in TDD style to define tests before the actual functions are complete. This is the "Red" phase of TDD.
---

Your goal is to write tests for the currently scoped task. You should be able to do this autonomously with no input from the user, if you need more information look at the SCOPES.yml or DESIGN.yml files for the project.

## Tasks That Don't Require Tests

Some tasks have no testable behavior. Before writing tests, evaluate if the task falls into one of these categories:

- **TypeScript type definitions** - Interfaces, type aliases, enums, and other pure type constructs have no runtime behavior to test. The TypeScript compiler validates these.
- **Type-only files** - Files that only export types (e.g., `webhookTypes.ts`, `*Types.ts`) don't need tests.
- **Re-exports** - Files that simply re-export from other modules.

If the task only involves creating types/interfaces with no runtime code:
1. Skip directly to the ralph-code skill (no stubs or tests needed)
2. Pass the same arguments that were passed to this skill

Otherwise, proceed with the normal test-writing workflow below.

---

First, create stubs:
In the code being tested create stubs for any missing functions for the task we're devleoping. These functions can have hard coded or empty return values and should not cause any side effects.  This will give us something for the tests to import and run, expecting that the tests themselves will initially be failing.

Second, create tests:
- Tests should be organized by behaviors, using nested describe blocks if needed
- **DO** write tests for exported/public functions
- **DO** write tests for reasonable edge cases but these should be limited
- **DO NOT** over test, make sure intended behaviors and happy paths are tested but do not write tests for things that should not happen
- **DO NOT** write tests for private functions or internal implementation details
- Don't over-mock, try to use the real versions of methods when doing so doesn't add a lot of additional effort or make the tests hard to reason about
- Keep tests focused on just one or two assertions. If a test has more than 3 assertions it may need to be broken up into multiple tests. This is not a rule but a strong guideline.
- Don't write lots of test utility functions, limit these to things like object generators, but in general having a lot of code in tests causes confusing and brittle tests, prefer to hard code the values you need when this would not significantly bloat the test
- Don't test implementation details - directly or indirectly - of third party modules or systems, trust those development teams to have done their jobs and only test the systems we're responsible for

Third, reevaluate the quality of each test - delete or update any that do not pass these criteria
- Is the test accurate
- Does the test describe a behavior that needs to be protected and/or documented, or is it just an implementation detail
- Is the test simple and readable
- Is this test redundant
- **IMPORTANT** Is this test testing code, or just testing itself. It is easy to accidentally write tests that, because of mocking and contrived data, do not test the function in any meaningful way and instead just confirm that they return what they've already forced the code to return

Fourth, update the current task in the SCOPES.yml file to assign a status of "testing"

Fifth, commit ALL changes (including the status update) to VCS.

Finally, call the ralph-code skill using the Skill tool with the same arguments that were passed to this skill.
