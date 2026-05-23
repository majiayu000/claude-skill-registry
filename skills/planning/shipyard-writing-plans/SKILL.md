---
name: shipyard-writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

<!-- TOKEN BUDGET: 170 lines / ~510 tokens -->

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Shipyard Plan Format

Shipyard plans use XML-structured tasks with verification criteria. Each task includes:

```xml
<task id="1" name="Component Name">
  <description>What this task accomplishes</description>
  <files>
    <create>exact/path/to/file.py</create>
    <modify>exact/path/to/existing.py:123-145</modify>
    <test>tests/exact/path/to/test.py</test>
  </files>
  <steps>
    <step>Write the failing test</step>
    <step>Run test to verify it fails</step>
    <step>Write minimal implementation</step>
    <step>Run test to verify it passes</step>
    <step>Commit</step>
  </steps>
  <verification>
    <command>pytest tests/path/test.py::test_name -v</command>
    <expected>PASS</expected>
  </verification>
</task>
```

This structured format enables `/shipyard:build` to parse and execute tasks systematically, and `/shipyard:status` to track progress.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use shipyard:shipyard-executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
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
```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Agent-Driven (this session)** - I dispatch fresh builder agent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Agent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use shipyard:shipyard-executing-plans
- Stay in this session
- Fresh builder agent per task + two-stage review (spec compliance then code quality)

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses shipyard:shipyard-executing-plans
