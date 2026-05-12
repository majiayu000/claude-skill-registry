---
name: financial-model-review
description: "Reviews startup financial models for investor readiness — validates unit economics, stress-tests runway scenarios, and benchmarks metrics against stage-appropriate targets. Accepts Excel, CSV, or text."
when_to_use: >
  Use ONLY when the user has provided a financial model file (Excel/CSV)
  or a structured numerical model in pasted form, AND has asked for
  review, validation, runway analysis, or unit-economics scoring.
  Do not auto-invoke on general questions about financial models or
  fundraising metrics.
user-invocable: true
---

# Financial Model Review Skill

Help startup founders understand how investors will evaluate their financial model — validating structure, unit economics, runway, and metrics against stage-appropriate standards. Produce a thorough review with actionable improvements. The tone is founder-first: a rigorous but supportive coaching session.

## Skill Metadata

- **Author:** lool-ventures
- **Version:** managed in `founder-skills/.claude-plugin/plugin.json`
- **Compatibility:** Python 3.10+ and `uv` for script execution. `openpyxl` required for Excel parsing.
- **Imports (optional):**
  - `market-sizing:sizing.json` — validate revenue-to-SOM consistency
  - `deck-review:checklist.json` — cross-check model-to-deck number alignment
- **Exports:**
  - `report.json` → `ic-sim`, `fundraise-readiness`, `dd-readiness`
  - `unit_economics.json` → `metrics-benchmarker`, `ic-sim`
  - `runway.json` → `fundraise-readiness`

## Skill Execution Model (READ FIRST)

This skill runs **inline in the main thread** (not as a sub-agent). The main thread has full tool access including Bash, and is responsible for orchestrating the full pipeline: running producer scripts, persisting artifacts, and dispatching the financial-model-review sub-agent at specific moments.

**Two dispatch contexts for the sub-agent:**

- **Context A — Per-step analytical dispatch (Mitigation 1):** Steps for INPUTS_REVIEW, UNIT_ECONOMICS, RUNWAY_SCENARIOS, and CHECKLIST dispatch the financial-model-review agent via the `Task` tool. The agent does deep analysis and returns structured JSON. The main thread captures the JSON and pipes it through the producer script. The sub-agent does NOT write artifacts directly.
- **Context B — Post-compose coaching dispatch:** The final step dispatches the sub-agent after `compose_report.py` writes `report.md`. The sub-agent reads `report.md`, appends `## Coaching Commentary`, verifies all canonical artifacts on disk, and returns a structured success payload.

**Why this model:** In Cowork, sub-agents have a restricted tool allowlist (no Bash). By keeping orchestration in the main thread and dispatching sub-agents only for analytical or post-compose tasks that use only Read/Edit/Glob/Grep, the pipeline works correctly in both Claude Code (CLI) and Cowork.

**Tolerant JSON extraction protocol (Context A):** After dispatching the sub-agent, capture its final assistant message. The sub-agent should return raw JSON, but may wrap it in ` ```json ... ``` ` fences or add a prose preamble. Extract JSON tolerantly:

1. If the message is wrapped in a ` ```json ... ``` ` (or plain ` ``` ... ``` `) fence, strip the fence first.
2. Try to parse the stripped text directly as JSON.
3. If that fails, walk through the text looking for the first `{` character and try `json.JSONDecoder().raw_decode(text[i:])` — this is brace-aware and handles nested objects correctly (unlike regex, which truncates on the first `}`).
4. If extraction fails entirely, re-prompt the sub-agent with: "Your previous reply could not be parsed as JSON. Return ONLY the JSON object — no markdown fences, no prose preamble."

**Context-pressure note:** This skill has the highest context budget of the 5 skills. The win from Mitigation 1 is excluding sub-agent reasoning and the 40-60 KB raw `extract_model.py` output — which flows *through* the INPUTS_REVIEW dispatch: the sub-agent reads it in its own context window, returns only the corrected `inputs.json`. The artifacts themselves still accumulate in the main thread (~80-130K total), but that is manageable.

> See `founder-skills/references/skill-execution-model.md` for the full inline-skill execution model (3 dispatch contexts, Mitigation 1+2, producer contract, Cowork quirks, per-symptom triage).

## Input Formats

Accept any format: Excel (.xlsx), CSV, Google Sheets exports, financial documents, or conversational input. For Excel files, use `extract_model.py` to parse. For other formats, extract data manually into the `inputs.json` schema. If multiple copies of the same file exist (e.g., `Financials.xlsx` and `Financials (1).xlsx`), use the most recently modified version and note the duplication to the founder. If timestamps are identical, ask the founder which file to use. If the founder cannot be queried, prefer the file without parenthetical suffixes (e.g., `(1)`, `(2)`) — these typically indicate browser re-download duplicates.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/scripts/`:

- **`extract_model.py`** — Extracts structured data from Excel (.xlsx) and CSV files
- **`validate_extraction.py`** — Anti-hallucination gate: cross-references `model_data.json` against `inputs.json` to catch mismatches (company name, salary, revenue, cash traceability); run after extraction, before review
- **`validate_inputs.py`** — Four-layer validation of `inputs.json` (structural, consistency, sanity, completeness); supports `--fix` to auto-correct sign errors
- **`checklist.py`** — Scores 46 criteria across 7 categories with profile-based auto-gating
- **`unit_economics.py`** — Computes and benchmarks 11 unit economics metrics
- **`runway.py`** — Multi-scenario runway stress-test with decision points
- **`compose_report.py`** — Assembles report with cross-artifact validation; `--strict` exits 1 on high-severity warnings (corrupt/missing artifacts)
- **`apply_corrections.py`** — Processes founder's downloaded corrections file: coerces types, normalizes ILS→USD, merges overrides, writes `corrected_inputs.json` and `extraction_corrections.json`
- **`verify_review.py`** — Review completeness gate: checks artifact existence, content quality, and cross-artifact consistency; `--gate 1` for after-compose, `--gate 2` (default) for final; exit 0 = publishable, exit 1 = gaps remain
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)
- **`explore.py`** — Generates self-contained interactive HTML explorer from review artifacts; outputs HTML (not JSON)
- **`review_inputs.py`** — Dual-mode review viewer: HTTP server with live validation (Claude Code) or self-contained static HTML with JS sanity metrics (Cowork); outputs HTML

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`find_artifact.py`** — Resolves artifact paths by skill name and filename (used for cross-skill lookups)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/scripts/<script>.py --pretty [args]`

## Available References

Read as needed from `${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references/`:

- **`checklist-criteria.md`** — All 46 checklist criteria with gate definitions
- **`schema-inputs.md`** — JSON schema for `inputs.json` (the artifact the agent writes)
- **`artifact-schemas.md`** — JSON schemas for script-produced output artifacts
- **`data-sufficiency.md`** — Data sufficiency gate and qualitative path
- **`extraction-pitfalls.md`** — 8 common extraction errors (scale denomination, payroll aggregation, collections vs revenue, etc.)

From `${CLAUDE_PLUGIN_ROOT}/references/` (shared): `stage-expectations.md`, `benchmarks.md`, `israel-guidance.md`, `revenue-model-types.md`, `common-mistakes.md`

## Artifact Pipeline

Every review deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | founder context | `founder_context.py` read/init |
| 2 | `model_data.json` | `extract_model.py` (Excel/CSV in main thread) |
| 3 | `inputs.json` | Context A dispatch: INPUTS_REVIEW → `apply_corrections.py` |
| 3.5 | `corrected_inputs.json` | `apply_corrections.py` (from INPUTS_REVIEW dispatch) |
| 4 | `checklist.json` | Context A dispatch: CHECKLIST → `checklist.py` |
| 5 | `unit_economics.json` | Context A dispatch: UNIT_ECONOMICS → `unit_economics.py` |
| 6 | `runway.json` | Context A dispatch: RUNWAY_SCENARIOS → `runway.py` |
| 7 | Report | `compose_report.py` (writes both `report.json` and `report.md`) |
| 8a | HTML report | `visualize.py` |
| 8b | Explorer | `explore.py` |
| 8c | Coaching | Context B dispatch: POST_COMPOSE_COACHING |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (inputs.json), consult `references/schema-inputs.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$REVIEW_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (3–6), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

**Every Bash tool call runs in a fresh shell — variables do not persist.** Prefix every Bash call that uses these paths with the variable block below, or substitute absolute paths directly:

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/scripts"
REFS="${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references"
SHARED_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"
SHARED_REFS="${CLAUDE_PLUGIN_ROOT}/references"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="./artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: run `Glob` with pattern `**/founder-skills/skills/financial-model-review/scripts/checklist.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `./artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p ./artifacts` and proceed.

After Step 1 (when the slug is known):

```bash
REVIEW_DIR="$ARTIFACTS_ROOT/financial-model-review-${SLUG}"
mkdir -p "$REVIEW_DIR"
mkdir -p "$REVIEW_DIR/.staging"   # for ad-hoc sub-agent JSON staging (v0.4.2)
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Pass `RUN_ID` to all sub-agents. Every artifact written to `$REVIEW_DIR` must include `"metadata": {"run_id": "$RUN_ID"}` at the top level. `compose_report.py` checks that all artifact run IDs match — a mismatch triggers a `STALE_ARTIFACT` high-severity warning, blocking under `--strict`.

If `REVIEW_DIR` already contains artifacts from a previous run, remove them before starting:

    rm -f "$REVIEW_DIR"/{inputs,checklist,unit_economics,runway,report,model_data}.json "$REVIEW_DIR/report.html"

In Cowork, file deletion may require explicit permission. If cleanup fails with "Operation not permitted", request delete permission and retry before proceeding.

### Step 1: Read or Create Founder Context

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" read --artifacts-root "$ARTIFACTS_ROOT" --pretty
```

Three cases based on exit code:

**Exit 0 (found, single context):** Use the company slug and pre-filled fields. Before proceeding to extraction, use `AskUserQuestion` to ask the founder for current cash balance and date if not already stated in the conversation — this is the #1 cause of incomplete runway analysis. If files are attached, also ask about monthly burn rate unless the conversation already contains it. Batch all questions into a **single `AskUserQuestion` call**.

**Exit 1 (not found):** Use `AskUserQuestion` (NOT plain chat) to ask the founder for company details AND key financial context. **You MUST use the `AskUserQuestion` tool** — do not just list questions in the chat. Gather everything in a **single call** (one interaction = one chance for the UI to render correctly):
- Company name, stage, sector, geography (required for context creation)
- Current cash balance and date (critical for runway — the #1 cause of incomplete reports)
- Monthly burn rate if not obvious from the provided files

**IMPORTANT:** Always use the `AskUserQuestion` tool for founder questions — never ask as plain chat text. The tool provides a structured UI that renders correctly in Cowork. Always provide at least 2 options (the tool requires a minimum of 2). Valid `--stage` values: `pre-seed`, `seed`, `series-a`, `series-b`, `later` (hyphenated, not underscored).

**Why everything upfront:** Extraction sub-agents run in parallel and cannot pause to ask questions. Asking early prevents pipeline stalls.

If the founder provides files (Excel/CSV), still ask about cash balance — extraction may miss or misinterpret values, and having the founder's stated number lets the agent cross-check later.

Then create:

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" init \
  --company-name "Acme Corp" --stage seed --sector "B2B SaaS" \
  --geography "US" --artifacts-root "$ARTIFACTS_ROOT"
```

If the script prints a `sector_type` warning but exits 0, that's non-fatal — proceed without retrying. However, a null `sector_type` may suppress sector-specific checklist gating downstream. If you know the correct type, re-run with `--sector-type` (valid values: `saas`, `ai-native`, `marketplace`, `hardware`, `hardware-subscription`, `consumer-subscription`, `usage-based`).

**Exit 2 (multiple context files):** Present the list to the founder, ask which company, then re-read with `--slug`.

### Step 2: Extract Model Data

**When Excel (.xlsx) or CSV files are provided,** run `extract_model.py` directly in the main thread:

```bash
python3 "$SCRIPTS/extract_model.py" --file <path> --pretty -o "$REVIEW_DIR/model_data.json"
```

Check the `periodicity_summary` and per-sheet `periodicity` fields. If periodicity is `quarterly` or `annual`, all **flow metrics** (burn, revenue, expenses — anything measured per period) must be divided by 3 or 12 respectively in the next step. Do NOT convert stock metrics (cash balance, headcount, customer count, ARR — point-in-time snapshots). If periodicity is `unknown`, flag it.

**When documents (PDFs, data room dumps, Google Sheets exports) are provided:** Extract what you can directly from the documents, consulting `$REFS/schema-inputs.md` for the schema and `$REFS/data-sufficiency.md` for sufficiency assessment. Write a provisional `inputs.json`.

**When conversational input is provided (no files):** Gather all needed fields within Step 1 through normal conversation. Consult `references/schema-inputs.md` for the full schema.

### Sub-agent JSON staging (v0.4.2)

When a sub-agent returns JSON too large for bash heredoc, write it to
`$REVIEW_DIR/.staging/<step>_input.json` first, then pipe via:

```bash
cat "$REVIEW_DIR/.staging/<step>_input.json" | python3 "$SCRIPTS/<producer>.py" ...
```

The `.staging/` directory is created at setup and removed at cleanup.
This avoids `Operation not permitted` errors that occur when writing to
`$OUTPUTS_ROOT/` (Cowork sandbox marks that read-only post-write).

### Step 3: INPUTS_REVIEW Dispatch (Context A)

**Dispatch the financial-model-review sub-agent in Context A (INPUTS_REVIEW).** Dispatch via the `Task` tool. This is the highest context-pressure dispatch — the sub-agent reads the full `model_data.json` (40-60 KB) inside its own context window and returns only the corrected `inputs.json`. This is the primary Mitigation 1 win: the raw extraction output never accumulates in the main thread context.

**Dispatch prompt template:**

```
CONTEXT: INPUTS_REVIEW
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the financial-model-review agent dispatched in Context A (INPUTS_REVIEW).
Read model_data.json at <REVIEW_DIR>/model_data.json (the full extraction output).
Also read:
  - ${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references/schema-inputs.md
  - ${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references/extraction-pitfalls.md
  - ${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references/data-sufficiency.md

Construct a complete, valid inputs.json from the extracted data. Apply all
extraction pitfall checks (scale denomination, ARPU sanity, periodicity
conversion, company name sourcing, payroll aggregation, collections vs revenue).

ARPU sanity check: if drivers.arpu_monthly or unit_economics.ltv.inputs.arpu_monthly
exceeds total MRR, it is probably aggregate revenue, not per-customer ARPU —
divide by customer count.

Return JSON only — exactly the validated inputs.json structure per schema-inputs.md,
plus a top-level "changes" array listing what was corrected and a "base_hash"
field (sha256 of the original model_data.json content, or empty string if no
prior inputs.json existed). Shape:
{
  "changes": [
    {"path": "cash.current_balance", "expected_old": null, "new": 1500000, "type": "set"}
  ],
  "base_hash": "",
  "corrected": {<full validated inputs.json contents>}
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol (see "Skill Execution Model" preamble) to obtain the structured JSON.

**INPUTS_REVIEW special handling — file-args-based script:** Unlike other dispatch points, `apply_corrections.py` takes file arguments, not stdin. The main thread must:

1. Write the sub-agent's returned JSON to a temp file:
   ```bash
   cat <<'CORRECTIONS_EOF' > "$REVIEW_DIR/corrections_from_agent.json"
   <JSON extracted from sub-agent reply>
   CORRECTIONS_EOF
   ```
2. If `inputs.json` does not yet exist, write an empty inputs stub first:
   ```bash
   echo '{}' > "$REVIEW_DIR/inputs.json"
   ```
3. Run `apply_corrections.py` with file arguments:
   ```bash
   python3 "$SCRIPTS/apply_corrections.py" "$REVIEW_DIR/corrections_from_agent.json" \
     --original "$REVIEW_DIR/inputs.json" \
     --output-dir "$REVIEW_DIR"
   ```
4. Read the stdout JSON:
   - If `status == "completed"`: promote `corrected_inputs.json` to `inputs.json`:
     ```bash
     mv "$REVIEW_DIR/corrected_inputs.json" "$REVIEW_DIR/inputs.json"
     ```
   - If `status == "error"`: log the errors and write `inputs.json` directly from the `corrected` field in the sub-agent reply.

### Step 3.5: Validate `inputs.json` — STOP GATE

Run the validation script:

```bash
cat "$REVIEW_DIR/inputs.json" | python3 "$SCRIPTS/validate_inputs.py" --pretty
```

If `valid == false` (errors present), run with `--fix` to auto-correct fixable issues:

```bash
python3 "$SCRIPTS/validate_inputs.py" --fix < "$REVIEW_DIR/inputs.json" > "$REVIEW_DIR/inputs_fixed.json" && mv "$REVIEW_DIR/inputs_fixed.json" "$REVIEW_DIR/inputs.json"
```

Then re-validate. If errors persist after `--fix`, correct `inputs.json` manually.

Also run the extraction validation script to cross-reference `model_data.json` against `inputs.json` (if `model_data.json` exists):

```bash
python3 "$SCRIPTS/validate_extraction.py" --inputs "$REVIEW_DIR/inputs.json" --model-data "$REVIEW_DIR/model_data.json" --fix --pretty -o "$REVIEW_DIR/extraction_validation.json"
```

**Do NOT proceed to Step 4 until `valid == true` and `has_critical_warnings == false`.**

### Step 3.6: Review Extracted Values

**Path A — File extraction** (`model_format` is `spreadsheet` or `partial`):

Generate the HTML review page for the founder to inspect extracted values. In Cowork (VM, no display), use **static mode**:

```bash
python3 "$SCRIPTS/review_inputs.py" "$REVIEW_DIR/inputs.json" --static "$REVIEW_DIR/review.html" --extraction-warnings "$REVIEW_DIR/extraction_validation.json"
```

Tell the founder to open the review page, edit anything wrong, click Submit to download a corrections file, then upload it back. When they upload `corrections.json`:

```bash
python3 "$SCRIPTS/apply_corrections.py" <uploaded-file> --original "$REVIEW_DIR/inputs.json" --output-dir "$REVIEW_DIR"
```

In Claude Code (local terminal), use **server mode**:

```bash
python3 "$SCRIPTS/review_inputs.py" "$REVIEW_DIR/inputs.json" --workspace "$REVIEW_DIR" --extraction-warnings "$REVIEW_DIR/extraction_validation.json" &
```

Wait for the founder to say done, then kill the server and apply corrections.

**Path B — Conversational** (`model_format` is `conversational` or `deck`): present a confirmation table (stage, MRR, growth rate, burn, cash, customers, CAC, target raise) and use `AskUserQuestion` to confirm.

### Steps 4-6: Parallel Analysis Dispatch (Context A)

**IMPORTANT — PARALLEL DISPATCH IS MANDATORY for Steps 5 and 6:** Spawn the UNIT_ECONOMICS and RUNWAY_SCENARIOS dispatches **in a single message** — both Task calls MUST appear in the same assistant response. CHECKLIST may be dispatched alongside them or separately. No `isolation: "worktree"`.

#### CHECKLIST Dispatch

**Dispatch prompt template:**

```
CONTEXT: CHECKLIST
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the financial-model-review agent dispatched in Context A (CHECKLIST).
Read inputs.json at <REVIEW_DIR>/inputs.json.
Also read ${CLAUDE_PLUGIN_ROOT}/skills/financial-model-review/references/checklist-criteria.md.

Assess all 46 checklist items (STRUCT_01..09, UNIT_10..19, CASH_20..32,
METRIC_33..35, SCENARIO_36..38, BRIDGE_37..38, SECTOR_39..44, OVERALL_45..46).
Profile-based auto-gating applies by stage/geography/sector/model_format.

Evidence is MANDATORY for every item: every fail and warn MUST have a non-empty
evidence string citing specific values from the model. Every pass MUST have
evidence noting what was checked.

Return JSON only — items array without summary (producer script computes summary):
{"items": [{"id": "STRUCT_01", "status": "pass", "evidence": "...", "notes": null}, ...all 46 items...]}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol. Pipe through the producer script:

```bash
cat <<'CHECKLIST_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$REVIEW_DIR/checklist.json"
<JSON extracted from sub-agent reply>
CHECKLIST_EOF
```

#### UNIT_ECONOMICS Dispatch

**Dispatch prompt template:**

```
CONTEXT: UNIT_ECONOMICS
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the financial-model-review agent dispatched in Context A (UNIT_ECONOMICS).
Read inputs.json at <REVIEW_DIR>/inputs.json.

Return JSON only — the full inputs.json structure (pass-through) for unit_economics.py
to process via stdin. Include the company, revenue, expenses, unit_economics, and
cash sections. Shape:
{<full inputs.json contents>}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol. Pipe through the producer script:

```bash
cat <<'UE_EOF' | python3 "$SCRIPTS/unit_economics.py" --pretty -o "$REVIEW_DIR/unit_economics.json"
<JSON extracted from sub-agent reply>
UE_EOF
```

#### RUNWAY_SCENARIOS Dispatch

**Dispatch prompt template:**

```
CONTEXT: RUNWAY_SCENARIOS
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the financial-model-review agent dispatched in Context A (RUNWAY_SCENARIOS).
Read inputs.json at <REVIEW_DIR>/inputs.json.

Return JSON only — the full inputs.json structure (pass-through) for runway.py
to process via stdin. The company and cash sections are required; revenue and
israel_specific are optional but include if present. Shape:
{<full inputs.json contents>}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol. Pipe through the producer script:

```bash
cat <<'RUNWAY_EOF' | python3 "$SCRIPTS/runway.py" --pretty -o "$REVIEW_DIR/runway.json"
<JSON extracted from sub-agent reply>
RUNWAY_EOF
```

### Step 7: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$REVIEW_DIR" --pretty \
  -o "$REVIEW_DIR/report.json" \
  --write-md "$REVIEW_DIR/report.md"
```

`compose_report.py` writes both `report.json` and `report.md` deterministically. **Do NOT** read `report_markdown` out of `report.json` and re-write it via heredoc.

Check `validation.warnings`: fix high-severity (corrupt/missing artifacts), present medium-severity (checklist failures, runway inconsistencies, metrics gaps) in the report, note low/info. `--strict` only blocks on high-severity warnings. Fix high-severity warnings, re-deposit, re-compose.

**Post-write verification:** `compose_report.py` exits non-zero (code 2) if the declared output files don't exist or are empty after writing. If compose exits non-zero, stop and report the exact stderr — do not proceed.

### Verification Gate 1 (after compose)

```bash
python3 "$SCRIPTS/verify_review.py" --dir "$REVIEW_DIR" --gate 1 --pretty
```

**If exit code is non-zero:** read `summary.errors`. Fix the issue by re-running the failing step, then re-run `verify_review.py --gate 1`. **Do not proceed until it exits 0.**

### Steps 8a-8b: Visualize and Generate Explorer (Optional)

```bash
python3 "$SCRIPTS/visualize.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/report.html"
python3 "$SCRIPTS/explore.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/explore.html"
```

Generate files silently — present paths after Gate 2 passes.

### Step 8c: Post-Compose Coaching Commentary (Context B dispatch — POST_COMPOSE_COACHING)

**Dispatch the financial-model-review sub-agent in Context B.** Dispatch via the `Task` tool after `compose_report.py` has successfully written both `report.json` and `report.md`.

**Mitigation 2 protocol (v0.4.2):** the main thread reads the structured `coaching_payload` from `report.json` and inlines it into the dispatch prompt. The sub-agent does NOT Read full `report.md` — it consumes `coaching_payload` directly, performs Grep idempotency, Edits via the per-run uuid `insertion_marker`, and Grep-verifies all artifacts. See the financial-model-review agent body's "Context B — Post-compose coaching dispatch (POST_COMPOSE_COACHING)" section for the full procedure.

<!-- skill-quality-ci: bash-after-subagent-ok -->
```bash
COACHING_PAYLOAD="$(python3 -c '
import json, sys
data = json.load(open(sys.argv[1]))
print(json.dumps(data["coaching_payload"], indent=2))
' "$REVIEW_DIR/report.json")"
```

**Dispatch prompt template:**

```
CONTEXT: POST_COMPOSE_COACHING

You are dispatched to add coaching commentary to a financial model review.

The compose_report.py script has finished. The structured `coaching_payload`
from report.json is:

<paste $COACHING_PAYLOAD JSON here verbatim>

Follow your agent body's Context B procedure
(POST_COMPOSE_COACHING):

1. grep_idempotency_check — Grep "## Coaching Commentary" (output_mode:count)
   and Grep the EXACT coaching_payload.insertion_marker (output_mode:count)
   on coaching_payload.report_path. Apply the 6-state decision matrix.
2. Compose commentary from the inlined coaching_payload (failed_items,
   warned_items, summary, high_severity_warnings, company_name).
   If truncated:true, acknowledge that not all failures are shown.
   Do NOT Read the full report.md.
3. edit_via_marker — single Edit on coaching_payload.report_path:
     old_string = coaching_payload.insertion_marker  (EXACT uuid string)
     new_string = "## Coaching Commentary\n\n<your commentary>"
4. self_verify_artifacts_via_grep_run_id — Grep run_id from each producer
   artifact (inputs.json, checklist.json, unit_economics.json, runway.json),
   confirm all 4 match; bounded Read (limit:1) on report.json and report.md;
   re-Grep the marker (must be 0) and the "## Coaching Commentary" header
   (must be 1).
5. Return the success payload:
   {"status": "complete", "review_dir": "<path>", "report_path": "<path>",
    "runway_months": <number>, "unit_economics_status": "<status>",
    "red_flags": [<list>], "high_severity_warnings": [<list>]}
   OR if verification fails:
   {"status": "blocked", "reason": "<specific gap>"}

Stop after returning JSON. Do not narrate.
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the success/blocked payload. If `status == "blocked"`, stop and report the reason to the founder. If `status == "complete"`, proceed to Verification Gate 2.

### Step 8d: Cleanup

```bash
rm -rf "$REVIEW_DIR/.staging" 2>/dev/null || true
```

### Verification Gate 2 (final)

```bash
python3 "$SCRIPTS/verify_review.py" --dir "$REVIEW_DIR" --pretty
```

**This is the final quality gate.** If it exits non-zero, fix the issues before presenting anything to the founder. Once it passes, present everything to the founder:

1. Present `$REVIEW_DIR/report.md` — the primary deliverable (do NOT inline the markdown in the assistant message; present the file path)
2. Present the `report.html` file path
3. Present the `explore.html` file path

**Do NOT inline `report_markdown` in the assistant message.** The founder reads the file via the path. (Closing the ~80-130K context accumulation issue.)

## Main-Thread Return

This skill runs inline in the main thread (not as a sub-agent). The final outcome the main thread delivers to the founder is:

- The path to `$REVIEW_DIR/report.md` — the primary deliverable.
- The structured success payload from the Context B sub-agent: `{status, review_dir, report_path, runway_months, unit_economics_status, red_flags, high_severity_warnings}`.
- Optionally: the HTML report and explorer paths.

## Scoring

- Each of 46 items: pass / fail / warn / not_applicable
- `score_pct` = (pass + 0.5 * warn) / (total - not_applicable) * 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)
