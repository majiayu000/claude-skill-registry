---
name: financial-model-review
disable-model-invocation: true
description: "Reviews startup financial models for investor readiness — validates unit economics, stress-tests runway scenarios, and benchmarks metrics against stage-appropriate targets. Accepts Excel, CSV, or text."
compatibility: Requires Python 3.10+ and uv for script execution. openpyxl required for Excel parsing.
metadata:
  author: lool-ventures
  version: "0.3.0"
imports:
  - "market-sizing:sizing.json (optional — validate revenue-to-SOM consistency)"
  - "deck-review:checklist.json (optional — cross-check model-to-deck number alignment)"
exports:
  - "report.json -> ic-sim, fundraise-readiness, dd-readiness"
  - "unit_economics.json -> metrics-benchmarker, ic-sim"
  - "runway.json -> fundraise-readiness"
---

# Financial Model Review Skill

Help startup founders understand how investors will evaluate their financial model — validating structure, unit economics, runway, and metrics against stage-appropriate standards. Produce a thorough review with actionable improvements. The tone is founder-first: a rigorous but supportive coaching session.

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
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)
- **`explore.py`** — Generates self-contained interactive HTML explorer from review artifacts; outputs HTML (not JSON)
- **`review_inputs.py`** — Dual-mode review viewer: HTTP server with live validation (Claude Code) or self-contained static HTML with JS sanity metrics (Cowork); both modes produce corrections.json for apply_corrections.py
- **`apply_corrections.py`** — Processes founder's downloaded corrections file: coerces types, normalizes ILS→USD, merges overrides, writes `corrected_inputs.json` and `extraction_corrections.json`
- **`verify_review.py`** — Review completeness gate: checks artifact existence, content quality, and cross-artifact consistency; `--gate 1` for after-compose, `--gate 2` (default) for final; exit 0 = publishable, exit 1 = gaps remain

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`find_artifact.py`** — Resolves artifact paths by skill name and filename (used by Sub-agent B for cross-skill lookups)

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
| 2 | `model_data.json` | Sub-agent (Task) + `extract_model.py` (Excel/CSV) |
| 3 | `inputs.json` | Sub-agent (Task, single-pass or two-pass) or agent (heredoc) |
| 4 | `checklist.json` | Sub-agent (Task) + `checklist.py` |
| 5 | `unit_economics.json` | Sub-agent (Task) + `unit_economics.py` |
| 6 | `runway.json` | Sub-agent (Task) + `runway.py` |
| 7 | Report | `compose_report.py` reads all |
| 8a | HTML report | `visualize.py` |
| 8b | Commentary | agent-written `commentary.json` |
| 8c | Explorer | `explore.py` |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (Step 2), consult `references/schema-inputs.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$REVIEW_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4–6), share a one-sentence finding before moving on.

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

### Step 2: Extract Model Data and Build `inputs.json`

**When Excel (.xlsx) or CSV files are provided,** spawn a `general-purpose` Task sub-agent to handle extraction and input construction. The sub-agent receives: file path, `SCRIPTS`, `REFS`, `SHARED_REFS`, and `REVIEW_DIR` paths. **Do NOT use `isolation: "worktree"`** — files written in a worktree won't appear in the main `$REVIEW_DIR`. **Save the sub-agent's ID** — you may need to resume it in Step 2.5 if extraction validation fails.

The sub-agent:
1. Runs `extract_model.py --file <path> --pretty -o "$REVIEW_DIR/model_data.json"` (note: `--file`, not positional)
2. **Checks the `periodicity_summary` and per-sheet `periodicity` fields** in the extraction output. If periodicity is `quarterly` or `annual`, all **flow metrics** (burn, revenue, expenses — anything measured per period) must be divided by 3 or 12 respectively before writing to `inputs.json`. **Do NOT convert stock metrics** (cash balance, headcount, customer count, ARR — point-in-time snapshots). For time-series data, use `revenue.quarterly[]` instead of forcing quarterly observations into `revenue.monthly[]`. If periodicity is `unknown`, flag it for the main agent to ask the founder — do not guess. Record the conversion in `metadata.source_periodicity` and `metadata.conversion_applied`.
3. Reads `$REFS/schema-inputs.md` for the JSON schema
4. Reads `$REFS/data-sufficiency.md` to assess data sufficiency
5. Constructs `inputs.json` from extracted data, writing it to `$REVIEW_DIR/inputs.json`
6. **FX rate for Israeli companies:** If `geography` is "Israel", use web search to get the current ILS/USD exchange rate and populate `israel_specific.fx_rate_ils_usd`. **Do not use a hardcoded default** — exchange rates change frequently and an outdated rate will skew all ILS-denominated values. Also set `ils_expense_fraction` (typically 0.5 for Israeli startups — salaries in ILS, revenue in USD). This enables the ILS/USD toggle in the review page and FX sensitivity in the explorer.

Instruct the sub-agent: **Do not run any scripts other than `extract_model.py`. Do not create any files other than `model_data.json` and `inputs.json`.** Before writing `inputs.json`, verify that no numeric field is null when the source data contains a value — null fields cascade into bad downstream outputs (unit economics scores wrong metrics, runway reports infinite runway). **ARPU sanity check:** If `drivers.arpu_monthly` or `unit_economics.ltv.inputs.arpu_monthly` exceeds total MRR, it's probably the aggregate revenue, not per-customer ARPU. Divide by customer count to get the correct value. This is the most common extraction error. Return ONLY: (1) file paths written, (2) company name/stage/sector, (3) `model_format`, (4) data sufficiency verdict (sufficient/insufficient + count of missing critical fields), (5) any `company.traits` detected, and (6) **confidence per key field** — for each extracted metric, report `high` (directly stated in source), `low` (inferred, converted, or single data point), or `missing`. Do not echo the full JSON back.

**Extraction constraints:**
- Use `arpu_monthly` and `churn_monthly` as field names in `ltv.inputs` (not `arpu`/`churn`).
- Populate `revenue.customers` with the current customer count.
- ARPU is **per-customer** average revenue: `ARPU = MRR / customer_count`. Never use total revenue as ARPU.
- Place `arr` at the top level of each `monthly[]` entry (per schema), not inside `drivers`.
- Do NOT compute derived metrics (burn multiple, LTV/CAC, Rule of 40, etc.). Only scripts produce metric values.
- If `growth_rate_monthly` cannot be reliably determined (pre-revenue, lumpy enterprise billing, forecast-only), set it to `null` — never use `0.0` as a stand-in for "unknown." Validation will flag the gap.
- Create ONLY `model_data.json` and `inputs.json`. No summaries, notes, or extra artifacts.

**Read `$REFS/extraction-pitfalls.md` before constructing inputs.json** — 8 common errors (scale denomination, company name sourcing, payroll aggregation, collections vs revenue, expense coverage, SaaS metrics tabs, actuals vs forecast, volatile growth) that produce wildly wrong downstream results.

After the sub-agent returns, **proceed to Step 2.5: Validate Extraction** before continuing.

### Step 2.5: Validate Extraction — Anti-Hallucination Gate

Run the extraction validation script to cross-reference `model_data.json` against `inputs.json`:

```bash
python3 "$SCRIPTS/validate_extraction.py" --inputs "$REVIEW_DIR/inputs.json" --model-data "$REVIEW_DIR/model_data.json" --fix --pretty -o "$REVIEW_DIR/extraction_validation.json"
```

The `--fix` flag automatically corrects scale denomination issues (e.g., model in $000 → multiplies all monetary fields by 1000). It only applies when a scale indicator is found in `model_data` AND values appear implausibly low. It will not double-scale already-correct values. When a fix is applied, the output includes `"fixed": true` and `metadata.scale_correction` is written to `inputs.json`.

**If `status` is `"warn"` (after --fix):** Check `correction_hints` for specific issues. Scale issues are auto-fixed; remaining warnings (company name mismatch, untraceable values) may need manual correction. Resume the extraction sub-agent (using the saved agent ID from Step 2) with the correction hints and ask it to fix the flagged values. Then re-run the validation **without --fix** (scale is already handled). **Maximum 2 retries** — if warnings persist after 2 attempts, proceed to Step 3 with the warnings intact; they will appear as a banner in the review page for the founder to see.

**If `status` is `"pass"` or `"skip"`:** Proceed to Step 3.

Pass `$REVIEW_DIR/extraction_validation.json` to Step 3 so it can be displayed in the review page.

**When documents (PDFs, data room dumps, Google Sheets exports) are provided,** use a two-pass sub-agent flow:

1. **Probe pass:** Spawn a `general-purpose` Task sub-agent with the file path(s), `SCRIPTS`, `REFS`, `SHARED_REFS`, and `REVIEW_DIR` paths. The sub-agent reads the document(s), reads `$REFS/schema-inputs.md` for the schema, extracts what it can, and returns ONLY: (1) partial data extracted (company name, stage, sector, any metrics found), (2) `model_format`, (3) a list of fields that could not be extracted, and (4) any `company.traits` detected. Save the sub-agent's ID for resumption. **Important:** Always prefer explicit labeled fields in the spreadsheet (e.g., a "Company Name" cell in a Controls/Settings tab) over filenames or cover page text when extracting company identity fields.

2. **Build pass:** Resume the same sub-agent (using `resume` with the saved agent ID — preserves full document context). Pass the founder's answers from Step 1 to fill any gaps. The sub-agent reads `$REFS/data-sufficiency.md`, constructs `inputs.json`, and writes it to `$REVIEW_DIR/inputs.json`. Returns ONLY: (1) file paths written, (2) data sufficiency verdict (sufficient/insufficient + count of missing critical fields), (3) final `model_format`, and (4) **confidence per key field** — for each extracted metric, report `high`, `low`, or `missing`.

After the sub-agent returns, **proceed to Step 2.5: Validate Extraction** (same as the spreadsheet path above) before continuing to Step 3.

**When conversational input is provided (no files):** Handle directly in the main agent — the data is already in the conversation. Gather all needed fields within Step 1 through normal conversation (not via `AskUserQuestion` after extraction starts). Ask for: revenue figures, cost structure, headcount, funding history, growth rates, key assumptions. Consult `references/schema-inputs.md` for the full schema. Since there are no files to extract, there is no extraction pipeline to block — but all data gathering must complete before dispatching sub-agents in Steps 4-6.

```bash
cat <<'INPUTS_EOF' > "$REVIEW_DIR/inputs.json"
{...inputs JSON — see references/schema-inputs.md for format...}
INPUTS_EOF
```

### Step 3: Review Extracted Values

**Path A — File extraction** (`model_format` is `spreadsheet` or `partial`):

**MANDATORY — READ THIS FIRST:**
1. Do NOT show a summary table, preview, or confirmation dialog in chat. Do NOT ask the founder to confirm values in chat. Do NOT present extracted values as a message.
2. Generate the HTML review page IMMEDIATELY using the commands below.
3. Present the file path or URL to the founder so they can open it. In Cowork, present the full `file://` path.
4. The HTML page IS the review interface — all review happens there, not in chat.

**Environment detection:** If you are in Cowork (VM, no display, `/sessions/` path), use **static mode**. Otherwise (Claude Code, local terminal), use **server mode**.

#### Server mode (Claude Code)

```bash
pkill -f "review_inputs.py.*--workspace" 2>/dev/null  # kill any stale viewer from a previous run
python3 "$SCRIPTS/review_inputs.py" "$REVIEW_DIR/inputs.json" --workspace "$REVIEW_DIR" --extraction-warnings "$REVIEW_DIR/extraction_validation.json" &
```

Tell the founder:

> I've opened a review page in your browser. The extracted values are shown in 6 tabs — edit anything that looks wrong. Warnings will appear if the validation detects issues. When done, click Submit and tell me you're done.

Wait for the founder to say they're done.

```bash
pkill -f "review_inputs.py.*--workspace" 2>/dev/null
python3 "$SCRIPTS/apply_corrections.py" "$REVIEW_DIR/corrections.json" --original "$REVIEW_DIR/inputs.json" --output-dir "$REVIEW_DIR"
```

#### Static mode (Cowork)

```bash
python3 "$SCRIPTS/review_inputs.py" "$REVIEW_DIR/inputs.json" --static "$REVIEW_DIR/review.html" --extraction-warnings "$REVIEW_DIR/extraction_validation.json"
```

Tell the founder:

> I've generated a review page. Open the file and review the extracted values — the sanity metrics update live as you edit. When done, click Submit to download a corrections file, then upload it back here.

Wait for the founder to upload `corrections.json`.

```bash
python3 "$SCRIPTS/apply_corrections.py" <uploaded-file> --original "$REVIEW_DIR/inputs.json" --output-dir "$REVIEW_DIR"
```

> `apply_corrections.py` accepts both patch-based payloads (v2: `changes[]` + `base_hash`) and legacy payloads (v1: `corrected` object). The review UI emits v2 format. If applying a manually constructed corrections file, use the v2 format.

#### After apply_corrections (both modes)

Read the stdout JSON:
- If `status == "completed"`: replace `inputs.json` with `corrected_inputs.json`:
  ```bash
  mv "$REVIEW_DIR/corrected_inputs.json" "$REVIEW_DIR/inputs.json"
  ```
- If `status == "error"`: show the errors to the founder, explain what needs fixing, and ask them to re-edit and re-submit.

The review page includes live sanity checks (runway, burn multiple, ARPU consistency, expense coverage). In server mode, full Python validation runs live via `/api/check`. In static mode, JS-computed sanity metrics provide immediate feedback. Full Python validation runs in Step 3.5 after corrections are applied.

**Path B — Conversational / deck extraction** (`model_format` is `conversational` or `deck`):

Present the confirmation table to the founder as a normal conversation message (8-field table with confidence flags). Use AskUserQuestion to enforce the stop. Apply any corrections to `inputs.json` before continuing.

| # | Field | Value | Confidence |
|---|-------|-------|------------|
| 1 | Stage | seed / series-a / etc. | — |
| 2 | MRR | $X | high/low/missing |
| 3 | Growth rate (MoM) | X% | high/low/missing |
| 4 | Monthly burn | $X | high/low/missing |
| 5 | Cash balance | $X | high/low/missing |
| 6 | Customers | X | high/low/missing |
| 7 | CAC | $X | high/low/missing |
| 8 | Target raise | $X | high/low/missing |

**Both paths:** Do NOT proceed to Step 3.5 until the founder has confirmed. Step 3.5 (validate_inputs.py) still runs — the validation gate is NOT bypassed.

**Step 3.5 addition — founder override promotion:** When `has_critical_warnings == true` and the inputs contain founder overrides (`reviewed_by: "founder"`), the agent reads the founder's rationale for each. If the agent agrees the data is correct, it promotes the override by adding a new entry with `reviewed_by: "agent"` (keeping the founder's entry for audit) and re-runs validation. If the agent disagrees, it corrects `inputs.json` and removes the founder override. Only agent overrides clear `has_critical_warnings`.

**Data sufficiency:** After confirming extracted values with the founder, consult `references/data-sufficiency.md` to determine if enough quantitative data is available. If 3+ critical fields are missing, follow the data sufficiency gate procedure.

**Setting `model_format`:** `spreadsheet` (Excel/CSV/Google Sheets), `deck` (pitch deck), `conversational` (gathered through conversation), `partial` (incomplete spreadsheet). When `model_format` is `deck` or `conversational`, structural items auto-gate to `not_applicable`.

**AI-powered products:** Include `"ai-powered"` in `company.traits` ONLY if there is explicit evidence in the source files that AI/ML inference is a core product feature — e.g., COGS showing GPU/inference costs, product descriptions mentioning ML models, or inference-related line items. Do NOT infer `ai-powered` from the sector name alone (e.g., "Fintech" does not imply AI).

**Graceful degradation:** If Task tool is unavailable, extract directly in the main agent.

### Step 3.5: Validate `inputs.json` Before Proceeding — STOP GATE

Run the validation script:

```bash
cat "$REVIEW_DIR/inputs.json" | python3 "$SCRIPTS/validate_inputs.py" --pretty
```

If `valid == false` (errors present), run with `--fix` to auto-correct fixable issues:

```bash
python3 "$SCRIPTS/validate_inputs.py" --fix < "$REVIEW_DIR/inputs.json" > "$REVIEW_DIR/inputs_fixed.json" && mv "$REVIEW_DIR/inputs_fixed.json" "$REVIEW_DIR/inputs.json"
```

Then re-validate. If errors persist after `--fix`, correct `inputs.json` manually (e.g., fill nulls from founder-provided data in Step 1).

**Do NOT proceed to Step 4 until `valid == true` and `has_critical_warnings == false`.** If `has_critical_warnings` is true, investigate the flagged warnings (these signal likely data errors such as wrong periodicity or implausible magnitudes) and correct `inputs.json` before dispatching sub-agents. If investigation confirms the data is correct (e.g., enterprise SaaS with lumpy deal flow), record the override in `metadata.warning_overrides` (see `schema-inputs.md`) and proceed. Non-critical warnings are informational and do not block.

Additional manual checks:
- **Cash balance missing?** If `cash.current_balance` is null but burn rate is known, use the value collected in Step 1. If the founder didn't provide it in Step 1, proceed without it — the runway analysis will flag the gap, and coaching commentary should note that cash balance is needed for a complete picture.

Fix any issues in `inputs.json` before dispatching the parallel sub-agents. Fixing between sub-agent dispatches (e.g., after checklist but before metrics) breaks the parallel rule.

### Steps 4-6: Parallel Analysis (Checklist + Metrics & Runway)

**IMPORTANT — PARALLEL DISPATCH IS MANDATORY:** Spawn 2 `general-purpose` Task sub-agents **in a single message** — both Agent tool calls MUST appear in the same assistant response. This is not a suggestion. If you spawn Sub-agent A first and wait for its result before spawning Sub-agent B, you are violating this rule. No `isolation: "worktree"`. Each receives the expanded `SCRIPTS`, `REFS`, `SHARED_SCRIPTS`, `SHARED_REFS`, and `REVIEW_DIR` paths.

**Sub-agent A — Checklist Scorer:**

Reads `$REFS/checklist-criteria.md`, reads `$REVIEW_DIR/inputs.json`, assesses all 46 items with evidence, and runs `checklist.py`. **Do not run any other scripts** — only `checklist.py`. Do not create any files other than `checklist.json`.

| Format | Assess | Auto-gated by script |
|--------|--------|---------------------|
| `spreadsheet` | All 46 items | None |
| `deck` / `conversational` | 24 business-quality items | STRUCT_01–09, CASH_20–32 (22 items) |
| `partial` | All 46 items | None |

```bash
cat <<'CHECK_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$REVIEW_DIR/checklist.json"
{"items": [
  {"id": "...", "status": "pass", "evidence": "...", "notes": null},
  ...all 46 items...
], "company": {...from inputs.json...}, "metadata": {...from inputs.json if present...}}
CHECK_EOF
```

**Evidence is MANDATORY for every item:** Every `fail` and `warn` item MUST have a non-empty `evidence` string explaining WHY it failed/warned, citing specific values from the model. Every `pass` item MUST have `evidence` noting what was checked. Empty evidence produces blank lines in the final report — this is a quality gate failure.

Instruct Sub-agent A: **Return ONLY a short JSON object** with keys: `path`, `score_pct`, `overall_status`, `top_issues` (array of max 3 strings). Do not return tables, recommendations, category breakdowns, or any other text. Keep total output under 500 characters.

**Sub-agent B — Metrics & Runway:**

Runs `unit_economics.py`, `runway.py`, and cross-skill lookups.

```bash
cat "$REVIEW_DIR/inputs.json" | python3 "$SCRIPTS/unit_economics.py" --pretty -o "$REVIEW_DIR/unit_economics.json"
cat "$REVIEW_DIR/inputs.json" | python3 "$SCRIPTS/runway.py" --pretty -o "$REVIEW_DIR/runway.json"
```

Cross-skill: Use `find_artifact.py` to locate prior market-sizing and deck-review artifacts. If market-sizing found, compare projected Year 3 ARR against SOM. If deck-review found, cross-reference financial claims. Record findings for coaching commentary. If neither found, note and proceed.

If the main agent indicates the **qualitative path** (data insufficient for quantitative analysis), Sub-agent B deposits stubs instead of running unit_economics/runway scripts: `{"skipped": true, "reason": "qualitative path — insufficient quantitative data"}`

Instruct Sub-agent B: **Do not run any scripts other than `unit_economics.py`, `runway.py`, and `find_artifact.py`. Do not create any files other than `unit_economics.json` and `runway.json`.** After running `unit_economics.py`, sanity-check the burn multiple — if it exceeds 20x for a company with meaningful ARR (>$500K), re-examine the `growth_rate_monthly` and `monthly_net_burn` inputs for unit inconsistency (e.g., monthly vs. annual mixing). **Return ONLY a short JSON object** with keys: `paths` (array), `burn_rate`, `runway_months`, `ltv_cac`, `burn_multiple`, `cross_skill` (string or null). Do not return tables, recommendations, or any other text. Keep total output under 500 characters.

If `runway.py` produces minimal output (< 500 bytes) due to missing `cash_balance_current`, note this gap explicitly — the coaching commentary should address it.

**Graceful degradation:** If Task tool is unavailable, run Steps 4-6 sequentially in the main agent.

After both sub-agents return, share a brief coaching update with the founder before proceeding to Step 7.

After both sub-agents return, verify that `$REVIEW_DIR` contains fresh `checklist.json`, `unit_economics.json`, and `runway.json`. If any are missing, the corresponding sub-agent failed — re-run it before proceeding.

**Post-dispatch corrections:** If `inputs.json` is corrected after sub-agents have completed (e.g., due to data errors discovered during report composition), re-run only the sub-agents whose outputs reference the corrected values. Single re-runs are permitted — the parallel dispatch mandate applies to the initial launch, not to error recovery.

### Step 7: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$REVIEW_DIR" --pretty -o "$REVIEW_DIR/report.json" --strict
```

Check `validation.warnings`: fix high-severity (corrupt/missing artifacts), present medium-severity (checklist failures, runway inconsistencies, metrics gaps) in the report, note low/info. `--strict` only blocks on high-severity warnings — medium-severity warnings like `CHECKLIST_FAILURES` are review findings to present, not data errors to fix. This is a refinement loop — fix high-severity warnings, re-deposit, re-compose. If a warning flags a computed value that looks implausible (e.g., burn multiple > 20x), investigate the source artifact's inputs before re-composing — the fix may be in `inputs.json` or `unit_economics.json`, not in the compose step. If a `RUNWAY_INCONSISTENCY` warning mentions cash direction (cash increasing despite positive burn), check `inputs.json` for null or zero fields that should have values — null fields are the most common cause of phantom 'infinite runway' results.

**Primary deliverable:** Read `report_markdown` from the output JSON and write it to `$REVIEW_DIR/report.md`. **Do not display the report to the founder yet** — it will be presented after the final verification gate passes (Gate 2 below).

### Verification Gate 1 (after compose)

```bash
python3 "$SCRIPTS/verify_review.py" --dir "$REVIEW_DIR" --gate 1 --pretty
```

**If exit code is non-zero:** read `summary.errors`. Each error names the artifact and what's wrong. Fix the issue by re-running the failing step, then re-run `verify_review.py --gate 1`. **Do not proceed to Step 8 until it exits 0.**

### Step 8a: Visualize (Optional)

```bash
python3 "$SCRIPTS/visualize.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/report.html"
```

Generate the file silently — it will be presented after Gate 2 passes.

### Step 8b: Write Commentary (Quantitative Path Only — MANDATORY)

**Do NOT skip this step.** The explorer (Step 8c) depends on `commentary.json` — without the `headline` field, the explorer renders without any narrative context. This step is mandatory for all quantitative reviews.

Write `commentary.json` to `$REVIEW_DIR`. Use the review findings to write specific, actionable narrative for each lens. Reference actual numbers from the review (runway months, metric values, scenario outcomes). Do not use generic advice.

**Required structure** (see `references/artifact-schemas.md` for full schema):

```json
{
  "headline": "One-sentence financial health summary",
  "lenses": { ... per-lens commentary ... }
}
```

The `headline` field is required — `explore.py` skips commentary entirely if it's missing.

Only write commentary for lenses whose required artifacts exist. Omit keys for disabled lenses (e.g., if runway.json is missing, omit "runway" and "raise_planner" keys from lenses). Do not reference grant details (iia_pending, royalty_rate, iia_royalties_modeled) that the explorer cannot model.

The investor_talking_points should be sentences the founder can literally say out loud during a fundraise conversation. Frame strengths confidently, frame gaps as "here's our plan to address X."

Every sentence must contain at least one number from this company's review.

### Step 8c: Generate Interactive Explorer (Quantitative Path Only)

```bash
python3 "$SCRIPTS/explore.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/explore.html"
```

Generate the file silently — it will be presented after Gate 2 passes.

### Verification Gate 2 (final)

```bash
python3 "$SCRIPTS/verify_review.py" --dir "$REVIEW_DIR" --pretty
```

**This is the final quality gate.** If it exits non-zero, fix the issues before presenting anything to the founder. Once it passes, present everything to the founder:

1. Display the full report markdown from `$REVIEW_DIR/report.md`
2. Present the `report.html` file path
3. Present the `explore.html` file path
4. Add coaching commentary: (1) what metrics look strong and why investors will notice, (2) the single highest-leverage fix to improve investor readiness, (3) any data gaps that weaken the story, (4) what to prioritize before the next fundraise conversation

## Scoring

- Each of 46 items: pass / fail / warn / not_applicable
- `score_pct` = (pass + 0.5 * warn) / (total - not_applicable) * 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)
