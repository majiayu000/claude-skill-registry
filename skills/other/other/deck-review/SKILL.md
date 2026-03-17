---
name: deck-review
disable-model-invocation: true
description: "Scores and strengthens startup pitch decks against 35 investor-grade criteria before founders send them to VCs. Use when user asks to 'review my deck', 'pitch deck feedback', 'check my slides', 'is my deck ready', 'review this pitch deck', 'deck critique', 'improve my pitch deck', 'what's wrong with my deck', 'pitch deck review', 'fundraising deck feedback', or provides a pitch deck (PDF, PPTX, markdown, or text) for evaluation. Covers pre-seed, seed, and Series A against 2026 best practices from Sequoia, DocSend, YC, a16z, and Carta data. Do NOT use for financial model review, market sizing, or general document editing."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.2.0"
exports:
  - "checklist.json -> financial-model-review, ic-sim, fundraise-readiness"
---

# Deck Review Skill

Help startup founders strengthen their pitch decks before sending them to investors. Produce a structured, scored review with specific, actionable recommendations grounded in 2026 best practices from Sequoia, DocSend, YC, a16z, and Carta data. The tone is founder-first: a candid coaching session, not a VC evaluation.

## Input Formats

Accept any format: PDF, PowerPoint (PPTX), markdown, or text descriptions of slides.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/deck-review/scripts/`:

- **`checklist.py`** — Scores 35 criteria across 7 categories (pass/fail/warn/not_applicable)
- **`compose_report.py`** — Assembles artifacts into final report with cross-artifact validation; `--strict` exits 1 on high/medium warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/deck-review/scripts/<script>.py --pretty [args]`

## Available References

Read as needed from `${CLAUDE_PLUGIN_ROOT}/skills/deck-review/references/`:

- **`deck-best-practices.md`** — Full 2026 best practices: slide frameworks, stage-specific guidelines, design rules, AI-company requirements
- **`checklist-criteria.md`** — Definitions for all 35 criteria with pass/fail/warn thresholds
- **`artifact-schemas.md`** — JSON schemas for all artifacts

## Artifact Pipeline

Every review deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | `deck_inventory.json` | Agent (heredoc) |
| 2 | `stage_profile.json` | Agent (heredoc) |
| 3 | `slide_reviews.json` | Agent (heredoc) |
| 4 | `checklist.json` | `checklist.py` |
| 5 | Report | `compose_report.py` |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (Steps 1-3), consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (3–4), share a one-sentence finding before moving on.

## Workflow

### Path Setup

```bash
SCRIPTS="$CLAUDE_PLUGIN_ROOT/skills/deck-review/scripts"
REFS="$CLAUDE_PLUGIN_ROOT/skills/deck-review/references"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/deck-review/scripts/checklist.py`, strip to get `SCRIPTS`, derive `REFS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

```bash
REVIEW_DIR="$ARTIFACTS_ROOT/deck-review-{company-slug}"
mkdir -p "$REVIEW_DIR"
```

### Step 1: Ingest Deck -> `deck_inventory.json`

Read the provided deck. For each slide, extract: headline, content summary, visuals description, word count estimate. Record metadata: company name, total slides, format, any claimed stage or raise amount.

### Step 2: Detect Stage -> `stage_profile.json`

Determine pre-seed/seed/series-a from signals in the deck. Read `references/deck-best-practices.md` for stage-specific frameworks. Record: detected stage, confidence, evidence, whether AI company, expected slide framework, stage benchmarks.

**Stage signals:** Pre-seed: no revenue, LOIs/waitlist, prototype, <$2.5M ask. Seed: early ARR, paying customers, <$6M ask. Series A: $1M+ ARR, cohort data, repeatable GTM, $10M+ ask. Later-stage: set detected_stage to `"series_b"` or `"growth"` — compose report flags this as out of calibrated scope. If ambiguous, ask the user.

### Step 3: Review Each Slide -> `slide_reviews.json`

Compare each slide against the stage-specific framework and non-negotiable principles. For each slide: identify strengths, weaknesses, and specific recommendations. Map to expected framework. Flag missing expected slides.

**Critical:** Every critique must cite a specific best-practice principle. No vague feedback.

### Step 4: Score Checklist -> `checklist.json`

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

**Evidence required:** Always provide `evidence` for `fail` and `warn` items.

### Step 5: Compose Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$REVIEW_DIR" --pretty -o "$REVIEW_DIR/report.json"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Primary deliverable:** Read `report_markdown` from the output JSON, write it to `$REVIEW_DIR/report.md`, and display it to the user in full. **Present the file path** so the user can access it directly. Then add coaching commentary.

### Step 6 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$REVIEW_DIR" -o "$REVIEW_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 7: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_Deck_Review.md`, `.html` (if generated), `.json` (optional).

## Scoring

- Each of 35 items: pass / fail / warn / not_applicable
- `score_pct` = pass / (total - not_applicable) x 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)
