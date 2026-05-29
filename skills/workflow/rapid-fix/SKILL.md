---
name: rapid-fix
description: Rapid bug fix workflow - auto-plan, execute, test, and close simple fixes in one command. Use for simple bug fixes, one-line changes, minor validation issues.
---

# SKILL: Rapid Fix (Rapid Bug Fix Workflow)

> **Purpose**: Automated planning, execution, and closure for simple bug fixes in one command
> **Target**: Coder Agent fixing simple bugs (1-3 SCs)

---

## Quick Start

### When to Use This Skill
- One-line fixes (typos, simple validation)
- Minor bug fixes (null pointer, off-by-one)
- Simple validation additions
- Formatting issues

### When NOT to Use
- Features or architecture changes
- Multi-file refactors
- Design changes
→ Use `/00_plan` for complex tasks

---

## What This Skill Covers

### In Scope
- Scope validation (complexity score algorithm)
- Auto-generation of minimal plans (1-3 SCs)
- Direct execution via Coder agent with TDD + Ralph Loop
- User confirmation before commit
- Commit with Co-Authored-By attribution

### Out of Scope
- Full planning methodology → `/00_plan` command
- TDD cycle execution → @.claude/skills/tdd/SKILL.md
- Ralph Loop iteration → @.claude/skills/ralph-loop/SKILL.md
- Manual plan closure → `/03_close` command

---

## Execution Steps

---

## ⛔ MAIN ORCHESTRATOR RESTRICTIONS (ABSOLUTE)

**FORBIDDEN** (orchestrator direct use prohibited):
- Direct code modification without Task tool
- Direct fix verification without agent delegation

**MANDATORY** (must delegate via Task tool):
- Step 1 scope validation: `Task: subagent_type: researcher` (verify classification)
- Step 3 fix execution: `Task: subagent_type: coder`
- Step 4 diff verification: `Task: subagent_type: validator` (before user confirmation)
- Step 6 completion check: `Task: subagent_type: validator`

**TRIVIAL EXCEPTIONS** (no delegation needed):
- Complexity score calculation, plan file creation, git diff display, user prompts

**WHY**: Subagent isolation provides 50-80% context savings (CLAUDE.md:58-59)

---

### Step 1: Validate Scope
**Goal**: Reject complex tasks that belong in `/00_plan`

Check for complexity keywords: `feature`, `architecture`, `refactor`, `design`
If detected → Reject with suggestion to use `/00_plan`

### Step 2: Create Mini-Plan
**Goal**: Generate minimal plan (1-3 SCs) with absolute path

Create plan file at `.pilot/plan/draft/{TIMESTAMP}_rapid_fix.md` with:
- Success Criteria (SC-1, SC-2, SC-3)
- PRP Analysis (What/Why/How)
- Test Plan
- Quality Gates

### Step 3: Execute Fix
**Goal**: Invoke Coder agent with TDD + Ralph Loop

Analyze bug type (frontend/backend/general) and invoke appropriate agent with:
- TDD cycle (Red-Green-Refactor)
- Ralph Loop (autonomous iteration)
- Quality gates (tests, type-check, lint, coverage ≥80%)

Wait for completion marker: `<CODER_COMPLETE>` or `<CODER_BLOCKED>`

### Step 4: Show Diff & Confirm
**Goal**: Show user the changes and get approval

Display `git diff` and prompt user (y/N):
- If approved → Proceed to Step 5
- If not approved → Preserve plan and changes

### Step 5: Commit Changes
**Goal**: Commit with conventional commit message and Co-Authored-By

Create commit: `fix: {BUG_DESCRIPTION}\n\nCo-Authored-By: Claude <noreply@anthropic.com>`

---

## Core Concepts

### Scope Validation Algorithm

**Complexity Keywords**: `feature`, `architecture`, `refactor`, `design`

**Rationale**: Rapid fix is for simple bugs (≤3 SCs, ≤20 minutes)

### Auto-Generated Plan Structure

**Minimal plan** (1-3 SCs):
- SC-1: Analyze bug and identify root cause
- SC-2: Implement fix with test coverage
- SC-3: Verify fix and close with commit

**Estimated time**: 20 minutes total

### Execution Integration

**Invokes Coder agent directly** with TDD + Ralph Loop

### User Confirmation Flow

**Before commit**:
1. Show `git diff` to user
2. Prompt for approval (y/N)
3. If approved: Commit with Co-Authored-By
4. If not approved: Preserve plan and changes

---

## Further Reading

**Internal**: @.claude/skills/rapid-fix/REFERENCE.md - Detailed algorithm, rejection criteria, continuation workflow, error handling | @.claude/skills/tdd/SKILL.md - Red-Green-Refactor cycle | @.claude/skills/ralph-loop/SKILL.md - Autonomous completion loop | @.claude/skills/vibe-coding/SKILL.md - Code quality standards | @.claude/skills/git-master/SKILL.md - Git operations

**External**: [Working Effectively with Legacy Code by Michael Feathers](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052) | [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
