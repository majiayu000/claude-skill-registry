---
name: 054-design-tdd
description: Use when Java implementation work should be guided by Test-Driven Development, including maintaining a test list, choosing the next behavior, writing a failing test first, implementing only enough production code to pass, and refactoring while keeping tests green. This should trigger for requests such as Apply TDD; Use test-driven development; Drive this Java change with tests; Write the failing test first; Red-green-refactor this feature. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Test-Driven Development Design

Guide Java developers through Test-Driven Development for implementation work. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Maintaining or refining a list of candidate test cases
- Selecting the next useful behavior or test case before editing production code
- Writing a failing test first to clarify the public interface, API shape, or usage of the code
- Writing only enough functional production code to pass the selected test
- Refactoring new and existing code while tests remain green
- Adding newly discovered test cases to the list without losing the current TDD cycle
- Reporting skipped checks, missing tests, and remaining risks when verification is incomplete

## Constraints

Keep implementation work inside the red-green-refactor cycle, with one selected behavior driving each small change.

- **MUST** read `references/054-design-tdd.md` before applying TDD guidance
- **MUST** maintain or refine a test list when more than one behavior, edge case, or question is in scope
- **MUST** select the next useful behavior or test case before writing production code
- **MUST** write or describe the failing test first and use it to clarify the public interface or usage
- **MUST** implement only the functional production code needed to pass the selected failing test
- **MUST** refactor new and existing code only after the selected test passes and while keeping tests green
- **MUST** report skipped checks, missing tests, and remaining risks when verification is incomplete

## When to use this skill

- Apply TDD
- Use test-driven development
- Drive this Java change with tests
- Write the failing test first
- Red-green-refactor this feature
- Build this behavior test first

## Workflow

1. **Build the Test List**

Read `references/054-design-tdd.md`, then list candidate behaviors, edge cases, error paths, integration boundaries, and design questions that may need tests. Add newly discovered cases to the list as work proceeds.

2. **Select the Next Behavior**

Choose the next useful test case: small enough to implement in one cycle, valuable enough to move the design forward, and specific enough to expose the expected observable outcome.

3. **Write the Failing Test First**

Write or describe the failing unit, integration, acceptance, or characterization test before production code. Use the test to clarify the public interface, API shape, inputs, outputs, errors, or usage of the code.

4. **Make the Test Pass**

Implement the smallest functional production code needed to pass the selected test. Avoid speculative branches, abstractions, framework wiring, or cleanup that is not required by the current failing test.

5. **Refactor While Green**

After the selected test passes, refactor new and existing code to improve names, duplication, responsibility placement, type design, and test clarity while keeping the relevant tests green.

6. **Report and Continue**

Report the selected behavior, failing-test-first signal, code added to pass, refactoring performed, verification results, skipped checks, missing tests, and remaining risks. Return to the test list for the next cycle.

## Reference

For detailed guidance, examples, and constraints, see [references/054-design-tdd.md](references/054-design-tdd.md).
