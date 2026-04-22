---
name: deck-review
disable-model-invocation: true
description: "Scores and strengthens startup pitch decks (pre-seed through Series A) against 35 investor-grade criteria grounded in Sequoia, DocSend, YC, a16z, and Carta data."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.3.0"
exports:
  - "checklist.json -> financial-model-review, ic-sim, fundraise-readiness"
---

# Deck Review Skill

Help startup founders strengthen their pitch decks before sending them to investors. Produce a structured, scored review with specific, actionable recommendations grounded in current best practices from Sequoia, DocSend, YC, a16z, and Carta data. The tone is founder-first: a candid coaching session, not a VC evaluation.

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
| 2 | `deck_inventory.json` | Agent (heredoc) |
| 3 | `stage_profile.json` | Agent (heredoc) |
| 4 | `slide_reviews.json` | Agent (heredoc) |
| 5 | `checklist.json` | `checklist.py` |
| 6 | Report | `compose_report.py` |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (Steps 2-4), consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4–5), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

```bash
SCRIPTS="$CLAUDE_PLUGIN_ROOT/skills/deck-review/scripts"
REFS="$CLAUDE_PLUGIN_ROOT/skills/deck-review/references"
SHARED_SCRIPTS="$CLAUDE_PLUGIN_ROOT/scripts"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/deck-review/scripts/checklist.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

After Step 1 (when the slug is known):

```bash
REVIEW_DIR="$ARTIFACTS_ROOT/deck-review-${SLUG}"
mkdir -p "$REVIEW_DIR"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Pass `RUN_ID` to all sub-agents. Every artifact written to `$REVIEW_DIR` must include `"metadata": {"run_id": "$RUN_ID"}` at the top level. `compose_report.py` checks that all artifact run IDs match — a mismatch triggers a `STALE_ARTIFACT` high-severity warning, blocking under `--strict`.

If `REVIEW_DIR` already contains artifacts from a previous run, remove them before starting:

    rm -f "$REVIEW_DIR"/{deck_inventory,stage_profile,slide_reviews,checklist,report}.json "$REVIEW_DIR"/report.{html,md}

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

### Step 2: Ingest Deck -> `deck_inventory.json`

**Ingestion pitfalls — common issues that degrade review quality:**

1. **PDF image-only slides:** Some PDFs embed slides as images with no extractable text. If Read returns blank or garbled content, note `input_quality: "image_only"` in `deck_inventory.json` and base the review on visual description + OCR-level best effort. Flag reduced confidence in coaching commentary.
2. **PPTX speaker notes vs. slide content:** Speaker notes often contain the real narrative; slide text is abbreviated. Extract both — notes go into `content_summary`, slide text into `headline`. Do not discard notes.
3. **Multi-file submissions:** Founder sends v1 + v2, or deck + appendix as separate files. Ask which is the primary deck before proceeding. Do not merge or review both simultaneously.
4. **Partial decks:** Deck has fewer than 5 slides or is clearly a subset. Proceed but set `confidence: "low"` in stage_profile and note the limitation. Missing-slides detection still runs normally.
5. **Wrong file type:** File named `.pdf` but is actually a Word doc or image. If Read fails, try alternate format before asking the founder for a re-upload.

Read the provided deck. For each slide, extract: headline, content summary, visuals description, word count estimate. Record metadata: company name, total slides, format, any claimed stage or raise amount.

### Step 3: Detect Stage -> `stage_profile.json`

Determine pre-seed/seed/series-a from signals in the deck. Read `references/deck-best-practices.md` for stage-specific frameworks. Record: detected stage, confidence, evidence, whether AI company, expected slide framework, stage benchmarks.

**Stage signals:** Pre-seed: no revenue, LOIs/waitlist, prototype, <$2.5M ask. Seed: early ARR, paying customers, <$6M ask. Series A: $1M+ ARR, cohort data, repeatable GTM, $10M+ ask. Later-stage: set detected_stage to `"series_b"` or `"growth"` — use the Gate below. Do not ask outside the gate.

**AI company detection signals:** The company is AI-first if ANY of: (1) core product uses ML/AI for its primary value proposition, (2) inference or training costs appear in COGS or margins, (3) deck mentions foundation models, fine-tuning, or AI infrastructure as product components, (4) retention or engagement metrics reference AI-specific patterns (usage retention vs. seat retention). Set `is_ai_company: true` and record the evidence in `ai_evidence`. When in doubt, flag it — the gate will let the founder correct.

### Gate: Confirm Stage and Scope

**MANDATORY STOP — TWO SEPARATE STEPS. DO NOT COMBINE THEM.**

**Step A: Output a chat message** with the stage detection results. Use a formatted summary. This is a normal assistant message — NOT an AskUserQuestion call. Example:

```
Based on the deck, here's what I'm seeing:

- **Detected stage:** Seed
- **Confidence:** High
- **Key evidence:** $4.2M ARR, 3 paying enterprise customers, $5M raise ask
- **AI company:** Yes — inference costs in COGS
- **Expected framework:** Sequoia seed (12-15 slides)
- **Slides in deck:** 14
```

**If `detected_stage` is `pre_seed`, `seed`, or `series_a`:**

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question. The question field is plain text — NO markdown, NO tables, NO bullet points.

Question: `Does this stage detection look right?`
Options: `Looks right` / `Different stage` / `Not sure — proceed anyway`

**If `detected_stage` is `"series_b"` or `"growth"`:** include a note in Step A: "This skill is calibrated only for pre-seed through Series A, so this deck is currently out of scope."

Then call `AskUserQuestion` with:
Question: `This looks out of scope for this skill. What should I do?`
Options: `Stop review` / `Different stage` / `Proceed anyway (best-effort)`

**CRITICAL: The AskUserQuestion question must be ONE SHORT SENTENCE. Put ALL details in the chat message (Step A), not in the question.**

This two-step pattern (chat message then AskUserQuestion) is required because AskUserQuestion renders as plain text. Detailed content goes in the chat message; only the gate question goes in AskUserQuestion.

**If the founder selects "Looks right":** Proceed to Step 4 (Review Each Slide) with the detected stage.

**If the founder selects "Different stage":** Ask which stage they want to use (pre-seed / seed / series-a / series-b / growth). Then rebuild `stage_profile.json` for the corrected stage (do not re-read the deck or re-detect signals — the deck evidence is unchanged): re-read `references/deck-best-practices.md` for the new stage's framework and benchmarks, rebuild the artifact, and repeat the gate.

For the rebuilt `stage_profile.json`:
- `detected_stage`: the founder's corrected value
- `confidence`: `"high"` (founder confirmed directly)
- `evidence`: include original detection signals plus `"Founder corrected stage from X to Y"`
- `is_ai_company`, `ai_evidence`: unchanged from original detection unless the founder also corrected those inputs
- `expected_framework`, `stage_benchmarks`: rebuild from `deck-best-practices.md` only if the corrected stage is `pre_seed`, `seed`, or `series_a`

**If the corrected stage is still `"series_b"` or `"growth"`:** stop after the gate. Do not continue to Step 4 or any later steps. Do **not** use Series A as a proxy for later-stage companies.

**If the founder selects "Stop review":** stop the skill here. Do not continue to Step 4 (Review Each Slide), Step 5 (Score Checklist), or report composition.

**If "Proceed anyway (best-effort)":** Use Series A criteria as the closest available proxy. Set `confidence: "low"` in `stage_profile.json` and add `"Founder chose best-effort review for out-of-scope stage"` to evidence. Include a prominent disclaimer in the final coaching commentary that scoring criteria are calibrated for pre-seed through Series A and may not reflect later-stage investor expectations.

**If "Not sure — proceed anyway":** Use the detected stage but note the uncertainty in `stage_profile.json` under `confidence: "low"`. Mention in the final coaching commentary that the founder should confirm their stage positioning.

### Step 4: Review Each Slide -> `slide_reviews.json`

Compare each slide against the stage-specific framework and non-negotiable principles. For each slide: identify strengths, weaknesses, and specific recommendations. Map to expected framework. Flag missing expected slides.

**Critical:** Every critique must cite a specific best-practice principle. No vague feedback.

### Step 5: Score Checklist -> `checklist.json`

Evaluate all 35 criteria from `references/checklist-criteria.md`. For non-AI companies, mark AI category items as `not_applicable`.

```bash
cat <<'CHECKLIST_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$REVIEW_DIR/checklist.json"
{
  "items": [
    {"id": "purpose_clear", "status": "pass", "evidence": "Sequoia: single declarative sentence", "notes": "Clear one-liner with quantified outcome"},
    ...all 35 items...
  ]
}
CHECKLIST_EOF
```

**Evidence quality rules:**
- Every `fail` and `warn` MUST cite a specific best-practice principle or benchmark (e.g., "Sequoia: single declarative sentence" or "DocSend: median 11 slides for seed").
- Every `pass` MUST note what was checked — not just "pass" with empty evidence.
- `not_applicable` items MUST include a reason (e.g., "Not an AI company — AI category gated").
- Empty `evidence` on any non-pass item = quality gate failure. Fix before running compose.

### Step 6: Compose Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$REVIEW_DIR" --pretty -o "$REVIEW_DIR/report.json"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Primary deliverable:** Read `report_markdown` from the output JSON, write it to `$REVIEW_DIR/report.md`, and display it to the user in full. **Present the file path** so the user can access it directly. Then add coaching commentary.

### Step 7 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 8: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_Deck_Review.md`, `.html` (if generated), `.json` (optional).

## Gotchas

- **"Looks polished" bias:** A well-designed deck is not a strong deck. Score content, narrative, and evidence independently of visual quality. The checklist separates design (5 items) from content (8 items) for this reason.
- **Template / AI-generated copy:** If multiple slides use generic phrasing ("revolutionize," "disrupt," "world-class team") with no specifics, flag this in coaching commentary as a credibility risk — investors notice formulaic decks. This is not a checklist item but affects overall narrative assessment.
- **Benchmarks are medians, not gates:** A $3M seed round in a $1B TAM market is not automatically wrong — context matters. Use benchmarks from `deck-best-practices.md` as reference points, not hard pass/fail thresholds. The coaching commentary should explain deviations rather than penalize them.
- **Founder provided text, not a file:** When the founder describes slides in conversation rather than uploading a file, adapt: write `deck_inventory.json` from the conversation, set `input_format: "text"`, and note reduced confidence in visual/design assessments. Design category items become `not_applicable` unless the founder shares screenshots.
- **Cross-skill context:** If `founder_context.py` returned prior market-sizing or financial-model-review runs, mention relevant findings in coaching commentary (e.g., "Your market sizing calculated $X TAM — your deck claims $Y"). Do not hard-fail on discrepancies; flag them for the founder.

## Scoring

- Each of 35 items: pass / fail / warn / not_applicable
- `score_pct` = pass / (total - not_applicable) x 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)
