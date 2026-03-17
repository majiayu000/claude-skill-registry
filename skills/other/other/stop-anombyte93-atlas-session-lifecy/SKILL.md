---
name: stop
description: "Gracefully close, pause, or verify a session: harvest promotable content, save progress, archive soul purpose, settle AtlasCoin bounty. Use when user says /stop, wrap up, done for the day, finishing up, close session, pause, verify, or end session."
user-invocable: true
---

# Session Stop Skill

> Graceful session close, pause, or verification. Three intents: Pause | Finish | Verify.

All session operations use `atlas-session` MCP tools directly (prefixed `session_*` and `contract_*`). Use `ToolSearch` to discover them.

## Hard Invariants

1. **User authority is absolute** — AI NEVER closes without confirmation.
2. **Human-visible memory only** — All state lives in files.
3. **Trust separation** — for bounty verify, spawn a separate finality Task agent. Never the same agent that submits.
4. **AtlasCoin is optional** — if down, skip bounty steps and continue.
5. **Idempotent** — Running /stop on an already-closed session exits cleanly.
6. **Archive after verification** — Soul purpose is archived AFTER bounty settlement, not before.

## UX Contract

- User sees ONE intent question, then results. Nothing else.
- No step announcements, no narration, no internal process descriptions.

---

## Phase 0: Sync + State Detection

First, save the current session state so context files are up to date:

1. Invoke `/sync` — updates all session-context files and MEMORY.md with current progress. Silent, no output shown.

Then detect state:

2. Call `session_read_context(project_dir)` — get soul purpose, status hint, open tasks.
2. If `status_hint` is `no_purpose` or soul purpose is empty: tell user "No active soul purpose to close." **EXIT**.
3. Check bounty: if `session-context/BOUNTY_ID.txt` exists, call `contract_get_status(project_dir)`. Store `HAS_BOUNTY`.

## Phase 1: Intent Question

Ask ONE question via AskUserQuestion:

**Question**: "Soul purpose: '[soul purpose text]'. What would you like to do?"
- **"Pause for the day"** — Save state, keep purpose active.
- **"Finished — verify and close"** — Full settlement + PR + archive.
- **"Just verify"** — Check status, show results, return to work.
- **"Cancel"** — Do nothing. **EXIT**.

Store the user's choice as `INTENT`.

Read `custom.md` if it exists, follow instructions under "During Settlement".

---

## Intent A: Pause for the Day

> Save progress. Soul purpose, bounty, and Ralph Loop all stay active.

### Step 1: Harvest

1. Call `session_harvest(project_dir)`.
2. If promotable content exists, assess and present to user for approval.
3. After approval, append promoted content to target files via Edit tool.

### Step 2: Write Checkpoint

Read `session-context/CLAUDE-activeContext.md`, then append a timestamped checkpoint:

```markdown
## [CHECKPOINT] HH:MM DD/MM/YY
### Session Paused — Progress Saved

**Accomplished this session:**
- [AI fills in based on what was done]

**In progress:**
- [AI fills in based on current state]

**Next steps:**
- [AI fills in based on remaining work]

**Blockers/Decisions pending:**
- [AI fills in, or "None"]
```

Fill each section with real, specific content — not placeholders.

### Step 3: Optional Save-Point Commit

Ask: "Create a save-point commit?" (Yes / No)

If Yes and project is git: `git add -A && git commit -m "checkpoint: [brief summary]"`. If commit fails, inform user and continue.

### Step 4: Done

- Do NOT archive the soul purpose — it stays active.
- Do NOT settle the bounty — it stays active.
- Do NOT remove Ralph Loop indicator.
- Tell user: "Progress saved. Soul purpose '[text]' remains active. Run `/start` to pick up where you left off."

---

## Intent B: Finished — Verify and Close

> Full settlement: harvest, verify, review, PR, bounty, archive.

### Step 1: Harvest + Promote

1. Call `session_harvest(project_dir)`.
2. If promotable content exists, assess and present to user. Append approved content.

### Step 2: Feature Verification

1. Call `session_features_read(project_dir)`.
2. If pending features exist, run their proofs. Update status in `CLAUDE-features.md`.

### Step 3: Verification Gate

1. Invoke `superpowers:verification-before-completion` — run doubt review on recent changes.
2. If critical issues: present to user — "Fix first" / "Close anyway" / "Continue working".
3. If "Continue working": **EXIT** (return to active work).

### Step 4: Deactivate Hook

Call `session_hook_deactivate(project_dir)`.

### Step 5: PR Creation

1. Push current branch: `git push -u origin HEAD`
2. Invoke `superpowers:requesting-code-review` for review body.
3. Create PR: `gh pr create --title "..." --body "..."` with review summary.
4. Return PR URL to user.

### Step 6: Bounty Settlement (if bounty exists)

1. Call `contract_run_tests(project_dir)` — execute all criteria.
2. If tests pass: call `contract_submit(project_dir)`.
3. Spawn a single finality Task agent: `Task(subagent_type: "general-purpose", prompt: "You are finality-agent. Verify bounty [ID] independently. Call contract_verify(project_dir). Report pass/fail.")`
4. Wait for finality result.
5. If verified: call `contract_settle(project_dir)`. Tell user tokens earned.
6. If failed: "Fix and re-verify" / "Close anyway (forfeit)" / "Continue working".

### Step 7: Archive + Cleanup

1. If user chose to set a new purpose, ask for it now. Store as `NEW_PURPOSE`.
2. Call `session_archive(project_dir, OLD_PURPOSE, NEW_PURPOSE)`.
3. Remove Ralph Loop indicator: `rm -f ~/.claude/ralph-loop.local.md`
4. Tell user: "Session closed. Soul purpose '[text]' archived." (Include token/PR info.)

---

## Intent C: Just Verify

> Check status without closing. Return to work after.

1. Invoke `superpowers:verification-before-completion` — doubt review.
2. Call `session_features_read(project_dir)` — show feature status.
3. If bounty exists: call `contract_run_tests(project_dir)` — show results.
4. Present all findings to user. No close, no archive.
5. Tell user: "Verification complete. Returning to work."
