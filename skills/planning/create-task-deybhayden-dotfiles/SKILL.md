---
name: create-task
description: Create a task and add it to the master TODO.md file
---

TODO.md (at the root of this repo) contains an ordered checklist of tasks.

- Tasks that are complete are checked off the checklist
- Tasks **MUST** contain the path to their detailed spec, which should be located in docs/roadmap/

I want you to expand on TODO.md, so that each item in the list has a detailed write-up as a separate
document in docs/roadmap/

Each item also needs a very clearly defined exit criteria or "definition of done".

In the case of software changes where a reasonable test makes sense, the exit criteria should be a
passing test that actually tests the behavior of the software properly. Some tasks may not make
sense with an automated test, and may instead need to be manually tested, but this should be fairly
rare.

Tests should never be brittle and must always test the actual code under test.

No task is done until:

- All tests have been run and are passing.
- A code review has been completed and is clean, which may take several "code review and fix" cycles
- You may not stop until the code review is complete. If you have to wait, you wait and you don't
  stop waiting until you have received the code review.
- All documentation has been updated, and new documentation has been added where appropriate
- All changes have been committed with a single conventional commit for the task
- The task has been marked off in TODO.md and saved

Nothing should exist in TODO.md that doesn't also have a detailed document in docs/roadmap/ and no
document should exist in docs/roadmap/ that isn't referenced in TODO.md

All Definition of Done sections must include this global section:

```markdown
Global completion criteria:

- All tests have been run and are passing.
- A code-review has been run and is clean, which may take several code review and fix cycles.
- All documentation has been updated, and new documentation has been added where appropriate.
- All changes have been committed with a single conventional commit for the task.
- The task has been marked off in TODO.md and saved.
```
