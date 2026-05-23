---
id: 006
title: Add esper:done skill — finalize a plan with a guaranteed commit
status: done
priority: 2
phase: phase-1
branch: phase/phase-1
created: 2026-02-18
shipped_at: 2026-02-18
pr: merged-to-main
---

# Add esper:done skill — finalize a plan with a guaranteed commit

## Context

Currently the esper workflow has two commit-related commands:
- `/esper:commit` — save partial progress anytime; only commits if there are changes
- `/esper:ship` — verify + commit + push + open PR + archive

There is no command that finalizes a plan (archives it to `done/`) without opening a PR. This gap matters most in `type: "feature"` plans, where per-plan PRs are skipped — the user needs a way to say "this plan is complete, commit my work and archive it" before moving on to the next plan. The phase PR is opened later by `esper:ship` when all phase plans are done.

The key difference from `/esper:commit`:
- `/esper:commit`: partial save, can be called anytime, no-ops if nothing changed
- `/esper:done`: finalization step — **always** produces a commit (even if the only change is the plan file itself), then archives the plan to `done/`

## Files changed

- `skills/esper-done/SKILL.md` (created — the new skill)
- `skills/esper-ship/SKILL.md` (modified — Step 1: check done/ fallback; Step 6: handle already-archived plans)

## Verification

- Run: manual
- Expected:
  - Feature plan workflow: implement plan → `/esper:done` → plan is in `done/` with `status: done`, `shipped_at` set, no `pr` field; working tree committed → repeat for next plan → `/esper:ship` finds done plans, opens phase PR, adds `pr:` to each plan's frontmatter
  - Fix plan workflow: implement → `/esper:done` → `/esper:ship` finds the done plan, pushes, opens PR, updates plan frontmatter with `pr:` URL
  - `/esper:commit` behavior unchanged

## Progress

- Created `skills/esper-done/SKILL.md`: 5-step workflow — check setup → verify → commit (always, skip if clean) → archive to done/ (no pr field) → summary with type-aware next-step message
- Updated `skills/esper-ship/SKILL.md` Step 1: checks done/ for unshipped plan (no pr field) if active/ is empty; updated Step 6: handles already-archived plans in done/ by only updating pr field instead of moving
- Adapted plan to use `type` field instead of deprecated `pr_mode` references
- Modified: skills/esper-done/SKILL.md (created), skills/esper-ship/SKILL.md
- Verification: manual — new skill visible via `node bin/cli.js`
