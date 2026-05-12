---
name: deck-review
description: "Scores and strengthens startup pitch decks (pre-seed through Series A) against 35 investor-grade criteria grounded in Sequoia, DocSend, YC, a16z, and Carta data."
when_to_use: >
  Use ONLY when the user has attached a pitch deck file (PDF, PPTX, markdown,
  or pasted slide text describing slide-by-slide content) AND has asked for
  review, scoring, feedback, or critique of the deck. Do not auto-invoke on
  general fundraising or pitch questions; use ONLY when there is actual
  deck content to review.
user-invocable: true
---

# Deck Review Skill

Help startup founders strengthen their pitch decks before sending them to investors. Produce a structured, scored review with specific, actionable recommendations grounded in current best practices from Sequoia, DocSend, YC, a16z, and Carta data. The tone is founder-first: a candid coaching session, not a VC evaluation.

## Skill Metadata

- **Author:** lool-ventures
- **Version:** managed in `founder-skills/.claude-plugin/plugin.json`
- **Compatibility:** Python 3.10+ and `uv` for script execution.
- **Exports:**
  - `checklist.json` → `financial-model-review`, `ic-sim`, `fundraise-readiness`

## Skill Execution Model (READ FIRST)

This skill runs **inline in the main thread** (not as a sub-agent). The main thread has full tool access including Bash, and is responsible for orchestrating the full pipeline: running producer scripts, persisting artifacts, and dispatching the deck-review sub-agent at specific moments.

**Two dispatch contexts for the sub-agent:**

- **Context A — Per-step analytical dispatch (Mitigation 1):** Steps 4 and 5 dispatch the deck-review agent via the `Task` tool. The agent does deep analysis and returns structured JSON. The main thread captures the JSON and pipes it through the producer script (`slide_reviews.py` or `checklist.py`). The sub-agent does NOT write artifacts directly.
- **Context B — Post-compose coaching dispatch:** Step 7 dispatches the sub-agent after `compose_report.py` writes `report.md`. The sub-agent reads `report.md`, appends `## Coaching Commentary`, verifies all canonical artifacts on disk, and returns a structured success payload.

**Why this model:** In Cowork, sub-agents have a restricted tool allowlist (no Bash). By keeping orchestration in the main thread and dispatching sub-agents only for analytical or post-compose tasks that use only Read/Edit/Glob/Grep, the pipeline works correctly in both Claude Code (CLI) and Cowork.

**Tolerant JSON extraction protocol (Context A):** After dispatching the sub-agent, capture its final assistant message. The sub-agent should return raw JSON, but may wrap it in ` ```json ... ``` ` fences or add a prose preamble. Extract JSON tolerantly:

1. If the message is wrapped in a ` ```json ... ``` ` (or plain ` ``` ... ``` `) fence, strip the fence first.
2. Try to parse the stripped text directly as JSON.
3. If that fails, walk through the text looking for the first `{` character and try `json.JSONDecoder().raw_decode(text[i:])` — this is brace-aware and handles nested objects correctly (unlike regex, which truncates on the first `}`).
4. If extraction fails entirely, re-prompt the sub-agent with: "Your previous reply could not be parsed as JSON. Return ONLY the JSON object — no markdown fences, no prose preamble."

> See `founder-skills/references/skill-execution-model.md` for the full inline-skill execution model (3 dispatch contexts, Mitigation 1+2, producer contract, Cowork quirks, per-symptom triage).

## Input Formats

Accept any format: PDF, PowerPoint (PPTX), markdown, or text descriptions of slides.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/deck-review/scripts/`:

- **`checklist.py`** — Scores 35 criteria across 7 categories (pass/fail/warn/not_applicable)
- **`compose_report.py`** — Assembles artifacts into final report with cross-artifact validation; `--strict` exits 1 on high/medium warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`founder_context.py`** — Per-company context management (init/read/merge/validate)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/deck-review/scripts/<script>.py --pretty [args]`

## Available References

Read as needed from `${CLAUDE_PLUGIN_ROOT}/skills/deck-review/references/`:

- **`deck-best-practices.md`** — Full best practices: slide frameworks, stage-specific guidelines, design rules, AI-company requirements
- **`checklist-criteria.md`** — Definitions for all 35 criteria with pass/fail/warn thresholds
- **`artifact-schemas.md`** — JSON schemas for all artifacts

## Artifact Pipeline

Every review deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | founder context | `founder_context.py` read/init |
| 2 | `deck_inventory.json` | `deck_inventory.py` (agent provides JSON via stdin) |
| 3 | `stage_profile.json` | `stage_profile.py` (agent provides JSON via stdin) |
| 4 | `slide_reviews.json` | `slide_reviews.py` (agent provides JSON via stdin) |
| 5 | `checklist.json` | `checklist.py` |
| 6 | Report | `compose_report.py` (writes both `report.json` and `report.md`) |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For producer-script artifacts (Steps 2-4), the agent supplies JSON on stdin and the script schema-validates against `references/schemas/<artifact>.schema.json`. Never write artifacts directly via `Write` or `Edit` — always pipe through the producer script so `metadata.run_id` is injected and the schema is enforced.
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4–5), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/deck-review/scripts"
REFS="${CLAUDE_PLUGIN_ROOT}/skills/deck-review/references"
SHARED_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"
ARTIFACTS_ROOT="${ARTIFACTS_ROOT:-$(pwd)/artifacts}"
mkdir -p "$ARTIFACTS_ROOT"

# Preliminary RUN_ID — used by Step 1 (founder_context init) before slug-aware
# setup_run.py runs. Will be reused by setup_run via --run-id, OR overwritten
# by gate_state.json on re-invocation (see below).
RUN_ID="${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/deck-review/scripts/checklist.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

After Step 1 (when the slug is known) — call `setup_run.py` to resolve `REVIEW_DIR` and clean stale state in one atomic step. **Re-invocation special case:** if the caller's task prompt indicated this is a resume (it includes `REVIEW_DIR=...` and / or `RUN_ID=...`, or `$REVIEW_DIR/gate_state.json` already exists with a non-empty `answer`), rehydrate `RUN_ID` from `gate_state.json`'s `metadata.run_id` and skip the `--clean` flag:

```bash
# Resolve REVIEW_DIR (from prompt if provided, else derive)
if [ -z "$REVIEW_DIR" ]; then
  REVIEW_DIR="$ARTIFACTS_ROOT/deck-review-$SLUG"
fi
mkdir -p "$REVIEW_DIR"
mkdir -p "$REVIEW_DIR/.staging"   # for ad-hoc sub-agent JSON staging (v0.4.2)

IS_RESUMING=""
if [ -f "$REVIEW_DIR/gate_state.json" ]; then
  GATE_ANSWER="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("answer",""))' "$REVIEW_DIR/gate_state.json")"
  if [ -n "$GATE_ANSWER" ]; then
    IS_RESUMING=1
    RUN_ID="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("metadata",{}).get("run_id",""))' "$REVIEW_DIR/gate_state.json")"
  fi
fi

if [ -z "$IS_RESUMING" ]; then
  SETUP_JSON="$(python3 "$SCRIPTS/setup_run.py" \
    --artifacts-root "$ARTIFACTS_ROOT" \
    --slug "$SLUG" \
    --run-id "$RUN_ID" \
    --clean \
    --pretty)"
  REVIEW_DIR="$(echo "$SETUP_JSON" | python3 -c 'import json,sys;print(json.load(sys.stdin)["review_dir"])')"
  # RUN_ID stays the preliminary value passed via --run-id; setup_run echoes it back.
fi
```

Pass `RUN_ID` to every producer script via `--run-id`. Producer scripts inject it into `metadata.run_id` automatically. `compose_report.py` enforces that all required artifacts share the same `run_id` and emits a `MISSING_METADATA` (high) warning for any artifact without one. **The rehydration above is what keeps `run_id` stable across the gate** — without it, a fresh `RUN_ID` on re-invocation would mismatch the pre-gate artifacts and trip `STALE_ARTIFACT` in compose.

**On re-invocation (`$IS_RESUMING` is set):** skip Steps 2 and 3 if `deck_inventory.json` and `stage_profile.json` already exist with a matching `metadata.run_id`. They were preserved across `setup_run.py` because that path was skipped, so re-running them would just overwrite identical content.

### Step 1: Read or Create Founder Context

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" read --artifacts-root "$ARTIFACTS_ROOT" --pretty
```

**Exit 0 (found):** Use the company slug and pre-filled fields. Proceed to Step 2.

**Exit 1 (not found):** This is normal for a first run — do not treat it as an error. Use `AskUserQuestion` (NOT plain chat) to ask for company name, stage, sector, and geography. Provide at least 2 options. Then create:

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" init \
  --company-name "Acme Corp" --stage seed --sector "B2B SaaS" \
  --geography "US" --artifacts-root "$ARTIFACTS_ROOT" \
  --run-id "$RUN_ID"
```

**Exit 2 (multiple):** Present the list, ask which company, re-read with `--slug`.

### Step 2: Ingest Deck -> `deck_inventory.json`

**Ingestion pitfalls — common issues that degrade review quality:**

1. **PDF image-only slides:** Some PDFs embed slides as images with no extractable text. If Read returns blank or garbled content, note `input_quality: "image_only"` in `deck_inventory.json` and base the review on visual description + OCR-level best effort. Flag reduced confidence in coaching commentary.
2. **PPTX speaker notes vs. slide content:** Speaker notes often contain the real narrative; slide text is abbreviated. Extract both — notes go into `content_summary`, slide text into `headline`. Do not discard notes.
3. **Multi-file submissions:** Founder sends v1 + v2, or deck + appendix as separate files. Ask which is the primary deck before proceeding. Do not merge or review both simultaneously.
4. **Partial decks:** Deck has fewer than 5 slides or is clearly a subset. Proceed but set `confidence: "low"` in stage_profile and note the limitation. Missing-slides detection still runs normally.
5. **Wrong file type:** File named `.pdf` but is actually a Word doc or image. If Read fails, try alternate format before asking the founder for a re-upload.

Read the provided deck. For each slide, extract: headline, content summary, visuals description, word count estimate. Then write the inventory through the producer script:

```bash
cat <<'INVENTORY_EOF' | python3 "$SCRIPTS/deck_inventory.py" --run-id "$RUN_ID" -o "$REVIEW_DIR/deck_inventory.json" --pretty
{
  "company_name": "...",
  "review_date": "YYYY-MM-DD",
  "input_format": "pdf",
  "total_slides": 12,
  "claimed_stage": "...",
  "claimed_raise": "...",
  "slides": [
    {"number": 1, "headline": "...", "content_summary": "...", "visuals": "...", "word_count_estimate": 15}
  ]
}
INVENTORY_EOF
```

The script validates against `references/schemas/deck_inventory.schema.json` and injects `metadata.run_id`. **Never write `deck_inventory.json` directly via heredoc** — the schema-validation gate is what keeps the pipeline honest.

### Step 3: Detect Stage -> `stage_profile.json`

Determine pre-seed/seed/series-a from signals in the deck. Read `references/deck-best-practices.md` for stage-specific frameworks. Record: detected stage, confidence, evidence, whether AI company, expected slide framework, stage benchmarks.

**Stage signals:** Pre-seed: no revenue, LOIs/waitlist, prototype, <$2.5M ask. Seed: early ARR, paying customers, <$6M ask. Series A: $1M+ ARR, cohort data, repeatable GTM, $10M+ ask. Later-stage: set detected_stage to `"series_b"` or `"growth"` — use the Gate below. Do not ask outside the gate.

**AI company detection signals:** The company is AI-first if ANY of: (1) core product uses ML/AI for its primary value proposition, (2) inference or training costs appear in COGS or margins, (3) deck mentions foundation models, fine-tuning, or AI infrastructure as product components, (4) retention or engagement metrics reference AI-specific patterns (usage retention vs. seat retention). Set `is_ai_company: true` and record the evidence in `ai_evidence`. When in doubt, flag it — the gate will let the founder correct.

Then write the profile through the producer script:

```bash
cat <<'PROFILE_EOF' | python3 "$SCRIPTS/stage_profile.py" --run-id "$RUN_ID" -o "$REVIEW_DIR/stage_profile.json" --pretty
{
  "detected_stage": "seed",
  "confidence": "high",
  "evidence": ["Claims $2M ARR", "..."],
  "is_ai_company": false,
  "ai_evidence": "...",
  "expected_framework": ["..."],
  "stage_benchmarks": {"round_size_range": "...", "expected_traction": "...", "runway_expectation": "..."},
  "reference_file_read": ["deck-best-practices.md", "checklist-criteria.md", "artifact-schemas.md"]
}
PROFILE_EOF
```

### Gate: Confirm Stage and Scope

**Sub-agent execution model:** sub-agents in Cowork cannot reliably call `AskUserQuestion`. The gate uses a checkpoint-and-resume pattern — the sub-agent writes a `gate_state.json` to disk and emits a structured `needs_input` payload as its final message. The parent (main thread or invoking agent) calls `AskUserQuestion` *if available* — or otherwise asks the founder via plain text — then writes the answer back into `gate_state.json` via `gate_state.py answer`, then re-invokes this sub-agent. The sub-agent detects re-invocation by checking whether `gate_state.json` already has an `answer` field. (Round-1 of the Phase 5 experiment confirmed plain-text round-trip works correctly even without `AskUserQuestion`.)

**How to detect re-invocation:** if `$REVIEW_DIR/gate_state.json` already exists AND has a non-empty `answer` field, you were re-invoked. Skip the gate-emit and read the answer:

```bash
GATE_ANSWER=""
if [ -f "$REVIEW_DIR/gate_state.json" ]; then
  GATE_ANSWER="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("answer",""))' "$REVIEW_DIR/gate_state.json")"
fi
```

If `$GATE_ANSWER` is set and non-empty, jump to "After the gate" below.

**Otherwise, write `gate_state.json` via the producer script and emit a needs_input payload:**

```bash
cat <<'GATE_EOF' | python3 "$SCRIPTS/gate_state.py" emit --run-id "$RUN_ID" -o "$REVIEW_DIR/gate_state.json" --pretty
{
  "gate_id": "stage_confirmation",
  "question": "Does this stage detection look right?",
  "options": ["Looks right", "Different stage", "Not sure — proceed anyway"],
  "context_summary": "Detected stage: Seed (high confidence). Key evidence: $4.2M ARR, 3 paying enterprise customers, $5M raise ask. AI company: Yes — inference costs in COGS. Expected framework: Sequoia seed (12-15 slides). Slides in deck: 14."
}
GATE_EOF
```

The script schema-validates the body and injects `metadata.run_id`. **Never write `gate_state.json` directly via heredoc.**

Then return — as your final assistant message — a JSON object the parent agent can act on:

```json
{
  "needs_input": {
    "gate_state_path": "<absolute path to gate_state.json>",
    "question": "Does this stage detection look right?",
    "options": ["Looks right", "Different stage", "Not sure — proceed anyway"],
    "context_summary": "..."
  },
  "review_dir": "<REVIEW_DIR>",
  "run_id": "<RUN_ID>"
}
```

**For out-of-scope stages (series_b, growth):** use `gate_id: "out_of_scope_choice"`, question `"This looks out of scope. What should I do?"`, options `["Stop review", "Different stage", "Proceed anyway (best-effort)"]`.

**After the gate (when `gate_state.json` already has an `answer`):** read `$GATE_ANSWER` from the file and branch:

- `Looks right`: proceed to Step 4 with the detected stage.
- `Different stage`: emit a second gate (gate_id `stage_choice`) via `gate_state.py emit` to ask which stage. Treat this as a fresh gate — return a new `needs_input` payload and let the parent answer it the same way. When that one comes back answered, run `stage_profile.py --rebuild-stage <chosen>` and re-emit the original `stage_confirmation` gate to confirm.
- `Not sure — proceed anyway`: proceed with detected stage, set `confidence: "low"` via `stage_profile.py --rebuild-stage <detected>`.
- `Stop review` (out-of-scope): exit. Do not run later steps.
- `Proceed anyway (best-effort)`: rebuild profile with `--rebuild-stage series_a` and add a low-confidence note.

### Sub-agent JSON staging (v0.4.2)

When a sub-agent returns JSON too large for bash heredoc, write it to
`$REVIEW_DIR/.staging/<step>_input.json` first, then pipe via:

```bash
cat "$REVIEW_DIR/.staging/<step>_input.json" | python3 "$SCRIPTS/<producer>.py" ...
```

The `.staging/` directory is created at setup and removed at cleanup.
This avoids `Operation not permitted` errors that occur when writing to
`$OUTPUTS_ROOT/` (Cowork sandbox marks that read-only post-write).

### Step 4: Review Each Slide -> `slide_reviews.json` (Context A dispatch)

**Dispatch the deck-review sub-agent in Context A (SLIDE_REVIEWS).** Do not do the slide analysis yourself in the main thread — dispatch it via the `Task` tool so the analysis runs in an isolated context with the full deck text and stage profile.

**Dispatch prompt template:**

```
CONTEXT: SLIDE_REVIEWS
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the deck-review agent dispatched in Context A (SLIDE_REVIEWS). Read
the deck at <deck file path or attached content> and the stage profile at
<REVIEW_DIR>/stage_profile.json. Compare each slide against the stage-specific
framework and non-negotiable principles from
${CLAUDE_PLUGIN_ROOT}/skills/deck-review/references/deck-best-practices.md
and references/checklist-criteria.md.

For each slide: identify strengths, weaknesses, and specific recommendations.
Map to expected framework. Flag missing expected slides. Every critique must
cite a specific best-practice principle.

Return JSON only — exactly the shape expected by slide_reviews.py (no metadata
block; the producer script adds it):
{
  "reviews": [
    {"slide_number": 1, "maps_to": "...", "strengths": ["..."],
     "weaknesses": ["..."], "recommendations": ["..."],
     "best_practice_refs": ["..."]}
  ],
  "missing_slides": [
    {"expected_type": "...", "importance": "important", "recommendation": "..."}
  ],
  "overall_narrative_assessment": "..."
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol (see "Skill Execution Model" preamble) to obtain the structured JSON from the sub-agent's final message. Then pipe through the producer script:

```bash
cat <<'REVIEWS_EOF' | python3 "$SCRIPTS/slide_reviews.py" --run-id "$RUN_ID" -o "$REVIEW_DIR/slide_reviews.json" --pretty
<JSON extracted from sub-agent reply>
REVIEWS_EOF
```

### Step 5: Score Checklist -> `checklist.json` (Context A dispatch)

**Dispatch the deck-review sub-agent in Context A (CHECKLIST).** Dispatch via the `Task` tool.

**Dispatch prompt template:**

```
CONTEXT: CHECKLIST
REVIEW_DIR: <absolute path to REVIEW_DIR>
RUN_ID: <RUN_ID>

You are the deck-review agent dispatched in Context A (CHECKLIST). Evaluate all
35 criteria from ${CLAUDE_PLUGIN_ROOT}/skills/deck-review/references/checklist-criteria.md
using the deck content (read from deck file or from slide_reviews.json for
reference), the stage profile at <REVIEW_DIR>/stage_profile.json, and the
deck inventory at <REVIEW_DIR>/deck_inventory.json.

For non-AI companies (is_ai_company: false), mark the 4 AI criteria
(ai_retention_rebased, ai_cost_to_serve_shown, ai_defensibility_beyond_model,
ai_responsible_controls) as not_applicable.

Evidence quality rules:
- Every fail and warn MUST cite a specific best-practice principle or benchmark.
- Every pass MUST note what was checked.
- not_applicable items MUST include a reason.

Return JSON only — the items array without a summary (the producer script
computes the summary):
{"items": [{"id": "purpose_clear", "status": "pass", "evidence": "...", "notes": "..."}, ...all 35 items...]}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the structured JSON. Then pipe through the producer script:

```bash
cat <<'CHECKLIST_EOF' | python3 "$SCRIPTS/checklist.py" --run-id "$RUN_ID" --pretty -o "$REVIEW_DIR/checklist.json"
<JSON extracted from sub-agent reply>
CHECKLIST_EOF
```

### Step 6: Compose Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$REVIEW_DIR" --pretty \
  -o "$REVIEW_DIR/report.json" \
  --write-md "$REVIEW_DIR/report.md"
```

`compose_report.py` writes both `report.json` and `report.md` deterministically. **Do NOT** read `report_markdown` out of `report.json` and re-write it via heredoc — the agent's heredoc handling drifted in the original Cowork run and produced an unparseable `report.json`. Compose owns the file outputs.

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Post-write verification:** `compose_report.py` exits non-zero (code 2) if the declared output files don't exist or are empty after writing. If compose exits non-zero, stop and report the exact stderr — do not proceed to Step 7.

### Step 7: Post-Compose Coaching Commentary (Context B dispatch — POST_COMPOSE_COACHING)

**Dispatch the deck-review sub-agent in Context B.** Dispatch via the `Task` tool after `compose_report.py` has successfully written both `report.json` and `report.md`.

**Mitigation 2 protocol (v0.4.2):** the main thread reads the structured `coaching_payload` from `report.json` and inlines it into the dispatch prompt. The sub-agent does NOT Read full `report.md` — it consumes `coaching_payload` directly, performs Grep idempotency, Edits via the per-run uuid `insertion_marker`, and Grep-verifies all artifacts. See the deck-review agent body's "Context B — Post-compose coaching dispatch (POST_COMPOSE_COACHING)" section for the full procedure.

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

You are dispatched to add coaching commentary to a deck review.

The compose_report.py script has finished. The structured `coaching_payload`
from report.json is:

<paste $COACHING_PAYLOAD JSON here verbatim>

Follow your agent body's Context B procedure
(POST_COMPOSE_COACHING):

1. grep_idempotency_check — Grep "## Coaching Commentary" (output_mode:count)
   and Grep the EXACT coaching_payload.insertion_marker (output_mode:count)
   on coaching_payload.report_path. Apply the 6-state decision matrix.
2. Compose commentary from the inlined coaching_payload (failed_items,
   warned_items, summary, high_severity_warnings, stage, is_ai_company).
   Do NOT Read the full report.md.
3. edit_via_marker — single Edit on coaching_payload.report_path:
     old_string = coaching_payload.insertion_marker  (EXACT uuid string)
     new_string = "## Coaching Commentary\n\n<your commentary>"
4. self_verify_artifacts_via_grep_run_id — Grep run_id from each producer
   artifact, confirm all 4 match; bounded Read (limit:1) on report.json
   and report.md; re-Grep the marker (must be 0) and the
   "## Coaching Commentary" header (must be 1).
5. Return the success payload:
   {"status": "complete", "review_dir": "<path>", "report_path": "<path>",
    "score_pct": <number>, "overall_status": "<string>",
    "high_severity_warnings": [<list>]}
   OR if verification fails:
   {"status": "blocked", "reason": "<specific gap>"}

Stop after returning JSON. Do not narrate.
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the success/blocked payload. If `status == "blocked"`, stop and report the reason to the founder. If `status == "complete"`, present `report_path` to the founder.

### Step 8 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 9: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_Deck_Review.md`, `.html` (if generated), `.json` (optional).

```bash
rm -rf "$REVIEW_DIR/.staging" 2>/dev/null || true
```

## Gotchas

- **"Looks polished" bias:** A well-designed deck is not a strong deck. Score content, narrative, and evidence independently of visual quality. The checklist separates design (5 items) from content (8 items) for this reason.
- **Template / AI-generated copy:** If multiple slides use generic phrasing ("revolutionize," "disrupt," "world-class team") with no specifics, flag this in coaching commentary as a credibility risk — investors notice formulaic decks. This is not a checklist item but affects overall narrative assessment.
- **Benchmarks are medians, not gates:** A $3M seed round in a $1B TAM market is not automatically wrong — context matters. Use benchmarks from `deck-best-practices.md` as reference points, not hard pass/fail thresholds. The coaching commentary should explain deviations rather than penalize them.
- **Founder provided text, not a file:** When the founder describes slides in conversation rather than uploading a file, adapt: write `deck_inventory.json` from the conversation, set `input_format: "text"`, and note reduced confidence in visual/design assessments. Design category items become `not_applicable` unless the founder shares screenshots.
- **Cross-skill context:** If `founder_context.py` returned prior market-sizing or financial-model-review runs, mention relevant findings in coaching commentary (e.g., "Your market sizing calculated $X TAM — your deck claims $Y"). Do not hard-fail on discrepancies; flag them for the founder.

## Main-Thread Return

This skill runs inline in the main thread (not as a sub-agent). The final outcome the main thread delivers to the founder is:

- The path to `$REVIEW_DIR/report.md` — the primary deliverable.
- The structured success payload from the Context B sub-agent (Step 7): `{status, review_dir, report_path, score_pct, overall_status, high_severity_warnings}`.
- Optionally: the HTML report path from Step 8.

**Do NOT inline `report_markdown` in the assistant message.** The founder reads the file via the path. (Closes issue #13: ~25 KB of markdown was previously round-tripped through the parent context.)

## Scoring

- Each of 35 items: pass / fail / warn / not_applicable
- `score_pct` = pass / (total - not_applicable) x 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)
