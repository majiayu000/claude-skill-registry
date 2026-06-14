---
name: vibing-with-ntm
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when tending NTM agent swarms, unsticking panes, handling rate limits, or coordinating convergence."
practices:
- pragmatic-programmer
---
<!-- TOC: One Rule | Cold Start | Tick Loop | Intervention Score Matrix | Operator Proof Card | Swarm Pathology Triggers | Pattern Tiers | Metrics | Checklist | Decision Tree | Quick Start | Attention-Feed Loop | Marching Orders | Swarm Loop | Operator Loop | Autonomous Unstick | Observability | Steady-State Cadence | Quality Loops | Coordination | Anti-Patterns | Troubleshooting | References | Related Skills -->

> **If you are tending a swarm right now:** jump to the [Orchestrator Decision Tree](#orchestrator-decision-tree) below. Drop into [Autonomous Unstick](#autonomous-unstick--dont-wait-for-the-human) for recovery recipes. Everything else is context.

# Vibing With NTM

> **The One Rule:** Observe real state before every nudge. A swarm is not stuck, done, or blocked until pane truth, robot state, work graph, and artifact/git evidence agree.

## Outcome — When a Tending Session Has Delivered

An operator tending session is complete (for now) when **all** of the following hold:

- Every pane is in one of three explicit states: **making progress** (recent useful output / git activity / br/beads movement), **explicitly blocked** with a logged blocker and a handoff path, or **standing down** by policy (queue-dry, convergence, rate-limit cool-down). "Idle and you don't know why" is not a terminal state — it is unfinished tending work.
- Every intervention you applied during the tick was **observed to land** via tail/event/git/br/mail evidence within one observation window. Sends that produced no downstream signal are presumed lost, not silently successful.
- Any policy lever you adjusted (review-only, rate-limit posture, ensemble member set) has been **logged** so the next operator can see what the swarm's contract currently is. Undocumented policy changes are how swarms drift.
- For convergence: the **triple-check** has fired — ready queue empty AND no in-flight work AND no expected upstream signals — before you declare done. Two of three is not convergence; it is observation lag.
- For queue-dry / stand-down: you have **stopped manufacturing work** rather than papering over the dry queue with synthetic tasks. Tending discipline includes the discipline of doing nothing.

If you find yourself sending the same nudge twice without movement, the failure mode has escalated past nudging — drop into [Autonomous Unstick](#autonomous-unstick--dont-wait-for-the-human), don't keep nudging.

## Grounding — Where Operator Truth Lives

Operator decisions must be grounded in observable artifacts, never in agent self-report:

- **Pane truth:** `ntm --robot-tail=<session> --lines=N`. What the agent says it's doing is a hypothesis; what the pane shows is the data.
- **Work graph:** `br ready --json`, `br show <id> --json`. "Ready" status is canonical; if the agent thinks something is ready that br disagrees with, the agent is wrong.
- **Mail / coordination:** the Agent Mail inbox and threads — not Slack screenshots, not summary cards. The thread is the source.
- **Git state:** `git log --since=`, `git status` on the project worktrees. Commits and uncommitted changes are ground truth for "is real work being produced."
- **Snapshot deltas:** compare two `--robot-snapshot` outputs N seconds apart. The diff is what actually changed; everything else is narrative.

Never base an intervention on a swarm participant's self-report when one of these grounding sources can confirm or refute it. If they disagree, the artifact wins.

## Cold Start For Operators

When you open this skill cold, do not read every reference first. Run one bounded operator tick:

1. `ntm --robot-snapshot` and read `sources` / `degraded_sources`, pane states, and cursor.
2. If the state is unclear, use `ntm --robot-tail=<session> --lines=40` for the suspect panes.
3. Match exactly one card or branch in the [Orchestrator Decision Tree](#orchestrator-decision-tree).
4. Act on one pane or one policy lever, then verify tail/event/git/br/mail movement.
5. If no branch fires, wait on the attention feed instead of inventing work.

Use `/ntm` only when command syntax or schema details are unclear; return here for the intervention decision.

## The Tick Loop (Mandatory)

```
1. BASELINE    -> ntm --robot-snapshot; capture cursor + sources/degraded_sources
2. ATTEND      -> ntm --robot-attention / --robot-wait; read only actionable deltas
3. CLASSIFY    -> match one OC card or AP red flag; no card means observe more
4. SCORE       -> choose the smallest reversible intervention with highest action score
5. ACT         -> one targeted send/assign/lock/restart/review instruction; never blanket-nudge
6. VERIFY      -> tail/event/git/br/mail/pipeline state changed; otherwise escalate one rung
7. STOP CHECK  -> convergence triple-check or queue-dry; stop instead of manufacturing work
8. LOG         -> record blocker, degraded source, or handoff when the operator loop changes policy
```

This is the operator counterpart to `/ntm`. `/ntm` tells you what command exists; this skill tells you when to use it, how to avoid thrashing panes, and when to stop.

## Intervention Score Matrix

When several actions are possible, score them before acting:

```
Score = (Evidence x Impact x Reversibility) / BlastRadius

Evidence       1-5: independent sources agree this state is real
Impact         1-5: likely to move code/beads/artifacts, not just produce prose
Reversibility  1-5: can undo/stop/retry without losing work
BlastRadius    1-5: one pane/message is low; all panes/session kill is high
```

Only take Score >= 2.0. If every action scores below 2.0, wait on the attention feed or gather better evidence.

| Candidate action | Evidence | Impact | Reversible | Blast | Decision |
|---|---:|---:|---:|---:|---|
| Terse prompt to one idle pane with no output and no commits | 4 | 3 | 5 | 1 | yes |
| Smart-restart one pane with identical tail across 3 ticks | 5 | 4 | 4 | 2 | yes |
| Broadcast "status?" to all panes | 1 | 1 | 3 | 4 | no |
| Kill a pane because it says "Cogitated 35m" | 1 | 3 | 1 | 4 | no |
| Stop swarm after convergence triple-check + queue-dry | 5 | 5 | 4 | 1 | yes |

## Operator Proof Card

Before any intervention stronger than a read-only check, fill this mentally or in the session log:

```markdown
## Intervention: <one-line action>
- Evidence: <robot attention/events>; <pane tail>; <git/br/mail/pipeline fact>
- Card matched: OC-___ / AP-___ / queue-dry / convergence / other
- Target: <session>; panes=<N or type>; user pane included? <yes/no>
- Expected state change: <commit/bead/artifact/tail/status>
- Reversibility: <wait/interrupt/smart-restart/checkpoint/restore/cancel>
- Verification command: <exact command>
- Escalation if unchanged: <next rung, not a jump to nuclear>
```

No proof card -> no nudge, restart, force-release, or shutdown.

## Swarm Pathology Triggers

| Pathology | Smell | First detector | First move |
|---|---|---|---|
| Prose treadmill | many "I'll investigate" lines, no commits/beads | `git log --since=1h`, `br list` | ship-or-surface prompt to that pane |
| False convergence | "LGTM"/"ready" everywhere, open work unchanged | convergence triple-check | stop if true, targeted artifact demand if false |
| Stale robot state | activity says old/stale but tail/git moving | attention + tmux capture | trust newer/direct source, resync cursor |
| Rate-limit mirage | pane text mentions old reset time | `--robot-health-oauth`, quota status | ping-probe before rotation |
| Coordination drag | mail/register retries consume ticks | stale/unavailable mail or reservation source | degraded fallback, record it, continue |
| Reservation deadlock | broad lock blocks ready work | `ntm locks list`, coordinator conflicts | narrow/renew/release with evidence |
| Review bead flood | agents file issues but close none | `br` plus BV status mix | switch to close-the-backlog mode |
| Context cliff | context >85%, repeated summaries | snapshot/context | handoff-then-restart |
| Queue-dry ambiguity | `br ready` empty but stale in-progress exists | `ntm work queue-dry` | decide stand-down vs ideate, do not invent silently |
| Operator overreach | repeated global broadcasts/restarts | tick log | pause, classify one pane at a time |

## Pattern Tiers

### Tier 1: Low-Risk Tending

| Pattern | Use when | Proof |
|---|---|---|
| Attention-feed wait | no urgent issue | cursor/event advances |
| Terse single-pane nudge | one pane genuinely idle | tail changes or blocker appears |
| Work graph refresh | ready/in-progress unclear | `br`/`bv`/queue-dry agree |
| Mail/lock digest | coordination seems stale | inbox/conflict list read |

### Tier 2: Directed Recovery

| Pattern | Use when | Guard |
|---|---|---|
| Account rotation | confirmed rate limit | provider/quota state, not pane text alone |
| Smart restart | pane not productively working | refuses active work |
| Interrupt + replace task | pane on wrong task | tail proves wrong task |
| Context handoff | context hot | handoff prompt and resume target ready |
| Reservation mediation | conflict blocks ready work | holder inactive or pattern too broad |

### Tier 3: Session Policy Changes

| Pattern | Use when | Guard |
|---|---|---|
| Review-only mode | code churn risky or user asked for audit | no implementer claims |
| Close-the-backlog mode | review beads exceed shipped fixes | one bead per pane, no new findings unless critical |
| Queue-dry stand-down | no ready/claimable work | `ntm work queue-dry` confirms |
| Pipeline handoff | repeated phase work | dry-run/status/cancel path known |
| Shutdown/convergence | triple-check passes | record final state; stop nudging |

## Metrics You Report

At closeout, summarize the swarm in concrete deltas:

| Metric | Meaning |
|---|---|
| Commits landed | real work, not pane chatter |
| Beads closed / opened | backlog burn vs review inflation |
| In-flight unchanged ticks | convergence/stall signal |
| Pane interventions | nudges, restarts, rotations, force-releases |
| Degraded sources | mail/CASS/beads/RCH/tool health that shaped decisions |
| Queue state | ready, blocked-only, queue-dry, or active |
| Residual risk | unverified tests, stale locks, partial runs, open blockers |

## Checklist Before Ending A Tending Turn

- [ ] No command sessions needed for the user's request are still running.
- [ ] Active panes are either working, blocked with a named blocker, or intentionally stopped.
- [ ] `br ready` / `ntm work queue-dry` state is known.
- [ ] Reservations and Agent Mail state are not silently stale.
- [ ] Any restart/force-release/shutdown has evidence and a verification result.
- [ ] User-facing closeout names commits/beads/tests/blockers, not "the swarm seems fine."

## When To Use This Skill / When To Skip

**Use this skill when:**

- You are acting as the orchestrator / babysitter of an NTM session with ≥2 panes.
- A pane looks stuck, wedged, rate-limited, context-saturated, or silently dead.
- You need to dispatch marching orders, rotate accounts, or restart a pane.
- The swarm is filing many review beads but closing few ("close-the-backlog" trigger).
- You're switching the swarm between implementer and review-only mode.
- You need to know whether the swarm has actually converged (and can be shut down).
- You're diagnosing cross-session contention (bead DB locks, cargo registry locks, zombie processes) that affects a running swarm.

**Skip this skill when:**

- You just need the `ntm` command catalog itself — use `/ntm`.
- You're doing single-agent work in one pane — no orchestration layer is needed.
- You're configuring a brand-new NTM install or provisioning a machine — use `provision-new-machine`.
- You're fixing Beads DB corruption or JSONL drift — use `fixing-beads-problems`.
- You want Gemini-specific review-swarm tuning (Flash fallback, model lock) — use `code-review-gemini-swarm-with-ntm`.
- You want to spawn a weighted swarm from bead backlog size — use `open-beads-weighted-tmux-agent-sessions`.

**This skill deliberately does NOT cover:** the full `ntm` command surface (see `/ntm`), MCP Agent Mail primitives (see `/agent-mail`), Beads mechanics (see `/beads-br`), BV triage internals (see `/beads-bv`), or CAAM account management (see `/caam`). It focuses on the **operator layer that sits above those tools** — the decisions, ticks, nudges, and recoveries an orchestrator performs.

**Degrees of freedom.** This is a **medium-freedom methodology skill**: the recipes and cards codify a defensible default, but every tick requires judgment about which card applies. Prefer the specific OC/AP/recipe when evidence fires its trigger; fall back to the decision tree otherwise. It is not a turn-by-turn playbook, and blindly following steps without the evidence that their triggers fired produces worse outcomes than skipping the card.

## Orchestrator Decision Tree

Run one tick. Pick the FIRST branch whose condition fires.

```
Is CURSOR expired (or missing)?
  → ntm --robot-snapshot  (resync, get new cursor); continue next tick.

Is ANY pane rate_limited?  (check via --robot-health-oauth, NOT pane buffer text)
  → See OC-001 & OC-002 in [OPERATOR-CARDS.md](references/OPERATOR-CARDS.md).
    Probe: tmux send-keys "ping" Enter; sleep 5; --robot-tail.
    Rotate: ntm rotate <session> --all-limited.
    Or switch: ntm --robot-switch-account=<provider>:<account>.

Is ANY pane stuck (identical tail ≥3 ticks, zero output growth)?
  → Climb the stuck-pane ladder (see OC-003 in [OPERATOR-CARDS.md](references/OPERATOR-CARDS.md)):
    wake-ping → C-u + send → smart-restart → hard-kill → restart-pane → add+kill.

Is there prose-without-commits? (pane is_working=true but git log 1h=0)
  → Dispatch OC-004 Ship-or-Surface prompt (see PROMPTS.md).

Is context >85% on any pane?
  → Dispatch handoff-then-restart (OC-009).

Is there a file-reservation conflict or coordinator-reported collision?
  → Force-release too-broad patterns (OC-008); mediate via bead status-flip (OC-015).

Does convergence triple-check hold?
  ( git log 1h=0 AND br ready=0 AND in-flight unchanged ≥2 ticks AND convergence language in every pane )
  → STOP. Do not nudge. Exit the loop; report final state.

Otherwise — one specific-terse nudge per genuinely-idle pane (OC-010). Then wait.
```

Every card (OC-###) and anti-pattern (AP-###) is documented with recipe, prompt module, and validator. See [OPERATOR-CARDS.md](references/OPERATOR-CARDS.md) and [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md).

### Operator Kernel: OIAVS

Use this loop for every tick:

| Phase | Question | Preferred evidence |
| --- | --- | --- |
| Observe | What changed since the last tick? | `--robot-attention`, `--robot-events`, `git log`, pane truth stack |
| Interpret | Which failure or workflow pattern fired? | OC/AP card trigger, `sources`, quota/pressure state |
| Act | What is the smallest reversible intervention? | Targeted `--robot-send`, assignment, reservation fix, restart ladder |
| Verify | Did the action change reality? | New commit, bead status, tail movement, health/retry count |
| Stop | Is the swarm converged or queue-dry? | convergence triple-check, `ntm work queue-dry`, unchanged in-flight set |

If you cannot name the phase and the evidence, do not nudge. Re-observe.

### Red-Flag Phrases In Pane Tail (Scan → Match → Apply)

During a tick, skim each pane's last ~20 lines for these exact-or-near substrings. Match → apply the card. This is the fastest classifier when you don't have time to read every pane.

| If tail contains this phrase | State | Card to apply |
| --- | --- | --- |
| "resets 3pm", "You've hit your limit", "Upgrade to Max" | (maybe-stale) rate-limit | OC-001 Ping-Probe; then OC-002 Rotate if confirmed |
| "Stop and wait / Switch to extra usage" | `rate-limit-options` dialog | Autonomous Unstick → send `2` Enter |
| "[Pasted text]" alone | codex paste buffer | Autonomous Unstick → flush Enter |
| "Ready for validation", "MISSION ACCOMPLISHED", "Awaiting review", "Successfully identified and optimized" | **Handoff failure** (not success!) | OC-036 + Ship-Don't-Hand-Off prompt |
| "exemplary", "already complete", "no fixes needed", "ready to ship", "LGTM", "tests are passing" | Convergence language | OC-016 three-condition check; if all hold, STOP |
| "compile error", "build failed", "blocked by unrelated" | Build drift | PROMPTS.md → Build-Drift Repair |
| "bead DB was locked", "database is locked" | Bead DB contention | RECOVERY.md → `--no-db` bypass + OC-031 |
| "server unavailable" / "register_agent timed out" / "Resource temporarily unavailable" | Mail down/degraded | OC-007 fallback to bead-assignee lock |
| "FILE_RESERVATION_CONFLICT" | Over-broad reservation | OC-008 force-release |
| "Already covered, no bead filed" | Skill rotation dup | OC-041 session-scoped skill de-dup |
| "zsh: command not found" / "zsh: no matches found" | Prompt landed at bare zsh | OC-026 pid audit → OC-027 two-step relaunch |
| "Summarize recent commits", "Explain this codebase" (alone, no `• Working`) | Codex idle placeholder (NOT stuck) | Do not nudge; check dispatch history first |
| "waiting for file lock on registry" | Cargo registry contention | OC-031 cross-session zombie sweep |
| "Remove lock file?", "Force-push?", "Delete …?" (dialog) | Destructive-action dialog | OC-040 auto-decline (send "No") |
| `⏵⏵ bypass` bar at bottom of cc pane + long "Cogitated" | Actually executing | Do NOT nudge; cross-check with git log |

When in doubt, apply the **Liveness Truth Stack** above before any state-changing action.

### Liveness Truth Stack (what to believe, in order)

Before acting on any "pane is stuck / rate-limited / done / idle" judgment, verify in this order — each layer catches lies from the one above:

1. **`tmux list-panes … -F '#{pane_current_command} #{pane_pid}'`** — is the agent CLI even running? Silent exits back to zsh are common and invisible to `--robot-tail`. (OC-026)
2. **`tmux capture-pane -p -S -20`** — ground truth for transient state (post-keypress, dialog transitions). `--robot-tail` can sample stale buffer content for several ticks in a row. (AP-41)
3. **`git log --since='15 minutes ago'` + `pgrep -af cargo|rustc|go|bun`** — are commits landing? Are build processes running? Timer labels like "Cogitated for 35m" are display artifacts, not activity. (AP-42)
4. **`ntm --robot-is-working` / `--robot-health-oauth`** — provider-side state (rate-limit, context, quota).
5. **`ntm --robot-snapshot | jq '{sources, degraded_sources}'`** — data-source freshness before acting on any derived state.

If any two layers disagree, resync before acting. See OBSERVABILITY.md → "Liveness Signals That Can Lie" for the full catalog (timer labels, `⏵⏵ bypass` authoritativeness, codex placeholder suggestions, tmux window-index discovery, disk trajectory, "degraded ≠ broken").

> **Core flow:** understand the repo -> pick work intelligently -> coordinate explicitly -> keep agents moving -> review relentlessly.

> **Core insight:** every agent is fungible, but the swarm only works when work selection, reservations, mail, and operator tending all stay aligned.

> **Human vs agent surfaces:**
> - Humans can use `ntm dashboard`, `ntm palette`, `ntm view`, and other interactive surfaces.
> - Agents should avoid interactive TUIs and prefer `--robot-*` for structured state.
> - Non-interactive commands such as `ntm send`, `ntm work triage`, `ntm mail inbox`, `ntm locks list`, and `ntm assign` are still valid operator tools.

> **Isolation model:**
> - Default: Agent Mail file reservations plus clear bead ownership.
> - Optional: `--worktrees` when the repo policy allows it and branch/worktree isolation is useful.
> - Repo-local `AGENTS.md` always wins if it prefers or forbids a specific coordination model.

## Quick Start

```bash
# 1. Prerequisites
ntm deps -v
br ready
bv --robot-triage

# 2. Start a manageable swarm
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# 3. Send marching orders
ntm send myproject --all "$(cat marching_orders.txt)"

# 4. Watch the swarm
ntm dashboard myproject
ntm --robot-snapshot
```

Scale up only when the operator loop is under control.

## Marching Orders

Use [PROMPTS.md](references/PROMPTS.md) for copy-paste marching orders. Keep the operating constraints here in the live context:

- First dispatch: read repo instructions, register or coordinate if required, claim one scoped work item, reserve files or worktree scope, and start work.
- Steady-state dispatch: do not re-read onboarding docs every tick; ask for one commit or one explicit blocker within the timebox.
- Wide swarm dispatch: assign each pane a domain before work starts, then enforce file reservations or worktrees.
- Review dispatch: switch panes into review-only mode explicitly and block implementer-style bead claims.

## Operator Commands

Prefer robot surfaces and one-pane actions:

```bash
ntm --robot-snapshot
ntm --robot-attention --attention-cursor=<cursor>
ntm --robot-is-working=<session>
ntm --robot-health-oauth=<session>
ntm --robot-health-restart-stuck=<session> --stuck-threshold=10m --dry-run
ntm --robot-send=<session> --panes=<pane> --msg="<specific instruction>"
ntm --robot-smart-restart=<session> --panes=<pane> --prompt="<restart prompt>"
ntm --robot-restart-pane=<session> --panes=<pane> --restart-prompt="<fresh prompt>"
```

Use interactive dashboards for humans only. Agents should use `--robot-*`, `br`, `bv`, git, and Agent Mail evidence.

### Pending-input etiquette (meta-orchestrator rule)

A pane's input box may hold staged-but-unsent text. Submit it ONLY if it is clearly an
agent/orchestrator-staged directive awaiting send (a complete marching order, a queued
prompt from a prior dispatch). NEVER submit text that reads as the human operator's live
composition — a question addressed to that pane, a partial sentence, anything mid-thought.
When in doubt, leave it untouched and log the observation in the tick log.

## Recovery Shortcuts

| State | First move | Escalation |
| --- | --- | --- |
| stale cursor | `ntm --robot-snapshot` | resume from new cursor |
| stale rate-limit text | ping probe + `--robot-health-oauth` | rotate account if confirmed |
| identical tail >=3 ticks | smart-restart dry run | hard-kill or respawn pane |
| paste buffer / dialog | `Escape Escape Escape C-u`, then targeted send | respawn if submit does not land |
| mail or reservation down | mark bead owner/blocker directly | backfill Agent Mail when fresh |
| prose without commits | ship-or-surface prompt | close-the-backlog or stand down |
| destructive dialog | decline by default | require explicit justification |

Full recipes live in [RECOVERY.md](references/RECOVERY.md), [OPERATOR-CARDS.md](references/OPERATOR-CARDS.md), and [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md).

## Cadence And Stop Conditions

Tick every 4 minutes during nucleation, 10-17 minutes in steady state, and 30 minutes when panes are deep in real work. Stop tending when the convergence triple-check holds: no new commits, no ready work, and in-flight panes unchanged or explicitly standing down across repeated observations.

If the queue is dry, do not manufacture tasks. Report the state, blockers, degraded sources, and residual risk.

## Quality And Coordination Loops

- Use [PROMPTS.md](references/PROMPTS.md) for self-review, cross-review, exploration, close-backlog, and mode-switch prompts.
- Use Beads for work selection, Agent Mail for coordination, reservations or worktrees for write isolation, and NTM for shared state.
- If coordination surfaces degrade, continue with explicit bead ownership and backfill mail later.
- Track productivity with commits, closed beads, changed artifacts, pane interventions, degraded sources, and queue state.

## Anti-Patterns

The common failure modes are communication purgatory, stale bead state, review-bead inflation, false rate-limit assumptions, duplicate-work collisions, stale activity signals, context drift, and over-broad broadcasts. Match symptoms to [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) before escalating.

## Review-Only Mode

When the swarm is auditing rather than implementing, dispatch review-only instructions from [REVIEW-MODE.md](references/REVIEW-MODE.md): no Agent Mail registration, no bead claims, read recent diffs, tag findings by severity, and rotate reviewers between study, fresh-eyes, cross-review, and continuation passes.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `spawn` cannot resolve the project | Use `ntm quick`, check `ntm config get projects_base`, or make the repo discoverable from that base |
| No clear next work item | Run `bv --robot-triage`, `bv --robot-next`, or `ntm work triage` |
| Coordination feels chaotic | Check Agent Mail inboxes, lock state, and `ntm coordinator digest/conflicts` |
| Agents appear idle | Use `ntm --robot-is-working=myproject` and `ntm --robot-agent-health=myproject` — they are the authoritative live signals |
| Pane stuck identical ≥3 ticks | `ntm --robot-health-restart-stuck` → `ntm --robot-smart-restart --hard-kill` → `ntm --robot-restart-pane` |
| Pane showing "resets Xpm" rate-limit | Probe with `tmux send-keys ping Enter` + `ntm --robot-tail`. If still limited: `ntm rotate myproject --all-limited` or `ntm --robot-switch-account=claude:<account>` |
| cc pane on `rate-limit-options` dialog | `tmux send-keys -t session:0.N "2" Enter` to pick "Switch to extra usage"; or rotate the account |
| codex pane on `[Pasted text]` limbo | `tmux send-keys -t session:0.N "" Enter` to flush the paste buffer |
| `ntm send` aborts with `Continue anyway?` | Pass `--no-cass-check`, or use `ntm --robot-send` (non-interactive) |
| Agent Mail server down/degraded/DB-busy | Proceed without it (see repo AGENTS.md); use `br update --assignee=...` as a soft coordination lock |
| `ntm activity` / `ntm health` show epoch / "56 years stale" | Use `--robot-is-working` / `--robot-agent-health` / `--robot-diagnose` instead |
| Cursor expired | Re-run `ntm --robot-snapshot` |
| Saturated-context cc (4+ days old, circular planning) | `ntm --robot-restart-pane --panes=N --restart-bead=br-xxx` on a fresh account |
| Beads look inconsistent | Use normal `br`/`bv` recovery commands for the repo; do not mutate `.beads` internals from habit |
| Duplicate-work collisions | Enable coordinator auto-assign; compute avoid-list from `br list --status=in_progress,claimed` at each dispatch |
| Swarm converges ("no fixes needed" × 2 rounds, zero new commits) | Stop. The backlog is exhausted; don't nudge further. |

## Review-Only Mode

When the swarm's job is audit rather than implement (post-refactor hardening, pre-release bug hunt, mixed-swarm quality layer), flip agents into **Review-Only Mode**. Same operator loop, different prompt sequence and coordination rules.

**Core cycle:** per round, per pane: `P1 (study) → P2 (explore+fresh-eyes) → P3 (cross-review) → P4 (continuation) → repeat P2-P4 ×2 more times`. End of round: kill + relaunch all reviewer panes. Exploits prompt caching within a round; resets context between rounds.

**Reviewer coordination rules** (enforce in marching orders):
- Do NOT register with MCP Agent Mail (avoids communication purgatory)
- Do NOT claim beads from bv / br (not implementers)
- DO read `git log` / `git diff` to find recent implementer activity
- DO run repo's tests/linters after every fix
- DO tag findings by severity: `[CRITICAL] / [HIGH] / [MEDIUM] / [LOW]`

**Mixed-swarm ratios** (implementer : reviewer):

| Swarm size | Implementer | Reviewer |
| --- | --- | --- |
| Small (6) | 5 | 1 |
| Medium (14) | 10 | 4 |
| Large (24) | 20 | 4 |

Reviewers scale sub-linearly — 4 covers most codebases; more produces redundant findings.

**Hot mode-switch:** flip a pane between implementer and reviewer mid-session via the MODE-SWITCH prompts in [PROMPTS.md](references/PROMPTS.md).

Full spec — spawn, dispatch cadence, quality rubric, kill-relaunch timing, anti-patterns, real-bug examples — lives in [REVIEW-MODE.md](references/REVIEW-MODE.md). For **Gemini-specific** tuning (Flash-fallback detection, `gemini-3.1-pro-preview` model lock, `~/.gemini/settings.json` config), use `code-review-gemini-swarm-with-ntm` directly.

## Reference Index

| Topic | Reference |
| --- | --- |
| **137 robot-mode surfaces in the current mainline snapshot; always re-query** for commands, lanes, categories, transport availability, deprecated flags | [ROBOT-MODE.md](references/ROBOT-MODE.md) |
| **Error taxonomy + autonomous recovery decision tree** (cursor, quota, entity, source, request) | [RECOVERY.md](references/RECOVERY.md) |
| **Freshness, source health, attention state machine, three-observation rule** | [OBSERVABILITY.md](references/OBSERVABILITY.md) |
| **46 operationalized field-expertise cards** (trigger + recipe + prompt + validator) | [OPERATOR-CARDS.md](references/OPERATOR-CARDS.md) |
| **61 named anti-patterns** from real swarm sessions, each with a fix | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| **/loop, CronCreate, shell cron, schedule** — when to use each; convergence-gated tick scripts | [CRON-AND-AUTOMATION.md](references/CRON-AND-AUTOMATION.md) |
| **Review-Only Mode** — phase cycle, mixed-swarm ratios, kill-relaunch rhythm, quality rubric, mode-switch prompts | [REVIEW-MODE.md](references/REVIEW-MODE.md) |
| Marching orders, review prompts, ship-or-surface, close-backlog, orchestrator diagnosis, autonomous unstick playbook | [PROMPTS.md](references/PROMPTS.md) |
| Spawn mixes, cadence, close/review ratio, convergence termination, domain assignment, agent-pool awareness, scope discipline | [PLAYBOOK.md](references/PLAYBOOK.md) |
| **Operator helper scripts** (tick snapshot, convergence check, pane liveness, contention sweep, disk trajectory, depth-gate evidence, stale-bead audit) — zero context cost | [scripts/](scripts/) and [scripts/README.md](scripts/README.md) |
| **Marching-orders template** (placeholders for session/repo/scope/domains/peers) | [assets/marching-orders-template.md](assets/marching-orders-template.md) |
| **Trigger-phrase self-test** — confirms this skill activates on operator language and defers to siblings on adjacent language | [SELF-TEST.md](SELF-TEST.md) |

### Lookup By Symptom

| What you see | Start here |
| --- | --- |
| stale activity, epoch timestamps, unclear liveness | `--robot-is-working`, OBSERVABILITY.md, OC-026/027 |
| possible rate limit | RECOVERY.md `QUOTA_*`, OC-001/002 |
| pane stuck, prompt in wrong pane, send no-op | OC-003, OC-026-029, AP-39-44 |
| prose without commits or handoff failure | OC-004, OC-036, PROMPTS.md |
| Agent Mail, reservation, or coordinator drift | OC-007/008/019, AP-19/20/23 |
| queue dry or convergence | OC-016/043, OBSERVABILITY.md, PROMPTS.md |
| review-only swarm | REVIEW-MODE.md or Gemini-specific review skill |

## Related Skills

| Concern | Skill |
| --- | --- |
| NTM command catalog and work intelligence | `ntm` |
| Agent Mail primitives | `agent-mail` |
| Bead state and dependencies | `br`, `bv` |
| Account rotation and quota | `caam` |
| Multi-model or review swarms | `multi-model-triangulation`, `code-review-gemini-swarm-with-ntm` |
| Remote build offload | `rch` |
| Past-session mining | `cass` |

This skill stays focused on swarm tending decisions: observe, classify, act once, verify, and stop when the evidence says stop.
