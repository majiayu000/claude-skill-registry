---
name: obsidian-session-sync
description: |
  End-of-session ritual that syncs Claude Code session artifacts to an Obsidian
  vault. Chains breadcrumbs, retrospective, note creation, and daily driver
  into a single flow. Creates session notes, updates daily note, and leaves
  breadcrumbs. Activates on "sync to obsidian", "save session", "end session",
  or when user wraps up significant work in a vault-connected project.
allowed-tools: |
  bash: ls, find, cat, date, grep, obsidian-cli, obsidian
  file: read, write
---

# Obsidian Session Sync

<purpose>
You just spent an hour in Claude Code — built features, made decisions, discovered
things about the codebase. You close the terminal and all that context evaporates.
Your Obsidian vault has no idea what happened. This elixir chains together
breadcrumbs, retrospective, note creation, and daily logging into a single
end-of-session ritual that persists everything to your vault.
</purpose>

## When To Activate

<triggers>
- User says "sync to obsidian", "save session", "session sync"
- User says "end session", "wrap up", "I'm done for now"
- User says "save this to my vault"
- After completing significant work on a vault-connected project
- User explicitly asks to persist session artifacts
</triggers>

Do NOT trigger for:
- Quick one-off questions (nothing to sync)
- Sessions that didn't produce meaningful artifacts
- Vaults without CLAUDE.md (suggest obsidian-vault-init first)

## Instructions

### Step 1: Assess What Happened This Session

<assess>
Before syncing, inventory what this session produced:

```markdown
Session Assessment:

Files created:     [list new files]
Files modified:    [list changed files]
Decisions made:    [list key decisions]
Discoveries:       [things learned about the codebase]
Tasks completed:   [what was done]
Tasks remaining:   [what's left]
Dead ends:         [approaches that failed]
```

This drives what gets synced and where.
</assess>

### Step 2: Read Vault State

<vault_state>
Check the vault before writing anything:

```bash
# Read vault conventions
cat "$VAULT_PATH/CLAUDE.md"

# Read today's daily note
TODAY=$(date +%Y-%m-%d)
cat "$VAULT_PATH/Daily/$TODAY.md" 2>/dev/null

# Read existing breadcrumbs
cat "$VAULT_PATH/.claude/breadcrumbs.md" 2>/dev/null
# Or project-level breadcrumbs
cat .claude/breadcrumbs.md 2>/dev/null

# Check for existing session notes from today
find "$VAULT_PATH" -name "*$TODAY*session*" -o -name "*$TODAY*claude*" 2>/dev/null
```
</vault_state>

### Step 3: Create Session Note (uses [obsidian-note-create](../obsidian-note-create/SKILL.md))

<session_note>
Create a session note capturing the full context:

**Filename:** `YYYY-MM-DD-session-brief-topic.md`
**Location:** Project folder or Notes/

```markdown
---
type: session
project: [project-name]
date: YYYY-MM-DD
status: completed
tags:
  - session
  - claude-code
source: claude-session
---

# Session: [Brief Topic]

**Date:** YYYY-MM-DD
**Duration:** ~[estimate]
**Project:** [[project-name]]

## What We Did

[2-3 sentence summary]

## Changes Made

- [file1.py] — [what changed and why]
- [file2.py] — [what changed and why]

## Decisions

- **[Decision 1]:** [what was decided and why]
- **[Decision 2]:** [what was decided and why]

## Discoveries

- [Thing learned about codebase]
- [Unexpected finding]

## Failed Attempts

| Approach | Why It Failed |
|----------|--------------|
| [attempt 1] | [reason] |
| [attempt 2] | [reason] |

## Next Steps

- [ ] [Follow-up task 1]
- [ ] [Follow-up task 2]

## Links

- [[related-note-1]]
- [[related-note-2]]
- [[daily-note-link]]
```

Only create a session note if there's substance. A session that answered one
question doesn't need its own note — just log it in the daily note.
</session_note>

### Step 4: Update Daily Note (uses [obsidian-daily-driver](../obsidian-daily-driver/SKILL.md))

<update_daily>
Append session summary to today's daily note:

Under `## Log`:
```markdown
### Claude Session — HH:MM

**Worked on:** [brief description]
**Outcome:** [what was achieved]
**Session note:** [[YYYY-MM-DD-session-topic]]
**Created:**
- [[new-note-1]]
- [[new-note-2]]
**Next:**
- [ ] Follow-up task
```

Under `## Links`:
```markdown
- [[YYYY-MM-DD-session-topic]]
```

If no daily note exists, create one first.
</update_daily>

### Step 5: Write Breadcrumbs (uses [breadcrumbs](../breadcrumbs/SKILL.md))

<write_breadcrumbs>
Append to `.claude/breadcrumbs.md` (project-level):

```markdown
---
## YYYY-MM-DD — [Brief Topic]

**What we worked on:**
[1-2 sentence summary]

**What worked:**
- [approach that succeeded]

**What didn't work:**
- [approach that failed] — [why]

**Left off at:**
[current state, what's next]

**Vault notes:**
- [[YYYY-MM-DD-session-topic]] (session note)
- [[other-created-notes]]

**Notes for next time:**
- [important context for future sessions]
- [file locations worth knowing]
```

Breadcrumbs live in the project repo (`.claude/breadcrumbs.md`), not the vault.
They're for future Claude sessions. The vault notes are for future you.
</write_breadcrumbs>

### Step 6: Cross-Link Everything

<crosslink>
Ensure bidirectional linking:

1. Session note → daily note: `[[YYYY-MM-DD]]`
2. Daily note → session note: `[[YYYY-MM-DD-session-topic]]`
3. Session note → related project notes
4. Related project notes → session note (in their Activity section)
5. Session note → any notes created during the session

The goal: from any note, you can trace back to the session that created it
and forward to what came next.
</crosslink>

### Step 7: Confirm Sync

<confirm>
Report everything that was synced:

```markdown
## Session Synced to Obsidian

**Session note:** [[YYYY-MM-DD-session-topic]]
  → Path/to/session-note.md

**Daily note updated:** [[YYYY-MM-DD]]
  → Added session summary under ## Log

**Breadcrumbs written:** .claude/breadcrumbs.md
  → Context for next Claude session

**Links created:**
  → [[session]] ↔ [[daily]]
  → [[session]] ↔ [[related-note-1]]
  → [[session]] ↔ [[related-note-2]]

Everything persisted. Safe to close this session.
```
</confirm>

## Composability

This skill orchestrates patterns from:
- [breadcrumbs](../breadcrumbs/SKILL.md) — Session-to-session memory
- [retrospective](../retrospective/SKILL.md) — Failed attempts and learnings
- [obsidian-note-create](../obsidian-note-create/SKILL.md) — Proper note creation
- [obsidian-daily-driver](../obsidian-daily-driver/SKILL.md) — Daily note updates

If those skills are installed, their full capabilities enhance this flow.
If not, this skill includes the core patterns inline.

## Decision: Session Note vs. Daily Log Only

Not every session needs its own note:

| Session Type | Action |
|-------------|--------|
| Significant work (multi-step, decisions made) | Full session note + daily log |
| Quick fix or small change | Daily log entry only |
| Research / exploration | Session note (captures what was learned) |
| Single question answered | Daily log entry only |
| Failed attempt / dead end | Session note (documents the dead end) |

Default to daily-log-only for short sessions. Only create session notes for
sessions you'd want to reference later.

## NEVER

- Sync an empty session (nothing to persist)
- Overwrite existing daily note content
- Skip the breadcrumbs (future Claude needs them)
- Create session notes for trivial interactions
- Leave orphaned notes (everything must link to something)
- Sync without reading vault state first

## ALWAYS

- Assess what happened before deciding what to sync
- Read CLAUDE.md and existing daily note before writing
- Cross-link session note ↔ daily note ↔ related notes
- Include failed attempts in session notes (most valuable part)
- Write breadcrumbs for project-level context
- Confirm what was synced before closing

## Example

**End of session where user built auth middleware and discovered a gotcha:**

```
Session Sync

Assessing session...
- Built JWT auth middleware (src/middleware/auth.ts)
- Discovered: session tokens stored in Redis with 1hr TTL (not documented)
- Failed: tried cookie-based approach first, CORS issues killed it
- Next: add refresh token rotation

Creating session note...
→ Projects/api/notes/2026-02-12-session-auth-middleware.md

Updating daily note...
→ Daily/2026-02-12.md
  Added to ## Log:
  - Claude session: built JWT auth middleware, discovered Redis TTL gotcha
  Added to ## Links:
  - [[2026-02-12-session-auth-middleware]]

Writing breadcrumbs...
→ .claude/breadcrumbs.md
  - Auth middleware complete, cookie approach failed (CORS), Redis TTL is 1hr

Cross-linking...
→ [[2026-02-12-session-auth-middleware]] ↔ [[2026-02-12]]
→ [[2026-02-12-session-auth-middleware]] ↔ [[api-design]]
→ [[api-design]] Activity section updated

Session synced. Safe to close.
```

<failed-attempts>
What DOESN'T work:
- Syncing at the START of a session — nothing has happened yet, nothing to sync
- Creating session notes for every session — clutter; only when there's substance
- Skipping breadcrumbs because vault has session notes — breadcrumbs are for Claude, vault notes are for you
- Not reading existing daily note — you duplicate entries or break structure
</failed-attempts>
