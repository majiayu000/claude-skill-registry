---
name: session-end
user-invocable: false
tags: [orchestration, verification, commits, issues]
model-preference: sonnet
model-preference-codex: gpt-5.4-mini
model-preference-cursor: claude-sonnet-4-6
description: >
  Full session close-out: verifies all planned work against the agreed plan, creates issues
  for gaps, runs quality gates, commits cleanly, mirrors to GitHub, and produces a session
  summary. Triggered by /close command.
---

# Session End Skill

> **Platform Note:** State files (STATE.md, wave-scope.json) live in the platform's native directory: `.claude/` (Claude Code), `.codex/` (Codex CLI), or `.cursor/` (Cursor IDE). All references to `.claude/` below should use the platform's state directory. Shared metrics live in `.orchestrator/metrics/`. See `skills/_shared/platform-tools.md`.

## Phase 0: Bootstrap Gate

Read `skills/_shared/bootstrap-gate.md` and execute the gate check. If the gate is CLOSED, invoke `skills/bootstrap/SKILL.md` and wait for completion before proceeding. If the gate is OPEN, continue to Phase 1.

<HARD-GATE>
Do NOT proceed past Phase 0 if GATE_CLOSED. There is no bypass. Refer to `skills/_shared/bootstrap-gate.md` for the full HARD-GATE constraints.
</HARD-GATE>

## Phase 1: Plan Verification

Read back the session plan that was agreed at the start. For EACH planned item:

### 1.1 Done Items
- **Verify with evidence**: read the changed files, check git diff, run relevant test
- Confirm acceptance criteria are met
- Mark as completed

### 1.2 Partially Done Items
- Document what was completed and what remains
- Create a VCS issue for the remaining work with:
  - Title: `[Carryover] <original task description>`
  - Labels: `priority:<original>`, `status:ready`
  - Description: what's done, what's left, context for next session
- Link to original issue if applicable

### 1.3 Not Started Items
- Document WHY (blocked? de-scoped? out of time?)
- If still relevant: ensure original issue remains `status:ready`
- If no longer relevant: close with comment explaining why

### 1.4 Emergent Work
- Tasks that were NOT in the plan but were done (fixes, discoveries)
- Document and attribute to relevant issues
- If new issues were identified: create them on the VCS platform

### 1.5 Discovery Scan (if enabled)

Read `skills/session-end/discovery-scan.md` for embedded discovery dispatch and findings triage.

### 1.6 Safety Review

> Skip if `persistence` is `false` in Session Config (STATE.md won't exist).

Review safety metrics from the session. This is informational — it does NOT block the session close.

1. Read `<state-dir>/STATE.md` to extract:
   - **Circuit breaker activations**: agents that hit maxTurns (`PARTIAL`), agents that spiraled (`SPIRAL`), agents that failed (`FAILED`)
   - **Worktree status**: which agents used worktree isolation, any fallbacks or merge conflicts
2. Read enforcement hook logs from stderr (if captured): count of scope violations blocked/warned, command violations blocked/warned
3. Summarize:
   ```
   Safety review:
   - Agents: [X] complete, [Y] partial (hit turn limit), [Z] spiral/failed
   - Enforcement: [N] scope violations, [M] command blocks
   - Isolation: [K] agents in worktrees, [J] fallbacks
   ```
4. If any agents were `SPIRAL` or `FAILED`, ensure carryover issues exist (cross-reference with Phase 1.2)

### 1.7 Metrics Collection

Read `skills/session-end/metrics-collection.md` for JSONL schema and conditional field rules.

### 1.8 Session Review

Dispatch the session-reviewer agent to verify implementation quality before the quality gate:

> On Codex CLI, dispatch via the `session-reviewer` agent role defined in `.codex-plugin/agents/session-reviewer.toml`.

1. Invoke `subagent_type: "session-orchestrator:session-reviewer"` with:
   - **Scope**: all files changed this session (from `git diff --name-only` against the base branch)
   - **Context**: the session plan (issues, acceptance criteria) and all wave results from STATE.md
2. Wait for the reviewer's **Verdict**:
   - **PROCEED** — continue to Phase 2
   - **FIX REQUIRED** — address each listed item before proceeding. For quick fixes (<2 min each), fix inline. For larger items, create carryover issues (same as Phase 1.2) and note them as unresolved review findings in the Final Report

## Phase 2: Quality Gate

> **Verification Reference:** See `verification-checklist.md` in this skill directory for the full quality gate checklist.

Run ALL checks listed in the verification checklist. If any check fails: fix if quick (<2 min), otherwise create a `priority:high` issue. Do NOT commit broken code.

### 2.1 Vault Validation (if configured)

Read `skills/session-end/vault-operations.md` for validator bash contract and reporting matrix.

## Phase 3: Documentation Updates

### 3.0 Defensive Cleanup

Delete `<state-dir>/wave-scope.json` if it still exists:

```bash
rm -f <state-dir>/wave-scope.json
```

This should have been cleaned up by wave-executor after the final wave, but crashed sessions or interrupted executions may leave it behind. A stale scope manifest from a previous session could incorrectly restrict the next session's enforcement hooks.

### 3.1 SSOT Files
- Update `STATUS.md` / `STATE.md` if they exist (metrics, dates, status)
- Update `CLAUDE.md` if patterns or conventions changed during this session
- Check `<state-dir>/rules/` — if a new pattern was established, suggest a new rule file

### 3.2 Session Handover (for significant sessions)
If this session made substantial changes, create or update:
- `<state-dir>/session-handover/` doc with: tasks completed, resume point, metrics changed, issues opened/closed
- Or update `<state-dir>/STATE.md` with session digest

### 3.3 Claude Rules Freshness
Review `<state-dir>/rules/` files that are relevant to this session's work:
- Are the rules still accurate after this session's changes?
- Should any rule be updated with new patterns?
- Should a new path-scoped rule be created?
- Suggest changes but DO NOT modify without user confirmation

### 3.4 Update STATE.md

> **Ownership Reference:** See `skills/_shared/state-ownership.md`. session-end is authorized to set `status: completed` only — no other fields.

> Gate: Only run if `persistence` is enabled in Session Config and `<state-dir>/STATE.md` exists.
1. Set frontmatter `status: completed`
2. Record final wave count and completion time in the frontmatter
3. Keep the file as a record — do NOT delete it (next session-start reads it)

If STATE.md doesn't exist, skip this subsection.

### 3.5 Session Memory

> Gate: Only run if `persistence` is enabled in Session Config AND platform is Claude Code (session memory at `~/.claude/projects/` is Claude Code-only). Learnings (Phase 3.5a) and metrics (Phase 3.7) still write to `.orchestrator/metrics/` on all platforms.

1. Create `~/.claude/projects/<project>/memory/session-<YYYY-MM-DD>.md` with:
   - Frontmatter: `name`, `description` (1-line summary), `type: project`
   - `## Outcomes` — per-issue status (completed / partial / not started) with evidence
   - `## Learnings` — patterns discovered, architectural insights, gotchas
   - `## Next Session` — priority recommendations, suggested session type, blockers
2. Update `~/.claude/projects/<project>/memory/MEMORY.md`:
   - Under a `## Sessions` heading (create if missing), add:
     `- [Session <date>](session-<date>.md) — <one-line summary>`

### 3.5a Learning Extraction + 3.6 Memory Cleanup & Learnings Write

Read `skills/session-end/learning-patterns.md` for extraction heuristics, confidence updates, passive decay, and JSONL write procedure.

### 3.7 Write Session Metrics

Read `skills/session-end/session-metrics-write.md` for JSONL append, vault-mirror invocation, and behavior matrix.

## Phase 4: Commit & Push

### 4.1 Stage Changes
- **Stage files individually**: `git add <file>` — NEVER `git add .` or `git add -A`
- **Always stage these session artifacts** (if modified):
  - `.orchestrator/metrics/sessions.jsonl` (session summary from Phase 3.7)
  - `.orchestrator/metrics/learnings.jsonl` (learnings from Phase 3.6)
  - `<state-dir>/STATE.md` (session state, if persistence enabled)
  - Any files created or modified by wave agents
- Review staged changes: `git diff --cached` — verify every change is from THIS session
- If you see changes you did NOT make, ask the user (parallel session awareness)

### 4.2 Commit
Use Conventional Commits format:
```
type(scope): description

- [bullet points of what changed]
- Closes #IID1, #IID2 (if applicable)

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

For sessions with many changes, prefer ONE commit per logical unit (not one mega-commit).

### 4.3 Push
```bash
git push origin HEAD
```

### 4.4 GitHub Mirror (if configured in Session Config)
```bash
# Only attempt if 'mirror: github' is in Session Config AND remote exists
git remote get-url github 2>/dev/null && git push github HEAD 2>/dev/null || echo "GitHub mirror: not configured"
```

## Phase 5: Issue Cleanup

> **VCS Reference:** Use CLI commands per the "Common CLI Commands" section of the gitlab-ops skill.

1. **Close resolved issues**: Use the issue close and note commands per the "Common CLI Commands" section of the gitlab-ops skill. Note: some VCS platforms require separate note and close commands.
2. **Update in-progress issues**: ensure labels reflect actual state using the issue update command
3. **Create carryover issues**: for partially-done work (from Phase 1.2), use the issue create command with appropriate labels

#### Discovery Issue Creation (if discovery ran in Phase 1.5)

For each finding with severity `critical` or `high` from Phase 1.5:
1. Create a VCS issue using the detected platform CLI:
   - Title: `[Discovery] <description>` (truncated to 70 chars)
   - Body: `**Probe:** <probe>\n**File:** <file>:<line>\n**Severity:** <severity>\n**Confidence:** <confidence>%\n**Recommendation:** <recommendation>`
   - Labels: `type:discovery`, `priority:<severity>` (critical→critical, high→high)
2. Log each created issue ID for the Final Report
3. Update `discovery_stats.issues_created` count

4. **Create gap issues**: for newly-discovered problems
5. **Update milestones**: if milestone progress changed

## Phase 6: Final Report

Present to the user:

```
## Session Summary

### Completed
- [x] Issue #N: [description] — [evidence: tests passing, files changed]
- [x] Issue #M: [description]

### Carried Over
- [ ] Issue #P: [what's left] — new issue #Q created
- [ ] [description] — blocked by [reason]

### New Issues Created
- #R: [title] (priority: [X], status: ready)
- #S: [title] (priority: [X], status: ready)

### Metrics
- Duration: [total wall-clock time]
- Waves: [N completed]
- Agents: [total dispatched] ([X complete, Y partial, Z failed])
- Files changed: [N]
- Per-wave breakdown:
  - Wave 1 (Discovery): [duration] — [N agents] — [K files]
  - Wave 2 (Impl-Core): [duration] — [N agents] — [K files]
  - ...
- Tests: [passing/total]
- TypeScript: 0 errors
- Commits: [N] pushed to [branch]
- Mirror: [synced/skipped]
- Enforcement: [N violations blocked / M warnings] (or "N/A" if enforcement off)
- Circuit breaker: [N agents hit limits, M spirals detected] (or "none")
- Metrics written to: `.orchestrator/metrics/sessions.jsonl`
- Learnings: [N] new, [M] confirmed, [K] contradicted/expired — written to `.orchestrator/metrics/learnings.jsonl`

### Next Session Recommendations
- Priority: [what should be tackled next]
- Type: [housekeeping/feature/deep recommended]
- Notes: [any context for next session]
```

## Sub-File Reference

| File | Purpose |
|------|---------|
| `plan-verification.md` | Phase 1 plan verification and metrics collection |
| `verification-checklist.md` | Phase 2 quality gate checklist and checks |
| `discovery-scan.md` | Phase 1.5 embedded discovery dispatch and findings triage |
| `metrics-collection.md` | Phase 1.7 JSONL schema and conditional field rules |
| `vault-operations.md` | Phase 2.1 validator bash contract and reporting matrix |
| `learning-patterns.md` | Phases 3.5a + 3.6 extraction heuristics, confidence updates, passive decay, and JSONL write procedure |
| `session-metrics-write.md` | Phase 3.7 JSONL append, vault-mirror invocation, and behavior matrix |

## Anti-Patterns

- **DO NOT** commit before running quality gates — a "clean commit" with TypeScript errors is not clean
- **DO NOT** mark issues as closed without verifying the implementation actually addresses them
- **DO NOT** skip creating tracking issues for unfinished work — "I'll remember for next session" always fails
- **DO NOT** use `git add .` or `git add -A` — parallel sessions may have uncommitted work in the tree
- **DO NOT** push to mirrors before verifying origin push succeeded — broken state propagates

## Critical Rules

- **NEVER claim work is done without running verification** — evidence before assertions
- **NEVER commit with TypeScript errors** — 0 errors is non-negotiable
- **NEVER use `git add .`** — stage files individually to avoid capturing parallel session work
- **NEVER skip issue updates** — VCS must reflect reality after every session
- **ALWAYS create issues for unfinished work** — nothing should be "remembered" without a ticket
- **ALWAYS push to origin** — local-only work is lost work
- **ALWAYS mirror to GitHub** if configured — keep mirrors in sync
- **ALWAYS review `git diff --cached`** before committing — verify only YOUR changes are staged
