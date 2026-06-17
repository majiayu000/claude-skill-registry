---
name: ntm
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Orchestrates NTM tmux agent swarms and robot APIs. Use when spawning/sending
  panes, reading robot state, triaging work, locks/mail, safety, pipelines,
  serve, or NTM errors.
practices:
- pragmatic-programmer
---
<!-- TOC: One Rule | Cold Start | Mandatory Loop | NTM Action Card | Command Selection Matrix | Pattern Tiers | Anti-Patterns | Pre-Flight Checklist | Quick Start | Mental Model | Session Orchestration | Dispatch & Reusable Assets | Work Intelligence | Coordination | Safety | Robot Mode | Controller Agents | Serve API | Project Resolution | Gotchas | References | Related Skills -->

> **Scope:** this skill is the **NTM tool reference** — every verb, flag, schema, and integration point. For operator loops, marching orders, unstick ladders, swarm anti-patterns, and tending cadence, use the companion `vibing-with-ntm` skill.

# NTM — Named Tmux Manager

> **The One Rule:** Discover the live NTM contract first, then use the least interactive surface that can prove and execute the action. No `--robot-capabilities` / `--robot-snapshot` evidence -> no automation assumption.

## Outcome — When an NTM Action Has Delivered

A state-changing NTM action is complete only when **all** of the following hold:

- The intended state transition is **visible in `ntm --robot-snapshot`** — not just acknowledged by the command's exit code. (NTM commands can succeed at the API layer while panes/work/locks remain unchanged; trust the snapshot, not the return value.)
- The **attention feed** (`--robot-attention` / `--robot-tail`) shows the expected event(s) — pane output, work-graph movement, lock acquire/release, mail delivery. Absence is evidence of failure.
- Adjacent state (git, br/beads, mail, pipelines) reflects the action's downstream effects within one observation window — otherwise the action fired in isolation and likely didn't accomplish its real purpose.
- Locks and pipelines you opened are either **released / completed** by you, or explicitly handed off via mail with a thread the next operator can claim. Orphaned locks block the swarm.
- For dispatched marching orders: the targeted pane has acknowledged (printed the order, started the work, or replied via mail). A sent-but-not-acknowledged order is not "done."

If the snapshot or attention feed disagrees with what the command said happened, **trust the snapshot** and re-discover the contract — the local model of NTM is stale.


## Cold Start: Which NTM Skill?

If you are coming in fresh, pick the narrowest starting point:

| Situation | Start here |
|---|---|
| You need exact NTM command syntax, robot flags, schemas, or failure-mode fixes | This skill |
| You are tending an already-running swarm and deciding whether to nudge, restart, stand down, or dispatch marching orders | `/vibing-with-ntm` |
| You are running a Brenner-style hypothesis investigation or incident RCA through NTM panes | `brennerbot-with-ntm` |
| You only need Beads or BV mechanics | `/beads-br` or `/beads-bv` |

For any state-changing action, read just enough of this file to choose the command, then verify the live contract with `ntm --robot-capabilities` before executing.

## The Loop (Mandatory)

```
1. DISCOVER   -> ntm --robot-capabilities; ntm --robot-tools; repo AGENTS.md/README.md
2. SNAPSHOT   -> ntm --robot-snapshot; inspect sources/degraded_sources, cursor, sessions, panes
3. SELECT     -> choose the smallest surface: work/assign/send/wait/pipeline/locks/mail
4. PROVE      -> fill the NTM action card: target, contract, safety, ownership, rollback
5. EXECUTE    -> prefer --robot-* for automation; avoid human-only TUIs
6. VERIFY     -> attention/events/causality/tail plus git/br/mail evidence changed as expected
7. CLEANUP    -> release/renew locks, checkpoint/handoff, prune old pipeline state when appropriate
8. REPEAT     -> re-snapshot on cursor expiry or after any state-changing action
```

The most common NTM mistake is treating it like a tmux macro runner. Current NTM is a control plane: robot API, attention feed, work graph, locks/mail, pipelines, ensembles, safety, approvals, serve API, and durability all have explicit contracts. Use the contract.

## NTM Action Card

For every state-changing NTM action, be able to answer this before running it:

```markdown
## NTM action: <command>
- Target session/project: <name/path>; resolved by: `ntm config get projects_base` / `ntm quick` / snapshot
- Live contract checked: `ntm --robot-capabilities` contains <flag>; schema/docs checked if unfamiliar
- Evidence before: cursor=<N>; sources=<fresh/degraded>; panes=<count>; locks=<summary>
- Ownership/safety: Agent Mail reservation or worktree policy is clear; user pane inclusion is intentional
- Blast radius: panes/files/sessions affected; destructive/safety/policy approvals required? <yes/no>
- Verification after: <robot event / tail movement / bead state / git change / pipeline status>
- Recovery: <smart restart / interrupt / checkpoint restore / cancel pipeline / handoff>
```

If you cannot fill the card, do a read-only discovery pass first.

## Command Selection Matrix

Score candidate surfaces when several could work:

```
Score = (ContractFit x Observability x Reversibility) / BlastRadius

ContractFit    1-5: exact robot/schema match beats human help text
Observability  1-5: action emits cursor/event/status/causality evidence
Reversibility  1-5: easy cancel/retry/restore/checkpoint
BlastRadius    1-5: one pane/file is low; whole session/process tree is high
```

Pick the highest score. In ties, prefer the surface that produces structured output.

| Need | Best first surface | Usually wrong |
|---|---|---|
| Know what exists | `ntm --robot-capabilities` | `ntm --help | grep` as sole truth |
| Tend a swarm | `--robot-snapshot` -> `--robot-attention` | fixed sleep/poll loops |
| Send machine-driven prompt | `ntm --robot-send=<session>` | `ntm send` when CASS/confirm prompts can block |
| Recover a pane | `--robot-diagnose` -> `--robot-smart-restart` | immediate hard restart |
| Run repeatable phase work | `ntm pipeline run` / `--robot-pipeline-run` | copy-paste manual dispatch |
| Explain what happened | `--robot-causality` + `--robot-events` | pane scrollback only |
| No ready work | `ntm work queue-dry --format=json` | inventing new work without duplicate/source checks |
| Cross-machine continuity | `checkpoint export` / `handoff create` | shipping attention cursors |

## Pattern Tiers

### Tier 1: Safe Read-Only Surfaces

| Pattern | Use | Proof |
|---|---|---|
| Capabilities/schema | Current command contract | Flag + params exist |
| Snapshot | Baseline state + cursor | `sources` / `degraded_sources` reviewed |
| Events/digest/attention | Tending loop | cursor advances or resync command returned |
| Work triage/queue-dry | Work selection | ready/dry status plus warnings |
| Locks list/check | Coordination truth | no conflicting active reservation |

### Tier 2: Reversible Control

| Pattern | Use | Guard |
|---|---|---|
| `--robot-send` | Directed instruction | panes/type/all explicitly scoped |
| `--robot-interrupt` | Stop wrong task | tail proves wrong task/stall |
| `--robot-smart-restart` | Recover stuck pane | refuses active work |
| `ntm assign` | Match agents to beads | ready work and ownership checked |
| `pipeline cancel/resume` | Workflow control | run id and state file confirmed |

### Tier 3: Durable Orchestration

| Pattern | Use | Guard |
|---|---|---|
| Pipelines | Repeatable multi-step work | dry-run first; state captured |
| Agent Mail / locks | Shared edits | reservation lease and thread id |
| Checkpoint / handoff | Recovery/resume | archive exists and metadata matches |
| Serve API | Long-lived integrations | auth mode and local exposure understood |
| Safety / approve / policy | Risk control | token/policy target, not bead id |

## Anti-Patterns (Never Do)

| Bad move | Why it fails | Use instead |
|---|---|---|
| Call `ntm view` from automation | Retiles the human layout and returns nothing useful | `--robot-tail`, `--robot-snapshot`, or `--robot-dashboard` |
| Trust old notes over `--robot-capabilities` | NTM surface changes quickly | Discover first |
| Send to `--all` without naming the user-pane intent | Can hit the operator pane | use type/panes or `-s/--skip-first` |
| Treat cursor values as portable | Cursors are per-server monotonic | checkpoint/handoff for portability |
| Kill/restart before a liveness proof | Destroys partial work | diagnose -> smart restart -> explicit restart |
| Conflate pipeline status and run | `--robot-pipeline=<id>` is status | `--robot-pipeline-run=<file>` |
| Retry degraded mail/CASS forever | Burns the session | record degraded source, use fallback, continue |
| Infer abandoned beads from silence | NTM deliberately does not implement `bead_orphaned` | explicit status/mail/reservation evidence |

## Pre-Flight Checklist

- [ ] Repo `AGENTS.md` / README read when operating inside a codebase.
- [ ] `ntm --robot-capabilities` checked for any unfamiliar flag.
- [ ] `ntm --robot-snapshot` captured and `sources` / `degraded_sources` reviewed.
- [ ] Session/project resolution verified; labels and `projects_base` make sense.
- [ ] User pane inclusion/exclusion is explicit.
- [ ] File ownership is clear: Agent Mail reservation, bead assignee, or approved worktree policy.
- [ ] For pipelines: dry-run passed; run id/state file plan known.
- [ ] For recovery: liveness truth stack supports intervention.
- [ ] For destructive/risky actions: safety/policy/approval surfaces checked.
- [ ] Post-action verifier named before execution.

---

> **Core capability:** Turn `tmux` into a structured, recoverable multi-agent workspace.

> **Read the repo first.** If the target repository has `AGENTS.md` or `README.md`, read those before applying this skill. Repo-local instructions override generic NTM advice.

> **Discover, don't guess.** `ntm --robot-capabilities` returns the machine-readable API schema. `ntm --robot-docs=quickstart|commands|examples|exit-codes` returns focused docs. Use these before parsing human help text or trusting stale instructions.

> **Interactive vs automation:**
> - `ntm dashboard`, `ntm palette`, and other TUI surfaces are for humans. `ntm view` retiles the operator's tmux layout and returns nothing to you — never call it from automation.
> - For machine-readable automation, prefer `--robot-*`. Set `--robot-format=toon` (or `NTM_ROBOT_FORMAT=toon`) for a token-efficient structured format, and `--robot-verbosity=terse` when context is tight.
> - Non-interactive CLI commands such as `ntm send`, `ntm work triage`, `ntm locks list`, `ntm pipeline status`, and `ntm serve` are fine when they are the clearest tool.

> **Coordination and isolation:**
> - Agent Mail reservations are the default coordination primitive.
> - `--worktrees` and `ntm worktrees ...` are supported isolation tools when the repo policy allows them.
> - If a repo `AGENTS.md` prefers reservations-only or has worktree-specific rules, follow that repo.

## Quick Start

```bash
# Install / sanity check
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ntm/main/install.sh?$(date +%s)" | bash -s -- --easy-mode
ntm deps -v

# Create or resolve a project
ntm quick myproject --template=go

# Launch a mixed swarm
ntm spawn myproject --cc=2 --cod=1 --gmi=1

# Codex fallback when --cod opens a bare shell instead of Codex
codex exec -s danger-full-access --skip-git-repo-check -C "$PWD" \
  "Read AGENTS.md, claim the assigned bead, implement only that scope, and report evidence."

# Dispatch work
ntm send myproject --cc "Map the auth layer and propose a refactor plan."

# Inspect the current work graph and system state
ntm work triage --format=markdown
ntm work queue-dry --format=json
ntm --robot-snapshot

# Discover the full surface without parsing --help output
ntm --robot-capabilities
ntm --robot-docs=commands
```

## Mental Model

NTM wraps tmux with structured metadata and durable state. Five concepts are worth internalizing:

- **Project** — resolved via `NTM_PROJECTS_BASE + <session>` (or `projects_base` config). Session name MUST equal the directory basename under that base, or agent-mail/beads/reservations register under a different key than NTM sees. This is the single most common source of cross-tool breakage.
- **Session name** — bare project (`myproject`) or labeled variant (`myproject--frontend`). `--` is the reserved label separator; project names cannot contain `--`. Labels must match `^[a-zA-Z0-9][a-zA-Z0-9_-]*$` and be ≤50 chars.
- **Pane** — a tmux pane typed as an agent (cc/cod/gmi/cursor/windsurf/aider/oc/opencode/ollama) or the user pane (index 0 by default). `ntm send` defaults **exclude** the user pane; `--all` includes it; `-s/--skip-first` explicitly skips it.
- **Attention feed** — a monotonic event stream. `--robot-snapshot` bootstraps; `--robot-events --since-cursor=N --events-limit=M` replays; `--robot-attention --attention-cursor=N` blocks until new events. Cursors are per-server monotonic and **not portable across machines**; expired cursors return a `resync_command` ready to paste.
- **Robot mode** — every state-read has a `--robot-*` variant returning structured JSON or TOON. Prefer robot mode over TUIs in all automation; `ntm view`, `ntm dashboard`, `ntm palette` are operator-only and will return nothing useful to automation (and `ntm view` additionally retiles the human's layout).

## Current Reality Snapshot

Recent NTM builds are a full operator control plane, not only a launcher:

- `--robot-capabilities` is the source of truth; the current mainline advertises 137 robot surfaces across attention, state, control, beads, BV, CASS, ensemble, pipeline, spawn, and utility lanes.
- `--oc` / opencode is a first-class agent type in spawn/add/adopt/controller paths; older docs that list only cc/cod/gmi/cursor/ws/aider/ollama are incomplete.
- Operator state now includes source-health, capture provenance, resource pressure, assurance/quiescence, and degraded coordination signals. Check `sources` and `degraded_sources` before acting on stale beads/mail/CASS-derived advice.
- Queue-dry is a concrete workflow: `ntm work queue-dry` diagnoses no-ready-work states, and `--ideate --create-beads --yes` is the explicit mutation path.
- Ensemble catalog/status/suggest surfaces are useful in normal builds, but ensemble spawn is experimental; if `--robot-ensemble-spawn` returns `NOT_IMPLEMENTED`, rebuild NTM with `-tags ensemble_experimental` or use ordinary `ntm spawn` / pipeline orchestration.
- Serve/robot pane targeting is pane-ID aware; avoid code or docs that assume `session:index` is stable under tmux base-index changes.

## Tool Selection Kernel

When you are unsure which NTM surface to use, route by intent:

| Intent | First surface | Act only after |
| --- | --- | --- |
| Discover current API shape | `ntm --robot-capabilities` | Command + parameter exists in registry |
| Understand live swarm state | `ntm --robot-snapshot` or `ntm --robot-is-working=<session>` | Relevant `sources` entry is fresh or degraded status is acknowledged |
| Pick work | `ntm work triage` / `bv --robot-triage` | Ready item is unblocked and not owned by another agent |
| No ready work | `ntm work queue-dry --format=json` | Dry queue is confirmed; warnings/guards are reviewed |
| Push work to panes | `ntm assign` or `ntm --robot-send` | File/domain ownership is clear |
| Recover a pane | `ntm --robot-diagnose`, then `--robot-smart-restart` | Liveness truth stack says the pane is not productively working |
| Integrate with scripts/services | `--robot-*` or `ntm serve` | JSON/OpenAPI contract is validated |

## Session Orchestration

Use these for day-to-day session lifecycle management:

```bash
ntm spawn myproject --cc=3 --cod=2 --gmi=1
ntm spawn myproject --label frontend --cc=2
ntm spawn myproject --label backend --cc=2 --worktrees
ntm add myproject --cc=1
ntm add myproject --label frontend --cod=1
ntm list
ntm status myproject
ntm zoom myproject 3
ntm attach myproject
ntm dashboard myproject   # human only
ntm palette myproject     # human only
```

Useful spawn patterns:

```bash
ntm spawn myproject --prompt "Read AGENTS.md and start on ready work"
ntm spawn myproject -r full-stack                          # named recipe (see `ntm recipes list`)
ntm spawn myproject -t red-green                           # named workflow (see `ntm workflows list`)
ntm spawn myproject --persona=architect --persona=implementer:2
ntm spawn myproject --stagger-mode=smart --cc=6 --cod=4    # smart|fixed|none
ntm spawn myproject --no-user --cc=5 --cod=5               # no human-driver pane
```

Adjust a running swarm instead of re-spawning:

```bash
ntm scale myproject --cc=4                # grow/shrink one agent type
ntm rebalance myproject                   # even out agents by workload
ntm swarm plan                            # show what a spawn would do
ntm swarm status                          # cross-session swarm view
ntm swarm stop <pattern>                  # stop sessions by name pattern
ntm respawn myproject                     # recover dead agents in place
ntm adopt <tmux-session>                  # bring an existing tmux session under ntm
```

### Codex spawn fallback

Treat `ntm spawn <project> --cod=N` as **provisional until observed**. Some local
NTM builds have created and registered the `cod` pane but left it at a bare `zsh`
prompt; the next sent "contract" then executes as shell text and fails with parse or
`command not found` noise.

Verification:

```bash
ntm spawn myproject --cod=1
ntm --robot-tail=myproject --panes=2 --lines=20
ntm --robot-snapshot
```

If the Codex pane is a shell instead of an active `codex` session, **do not** keep
sending prompts to that pane. Use a Codex-native one-shot worker from the repo root
or the intended worktree:

```bash
codex exec -s danger-full-access --skip-git-repo-check -C /path/to/gitdir \
  "Read AGENTS.md, claim bead <id>, implement only that scope, run the gate, and report evidence."
```

For parallel lanes, prefer one `codex exec -C <isolated-worktree>` per worker until
the live NTM `--cod` launcher is verified fixed by `--robot-tail` evidence.

## Dispatch and Reusable Assets

High-leverage NTM usage is not just `spawn` plus `send`. The real power shows up when
you combine richer dispatch patterns with reusable session and prompt assets.

```bash
ntm send myproject --all "Checkpoint and summarize blockers."
ntm send myproject --pane=2 "Own the auth migration."
ntm send --project myproject "Sync to main and report conflicts."
ntm send myproject -c internal/auth/service.go "Review this subsystem"
ntm send myproject -t fix --var issue="nil pointer" --file internal/auth/service.go
ntm send myproject --smart --route=affinity "Take the auth follow-up"
ntm send myproject --distribute --dist-strategy=dependency

ntm recipes list
ntm recipes show full-stack
ntm workflows list
ntm workflows show red-green
ntm template list
ntm template show refactor
ntm session-templates list
ntm session-templates show refactor
```

User-level and project-level assets both matter. NTM can resolve configuration from
`~/.config/ntm/...` and project-local `.ntm/...` trees, so check the repo before
assuming defaults.

## Work Intelligence

NTM is no longer just a pane launcher. It has first-class work selection and assignment:

```bash
ntm work triage
ntm work triage --by-track
ntm work alerts
ntm work search "JWT auth"
ntm work impact internal/api/auth.go
ntm work next
ntm work graph
ntm work queue-dry --format=markdown
ntm work queue-dry --ideate --format=json
ntm work queue-dry --ideate --create-beads --yes

ntm assign myproject --auto --strategy=dependency
ntm assign myproject --beads=br-123,br-124 --agent=codex
```

Use `ntm work ...` when you want NTM to wrap `bv` and present work in operator-friendly form.
Use raw `bv --robot-*` when you specifically want the graph engine's native robot output.

## Coordination and Recovery

NTM now exposes the surrounding coordination stack directly:

```bash
# Mail (Agent Mail MCP, wrapped for CLI use)
ntm mail send myproject --all "Report blockers and current file focus."
ntm mail inbox myproject                      # or: ntm mail inbox myproject --json

# File reservations (advisory locks)
ntm locks list myproject --all-agents
ntm locks check internal/auth/service.go --session myproject --pane 2 --json
ntm locks renew myproject --extend 30         # minutes
ntm locks force-release myproject 42 --note "agent inactive"

# Multi-agent coordinator
ntm coordinator status myproject              # alias: ntm coord status
ntm coordinator digest myproject
ntm coordinator conflicts myproject
ntm coordinator enable auto-assign            # background automation
ntm coordinator enable digest --interval=30m

# Durable session state
ntm checkpoint save myproject -m "before risky refactor"
ntm checkpoint list myproject
ntm checkpoint restore myproject              # latest; takes optional <id>
ntm checkpoint export myproject <id>          # portable archive
ntm checkpoint import <archive>

# Persisted timelines of agent state transitions
ntm timeline list
ntm timeline show <session-id>
ntm timeline stats

# Audit, conflict, history surfaces
ntm history search "authentication error"
ntm audit show myproject
ntm changes myproject                         # recent file changes attributed to agents
ntm conflicts myproject --since 6h            # top-level command; not a changes subcommand
ntm resume myproject                          # re-attach + context-inject after restart

# Handoff bundles for cross-machine or cross-session resumes
ntm handoff create myproject
ntm handoff list
ntm handoff show <path>
```

Isolation options:

```bash
# Coordination-first
ntm locks list myproject

# Isolation-first when policy allows it
ntm spawn myproject --cc=3 --worktrees
ntm worktrees list
ntm worktrees merge claude_1
```

## Safety and Approvals

NTM has built-in safety, policy, and approval surfaces. Use them instead of ad hoc shell habits:

```bash
ntm safety status
ntm safety check --json git status            # checks a candidate command without running it
ntm safety blocked --hours 24
ntm safety install

ntm policy show --all
ntm policy validate
ntm policy edit
ntm policy automation

ntm approve list
ntm approve show <token>
ntm approve <token>                         # approve by token (not bead/issue id)
ntm approve deny <token> --reason "wrong target branch"
ntm approve history
```

If the repo instructions require offloading builds or tests through another tool such as `rch`, obey the repo instructions.

Current hook/tool contracts to remember:

- `ntm safety install` writes `git`/`rm` wrappers plus a Claude Code PreToolUse hook. The hook reads the modern Claude JSON payload on stdin (`tool_name`, `tool_input.command`) and exits `2` to block; `CLAUDE_TOOL_*` env vars are legacy fallback only.
- NTM's DCG adapter uses DCG's real contract: `dcg doctor --format json` for status and `dcg --robot test --format json <command>` for checks. Do not document or call `dcg check`.
- RCH is external build offload. Use `rch exec -- <build command>` directly when repo rules require offloading; the NTM robot surface reports RCH health/workers, it does not replace the build command.

## Canonical Robot Mode

Start with these:

```bash
ntm --robot-help
ntm --robot-capabilities                    # canonical machine-readable API schema
ntm --robot-docs=quickstart                 # also: commands, examples, exit-codes
ntm --robot-schema=all                      # JSON Schema for every robot response
ntm --robot-status
ntm --robot-snapshot
ntm --robot-plan
ntm --robot-dashboard
ntm --robot-markdown --md-compact
ntm --robot-terse
```

Format and verbosity knobs (token-budget friendly):

```bash
ntm --robot-snapshot --robot-format=toon        # toon is far more token-efficient than json
ntm --robot-snapshot --robot-verbosity=terse    # terse | default | debug
# Env fallbacks honored: NTM_ROBOT_FORMAT / NTM_OUTPUT_FORMAT / TOON_DEFAULT_FORMAT
```

Common task-specific robot surfaces:

```bash
ntm --robot-send=myproject --panes=2 --msg="Summarize blockers." --type=claude
ntm --robot-ack=myproject --timeout=30s
ntm --robot-tail=myproject --panes=2 --lines=50
ntm --robot-mail-check --mail-project=myproject --urgent-only
ntm --robot-cass-search="authentication error"
ntm --robot-beads-list --beads-status=open
ntm --robot-bead-claim=br-123 --bead-assignee=agent1
ntm --robot-bead-close=br-123 --bead-close-reason="Completed"
```

**Polite-probe-then-act** (preferred over raw interrupt):

```bash
ntm --robot-is-working=myproject --panes=2,3    # check first
ntm --robot-smart-restart=myproject --panes=2   # refuses if the pane is actively working
ntm --robot-probe=myproject --panes=2           # responsiveness probe
ntm --robot-diagnose=myproject                  # comprehensive health + recommendations
ntm --robot-context=myproject                   # context-window usage per agent
```

Event-driven tending instead of polling:

```bash
ntm --robot-wait=myproject --wait-until=attention --timeout=5m
ntm --robot-wait=myproject --wait-until=action_required
ntm --robot-wait=myproject --wait-until=mail_ack_required
ntm --robot-events --since-cursor=42 --events-limit=50 --events-category=agent
```

Operator loop:

```text
1. Bootstrap with --robot-snapshot
2. Tend with --robot-attention or --robot-wait (blocks until an event)
3. Act with --robot-send / --robot-smart-restart / ntm send / ntm assign / ntm mail / ntm locks
4. Re-bootstrap with --robot-snapshot if the cursor expires
```

Prefer `--robot-*` when another agent or script needs structured output.

## Controller Agents

`ntm controller <session>` launches a coordinator agent in pane 1 whose job is to
watch the other agents, resolve conflicts, and drive the operator loop.

```bash
ntm controller myproject                      # default: Claude controller, coord prompt
ntm controller myproject --agent-type=cod     # cc|cod|gmi|cursor|windsurf|ws|aider|ollama
ntm controller myproject --prompt=ctrl.txt    # custom prompt template
ntm controller myproject --no-prompt          # launch agent, send no initial prompt
```

Custom prompts support template variables: `{{.Session}}`, `{{.AgentList}}`, `{{.ProjectDir}}`.

The built-in default prompt tells the controller to:

- Prefer `--robot-*` commands over interactive TUIs.
- Start with `ntm --robot-snapshot`, then block on `ntm --robot-attention --attention-session={{.Session}}`.
- Tail panes with `ntm --robot-tail={{.Session}} --panes=N --lines=50`.
- Check Agent Mail via `ntm mail inbox {{.Session}} --json` for the CLI path; use `--mail-project=` only with `--robot-mail-check`.
- Use `ntm send {{.Session}} --pane N "message"` for single pane, `--panes=1,2` for many.
- Use `ntm --robot-interrupt={{.Session}} --panes=N` to interrupt without killing.
- **Never** call `ntm view` — it retiles the human operator's tmux layout and returns nothing.

## Serve API and Pipeline Surfaces

NTM also exposes local API and durable workflow surfaces:

```bash
ntm serve --port 7337
ntm openapi generate
ntm pipeline run .ntm/pipelines/review.yaml --session myproject
ntm pipeline status run-20241230-123456-abcd
ntm pipeline list
ntm pipeline resume run-20241230-123456-abcd
ntm pipeline cleanup --older=7d
```

Use `ntm serve` for long-lived local integrations. Use `--robot-*` for single-shot agent control.

## Project Resolution

`ntm spawn` needs a project directory that NTM can resolve.

```bash
ntm config get projects_base
ntm quick myproject --template=go

# Or point projects_base at an existing repo layout / create a symlink when needed
```

The session name usually matches the project directory name. Labels extend the session name as `project--label`.

## Gotchas (distilled from real agent sessions)

These are the NTM-specific trip-wires most commonly hit in practice. Each has a full entry in `TROUBLESHOOTING.md`; these are the one-liners.

1. **Project resolution** — `NTM_PROJECTS_BASE` + session name must equal the directory basename. Mismatch breaks agent-mail registration silently. If agent-mail and ntm "see different projects," fix this first.
2. **`ntm send` default skips the user pane** — so plain `ntm send myproject --cc "msg"` is safe; `ntm send myproject --all "msg"` hits the operator's zsh. Use `-s/--skip-first` if you want `--all` agents but no user pane.
3. **CASS dedup blocks sends** — default `--cass-check=true` with 0.7 similarity, 7-day lookback. If `ntm send` aborts with "similar past prompt," either add a rotating suffix (e.g. `"... pass 17 at 16:40"`) or pass `--no-cass-check`. In robot automation, `--robot-send` is non-interactive and never prompts.
4. **Label separator is literal `--`** — project names cannot contain `--`. `myproject--frontend` is the labeled variant; `my-project` is a valid project name; `my--project` is rejected.
5. **`send --cc=X` vs `spawn --cc=N:X`** — same flag name, different parsers. `send --cc=opus` filters *existing* panes by variant; `spawn --cc=2:opus` creates 2 new panes of model `opus`.
6. **`--route=affinity` is a send flag, not an assign strategy** — `assign --strategy=` accepts `balanced|speed|quality|dependency|round-robin` only.
7. **`--robot-pipeline=<id>` is *status*, not run** — to run, use `--robot-pipeline-run=<file>`. Conflating these is common.
8. **Pipeline state files accumulate forever** — `.ntm/pipelines/<run-id>.json` is never auto-pruned. Run `ntm pipeline cleanup --older=7d` periodically.
9. **Safety wrappers need PATH precedence** — `ntm safety install` drops `git`/`rm` wrappers at `~/.ntm/bin/` but does NOT modify `$PATH`. Confirm `~/.ntm/bin` is earlier in `$PATH` than `/usr/bin`.
10. **`bead_orphaned` is *deliberately* unsupported** — ntm refuses to infer abandonment from silence; explicit `bead abandon` mail messages would be required and don't exist yet. Don't try to wait on it.
11. **Cursors are per-server monotonic** — they are NOT portable across machines. Cross-machine continuity is via `checkpoint export`/`import` or `handoff`, not cursor shipping.
12. **`ntm approve` takes a token, not a bead id** — tokens are issued by the approval engine and returned with each approval request; beads ids like `br-123` will be rejected.
13. **`ntm changes` and `ntm conflicts` are separate top-level commands** — there is no `ntm changes conflicts` (use one or the other).
14. **Attention flags are namespaced** — events use `--since-cursor`, `--events-limit`, `--events-category`, and `--events-actionability`; attention/digest waits use `--attention-cursor`, `--attention-timeout`, and `--attention-condition`.
15. **Agent Mail can be degraded without blocking work** — if the mail/reservation source in `sources` is stale/unavailable or reservations time out, stop retry loops and use bead assignee/status notes as the temporary soft lock.
16. **`locks check` is for wrappers and commit guards** — it returns `free|held|blocked` for one path and caller context; use it instead of inventing per-wrapper reservation ledgers.
17. **`--oc` is opencode** — if a prompt or profile says "opencode" but no agent appears, check `[agents] oc` config or that `opencode` is on PATH.
18. **`--cod` must be observed before use** — if a Codex pane is just a bare shell,
    stop sending prompts to it and run `codex exec -s danger-full-access --skip-git-repo-check -C <gitdir> "<contract>"` from an isolated repo/worktree instead.

## Reference Index

Keep depth out of this file. Load these on demand for the operator-handbook-level detail.

| Topic | Reference |
| --- | --- |
| **`ntm send` deep reference** — agent-type selectors with variants, pane selectors, input sources, file context ranges, templates & vars, smart/route, distribute, batch, CASS dedup, prefix/suffix, dry-run, error modes | [SEND.md](references/SEND.md) |
| **`ntm spawn` deep reference** — agent counts & model variants, labels, worktrees, personas/recipes/workflows, stagger modes, session profiles, CASS context, assign pipeline, privacy, interactive wizard | [SPAWN.md](references/SPAWN.md) |
| **Work intelligence & assignment** — `ntm work *`, `ntm assign`, strategies, bv integration, robot wrappers | [WORK-AND-ASSIGN.md](references/WORK-AND-ASSIGN.md) |
| **Ensemble mode** — reasoning modes, presets, multi-agent debate sessions, `--robot-ensemble-*` surfaces | [ENSEMBLE.md](references/ENSEMBLE.md) |
| **Pipelines** — YAML schema v2.0, steps / conditionals / loops / retries, run IDs, resume & cancel, robot pipeline flags, legacy `exec` | [PIPELINES.md](references/PIPELINES.md) |
| **Serve API** — auth modes (`local`/`api_key`/`oidc`/`mtls`), OIDC/mTLS flags, REST v1 route map, OpenAPI endpoint, SSE streams | [SERVE.md](references/SERVE.md) |
| **Safety, Policy, Approvals** — `policy.yaml` schema, precedence, automation flags, approval tokens & TTL, SLB two-person, what `safety install` actually drops on disk | [SAFETY.md](references/SAFETY.md) |
| **Durability stack** — checkpoint vs timeline vs handoff vs resume vs rollback; export/import archives; cross-machine continuity | [DURABILITY.md](references/DURABILITY.md) |
| **Integration surfaces** — DCG, SLB, CAAM, RCH, RANO, mail, cass-from-ntm, quota, ru, giil, context-inject | [INTEGRATIONS.md](references/INTEGRATIONS.md) |
| **Environment variables** — every `NTM_*` + `TOON_*` + inherited vars with source citations | [ENV-VARS.md](references/ENV-VARS.md) |
| **Troubleshooting** — failure symptoms / root cause / fix, including projects_base, stale `ntm view`, `--mail-project` scope, cursor expiry | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| **Self-test / trigger phrases** — canonical phrasings the skill should activate on, mapped to first action | [SELF-TEST.md](references/SELF-TEST.md) |
| High-leverage command patterns, output capture, monitoring, reusable assets | [COMMANDS.md](references/COMMANDS.md) |
| Attention feed, robot output formats, wait conditions, mail/cass/bead robot flows, full `--robot-*` index | [ROBOT-MODE.md](references/ROBOT-MODE.md) |
| Human dashboard, palette, keybindings, and TUI implementation notes | [DASHBOARD.md](references/DASHBOARD.md) |
| Project resolution, `projects_base`, config paths, and project-local assets | [CONFIG.md](references/CONFIG.md) |

### Quick Search (grep hints)

When scanning the skill without loading every file, these literal strings are indexed:

```bash
# From the ntm skill root:
rg 'robot-' references/ROBOT-MODE.md          # every --robot-* flag with root.go line
rg '^###'  references/SEND.md                 # every send flag family
rg '^###'  references/SPAWN.md                # every spawn knob
rg 'Symptom' references/TROUBLESHOOTING.md    # all failure-mode entries
rg '^-'    references/SELF-TEST.md            # trigger phrases agents should match
rg '^| `'  references/ENV-VARS.md             # every NTM_* env var (leading table cell)
grep -l 'policy.yaml'  references/           # finds SAFETY.md
grep -l 'schema_version' references/          # finds PIPELINES.md
```

### Assets

Drop-in examples live under `assets/`:

- [`pipeline-example.yaml`](assets/pipeline-example.yaml) — a review pipeline with parallel step + retry
- [`policy-example.yaml`](assets/policy-example.yaml) — opinionated `~/.ntm/policy.yaml` starter
- [`envrc.example`](assets/envrc.example) — recommended `direnv`/shell env vars

## Related Skills

- **`vibing-with-ntm`** — the companion **operator / orchestration** skill: tending loops, marching-orders prompts, autonomous unstick recipes, anti-patterns, steady-state cadence. Use it whenever the question is "how do I run the swarm well?" rather than "what does NTM do?"
- `agent-mail` for inboxes, contact handshakes, and file reservations
- `br` for bead state changes and syncing
- `bv` for graph-aware task prioritization
- `cass` for prior-session retrieval
- `caam` for account rotation across providers (paired with `--robot-switch-account`)
- `dcg`, `slb` for destructive-command and two-person approval policy
