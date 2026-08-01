# LLM Judge Extraction

Phase 4 of the compiler turns every `llm_judge` node's fuzzy prose
rubric into a typed signature with bounded inputs and outputs. This
file is the reference for that extraction.

The premise is simple: if the source skill's rubric defines a
classification (red flags, tiers, decision categories), that
classification has a natural schema — and *running it as an unbounded
LLM prompt throws away all the structure*. A typed signature recovers
the structure, makes the step regression-testable, and lets downstream
nodes consume a predictable shape instead of parsing free text.

## What a typed signature looks like

A typed signature is a Python class (or BAML function, or DSPy
Signature) with three parts:

1. **Input model** — a Pydantic BaseModel with every field the LLM
   needs, sourced from upstream nodes.
2. **Output model** — a Pydantic BaseModel with enum-bounded fields
   wherever the rubric implies a discrete choice, plus any structured
   rationale.
3. **Forward method** — the call site that dispatches to the LLM. For
   v0 this is a stub; downstream work fills it in with DSPy or BAML.

The BDR example `signatures/vet_contact.py` is the canonical reference
implementation.

## The extraction procedure

### Step 1 — Read the source rubric

Find every piece of prose in the source skill that describes how to
classify the input. For BDR's `vet_contact`, this is
`references/quality-and-vetting.md`:

- High-signal indicators (boosts)
- Red flags (discard)
- The core test ("would this person commission an RWE study?")
- Tier definitions (ideal / strong / good)
- Numeric thresholds (accuracy ≥ 85)

### Step 2 — Enumerate the decision space

Ask: what are the possible outputs? For `vet_contact`:

| Dimension | Values |
|---|---|
| Decision | `keep`, `discard` |
| Tier (if keep) | `ideal`, `strong`, `good` |
| Reason (if discard) | `indication_mismatch`, `msl_role`, `biomarker_discovery`, `translational`, `sales_commercial`, `ops_strategy`, `program_management`, `low_accuracy`, `no_valid_email`, `other` |
| Evidence | free-form string (1-2 sentences) |

Anything with a small enumerable value space becomes an **enum**. Free
text is only used for the *evidence* or *explanation* field, never for
the core decision.

**Rule of thumb:** if you can write the values in a table like the one
above, it's an enum. If the values would span a paragraph, it's free
text.

### Step 3 — Design the input model

Walk the IR backward from the node. The input model must contain every
field the LLM needs to make the decision. For `vet_contact`:

```python
class VetContactInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contact: EnrichedContact  # from enrich_contact_batch upstream
    brief: CampaignBrief  # from pipeline input
    intel: IntelBrief  # from target_research upstream
```

**`extra="forbid"`** prevents accidental field additions that would
silently break downstream reads. Strict-by-default.

### Step 4 — Design the output model

```python
class VetDecision(str, Enum):
    KEEP = "keep"
    DISCARD = "discard"


class ContactTier(str, Enum):
    IDEAL = "ideal"
    STRONG = "strong"
    GOOD = "good"


class DiscardReason(str, Enum):
    INDICATION_MISMATCH = "indication_mismatch"
    MSL_ROLE = "msl_role"
    BIOMARKER_DISCOVERY = "biomarker_discovery"
    # ... one per rubric category


class VetContactOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: VetDecision
    tier: ContactTier | None = None  # only when decision == keep
    discard_reason: DiscardReason | None = None  # only when decision == discard
    relevance_evidence: str
```

**Optional fields with `None` defaults** are how you express "this
field only applies in some decision branches" without making the
schema conditional. Downstream consumers handle the None case.

### Step 5 — Lift hard thresholds into a pre-filter

If the rubric contains any numeric threshold or enum check that can be
evaluated without the LLM, put it in the `forward()` method as a
pre-filter that short-circuits before calling the model.

From `signatures/vet_contact.py`:

```python
MIN_ACCURACY_SCORE: int = 85


class VetContact:
    async def forward(self, inputs: VetContactInput) -> VetContactOutput:
        if inputs.contact.accuracy_score < MIN_ACCURACY_SCORE:
            return VetContactOutput(
                decision=VetDecision.DISCARD,
                discard_reason=DiscardReason.LOW_ACCURACY,
                relevance_evidence=(
                    f"Accuracy score {inputs.contact.accuracy_score} "
                    f"below threshold {MIN_ACCURACY_SCORE}."
                ),
            )
        # ... dispatch to LLM for fuzzy cases
```

**Why this matters:** the pre-filter saves tokens on the obvious cases
(probably 20-40% of real contacts) and guarantees the hard rule cannot
drift. The LLM can never "forget" the accuracy threshold because it
never sees those contacts.

### Step 6 — Scaffold a seed eval set

For every `llm_judge` node, create a seed evals file at the path
referenced by the node's `eval_set:` field. Each line is one test case.

Harvest examples directly from the source rubric. For every
discard_reason enum value, construct at least one input that should
produce that reason.

For BDR `evals/vet_contact.jsonl`:

```jsonl
{"name": "msl_role_discard", "input": {"contact": {"job_title": "Medical Science Liaison, Respiratory", "employment_history": [{"title": "MSL, Oncology"}], "accuracy_score": 95}, "brief": {"therapeutic_area": "respiratory"}}, "expected": {"decision": "discard", "discard_reason": "msl_role"}}
{"name": "biomarker_discard", "input": {"contact": {"job_title": "Director, Biomarker Sciences", "accuracy_score": 92}}, "expected": {"decision": "discard", "discard_reason": "biomarker_discovery"}}
{"name": "low_accuracy_discard", "input": {"contact": {"job_title": "Sr. Director RWE", "accuracy_score": 70}}, "expected": {"decision": "discard", "discard_reason": "low_accuracy"}}
{"name": "ideal_coe", "input": {"contact": {"job_title": "Sr. Director, Real World Evidence CoE", "employment_history": [...]}}, "expected": {"decision": "keep", "tier": "ideal"}}
```

These seed examples are not a full eval suite — they're the starting
point a human can expand as they encounter real cases. But having them
in the repo means the downstream DSPy/BAML compile step has a regression
baseline to optimize against.

## Common patterns

### Pattern: "discard categories" rubric

The source skill has an explicit list of categories to reject. Each
becomes an enum member of a `Reason` enum, and the eval set has one
example per category.

### Pattern: "tier the keepers" rubric

The source skill defines tiers (ideal / strong / good) with criteria
for each. Each tier becomes an enum member of a `Tier` field, which is
optional (only set when the decision is to keep).

### Pattern: "one judge, fan out"

If the source skill applies the same judgment to a list of inputs
(vet 50 contacts, personalize 10 emails), set `fan_out: true` on the
node in the IR. The adapter will invoke the signature once per input
element in parallel. The signature itself handles one input at a time.

### Pattern: "cheap pre-filter + expensive LLM"

Almost every `llm_judge` has at least one numeric or enum constraint
hiding in the rubric. Always check.

## What does NOT belong in a signature

- **Exploratory work.** If the "classification" requires the agent to
  decide which external sources to consult, it's an `agent_loop`, not
  an `llm_judge`.
- **Unbounded generation.** If the output is a paragraph of free prose
  with no schema, reconsider whether it's the right kind. Most
  "generate a paragraph" tasks can be narrowed to a few structured
  fields (opening line + TA callout + CTA, for example).
- **Multi-step reasoning across many inputs.** Signatures take one
  bounded input and return one bounded output. If the step needs to
  reason across a batch, use `fan_out: true` so each input is its
  own invocation.

## The output of Phase 4

For each `llm_judge` node:

1. A file at `signatures/<node_name>.py` with:
   - The input model
   - The output model
   - The enum definitions
   - The signature class with a stub `forward()` method (pre-filter
     logic included; LLM dispatch raises `NotImplementedError`)
2. A file at `evals/<node_name>.jsonl` with 3–10 seed examples, one
   per distinct decision path.
3. A `signature_spec:` block embedded directly in the
   `pipeline.yaml` node — see "Cross-runtime signature_spec" below.

Record every signature extracted in the Phase 7 compilation report with
the source rubric location and a one-line summary of the output schema.
This is the audit trail for the human reviewer.

## Cross-runtime signature_spec

Python signature files (item 1 above) work for the Temporal adapter,
which emits Python and can `import` them directly. They do **not**
work for runtimes that emit a different language — the Cloudflare
adapter emits TypeScript, can't read Python, and has no way to call
into a Python BAML/DSPy client (those have native Rust binaries that
don't run on Cloudflare Workers' V8 isolate).

The IR carries a runtime-agnostic structured form alongside the path:
`signature_spec`. Every `llm_judge` node should populate it. The
adapter that consumes the IR converts the schemas to whatever native
shape its target language expects — Pydantic for Python, Zod for
TypeScript, etc.

### Field shape

```yaml
signature_spec:
  input_schema: { ... }          # JSON Schema for the input model
  output_schema: { ... }          # JSON Schema for the output model
  prompt: |                       # Jinja-style {{ var }} interpolation
    <multi-line prompt template>
  client: anthropic               # 'anthropic' | 'openai'
  model: claude-sonnet-4-6        # optional; adapter chooses default
  base_url: https://...           # optional; custom endpoint. With client
                                  # 'openai' this reaches any OpenAI-compatible
                                  # server (Ollama, vLLM, a gateway). Only set
                                  # it when the source skill names an endpoint.
  temperature: 0.0                # DO NOT SET — see below
```

Emitted code layers runtime overrides on top of these defaults —
`ROTE_MODEL_<NODE_ID>` and `ROTE_BASE_URL_<NODE_ID>` environment
variables — so pick sensible defaults and let operators retarget a
judge without re-compiling.

### Never set `temperature`

Leave `temperature` out of `signature_spec`. It reads like the
obviously-right knob for a deterministic judge, and it is a trap:
**current Anthropic models reject the parameter outright** with

```
400 invalid_request_error: `temperature` is not supported on this
model. Remove it from your request.
```

A judge carrying `temperature: 0.0` is therefore dead on arrival
against a current model, which is exactly where an operator's
`ROTE_MODEL_<NODE_ID>` override points it. Found live: a compiled
pipeline whose every judge call 400'd on the first real run.

Determinism does not come from temperature anyway. It comes from the
schema-locked decoding the adapters already emit: a forced tool call
(Anthropic), `response_format: json_schema` (OpenAI / Workers AI). The
output shape is pinned whatever the sampler does.

If a source skill *explicitly* names a temperature, set it and know
that emitted code turns it into a `ROTE_TEMPERATURE_<NODE_ID>`
override whose empty value drops the parameter again.

### Deriving the JSON Schemas

The Pydantic models you wrote in step 3 (input model) and step 4
(output model) already know how to emit JSON Schema:

```python
VetContactInput.model_json_schema()
VetContactOutput.model_json_schema()
```

Embed those dictionaries verbatim under `input_schema` and
`output_schema`. The `$defs` block stays inline — adapters resolve
references at emit time.

If you can't run Python, derive the JSON Schema by hand from the
Pydantic source:

| Pydantic | JSON Schema |
| --- | --- |
| `field: str` (required) | `{"type": "string"}` in `properties`, name in `required` |
| `field: int` | `{"type": "integer"}` |
| `field: float` | `{"type": "number"}` |
| `field: bool` | `{"type": "boolean"}` |
| `field: list[X]` | `{"type": "array", "items": <X>}` |
| `field: SomeEnum` | `{"enum": [<member values>]}` (or `$ref` to a `$defs` entry) |
| `field: X \| None = None` | `{"anyOf": [<X>, {"type": "null"}], "default": null}`, optional in `required` |
| `model_config = ConfigDict(extra="forbid")` | `"additionalProperties": false` on the object |

For nested Pydantic models, hoist the inner model into a `$defs`
entry and use `{"$ref": "#/$defs/InnerModelName"}` at the use site.
This matches Pydantic's own emission shape and lets adapters resolve
references with a single helper.

#### A key that can be null is not a required string

`required` in an *input* schema is a claim about the data a real
upstream step will hand you, and it is the single easiest way to make
a pipeline die on live data. A field that a tool returns as `null` —
on drafts, on unpublished rows, on anything half-filled — must be
either omitted from `required` or typed `{"anyOf": [{"type":
"string"}, {"type": "null"}]}`. Emitted models make a non-required
field `X | None = None`, so dropping it from `required` is enough.

Presence is not non-nullness. An observed payload that always carries
a `summary` key still tells you nothing about whether its value is
ever `null`, and schema inference from observations records the key,
not the nullability.

Found live: a weekly-report pipeline judged nine posts one at a time;
one of them had `summary: null`, the judge's input model required a
string, and the whole workflow failed on that single element. When you
have observed payloads (the baseline run's tool results), scan the
values you actually saw — any `null` in a sample is proof the field
belongs in the nullable set.

### Designing the prompt template

The prompt is a Jinja-style template. Variables are addressed by the
input model's field names (top-level only — adapters use simple
`{{ contact }}` substitution that JSON-stringifies non-string
values). Three rules:

1. **Always end with a directive that names the structured-output
   tool** — the adapter wraps the call in tool-use mode and the LLM
   needs the cue to invoke it. Example: *"Return your decision via
   the structured output tool."*
2. **Reproduce the discard-categories table inline.** The schema
   already constrains the output enum, but the prompt should still
   describe each category in prose so the LLM has the rubric.
3. **Don't paste the source skill's entire reference file** — just
   the rubric. The skill bundle has plenty of context that's
   irrelevant at decision time and inflates token cost per call.

### Worked example: vet_contact prompt

```yaml
prompt: |
  You are vetting a contact for a BDR outreach campaign.

  Apply this rubric:
  - Discard if job title indicates MSL, Biomarker/Discovery,
    Translational Research, Sales/Commercial, Operations/Strategy,
    or Program Management.
  - Discard on indication mismatch with the campaign therapeutic
    area.
  - Tier surviving contacts: ideal / strong / good based on RWE/HEOR
    signal density.

  Core test: would this person commission, design, or approve a
  real-world evidence study?

  Contact: {{ contact }}
  Campaign brief: {{ brief }}
  Intel brief: {{ intel }}

  Return your decision via the structured output tool.
```

### Pre-filter logic and signature_spec

Hard thresholds (the Step 5 pre-filter) live in **Python**, not in the
prompt. Cross-language emission is the responsibility of the runtime
adapter. The Temporal adapter calls the Python signature class, which
runs the pre-filter then dispatches to the LLM. The Cloudflare adapter
emits a TS function that calls the LLM directly — a future iteration
will model the pre-filter as a separate `pure_function` node so it
runs cross-runtime, but for v0.2 the signature_spec is "schema +
prompt only" and the pre-filter only short-circuits in the Python
runtime.

If you want a hard rule to apply on every runtime today, model it as
a separate `pure_function` node *before* the `llm_judge` and route
short-circuited inputs around the LLM via an explicit edge.
