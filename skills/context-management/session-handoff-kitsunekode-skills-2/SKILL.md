---
name: session-handoff
description: Save and restore cross-session state for coding work. Use when ending a session, switching tasks, or resuming work later and you want a concise “where we left off” handoff.
---

# Context Handoff

Session continuity for coding agents. Write compressed state at session end,
read it at session start. The next session skips re-discovery and starts
working immediately.

**Why this matters**: LLMs are stateless. Every new session starts from zero.
Without a handoff, agents waste 30-50% of their context window just
rediscovering what the last session already knew — files, decisions, blockers.
This skill solves that by compressing session state into a lightweight file
that the next session reads in seconds.

## Session Start Behavior

If `.context/handoff.md` exists (injected via the plugin's SessionStart hook
or read manually), use it as your primary orientation:

1. Read the handoff file.
2. Note the branch, what was done, what's in progress, and what's next.
3. Check alignment: does the handoff's `session_name` match what the user is
   asking now? If unrelated, ask: "I have a handoff from a previous session on
   [session_name]. Is this related, or should I start fresh?"
4. **Verify files exist** before trusting the handoff. Spot-check 1-2 files
   from "Key Files" to confirm they're on disk. If missing, tell the user.
5. If aligned, start from the "Next" checklist — do NOT re-explore files
   already in "Key Files" unless the handoff indicates uncertainty.
6. If stale (branch mismatch, files changed since `updated` timestamp),
   mention this and do targeted re-discovery only on changed areas.

## Session End Behavior

When the session is ending (user says goodbye, you're about to /clear, or
context is getting heavy):

### Step 1: Read Config

Check `.context/config.yaml` for mode setting. Default: `mode: ask`.

### Step 2: Introspect

Gather state from:

- `git diff --stat` and `git branch --show-current`
- Files you read, created, or edited during this session
- Decisions made (especially where you chose between alternatives)
- Blockers hit or gotchas discovered
- The user's original task and any refinements

### Step 3: Draft Handoff

Write a handoff document with these sections:

```markdown
---
updated: [current ISO 8601 timestamp]
branch: [current branch from git branch --show-current]
session_name: '[brief label for this work]'
context_pressure: [low | medium | high]
---

## Done

[Completed work — each item references specific files:line numbers]

## In Progress

[Partially completed work — what state it's in]

## Blocked

[External dependencies, failing tests, missing info]

## Next

- [ ] [Ordered actionable checklist]

## Decisions

[Non-obvious choices and why they were made]

## Key Files

[All files relevant to the task, with line refs where useful]
```

### Step 4: Write or Ask

- **yolo mode**: Write `.context/handoff.md` directly. Tell the user.
- **ask mode**: Show draft, incorporate feedback, then write.

### Step 5: Verify Quality

After writing, check against targets:
- 30-80 lines, under 1k tokens
- Every "Done" item has a `file:line` reference
- "Next" items are actionable without reading conversation history
- A new agent reading only the handoff starts productive work in 2-3 tool calls

If the handoff fails any target, revise before saving.

## Compaction Philosophy

The handoff is a compression of truth, not a transcript. Think of it like a
teammate's sticky note: just enough to get you going, nothing more.

**Include (high signal):**

- Key files with line numbers — lets the next session jump to the right code
- Decisions and why — prevents re-debating the same choices
- Blockers and gotchas — the next session will hit the same walls without these
- Next steps as ordered checklist — clear starting point

**Exclude (noise):**

- Full file contents — files are on disk, just reference them
- Code snippets — reference by `file:line` instead. Exception: a one-line
  type signature the next session needs without reading the file
- Tool call transcripts — the handoff replaces these
- Exploratory dead ends — unless they're gotchas worth warning about
- Verbose error output — summarize the error and what fixed it

## Subagent Strategy

For large repos (>10 key files or heavy git history), delegate the
introspection step to a read-only subagent to keep the main context clean:

1. Spawn a background subagent with Haiku model and read-only tools
   (Read, Grep, Glob, Bash for `git` commands)
2. The subagent gathers: git diff, changed files, branch info, file summaries
3. It returns a compressed state summary (not raw output)
4. Use the summary to draft the handoff in the main conversation

This prevents file-reading noise from consuming the main context window.

## Manual Checkpoint

Invoke `/session-handoff` mid-session to checkpoint progress without ending
the session. This writes the handoff and the session continues.

## Config Reference

`.context/config.yaml` (optional, all fields have defaults):

```yaml
handoff:
  mode: ask # yolo | ask
  auto_trigger: true # true: activate on session end. false: only on /session-handoff
  include_git_diff: true # include git diff --stat
  max_key_files: 20 # cap on listed files
```

When `auto_trigger` is false, the skill only writes a handoff when explicitly
invoked. It will not activate automatically at session end.
