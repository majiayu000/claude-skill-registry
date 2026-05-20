---
name: tdd
description: a workflow for practicing Test-Driven Development (TDD)
---

# TDD Skill (Test-Only, Anti-Cheat, Minimal Version)

This skill defines a strict but lightweight TDD workflow designed for coding agents.
It enforces honesty, prevents cheating, and minimizes token usage by focusing solely on **tests**.

---

## Core Anti-Cheat Contract
*(Always enforced in every state)*

1. **Never claim tests passed or failed unless you have just run them and shown the exact output.**
2. **If you cannot run tests, enter `BLOCKED` immediately. Do not guess or infer results.**
3. **Never modify test assertions just to make a failing test pass.**
4. **Only transition between TDD states when the required test evidence has been shown.**
5. **In RED, implement only the *minimum* code necessary to make the currently failing test pass.**
6. **Every message must begin with a TDD state prefix**, and the prefix must match the actual test evidence.
7. **Promote the Dependency Rule**
   If making a failing test for the current SUT pass requires changing a dependency,
   you must stop and promote that dependency to be the SUT.
   Write a failing test for the dependency, make it pass, then return to the original SUT.

   Clarification:
    - Modifying a dependency counts as production code.
    - Production code may only be written to satisfy the currently failing test.
    - Therefore, any dependency change must be justified by its own failing test.

---

## TDD Layer Discipline

When testing layer A that mocks layer B:
- Layer B only needs a **method signature** (stub returning null or throwing UnsupportedOperationException)
- Do NOT implement Layer B's logic until you write Layer B's tests
- Ask: "Is the service/dependency mocked in this test?" If yes, only a stub is needed.

Example:
- Controller test mocks CustomerService → CustomerService.createLocationForCustomer() should be `throw new UnsupportedOperationException("implement me")`
- CustomerService test (separate task) will drive the actual implementation

---

## Outside-In Development

Use outside-in development: start from the external interface and work inward.

**Why:** Every piece of code should be immediately callable and tested from an external perspective. Avoid creating "infrastructure only" code to be connected later.

**Correct order for implementing a feature:**
1. Write test for the external interface (command handler, REST endpoint)
2. Implement the handler/controller, which calls the service method
3. Implement the service method, which uses infrastructure (events, repositories)
4. Create infrastructure as needed to satisfy the test

**Anti-pattern:** Creating event publishing code or domain methods without a caller (no REST endpoint or command handler to invoke them). Every method should have an entry point that exercises it.

---

## Evidence Format (Required)

Whenever tests are mentioned:

Evidence:

* tests: pass | fail | not-run
* last_output: <exact test output snippet>


Rules:
- `pass` or `fail` may only be used if tests were just executed.
- `not-run` must be used if tests cannot be executed.
- Never infer test status from code.

---

# TDD States

## ⚪ TDD: PLANNING
**Goal:**  
Write a meaningful failing test that expresses the desired behavior.

**Allowed actions:**  
- Ask clarification questions  
- Write or update a test  
- Run tests to show failure  

**Pre-conditions to enter RED:**  
- A test exists  
- The test was just run  
- A failing test is shown  
- The failure reflects missing/incorrect behavior  

**Transition:**  
- If pre-conditions satisfied → `RED`  
- Otherwise remain in `PLANNING`

---

## 🔴 TDD: RED
**Goal:**  
Make the failing test pass using the *minimum* implementation.

**Allowed actions:**  
- Analyze the failing test  
- Implement the smallest possible change  
- Run tests again  
- Justify why the implementation is minimal  

**Pre-conditions to enter GREEN:**  
- The previously failing test now passes  
- All tests pass  
- Test output is shown  

**Transition:**  
- If all tests pass → `GREEN`  
- If tests still fail → remain in `RED`  
- If tests cannot run → `BLOCKED`

---

## 🟢 TDD: GREEN
**Goal:**
The behavior is now correct; evaluate and prepare safe refactoring.

**Allowed actions:**
- Re-read the actual code changes made in this cycle
- Identify safe refactorings
- Explain improvement intent
- Run tests as needed

**Required Evaluation (before any transition):**
1. **Re-read the actual code changes** made in this cycle (use `git diff HEAD`, not memory)
2. **List at least one observation** about potential refactoring (even if "no duplication found")
3. **If duplication exists**, either refactor it OR note it as intentional with justification

Skipping directly from GREEN to VERIFY without this explicit evaluation is a TDD violation.

**Pre-conditions to enter REFACTOR:**
- All tests currently pass
- Recent test output shown
- A refactoring goal identified

**Transition:**
- If refactoring is needed → `REFACTOR`
- If no refactoring needed → `VERIFY`

---

## 🛠️ TDD: REFACTOR
**Goal:**  
Improve internal code structure without changing behavior.

**Allowed actions:**  
- Perform small safe refactorings  
- Run tests immediately after each change  

**Pre-conditions to exit REFACTOR:**  
- Tests were run after the last change  
- All tests pass  
- Test output is shown  

**Transition:**  
- If tests pass → `VERIFY`  
- If tests fail → return to `RED`  
- If tests cannot run → `BLOCKED`

---

## ✅ TDD: VERIFY
**Goal:**  
Confirm the entire TDD cycle is complete.

**Allowed actions:**  
- Run the full test suite  
- Show test results  
- Summarize completed behavior  

**Pre-conditions to enter COMPLETE:**  
- All tests pass  
- Test output is shown  

**Transition:**  
- If all tests pass → `COMPLETE`  
- If any test fails → `RED`  
- If tests cannot run → `BLOCKED`

---

## 🏁 TDD: COMPLETE
**Goal:**  
The TDD cycle for this behavior is finished.

**Allowed actions:**  
- Provide a concise summary  
- Stop unless the user starts a new cycle  

---

## ⚠️ TDD: BLOCKED
**Goal:**  
Tests cannot be run; you cannot proceed honestly.

**Actions:**  
- State explicitly why tests cannot run  
- Show the exact command the user should run  
- Ask for the output  

**Transition:**  
- When test results are provided → return to prior state  
- Do *not* infer test status  

---

## 🚨 TDD: VIOLATION
**Goal:**  
The agent has broken the TDD rules.

**Actions:**  
1. State what rule was violated  
2. Explain the correct behavior  
3. Undo or repair the incorrect action  
4. Return to the correct state  

---

# End of Skill
