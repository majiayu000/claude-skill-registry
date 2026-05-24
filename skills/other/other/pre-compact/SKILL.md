---
name: pre-compact
description: Pre-compaction housekeeping. Walks a checklist (persistent memory updates, git hygiene, trash cleanup) plus an open-judgment audit, produces an SBAR with a go/no-go recommendation, and emits a copy-pasteable resume prompt for the post-compaction agent if work remains. Run this immediately before /compact.
model: opus
---

# Pre-Compact - Session Housekeeping Before Compaction

The user is about to run `/compact`. Compaction destroys conversation
context. Anything important from this session that is not persisted
somewhere durable — memory files, commits, tickets, code, the issue
tracker — is lost.

This skill is the last-chance pass to capture session state. Walk a
fixed checklist as a floor, then use judgment for anything the
checklist does not anticipate, and end with an SBAR-formatted go/no-go
report.

## Philosophy

- **Persist before you compact.** If a fact will matter next session,
  it goes into persistent memory now. If a change should be in the
  project, it gets committed (with permission). If an artifact is
  trash, it gets deleted.
- **Surface uncertainty instead of guessing.** When unsure whether
  something is trash, abandoned, or important, ask the user.
- **Bias toward asking, not committing.** Never commit on the user's
  behalf without per-invocation permission. Standing rules from
  CLAUDE.md still apply.
- **The checklist is a floor, not a ceiling.** Walk every item, but
  also use judgment to spot session-specific cleanup the checklist
  cannot anticipate.
- **Do not invoke /compact yourself.** Compaction is the user's call.

## Workflow

### 1. Persistent memory pass

Updating persistent memory is the core reason this skill exists. The
user invokes `/pre-compact` *because* they want memory written before
compaction. Do not skip this step or treat it as conditional. Follow
whatever memory conventions are documented in the user's global or
project CLAUDE.md (auto-memory directory, project notes, etc.).

Re-scan the session for facts worth saving across conversations.
Look for:

- **About the user**: role, expertise, preferences, current focus
- **Feedback**: corrections received OR non-obvious approaches the
  user confirmed worked. Capture the *why* the user gave, not just
  the rule.
- **Project state**: ongoing initiatives, constraints, deadlines,
  decisions, stakeholder context. Convert relative dates to absolute
  ones.
- **External references**: pointers to issue trackers, dashboards,
  channels, docs the user mentioned

For each candidate:

- Check existing memory files first. Update an existing memory rather
  than writing a duplicate.
- Skip anything already saved, derivable from `git log` / current
  code, or ephemeral to this conversation.
- Honor the exclusion rules in the user's memory instructions
  (architecture, conventions, fix recipes, ephemeral state).

### 2. Git hygiene pass

Run `git status` and assess:

- **Uncommitted intentional changes**: surface them. Ask the user
  whether to commit. If yes, draft a commit message and ask for
  approval before running `git commit`.
- **Uncommitted in-progress changes**: surface them. The filesystem
  survives compaction, so the *files* are not at risk — but the
  *context* about what is in flight may be. Either commit as WIP, or
  capture the in-flight state in the SBAR.
- **Untracked files**: route each to step 3 (trash) or surface as
  work product that should be tracked.
- **Branch state**: note any unusual condition (detached HEAD,
  mid-rebase, mid-merge, conflicts) so the user is aware before
  compacting.

Do not commit or stage on the user's behalf without explicit
per-invocation permission. Match the scope of any granted permission
exactly.

### 3. Trash cleanup pass

Identify candidate trash:

- Untracked scratch files created during this session (`/tmp/*`,
  `*.bak`, ad-hoc test scripts, debug dumps)
- Files matching obvious throwaway patterns (`scratch.*`, `debug.*`,
  `tmp_*`, `nohup.out`)
- Stray build artifacts that should have been gitignored

For each candidate:

- **Clearly trash and clearly mine**: delete and report.
- **Ambiguous origin or intent**: ask the user. When in doubt, do
  not delete.
- **Not mine**: leave alone.

A false delete loses the user's work-in-progress. A false retain
costs nothing. Bias accordingly.

### 4. Open audit (judgment)

Walk the session and look for anything else that would be hard to
reconstruct from `git log` + persistent memory + the issue tracker
after compaction. Examples (non-exhaustive — the point of this step
is to think past the checklist):

- Decisions made during the session that are not captured in any
  ticket, commit message, code comment, or memory
- Pending TODOs from the conversation that have no durable home
- Open threads with the user — questions asked but not answered,
  options proposed but not chosen
- Work-in-progress with no plan/task/ticket capturing the current
  state
- Long-running background processes (`run_in_background` tasks, dev
  servers, watchers) that the user may have forgotten about
- Active worktrees, stashes, or branches that need a decision before
  context is lost

For each item: either persist it now (memory, ticket, comment) or
flag it explicitly in the SBAR.

### 5. Produce SBAR

Per the user's session handoff format:

- **Situation:** state of the working tree, repo, and any in-flight
  work right now
- **Background:** what was tried this session, what was rejected,
  what surprised
- **Assessment:** what you believe is true, calibrated by confidence
  — *verified* (ran the command, read the file), *inferred*
  (reasoned from observation), or *recalled* (training knowledge,
  possibly stale)
- **Recommendation:** exactly one of:
  - **Safe to compact.** All housekeeping done, nothing material
    at risk.
  - **Safe to compact after [X].** A small action remains for the
    user (commit a staged change, answer a pending question);
    after that, compaction is fine.
  - **Do not compact yet — [Y].** Genuine blocker. Compaction
    would lose load-bearing context that has not been captured.

Keep each field tight — one to three lines. The user reads this
returning to a stale tmux pane, and may also use it to brief the
post-compaction version of the session.

### 6. Produce resume prompt

The post-compaction agent reads the lossy summary, not the live
conversation. A resume prompt drafted *now*, while full context is
still in scope, is far higher-quality than what that agent could
reconstruct from the summary. Always emit one of two outputs in this
step — never silently skip it, since absence is ambiguous.

If there is pending work the next turn should pick up, emit a single
fenced block the user can copy clean into the next prompt. The block
must be:

- **For Claude, not the user.** Imperative, technical register. Not
  conversational.
- **Self-contained.** Name files with line numbers, decisions already
  made, constraints already negotiated, and the next concrete step.
  Do not write "continue where we left off" — write "edit
  `path/to/file.py:42` to do Y, then run Z."
- **Singular.** One next action, not a menu. If multiple threads are
  open, pick the load-bearing one here and let the SBAR's
  Recommendation field flag the others.

If there is no pending work, emit exactly this line and nothing else
in this step:

> **No resume prompt — work is sealed.**

### 7. Stop

Wait for the user. Do not run `/compact`. Do not start new
implementation work — this skill exists to seal the session, not to
extend it.
