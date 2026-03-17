---
name: dev-session
description: "Manage long development sessions with structured progress tracking. Creates SESSION.md files for multi-session handoff, checkpoints progress with WIP commits, and captures learnings to CLAUDE.md. Trigger with 'start session', 'checkpoint', 'wrap session', 'resume session', or 'context getting full'."
compatibility: claude-code-only
---

# Dev Session

Manage multi-session development work with structured progress files, checkpoint commits, and durable learnings. Produces SESSION.md files that survive context compaction and enable clean handoff between sessions.

## Operating Modes

### Mode 1: Start Session

**When**: Beginning multi-step work, "start session", "new session for [feature]"

1. Check if `SESSION.md` already exists in the project root
   - If yes: read it and ask whether to **continue** the existing session or **start fresh**
   - If no: create from template (see [references/session-template.md](references/session-template.md))
2. Pre-fill fields:
   - **Project**: from CLAUDE.md or directory name
   - **Branch**: from `git branch --show-current`
   - **Last Updated**: current timestamp
   - **Phase**: ask user what they're working on
3. Read the project's CLAUDE.md to orient on context
4. Present a brief summary: "Session started. Working on [phase] on branch [branch]."

### Mode 2: Checkpoint

**When**: "checkpoint", major milestone reached, before risky changes, context getting large

1. Update SESSION.md:
   - Add completed items to **What Works**
   - Update **Current Position** with exact location (file paths, line numbers)
   - Clear resolved **Blockers**, add new ones
   - Write concrete **Resume Instructions**
2. Capture learnings:
   - If any patterns, gotchas, or commands were discovered during work, add them to CLAUDE.md
   - One line per concept — concise, not verbose
3. Git checkpoint:
   ```bash
   git add -A && git commit -m "WIP: [what was accomplished]"
   ```
4. Record the commit hash in SESSION.md under **Checkpoint**
5. Confirm: "Checkpointed at [hash]. SESSION.md updated."

### Mode 3: Resume Session

**When**: "resume", "continue from last session", "where were we", start of a new conversation

1. Read `SESSION.md` — if missing, inform user and offer to start a new session
2. Read the project's `CLAUDE.md` for context
3. Check what's changed since the recorded checkpoint:
   ```bash
   git log --oneline [checkpoint-hash]..HEAD
   ```
4. Check for uncommitted changes: `git status`
5. Present a summary:
   - **Phase**: what we were working on
   - **Position**: where we left off
   - **Changes since**: any commits or modifications since checkpoint
   - **Blockers**: anything unresolved
   - **Suggested next step**: first item from Resume Instructions

### Mode 4: Wrap Session

**When**: "wrap session", "done for now", "save progress", ending a session

1. Run a full checkpoint (Mode 2)
2. Review SESSION.md for completeness:
   - Are Resume Instructions concrete enough for a fresh session to continue?
   - Is Current Position specific (file paths, not vague descriptions)?
3. If the phase is complete:
   - Collapse the phase summary to 2-3 lines
   - Clear Resume Instructions or note "Phase complete — ready for next phase"
4. Confirm: "Session wrapped. Resume with 'resume session' next time."

## When to Use

| Scenario | Use this skill? |
|----------|----------------|
| Multi-phase feature spanning 2+ sessions | Yes |
| Work that might hit context compaction | Yes |
| Before making risky or destructive changes | Yes (checkpoint first) |
| Quick bug fix or single-file edit | No |
| Single-session task with clear scope | No |

## SESSION.md Principles

- **Track progress, not architecture** — SESSION.md is a work log, not project documentation
- **Concrete over vague** — "Resume at `src/auth.ts:42`, implement token refresh" beats "Continue auth work"
- **Collapse completed work** — finished phases become 1-2 line summaries
- **Keep under 100 lines** — if it's longer, collapse more aggressively

## Autonomy Rules

- **Just do it**: Read SESSION.md, read CLAUDE.md, check git status/log, present summaries
- **Brief confirmation**: Creating new SESSION.md, committing WIP checkpoints
- **Ask first**: Overwriting an existing SESSION.md, deleting session data

## Reference Files

| When | Read |
|------|------|
| Creating a new SESSION.md | [references/session-template.md](references/session-template.md) |
| Context compaction tips, what survives | [references/compaction-survival.md](references/compaction-survival.md) |
