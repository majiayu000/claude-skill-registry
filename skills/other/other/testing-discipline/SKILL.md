---
name: testing-discipline
description: Use when writing or reviewing tests, designing test data, naming a test, choosing what to assert, or writing test helpers/mocks/fixtures
---

# Testing Discipline

## Overview

**A good test pins the contract, uses concrete examples, names the scenario in domain language, and uses test data safe to show a customer.** Run the checklist in order when writing or reviewing a test.

## When to invoke

Invoke when you're about to:

- Write a new test (unit, integration, end-to-end, characterization)
- Name or rename a test method, test class, or test file
- Design a fixture, mock, stub, or shared test helper
- Choose test data — names, IDs, sample strings, sample numbers
- Decide what to assert in a test (exact value? structural property? both?)
- Schedule a long-running suite (soak, perf, cross-platform matrix)
- Hand off requirements between programmers and testers, or work on acceptance tests
- Review existing tests for quality, coverage gaps, or test smells
- Evaluate whether a test suite adequately covers a contract

### Non-triggers — do NOT invoke for

- Running the existing test suite (`npm test`, `pytest`)
- Fixing a one-line broken assertion where the intent is unchanged
- Adding a docstring or comment to an existing test
- Reordering imports in a test file
- Updating a snapshot file when the underlying intentional change is already understood

If you're not sure whether a change counts as "writing a test," **invoke anyway** — the checklist is short and skipping it produces tests that pass forever while protecting nothing.

## Test quality checklist

Run every step in order when writing a new test. When reviewing, use the same checks to evaluate quality.

1. **Tests are part of the change, not optional polish.** Software's only practical pre-deployment validation is execution under realistic conditions. A change without tests is an incomplete change. *(Ford, 97/83.)*
2. **Assert the required behavior, not an incidental of the current implementation.** Ask: what does the contract actually promise? For a 3-way comparator the contract is "negative if less, positive if greater, zero if equal" — not "exactly -1 or +1." Asserting ±1 nails an incidental and will go red the day someone returns -2. Tests that mirror code structure end up asserting that the code does what the code does. *(Henney, 97/80.)*
3. **Be precise *and* accurate. Use concrete examples.** "Result is sorted and same length" passes for `[3,3,3,3,3,3]` against an input of `[3,1,4,1,5,9]`. The full postcondition is sorted *and a permutation of the input* — but expressing that as a generic checker is often more code than the function under test. Prefer a concrete example pair: input `[3,1,4,1,5,9]`, expected `[1,1,3,4,5,9]`. "Adding to an empty collection" is not "now non-empty" — it's "now contains exactly one item, and that item is X." *(Henney, 97/81.)*
4. **Write the test for the next person who has to read it.** A good test is documentation. Make three parts visible in this order: the context/preconditions, the call into the system, the expected result. Hide trivia behind named helpers (Extract Method) so the reader sees the scenario, not the scaffolding. Give the test a name describing the scenario *and* the entry point — `Stack_pop_on_empty_throws` reads better than `test17`. Then test the test: introduce a deliberate bug into the code under test on a private branch and verify the failure message tells you what went wrong. *(Meszaros, 97/95.)*
5. **Choose test data that is safe in front of a customer.** Placeholder names, fake company names, sample log strings, mock error dialogs, and seeded database rows have a habit of surfacing in screenshots, demos, leaked source, and production logs. Do not use real people's names you mean to mock, do not use band names or song titles as a private joke, do not write `"don't click that again, you moron"` as a placeholder dialog, do not use four-letter words as fake stock tickers. Use boring, obviously-fake, professional data. *(Begbie, 97/25.)*
6. **Accept acceptance tests as requirements input.** When acceptance tests exist for a behavior (from QA, from the customer, from a spec), use them as input to the work — they surface ambiguities cheaper than defect tickets. *(Hufnagel, 97/60; Gregory, 97/92.)*

## Red Flags

These thoughts mean STOP — restart the checklist:

| Thought | Reality |
|---|---|
| "I'll just assert the function returns exactly -1." | The contract says "negative" — ±1 is an implementation incidental. The test will go red on a valid refactor and tell you nothing about the requirement. (97/80) |
| "Same length, all elements in range — that's enough for a sort test." | `[3,3,3,3,3,3]` satisfies that and is wrong. Use a concrete input/output pair so the only correct answer is the one in the assertion. (97/81) |
| "I'll seed the database with band members and song titles — funnier than `User1`." | Cute test data ends up in customer screenshots, demos, and leaked source. Use boring, obviously-fake, professional data. (97/25) |
| "No time to write the test — we'll add it later." | "Later" rarely arrives, and shipping without verification is professionally irresponsible. The test is part of the change. (97/83) |
| "I know what this test means — I just wrote it." | You will not, in six months. Tests are read more than they are written. Name the scenario, structure as context/act/assert, hide scaffolding. (97/95) |
| "`test17` is a fine name — the body explains it." | Test names are scanned to verify coverage and to read failure reports. Encode the scenario and the entry point in the name. (97/95) |
| "The test setup is fifty lines, then a one-line assert — but it works." | Test pain is design pressure. If the setup dwarfs the body, reshape the production code. Do not mock harder. (`GOOS/ListenToTestPain`) |
| "I'll assert that `repo.save` was called exactly three times." | Over-specifying mock interactions makes the test red on innocent refactors. Assert on the observable contract, not the call shape. (`xUnit/FragileTest`) |
| "The test reads from `/tmp/fixtures/users.json` set up in `conftest.py`." | Mystery Guest. The test cannot be read in isolation. Build the fixture in the test or in a function named for what it returns. (`xUnit/MysteryGuest`) |
| "I'll branch on the return value and assert different things in each branch." | One test, two scenarios fighting for one name. Split into two tests, or use named parameterized cases. (`xUnit/ConditionalTestLogic`) |

## What "done" looks like

A single well-written test is done when **all** of the following are true:

- [ ] The assertion targets the contract, not an incidental of the current implementation.
- [ ] The expected result is concrete enough that a reader can check it by eye in under thirty seconds.
- [ ] The test name describes the scenario and the entry point in domain language.
- [ ] Context, action, and expected result are visible as three readable sections; scaffolding is behind named helpers.
- [ ] Test data (names, IDs, strings, log lines, error messages) is safe to appear in a customer screenshot.
- [ ] You verified the test fails for the right reason — by introducing a deliberate bug on a private branch and reading the failure message.

If any box is unchecked, the test is not done. Either finish, or delete it and start over.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/25 | Don't Be Cute with Your Test Data | Rod Begbie |
| 97/60 | News of the Weird: Testers Are Your Friends | Burk Hufnagel |
| 97/80 | Test for Required Behavior, Not Incidental Behavior | Kevlin Henney |
| 97/81 | Test Precisely and Concretely | Kevlin Henney |
| 97/82 | Test While You Sleep (and over Weekends) | Rajith Attapattu |
| 97/83 | Testing Is the Engineering Rigor of Software Development | Neal Ford |
| 97/92 | When Programmers and Testers Collaborate | Janet Gregory |
| 97/95 | Write Tests for People | Gerard Meszaros |
| `GOOS/ListenToTestPain` | Listen to Test Pain | Steve Freeman & Nat Pryce |
| `xUnit/ObscureTest` | Obscure Test | Gerard Meszaros |
| `xUnit/FragileTest` | Fragile Test | Gerard Meszaros |
| `xUnit/MysteryGuest` | Mystery Guest | Gerard Meszaros |
| `xUnit/ConditionalTestLogic` | Conditional Test Logic | Gerard Meszaros |

See `principles.md` for the long-form distillations, citations, and source links.
