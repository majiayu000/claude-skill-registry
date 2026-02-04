---
name: implementation-planning
description: Use when you have specifications or requirements for multi-step implementation tasks requiring comprehensive documentation for handoff
---

# Implementation Planning

## Overview

Write comprehensive implementation plans assuming the engineer is skilled but unfamiliar with the codebase and project conventions. Document everything they need: which files to touch for each task, complete code examples, testing commands, documentation to reference, and verification steps. Break work into atomic, committable units following DRY, YAGNI, and TDD principles.

**Announce at start:** "I'm using the implementation-planning skill to create the implementation plan."

**Context:** Plans should be created in a dedicated worktree for isolation.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## When to Use

**Use implementation-planning when:**
- Multi-step implementation (3+ distinct tasks)
- Complex integration requiring file-level navigation guidance
- Handoff to another developer or future execution session
- TDD cycle needs documentation for consistency across tasks
- Clear requirements exist and architecture approach is defined

**Don't use for:**
- Single-file changes (just implement directly)
- Well-established patterns with existing guides (reference those instead)
- Exploratory prototyping (plans constrain necessary experimentation)
- Unclear requirements (use brainstorming first)

## Atomic Task Granularity

**Each step is one atomic action:**
- Focused on single outcome
- Independently testable
- Committable as logical unit
- Has clear Definition of Done

**Examples of atomic steps:**
- "Write the failing test" - one step
- "Run it to verify failure" - one step
- "Implement minimal code to make test pass" - one step
- "Run tests and verify they pass" - one step
- "Commit changes" - one step

**NOT atomic:**
- "Write and run tests" - two steps combined
- "Implement feature with error handling" - multiple concerns
- "Update code and documentation" - separate commits

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Prerequisites:**
- [Any setup needed before starting]
- [Dependencies that must be installed]

---
```

## Task Structure

Each task follows this template:

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145` (lines if known)
- Test: `tests/exact/path/to/test.py`
- Docs: `docs/path/to/reference.md` (if relevant)

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    # Arrange
    input_data = create_test_input()

    # Act
    result = function(input_data)

    # Assert
    assert result == expected_output
```

**Why this test:** [Explain what behavior this verifies]

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_specific_behavior -v`

Expected output:
```
FAILED - NameError: name 'function' is not defined
```

**Step 3: Write minimal implementation**

```python
def function(input_data):
    """Brief docstring explaining purpose."""
    # Minimal code to make test pass
    return expected_output
```

**Why minimal:** [Explain what's deliberately omitted for now]

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_specific_behavior -v`

Expected output:
```
PASSED
```

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature

- Implements [specific behavior]
- Tests verify [specific condition]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Definition of Done:**
- [ ] Test written and fails for right reason
- [ ] Implementation makes test pass
- [ ] No other tests broken
- [ ] Code committed with clear message
```

## Quality Standards

**Every task MUST include:**

1. **Exact file paths** - No "update the config file" without path
2. **Complete code** - No "add validation logic" without showing the code
3. **Exact commands** - Full command with flags, not "run tests"
4. **Expected output** - What success/failure looks like
5. **Definition of Done** - Checklist for task completion

**Code examples must be:**
- Complete and runnable
- Include necessary imports
- Show actual logic, not pseudocode
- Have minimal comments (code should be self-explanatory)

## Cross-Skill References

**Reference skills using requirement markers, NOT @ syntax:**

```markdown
# ✅ GOOD: Explicit requirement marker
**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development

**BACKGROUND:** Understanding superpowers:systematic-debugging helps with troubleshooting

# ❌ BAD: @ syntax force-loads and burns context
@skills/test-driven-development/SKILL.md
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Vague tasks ("add validation") | Engineer doesn't know what to implement | Include complete validation code in plan |
| Missing file paths | Time wasted searching codebase | Exact path for every file touched |
| "Run tests" without specifics | Wrong tests run, or none at all | Exact command with file::function and expected output |
| Generic commit messages | Hard to review, poor history | Follow conventional commits with context |
| Skipping test failure verification | False confidence (test might not work) | Always verify RED before implementing GREEN |
| Combining multiple actions in one step | Unclear what to commit, harder to debug | Each step = one atomic action |
| Assuming context knowledge | Engineer unfamiliar with codebase stuck | Document which files define types, where utilities live |
| Incomplete code examples | "Figure it out" wastes time | Complete, runnable code in plan |

## Red Flags - STOP and Revise Plan

These thoughts mean incomplete plan:

| Excuse | Reality |
|--------|---------|
| "They'll figure out the details" | Details ARE the plan. Document them. |
| "File path is obvious from context" | Not obvious to someone unfamiliar. State it explicitly. |
| "Standard validation, doesn't need code" | What's standard to you is unclear to others. Show the code. |
| "Test command is straightforward" | Exact command eliminates ambiguity. Specify it. |
| "This step is quick, combine with next" | Atomic steps = atomic commits. Keep separate. |

**If you catch yourself using these rationalizations, STOP and add the missing details.**

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task with code review between tasks for fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans for batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review after each

**If Parallel Session chosen:**
- Guide them to open new session in the worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans
- Batch execution with review checkpoints

## Principles Summary

**DRY (Don't Repeat Yourself):**
- Extract common utilities rather than duplicating code
- Reference existing patterns instead of reinventing

**YAGNI (You Aren't Gonna Need It):**
- Implement only what's specified in requirements
- Don't add "nice to have" features preemptively

**TDD (Test-Driven Development):**
- Always test first, implementation second
- Watch test fail before writing production code
- Keep implementation minimal to pass test

**Frequent Commits:**
- Each atomic step = one commit
- Clear, conventional commit messages
- Commits tell the story of implementation
