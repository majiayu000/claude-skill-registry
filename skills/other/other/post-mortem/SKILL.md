---
name: post-mortem
description: Review completed work and learn.
practices:
- dora-metrics
- sre
- lean-startup
hexagonal_role: domain
consumes:
- implement
- vibe
- council
produces:
- result.json
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
metadata:
  tier: judgment
  dependencies:
  - council
  - beads
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
output_contract: skills/council/schemas/verdict.json
---
# Post-Mortem Skill

> **Purpose:** Wrap up completed work — validate it shipped correctly, extract learnings, process the knowledge backlog, activate high-value insights, and retire stale knowledge.
>
> **Runtime note:** Hook-driven closeout is runtime-dependent. Claude/OpenCode can wire Phase 2-5 maintenance through lifecycle hooks. Codex CLI v0.115.0+ supports native hooks (same behavior). For older Codex versions without hook surfaces, finish closeout with `ao codex stop`.

## Loop position

Move **7 (capture evidence + learning, then ratchet)** of the [operating loop](../../docs/architecture/operating-loop.md). Two outputs per loop turn: evidence (test names, snapshot keys, council verdicts, citation events) recorded against the bead and `.agents/ratchet/`; learnings promoted only under the [ratchet rules](../../docs/architecture/operating-loop.md#the-promotion-ratchet) — noticed once stays in the handoff, repeats twice goes to `.agents/learnings/`, changes future behavior updates a SKILL.md or template, must-never-regress becomes a gate, core doctrine promotes into PRODUCT.md/GOALS.md/docs/cdlc.md. Most observations die at handoff. That is correct.

Six phases:
1. **Council** — Did we implement it correctly?
2. **Extract** — What did we learn?
3. **Process Backlog** — Score, deduplicate, and flag stale learnings
4. **Activate** — Promote high-value learnings to MEMORY.md and constraints
5. **Retire** — Archive stale and superseded learnings
6. **Harvest** — Surface next work for the flywheel

---

## Quick Start

```bash
/post-mortem                    # wraps up recent work
/post-mortem epic-123           # wraps up specific epic
/post-mortem --quick "insight"  # quick-capture single learning (no council)
/post-mortem --process-only     # skip council+extraction, run Phase 3-5 on backlog
/post-mortem --skip-activate    # extract + process but don't write MEMORY.md
/post-mortem --deep recent      # thorough council review
/post-mortem --mixed epic-123   # cross-vendor (Claude + Codex)
/post-mortem --skip-checkpoint-policy epic-123  # skip ratchet chain validation
```

### Codex Closeout

Codex CLI v0.115.0+ has native hooks and handles closeout automatically (no extra steps needed). For older Codex versions (hookless fallback), run these after the post-mortem workflow writes learnings and next work:

```bash
ao codex stop
ao codex status
```

`ao codex stop` uses the latest transcript or history fallback to queue/persist learnings and run close-loop maintenance without runtime hooks.

---

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--quick "text"` | off | Quick-capture a single learning directly to `.agents/learnings/` without running a full post-mortem. Formerly handled by `/retro --quick`. |
| `--process-only` | off | Skip council and extraction (Phase 1-2). Run Phase 3-5 on the existing backlog only. |
| `--skip-activate` | off | Extract and process learnings but do not write to MEMORY.md (skip Phase 4 promotions). |
| `--deep` | off | 3 judges (default for post-mortem) |
| `--mixed` | off | Cross-vendor (Claude + Codex) judges |
| `--explorers=N` | off | Each judge spawns N explorers before judging |
| `--debate` | off | Two-round adversarial review |
| `--skip-checkpoint-policy` | off | Skip ratchet chain validation |
| `--skip-sweep` | off | Skip pre-council deep audit sweep |

---

## Quick Mode

Read [references/quick-mode.md](references/quick-mode.md) when you need the `--quick` flag procedure (slug generation, direct learning write, confirmation).

---

## Execution Steps

Read [references/execution-steps.md](references/execution-steps.md) when you need the full Phase 1 procedure: pre-flight checks, reference loading (Step 0.4), checkpoint-policy preflight (0.5), plan/spec loading (Steps 1-2.3), closure integrity audit (2.4), metadata verification (2.5), deep audit sweep (2.6), council invocation (Step 3), and prediction accuracy (3.5).

### Step 2.1: Load Compiled Prevention Context

Before council and retro synthesis, load compiled prevention outputs when they exist:

- `.agents/planning-rules/*.md`
- `.agents/pre-mortem-checks/*.md`

Use these compiled artifacts first, then fall back to `.agents/findings/registry.jsonl` only when compiled outputs are missing or incomplete. Carry matched finding IDs into the retro as `Applied findings` / `Known risks applied` context so post-mortem can judge whether the flywheel actually prevented rediscovery.

## Phase 2: Extract Learnings

Read [references/phase-2-extract.md](references/phase-2-extract.md) when you need the inline learning extraction procedure: gather context (EX.1), classify (EX.2), write learnings (EX.3), test pyramid gap analysis (EX.3.5), scope classification (EX.4), findings registry (EX.5-6).

Before backlog processing, normalize reusable council findings into `.agents/findings/registry.jsonl`.

Use the tracked contract in `docs/contracts/finding-registry.md`:

- persist only reusable findings that should change future planning or review behavior
- require `dedup_key`, provenance, `pattern`, `detection_question`, `checklist_item`, `applicable_when`, and `confidence`
- `applicable_when` must use the controlled vocabulary from the contract
- append or merge by `dedup_key`
- use the contract's temp-file-plus-rename atomic write rule

After the registry mutation, refresh compiled outputs immediately so the same session can benefit from the updated prevention set.
If `hooks/finding-compiler.sh` exists, run:

```bash
bash hooks/finding-compiler.sh --quiet 2>/dev/null || true
```

#### Step ACT.3: Feed Next-Work

Actionable improvements identified during processing -> append one schema v1.4
batch entry to `.agents/rpi/next-work.jsonl` using the tracked contract in
[`../../docs/contracts/next-work.schema.md`](../../docs/contracts/next-work.schema.md)
and the write procedure in
[`references/harvest-next-work.md`](references/harvest-next-work.md).
Follow the claim/finalize lifecycle documented in `references/harvest-next-work.md`.

```bash
mkdir -p .agents/rpi
# Build VALID_ITEMS via the schema-validation flow in references/harvest-next-work.md
# Then append one entry per post-mortem / epic.
# If a harvested item already maps to a known proof surface, preserve it on the
# item as "proof_ref" instead of burying target IDs in free text. Example item:
# [{"title":"Verify the parity gate after proof propagation lands","type":"task","severity":"medium","source":"council-finding","description":"Re-run the targeted validator after the follow-up lands.","target_repo":"agentops","proof_ref":{"kind":"execution_packet","run_id":"6f36a5640805","path":".agents/rpi/runs/6f36a5640805/execution-packet.json"}}]
ENTRY_TIMESTAMP="$(date -Iseconds)"
SOURCE_EPIC="${EPIC_ID:-recent}"
VALID_ITEMS_JSON="${VALID_ITEMS_JSON:-[]}"

printf '%s\n' "$(jq -cn \
  --arg source_epic "$SOURCE_EPIC" \
  --arg timestamp "$ENTRY_TIMESTAMP" \
  --argjson items "$VALID_ITEMS_JSON" \
  '{
    source_epic: $source_epic,
    timestamp: $timestamp,
    items: $items,
    consumed: false,
    claim_status: "available",
    claimed_by: null,
    claimed_at: null,
    consumed_by: null,
    consumed_at: null
  }'
)" >> .agents/rpi/next-work.jsonl
```

#### Step ACT.4: Update Marker

```bash
date -Iseconds > .agents/ao/last-processed
```

This must be the LAST action in Phase 4.

**Phases 3-6 (Maintenance):** Read [references/maintenance-phases.md](references/maintenance-phases.md) for backlog processing, activation, retirement, and harvesting phases. Load when `--process-only` flag is set or when running full post-mortem.

## Reporting and Workflow

Read [references/user-reporting.md](references/user-reporting.md) when you need the Step 7 report template, mandatory next-`/rpi` suggestion format, workflow integration diagram, and example invocations.

## Examples

Read [references/user-reporting.md](references/user-reporting.md) for full example invocations and what happens in each mode.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Council times out | Epic too large or too many files changed | Split post-mortem into smaller reviews or increase timeout |
| No next-work items harvested | Council found no tech debt or improvements | Flywheel stable — write entry with empty items array to next-work.jsonl |
| Checkpoint-policy preflight blocks | Prior FAIL verdict in ratchet chain without fix | Resolve prior failure (fix + re-vibe) or skip checkpoint-policy via `--skip-checkpoint-policy` |
| Metadata verification fails | Plan vs actual files mismatch or missing cross-references | Include failures in council packet as `context.metadata_failures` — judges assess severity |

---

## Compound-Engineering Retro (`--compound`)

A comparative-delta mode for projects that run `ao goals measure` repeatedly
across iterations of the same domain slice. Use when a slice has ≥2 iterations
in the verdict ledger and you want to know: what improved, what regressed, and
what the learning yield was since the last run.

**Trigger:** run this mode after any `ao goals measure` where the slice has a
prior iteration record in `.agents/goals/verdict-ledger.json`.

```bash
# Confirm ≥2 iterations exist for a directive in the slice:
jq '[.records[] | select(.record_type=="iteration" and .directive_id=="d-<id>")] | length' \
   .agents/goals/verdict-ledger.json

# Run a new iteration (appends one record per directive):
ao goals measure

# Browse iteration history:
ao goals history --goal <directive-id>
```

Then follow the step-by-step procedure in
[references/compound-engineering-retro.md](references/compound-engineering-retro.md)
(Steps CE.0–CE.5): extract N and N-1 records from the ledger, compute the
verdict and satisfaction delta, count learning yield, and write the delta as a
draft learning to `.agents/learnings/YYYY-MM-DD-<slice>-iter-delta.md`.

The output learning carries `status: draft` and the run IDs of both iterations;
human or Tier-3 synthesis promotes it to `status: reviewed`.

**Closing the loop with re-steer.** When the delta shows a directive failing
chronically, the verdict ledger also drives auto re-steer: `ao goals steer
recommend` prints policy-driven directive mutations from the same ledger, and
`ao goals steer apply` writes the chosen mutation to GOALS.md — human-gated, via
the non-lossy patcher (policy `auto_apply` plus explicit confirmation; ADR-0006).
The compound retro names *what* regressed; re-steer proposes *how* the directive
should change. See the `/goals` skill.

---

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/vibe/SKILL.md` — Council validates code (`/vibe` after coding)
- `skills/pre-mortem/SKILL.md` — Council validates plans (before implementation)


## Reference Documents

- [references/post-mortem.feature](references/post-mortem.feature) — Executable spec: validate-shipped, ratcheted learning promotion, next-work harvest, result.json (soc-qk4b.2)
- [references/harvest-next-work.md](references/harvest-next-work.md)
- [references/learning-templates.md](references/learning-templates.md)
- [references/plan-compliance-checklist.md](references/plan-compliance-checklist.md)
- [references/closure-integrity-audit.md](references/closure-integrity-audit.md)
- [references/security-patterns.md](references/security-patterns.md)
- [references/checkpoint-policy.md](references/checkpoint-policy.md)
- [references/metadata-verification.md](references/metadata-verification.md)
- [references/context-gathering.md](references/context-gathering.md)
- [references/output-templates.md](references/output-templates.md)
- [references/backlog-processing.md](references/backlog-processing.md)
- [references/activation-policy.md](references/activation-policy.md)
- [references/prediction-tracking.md](references/prediction-tracking.md)
- [references/retro-history.md](references/retro-history.md)
- [references/streak-tracking.md](references/streak-tracking.md)
- [references/maintenance-phases.md](references/maintenance-phases.md)
- [references/four-surface-closure.md](references/four-surface-closure.md)
- [references/quick-mode.md](references/quick-mode.md)
- [references/execution-steps.md](references/execution-steps.md)
- [references/phase-2-extract.md](references/phase-2-extract.md)
- [references/user-reporting.md](references/user-reporting.md)
- [references/compound-engineering-retro.md](references/compound-engineering-retro.md)
