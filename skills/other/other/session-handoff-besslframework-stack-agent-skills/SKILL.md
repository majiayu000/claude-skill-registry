---
name: session-handoff
description: |
  Compresses the current session state into a handoff document for seamless
  continuation in the next session. Captures progress, decisions, blockers,
  and next steps. Use at the end of a session or when context is getting large.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Session Handoff

Create seamless transitions between Claude Code sessions.

---

## Quick Start

1. **When you are done for now, run `/session-handoff`.** The skill extracts completed work, decisions, blockers, and next steps from the current conversation and writes them to `docs/handoffs/[date]-[topic].md`.
2. **Start a new session. Run `/session-handoff load docs/handoffs/[date]-[topic].md`.** The skill reads the handoff, verifies that referenced files still exist, and summarizes the context.
3. **Continue working.** The new session picks up where the old one left off. No re-explaining needed.

---

## Overview

Context windows are finite. When a session gets long or you need to continue work later, this skill compresses the essential state into a handoff document that the next session can load and continue from.

---

## Commands

### `/session-handoff` or `/session-handoff save`

Generate a handoff document from the current session.

1. Analyze the conversation for: completed work, decisions, current state, next steps
2. Check git status and recent diffs for file-level changes
3. Write handoff to `docs/handoffs/[date]-[topic].md`
4. Confirm save location with the user

### `/session-handoff load [path]`

Load a handoff document and apply its context.

1. Read the handoff file
2. Summarize the context for the current session
3. Confirm understanding with the user
4. Continue from where the previous session left off

### `/session-handoff list`

List available handoff documents in `docs/handoffs/`.

---

## The Job

### When Saving

Extract from the current conversation:

1. **What was accomplished** - Completed tasks, files created/modified, tests written
2. **Key decisions made** - Architectural choices, trade-offs accepted, approaches chosen
3. **Current state** - What's working, what's broken, test status, build status
4. **Blockers** - Issues discovered, external dependencies, questions needing answers
5. **Next steps** - Clear, ordered list of what to do next
6. **Context** - Important background info the next session needs

### When Loading

1. Read the handoff document
2. Present a brief summary to the user
3. Verify the files mentioned still exist and match expected state
4. Ask: "Ready to continue from where we left off?"

---

## Output Format

Use the template at `templates/handoff-template.md`.

```markdown
# Session Handoff: [Date] [Topic]

**Previous Session**: [session ID or description]
**Handoff Created**: [timestamp]
**Project**: [project path]
**Branch**: [git branch]

---

## Completed

- [x] [Task 1 description]
- [x] [Task 2 description]
- [x] [Task 3 description]

## Key Decisions

- **[Decision 1]**: [What was decided and why]
- **[Decision 2]**: [What was decided and why]

## Current State

### Files Modified
| File | Change | Status |
|------|--------|--------|
| `path/to/file1.ts` | Created new component | Working |
| `path/to/file2.ts` | Updated API handler | Needs testing |

### Build/Test Status
- Build: [passing/failing]
- Tests: [X passing, Y failing]
- Lint: [passing/failing]
- Specific failures: [if any]

### Git Status
- Branch: [branch name]
- Uncommitted changes: [yes/no, brief summary]
- Last commit: [hash + message]

## Blockers

- [ ] [Blocker 1]: [description and what's needed to resolve]
- [ ] [Blocker 2]: [description and what's needed to resolve]

## Next Steps

1. [ ] [Most important next task]
2. [ ] [Second task]
3. [ ] [Third task]
4. [ ] [Further tasks...]

## Context

[Any background information the next session needs to understand.
Include relevant architecture decisions, patterns being followed,
external documentation references, etc.]

## Key Files

- `path/to/main/file.ts` - [why it's important]
- `path/to/config.ts` - [relevant config]
- `docs/relevant-doc.md` - [reference material]
```

---

## Extraction Heuristics

### Completed Work Detection

Look for:
- Tool calls that successfully created or edited files
- User confirmations ("looks good", "that works", "perfect")
- Test passes after implementation
- Commit messages in the session

### Decision Detection

Look for:
- "Let's go with [option]"
- "I chose X because Y"
- AskUserQuestion results
- Explicit trade-off discussions
- User preferences stated

### Blocker Detection

Look for:
- Unresolved errors at end of session
- "TODO" or "we'll need to" statements
- External dependencies mentioned
- Questions that weren't answered

### Next Steps Detection

Look for:
- Explicit "next steps" or "TODO" lists
- Incomplete task lists
- Plans that were partially executed
- User's stated goals minus completed work

---

## Important Constraints

- **Be concise**: The handoff should be loadable in < 2,000 tokens
- **Be specific**: File paths, not "the component". Commit hashes, not "recent commit"
- **Be honest**: If tests are failing, say so. If something is half-done, say so
- **Include git state**: Branch, uncommitted changes, last commit
- **Don't assume**: The next session might be a different person or agent
- **Save location**: Default to `docs/handoffs/` but respect user preference

---

## Auto-Detection

The skill can detect when a handoff is needed instead of waiting for the user to run the command. Watch for these signals during the session.

### Signals That Trigger a Handoff Suggestion

| Signal | How to Detect | Confidence |
|---|---|---|
| Long conversation | Exchange count exceeds ~50 user messages | High. Context window is filling up. |
| Context compression observed | Assistant responses start missing details mentioned earlier, or repeat questions already answered | High. The model is losing context. |
| User signals a break | User says "let's continue tomorrow", "I need to stop", "save this", "gotta go", "picking this up later" | High. Explicit intent. |
| Multiple failed tool calls | 3+ consecutive tool errors (file not found, wrong arguments, unexpected output) | Medium. May indicate context confusion, or may just be a tricky bug. |
| Topic drift | The current task diverges significantly from the stated goal at session start | Low. Might be intentional exploration. Only suggest if combined with another signal. |

### Behavior on Detection

Do not auto-save. Instead, suggest once:

```
This session is getting long (~55 exchanges). Want me to create a handoff
document so you can continue fresh? Run /session-handoff or say "not yet".
```

If the user declines, do not suggest again for at least 20 more exchanges.

---

## Compression Levels

Not all handoffs need the same detail. Use compression levels to control output size based on the situation.

### Level 1: Full Detail (default, ~2000 tokens)

Use when: continuing the same work in your next session.

Includes everything in the standard template: completed work, decisions with reasoning, full file table, build/test status, git state, blockers, next steps, context section.

### Level 2: Summary (~500 tokens)

Use when: the next session is a few days away and you need a reminder, not a full replay.

Includes:
- One-paragraph summary of what was accomplished
- Bullet list of key decisions (what, not why)
- Current blockers as a flat list
- Ordered next steps
- Branch name and uncommitted changes flag

Omits: file-level change table, build output details, full context section.

### Level 3: Bullet Points (~200 tokens)

Use when: handing off a small task, or when the handoff is just a bookmark to come back to.

Includes:
- 3-5 bullet points covering: what was done, what is left, which branch
- Nothing else

### Specifying a Level

```
/session-handoff save --level 2
```

If no level is specified, default to Level 1. If the session was short (< 15 exchanges), auto-downgrade to Level 2.

---

## Team Handoff

When the next session will be a different person or a different agent (not you continuing your own work), the handoff needs additional context. A solo handoff can rely on shared memory. A team handoff cannot.

### Additional Fields for Team Handoffs

Add these to the standard template:

```markdown
## Why (Decision Rationale)

Explain the reasoning behind key choices. The recipient was not in the room.

- **Chose Next.js App Router over Pages Router**: The project already uses App Router
  for other pages. Mixing routers adds complexity for no benefit.
- **Skipped unit tests for the UI component**: The component is pure presentation with
  no logic. An E2E test in the integration story covers it better.
- **Used server action instead of API route**: The form only needs server-side
  processing. A dedicated API route would be unnecessary indirection for this case.

## Gotchas

Things that are not obvious but will waste the next person's time:

- The `users` table has a trigger that auto-updates `updated_at`. Do not set it
  manually in the migration or it will be overwritten.
- The `AUTH_SECRET` env var must be base64-encoded. Plain strings cause a silent
  failure in the auth middleware.
- Tests must run with `--runInBand` because the DB fixtures collide under parallel
  execution.

## Open Questions

Questions that came up but were not resolved. The next person may need to make a call:

- Should the profile photo be required or optional? Spec is ambiguous. Currently
  implemented as optional.
- Rate limit on the upload endpoint: 10/min per user, or 10/min globally? Currently
  set to per-user.
```

### Triggering a Team Handoff

```
/session-handoff save --team
```

Or the skill auto-detects and suggests `--team` when:
- The user mentions handing off to someone by name
- The user says "someone else will pick this up"
- The conversation references a different agent or teammate

---

## Templates

See `templates/handoff-template.md` for the full output template.
