---
name: agy-sidecar-scheduled-tick
description: |-
  Run a recurring AGY sidecar loop tick and capture agentapi evidence.
  Triggers: agy, sidecar, schedule, agentapi.
practices:
- design-by-contract
- evidence-over-assertion
hexagonal_role: supporting
consumes:
- agy-native
- agy-headless-evidence
produces:
- agy-sidecar-tick-evidence
context_rel:
- kind: customer-of
  with: agy-native
- kind: supplier-to
  with: validate
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: execution
  dependencies: [agy-native, agy-headless-evidence, dcg, beads-br]
  stability: experimental
output_contract: A registered AGY sidecar (sidecar.json with the `schedule` builtin) plus a per-fire timestamped evidence directory holding events.jsonl (the agentapi event stream), agentapi-health.json (the runtime liveness probe), schedule.txt (cron/interval + builtin), exit-code (captured $?), and command.txt (argv/cwd/scopes) — the proof surface a distinct-context validator reads to confirm the recurring tick actually fired and did work, never trusting worker prose.
---

# agy-sidecar-scheduled-tick

Drive a **recurring** AgentOps loop tick on the **Antigravity image** (AGY) using a **sidecar** — AGY's
long-lived headless server — with the **`schedule` builtin** for the cadence and **`agentapi`** as the
runtime the tick talks to. Each fire leaves a durable, inspectable **agentapi evidence** surface so a
separate-context validator can confirm the tick ran and did real work after the fact. This closes the
AGY proof child that requires *sidecar scheduling* plus *agentapi runtime evidence* (`cp-c6k.3.2`):
a one-shot `agy -p` (see `agy-headless-evidence`) proves a single headless run; this skill proves the
**daemon-style recurring** path. **Configure the sidecar; never cold-start `agy` on a timer by hand.**

## Overview / When to Use

`agy -p` cold-starts the harness on every call. For a loop that ticks on a cadence (claim a ready bead,
do one scoped unit, persist, repeat) you want a **persistent brain and warm conversation state** instead
of a cold start per fire. AGY provides this through a **sidecar**: a long-lived process described by a
`sidecar.json`, driven by the **`schedule` builtin** (the AGY-native cron/interval cadence) and reachable
over the **agentapi** runtime (AGY's headless server API). Per `IMAGE-AGY.md`, the control-plane
"scheduled tick" role maps to *"Antigravity sidecars with the `schedule` builtin plus `agentapi` for
daemon-style recurring ticks."*

Use this skill when:

- a loop must fire **repeatedly without a human re-invoking it** (overnight burndown, periodic validate
  sweeps, a warm worker that picks up newly-ready beads);
- you need the cadence to be **AGY-native** (the `schedule` builtin) rather than an external `cron`/launchd
  wrapper around `agy -p`;
- a downstream validator must **trust the recurring tick** — so every fire must drop agentapi runtime
  evidence, not just print to a log nobody reads back.

Do **not** use this for a single headless run — that is `agy-headless-evidence` (`agy -p`, one shot). Use
the sidecar only when the *recurrence* is the point.

### AGY surfaces this skill uses

- **Sidecar** — a long-lived AGY process declared by `sidecar.json` (under the workspace or plugin), the
  daemon that hosts the recurring tick. Validate/list with `agy --help` surface checks (Door-9: discovery
  commands only).
- **`schedule` builtin** — the AGY-native cadence inside the sidecar (cron expression or interval). This
  is the scheduling source of truth, not an external timer.
- **agentapi** — AGY's headless server runtime the sidecar drives each fire; its **event stream** and a
  **health probe** are the runtime evidence.
- **Brain / knowledge** — durable memory + userFacing artifacts under `~/.gemini/antigravity-cli/{brain,knowledge}/`;
  mirror each fire's verdict here so a *different* context can consume it (author != judge).

## ⚠️ Critical Constraints

- **Rule 1 — The cadence lives in the sidecar's `schedule` builtin, not an external timer.** Encode the
  cron/interval in `sidecar.json`'s `schedule` builtin and record it in `schedule.txt`. **Why:** the
  whole point of this proof child is *AGY-native sidecar scheduling*; wrapping `agy -p` in host `cron`
  is the thing this skill exists to replace, and it leaves no AGY-side schedule to inspect.
- **Rule 2 — Every fire must produce agentapi runtime evidence.** Capture the agentapi **event stream**
  (`events.jsonl`) and a **health probe** (`agentapi-health.json`) per fire. **Why:** a sidecar that
  "is scheduled" but leaves no per-fire runtime trace cannot be distinguished from one that silently
  stopped firing — evidence over comfort.
- **Rule 3 — One fire, one timestamped directory.** Never append unrelated fires into the same evidence
  files. **Why:** a verdict must bind to exactly one event stream, one exit code, one command; fires
  otherwise clobber each other and the proof surface lies.
- **Rule 4 — Capture the exit code immediately.** `echo "$?" > exit-code` on the line right after the
  fire returns. **Why:** a plausible message with a non-zero exit is still a failed tick; the validator
  keys off process reality, not self-report.
- **Rule 5 — The sidecar tick does not close its own beads.** A scheduled author tick claims and works;
  an **independent context** judges and only the orchestrator closes. **Why:** author != judge holds on
  AGY exactly as on the Claude/Codex images (`IMAGE-AGY.md`, single-writer seam).
- **Rule 6 — Scope the sidecar; sandbox by default.** Bound the tick with `--add-dir` to one
  worktree/repo and keep project/worktree-scoped, sandboxed execution. **Why:** a long-lived recurring
  process with broad write scope is a standing hazard; the image path has no break-glass permission
  bypass.
- **Rule 7 — `dcg` BeforeTool guard stays on.** Keep the `dcg` `BeforeTool` hook on `run_shell_command`
  in `~/.gemini/settings.json` even for the sidecar. **Why:** a recurring auto-driven process is exactly
  where a destructive command would slip through unattended — `dcg` is the floor.
- **Rule 8 — This is the AGY lane only (LAW 0).** Never reach for `claude -p` / `claude --print` to make
  a "Claude sidecar." **Why:** `claude -p` bills the API per-token and is banned for worker dispatch;
  AGY runtime is `agy` + the agentapi sidecar. Door-9: do not use `agy --print` as the scheduled executor
  until it is proven subscription-safe; `agy --help`/`--version`/`models` are allowed surface checks.

## Distribution — where the sidecar lives

A sidecar is declared by a `sidecar.json` carried in the **workspace** (`.agents/` / Antigravity config)
or bundled in an **AGY plugin** alongside `plugin.json`, `skills/`, `hooks.json`, and `mcp_config.json`
(per `IMAGE-AGY.md` N=1 step 1). Prefer the plugin bundle so the recurring tick ships and validates with
the rest of the AgentOps laws (`agy plugin validate` / `agy plugin list`).

## Workflow / Methodology

### Phase 1: Declare the sidecar + cadence
Author a `sidecar.json` with the `schedule` builtin (cron or interval) and the scoped command the fire
runs. Record the cadence so it is inspectable.
```bash
RUN_ROOT="$(pwd)/.agy-evidence/sidecar"
mkdir -p "$RUN_ROOT"
{
  printf 'sidecar=%s\n' "agentops-tick"
  printf 'builtin=schedule\n'
  printf 'cadence=%s\n' "${AGY_SCHEDULE:-*/30 * * * *}"   # cron or interval
  printf 'runtime=agentapi\n'
  printf 'scopes=%s\n' "${REPO:-$PWD}"
} > "$RUN_ROOT/schedule.txt"
```
**Checkpoint:** `schedule.txt` records the sidecar name, the `schedule` builtin, the cadence, and that
the runtime is agentapi — and the cadence is in `sidecar.json`, not host `cron`.

### Phase 2: Bring the sidecar up on agentapi
Register/start the sidecar so agentapi hosts it; probe liveness before trusting any fire.
```bash
# agy surface checks only (Door-9: discovery, not the print executor)
agy --version > "$RUN_ROOT/agy-version.txt" 2>&1 || true
# Probe the agentapi runtime the sidecar drives; persist the liveness proof.
curl -fsS "${AGENTAPI_URL:-http://127.0.0.1:3284}/status" \
  > "$RUN_ROOT/agentapi-health.json" 2> "$RUN_ROOT/agentapi-health.err" \
  || printf '{"status":"unreachable"}\n' > "$RUN_ROOT/agentapi-health.json"
```
**Checkpoint:** `agentapi-health.json` exists and shows the runtime reachable (not `unreachable`) before
counting any fire as real.

### Phase 3: Capture one scheduled fire as evidence
Each time the sidecar fires, the tick runs scoped and drops a fresh timestamped evidence dir. (Driven by
the sidecar's `schedule` builtin; shown here as the per-fire command the sidecar invokes.)
```bash
FIRE_DIR="$RUN_ROOT/$(date -u +%Y%m%dT%H%M%SZ)-tick"
mkdir -p "$FIRE_DIR"
{
  printf 'cwd=%s\n' "$PWD"
  printf 'mode=sidecar\n'
  printf 'runtime=agentapi\n'
  printf 'scopes=%s\n' "${REPO:-$PWD}"
  printf 'cmd=%s\n' 'agentapi-driven tick: claim 1 ready bead, do it scoped, evidence to brain, DO NOT close'
} > "$FIRE_DIR/command.txt"

# The sidecar drives the tick through the agentapi runtime; capture its event stream.
agy -p "Claim one ready bead via br. Implement only it in this worktree. Commit scoped. \
  Write evidence to brain as userFacing. Do NOT close it — a separate judge will." \
  --add-dir "${REPO:-$PWD}" --print-timeout 600 \
  > "$FIRE_DIR/events.jsonl" 2> "$FIRE_DIR/stderr.log"
echo "$?" > "$FIRE_DIR/exit-code"
```
**Checkpoint:** for the fire, `events.jsonl` is non-empty, `exit-code` is written, and `command.txt`
records scope + the agentapi runtime.

### Phase 4: Mirror the verdict + validate the fire's evidence
Persist a userFacing brain artifact so a *different* context can judge it (author != judge), then assert
the proof surface holds.
```bash
test -s "$RUN_ROOT/schedule.txt"
test -s "$RUN_ROOT/agentapi-health.json"
grep -qv 'unreachable' "$RUN_ROOT/agentapi-health.json"
test -s "$FIRE_DIR/events.jsonl"
test -s "$FIRE_DIR/exit-code"
test "$(cat "$FIRE_DIR/exit-code")" = 0
test -s "$FIRE_DIR/command.txt"
```
Verdict/evidence brain mirror: `~/.gemini/antigravity-cli/brain/<conversation-id>/<name>_verification.md`
(+ `.metadata.json`, `userFacing:true`). If any check fails, the downstream verdict is FAIL or
NEEDS-EVIDENCE.

**Checkpoint:** the fire-dir path (and brain artifact) is referenced in the bead / Agent Mail compression
so the recurring tick's evidence is discoverable downstream.

## Output Specification

**Format:** a registered AGY sidecar (`sidecar.json`, `schedule` builtin) plus a per-fire directory of
plain files (JSONL + JSON + text + exit code), mirrored to a brain artifact.
**Filename / path:** `<workdir>/.agy-evidence/sidecar/` (root) and `.../sidecar/<UTC-timestamp>-tick/` (per fire)
**Structure:**
- `schedule.txt` — sidecar name, `schedule` builtin, cadence, runtime=agentapi, scopes (REQUIRED)
- `agentapi-health.json` — agentapi runtime liveness probe (REQUIRED runtime evidence)
- per fire `events.jsonl` — the captured agentapi event stream (REQUIRED proof surface)
- per fire `exit-code` — captured `$?` (REQUIRED)
- per fire `command.txt` — argv, cwd, mode=sidecar, runtime, `--add-dir` scopes (REQUIRED)
- per fire `stderr.log` — captured stderr (recommended)
- optional `agy-version.txt`, `last-message.{txt,json}`, `verdict.md`
- brain mirror: `~/.gemini/antigravity-cli/brain/<conversation-id>/<name>_verification.md` (`userFacing:true`)

## Quality Rubric

- [ ] Cadence is the sidecar's `schedule` builtin in `sidecar.json`, not host cron, and is in `schedule.txt` (Rule 1)
- [ ] Every fire produced agentapi runtime evidence: `events.jsonl` + `agentapi-health.json` (Rule 2)
- [ ] Each fire is a fresh timestamped dir — no overwrite of a prior `events.jsonl` (Rule 3)
- [ ] Exit code captured to `exit-code` immediately after the fire and used in the verdict (Rule 4)
- [ ] Sidecar tick claimed/worked but did NOT close its own bead — judged by a distinct context (Rule 5)
- [ ] Sidecar scoped with `--add-dir` to one worktree/repo, sandboxed default (Rule 6)
- [ ] `dcg` BeforeTool hook present in `~/.gemini/settings.json` (Rule 7)
- [ ] No `claude -p` / `claude --print` anywhere; runtime is the agentapi sidecar; `agy --print` not the executor (Rule 8 / LAW 0 / Door-9)
- [ ] Verdict mirrored to a userFacing brain artifact and the fire-dir referenced in the work artifact

## Examples

- **Half-hour burndown sidecar:** `sidecar.json` `schedule` builtin `*/30 * * * *`; each fire claims one ready bead scoped to `$WT`, writes evidence to brain, does not close. The agentapi `status` endpoint is probed before counting fires real.
- **Nightly validate sweep:** `schedule` builtin `0 3 * * *`; a read-mostly tick (no author scope) drives agentapi to emit PASS/WARN/FAIL verdicts over the day's evidence dirs; events captured to `events.jsonl` per fire.
- **Cross-vendor author != judge over the sidecar:** author fires drive Gemini through agentapi; an independent judge context (`agy --model "Claude Opus ..."` or a non-AGY image) reads the brain verdict — two contexts, one recurring loop, no shared session.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Sidecar "scheduled" but no fires landed | cadence put in host cron, not the `schedule` builtin | move the cron/interval into `sidecar.json`'s `schedule` builtin; record it in `schedule.txt` (Rule 1) |
| `agentapi-health.json` shows `unreachable` | agentapi runtime not up / wrong `AGENTAPI_URL` | bring the sidecar up; confirm the agentapi port; re-probe before counting fires |
| Empty `events.jsonl` but pretty output appeared | stdout not redirected to the fire dir | redirect the tick's stdout to `events.jsonl` |
| Fires overwrite each other's evidence | reused a single dir | one fire, one timestamped dir under `.../sidecar/` (Rule 3) |
| Tick "succeeded" but downstream is wrong | exit code ignored | always `echo $? > exit-code`; key the verdict off it (Rule 4) |
| Sidecar closed its own beads | author tick allowed to close | strip close from the tick; an independent context judges, orchestrator closes (Rule 5) |
| Recurring process ran a destructive command | unattended auto-approve | the `dcg` BeforeTool hook should block it — confirm it's wired in `~/.gemini/settings.json` (Rule 7) |
| Reached for a "Claude sidecar" via `claude -p` | LAW 0 violation | sidecar runtime is the agentapi server; Claude workers go through NTM panes / subagents (Rule 8) |

## See Also / References

- [agy-native](../agy-native/SKILL.md) — the AGY image + loop primitives this sidecar tick `consumes`.
- [agy-headless-evidence](../agy-headless-evidence/SKILL.md) — the one-shot `agy -p` headless path; this skill is its recurring/daemon counterpart.
- `dcg` — destructive-command guard; the BeforeTool floor this skill keeps on for the unattended path.
- `agentops:validate` — produces the PASS/WARN/FAIL verdict over this proof surface.
- `~/dev/control-plane/IMAGE-AGY.md` — the AGY image spec; this skill closes the `cp-c6k.3.2` sidecar/agentapi proof child.
- Door-9: `agy --print` is not the scheduled executor until proven subscription-safe; LAW 0 forbids `claude -p`.
