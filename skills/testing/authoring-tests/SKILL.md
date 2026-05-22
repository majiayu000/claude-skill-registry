---
name: authoring-tests
description: |
  Use when writing, reviewing, or modifying any test files, or when asked to add
  test coverage.
user-invocable: false
---

Adhere to these principles when writing tests:

- Use arrange-act-assert:
  1. Arrange: set up the requisite state and inputs.
  2. Act: run the code that triggers the behavior under test.
  3. Assert: assert the expected outcomes.

- Keep each test focused and orthogonal to other tests unless you're testing an
  interaction between two behaviors or each test is expensive.

- Prefer parameterized testing over multiple independent calls and assertions in
  the same test.

- Test behaviors, not functions. A single function may exhibit many behaviors,
  and a single behavior sometimes spans across multiple functions.

- Write test names that describe the scenario and expected outcome of the test.

- Avoid overspecifying tests. Rule of thumb: if changing the expected data in an
  assertion does not change the meaning of test, then it shouldn't be asserted.

- Don't test implementation details. Test the public API only.

- Avoid mocks. Prefer real implementations and test doubles over mocks. Reserve
  mocks for I/O boundaries and third-party services. If you must use mocks, then
  ONLY mock public APIs.

- Extract well named variables to split up and clarify complex test data.

- Use helper functions to remove redundant details from the test body. NEVER
  hide details relevant to the test in helper functions. Pass the relevant data
  into the helper function from the test instead.

- Don't put logic in tests. Avoid conditionals and loops, and state inputs and
  outputs directly to avoid bugs in the tests themselves. If the logic is truly
  necessary, then extract it to a function and test it as well.

- Do not write redundant change detector tests. If the test would break for
  _any_ change in the code under test, then it's likely a change detector test.
