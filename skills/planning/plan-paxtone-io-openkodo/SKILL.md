---
name: plan
description: >
  Create implementation plans with TDD approach.
  Use to structure work before coding, ensuring test coverage from the start.
---

# Writing Implementation Plans

## Overview

Create comprehensive implementation plans assuming the engineer has zero context.
Document everything: which files to touch, complete code snippets, how to test.
Break work into bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Core principle:** Each task is 2-5 minutes of work. Test first, implement second.

**Announce at start:** "I'm using the plan skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is ONE action (2-5 minutes):**

```
Task N: Add validation function

Step 1: Write the failing test
Step 2: Run it to verify it fails
Step 3: Implement minimal code to pass
Step 4: Run tests to verify they pass
Step 5: Commit
```

**NOT acceptable:**
- "Implement validation with tests" (too vague)
- "Add function and write tests" (multiple actions)

## Plan Document Structure

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** Use kodo:execute skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**GitHub Issue:** [Link if exists, or "Create with `kodo track issue`"]

---
```

## Task Structure Template

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.rs`
- Modify: `exact/path/to/existing.rs:123-145`
- Test: `tests/exact/path/to/test.rs`

**Step 1: Write the failing test**

```rust
#[test]
fn test_specific_behavior() {
    let result = function(input);
    assert_eq!(result, expected);
}
```

**Step 2: Run test to verify it fails**

Run: `cargo test test_specific_behavior`
Expected: FAIL with "cannot find function `function`"

**Step 3: Write minimal implementation**

```rust
pub fn function(input: Input) -> Output {
    // Minimal implementation
    expected
}
```

**Step 4: Run test to verify it passes**

Run: `cargo test test_specific_behavior`
Expected: PASS

**Step 5: Commit**

```bash
git add src/path/file.rs tests/path/test.rs
git commit -m "feat: add specific feature"
```
```

## What Plans Must Include

**For every task:**
- Exact file paths (not "in the tests folder")
- Complete code snippets (not "add validation logic")
- Exact commands with expected output
- Clear success criteria

**For the overall plan:**
- Dependency order between tasks
- Which tasks can run in parallel
- Estimated complexity flags for risky areas

## Integration with Kodo

**Before writing the plan:**
```bash
kodo query "similar features"     # Check existing patterns
kodo query "testing patterns"     # Check test conventions
```

**After writing the plan:**
```bash
kodo track issue "Implement <feature>"  # Create GitHub issue
kodo track link #123                     # Link to existing issue
```

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan saved to `docs/plans/<filename>.md`. Two execution options:**

1. **Continue in this session** - Execute tasks one-by-one with checkpoints
2. **Parallel session** - Open new session with `kodo:execute` skill

**Which approach?"**

**If continuing:**
- Use `kodo:execute` skill
- Stay in this session
- Execute in batches with review checkpoints

**If parallel session:**
- Guide user to open new Claude session
- Point to plan file location
- New session uses `kodo:execute` skill

## Key Principles

- **Exact file paths** - No ambiguity about where code goes
- **Complete code** - Copy-paste ready, not "add appropriate logic"
- **Test-first always** - Every task starts with failing test
- **Frequent commits** - One commit per task minimum
- **YAGNI ruthlessly** - Remove anything not strictly needed

## Red Flags

**You're doing it wrong if:**
- Tasks take more than 5 minutes
- Steps say "implement" without showing exact code
- File paths are relative or vague
- Tests come after implementation
- Plan has no commit checkpoints
- Skipping `kodo query` to check existing patterns
