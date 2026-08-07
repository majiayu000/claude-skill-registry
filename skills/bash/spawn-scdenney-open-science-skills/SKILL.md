---
name: spawn
description: Spawn full Claude Code peer sessions in their own terminal panes and git worktrees — real sessions, not subagents — each on a directed task with a contract brief, monitored and merged back by the spawning lead. Detects the environment and takes the strongest path — herdr first, then tmux, then a native claude background agent. Use when work must outlive or run beside the current session, needs its own worktree or its own permission settings, should stay steerable by the user in a visible pane, or when the user asks to spawn, hand off, or parallelize across full sessions. Also spawns Codex peers into the same panes. Not for bounded consults or work a subagent covers.
argument-hint: "[describe the task(s) to run in spawned peer sessions; one worktree and brief per task]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Spawn

<p align="center"><img src="assets/architecture.svg" alt="spawn: a lead session detects its environment (herdr, tmux, or plain terminal), creates a git worktree per task, starts full peer sessions in new panes, briefs each by contract, monitors without babysitting, and merges each branch back." width="900"></p>

You are the **lead**. A spawned peer is a **full Claude Code session** — its own context window, its own permission prompts, its own lifetime, steerable by the user in a visible pane (a split of the terminal window the user can watch and type into). That makes it a third kind of delegate, above the two the library already has:

| Tier | What it is | Lifetime | Reach it via |
|---|---|---|---|
| subagent | in-session worker inside your context budget | dies with your turn | `Agent` tool (orchestrate skills) |
| one-shot | fresh `claude -p` / `codex exec` process | one turn, deliberately not resumable | advisor and peer scripts |
| **spawned peer** | full interactive session, own pane + worktree | survives you; user-steerable | this skill |

## When to spawn — and when not

Fire on any one signal:

- the work must **survive this session** or run long beside it
- it needs **its own git worktree** (a separate working copy of the repository on its own branch, so nothing it edits collides with yours) — large parallel edits where sessions would otherwise keep touching the same files
- the user should be able to **watch and steer it live** in its own pane
- it needs **different permission settings or a different model** than your session (say, allowed to edit files without asking)

Do not spawn for a bounded consult (`advisor`), mechanical bounded work (a `fast-worker` subagent), or a read-only question (a `claude -p` one-shot). A peer costs a worktree, a pane, and a merge — spend that only when the lifetime, the pane, or the isolation is the point.

## Detect the environment

| Check, in order | You are in | Path |
|---|---|---|
| `HERDR_ENV` is set | herdr | full path below — worktree, tab, agent lifecycle |
| `$TMUX` is set | tmux | worktree + pane, manual monitoring (Fallbacks) |
| neither | plain terminal | `claude --bg` background agent, no pane (Fallbacks) |

## Spawn a peer — herdr, the verified path

Each command emits JSON carrying the ids the next one needs. `worktree create` returns the workspace id, the checkout path, and a root pane already open at a shell prompt, so a fresh spawn needs no `tab create` at all (`herdr tab create --workspace <WS_ID> --cwd <WT_PATH> --no-focus` is for additional tabs, each with its own root pane). If you lose an id, re-find it with `herdr worktree list`, `herdr agent list`, or `herdr api snapshot`. Parse the JSON — never scrape human-readable output, since the CLI drifts across stable and preview channels. Each Bash call is also a fresh shell: `$slug` and captured ids do not persist between calls, so redeclare them per call or substitute literally.

```bash
slug=fix-ingest    # short dashed name, 2–4 lowercase words, e.g. fix-ingest — names the branch, the workspace label, and the agent
herdr worktree create --branch "spawn/$slug" --label "$slug"   # JSON — workspace_id, checkout path, root pane_id
# write the brief before starting the agent (next section) → <WT_PATH>/.spawn/brief.md
herdr agent start "$slug" --kind claude --pane <PANE_ID>       # the root pane; agent flags go after --  (e.g. -- --model opus)
herdr agent prompt "$slug" "Read .spawn/brief.md and begin. Reply here when the acceptance checks pass."
```

`--base <ref>` on `worktree create` pins the baseline when main is moving under you.

Permissions match yours, not a hardcoded default. Before starting the peer, read your own pane to see your live mode: `herdr agent read "$HERDR_PANE_ID" --lines 3`. The status line names it directly (for example, "accept edits on" or "bypass permissions on"). Pass the matching flag after `--`, `--permission-mode <mode>`, one of `acceptEdits | auto | bypassPermissions | manual | dontAsk | plan`. Skip this and the peer falls back to Claude Code's own configured default (`~/.claude/settings.json`'s `permissions.defaultMode`), which can silently diverge from what you're actually running. This very session, for instance, is configured to `auto` but its live status line currently reads `bypassPermissions`, because the mode was cycled mid-session — only the self-read catches that gap. The visible pane is still the safety net either way, since herdr surfaces `blocked` the moment the peer asks for something its mode doesn't cover. If your own mode already grants broad access, the peer inherits that same exposure: worktree isolation confines its *file* edits, never its shell commands.

## Write the brief first

The brief is a file (`<WT_PATH>/.spawn/brief.md`), not an inline prompt. A real brief is too long to pass on the command line, survives the peer's own compaction for re-reading, and sits in the worktree at merge-review time as the audit record. The kickoff prompt is one line pointing at it.

Use the delegation contract the library already runs on — the same fields you would give any delegate: **Objective · Inputs and authoritative paths · In scope · Out of scope · Constraints and invariants · Write ownership · Expected artifact · Acceptance checks · Return format** (conclusion, evidence, changed files, residual risk). Then three spawn-specific lines:

```markdown
Branch etiquette — commit to spawn/<slug>; never merge, never push; do not commit .spawn/.
Suggested skills — the /oss: skills the peer should invoke, so it does not rediscover them.
Baseline — the commit this worktree was cut from. Reference artifacts by path at that commit; never paste secrets into the brief.
```

Once per repo, add `.spawn/` to `.git/info/exclude` — worktrees share it, so every peer's brief stays untracked with no `.gitignore` churn.

## Monitor without babysitting

One Bash call with `run_in_background: true` — you are notified when it exits, and your context never grows from polling:

```bash
herdr agent wait "$slug" --until working --timeout 15000 || true   # confirm launch; times out harmlessly if the peer already finished
herdr agent wait "$slug" --timeout 3600000                         # settles on idle | blocked | done
```

When the notification fires, judge the true state — the agent's word is not the artifact:

```bash
herdr agent read "$slug" --lines 60
git -C <WT_PATH> status --porcelain && git -C <WT_PATH> log --oneline -3
```

A blocked peer: `agent read` first. A question you can answer → `herdr agent prompt`. A TUI dialog (a permission menu) → `herdr agent send-keys`. A judgment call → `herdr agent focus` and tell the user which pane and why. Spot-check anytime with `agent read` and a small `--lines`; do not stream panes into your context.

## Integrate and clean up

1. The peer commits on `spawn/<slug>` and stops — it never merges (the brief says so).
2. Review from the main checkout: `git log main..spawn/<slug>` and `git diff main...spawn/<slug>` — worktree branches are visible with no fetch. Substitute the repo's integration branch when it is not `main`.
3. If main moved, have the **peer** rebase and re-run its acceptance checks — it holds the conflict context, you do not.
4. Merge from the main checkout and run the acceptance checks yourself. You retain integration ownership — of correctness and of rigor.
5. `herdr worktree remove --workspace <WS_ID>`, then `git branch -d spawn/<slug>`.

`--force` on `worktree remove` only when the agent is idle or done AND `git -C <WT_PATH> status --porcelain` is empty — or the work is deliberately abandoned. With several peers, merge one at a time and rebase the next between merges: worktrees prevent write collisions, not merge collisions.

## Fallbacks — tmux, then claude --bg

**tmux** (`$TMUX` set): same brief, manual lifecycle.

```bash
git worktree add "../$(basename "$PWD")-spawn-$slug" -b "spawn/$slug"
pane=$(tmux split-window -P -F '#{pane_id}' -c "<WT_PATH>")   # or new-window -n "$slug"
tmux send-keys -t "$pane" 'claude' Enter
# wait for the REPL to draw, then:
tmux send-keys -t "$pane" 'Read .spawn/brief.md and begin.' Enter
```

Monitor with `tmux capture-pane -p -t "$pane" | tail -30`. There is no agent-state detection — the pane is your `agent read`, and the human is your `blocked` detector.

**Plain terminal** (neither): same worktree, no pane.

```bash
git worktree add "../$(basename "$PWD")-spawn-$slug" -b "spawn/$slug"
( cd <WT_PATH> && claude --bg --name "$slug" "Read .spawn/brief.md and begin." )
```

Manage with `claude agents` — coarser steering, same brief, same merge-back.

## Gotchas

- `agent prompt --wait` from an idle agent demands an observed state change within 5000 ms or returns `agent_prompt_stalled` — and it matches *states*, not turns, so an already-working agent's current turn can satisfy it. Use the two-step wait idiom instead.
- `agent wait` (and `agent prompt --wait`) are **indefinite without `--timeout`**. Always bound them.
- **A worktree sees only committed state.** Uncommitted lead-side edits are invisible to the peer — commit first, or copy the file into the worktree, and name the baseline commit in the brief.
- A peer whose mode still prompts (e.g. `manual`, `dontAsk`, plain `auto`) sits `blocked` at its first permission prompt until someone answers. Attend its first minute, or pass the lead's own live mode (see Permissions above) so the peer starts already matched to what you're running.
- Forgot to pass a mode? The peer used Claude Code's configured default, not yours — check with `herdr agent read <name> --lines 3` and restart it with the right `--permission-mode` if the two diverge.
- `agent prompt` submits a *turn*; TUI dialogs need `agent send-keys`.
- A peer starts on the **user's** default model and effort, not yours — pin with `-- --model … --effort …` when the tier matters (observed 2026-08-06: a Fable lead spawned a Sonnet-default peer).
- Lost an id → `herdr worktree list`, `herdr agent list`, `herdr api snapshot`.
- `HERDR_*` variables exist only inside herdr — and spawned tabs inherit them, so peers can themselves spawn.
- The same branch cannot be checked out in two worktrees. Merge from the main checkout; delete the branch only after `worktree remove`.

## Troubleshooting

- **`agent start` times out** — the pane was not at an interactive shell prompt, or the agent binary is not on PATH in that shell. `herdr pane read <PANE_ID>` to see what the pane shows; raise `--timeout` (default 30000, max 300000) for slow cold starts.
- **`worktree create` fails** — usually an existing branch of the same name (`git branch --list 'spawn/*'`) or a repo state that cannot branch; create from a clean HEAD or pass `--base`.
- **Socket errors on every `herdr` command** — you are not inside herdr (`HERDR_ENV` unset) or the server restarted. Check `herdr status`, then fall back to tmux or `claude --bg`.

## Notes

- The library's other cross-model calls (`fable-advisor.sh`, `codex-peer.sh`, the committee members) are deliberately isolated one-shots with session persistence off; a spawned peer is the opposite — persistent, steerable, resumable. Choose by whether the work needs a lifetime.
- A **Codex peer** is one flag: `herdr agent start "$slug" --kind codex --pane <PANE_ID>` — same brief; the contract is Codex's own from `46-orchestrate`. herdr detects 21 agent kinds, so the same move spawns other agents too.
- Heritage: generalizes Matt Pocock's `claude-handoff` (MIT, [mattpocock/skills](https://github.com/mattpocock/skills)) — handoff compacts one conversation into a document for one `claude --bg` successor; spawn adds environment detection, worktree isolation, directed contract briefs, and lifecycle management for N peers. See [`RECOMMENDED.md`](../../../RECOMMENDED.md).
- Routed to by `fable-orchestrate` / `opus-orchestrate` routing row 8; standalone via `/oss:spawn`.
- herdr surface (worktree, tab, and agent commands; state detection) verified 2026-08-06 on herdr 0.7.5.
