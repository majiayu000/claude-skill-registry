---
name: task-workflow
description: '> Note: This skill has been adapted from claude-skillz'
---

---
name: Lightweight Task Workflow
description: FOLLOW THE STATE MACHINE IN SKILL.MD. When user says 'continue': (1) FIRST: Run pwd, (2) Announce STATE: CHECK_STATUS, (3) Read .claude/session.md to check Status field, (4) Route based on Status. NEVER auto-advance tasks. NEVER use TodoWrite. NEVER create git commits.
---

# GitHub Copilot Skill: task-workflow

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz)
> for use with GitHub Copilot Agent Skills.

---

# Lightweight Task Workflow

**🚨 CRITICAL: YOU MUST FOLLOW THE STATE MACHINE BELOW 🚨**

**🚨 EVERY SINGLE MESSAGE MUST START WITH: `🔵 STATE: [STATE_NAME]` 🚨**

NOT JUST THE FIRST MESSAGE. EVERY. SINGLE. MESSAGE.

When you read a file - prefix with state.
When you run a command - prefix with state.
When you explain something - prefix with state.
When you ask a question - prefix with state.

Example:
```
🔵 STATE: WORKING
Reading requirements.md...

🔵 STATE: WORKING
I can see the requirements specify...

🔵 STATE: WORKING
Now running tests...

🔵 STATE: WORKING
Test results show...
```

This skill is a persistent todo list based on 3 files in `.github/`: `tasks.md` (checklist), `requirements.md` (specs), `session.md` (current state).

When user says "continue", you MUST:
1. Run `pwd` to check current working directory
2. Announce `🔵 STATE: CHECK_STATUS`
3. Read `.github/session.md` from the current project directory
4. Follow the state machine below based on the Status field

**STATE MACHINE:**

```
                         user: "continue"
                                ↓
                       ┌────────────────┐
                   ┌───│ CHECK_STATUS   │←──────────┬──────────┐
                   │   │ Read session.md│           │          │
                   │   └────────┬───────┘           │          │
                   │            │                   │          │
        Status=    │            │ Status=           │          │
        "Complete" │            │ "in progress"     │          │
                   │            │                   │          │
                   ↓            ↓                   │          │
           ┌───────────┐  ┌──────────────┐         │          │
           │ AWAITING_ │  │ WORKING      │←────┐   │          │
           │ COMMIT    │  │              │     │   │          │
           │           │  │ Read:        │     │   │          │
           │ Ask       │  │ requirements │     │   │          │
           │ permission│  │ tasks.md     │     │   │          │
           │ STOP      │  │              │     │   │          │
           └─────┬─────┘  │ Write:       │     │   │          │
                 │        │ session.md   │     │   │          │
       user: yes │        └──────┬───────┘     │   │          │
                 │               │             │   │          │
                 │               │ task done   │   │          │
                 │               │             │   │          │
                 │               ↓             │   │          │
                 │        ┌──────────────┐     │   │          │
                 │        │ VERIFY       │     │   │          │
                 │        │              │     │   │          │
                 │        │ Run steps    │     │   │          │
                 │        │ from         │─────┘   │          │
                 │        │ requirements │ fail    │          │
                 │        └──────┬───────┘         │          │
                 │               │                 │          │
                 │               │ pass            │          │
                 │               │                 │          │
                 │               ↓                 │          │
                 │        ┌──────────────┐         │          │
                 │        │ COMPLETE     │         │          │
                 │        │              │         │          │
                 │        │ Write:       │         │          │
                 │        │ session.md   │         │          │
                 │        │ Status=      │─────────┘          │
                 │        │ "Complete"   │                    │
                 │        └──────────────┘                    │
                 │                                            │
                 ↓                                            │
           ┌──────────────────┐                              │
           │ MARK_TASK_       │                              │
           │ COMPLETE         │                              │
           │                  │                              │
           │ Write: tasks [x] │                              │
           │ Write: session.md│──────────────────────────────┘
           │ (next task)      │
           └──────────────────┘
```

**🚨 STATE DEFINITIONS - FOLLOW EXACTLY 🚨**

**CHECK_STATUS:**
```
ACTIONS:
1. Run pwd
2. Read .github/session.md
3. Look at Status field
4. IF Status="Complete" OR "ready to commit" → Go to AWAITING_COMMIT
5. IF Status="in progress" OR missing → Go to WORKING

DO NOT: Read other files, launch agents, do anything except route
IF ERROR: STOP and tell user what failed
```

**AWAITING_COMMIT:**
```
ACTIONS:
1. Say: "Task X is complete. May I mark Task X as complete in tasks.md?"
2. STOP - wait for user response
3. IF user says yes → Go to MARK_TASK_COMPLETE
4. IF user says no → STOP, await further instruction

DO NOT: Read files, launch agents, work on next task, do anything except ask permission and STOP
IF ERROR: STOP and tell user what failed
```

**MARK_TASK_COMPLETE:**
```
ACTIONS:
1. Write tasks.md: Change [ ] to [x] for current task
2. Write session.md: Update to next task with Status="in progress"
3. Go to CHECK_STATUS

DO NOT: Read other files, launch agents, research next task
IF ERROR (e.g., plan mode, can't write): Say "I cannot edit files: [reason]" and STOP
NEVER try alternative actions if write fails
```

**WORKING:**
```
REMINDER: EVERY message in this state must start with: 🔵 STATE: WORKING

ACTIONS:
1. Read requirements.md
2. Read tasks.md
3. Work on current task
4. Update session.md after TDD cycles
5. When task done → Go to VERIFY

EVERY message you send while WORKING must have the state prefix.
When you read a file → prefix with state
When you run tests → prefix with state
When you explain results → prefix with state

DO NOT: Skip to next task, work on multiple tasks
IF ERROR: Document in session.md as blocker, STOP
```

**VERIFY:**
```
REMINDER: EVERY message in this state must start with: 🔵 STATE: VERIFY

ACTIONS:
1. Read Verification section from requirements.md
2. Run all verification commands
3. IF all pass → Go to COMPLETE
4. IF any fail → Go to WORKING (treat as blocker)

EVERY message you send while VERIFYING must have the state prefix.

DO NOT: Skip verification, claim complete without running checks
IF ERROR running verification: STOP and tell user
```

**COMPLETE:**
```
ACTIONS:
1. Write session.md: Set Status="Complete"
2. Go to CHECK_STATUS

DO NOT: Read files, launch agents, ask permission (that happens in AWAITING_COMMIT)
IF ERROR writing: STOP and tell user
```

**CRITICAL: State Announcements**

**ALL messages MUST be prefixed with your current state.**

Format:
```
**🔵 STATE: [STATE_NAME]**

[Your message here]
```

When transitioning:
```
**🟢 TRANSITION: [STATE_A] → [STATE_B]**
```

Example:
```
**🔵 STATE: CHECK_STATUS**

Reading session.md to check current task status...

**🟢 TRANSITION: CHECK_STATUS → AWAITING_COMMIT**

**🔵 STATE: AWAITING_COMMIT**

Task 2 is complete and ready for you to commit. May I mark Task 2 as complete in tasks.md?
```

## When to Use This Skill

Activate when the user:
- Says "create a plan", "setup tasks", "new task list"
- Says "continue", "continue plan", "resume work", "where were we"
- Is working on multi-step projects that span multiple sessions

## ⚠️ CRITICAL: Task Management System

**THIS SKILL REPLACES GitHub Copilot's built-in task tracking functionality.**

**NEVER use the following tools:**
- ❌ task tracking
- ❌ task tracking
- ❌ Any built-in todo/task tracking features

**ALWAYS use this skill's files instead:**
- ✅ `.github/tasks.md` for task checklists
- ✅ `.github/requirements.md` for plans and implementation specs
- ✅ `.github/session.md` for session context and recovery

**Why this matters:** Using task tracking creates workflow conflicts. The built-in todo system stores tasks in internal state (not visible as files), causing the plan to be lost in chat history instead of persisted in `.github/requirements.md`. This prevents session continuity and defeats the purpose of this skill.

**If you find yourself wanting to use task tracking, STOP and use this skill's files instead.**

## Files This Skill Manages

**IMPORTANT PATH GUIDANCE:**
- This skill's definition files (SKILL.md, CLAUDE.md, README.md) live in `~/.github/skills/lightweight-task-workflow/`
- The task files are created in **THE PROJECT'S .github/ directory**, NOT the skill directory
- Example: If working on project `<project-root>/`, task files go in `<project-root>/.github/`
- Always use **relative paths** from the project root: `./.github/tasks.md`, `./.github/requirements.md`, `./.github/session.md`
- NEVER read from `~/.github/skills/lightweight-task-workflow/tasks.md` (that's the skill directory, not the project directory)

**`.github/tasks.md`** - the task checklist (in the PROJECT directory)
```markdown
- [ ] Task 1: Extract UserService
- [x] Task 2: Add tests
```

**`.github/requirements.md`** - implementation specs and guidelines
```markdown
## Global Guidelines
- Preserve existing API contracts - no breaking changes
- Add logging for error cases
- Follow repository's existing code style

## Verification & Definition of Done
Before marking any task complete, the following must pass:
- `npm test` - all tests must pass
- `npm run lint` - no lint errors
- `npm run build` - build must succeed

## Task 1: Extract UserService
- Move all user-related methods from AppService to new UserService
- Keep existing method signatures for backward compatibility
- Update dependency injection in app.module.ts

## Task 2: Add tests
- Cover happy path and error cases
- Include edge cases for null/undefined inputs
- Mock external dependencies
```

**`.github/session.md`** - session recovery context
```markdown
**Current Task:** Task 3
**Status:** in progress

## What's Done
- Task 1: Extracted UserService (commit a1b2c3d)
- Task 2: Added tests (commit e4f5g6h)

## Next Steps
1. Finish Task 3: Update documentation

## Context
- Using yarn for builds
- Commands: ./verify.sh
```

## Behavior

### When User Says "Create a Plan" or "Setup Tasks"

**FIRST: Remember you are NOT using task tracking. Use this skill's .github/ files exclusively.**

1. Ask user to describe their tasks
2. Ask user about implementation approach:
   - "What requirements or guidelines should I know for implementing these tasks?"
   - "Are there testing/quality standards I should follow?"
   - "Any architectural constraints or patterns to follow?"
   - **"What verification must pass before marking a task complete?"** (e.g., npm test, ./verify.sh, build, lint, manual review)
   - Capture their answers - these become the implementation specs
3. Create `.github/tasks.md` with numbered checklist - format: `- [ ] Task 1: [exact user wording]`, `- [ ] Task 2: [exact user wording]`, etc.
4. Create `.github/requirements.md` with:
   - Global Guidelines section (testing, commands, patterns)
   - **Verification & Definition of Done section** (commands/checks that must pass)
   - Per-task requirements (one section per task with specs)
5. Create `.github/session.md` initialized to Task 1 with Status="in progress"
6. Confirm setup complete

**After setup:** You enter the state machine at CHECK_STATUS with session.md showing Task 1 Status="in progress"

### When User Says "Continue" or "Resume"

**Start at CHECK_STATUS state:** Read session.md and route based on Status field. Follow the state machine at the top of this file.

## What to Track in requirements.md

**Include:** Global guidelines, Verification & Definition of Done (user can edit anytime), per-task requirements, learnings/edge cases discovered.

**NOT for:** Progress notes, debugging notes, code changes (that's git).

## What to Track in session.md

**Update at 4 triggers:** (1) Start task, (2) End of TDD cycle (one line), (3) Hit blocker, (4) Complete task.

**Include:** Current task/status, completed tasks with commits, brief progress notes, blockers, next steps.

**NOT for:** Every change, file paths, verbose explanations.

## Anti-Patterns: What NOT to Do

### ❌ WRONG: Investigating Codebase to Figure Out Progress
```
User: "continue"
Claude: *Reads tasks.md*
Claude: "Let me investigate the codebase to understand what's already been done"
Claude: *Searches through 10+ files, runs git log, checks test files*
Claude: *Wastes 2 minutes and 5000 tokens figuring out current state*
Claude: "I can see Task 1 was completed, let me start on Task 2..."
```
**Problem:** Wasted time and tokens. All that information was already in session.md.

### ✅ RIGHT: Reading session.md to Know Current State
```
User: "continue"
Claude: *Runs pwd*
Claude: "🔵 STATE: CHECK_STATUS"
Claude: *Reads session.md FIRST*
Claude: "Status shows 'in progress'. Routing to WORKING."
Claude: "🟢 TRANSITION: CHECK_STATUS → WORKING"
Claude: "🔵 STATE: WORKING"
Claude: "Continuing Task 2: Add email validation..."
```
**Result:** Instant context, no wasted time, exactly where to resume. That's the whole point of session.md.

### ❌ WRONG: Skipping Verification
```
Claude: *Completes task implementation*
Claude: "Task 1 is complete and ready for you to commit"
Claude: "May I mark this task as complete?"
*User commits and deploys*
*Build breaks in CI - test failures, lint errors discovered*
```
**Problem:** Introduced regressions, broken build, wasted time debugging issues that should have been caught before claiming "complete."

### ✅ RIGHT: Running Verification Before Completion
```
Claude: *Completes task implementation*
Claude: *Reads requirements.md Verification section*
Claude: *Runs npm test* → All pass ✅
Claude: *Runs npm run lint* → All pass ✅
Claude: *Runs npm run build* → Success ✅
Claude: *Updates session.md: "Task 1 complete - all verification passed"*
Claude: "Task 1 is complete, all verification passed (tests/lint/build), ready for you to commit"
```
**Result:** Confidence that task is truly complete, no regressions introduced, ready for production.

### ❌ WRONG: Creating Git Commits
```
Claude: *Completes task implementation*
Claude: *Runs git add .*
Claude: *Runs git commit -m "Add UTF-8 correction table"*
Claude: "I've committed the changes"
```
**Problem:** User loses control over commits - can't review changes, adjust commit message, or stage selectively.

### ✅ RIGHT: Handing Off for User to Commit
```
Claude: *Completes task implementation*
Claude: *Updates .github/session.md: "Task 1 complete - UTF-8 correction ready for commit"*
Claude: "Task 1 is complete and ready for you to commit. The changes include..."
Claude: "May I mark this task as complete in tasks.md?"
```
**Result:** User reviews changes, creates commit with their preferred message and staging, maintains full git control.

### ❌ WRONG: Auto-Advancing to Next Task
```
Claude: "Task 1 is complete, verification passed, ready for you to commit"
Claude: "May I mark this task as complete?"
Claude: "Let me explore the codebase to understand Task 2: Add email validation..."
Claude: *Launches Plan agent for Task 2*
```
**Problem:** User doesn't have time to review Task 1, commit changes, or decide when to proceed. Claude rushes ahead without permission.

### ✅ RIGHT: Stopping After Task Complete
```
Claude: "Task 1 is complete, verification passed, ready for you to commit"
Claude: "May I mark this task as complete in tasks.md?"
Claude: *Waits for user response*
User: *Reviews changes, creates commit*
User: "continue"
Claude: *Reads session.md, sees Status="Complete", routes to AWAITING_COMMIT*
Claude: "Task 1 is complete. May I mark it [x]?"
User: "yes"
Claude: *Updates tasks.md, updates session.md to Task 2 Status="in progress"*
User: "continue"
Claude: *Reads session.md, sees Task 2 Status="in progress", routes to WORKING*
```
**Result:** User controls the pace, reviews and commits when ready, decides when to proceed to next task.

## Troubleshooting: Common Path Mistakes

**Symptom:** "Error reading file" when trying to continue tasks

**Likely cause:** You're looking in the skill directory instead of the project directory

**Fix:**
1. Run `pwd` to check current working directory
2. Look for `.github/` subdirectory in the project root
3. Read from `./.github/tasks.md`, NOT `~/.github/skills/lightweight-task-workflow/tasks.md`
4. Remember: skill definition ≠ task files

**Example:**
- ❌ WRONG: Reading `~/.github/skills/lightweight-task-workflow/tasks.md` (skill directory)
- ✅ RIGHT: Reading `./.github/tasks.md` or `<project-root>/.github/tasks.md` (project directory)

## Important Rules

- **ALWAYS prefix EVERY SINGLE MESSAGE with your state** - Not just when entering a state. EVERY message. When you read a file, when you run a command, when you explain something - ALL messages start with `🔵 STATE: [STATE_NAME]`
- **ALWAYS run pwd first** - Check current working directory before reading files
- **ALWAYS follow the state machine** - Start at CHECK_STATUS, route based on Status field from session.md
- **NEVER use task tracking, task tracking, or GitHub Copilot's built-in todo features** - This skill replaces them entirely
- **NEVER create git commits** - User handles all commits
- **NEVER auto-advance to next task** - STOP and wait for user
- **ALWAYS run verification from requirements.md before claiming complete**
- **ALWAYS read task files from PROJECT's `.github/` directory**, not skill directory
- Preserve user's exact wording when creating tasks
- Always ask permission before marking tasks complete
- Update requirements.md when discovering new constraints
