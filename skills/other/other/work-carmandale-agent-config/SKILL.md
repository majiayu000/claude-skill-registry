---
name: work
description: Execute work plans efficiently while maintaining quality and shipping complete features. Use when implementing a plan, working through a todo list, or executing a specification. Focuses on finishing features, not perfecting process.
---

# Work Skill

Execute plans efficiently. Ship complete features.

## When to Use

- Implementing a plan from `plans/` directory
- Working through a specification or issue
- Executing a todo list
- Building a feature from start to finish

## Core Philosophy

**Ship complete features.** A finished feature that ships beats a perfect feature that doesn't.

- Get clarification once at the start, then execute
- Follow existing patterns—don't reinvent
- Test as you go, not at the end
- Quality is built in, not bolted on

---

## Workflow Overview

```
Plan/Spec Input
       │
       ▼
┌──────────────────┐
│  1. CLARIFY      │ ← Ask questions NOW, not later
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  2. SETUP        │ ← Branch, environment, task list
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  3. EXECUTE      │ ← Implement, test continuously
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. QUALITY      │ ← Lint, review, verify
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  5. SHIP         │ ← Commit, PR, done
└────────┬─────────┘
         │
         ▼
    Feature Live ✅
```

---

## Phase 1: Clarify

**Do not skip this phase.** Better to ask questions now than build the wrong thing.

### Read the Plan Completely

```bash
# Read the plan file
cat plans/<plan-file>.md

# Check for referenced files
# Load any files mentioned in "Files to Create/Modify"
```

### Ask Clarifying Questions

If anything is unclear or ambiguous:

1. List your questions
2. Wait for answers
3. Only then proceed

Common clarifications needed:
- Unclear acceptance criteria
- Missing technical details
- Ambiguous requirements
- Conflicting constraints

### Get Approval to Proceed

```markdown
## Ready to Start

**Plan**: [plan title]
**Scope**: [X files to create/modify]
**Estimated work**: [small/medium/large]

**My understanding**:
- [Key point 1]
- [Key point 2]

**Questions** (if any):
- [Question 1]

Ready to proceed?
```

---

## Phase 2: Setup

### Branch Strategy

**Option A: Direct branch** (simple, single-track work)

```bash
# Ensure clean state
git status
git checkout main && git pull origin main

# Create feature branch
git checkout -b feat/<feature-name>
```

**Option B: Worktree** (parallel work, complex features)

```bash
# Create isolated worktree
git worktree add .worktrees/<feature-name> -b feat/<feature-name>
cd .worktrees/<feature-name>
```

### Create Task List

Break the plan into actionable tasks:

```markdown
## Tasks

- [ ] Create `path/to/new/file.ext`
- [ ] Modify `path/to/existing.ext` - add X
- [ ] Write tests for X
- [ ] Update documentation
- [ ] Manual testing
```

Track progress by checking off tasks as you complete them.

### Verify Environment

```bash
# Dependencies installed?
# For Node: npm install / pnpm install
# For Ruby: bundle install
# For Python: pip install -r requirements.txt

# Can you build/run?
# Project-specific build command

# Tests passing before you start?
# Project-specific test command
```

---

## Phase 3: Execute

### The Implementation Loop

```
while tasks remain:
    1. Pick next task
    2. Find similar patterns in codebase
    3. Implement following those patterns
    4. Write/update tests
    5. Run tests
    6. Fix any failures immediately
    7. Mark task complete
    8. Commit if logical checkpoint
```

### Finding Patterns

Before implementing anything new, find existing examples:

```bash
# Find similar implementations
rg "class.*Service" --type ruby -l
rg "interface.*Props" --type ts -l
rg "def.*\(" --type python -l

# Look at how similar features are structured
ls app/services/ app/controllers/ src/components/

# Check imports/dependencies in similar files
head -30 path/to/similar/file.ext
```

**Follow existing patterns exactly.** Match:
- Naming conventions
- File organization
- Code style
- Error handling patterns
- Test structure

### Test Continuously

**Run tests after each significant change.** Don't wait until the end.

```bash
# Run relevant tests (project-specific)
# Rails: bin/rails test test/path/to/test.rb
# Jest: npm test -- path/to/test
# Pytest: pytest path/to/test.py

# Run full suite less frequently
# Only after completing a major piece
```

If tests fail:
1. **Stop immediately**
2. Fix the failure
3. Verify fix works
4. Then continue

### Commit Checkpoints

Commit at logical checkpoints:

```bash
# Stage changes
git add -A

# Review what you're committing
git status
git diff --staged

# Commit with conventional message
git commit -m "feat(scope): description

- Detail 1
- Detail 2"
```

Good commit points:
- Completed a task from the list
- Got a test passing
- Finished a logical unit of work
- Before making a risky change

---

## Phase 4: Quality Check

Before considering the work "done":

### Run All Checks

```bash
# Linting (project-specific)
# Rails: rubocop
# Node: npm run lint
# Python: ruff check .

# Type checking (if applicable)
# TypeScript: npx tsc --noEmit
# Python: mypy .

# Full test suite
# Project-specific test command

# Build (catches runtime issues)
# Project-specific build command
```

### Self-Review

Quick self-review checklist:

```bash
# Check for debug code
rg "console\.log|debugger|binding\.pry|print\(" $(git diff main --name-only)

# Check for TODOs you added
rg "TODO|FIXME" $(git diff main --name-only)

# Check diff size
git diff main --stat
```

### Verify Acceptance Criteria

Go through each acceptance criterion from the plan:

```markdown
## Acceptance Criteria Verification

- [x] Criterion 1 - verified by [how]
- [x] Criterion 2 - verified by [how]
- [ ] Criterion 3 - **NOT MET** - [what's missing]
```

If any criterion is not met, go back to Phase 3.

---

## Phase 5: Ship

### Final Commit

```bash
# Stage everything
git add -A

# Final review
git status
git diff --staged | head -100

# Commit
git commit -m "feat(scope): complete <feature>

- Implements <what>
- Adds tests for <what>
- Updates <what>

Closes #<issue-number>"
```

### Push and Create PR

```bash
# Push branch
git push -u origin feat/<feature-name>

# Create PR
gh pr create --title "feat: <title>" --body "## Summary
<what this does>

## Changes
- <change 1>
- <change 2>

## Testing
- <how tested>

## Checklist
- [x] Tests pass
- [x] Linting passes
- [x] Acceptance criteria met
- [x] Self-reviewed"
```

### Clean Up

If using worktree:

```bash
# Return to main repo
cd ..

# After PR is merged:
git worktree remove .worktrees/<feature-name>
git branch -d feat/<feature-name>
```

If using beads:

```bash
# Close the bead
bd close <bead-id> --reason "Merged in PR #X"
```

---

## Handling Problems

### Blocked by Unclear Requirements

1. Stop implementation
2. Document what's unclear
3. Ask for clarification
4. Wait for answer before continuing

### Tests Keep Failing

1. Stop and understand why
2. Check if you broke existing functionality
3. Check if your understanding is wrong
4. If stuck after 2 attempts, ask for help

### Scope Creep

If you notice the work is bigger than planned:

1. Finish the current task
2. Stop and report:
   - What's complete
   - What's remaining
   - What's larger than expected
3. Get guidance on whether to continue or split

### Stuck on Implementation

1. Re-read the plan for hints
2. Search codebase for similar patterns
3. Check framework documentation
4. If still stuck after 15 minutes, ask

---

## Quality Principles

### Do

- ✅ Follow existing patterns
- ✅ Test as you go
- ✅ Commit at checkpoints
- ✅ Ask questions early
- ✅ Ship complete features

### Don't

- ❌ Refactor unrelated code
- ❌ Add features not in the plan
- ❌ Skip tests to save time
- ❌ Guess at unclear requirements
- ❌ Leave work 80% done

---

## Checklist Before Calling Done

```markdown
## Completion Checklist

- [ ] All tasks from plan completed
- [ ] All acceptance criteria verified
- [ ] Tests written and passing
- [ ] Linting passes
- [ ] No debug code left
- [ ] Self-reviewed the diff
- [ ] Committed with good messages
- [ ] PR created with description
- [ ] Ready for review
```

Only when all boxes are checked is the work **done**.
