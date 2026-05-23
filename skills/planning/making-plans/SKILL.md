---
name: making-plans
description: Use when design is complete and you need detailed implementation tasks - breaks epics into coarse-grained Beans issues with TDD guidance, exact file paths, and verification steps
---

# Making Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch, code examples, testing approach, verification steps, docs they might need to check. But instead of a single big plan document, split the entire plan into bite-sized tasks, one Beans issue ("bean") per task. Each bean should represent a logical unit of work (e.g., "Implement auth middleware with TDD") with detailed guidance in the description.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the `making-plans` skill to create implementation tasks."

### ⚠️ PREREQUISITE: Linear ↔ Beans Epic

BEFORE continuing, you MUST read your `issue-tracking-with-beans-and-linear` skill.

Before breaking down tasks, you MUST have:

1. A Linear ticket (e.g., ZCO-123)
2. A Beans epic referencing that ticket in its title, e.g. "ZCO-123 - <title>"

If either is missing, STOP and create them first. Use `brainstorming` skill if no design exists yet.

## Task Granularity

**Each Beans issue is one logical unit:**

- "Implement auth middleware with TDD" — issue
- "Add user model and migrations" — issue
- "Create login endpoint with validation" — issue

**Within each issue description, include step-by-step guidance:**

1. Write the failing test
2. Run it to verify failure
3. Implement minimal code to pass
4. Run tests to verify
5. Commit

## Beans Issue Structure

For each task, create a Beans issue:

```bash
beans create "Implement <component>" --type task --parent <epic-id> --body "<description>"
```

**Issue description should include:**

````markdown
**Files:**

- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Steps:**

1. Write failing test:
   ```python
   def test_specific_behavior():
       result = function(input)
       assert result == expected
   ```

Run: `pytest tests/path/test.py::test_name -v` Expected: FAIL

2. Implement:
   ```python
   def function(input):
       return expected
   ```
   Run: `pytest tests/path/test.py::test_name -v` Expected: PASS

3. Commit:
   ```bash
   git commit -m "feat: add specific feature" -- tests/path/test.py src/path/file.py
   ```

**Verification:**

- [ ] Tests pass
- [ ] No type errors
- [ ] Committed
````

## Remember

- Exact file paths always
- Complete code examples (not "add validation")
- Exact commands with expected output
- Each task issue is a child of the epic

## Execution Handoff

After creating all issues:

```bash
beans list --links parent:<epic-id>
````

**"Tasks created under epic `<epic-id>`. Run `beans list --status open` to see unblocked work. Want me to start implementing?"**

When implementing:

- `beans update <id> --status in-progress` before starting
- `beans update <id> --status done` when done
