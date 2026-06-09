---
name: cc-loop-driver
user-invocable: false
description: |-
  Use when running a Claude-native control-plane tick loop with worker and separate-validator subagents.
  Triggers:
practices:
- design-by-contract
- continuous-delivery
- agile-manifesto
hexagonal_role: driving-adapter
consumes:
- beads
- validate
produces:
- evidence/<id>.md
- git-commit
context_rel:
- kind: customer-of
  with: beads
- kind: customer-of
  with: validate
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: orchestration
  dependencies: [beads-br, beads, cc-hooks]
  stability: experimental
output_contract: "Per-bead evidence file at evidence/<id>.md + validator verdict(s); a conventional-commit git commit per closed bead; a published shared-state artifact (Agent Mail summary or committed .agents note). The loop returns NO_READY or CONVERGED when drained."
---

# cc-loop-driver

The control-plane assured tick loop, packaged as a skill that runs in **pure Claude tools** — the Task tool for worker/validator fan-out, Bash for ledger/git mechanics, no NTM and no `claude -p`. The main agent is the orchestrator; it is the **only writer** that closes a bead.

## Overview / When to Use

This is the shippable form of the all-Claude control plane proven in `~/dev/control-plane`. One Claude session acts as the **orchestrator**: it reads the next ready bead, claims it, spawns a fresh **worker** subagent to do the work and emit evidence, spawns an **independent validator** subagent (a different context, so author != judge) to verify the evidence against the bead's acceptance, and — only on a verified PASS — closes the bead, commits the result, and publishes to shared state. It loops until the queue is drained.

Use it when you want the loop's assurance (evidence-gated, single-writer, no self-grade) without standing up NTM tmux swarms or Agent Mail. It works in any repo with a `bd` (beads) or `br` (beads_rust) ledger.

## ⚠️ Critical Constraints

- **Single writer.** Only the orchestrator (main agent) runs `claim`, `close`, and `git commit`. Workers and validators NEVER close or update the bead's verdict. **Why:** this is the seam that makes the loop assured — a worker that grades its own work is the failure mode this skill exists to prevent.
- **Author != judge.** The worker and the validator MUST be separate Task subagent invocations (separate contexts). **Why:** in an all-Claude system, independent assurance comes from context separation, not a second vendor; the same context grading itself is self-grade.
- **No `claude -p` / `--print`, ever.** Workers and validators are in-harness Task subagents (they run on the Max subscription). `claude -p` bills the API per token. **Why:** an overnight loop on `claude -p` silently burns API spend that the Max sub already covers; it is banned for worker dispatch.
- **Evidence-gated close.** A bead closes ONLY on `VERDICT: PASS` from a validator whose verdict cites real `COMMANDS RUN`. A verdict with no cited commands is rejected as unverified and re-routed. **Why:** a verdict without a proof surface is a claim, not assurance; fail-closed on uncertainty.
- **The close cannot lie.** Before closing, confirm the evidence ref resolves to a real artifact, and after `bd close` confirm the ledger shows the bead closed AND the commit actually landed; otherwise roll the close back. **Why:** a closed-but-unpersisted bead is worse than an open one — it claims done work that isn't in git.
- **Stage only scoped paths.** Never `git add -A` or `git add -u` in the close step. Stage the ledger, the evidence file, and the bead's explicitly-named files only. **Why:** the loop may run while you edit; a blanket add sweeps unrelated work into the bead's commit.

## Workflow / Methodology

The orchestrator runs **one tick** per ready bead; the tick is idempotent. Wrap the ledger/git mechanics in a `tick.sh` helper (see references) so the agent's job is dispatch + judgement, not shell plumbing.

### Phase 0: Preflight
- Confirm the tracker binary: `bd` (beads) or `br` (beads_rust). This skill uses `bd` in examples; substitute `br` if the repo declares it in `AGENTS.md`.
- Confirm `git` is clean enough that a scoped commit won't sweep unrelated work.
- `mkdir -p evidence/` for per-bead evidence files.

**Checkpoint:** tracker resolves (`bd ready` runs) and `evidence/` exists before dispatching any worker.

### Phase 1: Pull + claim
```bash
id=$(bd ready --json | jq -r '.[0].id // empty')   # highest-priority ready bead
[ -z "$id" ] && echo "NO_READY" && exit 0           # nothing schedulable; stop the tick
bd update "$id" --claim                              # orchestrator claims it (single writer)
bd show "$id"                                        # capture acceptance verbatim for the worker
```
**Checkpoint:** confirm a non-empty `$id` and that you have the bead's acceptance text verbatim. If `NO_READY`, distinguish it from `CONVERGED` (no open or in-progress beads at all) and stop.

### Phase 2: Worker (Task subagent, fresh context)
Dispatch via the **Task tool** (NOT `claude -p`). The worker does the work and writes evidence; it never closes.
```
You are a WORKER. Do ONE bead's work, then stop.
BEAD: <id> — <title>
ACCEPTANCE: <acceptance verbatim>
DO: (1) do exactly what ACCEPTANCE requires, no scope creep;
    (2) stay within the bead's write-scope;
    (3) write evidence/<id>.md with WHAT changed (file:line), PROOF (commands + output),
        ACCEPTANCE MAP (one line per acceptance point -> how met);
    (4) return the evidence path + a 3-line summary.
DO NOT: close/update the bead, use claude -p, or self-grade ("looks good").
```
**Checkpoint:** `evidence/<id>.md` exists and maps every acceptance point to a proof surface. If missing, re-dispatch or fail the bead — do NOT proceed to validation without evidence.

### Phase 3: Validator (separate Task subagent — author != judge)
Dispatch a FRESH Task subagent — must not be the worker context.
```
You are an INDEPENDENT VALIDATOR. You did NOT author this. Author != judge.
BEAD: <id> — <title>
ACCEPTANCE: <acceptance verbatim>
Read evidence/<id>.md AND the real artifacts it cites; re-run the cited commands.
Do not trust the evidence — verify against reality. Judge strictly; fail-closed on uncertainty.
Return EXACTLY:
VERDICT: PASS or FAIL
COMMANDS RUN: actual commands you ran + a snippet of each output (mandatory; a verdict without this is rejected)
REASONS: 2-4 bullets, each pointing at one COMMANDS RUN line.
```
**Checkpoint:** the verdict includes a non-empty `COMMANDS RUN` section. A verdict with no cited commands is **unverified** — reject it and dispatch a fresh tie-break validator. (Optional hardening: two validators in parallel; require unanimous verified PASS; on mixed PASS/FAIL dispatch a third tie-break — majority of verified verdicts decides, fail-closed if none.)

### Phase 4: Close + commit + publish (orchestrator only, on verified PASS)
```bash
# tick.sh close: verifies evidence ref is real, runs bd close, confirms the ledger shows
# closed, commits ONLY scoped paths, then confirms HEAD advanced — else rolls the close back.
./tick.sh close "$id" "feat(scope): <subject> (closes $id)" "evidence/$id.md" <scoped files...>
```
On **verified FAIL**: reopen the bead with the validator's reasons injected (informed retry; budget 2, then escalate to a human). On **PASS**: after the commit lands, publish to shared state — an Agent Mail summary, a committed `.agents/` note, or a bead comment — so other agents can consume the compression.

**Checkpoint:** after close, `git rev-parse HEAD` advanced AND the ledger shows the bead closed. If not, the close was rolled back; treat as FAIL.

### Phase 5: Loop
Repeat Phase 1–4 until `bd ready` is empty. Emit `NO_READY` (work blocked/in-progress) or `CONVERGED` (no open or in-progress beads). To run unattended, schedule the orchestrator re-drive with **CronCreate** (an in-session scheduled tick) rather than a shell `&` background loop.

## Output Specification

**Format:** Markdown evidence + git commits + a shared-state publish.
**Filenames:**
- `evidence/<bead-id>.md` — worker evidence (WHAT / PROOF / ACCEPTANCE MAP).
- `evidence/<bead-id>.v1.md`, `.v2.md` — validator verdict file(s) when running a council.
**Structure per closed bead:**
- One conventional-commit git commit: `<type>(<scope>): <subject> (closes <id>)`, staging only the ledger + evidence + the bead's scoped files.
- The `bd close` reason carries the evidence ref.
- One published compression (Agent Mail summary OR committed `.agents/` artifact OR bead comment).
**Loop terminal output:** `NO_READY` or `CONVERGED`.

## Quality Rubric

- [ ] Every closed bead has an `evidence/<id>.md` that maps each acceptance point to a real proof surface.
- [ ] The validator was a SEPARATE Task context from the worker (author != judge), and its verdict cites `COMMANDS RUN`.
- [ ] No `claude -p` / `--print` was used for any worker or validator (Task subagents only).
- [ ] Only the orchestrator closed/committed; the commit staged ONLY scoped paths (no `git add -A`/`-u`).
- [ ] For every close, HEAD advanced AND the ledger shows the bead closed (close-cannot-lie verified).
- [ ] FAIL beads were reopened with reasons injected, not silently dropped; retry budget respected.
- [ ] A published compression exists per closed bead (other agents can consume it without reading this session).
- [ ] The loop emitted a precise terminal word (`NO_READY` vs `CONVERGED`), not a vague "done".

## Examples

**Drain a queue with assurance (one session):** invoke the `cc-loop-driver` skill, then the orchestrator runs:
```
# bd ready -> claim ag-123 -> Task(worker) writes evidence/ag-123.md
#   -> Task(validator) returns VERDICT: PASS + COMMANDS RUN -> close + commit + publish
#   -> next bead ... until NO_READY
```

**Tie-break on a contested FAIL:** validator A returns FAIL but cites no commands -> rejected as unverified -> dispatch fresh validator B -> B returns verified PASS -> orchestrator closes (the false-FAIL was caught by the council gate, not acted on).

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Worker closed the bead itself | Worker prompt didn't forbid it / used wrong tool | Re-state single-writer rule; only the orchestrator closes. Reopen + redo via the seam. |
| Validator returns PASS with no commands | Missing `COMMANDS RUN` enforcement | Reject as unverified; dispatch a fresh tie-break validator. Never act on it. |
| Closed-but-unpersisted bead | `bd close` ran but commit didn't land | The close step must confirm HEAD advanced + ledger closed, else roll back. Use `tick.sh close`. |
| Commit swept unrelated files | Used `git add -A`/`-u` | Stage only ledger + evidence + the bead's explicitly-named paths. |
| API spend during overnight run | A worker used `claude -p` | Banned. Workers/validators are Task subagents on the Max sub. Audit + purge. |
| Loop re-pulls a finished bead | Tick not idempotent | Always `bd ready` first each tick; closed beads are never schedulable. |
| `NO_READY` but work remains | Beads blocked or in-progress | Distinct from `CONVERGED`. Resolve blockers / dependencies, then re-tick. |

## See Also / References

- `references/tick-helper.md` — the `tick.sh` close-cannot-lie / scoped-stage mechanics and the council-gate logic.
- `references/dispatch-templates.md` — full worker + validator + tie-break Task prompts.
- `~/dev/control-plane/{ORCHESTRATOR,WORKER,VALIDATOR}.md` + `tick.sh` + `LEARNINGS.md` — the proven reference implementation this skill packages.
- `../shared/references/claude-code-latest-features.md` — Task subagents (`isolation: worktree`), hook events. (Scheduling unattended re-ticks uses the harness `CronCreate` tool, not this contract.)
- Related skills: `beads-br` / `beads` (the ledger), `cc-hooks` (enforce no-`claude -p` + scoped-commit at the harness), `operating-loop` (the multi-agent NTM form of the same seven-move loop).

## References
- [tick-helper](references/tick-helper.md)
- [dispatch-templates](references/dispatch-templates.md)
