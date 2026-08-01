# Eval estimates — the `eval.yaml` sidecar

You have just read the source skill more carefully than anyone ever
will. Capture one extra artifact while that understanding is fresh: an
estimate of what the skill costs to run **as raw agent instructions**,
step by step. This powers `rote eval`'s before/after scorecard — the
number that tells the user what compilation bought them.

Write it to `eval.yaml`, next to `pipeline.yaml`. It is a sidecar, not
part of the IR: it describes how the *source skill* behaves when an
agent executes it, not how the compiled pipeline behaves.

## What you are estimating

For each step you identified in Phase 2, estimate how many **agent
turns** that step consumes when the skill runs as instructions in an
agent loop. One turn = one assistant message, usually containing one
tool call. Ranges, not points — a step that "usually takes 2 calls but
sometimes 5" is `{low: 2, high: 5}`.

Ground rules:

- **Count from the skill's own text.** If the prose says "make four
  parallel lookup calls", that's 4 tool calls but likely 1–2 turns
  (agents batch parallel calls). If it says "repeat until you have 25
  qualified contacts", estimate the realistic iteration count from any
  hints (quota sizes, batch sizes, typical yields), not the worst case.
- **Steps that repeat per item MUST declare `iterations`.** A "process
  each row" step costs its per-row turns *times the row count* — this
  is almost always the dominant term, and flattening it understates the
  whole run by 5–20×. Put the per-iteration turns in `estimated_turns`
  and the realistic item-count range in `iterations` (page sizes,
  pagination labels, batch quotas, and filter windows in the skill text
  are your evidence). The loader multiplies them; never pre-multiply.
- **Include the overhead the prose hides.** Reading reference files,
  re-checking rubric sections, correcting malformed tool calls — a
  realistic agent spends turns on these. A step whose happy path is 2
  calls is rarely under `{low: 2, high: 3}` in practice.
- **Exploration is where the range widens.** A deterministic step
  (fixed API call, fixed template) is a tight range. A research or
  search step is a wide one — say `{low: 3, high: 10}` — and that
  honesty is the point.
- **`totals` may be less than the sum.** If steps interleave or share
  context (the agent researches while it vets), give an explicit
  `totals` block with your whole-run judgment. Omit `totals` when the
  steps are genuinely sequential and the sum is right.

## Schema

```yaml
version: 1
source_skill: examples/bdr-outreach/skill
steps:
  - description: "Research target company and drug across data sources"
    node_id: target_research        # the IR node this step became, if 1:1
    phase: "1"
    estimated_turns: {low: 4, high: 10}
    estimated_tool_calls: {low: 5, high: 14}
  - description: "Resolve ZoomInfo taxonomy IDs (4 lookup calls)"
    node_id: taxonomy_lookup
    phase: "1"
    estimated_turns: {low: 1, high: 2}
    estimated_tool_calls: {low: 4, high: 4}
  - description: "Push each eligible invoice and capture its sent date"
    node_id: process_invoices_loop
    phase: "Processing"
    estimated_turns: {low: 3, high: 6}      # PER ROW —
    iterations: {low: 20, high: 90}         # — × realistic row count
totals:                             # optional — omit if the sum is right;
  low: 88                           # must be WHOLE-RUN (post-iteration)
  high: 602                         # when any step declares iterations
notes: >-
  Lead generation dominates: the loop re-queries ZoomInfo with adjusted
  filters until the quota is met; typical campaigns converge in 3-5
  iterations of 2-3 turns each.
```

Field reference:

| Field | Required | Meaning |
|---|---|---|
| `version` | yes | Always `1` |
| `source_skill` | no | Path to the skill you compiled |
| `steps[].description` | yes | The step, in the skill's own vocabulary |
| `steps[].node_id` | no | IR node id, only when the mapping is clean 1:1 |
| `steps[].phase` | no | Source skill phase, same convention as the IR |
| `steps[].estimated_turns` | yes | `{low, high}` agent turns (per iteration when `iterations` is set) |
| `steps[].estimated_tool_calls` | no | `{low, high}` tool calls, when distinct from turns |
| `steps[].iterations` | when the step repeats | `{low, high}` repeats per run (rows, pages, items); whole-run cost = turns × iterations |
| `totals` | no | Whole-run `{low, high}`; omit to mean "sum the steps (× iterations)" |
| `notes` | no | The one paragraph a reader needs to trust the numbers |

Validated by `rote.eval.sidecar.EvalEstimates` — if you can run Python,
`load_eval_estimates("eval.yaml")` is the dry check, same pattern as
`load_pipeline`.

## Calibration anchors (measured production runs)

Whole-run turn counts are regime-dependent — anchor to the skill's
*shape*, not to a universal range:

- **Sequential tool-heavy skills** (BDR-scale: 7 phases, ~20 distinct
  steps, no per-item loop): **30–57 turns** measured. ~13 seconds per
  turn including tool execution.
- **Per-item loop skills** (browser automation over a table, per-record
  processing): measured production runs landed at **184 and 730 turns**
  — the loop multiplier dominates everything else in the file. If a
  skill says "for each row…", expect hundreds of turns, not tens, and
  express it via `iterations`, never by inflating per-step turns.
- Per-step anchors: a single fixed API call step: 1–2 turns. A
  batch-and-review step: 2–4. A bounded search loop: 6–15. A genuinely
  open research step: 4–10. One iteration of a per-row browser cycle
  (locate, act, confirm, refresh): 2–6.

If your estimate lands wildly outside the anchor for the skill's shape,
re-examine before writing — either the skill really is bigger/smaller
(fine, say so in `notes`) or a step estimate is off. A per-item skill
whose whole-run total sums to under ~100 turns almost certainly has a
missing `iterations` block.

## What NOT to do

- **Do not estimate the compiled pipeline's cost.** `rote eval`
  computes that from the IR directly; your sidecar covers only the
  before side.
- **Do not put estimates in `pipeline.yaml`.** The IR stays
  runtime-agnostic and behavior-only; estimates live in the sidecar.
- **Do not give false precision.** `{low: 3, high: 3}` claims
  certainty. Reserve it for steps the skill fully pins down (fixed call
  counts, fixed batches).
- **Do not skip steps.** Every Phase 2 step appears exactly once, even
  the trivial ones — a reader reconciles your sidecar against the
  classification table.
