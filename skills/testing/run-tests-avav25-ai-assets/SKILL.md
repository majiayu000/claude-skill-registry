---
name: run-tests
description: Run the relevant test suite for the current task by reading TESTING.md, selecting the affected stack, executing tests, and summarizing failures or verification.
---

# Run Tests

## Workflow

1. Read `TESTING.md` if present, otherwise use `AGENTS.md` and project config.
2. Select the narrowest relevant test command first.
3. Run broader regression checks when the change warrants it.
4. Summarize failures with likely causes.
5. If possible, fix obvious test issues and rerun.
