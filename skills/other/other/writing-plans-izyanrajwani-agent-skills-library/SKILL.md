---
name: writing-plans
description: Structured implementation planning for multi-step development tasks. Use when you have a spec or requirements and need to break work into executable steps.
---

# Writing Plans

## Overview

Create implementation plans for an engineer with zero codebase context.

Each plan includes:
- Exact file paths for every operation
- Complete code (not "add validation here")
- Test-first approach with verification commands
- Bite-sized steps (2-5 min each)

Principles: DRY, YAGNI, TDD, frequent commits.

**Announce at start:** "I'm using the `writing-plans` skill to create the implementation plan."

**Context:** Run in dedicated worktree. If none exists, use `using-git-worktrees` skill first.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Before Writing

1. Read spec/requirements completely
2. Explore project structure (`view .`)
3. Identify tech stack (package.json, pyproject.toml, etc.)
4. Note existing patterns in similar files
5. Check docs/ for existing conventions

## Bite-Sized Task Granularity

Each step is one action (2-5 minutes), independently verifiable:

- "Write the failing test" — step
- "Run it to confirm failure" — step
- "Implement minimal code to pass" — step
- "Run tests to confirm pass" — step
- "Commit" — step

## Plan Document Header

Every plan MUST start with this header:

~~~markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
~~~

## Task Structure

~~~markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
~~~

## Before Handoff

Verify plan completeness:

- Every file path exists or will be created
- Every command can be run exactly as written
- No TODO/placeholder text remains
- Tests cover all acceptance criteria from spec
- Include exact test code, not descriptions

## Execution Handoff

After saving plan, present:

**"Plan saved to `docs/plans/<filename>.md`. Choose execution mode:**

1. **Subagent-Driven** — same session, fresh subagent per task, fast iteration
2. **Parallel Session** — new session, batched execution with checkpoints

**Which approach?"**

### If Subagent-Driven chosen

- Stay in this session
- **REQUIRED SUB-SKILL:** `subagent-driven-development`
- Fresh subagent per task + two-stage review

### If Parallel Session chosen

- Guide user to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses `executing-plans`
