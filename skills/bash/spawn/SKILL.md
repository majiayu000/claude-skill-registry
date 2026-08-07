---
name: spawn
description: Spawn full peer agent sessions in their own terminal panes and git worktrees — real sessions, not subagents — each on a directed task with a contract brief, monitored and merged back by the spawning lead. Herdr drives it; from a Codex lead the herdr socket needs an unsandboxed session, or the user runs the printed commands. Use when work must outlive or run beside the current session, needs its own worktree, or should stay steerable by the user in a visible pane. Spawns Codex or Claude Code peers alike.
---

# Spawn

You are the **lead**. A spawned peer is a **full agent session** — its own context window, its own approval flow, its own lifetime, steerable by the user in a visible pane. That makes it a third kind of delegate, above the two the Codex library already has:

| Tier | What it is | Lifetime | Reach it via |
|---|---|---|---|
| subagent | `spawn_agent` child — context isolation, same model | dies with the thread | `$46-orchestrate` |
| one-shot | fresh `codex exec` / `claude -p` process | one turn, deliberately not resumable | advisor and peer scripts |
| **spawned peer** | full interactive session, own pane + worktree | survives you; user-steerable | this skill |

## Preflight — the sandbox gate

Everything here drives the herdr socket through the `herdr` CLI, and the socket lives outside the workspace (`~/.config/herdr/herdr.sock`). Gate first, fail closed:

1. `HERDR_ENV=1`? If not, you are not inside herdr — jump to Fallbacks.
2. `herdr status` — if it answers, you have socket access; proceed.
3. `Operation not permitted` or `PermissionDenied` under `workspace-write` means the Codex sandbox blocks the out-of-workspace socket (both directions verified 2026-08-06). Two honest paths, both routed through the user: switch to Full Access (`/permissions` in a live interactive session, or a relaunch with `--sandbox danger-full-access`, either only with their explicit authorization — a custom permissions profile can also allowlist this one socket), or print the exact command sequence below for them to run in a normal shell. At `danger-full-access`, Codex does not block the socket. A failure there instead points to Herdr not running, a missing socket, or ordinary host permissions. Preserve and report the actual error. Never silently skip the spawn and never pretend a peer exists.

## When to spawn — and when not

Fire on any one signal:

- the work must **survive this session** or run long beside it
- it needs **its own git worktree** (a separate working copy of the repository on its own branch, so nothing it edits collides with yours) — large parallel edits where sessions would otherwise keep touching the same files
- the user should **watch and steer it live** in its own pane
- it needs a **different agent, model, or permission surface** than your session — including a genuinely decorrelated Claude peer with a lifetime

Do not spawn for a bounded consult (`$advisor`), mechanical bounded work (a `spawn_agent` child or a Luna one-shot), or a read-only question. A peer costs a worktree, a pane, and a merge — spend that only when the lifetime, the pane, or the isolation is the point.

## Spawn a peer

Each command emits JSON carrying the ids the next one needs. `worktree create` returns the workspace id, the checkout path, and a root pane already open at a shell prompt, so a fresh spawn needs no `tab create` at all (`herdr tab create --workspace <WS_ID> --cwd <WT_PATH> --no-focus` is for additional tabs, each with its own root pane). If you lose an id, re-find it with `herdr worktree list`, `herdr agent list`, or `herdr api snapshot`. Parse the JSON — never scrape human-readable output, since the CLI drifts across stable and preview channels. The command tool also runs each call in a fresh shell: `$slug` and captured ids do not persist between calls, so redeclare them per call or substitute literally.

```bash
slug=fix-ingest    # short dashed name, 2–4 lowercase words, e.g. fix-ingest — names the branch, the workspace label, and the agent
herdr worktree create --branch "spawn/$slug" --label "$slug"   # JSON — workspace_id, checkout path, root pane_id
# write the brief before starting the agent (next section) → <WT_PATH>/.spawn/brief.md
herdr agent start "$slug" --kind codex --pane <PANE_ID>        # the root pane; or --kind claude; agent flags go after --
herdr agent prompt "$slug" "Read .spawn/brief.md and begin. Reply here when the acceptance checks pass."
```

`--base <ref>` on `worktree create` pins the baseline when main is moving under you.

Permissions match yours, not a hardcoded default. Before starting the peer, read your own pane to see your live approval setting: `herdr agent read "$HERDR_PANE_ID" --lines 3`. A Claude peer takes `-- --permission-mode <mode>` with the matching value (`acceptEdits | auto | bypassPermissions | manual | dontAsk | plan`); a Codex peer takes its own equivalent sandbox or approval flags after `--`. Skip this and the peer falls back to its own tool's configured default, which can silently diverge from what you're actually running — check, don't assume. The visible pane is still the safety net either way, since herdr surfaces `blocked` the moment a peer asks for something its mode doesn't cover. If your own mode already grants broad access, the peer inherits that same exposure: worktree isolation confines its *file* edits, never its shell commands.

## Write the brief first

The brief is a file (`<WT_PATH>/.spawn/brief.md`), not an inline prompt. It survives the peer's own compaction and sits in the worktree at merge-review time as the audit record. The kickoff prompt is one line pointing at it. Use this library's own delegation contract, the same fields `$46-orchestrate` gives any worker: **Objective · Inputs and authoritative paths · In scope · Out of scope · Constraints and invariants · Write ownership · Expected artifact · Acceptance checks · Return format** (conclusion, evidence, changed files, residual risk). Then three spawn-specific lines:

```markdown
Branch etiquette — commit to spawn/<slug>; never merge, never push; do not commit .spawn/.
Suggested skills — list each Codex sibling as `$name`; for a Claude peer, use `/oss:name` only for the corresponding Claude-side skill.
Baseline — the commit this worktree was cut from. Reference artifacts by path at that commit; never paste secrets into the brief.
```

Once per repo, add `.spawn/` to `.git/info/exclude` — worktrees share it, so every peer's brief stays untracked with no `.gitignore` churn.

## Monitor without babysitting

Run the two-step wait as a foreground command with output to a file. Let the Codex command tool yield a live process handle, poll that handle, and read the file when it settles — your context never grows from polling. Do not append shell `&`: detached jobs are not preserved reliably by the Codex sandbox harness.

```bash
( herdr agent wait "$slug" --until working --timeout 15000 || true
  herdr agent wait "$slug" --timeout 3600000 ) > /tmp/spawn-$slug.wait 2>&1
```

Then judge the true state, since the agent's word is not the artifact: `herdr agent read "$slug" --lines 60`, plus `git -C <WT_PATH> status --porcelain` and `git -C <WT_PATH> log --oneline -3`. A blocked peer: `agent read` first. A question you can answer → `herdr agent prompt`. A TUI dialog → `herdr agent send-keys`. A judgment call → `herdr agent focus` and tell the user which pane and why.

## Integrate and clean up

1. The peer commits on `spawn/<slug>` and stops — it never merges (the brief says so).
2. Review from the main checkout: `git log main..spawn/<slug>` and `git diff main...spawn/<slug>`. Substitute the repo's integration branch when it is not `main`.
3. If main moved, have the **peer** rebase and re-run its acceptance checks — it holds the conflict context.
4. Merge from the main checkout and run the acceptance checks yourself; you retain integration ownership.
5. `herdr worktree remove --workspace <WS_ID>`, then `git branch -d spawn/<slug>`.

`--force` on `worktree remove` only when the agent is idle or done AND the worktree porcelain is empty — or the work is deliberately abandoned. With several peers, merge one at a time and rebase the next between merges.

## Fallbacks

**`$TMUX` set:** `git worktree add ../<repo>-spawn-<slug> -b spawn/<slug>`, then `tmux split-window -P -F '#{pane_id}' -c <WT_PATH>`, then `send-keys` the agent command (`codex` or `claude`) followed by the kickoff line. Monitor with `capture-pane -p | tail -30`. There is no state detection here — the human is the `blocked` detector.

**Plain terminal:** Claude peers only, `( cd <WT_PATH> && claude --bg --name "$slug" "Read .spawn/brief.md and begin." )`, managed with `claude agents`.

Under a restricted sandbox, both fallbacks are user-run too. The tmux socket and sibling-directory worktree writes may be equally blocked.

## Gotchas

- `agent prompt --wait` from an idle agent demands an observed state change within 5000 ms or returns `agent_prompt_stalled` — and it matches *states*, not turns. Use the two-step wait.
- `agent wait` is **indefinite without `--timeout`**. Always bound it.
- **A worktree sees only committed state.** Uncommitted lead-side edits are invisible to the peer — commit first, and name the baseline commit in the brief.
- A peer with an interactive approval policy sits `blocked` at an approval or question UI until someone answers; a peer running with approvals disabled rejects disallowed actions instead. Attend its first minute, or pass the lead's own live mode (see Permissions above) so the peer starts already matched to what you're running.
- Forgot to pass a mode? The peer used its own tool's configured default, not yours — check with `herdr agent read <name> --lines 3` and restart it with the right flag if the two diverge.
- `agent prompt` submits a *turn*; TUI dialogs need `agent send-keys`.
- A peer starts on the **user's** default model and effort, not yours — pin with agent flags after `--` when the tier matters (observed 2026-08-06: a Fable lead spawned a Sonnet-default peer).
- `HERDR_*` variables exist only inside herdr — and spawned tabs inherit them, so peers can themselves spawn.
- The same branch cannot be checked out in two worktrees. Merge from the main checkout; delete the branch only after `worktree remove`.

## Notes

- Heritage: generalizes Matt Pocock's `claude-handoff` (MIT, [mattpocock/skills](https://github.com/mattpocock/skills)). See [`RECOMMENDED.md`](../../RECOMMENDED.md). The Claude-side twin is `/oss:spawn`.
- The herdr surface (worktree, tab, and agent commands; state detection) was verified 2026-08-06 on herdr 0.7.5. Codex-lead socket access depends on the sandbox, hence the preflight gate. When the gate fails, the user-runs-commands path always works.
- The library's other cross-model calls (`sol-advisor.sh`, `claude-peer.sh`, committee members) are deliberately isolated one-shots; a spawned peer is the opposite — persistent, steerable, resumable. Choose by whether the work needs a lifetime.
