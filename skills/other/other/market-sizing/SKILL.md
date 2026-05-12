---
name: market-sizing
description: "Builds credible TAM/SAM/SOM analysis with external validation and sensitivity testing for startup fundraising. Supports top-down, bottom-up, or dual-methodology approaches."
when_to_use: >
  Use ONLY when the user has asked to size a market or validate
  market claims, AND has provided enough context (a product/service
  description, a market segment, or a deck with TAM/SAM/SOM claims).
  Do not auto-invoke on general fundraising or strategy questions.
user-invocable: true
---

# Market Sizing Skill

Help startup founders build credible, defensible TAM/SAM/SOM analysis — the kind that earns investor trust rather than raising eyebrows. Produce a structured, validated market sizing with external sources, sensitivity testing, and a self-check against common pitfalls. The tone is founder-first: a rigorous but supportive coaching session.

## Skill Metadata

- **Author:** lool-ventures
- **Version:** managed in `founder-skills/.claude-plugin/plugin.json`
- **Compatibility:** Python 3.10+ and `uv` for script execution.
- **Exports:**
  - `sizing.json` → `financial-model-review`, `ic-sim`, `fundraise-readiness`
  - `sensitivity.json` → `financial-model-review`
  - `checklist.json` → `ic-sim`

## Skill Execution Model (READ FIRST)

This skill runs **inline in the main thread** (not as a sub-agent). The main thread has full tool access including Bash and WebFetch, and is responsible for orchestrating the full pipeline: running producer scripts, persisting artifacts, performing web research, and dispatching the market-sizing sub-agent at specific moments.

**Two dispatch contexts for the sub-agent:**

- **Context A — Per-step analytical dispatch (Mitigation 1):** Steps 5 and 6 dispatch the market-sizing agent via the `Task` tool. The key element here is **parallel dispatch**: Step 5 (methodology calculation) dispatches the agent **twice simultaneously** — one for TOP_DOWN_METHODOLOGY and one for BOTTOM_UP_METHODOLOGY — in a **single assistant turn** when the methodology is "both". The sub-agent does deep analysis and returns structured JSON. The main thread captures the JSON and pipes it through the producer script (`market_sizing.py --stdin`). The sub-agent does NOT write artifacts directly.
- **Context B — Post-compose coaching dispatch:** The final step dispatches the sub-agent after `compose_report.py --write-md` has written `report.md`. The sub-agent reads `report.md`, appends `## Coaching Commentary`, verifies all canonical artifacts on disk, and returns a structured success payload.

**Why this model:** In Cowork, sub-agents have a restricted tool allowlist (no Bash). By keeping orchestration in the main thread and dispatching sub-agents only for analytical or post-compose tasks that use only Read/Edit/Glob/Grep, the pipeline works correctly in both Claude Code (CLI) and Cowork.

**WebFetch-before-dispatch pattern:** The main thread performs WebFetch/WebSearch research calls BEFORE dispatching sub-agents. Research data is passed inline in the sub-agent prompts. Sub-agents in Cowork cannot reach the network from inside the dispatch fork (no WebFetch/WebSearch in sub-agent allowlist).

**Tolerant JSON extraction protocol (Context A):** After dispatching the sub-agent, capture its final assistant message. The sub-agent should return raw JSON, but may wrap it in ` ```json ... ``` ` fences or add a prose preamble. Extract JSON tolerantly:

1. If the message is wrapped in a ` ```json ... ``` ` (or plain ` ``` ... ``` `) fence, strip the fence first.
2. Try to parse the stripped text directly as JSON.
3. If that fails, walk through the text looking for the first `{` character and try `json.JSONDecoder().raw_decode(text[i:])` — this is brace-aware and handles nested objects correctly (unlike regex, which truncates on the first `}`).
4. If extraction fails entirely, re-prompt the sub-agent with: "Your previous reply could not be parsed as JSON. Return ONLY the JSON object — no markdown fences, no prose preamble."

> See `founder-skills/references/skill-execution-model.md` for the full inline-skill execution model (3 dispatch contexts, Mitigation 1+2, producer contract, Cowork quirks, per-symptom triage).

## Input Formats

Accept any format: pitch deck (PDF, PPTX, markdown), financial model, market data, text descriptions, or verbal description of the business.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/scripts/`:

- **`market_sizing.py`** — TAM/SAM/SOM calculator (top-down, bottom-up, or both); accepts `--stdin` for JSON piping
- **`sensitivity.py`** — Stress-test assumptions with low/base/high ranges and confidence-based auto-widening
- **`checklist.py`** — Validates 22-item self-check with pass/fail per item
- **`compose_report.py`** — Assembles report with cross-artifact validation; `--write-md` writes report.md; `--strict` exits 1 on high/medium warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`founder_context.py`** — Per-company context management (init/read/merge/validate)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/scripts/<script>.py --pretty [args]`

## Available References

Read as needed from `${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/references/`:

- **`tam-sam-som-methodology.md`** — Definitions, calculation methods, industry examples, best practices
- **`pitfalls-checklist.md`** — Self-review checklist for common mistakes
- **`artifact-schemas.md`** — JSON schemas for all analysis artifacts

## Artifact Pipeline

Every analysis deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | founder context | `founder_context.py` read/init |
| 2 | `inputs.json` | Agent (heredoc) |
| 3 | `methodology.json` | Agent (heredoc) |
| 4 | `validation.json` | Main thread (WebFetch/WebSearch research) |
| 5 | `sizing.json` | Context A dispatch: TOP_DOWN_METHODOLOGY + BOTTOM_UP_METHODOLOGY **in parallel** → `market_sizing.py --stdin` |
| 6a | `sensitivity.json` | Context A dispatch: SENSITIVITY_TEST → `sensitivity.py` |
| 6b | `checklist.json` | Context A dispatch: CHECKLIST → `checklist.py` |
| 7 | Report | `compose_report.py --write-md` (writes both `report.json` and `report.md`) |
| 8 | Coaching | Context B dispatch: POST_COMPOSE_COACHING |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (Steps 2-4), consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$ANALYSIS_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (5–6), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

**Every Bash tool call runs in a fresh shell — variables do not persist.** Prefix every Bash call that uses these paths with the variable block below, or substitute absolute paths directly:

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/scripts"
REFS="${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/references"
SHARED_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"
SHARED_REFS="${CLAUDE_PLUGIN_ROOT}/references"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/market-sizing/scripts/market_sizing.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

After Step 1 (when the slug is known):

```bash
ANALYSIS_DIR="$ARTIFACTS_ROOT/market-sizing-${SLUG}"
mkdir -p "$ANALYSIS_DIR"
mkdir -p "$ANALYSIS_DIR/.staging"   # for ad-hoc sub-agent JSON staging (v0.4.2)
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Pass `RUN_ID` to all sub-agents. Every artifact written to `$ANALYSIS_DIR` must include `"metadata": {"run_id": "$RUN_ID"}` at the top level. `compose_report.py` checks that all artifact run IDs match — a mismatch triggers a `STALE_ARTIFACT` high-severity warning, blocking under `--strict`.

If `ANALYSIS_DIR` already contains artifacts from a previous run, remove them before starting:

    rm -f "$ANALYSIS_DIR"/{inputs,methodology,validation,sizing,sensitivity,checklist,report}.json "$ANALYSIS_DIR"/report.{html,md}

In Cowork, file deletion may require explicit permission. If cleanup fails with "Operation not permitted", request delete permission and retry before proceeding.

### Step 1: Read or Create Founder Context

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" read --artifacts-root "$ARTIFACTS_ROOT" --pretty
```

**Exit 0 (found):** Use the company slug and pre-filled fields. Proceed to Step 2.

**Exit 1 (not found):** This is normal for a first run — do not treat it as an error. Use `AskUserQuestion` (NOT plain chat) to ask for company name, stage, sector, and geography. Provide at least 2 options. Then create:

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" init \
  --company-name "Acme Corp" --stage seed --sector "B2B SaaS" \
  --geography "US" --artifacts-root "$ARTIFACTS_ROOT"
```

**Exit 2 (multiple):** Present the list, ask which company, re-read with `--slug`.

### Steps 2-3: Extract Inputs & Choose Methodology

**When files are provided (deck, model, market data),** read the provided file(s) directly and extract market-relevant data. Read `$REFS/tam-sam-som-methodology.md` and `$REFS/artifact-schemas.md`.

Extract all market-relevant data. If the deck includes explicit TAM/SAM/SOM claims, record them in `inputs.json` under `existing_claims`.

Write `inputs.json`:
```bash
cat <<'INPUTS_EOF' > "$ANALYSIS_DIR/inputs.json"
{
  "company_name": "...",
  "analysis_date": "YYYY-MM-DD",
  "stage": "seed",
  "sector": "...",
  "geography": "...",
  "product_description": "...",
  "target_segments": ["..."],
  "pricing_model": "...",
  "revenue_model": "...",
  "existing_claims": {},
  "materials_provided": ["..."],
  "metadata": {"run_id": "<RUN_ID>"}
}
INPUTS_EOF
```

Write `methodology.json`:
```bash
cat <<'METH_EOF' > "$ANALYSIS_DIR/methodology.json"
{
  "approach_chosen": "both",
  "rationale": "...",
  "metadata": {"run_id": "<RUN_ID>"}
}
METH_EOF
```

**When conversational input (no files):** Extract directly from the conversation. Read `references/tam-sam-som-methodology.md`, choose the approach, and write both artifacts directly.

After writing, verify that `$ANALYSIS_DIR` contains both `inputs.json` and `methodology.json`.

### Gate: Confirm Methodology and Inputs

**MANDATORY STOP — TWO SEPARATE STEPS. DO NOT COMBINE THEM.**

**Step A: Output a chat message** with the methodology choice and key inputs. Use a formatted summary. This is a normal assistant message — NOT an AskUserQuestion call. Example:

```
Here's what I've extracted and how I plan to approach the sizing:

**Company:** Acme Corp — AI-powered compliance for fintechs
**Geography:** US
**Target segments:** Mid-market fintechs ($10M-$500M revenue)

**Methodology:** Both top-down and bottom-up
- Top-down: Global RegTech market → US share → fintech compliance segment
- Bottom-up: ~2,400 target fintechs × $48K ARPU

**Key inputs found:**
| Input | Value | Source |
|-------|-------|--------|
| Current ARR | $850K | Deck slide 7 |
| Customers | 12 | Deck slide 8 |
| ARPU (monthly) | $4,000 | Derived from ARR/customers |
| Growth rate | 15% MoM | Deck slide 9 |

**Missing / needs clarification:**
- Geographic expansion plans (US only or international?)
- Enterprise vs SMB customer split
```

If `existing_claims` were found in the deck, include them: "Your deck claims TAM of $X — I'll validate this against external sources."

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question. The question field is plain text — NO markdown, NO tables, NO bullet points.

Question: `Does this approach and these inputs look right?`
Options: `Looks good` / `Change methodology` / `Correct or add data`

**CRITICAL: The AskUserQuestion question must be ONE SHORT SENTENCE. Put ALL details in the chat message (Step A), not in the question.**

This two-step pattern (chat message then AskUserQuestion) is required because AskUserQuestion renders as plain text. Detailed content goes in the chat message; only the gate question goes in AskUserQuestion.

**If the founder selects "Looks good":** Proceed to Step 4 (External Validation).

**If "Change methodology":** Ask which approach they prefer (top-down / bottom-up / both) and why. Update `methodology.json` and repeat Steps A+B.

**If "Correct or add data":** Ask which values are wrong or missing, correct/patch `inputs.json`, and check whether the updated inputs change what methodology is viable. If so, update `methodology.json` too. Repeat Steps A+B.

### Step 4: External Validation -> `validation.json`

**The main thread performs WebFetch/WebSearch research.** Do NOT dispatch a sub-agent for this step — the main thread has WebFetch/WebSearch capability, and sub-agents in Cowork do not. Perform all web research calls yourself.

**When methodology is "both":** Research both approaches in parallel (two WebSearch calls in one assistant turn — one for top-down market data, one for bottom-up customer/ARPU data).

- **Top-down research:** WebSearch for industry reports, government statistics, analyst estimates for total market size, segment percentages, market growth rates.
- **Bottom-up research:** WebSearch for customer counts, pricing/ARPU benchmarks, competitor data, serviceable segment data.

**When methodology is single:** Perform one research pass for the chosen approach.

**When pure calculation (user provides all numbers):** Skip research. Write a stub `validation.json` with `{"skipped": true, "reason": "User-provided inputs, no external validation required"}`.

**Source quality hierarchy:** Government/regulatory > Established analysts > Industry associations > Academic > Business press > Company blogs (product facts only).

Triangulate key numbers with 2+ independent sources. Every assumption must appear in the `assumptions` array with a `name` matching script parameter names and a `category` of `sourced`, `derived`, or `agent_estimate`.

Write `validation.json` directly:
```bash
cat <<'VAL_EOF' > "$ANALYSIS_DIR/validation.json"
{
  "assumptions": [
    {"name": "industry_total", "value": 50000000000, "category": "sourced", "label": "Global RegTech market", "source_url": "...", "source_title": "...", "confidence": "high"},
    ...
  ],
  "figure_validations": [
    {"figure": "TAM", "label": "Global RegTech TAM", "status": "validated", "source_count": 2}
  ],
  "sources": [
    {"title": "...", "url": "...", "publisher": "...", "date_accessed": "YYYY-MM-DD", "supported": "industry_total"}
  ],
  "metadata": {"run_id": "<RUN_ID>"}
}
VAL_EOF
```

### Sub-agent JSON staging (v0.4.2)

When a sub-agent returns JSON too large for bash heredoc, write it to
`$ANALYSIS_DIR/.staging/<step>_input.json` first, then pipe via:

```bash
cat "$ANALYSIS_DIR/.staging/<step>_input.json" | python3 "$SCRIPTS/<producer>.py" ...
```

The `.staging/` directory is created at setup and removed at cleanup.
This avoids `Operation not permitted` errors that occur when writing to
`$OUTPUTS_ROOT/` (Cowork sandbox marks that read-only post-write).

### Step 5: Calculate TAM/SAM/SOM -> `sizing.json` (Context A dispatch)

**The dispatch pattern depends on methodology:**

#### Parallel dispatch recipe (methodology = "both")

Dispatch the market-sizing agent **TWICE in parallel** via the Task tool — one for top-down, one for bottom-up. Use a **SINGLE assistant turn** with 2 Task tool calls (NOT two sequential turns). The Claude Code harness runs both Task calls in parallel when they appear in the same assistant response.

Pseudocode for the dispatch (executed as 2 parallel Task tool_use blocks):

```
[
  Task(description="Market sizing: top-down methodology",
       prompt="CONTEXT: TOP_DOWN_METHODOLOGY\nANALYSIS_DIR: <path>\nRUN_ID: <id>\n<research data from validation.json>"),
  Task(description="Market sizing: bottom-up methodology",
       prompt="CONTEXT: BOTTOM_UP_METHODOLOGY\nANALYSIS_DIR: <path>\nRUN_ID: <id>\n<research data from validation.json>"),
]
```

**Full dispatch prompt template (TOP_DOWN_METHODOLOGY):**

```
CONTEXT: TOP_DOWN_METHODOLOGY
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the market-sizing agent dispatched in Context A (TOP_DOWN_METHODOLOGY).
Read inputs.json at <ANALYSIS_DIR>/inputs.json and validation.json at
<ANALYSIS_DIR>/validation.json.

Using the top-down approach, compute TAM/SAM/SOM. Pre-fetched research data:
<inline the relevant assumptions from validation.json — industry_total, segment_pct, share_pct>

Return JSON only — exactly the shape expected by market_sizing.py --stdin
for approach "top_down":
{
  "approach": "top_down",
  "industry_total": <number>,
  "segment_pct": <number>,
  "share_pct": <number>
}
```

**Full dispatch prompt template (BOTTOM_UP_METHODOLOGY):**

```
CONTEXT: BOTTOM_UP_METHODOLOGY
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the market-sizing agent dispatched in Context A (BOTTOM_UP_METHODOLOGY).
Read inputs.json at <ANALYSIS_DIR>/inputs.json and validation.json at
<ANALYSIS_DIR>/validation.json.

Using the bottom-up approach, compute TAM/SAM/SOM. Pre-fetched research data:
<inline the relevant assumptions from validation.json — customer_count, arpu, serviceable_pct, target_pct>

Return JSON only — exactly the shape expected by market_sizing.py --stdin
for approach "bottom_up":
{
  "approach": "bottom_up",
  "customer_count": <integer>,
  "arpu": <number>,
  "serviceable_pct": <number>,
  "target_pct": <number>
}
```

**After both sub-agents return:** apply the tolerant JSON extraction protocol (see "Skill Execution Model" preamble) to each returned message. Then pipe through the producer script for each, combining results:

```bash
# Combine top-down and bottom-up into a single "both" payload
cat <<'SIZING_EOF' | python3 "$SCRIPTS/market_sizing.py" --stdin --pretty -o "$ANALYSIS_DIR/sizing.json"
{
  "approach": "both",
  "industry_total": <from top-down sub-agent>,
  "segment_pct": <from top-down sub-agent>,
  "share_pct": <from top-down sub-agent>,
  "customer_count": <from bottom-up sub-agent>,
  "arpu": <from bottom-up sub-agent>,
  "serviceable_pct": <from bottom-up sub-agent>,
  "target_pct": <from bottom-up sub-agent>
}
SIZING_EOF
```

#### Single methodology dispatch

When methodology is "top_down" only: dispatch one TOP_DOWN_METHODOLOGY task and pipe through `market_sizing.py --stdin`.
When methodology is "bottom_up" only: dispatch one BOTTOM_UP_METHODOLOGY task and pipe through `market_sizing.py --stdin`.

For "both" mode, check the comparison section — a >30% TAM discrepancy means investigating which assumptions are flawed. TAM must match the product's actual target universe (not inflated industry totals).

**Multi-vertical / platform companies:** If `inputs.json` lists applications in 2+ distinct industries:

1. **Identify verticals** — classify as `commercial` (revenue/pilots), `r_and_d` (demonstrated feasibility, 2-3yr commercialization path), or `future` (conceptual/early).
2. **Include `commercial` and `r_and_d` in TAM.** If top-down only covers one vertical, use bottom-up as primary. When verticals have different ARPUs, compute weighted blended ARPU. `Future` verticals go in coaching commentary as upside, not in the calculated TAM.
3. **Narrow SAM and SOM** — SAM = traction + active R&D segments. SOM = beachhead only.
4. **Document scope** in `methodology.json` `rationale`.

Default to full-scope TAM. Only narrow to beachhead if the user explicitly requests it.

### Step 5.5: Reality Check

Before proceeding, answer:

1. **Laugh test:** Would an experienced VC nod or raise an eyebrow? Seed + <5 pilots + >$1B TAM = explain yourself.
2. **Scope match:** Does TAM cover all `commercial` and `r_and_d` verticals from `inputs.json`?
3. **Customer count sanity:** Can you name a representative sample of the customers in your count?
4. **Convergence integrity:** Were top-down and bottom-up parameters set independently? If you adjusted one after seeing the other, revert and accept the delta.

This step produces no artifact. If it reveals problems, fix them before proceeding.

### Steps 6a & 6b: Parallel Analysis (Sensitivity + Checklist) (Context A dispatch)

**Dispatch the market-sizing agent TWICE in parallel** via the Task tool — one for SENSITIVITY_TEST, one for CHECKLIST. Use a **SINGLE assistant turn** with 2 Task tool calls. The Claude Code harness runs both Task calls in parallel.

#### SENSITIVITY_TEST dispatch prompt template

```
CONTEXT: SENSITIVITY_TEST
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the market-sizing agent dispatched in Context A (SENSITIVITY_TEST).
Read:
- <ANALYSIS_DIR>/validation.json — for confidence tiers
- <ANALYSIS_DIR>/sizing.json — for base values and approach

Construct sensitivity input with confidence-based ranges. Tag each parameter
with confidence from validation: `sourced` (range stands), `derived`
(min +/-30%), `agent_estimate` (min +/-50%). Include EVERY `agent_estimate`
parameter — compose_report.py flags missing ones as UNSOURCED_ASSUMPTIONS.

Return JSON only — exactly the shape expected by sensitivity.py:
{
  "approach": "bottom_up|top_down|both",
  "base": {<parameter: value pairs from sizing.json>},
  "ranges": {
    "<parameter>": {"low_pct": <negative number>, "high_pct": <positive number>}
  }
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol. Then pipe through the producer script:

```bash
cat <<'SENS_EOF' | python3 "$SCRIPTS/sensitivity.py" --pretty -o "$ANALYSIS_DIR/sensitivity.json"
<JSON extracted from sub-agent reply>
SENS_EOF
```

#### CHECKLIST dispatch prompt template

```
CONTEXT: CHECKLIST
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the market-sizing agent dispatched in Context A (CHECKLIST). Read:
- ${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/references/pitfalls-checklist.md
- ${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/references/artifact-schemas.md
  (read the "Canonical 22 checklist IDs" section)
- <ANALYSIS_DIR>/inputs.json
- <ANALYSIS_DIR>/methodology.json
- <ANALYSIS_DIR>/validation.json
- <ANALYSIS_DIR>/sizing.json

Assess all 22 items with status (pass/fail/not_applicable) and notes.

Return JSON only — the items array without a summary (the producer script
computes the summary):
{
  "items": [
    {"id": "structural_tam_gt_sam_gt_som", "status": "pass", "notes": null},
    ...all 22 items...
  ]
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol. Then pipe through the producer script:

```bash
cat <<'CHECK_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$ANALYSIS_DIR/checklist.json"
<JSON extracted from sub-agent reply>
CHECK_EOF
```

**Verify after both sub-agents return:** check that `$ANALYSIS_DIR` contains fresh `sensitivity.json` and `checklist.json`. If either is missing, re-run the failed dispatch before proceeding. Share a coaching update with the founder.

### Step 7: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --pretty \
  -o "$ANALYSIS_DIR/report.json" \
  --write-md "$ANALYSIS_DIR/report.md"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Post-write verification:** `compose_report.py` exits non-zero (code 2) if the declared output files don't exist or are empty after writing. If compose exits non-zero, stop and report the exact stderr — do not proceed to Step 8.

### Step 8: Post-Compose Coaching Commentary (Context B dispatch, POST_COMPOSE_COACHING)

**Dispatch the market-sizing sub-agent in Context B** (v0.4.2 Mitigation 2).
Dispatch via the `Task` tool after `compose_report.py` has successfully written
`report.md`.

**Before dispatching**, construct the `coaching_payload` from the compose
output. Read `report.json` to extract the checklist summary, failed items, and
high-severity warnings. Read `sizing.json` for `tam`, `sam`, `som`.
Read `methodology.json` for `methodology`. Read `checklist.json` for
`confidence` (or derive from the checklist `score_pct`). Extract the
`insertion_marker` from `report.json` (the compose script emits it alongside
`report_markdown`). Do NOT pass `warned_items` from a `warn` status —
market-sizing checklist has no `warn` status, so `warned_items` is always `[]`.

**Dispatch prompt template:**

```
CONTEXT: POST_COMPOSE_COACHING
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the market-sizing agent dispatched in Context B (POST_COMPOSE_COACHING).
The main thread has already run all producer scripts and composed the final
report using the v0.4.2 Mitigation 2 protocol. Do NOT read the full report.md.

coaching_payload:
{
  "schema_version": "v0.4.2-market-sizing",
  "summary": {
    "score_pct": <number from checklist.json summary>,
    "total": <number>,
    "pass": <number>,
    "fail": <number>,
    "not_applicable": <number>
  },
  "failed_items": [<array of failed checklist item objects with id and notes>],
  "warned_items": [],
  "high_severity_warnings": [<codes from report.json validation.warnings where severity=="high">],
  "methodology": "<top_down|bottom_up|both from methodology.json>",
  "confidence": "<high|medium|low from sizing.json or checklist>",
  "tam": <tam value from sizing.json>,
  "sam": <sam value from sizing.json>,
  "som": <som value from sizing.json>,
  "company_name": "<from inputs.json>",
  "review_dir": "<ANALYSIS_DIR absolute path>",
  "report_path": "<ANALYSIS_DIR>/report.md",
  "insertion_marker": "<EXACT marker string from report.json, e.g. <!-- COACHING_INSERTION_POINT_a1b2c3d4 -->"
}

Follow the POST_COMPOSE_COACHING procedure in your agent body exactly:
1. grep_idempotency_check (6-state matrix)
2. Compose commentary from coaching_payload (failed_items only; warned_items is always [])
3. edit_via_marker (single Edit call replacing insertion_marker with ## Coaching Commentary\n\n<commentary>)
4. self_verify_artifacts_via_grep_run_id (Grep run_id in all 6 producer artifacts)
5. Return success payload

Return:
{"status": "complete", "review_dir": "<path>", "report_path": "<path>",
 "tam": <number>, "sam": <number>, "som": <number>,
 "methodology": "<top_down|bottom_up|both>",
 "confidence": "<high|medium|low>",
 "high_severity_warnings": [<list>]}
OR if any step fails:
{"status": "blocked", "reason": "<specific gap>"}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the success/blocked payload. If `status == "blocked"`, stop and report the reason to the founder. If `status == "complete"`, present `report_path` to the founder.

### Step 9 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$ANALYSIS_DIR" -o "$ANALYSIS_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 10: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_Market_Sizing.md`, `.html` (if generated), `.json` (optional).

```bash
rm -rf "$ANALYSIS_DIR/.staging" 2>/dev/null || true
```

## Edge Cases

- **Founder provided text, not a file:** When the founder describes their market in conversation rather than uploading a file, adapt: write `inputs.json` from the conversation and note reduced confidence in data-backed assertions. Set `materials_provided: ["text"]`.
- **Cross-skill context:** If `founder_context.py` returned prior deck-review or financial-model-review runs, mention relevant findings in coaching commentary (e.g., "Your deck claims $X TAM — our analysis calculates $Y"). Do not hard-fail on discrepancies; flag them for the founder.

## Main-Thread Return

This skill runs inline in the main thread (not as a sub-agent). The final outcome the main thread delivers to the founder is:

- The path to `$ANALYSIS_DIR/report.md` — the primary deliverable.
- The structured success payload from the Context B sub-agent (Step 8): `{status, review_dir, report_path, tam, sam, som, methodology, confidence, high_severity_warnings}`.
- Optionally: the HTML report path from Step 9.

**Do NOT inline `report_markdown` in the assistant message.** The founder reads the file via the path. (Closes issue #13: ~25 KB of markdown was previously round-tripped through the parent context.)

## Scoring

- Each of 22 items: pass / fail / not_applicable
- `score_pct` = pass / (total - not_applicable) x 100
- compose_report.py validates cross-artifact consistency (assumption coverage, sensitivity ranges)
