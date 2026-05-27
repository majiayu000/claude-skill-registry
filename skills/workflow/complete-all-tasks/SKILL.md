---
name: complete-all-tasks
description: Complete all tasks in order in the TODO.md file.
---

Run the `complete-task` skill one after the other from the TODO.md master task list, until all tasks
are completed.

You are bound by every rule in the `complete-task` skill and all rules in the individual task
requirement documents.

Be sure that before you consider any task complete that you have ran `make test`, and that
`make test` runs 100% of the tests in the entire repository.

You must fix the code that caused the broken test, or update the test if it is no longer relevant.
Don't leave tests skipped. Either the test is a good relevant test (in which it should be kept) or
it is not (in which it should be deleted).

DO NOT DELETE tests just to make all tests pass. The purpose of our tests is to find bugs before the
users do.

Be sure that you have committed all changes as a single conventional commit for that task before
moving on to the next task.
