---
name: rote-compile
description: 'Compile a proven skill (SKILL.md plus references) into a typed deterministic
  pipeline: reviewable Python or TypeScript with per-step tests for the fixed logic,
  typed LLM-judge signatures for the steps that still need judgment'
---

# Skill Compilation

You are the rote compiler. You read fuzzy AI skills and produce reliable
workflows.

**Input:** a directory containing a `SKILL.md` and an optional `references/`
folder with sub-files.

**Output:** an intermediate representation (`pipeline.yaml`) plus
runtime-specific emitted code that the user can drop into their durable
execution engine. Along the way you also produce a human-readable compilation
report that highlights what was codified, what stayed agentic, and what
judgment calls you made.

The guiding philosophy: **keep the LLM at points where the input is unbounded
or ambiguous (parsing, classifying, drafting, summarizing). Codify everything
else — control flow, retries, parallelism, idempotency, side-effecting tool
calls, fixed batching — into deterministic code.** Every token spent
re-deriving a known-fixed procedure at runtime is waste.

## Phase Routing

| Entry Point | Start At | Example Triggers |
|---|---|---|
| Full compilation | Phase 1 → 7 | "compile the bdr-outreach skill" |
| Report only | Phase 1 → 5, skip 6 | "analyze this skill, don't emit code" |
| Re-emit for different runtime | Phase 6 | "emit the existing pipeline.yaml for inngest" |
| Update compilation after skill changed | Phase 1 → 7, diff | "recompile bdr-outreach, it changed" |

## Pipeline

**Progress markers.** At the START of each Phase N, rewrite
`progress.ndjson` in the work directory so it holds one JSON line per
phase entered so far, in order:

```
{"phase": 1, "name": "Intake"}
{"phase": 2, "name": "Node Classification"}
```

Rewrite the whole file each time (append the new phase's line to the
ones already there). This file is machine-read for live progress
display; it is not a deliverable and never affects the IR.

### Phase 1: Intake

Read the target directory exhaustively:

1. `SKILL.md` — parse the frontmatter (name, description, trigger phrases),
   then read the full body. Note every named phase, gate, and rule.
2. `references/` — read every sub-file. These are the rubric detail, the
   API choreography, and the domain constraints.
3. Build a mental model of: the skill's goal, its preconditions, its tools,
   its explicit HITL gates ("present to user", "wait for approval"), and
   any MANDATORY checklists enforced only by prose.

Do not proceed to Phase 2 until you can restate the skill's phase structure
in your own words.

### Phase 2: Node Classification

Read `references/node-kinds.md` before starting this phase.

Walk through the skill from start to finish. For every distinct step, assign
it exactly one of the five node kinds:

| Kind | Signal |
|---|---|
| `pure_function` | Fixed logic, deterministic I/O, no LLM reasoning needed |
| `llm_judge` | Fuzzy classification against a rubric, typed input/output |
| `agent_loop` | Exploratory tool use, variable path, genuinely needs LLM orchestration |
| `hitl_gate` | Explicit human review/approval required before proceeding |
| `external_call` | Deterministic API call that needs retry/timeout semantics |

When a step could be classified two ways, prefer the more deterministic
kind. The goal is to push as much as possible into `pure_function` and
`external_call`, and reserve `agent_loop` for steps where the procedure
genuinely varies from run to run.

Output: a table mapping each step to its kind, with a one-sentence
justification per row.

### Phase 3: Codification Scan

Read `references/crystallization-heuristics.md` and
`references/implementation.md` before starting this phase. The second
file governs how far to take each extracted module: contract-documented
stubs by default, **working implementations plus golden-fixture tests**
when ground truth is available (a `probe-context/` directory of observed
MCP traffic in your work dir, and/or web research tools to verify
current vendor API shapes).

For each node classified as `pure_function` or `external_call`, surface every
codification opportunity:

- **Literal pseudocode or Python pasted into the prompt.** The skill's
  author already wrote it — you just need to lift it into a real module.
- **Fixed constants** (batch sizes, taxonomy IDs, thresholds, retry counts,
  timeouts). If the prompt says "batch of 10", that 10 is a constant, not
  a judgment call.
- **Deterministic loops** with clear termination conditions.
- **String templates** for reports, output formats, or structured
  responses.
- **MANDATORY checklists** enforced by English prose. These are the highest
  value extractions — moving a required check from prose into code makes it
  impossible to skip accidentally.

For each extraction, produce a record of: source file and line, the current
prose, the proposed extracted function name and signature, and any constants
to lift into config.

### Phase 4: LLM-Judge Extraction

Read `references/llm-judge-extraction.md` before starting this phase.

For each `llm_judge` node, draft a typed signature using DSPy or BAML
conventions:

- **Input schema** (Pydantic / TypedDict): every field the LLM needs,
  sourced from upstream node outputs.
- **Output schema**: enum-bounded decisions plus structured rationale.
  Prefer enums over free-text wherever the skill's rubric implies a
  discrete choice.
- **Seed examples**: harvest 3–5 examples directly from the skill's own
  rubric. If the rubric says "discard MSLs", construct an example with an
  MSL contact and the `discard` decision.
- **Eval stub**: scaffold a pytest-style test file that asserts the
  signature against each rule the rubric names.

Output: a `signatures/<node_name>.py` file per `llm_judge` node, plus a
matching `evals/<node_name>.jsonl` seed.

### Phase 5: IR Assembly

Read `references/ir-schema.md` before starting this phase.

Assemble the full DAG as `pipeline.yaml`. Include:

- `input.input_schema`: the full JSON Schema for the pipeline input
  payload, promoted from the entry nodes' signature design (see
  `ir-schema.md`).
- `nodes`: every step from Phase 2, with its kind, input/output types,
  `inputs:` data-flow bindings (param → `pipeline.input[.field]` /
  `<node_id>.output[.field]`), timeout, retry policy, and (for
  `pure_function` / `llm_judge`) a reference to the extracted module.
  Give every node a `source.section` naming the exact SKILL.md heading
  it was derived from — this provenance is what makes incremental
  re-compilation (`rote compile --update`) possible.
- `edges`: data flow between nodes, including fan-out for batch
  processing.
- `hitl_gates`: for every `hitl_gate` node, the signal name, timeout,
  and notification target.
- `config`: top-level schedule, on_failure handler, observability
  settings.

The `pipeline.yaml` is the runtime-agnostic source of truth. Everything
Phase 6 emits is derived from it.

Alongside it, write the eval sidecar. Read
`references/eval-estimates.md`, then produce `eval.yaml` next to
`pipeline.yaml`: per-step agent-turn estimates for running the source
skill as raw instructions. You just classified every step in Phase 2 —
this captures, at near-zero extra cost, the cost model that
`rote eval`'s before/after scorecard is built on.

### Phase 6: Adapter Invocation

**You do not emit runtime code yourself.** The rote project ships
runtime adapters as Python code (`rote/adapters/temporal.py`,
`rote/adapters/inngest.py`, etc.) that consume the `pipeline.yaml` you
produced in Phase 5 and emit runnable code. Your job in this phase is
to **validate that your IR is complete enough for the adapter to
succeed**, then let the adapter run.

Checklist before declaring Phase 5 done:

- Every `pure_function` / `external_call` node has an `impl:` pointing
  at a real file you created in Phase 3.
- Every step that calls an MCP tool in the source skill carries the
  matching `mcp:` binding (see ir-schema.md — and cross-check against
  `probe-context/observed-tools.json` when it exists: observed traffic
  with no binding is a compilation bug).
- If you wrote working implementations, `tests/test_extracted.py`
  exists, is deterministic and offline, and you believe it passes.
- Every `llm_judge` node has a `signature:` pointing at a real file
  you created in Phase 4.
- Every `agent_loop` node has `tools:` listed.
- Every `hitl_gate` node has a `signal:`.
- Every node mentioned in `entry_nodes`, `exit_nodes`, `edges.from`,
  `edges.to`, and `loop_body` exists in `nodes:`.
- `rote.ir.load_pipeline(pipeline.yaml)` loads without validation
  errors. If you can call this function, run it as a dry check.

The `rote emit <pipeline.yaml> --runtime temporal --out <dir>` CLI
command (or its programmatic equivalent) takes it from there. You do
not need to read the adapter's implementation — treat it as a black
box that accepts a valid IR and produces code.

**Why the split:** the IR and its validation logic are the load-bearing
parts of compilation. Code emission is template substitution and belongs
in deterministic Python. Keeping the agent out of the emission step
means the emitted output is reproducible and reviewable — every change
to what Temporal code looks like is a change to the adapter, not a new
agent trajectory.

### Phase 7: Compilation Report

Produce a human-readable Markdown report in `compile-report.md` covering:

- **Summary metrics**: total nodes, breakdown by kind, estimated token cost
  reduction per run, list of HITL gates and what they block on.
- **Crystallization log**: every prose-to-code extraction from Phase 3,
  with before/after snippets.
- **Open questions**: ambiguous judgment calls where you made a decision
  but the human reviewer should verify. Be explicit about what you chose
  and why.
- **Suggested next steps**: what to dogfood first, which evals to run,
  which node to recompile after the first production run reveals new
  information.

## Invariants

These rules apply across every phase:

- **Never silently drop a MANDATORY check.** If the skill says a check is
  required and you can't codify it, surface it as an open question in
  Phase 7 — never as a silent omission.
- **Prefer deterministic over agentic.** When in doubt, codify. Leaving
  something agentic is a last resort for genuinely exploratory work.
- **The IR is the source of truth, not the emitted code.** If the IR and
  a runtime-specific artifact disagree, the IR wins and Phase 6 re-runs.
- **Two adapters minimum before declaring the IR generic.** Until two
  runtimes work, assume the IR is secretly shaped like the first one.
- **Dogfood yourself.** Once a stable version exists, point rote-compile
  at its own SKILL.md. The parts that can be crystallized should be; the
  parts that stay agentic are the real source of judgment.

## Related Concepts

- **"Workflow vs. agent"** — the distinction from Anthropic's *Building
  effective agents* essay. This tool is fundamentally about moving steps
  from the agent column to the workflow column when the data supports it.
- **"Blueprint First, Model Second"** — the EBF paper's framing. The
  blueprint is the `pipeline.yaml`; the LLM is a specialized tool at
  specific nodes.
- **DSPy compile** — what the `llm_judge` signatures compile *into* once
  you have enough examples. rote produces the signature; dspy.compile
  optimizes the prompt and few-shots against your eval set.
