---
name: session-state-manager
description: Persistently stores conversation state, decisions, and progress to allow seamless resume across sessions.
---

# Session State Manager

## Purpose
This skill prevents loss of context across sessions, restarts, or Claude limits by automatically saving state after every significant interaction.

## What to Persist
Persist continuously:
- Last completed phase
- Current active phase
- Decisions made
- Approved specs
- Pending tasks
- Last user instruction
- Next recommended action
- Files created/modified
- Commands executed
- Current branch

## Auto-Save Triggers (MANDATORY)
Automatically save state after:
1. **Every user message** - Update last instruction
2. **File creation/modification** - Log changed files
3. **Phase completion** - Mark phase as done
4. **Skill execution** (/sp.specify, /sp.plan, /sp.tasks, /sp.implement)
5. **Git operations** - Track branch and commits
6. **Major decisions** - Document choices made

## Save Strategy
- **Append-only log** at `.claude/state/session.md`
- **Timestamped entries** (ISO 8601 format)
- **Structured format**:
  ```markdown
  ## [TIMESTAMP] - [ACTION]
  - Phase: [Current Phase]
  - Status: [Status Message]
  - Files: [Modified Files]
  - Next: [Next Action]
  ---
  ```
- **Minimal but sufficient context** - No huge dumps

## Load Strategy (MANDATORY)
At session start or when user says "resume":
1. Check `.claude/state/session.md`
2. Load last known state (most recent entry)
3. Resume from exact stopping point
4. Briefly summarize:
   "Resuming from Phase X, step Y - Last action: Z"
5. Continue seamlessly

## Implementation (Auto-Execute)
After EVERY significant action, append to `.claude/state/session.md`:

```markdown
## [ISO-TIMESTAMP] - [Brief Action Description]
- **Phase**: Phase I - Python Console App (or current phase)
- **Status**: [What was just completed]
- **Branch**: [Current git branch]
- **Files Modified**: [List of files]
- **User Instruction**: "[Last thing user said]"
- **Next Action**: [What should happen next]
---
```

**Example Entry**:
```markdown
## 2025-12-27T15:30:00Z - Interactive CLI Created
- **Phase**: Phase I - Python Console App
- **Status**: Added colorful interactive menu with ANSI colors
- **Branch**: 001-console-todo
- **Files Modified**: src/todo_app/interactive.py, src/todo_app/__main__.py
- **User Instruction**: "mughy colorful cli chahiye"
- **Next Action**: Test interactive CLI and update session state
---
```

## Safety Rules
- Never hallucinate missing state
- If state file missing, create fresh with current state
- Never overwrite state history (append-only)
- Keep entries concise (max 10 lines per entry)
- Rotate file if > 1000 lines (move to session-archive.md)

## Auto-Execution Rule (CRITICAL)
This skill should run **automatically** without user asking:
- After every `/sp.*` skill completion
- After file modifications (Write, Edit tools)
- After user provides new instruction
- Before responding to "resume" command

**DO NOT wait for user to say "/session" - AUTO-SAVE ALWAYS!**

This skill ensures continuity and fast recovery.
