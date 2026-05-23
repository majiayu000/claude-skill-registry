---
name: fire-next-up
description: "Pull the next 'Up Next' item from the GitHub Project board and run the full agent chain (design → build → validate) via Depot remote sandboxes (default) or local worktrees (--local). Use when the user says 'fire next up', 'pull next item', 'work on next issue', or wants to dispatch work from the project board. Supports --peek flag to show the queue without dispatching, and --resume to scan all in-flight chains, auto-advance ready ones, and report status."
---

# Fire Next Up — Pull, Dispatch, and Chain Agents

Pulls the next "Up Next" item from the GitHub Project board and runs the full agent chain for that issue type. By default, agents run in **Depot remote sandboxes** (fire-and-forget). Use `--local` to fall back to local worktrees.

## Agent Chains

| Type | Step 1 | Step 2 | Step 3 |
|------|--------|--------|--------|
| `bug` | FiremanDecko (fix) | Loki (validate) | -- |
| `enhancement` | FiremanDecko (implement) | Loki (validate) | -- |
| `ux` | Luna (wireframes) | FiremanDecko (implement) | Loki (validate) |
| `security` | Heimdall (fix/audit) | Loki (validate) | -- |
| `research` | *(varies)* | -- | -- |

**Research:** Technical → FiremanDecko, Product → Freya. Sole agent, posts findings and creates PR. No Loki step. After PR merges, orchestrator presents findings to Odin for **Review** (plan into issues, shelve, or drop).

**Chain rules:** Same branch throughout. First agent creates PR with `PR for issue: #<NUMBER>` in the body (clean title, no issue ref). Loki adds tests on the same PR. If any agent fails, chain stops and orchestrator reports.

## Flags

| Flag | Effect |
|------|--------|
| `--peek` | Show the prioritized Up Next queue — do NOT spawn anything. |
| `--resume #N` | Resume an interrupted chain for issue #N **only**. Calls `--resume-detect N` (and optionally `--chain-status N`). Does **NOT** invoke `--status` and does **NOT** auto-advance other issues. Read `templates/resume-flow.md`. |
| `--resume <session-id>` | Extract issue number from session ID and resume that chain. Session IDs follow the pattern `issue-<N>-step<S>-<agent>-<uuid>` — parse `<N>` as the issue number. Example: `issue-621-step1-firemandecko-8d0410cd` → resume #621. |
| `--resume` | (no issue number) Full dashboard: scan ALL in-progress chains, **auto-advance ready ones** (dispatch next agents, merge PASS+CI green PRs, move completed to Done), and report status. **If no chains need advancing**, fall through to default dispatch: pick top Up Next item and present for refinement (always refine, even if `skip-refinement` is in body). |
| `--batch N` | Pull top N **unblocked** items from "Up Next", start chains in parallel. Max 5. |
| `--local` | Force local worktree execution instead of Depot. |
| `#N` | Start a fresh chain for a specific issue number (skip priority selection). |
| `#N1 #N2 #N3 ...` | **Multi-issue review loop.** Fetch all listed issues, sort by priority (critical → high → normal → low), then present each one-by-one via `AskUserQuestion`. See **Multi-Issue Review Loop** below. |
| *(no flag)* | **Default: Up Next review loop.** Fetch ALL items from the Up Next column (via `--peek`), sort by priority, then run the **Multi-Issue Review Loop** over the entire queue. Same interactive dispatch/skip/hold/stop flow as multi-issue mode. |

### Session ID Parsing

When `--resume` receives a Depot session ID instead of an issue number, extract the issue number from it. Session IDs follow the convention: `issue-<N>-step<S>-<agent>-<uuid8>`. Parse `<N>` as the issue number and resume that chain.

Examples:
- `issue-621-step1-firemandecko-8d0410cd` → `--resume #621`
- `issue-300-step2-loki-a1b2c3d4` → `--resume #300`

Also accept Depot URLs: `https://depot.dev/orgs/.../claude/<session-id>` — extract the session ID from the URL path, then parse as above.

### Multi-Issue Review Loop

When multiple issue numbers are passed (`#N1 #N2 #N3 ...`), the orchestrator runs an
interactive review loop instead of batch-dispatching blindly:

**Phase 1 — Pre-fetch everything in parallel (LOOP OPTIMIZATION):**

Do ALL of the following in a single parallel batch BEFORE starting the interactive loop.
This eliminates all per-issue latency during the loop — every AskUserQuestion response
can be acted on immediately without any additional I/O.

1. **Fetch all issues in parallel:** fire one `gh issue view <N> --json number,title,body,labels`
   per issue simultaneously. Do NOT fetch them one at a time.

2. **Pre-read all needed agent templates:** from the `--peek` output, each issue has a `chain`
   field (e.g. `"FiremanDecko → Loki"`, `"Luna → FiremanDecko → Loki"`). Collect the unique
   Step-1 agents across the entire queue (e.g. `firemandecko`, `luna`, `heimdall`) and read
   ALL their template files in parallel. This means every dispatch in the loop is a single
   tool call (just the spawn) rather than read-then-spawn.

3. **Pre-resolve all blockers:** scan each issue body for `Blocked by #N` patterns. For every
   blocker found, fetch `gh issue view <N> --json number,state` in parallel. Cache the results
   so blocked issues can be flagged immediately when presented in the loop (no per-issue fetch).

4. **Sort:** `critical` → `high` → `normal` → `low`. Within the same priority, preserve the
   order Odin listed them (or peek order for the default Up Next queue).

5. **Pre-compose all prompts:** with all issue data and templates already in context, compose
   every agent prompt before entering the loop. Store them keyed by issue number. Dispatch
   becomes a single `bash dispatch-job.sh` call — no compose step inside the loop.

**Phase 2 — Interactive loop (one issue at a time):**
For each issue in priority order, present via `AskUserQuestion`:

```
Question: "#<N> — <TITLE> (<priority>/<type>) — <1-line summary from body>"
Header: "#<N>"
Options:
  - "Dispatch" — dispatch via `/dispatch #<N>` immediately
  - "Skip" — leave on Up Next, move to next issue
  - "Hold" — move issue to the "On Hold" column on the project board, continue to next issue
  - "Double check" — verify issue status matches reality before deciding
  - "Stop" — stop processing remaining issues
```

**Phase 3 — Execute decisions:**

| Response | Action |
|----------|--------|
| **Dispatch** | Invoke `/dispatch #<N> --agent <inferred-agent> --step 1`. Collect the dispatch report. Continue to next issue. |
| **Skip** | Do nothing with this issue. Continue to next issue. |
| **Hold** | Move issue to the "On Hold" column: `node pack-status.mjs --move N on-hold`. Continue to next issue. |
| **Double check** | Run a reality check on this issue (see below), then re-present the same issue with updated context. |
| **Stop** | Immediately stop the loop. Do not process remaining issues. Report what was dispatched so far. |

#### Double Check — Reality Verification

When Odin selects "Double check", run these checks before re-presenting the issue:

1. **Branch check:** `git ls-remote --heads origin | grep <issue-number>` — does a branch already exist?
2. **PR check:** `gh pr list --search "<issue-number>" --state all --json number,title,state,headRefName` — any open/merged PRs?
3. **Agent dispatch check:** `kubectl get jobs -n fenrir-agents -l issue=<issue-number> --no-headers 2>/dev/null` and check `--chain-status <N>` — was an agent already dispatched?
4. **Issue comments:** `gh issue view <N> --json comments` — any handoff/verdict comments already posted?
5. **Board position:** Confirm the issue is actually in the column pack-status says it is.

Present findings as a brief status block before re-asking the same question:

```
**Double check #<N>:**
- Branch: `fix/issue-<N>-...` exists / none found
- PR: #<PR> (open/merged/none)
- Agent: dispatched step 1 FiremanDecko (running/succeeded/none)
- Handoff: FiremanDecko → Loki posted / none
- Verdict: PASS / FAIL / none
- Board: Up Next (confirmed)

→ Re-presenting for decision...
```

Then re-present the same `AskUserQuestion` with the same options. This lets Odin
make an informed dispatch/skip/hold decision after seeing the real state.

**Phase 4 — Summary report:**
After the loop completes (or is stopped), output a single summary:

```
## Dispatch Summary

| # | Title | Decision |
|---|-------|----------|
| 1397 | fix: exclude tests from coverage | Dispatched → session-id |
| 1406 | Karl tab styling | Skipped |
| 1416 | Thrall E2E timeout | Dispatched → session-id |
| 1415 | WSS status badge | Stopped (not processed) |
```

All dispatched issues are dispatched in sequence (not parallel) so Odin can adjust
decisions based on what was already dispatched. Each dispatch fires immediately after
Odin says "Dispatch" — do not batch them.

---

## Pack Status Script

All data queries go through the pack-status script. **Do not use `gh project item-list` or manual GraphQL.**

```bash
SCRIPT_DIR="$(git rev-parse --show-toplevel)/.claude/skills/fire-next-up/scripts"
node "$SCRIPT_DIR/pack-status.mjs" <subcommand>
```

| Subcommand | Returns |
|------------|---------|
| `--status` | Full dashboard JSON (in-flight chains, up-next queue, verdicts, actions) |
| `--peek` | Prioritized Up Next queue JSON (sorted by priority → type → issue number) |
| `--chain-status N` | Single issue chain analysis JSON |
| `--resume-detect N` | Chain position + next agent + completed steps JSON |
| `--move N <up-next\|in-progress\|done>` | Moves issue on project board |

`pack-status.mjs` is the sole source file — edit it directly. No build step needed.

### Dashboard Output Format

Render `--status` JSON as this markdown:

```
## Pack Status Dashboard

### In Flight (N issues)

| # | Title | Chain Position | PR | Job | Runtime | Next Action |
|---|-------|----------------|-----|-----|---------|-------------|
| 269 | Back button | Loki PASS | #286 | complete | 8m 12s | `gh pr merge 286 --squash --delete-branch` |
| 279 | Dashboard tabs | Awaiting FiremanDecko | #288 | running | 3m 45s | `/fire-next-up --resume #279` |

Use `job_runtime` and `job_status` from `--status` JSON to populate Job and Runtime columns.
Show "—" when no job data available (e.g. parent issues, old completed chains).

### Verdict Summary
- PASS, ready to merge: #X, #Y
- FAIL, needs attention: #Z
- Awaiting Loki: #A, #B
- No response (may need re-dispatch): #C

### Up Next Queue (N items)
- #X — Title (critical/bug) → `/fire-next-up #X`
- #Y — Title (high/ux) → `/fire-next-up #Y`
- #Z — Title (normal/enhancement) → `/fire-next-up #Z`
- *(show ALL items, not just top 3)*

### Research Awaiting Review
- #168 Marketing campaign plan — `/fire-next-up --resume #168`

### Suggested Next Actions (copy-paste ready)
gh pr merge 286 --squash --delete-branch   # #269 Loki PASS — merge it
/fire-next-up --resume #277                # Loki QA needed
/fire-next-up --resume #279                # FiremanDecko needed
/fire-next-up --resume #168                # Research review needed
```

### Auto-Advance Rules (`--resume` without #N — SCOPED COMMANDS EXCLUDED)

> **SCOPE:** These rules apply **only** when `--resume` is called **without** an issue number.
> When `--resume #N` is given, skip this section entirely — only advance issue N via `--resume-detect N`.
> No other in-progress chains are scanned, dispatched, or merged.

When `--resume` (no #N) finds actions that are clearly ready, execute them immediately:

| Condition | Auto-Action |
|-----------|-------------|
| Luna done (handoff exists) | Dispatch FiremanDecko on same branch |
| FiremanDecko/Heimdall done (handoff exists) | Dispatch Loki on same branch |
| Loki PASS + CI green + PR open | Merge PR, then close issue: `gh issue close N` |
| Loki PASS + no open PR (already merged) | Close issue if still open: `gh issue close N` |
| Completed chain still in "In Progress" | No action needed (GitHub auto-archives) |
| Research handoff + PR merged + issue open | Present research review to Odin |

**Only pause for Odin's approval on:** ambiguous situations or FAIL verdicts.

**Do NOT pause for:** merges, Loki dispatches, or any other obvious action.
Execute all clear-cut actions immediately and report what was done in the dashboard output.

**Board automation (GitHub Projects V2 built-in workflows):**
GitHub automatically handles these board transitions — do NOT move items manually for these:
- PR opened/linked → **In Progress** (auto)
- PR merged → **Done** (auto)
- Issue closed (via `Fixes #N`) → **Done** (auto)
- Stale Done items → **Archived** (auto)

The orchestrator only moves items manually for:
- `--move N up-next` — when filing new issues
- `--move N in-progress` — belt & suspenders when dispatching agents (redundant with PR auto-move, but ensures the issue moves even before the PR exists)

---

## Research Review Flow

When `--resume` detects a completed research chain (handoff comment exists, PR merged, issue still open), the orchestrator runs the review flow instead of spawning another agent.

### Detection

The dashboard and `resumeDetect()` identify research issues where:
- Has a `## Freya Handoff` or `## FiremanDecko Handoff` comment (without `→ Loki`)
- PR is merged (check via `gh pr list --state merged --head <branch>`)
- Issue is still open
- These show as `next_action: "review"` in the dashboard

### Review Presentation

Read the deliverable file(s) from the merged PR, then present to Odin:

```
**Research Complete: #<N> — <TITLE>**
**Agent:** <Freya/FiremanDecko>
**Deliverable:** `<file path>`

**Key findings:**
- <3-5 bullet summary from the deliverable>

**Odin — what's the call?**
1. **Plan it** → Break findings into actionable issues via /plan-w-team
2. **Shelve it** → Close issue, findings stay in repo for future reference
3. **Drop it** → Close issue, delete the deliverable file
```

### Odin's Decision

| Response | Action |
|----------|--------|
| **Plan it** | Read the deliverable, invoke `/plan-w-team` with the research as input context. Close the research issue with a comment linking to the new issues. Move to **Done**. |
| **Shelve it** | Close the issue with comment: "Shelved — deliverable at `<path>` for future reference." Move to **Done**. |
| **Drop it** | Delete the deliverable file, commit, close issue. Move to **Done**. |

---

## Dispatch Flow

### Step 1 — Select the Issue(s)

**Default (no flag):** Run `--peek` to get ALL Up Next items sorted by priority. Then run
Phase 1 of the **Multi-Issue Review Loop** (parallel pre-fetch) before entering the loop.

**Single issue (`#N`):** Use that issue directly — skip to Step 2 refinement.

**Multi-issue (`#N1 #N2 ...`):** Run Phase 1 of the Multi-Issue Review Loop (parallel
pre-fetch of all issues, templates, and blockers), then enter the loop.

> **Loop mode:** When the queue has 2+ issues, ALL issue fetches, agent template reads,
> blocker checks, and prompt composition happen in Phase 1 before any `AskUserQuestion`
> is shown. See **Multi-Issue Review Loop → Phase 1** for the full pre-fetch spec.
> For single-issue dispatch, fetch the issue and read the template before Step 2.

Before dispatching, check body for `Blocked by #N` — if blocking issue is open, warn and ask (single) or skip (batch).

### Step 2 — Refine with Odin

Present the selected issue:

```
**Issue #<NUMBER>**: <TITLE>
**Type:** <type label> | **Priority:** <priority label>
**Chain:** <Agent1> → <Agent2> [→ <Agent3>]

**Summary:** <3-4 sentences>
**Proposed approach:** <1-2 sentences>
**Acceptance criteria:** <bullet list>

Odin — does this look right? Any adjustments before I fire it off?
```

| Response | Action |
|----------|--------|
| Approval | Proceed to spawn. |
| Scope adjustment | Update agent prompt. |
| Rejection | Skip, pick next. |
| Different issue | Switch issue. |
| Interview request | Run **local design interview** (Step 2b). |

**Skip refinement when:** `--batch`, `skip-refinement` in body, or `--resume`.
**Always refine when:** First dispatch (Up Next → In Progress).

#### Step 2b — Local Design Interview

When Odin requests: adopt agent persona locally, ask 4-6 questions, post summary comment on issue. Return to remote execution.

### Step 3 — Dispatch via /dispatch

After refinement, delegate all spawning to `/dispatch`:

**Fresh dispatch:**
```
/dispatch #<NUMBER> --agent <agent> --step 1
```

**Chain continuation (resume):**
```
/dispatch #<NUMBER> --agent <next-agent> --step <N> --branch <existing-branch>
```

**Batch dispatch:**
```
/dispatch #N1 #N2 #N3 --parallel
```

**Refinement re-dispatch:**
```
/dispatch #<NUMBER> --agent <same-agent> --step <N> --branch <branch> --prompt-extra "<Odin's notes>"
```

**CI bounce-back:**
```
/dispatch #<NUMBER> --agent loki --step <N> --branch <branch> --template loki-bounce-back --prompt-extra "<CI failure details>"
```

**Local execution:**
Add `--local` to any of the above.

**Dry run (preview prompt without spawning):**
```
/dispatch #<NUMBER> --agent <agent> --dry-run
```

---

## Chain Continuation

Depot: fire-and-forget. User continues with `/fire-next-up --resume #N`. Read `templates/resume-flow.md`.

Local: when background agent completes, check result → spawn next agent on same branch → Loki = final step, report PR URL.

---

## Reports

Read `templates/reports.md` for dispatch summary, step transition, and chain completion report formats.

---

## Pre-Flight (Local Mode)

```bash
REPO_ROOT=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
git worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //' | while read -r wt; do
  [ "$wt" = "$REPO_ROOT" ] && continue
  echo "$wt" | grep -q '\.claude/worktrees/.*\.claude/worktrees/' && \
    git worktree remove "$wt" --force 2>/dev/null || rm -rf "$wt"
done
git worktree prune
```

After chain completes, clean up worktrees for the issue:

```bash
for wt in "$REPO_ROOT/.claude/worktrees/issue-<NUMBER>-"*; do
  [ -d "$wt" ] && git worktree remove "$wt" --force 2>/dev/null || rm -rf "$wt"
done
git worktree prune
```

---

## Rules

- One chain per invocation unless `--batch`.
- The orchestrator **coordinates** — never do an agent's work yourself.
- Each agent handles its own commits and pushes.
- For `test` issues, Loki is both first and final agent.
- Board transitions are handled by GitHub Projects V2 built-in workflows (PR opened → In Progress, PR merged → Done, issue closed → Done). `/dispatch` also moves issues to In Progress as belt & suspenders.
- **All agent spawning goes through `/dispatch`.** Never call `depot claude` directly.
- **Always use `AskUserQuestion` when asking Odin anything.** Never output a question as plain text and wait — use the `AskUserQuestion` tool so Odin gets a proper prompt. This applies to ALL interaction points: refinement questions, blocked-issue warnings, research review decisions, FAIL verdict approvals, design interview questions, and any other situation where you need Odin's input before proceeding.
