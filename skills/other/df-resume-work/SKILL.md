---
name: df:resume-work
description: |
  Resume work from previous session with full context restoration.
  Use when the user returns to continue work, wants to pick up where they left off, or starts a new session.
  Triggers on: "let's continue", "pick up where we left off", "resume", "what were we doing?", "where did we leave off?", "continue working"
allowed-tools:
  - Read
  - Bash
  - Write
  - AskUserQuestion
  - SlashCommand
---

<objective>
Restore complete project context and resume work seamlessly from previous session.

Routes to the resume-project workflow which handles:

- STATE.md loading (or reconstruction if missing)
- Checkpoint detection (.continue-here files)
- Incomplete work detection (JOB without SUMMARY)
- Status presentation
- Context-aware next action routing
  </objective>

<execution_context>
@~/.claude/devflow/workflows/resume-project.md
</execution_context>

<process>
**Follow the resume-project workflow** from `@~/.claude/devflow/workflows/resume-project.md`.

The workflow handles all resumption logic including:

1. Project existence verification
2. STATE.md loading or reconstruction
3. Checkpoint and incomplete work detection
4. Visual status presentation
5. Context-aware option offering (checks CONTEXT.md before suggesting plan vs discuss)
6. Routing to appropriate next command
7. Session continuity updates
   </process>
