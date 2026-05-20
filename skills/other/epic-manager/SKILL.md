---
name: epic-manager
description: >
  Monitor epic progress and dispatch next ready stories. Reads the [Epic] tracker
  issue body from GitHub, cross-references live issue states and active GKE K8s jobs,
  prints a wave-by-wave dashboard, and identifies what's ready to dispatch next.
  Use when the user says 'epic status', 'epic manager', 'what's next in epic',
  '/epic-manager <N>', or provides a root issue number to track.
---

# Epic Manager

Monitor an epic's dependency graph against live GitHub + K8s state and prepare
the next wave of stories for dispatch.

**Source of truth:** The `[Epic]` tracker issue on GitHub. No local YAML files.
The tracker issue body contains the dependency graph table and tracked issues checklist.

## Input

```
/epic-manager <tracker-issue-number> [--dispatch]
/epic-manager <tracker-issue-number> --add <N> --blocked-by <N>[,N...] [--wave <N>] [--note "..."]
```

| Arg | Required | Description |
|-----|----------|-------------|
| `<N>` | Yes | Tracker issue number (must be an `[Epic]` issue) |
| `--dispatch` | No | Print ready `/dispatch` commands after the dashboard |
| `--add <N>` | No | Add issue #N to the graph (updates tracker issue body on GitHub) |
| `--blocked-by <N>[,N...]` | With `--add` | Comma-separated blockers for the new story |
| `--wave <N>` | No | Override auto-computed wave (default: max blocker wave + 1) |
| `--note "..."` | No | Optional note text |

## Help

If no issue number is provided, or `--help` / `-h` is passed, **display this help
text directly** (do NOT run the script):

```
/epic-manager — Epic dependency graph tracker + dispatch advisor

USAGE
  /epic-manager <N>                          Show dashboard for epic tracker #N
  /epic-manager <N> --dispatch               Dashboard + copy-paste dispatch commands
  /epic-manager <N> --json                   Machine-readable JSON output
  /epic-manager <N> --add <M> --blocked-by <X>[,Y]   Add story #M to epic graph

DASHBOARD EXAMPLES
  /epic-manager 1526                         Live status of Odin's Spear epic
  /epic-manager 1527 --dispatch              Dashboard + ready dispatch commands

ADD STORY EXAMPLES
  /epic-manager 1526 --add 1507 --blocked-by 1495
  /epic-manager 1526 --add 1508 --blocked-by 1495 --wave 3

DASHBOARD ICONS
  ✅  done      — GitHub issue is CLOSED
  🔄  running   — Active K8s job found for this issue
  🟢  ready     — All blockers closed, not yet running
  🔴  blocked   — One or more blockers still OPEN

SOURCE OF TRUTH
  The [Epic] tracker issue body on GitHub contains the dependency graph.
  No local YAML files — GitHub is the single source of truth.
```

## Speed Rules (UNBREAKABLE)

1. **One tool call.** Run the MJS script directly — no pre-fetching, no narration between calls.
2. **Never re-fetch what the script already fetches.** The script queries GitHub and K8s itself.
3. **If the issue is not an `[Epic]` tracker**, tell Odin to check the issue number.
4. **If no issue number or `--help`**, display the Help section above — do NOT run the script.

## Execution

```bash
node .claude/skills/epic-manager/epic-manager.mjs <N> [--dispatch]
```

That is the entire execution. No other tool calls needed unless the output requires
follow-up action (e.g., dispatching a ready story).

## What the Script Does

### Phase 1 — Load epic graph from GitHub
Fetches the `[Epic]` tracker issue body via `gh issue view <N>`.
Parses the dependency graph markdown table:
```
| Wave | Issue | Title | Depends On |
|------|-------|-------|------------|
| 0 | #1516 | Migrate trial store | — |
| 1 | #1519 | Remove Redis client | #1516, #1517, #1518 |
```

### Phase 2 — GitHub state sync
For every issue number in the graph (stories + their blockers), calls:
```
gh issue view <N> --json number,state,title
```

### Phase 3 — K8s job sync
Queries active GKE jobs in `fenrir-agents` namespace:
```
kubectl get jobs -n fenrir-agents -o json
```
Only jobs with `status.active > 0` are counted as running.

### Phase 4 — Status computation
| Status | Condition |
|--------|-----------|
| `done` | GitHub state = CLOSED |
| `running` | Active K8s job found for this issue |
| `blocked` | One or more `Depends On` issues are still OPEN |
| `ready` | None of the above — all blockers closed, not running |

### Phase 5 — Dashboard output
Wave-by-wave table with icons (same format as before).

### --add mode
When `--add` is used, the script updates the tracker issue body directly on GitHub:
- Adds a new row to the dependency graph table
- Adds the issue to the tracked issues checklist
- No local files modified

## After the Dashboard

**Always use `AskUserQuestion` when asking Odin anything.** Never output a question as
plain text and wait — use the `AskUserQuestion` tool so Odin gets a proper prompt.

**Always show a summary before asking.** Before every `AskUserQuestion`, output a brief
markdown summary of the issues in question so Odin has context without needing to look
them up. Format:

```
**Ready to dispatch (Wave N):**
- #X — <title> (type/priority) — <1-line summary from issue body>
- #Y — <title> (type/priority) — <1-line summary from issue body>
```

or for stalls:
```
**Epic stalled — nothing ready or running:**
- N done, N blocked, 0 ready, 0 running
- Next unblock: #X needs #Y to close first
```

Then immediately follow with the `AskUserQuestion` call. The summary and the question
should appear in the same response — no extra round-trip.

Read the output and:

1. **If stories are ready** — summarize the ready issues with titles, types, and priorities,
   then use `AskUserQuestion`: *"Wave N is unblocked. Dispatch?"*
   Options: "Dispatch #X", "Dispatch all in parallel", "Skip". Then invoke `/dispatch`
   or `/fire-next-up #X #Y` accordingly.
2. **If nothing is ready and nothing is running** — summarize the blockage chain, then use
   `AskUserQuestion` to flag the stall. Options: "Re-check", "Close epic".
3. **If epic is complete** — congratulate and close the tracker issue immediately
   (do NOT ask for confirmation):
   ```bash
   gh issue close <N> --comment "🎉 Epic complete — all stories done."
   ```

## Rules

1. **Always run the script** — never manually reconstruct the dashboard from memory.
2. **K8s query is best-effort** — if `kubectl` is unavailable, the script continues without K8s data.
3. **Never dispatch without showing the dashboard first** — Odin must see the state before agents are spawned.
4. **GitHub is the source of truth** — the tracker issue body contains the dependency graph. No local YAML files.
5. **`--add` updates GitHub directly** — the tracker issue body is edited in-place via `gh issue edit`.
