---
description: Create comprehensive implementation plans for complex, multi-component
  tasks (>30 min, multiple files/modules, or >5 distinct steps). Breaks work into
  bite-sized tasks following TDD, DRY, YAGNI principles. After plan creation, execute
  using subagent-driven-development. For simple single-feature implementations, skip
  planning and use test-driven-development directly.
name: writing-plans
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase and limited domain knowledge. Document everything they need to know: which files to touch for each task, code samples, testing approach, relevant documentation to check, and verification steps. Structure the work as bite-sized, actionable tasks following engineering best practices: DRY, YAGNI, TDD, and frequent commits.

Assume a skilled developer who knows the programming language but has minimal familiarity with the specific toolset, frameworks, or problem domain. Provide sufficient guidance for test design and architecture decisions.

**Announce at start:** "Creating a comprehensive implementation plan."

**Context:** Ideally run in a dedicated branch or worktree for isolated development.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan should start with this header:**

```markdown

# [Feature Name] Implementation Plan

> **Note:** This plan should be executed task-by-task with verification at each step.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach and key design decisions]

**Tech Stack:** [Key technologies, frameworks, and libraries used]

**Prerequisites:** [Development environment, tools, or dependencies needed]

---
```

## Task Structure

```markdown

### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ext`
- Modify: `exact/path/to/existing.ext:123-145`
- Test: `tests/exact/path/to/test_file.ext`

**Step 1: Write the failing test**

```language
[Test code following project's testing framework conventions]
// Follow the Arrange-Act-Assert pattern:
test_specific_behavior() {
    // Arrange: Set up test data and prerequisites
    input = setup_test_data()
    
    // Act: Execute the function under test
    result = function(input)
    
    // Assert: Verify the expected outcome
    assert(result == expected)
}
```

**Step 2: Run test to verify it fails**

Run: `[test command with specific test selector]`
Expected: FAIL with "[expected error message]"

**Step 3: Write minimal implementation**

```language
[Minimal code that makes the test pass]
// Example:
function(input) {
    return expected
}
```

**Step 4: Run test to verify it passes**

Run: `[test command with specific test selector]`
Expected: PASS

**Step 5: Commit**

```bash
git add [list of modified files]
git commit -m "[conventional commit format: type: description]"
```
```

## Language-Specific Adaptations

**For Python projects:**
- Test files: `test_*.py` or `*_test.py`
- Test runner: `pytest`, `unittest`, or `nose2`
- Example: `pytest tests/path/test_module.py::test_function -v`

**For C# projects:**
- Test files: `*.Tests.cs` or `*Tests.cs`
- Test runner: `dotnet test`, `xUnit`, `NUnit`, or `MSTest`
- Example: `dotnet test --filter "FullyQualifiedName~ClassName.TestMethod"`

**For TypeScript/Node.js projects:**
- Test files: `*.test.ts`, `*.spec.ts`, or `*.test.js`
- Test runner: `jest`, `mocha`, `vitest`, or `node:test`
- Example: `npm test -- --testNamePattern="specific test"`

**For JavaScript projects:**
- Test files: `*.test.js` or `*.spec.js`
- Test runner: `jest`, `mocha`, `vitest`, or `node --test`
- Example: `npm test -- "path/to/test.js"`

## Remember
- Exact file paths always (use project conventions)
- Complete code in plan (avoid placeholders like "add validation")
- Exact commands with expected output
- Adapt test commands to project's testing framework
- Follow language-specific naming conventions
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, provide execution guidance:

**"Implementation plan saved to `docs/plans/<filename>.md`."**

**Execution options:**

**1. Interactive execution** - Work through tasks step-by-step with verification and adjustments as needed

**2. Automated execution** - Batch process tasks with checkpoints for review

**3. Manual execution** - Use the plan as a guide for self-directed implementation

Choose the approach that best fits your workflow and the complexity of the changes.

---

## Related Skills

**Followed by:**
- **subagent-driven-development**: Executes plans created by this skill

**References:**
- **test-driven-development**: Plans structure tasks following TDD methodology
- **senior-software-developer**: Plans reference language-specific patterns

**When to use:**
- Complex multi-component work (>30 min, multiple files, >5 steps)
- Requires architectural planning
- User provides spec/requirements for multi-step task

**When NOT to use:**
- Simple single-feature implementations (<30 min, single file, <5 steps)
- Trivial changes or quick fixes
- For simple tasks, use **test-driven-development** directly instead
