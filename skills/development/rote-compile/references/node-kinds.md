# Node Kinds — Classification Rubric

Every step in a compiled pipeline is exactly **one** of five kinds. Phase 2
of the compiler's job is assigning the right kind to every step in the
source skill. This file is the reference for that classification.

## The five kinds

### `pure_function`

A step whose logic is fully deterministic: same input, same output, no LLM
reasoning required, no external API calls.

**Signals to recognize one:**
- The skill's prose describes a fixed transformation (e.g., "format as
  markdown with these sections", "group contacts by company").
- The skill includes literal Python, pseudocode, or a concrete formula.
- The step produces a report, a formatted output, or a structured
  summary from already-structured inputs.
- The step is a loop with a clear termination condition over
  already-gathered data.

**Anti-signals (not a `pure_function`):**
- The step calls an external service → `external_call`.
- The step makes a fuzzy judgment → `llm_judge`.
- The logic varies based on context in a way that can't be enumerated
  → `agent_loop`.

**BDR example:** `pre_enrollment_report` — takes counts of vetted, passed,
and excluded contacts and renders a fixed markdown template. No LLM, no
APIs, just string formatting.

**Common mistake:** don't miss steps where the LLM was being used to
generate obvious string templates. If the skill's prose *already shows you
the exact output format*, the LLM was doing pure formatting and the step
is a `pure_function`.

---

### `external_call`

A step that makes a deterministic call to an external service (HTTP API,
database, file system) with retry and timeout semantics.

**Signals to recognize one:**
- The skill uses a tool in a fixed, repeatable way — not exploratory.
- The call has well-known limits (batch size, rate limits) that appear
  in the skill's prose.
- The step is "fetch X from service Y given params Z" with no LLM
  reasoning about the response shape.

**Anti-signals (not an `external_call`):**
- The response requires LLM interpretation before being useful →
  that's a pair of nodes: `external_call` followed by `llm_judge`.
- The tool is being used exploratorily with variable inputs →
  `agent_loop`.
- The step is a pure in-memory computation → `pure_function`.

**BDR example:** `enrich_contact_batch` — calls
`zoominfo_enrich_contacts` with a fixed output field set and a hard batch
size of 10. The parameters don't vary run-over-run.

**Common mistake:** treating every tool call as an `external_call`. A tool
call is only an `external_call` if the *semantics* of calling it are
deterministic. If the agent decides which tool to call and what to pass
each iteration, it's an `agent_loop`.

**MCP → deterministic API:** this is the kind that most often originates
as an MCP tool call in the source skill. Compiling it has TWO required
outputs, not one:

1. An **`mcp:` binding on the node** — `server` + `tool`, exactly as the
   skill calls it (see "MCP bindings" in ir-schema.md). This is
   load-bearing: the default backend emits a working call to that tool
   from the binding, and requirements/auth features derive from it.
   Omitting it on a step that calls an MCP tool is a compilation bug.
2. The underlying vendor API the tool wraps (e.g.,
   `POST /crm/v3/objects/contacts/batch/upsert`) recorded in the
   `impl`'s docstring, so the trace from skill → MCP tool → REST
   endpoint is visible in the code.

**An mcp-bound node must be a BARE tool call.** On the default backend
the emitted step is exactly "call `server.tool(arguments)` and return
the result" — any post-processing you fold into the node silently
vanishes at emission. So the node's declared `output` must be the tool's
own result shape (which the observed baseline traffic shows you). If the
skill's step is "call the tool, then filter/match/reshape the response",
that is TWO nodes:

- an `external_call` with the `mcp:` binding whose output is the raw
  tool result, and
- a `pure_function` that does the filtering/matching/reshaping, taking
  the raw result via `inputs:`.

Real failure this rule comes from: a skill step "call
`list_organizations`, keep the org whose name matches, return its id"
compiled as one mcp-bound node with `output: {organization_id}`. The
emitted pipeline called the tool bare, returned the raw org array, and
the name-matching logic existed nowhere — the workflow crashed
dereferencing `organization_id`. Split, both halves emit working code.
The declared-output-vs-observed-schema mismatch is also what
`rote compile` warns about at cross-check time; treat that warning as
this rule being violated.

---

### `llm_judge`

A step that asks an LLM to make a classification or generation against a
rubric, with typed input and typed output. The fuzzy part is bounded —
the output space is enumerable or naturally small.

**Signals to recognize one:**
- The skill describes "apply these rules to decide X" where X is a
  bounded decision (keep/discard, tier A/B/C, a short piece of
  generated text).
- There's an explicit rubric in the skill — red flags list, core test,
  tier definitions, discard categories.
- The output has a natural schema: decision + reason + evidence.
- The input is bounded (a single contact, a single row of data) rather
  than exploratory.

**Anti-signals (not an `llm_judge`):**
- The output is free-form prose with no schema → `agent_loop`.
- The input is exploratory (search queries, research topics) → `agent_loop`.
- The "judgment" has hard numerical thresholds that could be encoded
  in Python — lift those into a pre-filter in the signature, but the
  step itself can still be an `llm_judge`.

**BDR example:** `vet_contact` — takes an enriched contact plus the
campaign brief, applies the BDR red-flags rubric, returns
`{decision: keep|discard, tier: ideal|strong|good, discard_reason: ...,
relevance_evidence: str}`. The decision is fuzzy (reading employment
history) but the output schema is tight.

**Common mistake:** running an `llm_judge` when the classification is
actually deterministic. If every dimension of the decision maps to a
boolean check on the input, it's a `pure_function`.

---

### `agent_loop`

A step that requires genuine LLM orchestration — the agent decides what
to do next, which tools to call, and when to terminate, based on
intermediate results. Reserved for genuinely exploratory work.

**Signals to recognize one:**
- The skill's prose says things like "iterate until...", "try different
  searches", "backfill when gaps appear".
- The tool choices vary run-over-run.
- The termination condition depends on intermediate results, not a
  fixed iteration count.
- The step produces a summary or brief from external research where
  the sources aren't known in advance.

**Anti-signals (not an `agent_loop`):**
- The step is a fixed sequence of API calls with known inputs → chain
  of `external_call` nodes.
- The step is an LLM classification with bounded output → `llm_judge`.
- Every "iteration" does the same thing on different inputs → a
  `pure_function` or `external_call` with `fan_out: true`.

**BDR example:** `lead_generation_loop` — starts with three parallel
ZoomInfo searches, enriches in batches, discards contacts that fail
vetting, backfills with new targeted searches until the quota is met.
Both the number of iterations and the specific queries vary per campaign.

**Required fields:** `tools` must be set on every `agent_loop` node (the
tools the agent may call). `loop_body` is optional and lists the IDs of
sub-nodes the loop invokes each iteration.

**Also set `tool_servers`** — tool name → the MCP server providing it —
for every tool whose server you can identify from the skill (the same
evidence that gives an `external_call` its `mcp.server`). Without it the
tool is a bare name: the pipeline under-reports its MCP requirements, the
user is never prompted to authenticate, and the emitted loop has to guess
which server to search. A partial map is fine; guessing is not.

**Common mistake:** leaving things as `agent_loop` when they could be
crystallized. Most skills over-use this kind on their first pass because
"the LLM was doing it" is the easiest classification. Fight the urge —
prefer any other kind when the data supports it. Every step you keep as
`agent_loop` is a run-time cost and a reliability risk.

---

### `hitl_gate`

A step where the workflow pauses waiting for a human signal before
continuing. Survives worker restarts; resumes when the signal arrives.

**Signals to recognize one:**
- The skill explicitly says "present to the user", "wait for approval",
  "the user may add or remove".
- The next step is conditional on explicit human decision.
- The skill says something "must be done manually in the UI" — the
  gate is the thing that confirms it happened.

**Anti-signals (not a `hitl_gate`):**
- The step prints output but doesn't wait for a response → that's the
  end of a pipeline or a terminal `pure_function`.
- The "human" is conceptual — there's no actual signal → still a
  `pure_function` that produces a report.

**BDR examples:**
1. `contact_review_gate` — Phase 3 pause where the BDR reviews the
   vetted contact table before CRM upload. Signal:
   `contact_review_approved`.
2. `manual_enrollment_handoff` — Phase 7 pause where the BDR manually
   enrolls contacts in HubSpot's UI. Signal: `bdr_enrollment_complete`.

**Required field:** every `hitl_gate` MUST have a `signal`. The adapter
uses this to generate the corresponding signal handler in the workflow.

**Optional field:** `notify` tells the adapter how to alert the human
reviewer when the workflow reaches the gate (Slack channel, email, etc.).

---

## Decision rules for ambiguous cases

**When a step could be two kinds, prefer the more deterministic one.** In
descending order of determinism:

```
pure_function > external_call > llm_judge > agent_loop
```

The north star is "keep the LLM at points where the input is unbounded or
ambiguous, and codify everything else." Every step you move leftward on
this ladder is tokens saved and reliability gained.

**`agent_loop` vs `external_call`:** could the agent do this with a fixed
sequence of calls? If yes, it's `external_call`s (possibly chained via
edges or fan-out). If the sequence itself varies based on intermediate
results, it's `agent_loop`.

**`llm_judge` vs `pure_function`:** does the decision depend on reading
prose (job titles, descriptions, employment histories, free text)? If
yes, it's `llm_judge`. If it depends only on numeric thresholds or enum
matching, it's `pure_function`.

**`llm_judge` vs `agent_loop`:** does the output have a schema? If yes,
it's `llm_judge`. Free-form output usually indicates the agent is
orchestrating something and you haven't found its real boundaries yet.

**`hitl_gate` vs report-producing `pure_function`:** is there an explicit
signal or approval the workflow waits for? If yes, `hitl_gate`. If the
step just prints a summary and the pipeline ends or continues
unconditionally, it's a `pure_function`.

## Cheat sheet

| Question | Kind |
|---|---|
| Is there an explicit human signal? | `hitl_gate` |
| Is it a vendor API call with fixed semantics? | `external_call` |
| Is it fully deterministic Python? | `pure_function` |
| Is it a fuzzy classification with typed output? | `llm_judge` |
| Does the agent genuinely need to decide? | `agent_loop` |
