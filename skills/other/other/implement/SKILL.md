---
name: implement
description: "Execute implementation workflow phase by phase. Use after analysis passes. Triggers on: start implementation, implement feature, begin coding."
---

# Implementation Workflow Executor

Guide systematic implementation of features using TDD and quality-first approach.

> **Note:** This skill uses generic placeholders. Adapt commands and paths to your project:
> - Quality commands: Check your `package.json`, `Makefile`, or build config
> - File paths: Adjust based on your project structure
> - Examples show common conventions - your project may differ

---

## SpecKit Workflow

This skill is **Step 6 of 6** in the Relentless workflow:

specify → plan → tasks → convert → analyze → **implement**

Prerequisites:
- `spec.md` - Feature specification
- `plan.md` - Technical implementation plan
- `tasks.md` - User stories with acceptance criteria
- `prd.json` - Converted PRD with routing metadata
- `checklist.md` - Quality validation checklist
- Analysis must PASS (run `/relentless.analyze` first)

---

## The Job

Implement user stories one at a time, following strict TDD and updating all tracking files.

---

## Before You Start

1. **Read the Constitution** - Review your project's constitution (if exists) for governance principles
2. **Read prompt.md** - Review workflow guidelines (if exists)
3. **Read progress.txt** - Check learnings from previous iterations
4. **Review artifacts** - Ensure spec.md, plan.md, tasks.md, prd.json, checklist.md exist
5. **Verify Analysis Passed** - Run `/relentless.analyze` if not already done
6. **Identify Quality Commands** - Find your project's typecheck, lint, and test commands
7. **Check Branch** - Verify you're on the correct branch from PRD `branchName`

---

## CRITICAL: Quality Gates (Non-Negotiable)

Before marking ANY story as complete, ALL quality checks must pass.

**Find your project's commands** (examples for different ecosystems):

```bash
# JavaScript/TypeScript (npm/yarn/bun/pnpm):
npm run typecheck && npm run lint && npm test

# Python:
mypy . && ruff check . && pytest

# Go:
go build ./... && golangci-lint run && go test ./...

# Rust:
cargo check && cargo clippy && cargo test
```

**Requirements:**
- Typecheck: 0 errors
- Lint: 0 errors AND 0 warnings
- Tests: All pass

**If ANY check fails, DO NOT mark the story as complete. Fix the issues first.**

---

## TDD Workflow (MANDATORY)

For EVERY story, follow strict Test-Driven Development:

### Step 1: Write Failing Tests First (RED)
```bash
# Create test file if needed
# Write tests that define expected behavior
# Run your test command - tests MUST fail initially
```

### Step 2: Implement Minimum Code (GREEN)
```bash
# Write only enough code to pass tests
# Run tests - they MUST pass now
```

### Step 3: Refactor
```bash
# Clean up while keeping tests green
# Run tests - they MUST still pass
```

**Do NOT skip TDD. Tests are contracts that validate your implementation.**

---

## Research Phase (if story has `research: true`)

If the current story has `research: true` in prd.json and no research file exists yet:

1. **Explore the codebase** - Find relevant files, patterns, and dependencies
2. **Document findings** in `relentless/features/<feature>/research/<story-id>.md`:
   - Existing patterns that should be followed
   - Files that will likely need modification
   - Dependencies and integration points
   - Potential gotchas or edge cases
   - Recommended implementation approach
3. **Do NOT implement** - only research and document
4. Save your findings to the research file and end your turn

---

## Per-Story Implementation Flow

For each story (in dependency order):

### 1. Identify the Story
- Read `prd.json` to find the next story where `passes: false`
- Check dependencies are met (dependent stories have `passes: true`)
- Read the story's acceptance criteria
- Check routing metadata (complexity, model assigned)

### 2. Find Relevant Checklist Items
- Open `checklist.md`
- Find items tagged with `[US-XXX]` for this story
- Note any governance/compliance items
- **Ensure Quality Gates and TDD items are included**

### 3. Implement with TDD
Follow the TDD workflow above for each acceptance criterion.

### 4. Update tasks.md
As you complete each criterion:
```markdown
# Change from:
- [ ] Criterion text

# To:
- [x] Criterion text
```

### 5. Update checklist.md
For each verified checklist item:
```markdown
# Change from:
- [ ] CHK-XXX [US-001] Description

# To:
- [x] CHK-XXX [US-001] Description
```

### 6. Run Quality Checks
```bash
# Run your project's quality commands
# All must pass with 0 errors/warnings
```

### 7. Commit Changes
```bash
git add -A
git commit -m "feat: US-XXX - Story Title"
```

### 8. Update prd.json
Set the story's `passes` field to `true`:
```json
{
  "id": "US-001",
  "title": "...",
  "passes": true,  // <- Change from false to true
  ...
}
```

### 9. Update progress.txt
Append progress entry:
```markdown
## [Date] - US-XXX: Story Title

**Implemented:**
- What was built
- Key decisions made

**Files Changed:**
- path/to/file (new/modified)

**Tests Added:**
- path/to/test.file

**Learnings:**
- Patterns discovered
- Gotchas encountered

**Constitution Compliance:**
- [list principles followed]

---
```

---

## Check for Queued Prompts

Between iterations, check `.queue.txt` for user input:

```bash
# If .queue.txt exists, read and process it
# Acknowledge in progress.txt
# Process in FIFO order
```

---

## File Update Summary

After completing each story, these files MUST be updated:

| File | Update |
|------|--------|
| `tasks.md` | Check off `- [x]` completed acceptance criteria |
| `checklist.md` | Check off `- [x]` verified checklist items |
| `prd.json` | Set `"passes": true` for the story |
| `progress.txt` | Append progress entry with learnings |

---

## Implementation Phases

### Phase 0: Setup
- Infrastructure, tooling, configuration
- Usually US-001 type stories

### Phase 1: Foundation
- Data models, types, schemas
- Base utilities and helpers
- Core infrastructure

### Phase 2: User Stories
- Feature implementation
- Follow dependency order strictly

### Phase 3: Polish
- E2E tests
- Documentation
- Performance optimization

---

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

**If ALL stories are complete and passing, output:**
```
<promise>COMPLETE</promise>
```

**If there are still stories with `passes: false`, end your response normally** (another iteration will pick up the next story).

---

## Common Pitfalls to Avoid

1. **Skipping TDD** - Never implement without tests first
2. **Suppressing lints** - Fix issues properly, don't disable rules
3. **Large commits** - Keep commits focused and atomic
4. **Missing typecheck** - Always run typecheck before commit
5. **Ignoring progress.txt** - Read learnings from previous iterations
6. **Not checking queue** - Always check `.queue.txt` for user input
7. **Skipping analysis** - Run `/relentless.analyze` before implementing
8. **Ignoring routing metadata** - Check story complexity and model assignment

---

## Notes

- Work on ONE story at a time
- Follow dependency order strictly
- Never skip TDD - tests come FIRST
- Never skip quality checks
- Commit after each story
- Update ALL tracking files
- Check `.queue.txt` for mid-run input
- This is a guided workflow for systematic implementation
- **Adapt all commands and paths to your project's specific setup**
