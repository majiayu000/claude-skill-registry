---
name: workflow
description: Complete 5-step development workflow
user-invocable: true
---

# Development Workflow

A structured approach to software development that emphasizes understanding, minimal implementation, testing, documentation, and clean commits.

---

## Overview

```
Step 1: Focus Problem    → Understand before coding
Step 2: Prevent Overdev  → Only build what's needed (YAGNI)
Step 3: Test First       → Red-Green-Refactor
Step 4: Document         → Keep it clear and current
Step 5: Smart Commit     → Conventional Commits
```

---

## Step 1: Focus Problem (`/focus-problem`)

**Goal:** Thoroughly understand the problem before writing code.

### Checklist
- [ ] What is the user need? (Who / What / Why)
- [ ] What defines success? (How to verify completion?)
- [ ] What are the boundaries? (What NOT to do?)
- [ ] What files/modules are affected?
- [ ] Is there existing similar functionality?

### Use Explore Agent
```markdown
Task(subagent_type="Explore", model="haiku", prompt="""
Explore the codebase for: [feature name] (thoroughness: medium)
Find related files, similar implementations, and test patterns.
""")
```

---

## Step 2: Prevent Overdev

**Goal:** Ensure minimal viable implementation (YAGNI principle).

### Red Flags
```
"We might need this later..." → Don't build it now
"Just in case..." → YAGNI
"Let's make it generic..." → Solve current problem only
"We should create a framework..." → Write concrete implementation
```

### Checklist
- [ ] Is there immediate need for this?
- [ ] Is this over-abstracted?
- [ ] Can this be simpler?
- [ ] Are we adding unnecessary dependencies?

---

## Step 3: Test First (`/test-first`)

**Goal:** Strict TDD (Red-Green-Refactor).

### Red Phase (Write Failing Test)
- [ ] Write a test for expected behavior
- [ ] Run test, confirm it fails
- [ ] Failure message clearly indicates the issue

### Green Phase (Minimal Implementation)
- [ ] Write minimum code to pass test
- [ ] Don't optimize yet
- [ ] Run test, confirm it passes

### Refactor Phase
- [ ] Clean up code (keep tests passing)
- [ ] Remove duplication
- [ ] Improve naming
- [ ] Simplify logic

---

## Step 4: Document

**Goal:** Ensure code is understandable.

### Checklist
- [ ] README describes purpose and usage
- [ ] Public APIs have docstrings
- [ ] Complex logic has comments explaining "why"
- [ ] No obvious-comment clutter

---

## Step 5: Smart Commit (`/smart-commit`)

**Goal:** Clean version history with Conventional Commits.

### Format
```
<type>(<scope>): <description>
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Code restructure

---

## Quick Start

```bash
# Run full workflow
/workflow

# Or individual steps
/focus-problem "implement user login"
/test-first
/smart-commit
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `/focus-problem` | Step 1: Problem analysis |
| `/test-first` | Step 3: TDD cycle |
| `/smart-commit` | Step 5: Create commit |
| `/plan` | Break down complex tasks |
