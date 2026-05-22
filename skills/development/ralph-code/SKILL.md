---
name: ralph-code
description: Use this skill when developing code, especially during a TDD cycle. This is the "Green" phase of TDD
---

Implement the code to fulfill the task. If you have questions about what you're implementing 1) look at tests as they already should have been written, 2) look at SCOPES.md and DESIGN.md for the design you're implementing.

Write the code to implement the task. Do not go beyond the definition of the task, other agents will be developing those features, stick to the task you are assigned.

As you develop, after any significant piece of work is done you are permitted to commit your changes. Before commiting fix any linting errors.  Not all tests have to be passing for an in-progress commit.

Do not update tests to fit your code unless they are significantly out of line. Use the tests as they are and make your code fit the tests.

Your job is complete when: 1) All tests pass 2) All linting errors are fixed 3) all task acceptance criteria and the task description are satisfied

Once all criteria are met:
1. Ensure all tests are passing
2. Update the current task in the SCOPES.yml file to assign a status of "implementing"
3. Commit ALL remaining changes (including the status update) to VCS
4. Call the ralph-refactor skill using the Skill tool with the same arguments that were passed to this skill
