---
name: competitive-positioning
disable-model-invocation: true
description: "Maps a startup's competitive landscape, scores moat strength across 6+ dimensions, and generates an investor-ready competition narrative with positioning map."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.3.0"
imports:
  - "deck-review:checklist.json (optional — competition slide claims for cross-validation)"
  - "market-sizing:sizing.json (optional — validate market claims in positioning)"
exports:
  - "landscape.json -> deck-review, fundraise-readiness"
  - "report.json -> ic-sim, fundraise-readiness, cross-document-consistency"
---

# Competitive Positioning Skill

Help startup founders see their competitive landscape clearly — who the real competitors are, where they're differentiated, how defensible that differentiation is, and how to present it to investors. Produce a competitive analysis with positioning maps, moat scorecards, and an investor-ready narrative. The tone is founder-first: a coaching tool for preparation, not a judgment.

## Input Formats

Accept any combination: pitch deck (PDF), competitive analysis document, text description of the product and market, prior deck-review or market-sizing artifacts, or conversational input. If a pitch deck is provided, extract competitor claims from the competition slide for validation.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/scripts/`:

- **`validate_landscape.py`** — Validates and normalizes competitor landscape; checks slug uniqueness, category distribution, research depth; emits warnings for quality issues
- **`score_moats.py`** — Validates per-company moat assessments, computes aggregates (moat_count, strongest_moat, overall_defensibility), produces cross-company comparison by moat dimension
- **`score_positioning.py`** — Scores positioning views with rank-based differentiation, detects vanity axes, passes through stress-test results
- **`checklist.py`** — Scores 25 criteria across 6 categories (pass/fail/warn/not_applicable) with mode-based gating by input_mode
- **`compose_report.py`** — Assembles report with cross-artifact validation; `--strict` exits 1 on high-severity warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)
- **`explore.py`** — Generates interactive HTML explorer with Chart.js scatter plot, view switching, bubble encoding controls, and company detail panels (not JSON)

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`founder_context.py`** — Per-company context management (init/read/merge/validate)
- **`find_artifact.py`** — Resolves artifact paths by skill name and filename (for cross-skill lookups)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/scripts/<script>.py --pretty [args]`

## Available References

Read each when first needed — do NOT load all upfront. At `${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/references/`:

- **`competitive-analysis-methodology.md`** — Read before Step 3. Axis selection, competitor categorization, stress-testing, investor expectations
- **`moat-definitions.md`** — Read before Step 5. Six canonical moat dimensions with scoring rubrics and stage-calibrated expectations
- **`checklist-criteria.md`** — Read before Step 6. All 25 checklist criteria with category definitions and mode-based gating rules
- **`artifact-schemas.md`** — Consult as needed when depositing agent-written artifacts

From `${CLAUDE_PLUGIN_ROOT}/references/` (shared): `stage-expectations.md`, `benchmarks.md`, `israel-guidance.md`

## Artifact Pipeline

Every analysis deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 2 | `product_profile.json` | Agent (main) |
| 3 | `landscape_draft.json` | Agent (main) |
| 4 | `landscape_enriched.json` | Research sub-agent (Task) or agent (sequential) |
| 4b | `landscape.json` | `validate_landscape.py` (from enriched) |
| 5 | `positioning.json` | Agent (main — views, moats, stress-tests) |
| 6a | `moat_scores.json` | `score_moats.py` |
| 6b | `positioning_scores.json` | `score_positioning.py` |
| 6c | `checklist.json` | `checklist.py` |
| 7 | `report.json` | `compose_report.py` reads all |
| 7d | `report.html` | `visualize.py` |
| 7e | `explore.html` | `explore.py` |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts, consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$ANALYSIS_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4-6), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

**Every Bash tool call runs in a fresh shell — variables do not persist.** Prefix every Bash call that uses these paths with the variable block below, or substitute absolute paths directly:

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/scripts"
REFS="${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/references"
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

The path setup handles both Claude Code (local filesystem) and Cowork (mounted sessions). In most cases, only the first branch (`./artifacts`) applies.

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: run `Glob` with pattern `**/founder-skills/skills/competitive-positioning/scripts/validate_landscape.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `./artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p ./artifacts` and proceed.

After Step 1 (when the slug is known):

```bash
ANALYSIS_DIR="$ARTIFACTS_ROOT/competitive-positioning-${SLUG}"
mkdir -p "$ANALYSIS_DIR"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Pass `RUN_ID` to all sub-agents. Every artifact must include `"metadata": {"run_id": "$RUN_ID"}`. `compose_report.py` checks run_id consistency — a mismatch triggers `STALE_ARTIFACT`.

If `ANALYSIS_DIR` already contains artifacts from a previous run, remove them before starting:

    rm -f "$ANALYSIS_DIR"/{product_profile,landscape_draft,landscape_enriched,landscape,positioning,moat_scores,positioning_scores,checklist,report}.json "$ANALYSIS_DIR/report.html" "$ANALYSIS_DIR/explore.html"

### Step 1: Read or Create Founder Context

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" read --artifacts-root "$ARTIFACTS_ROOT" --pretty
```

**Exit 0 (found):** Use the company slug and pre-filled fields. Proceed to Step 2.

**Exit 1 (not found):** This is normal for a first run — do not treat it as an error. Use `AskUserQuestion` (NOT plain chat) to ask for company name, stage, sector, and geography. Provide at least 2 options. Note in the report metadata that no cross-skill validation was performed. Then create:

```bash
python3 "$SHARED_SCRIPTS/founder_context.py" init \
  --company-name "Acme Corp" --stage seed --sector "B2B SaaS" \
  --geography "US" --artifacts-root "$ARTIFACTS_ROOT"
```

**Exit 2 (multiple):** Present the list, ask which company, re-read with `--slug`.

### Step 2: Build Product Profile -> `product_profile.json`

Extract from the founder's materials or conversation: company name, product description, target customers, value propositions, differentiation claims, stage, sector, business model, and input_mode (`"deck"`, `"conversation"`, or `"document"`).

**For deck mode:** Read ALL pages of the deck systematically — not just the competition slide. Problem, solution, traction, and team slides contain competitive claims and differentiation context that inform the analysis. If the deck has a competition slide with its own positioning axes, record them in `product_profile.json` under `deck_axes` for potential use as a secondary positioning view.

Write `product_profile.json` to `$ANALYSIS_DIR`. Consult `references/artifact-schemas.md` for the schema.

If materials are sparse, use `AskUserQuestion` to gather missing fields. At minimum: product description, target customers, and what the founder believes differentiates them.

### Step 3: Identify Competitors -> `landscape_draft.json`

**REQUIRED — read `$REFS/competitive-analysis-methodology.md` now.**

Identify 5-7 competitors across categories: 2-3 direct, 1-2 adjacent, 1 do-nothing, 0-1 emerging. For each competitor, record: name, slug, category, description, key differentiators, and why included.

Select 2-3 candidate positioning axis pairs with rationale for each. Follow the axis selection principles from the methodology reference — axes must differentiate, matter to the buyer, and be measurable.

If the founder's deck mentions competitors you are excluding from the formal landscape (e.g., too small, different market segment, or redundant with an included competitor), note them with reasons in `landscape_draft.json` under a `deck_competitors_excluded` field. These will be referenced in the report to maintain deck alignment and prevent the NARR_03 checklist item from failing without explanation.

Write `landscape_draft.json` to `$ANALYSIS_DIR`.

### Gate 1: Founder Validation of Competitor Set

**MANDATORY STOP — TWO SEPARATE STEPS. DO NOT COMBINE THEM.**

**Step A: Output a chat message** with the competitor list and candidate axes. Use a markdown table or formatted list. This is a normal assistant message — NOT an AskUserQuestion call. Example:

```
Here's the competitive landscape I've identified:

| # | Competitor | Category | Description |
|---|---|---|---|
| 1 | Acme Corp | Direct | Same product, same market |
| 2 | Status quo | Do-nothing | Manual process |
...

Proposed positioning axes:
- **X: Deployment Speed** — how fast to integrate
- **Y: Detection Accuracy** — false positive rate
```

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question. The question field is plain text — NO markdown, NO tables, NO bullet points, NO competitor names.

Question: `Does this competitor set look right?`
Options: `Looks good` / `Missing competitors` / `Remove some` / `Change axes`

**CRITICAL: The AskUserQuestion question must be ONE SHORT SENTENCE. Put ALL details in the chat message (Step A), not in the question.**

This two-step pattern (chat message then AskUserQuestion) is required because AskUserQuestion renders as plain text. Detailed content goes in the chat message; only the gate question goes in AskUserQuestion.

If founder requests changes, apply corrections and repeat Steps A+B.

Apply all corrections to `landscape_draft.json` before proceeding.

### Step 4: Research & Enrich Competitors -> `landscape_enriched.json` -> `landscape.json`

Spawn a `general-purpose` Task sub-agent to research and enrich each competitor. The sub-agent receives: `landscape_draft.json` path, `product_profile.json` path, `ANALYSIS_DIR`, `RUN_ID`, and available search tool names.

**Sub-agent instructions:**

**Phase A — Enrich existing competitors:** For each competitor in `landscape_draft.json`, use web search to find: pricing model, funding history, team size, target customers, strengths, weaknesses. Record `evidence_source` per field (`"researched"` or `"agent_estimate"`). Set `research_depth` per competitor — MUST be one of: `"full"` (web research completed), `"partial"` (added via suggested_additions), `"founder_provided"` (no web research). Do NOT use values like "high", "medium", "low".

**Phase B — Gap detection:** After enriching, check for missing competitor categories. Search for: "alternatives to [startup product]", "[sector] competitors", G2/Capterra comparisons. If new competitors are found that would strengthen the analysis, add them to `suggested_additions[]` with `merged: false`. **CRITICAL: Do NOT add discovered competitors to `competitors[]` — only add them to `suggested_additions[]`. The main agent handles merging after founder approval.**

**Output format:** `competitors[]` must contain ONLY the original competitors from `landscape_draft.json` — no additions. Discovered competitors go exclusively in `suggested_additions[]`. Write `landscape_enriched.json` to `$ANALYSIS_DIR` with this exact structure:

```json
{
  "competitors": [
    {
      "name": "...", "slug": "...", "category": "...",
      "description": "...", "key_differentiators": ["..."],
      "research_depth": "full",
      "evidence_source": {"pricing_model": "researched", "funding": "agent_estimate"},
      "sourced_fields_count": 5,
      "pricing_model": "...", "funding": "...", "team_size": "...",
      "target_customers": ["..."], "strengths": ["..."], "weaknesses": ["..."]
    }
  ],
  "suggested_additions": [
    {
      "name": "...", "slug": "...", "category": "...",
      "rationale": "...", "partial_profile": {}, "merged": false
    }
  ],
  "suggested_axes": [],
  "assessment_mode": "sub-agent",
  "research_depth": "full",
  "input_mode": "...",
  "metadata": {"run_id": "..."}
}
```

`research_depth` per competitor MUST be one of: `"full"`, `"partial"`, `"founder_provided"`. Do NOT use `"high"`, `"medium"`, `"low"`.

All slugs MUST be kebab-case (lowercase, hyphens only, no underscores). Example: `"manual-campaigns"` not `"manual_campaigns"`. The validator auto-converts underscores to hyphens but it's better to get it right.

**Before returning:** Run `ls "$ANALYSIS_DIR/landscape_enriched.json"` to verify the file was actually written. Report the file path from the `ls` output, not from memory.

Return to the main agent ONLY: (1) verified file path from `ls`, (2) count of competitors enriched, (3) research_depth per competitor, (4) any `suggested_additions` found, (5) suggested axis pairs if any.

**Graceful degradation:** If Task tool is unavailable, research sequentially in the main agent. If no search tools are available, enrich from agent knowledge and set `research_depth: "founder_provided"`.

**After the sub-agent returns:**

If `suggested_additions` exist, review them first. If all discoveries are clearly irrelevant (wrong market, integration partners not competitors, too small to matter), you may skip the mini-gate and mark all as `merged: false` with a note explaining why. Otherwise, present relevant discoveries to the founder (each entry has a `rationale` field — the sub-agent may also use `reason` as an alias, check both). Use `AskUserQuestion` to ask which to include. Merge approved additions into `competitors[]` (set `merged: true`), mark declined ones as `merged: false`.

**Validate and normalize:**

```bash
cat "$ANALYSIS_DIR/landscape_enriched.json" | python3 "$SCRIPTS/validate_landscape.py" --pretty -o "$ANALYSIS_DIR/landscape.json"
```

Fix any errors (exit 1) and re-run. Warnings are acceptable — address medium-severity ones in the report.

**Competitor set boundary:** Target 5-7 competitors. `validate_landscape.py` enforces minimum 3 and maximum 10. If the founder wants to add more during Gate 1, cap at 10 and explain why — deeper analysis of fewer competitors beats shallow analysis of many.

### Gate 2: Founder Validation of Positioning

**MANDATORY STOP — TWO SEPARATE STEPS, same pattern as Gate 1.**

**Step A: Output a chat message** with the positioning preview. Use a markdown table showing competitor positions on chosen axes and moat highlights.

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question. NO details in the question field.

Question: `Does this positioning look right?`
Options: `Proceed to scoring` / `Adjust positions` / `Change axes` / `Other changes`

This two-step pattern (chat message then AskUserQuestion) is required because AskUserQuestion renders as plain text. Detailed content goes in the chat message; only the gate question goes in AskUserQuestion.

If founder changes an axis (not just coordinates), re-assign ALL competitor coordinates on the new axis with fresh evidence. Apply all corrections before proceeding to Step 5.

### Step 5: Positioning & Moat Assessment -> `positioning.json`

**REQUIRED — read `$REFS/moat-definitions.md` now.**

Before writing `positioning.json`, read `landscape.json` to get the competitor list and use it to scaffold the JSON structure. Write each section (views, moat_assessments, differentiation_claims) separately to manage complexity. The competitor slugs from `landscape.json` plus `_startup` define the complete set of entities that must appear in views and moat_assessments.

Build the full positioning artifact:

**Views:** 1-2 positioning views (primary required, secondary optional). For each view, assign coordinates (0-100) for every competitor and `_startup`. Every point needs `x_evidence`, `y_evidence`, and provenance source fields. **When `input_mode` is `"deck"` and the deck has its own competition axes** (recorded in `product_profile.json` as `deck_axes`), create a secondary view using the deck's axes. This strengthens NARR_03 (deck alignment) and gives the founder a direct comparison between their existing narrative and the analytically recommended positioning.

**Moat assessments:** Score every slug in `landscape.json` (including `_startup`) across 6 canonical moat dimensions: `network_effects`, `data_advantages`, `switching_costs`, `regulatory_barriers`, `cost_structure`, `brand_reputation`. Each moat gets: status (`strong`/`moderate`/`weak`/`absent`/`not_applicable`), evidence (required even for `not_applicable`), evidence_source, and trajectory (`building`/`stable`/`eroding`).

**Differentiation stress-tests:** For each of the startup's `differentiation_claims` from `product_profile.json`, assess: verifiable (boolean), supporting/challenging evidence, investor challenge, and verdict (`holds`/`partially_holds`/`does_not_hold`).

**Accepted warnings:** If you intentionally omit a do-nothing alternative or accept a known limitation, add an `accepted_warnings` entry with the warning code, match pattern, and reason. Common expected warnings:
- `SHALLOW_COMPETITOR_PROFILE` for do-nothing/status-quo alternatives (they always have thin evidence because they're not real companies)
- `MOAT_WITHOUT_EVIDENCE` for do-nothing moats rated `absent` (expected — the status quo has no moats)

Write `positioning.json` to `$ANALYSIS_DIR`. Consult `references/artifact-schemas.md` for the full schema.

### Step 6: Script Scoring Phase (Parallel)

**ALL THREE scripts below are MANDATORY. Do NOT skip any of them. `compose_report.py` will emit HIGH-severity warnings for any missing scoring artifact, and `--strict` will fail. Run all three — they can run in parallel (three Bash calls in one message):**

**6a — Moat scores:**

```bash
cat "$ANALYSIS_DIR/positioning.json" | python3 "$SCRIPTS/score_moats.py" --pretty -o "$ANALYSIS_DIR/moat_scores.json"
```

**6b — Positioning scores:**

```bash
cat "$ANALYSIS_DIR/positioning.json" | python3 "$SCRIPTS/score_positioning.py" --pretty -o "$ANALYSIS_DIR/positioning_scores.json"
```

**6c — Checklist:**

**REQUIRED — read `$REFS/checklist-criteria.md` now.**

Assess all 25 checklist items with evidence from the analysis. Mode-based gating applies: when `input_mode` is `"conversation"`, research-dependent items auto-gate to `not_applicable`.

Write the checklist JSON to `$ANALYSIS_DIR/checklist_input.json` using the Write tool (which handles escaping safely — no shell interpretation of quotes, newlines, or special characters). Then pipe it to the script:

```bash
cat "$ANALYSIS_DIR/checklist_input.json" | python3 "$SCRIPTS/checklist.py" --pretty -o "$ANALYSIS_DIR/checklist.json"
```

The JSON must contain: `{"items": [...all 25 items...], "input_mode": "<deck|conversation|document>", "metadata": {"run_id": "<RUN_ID>"}}`. Use the actual `input_mode` determined in Step 2 and the `RUN_ID` from Step 0.

**Evidence is MANDATORY for every item:** Every `fail` and `warn` item MUST have a non-empty `evidence` string citing specific findings. Every `pass` item MUST have `evidence` noting what was checked. Empty evidence produces blank lines in the report.

Fix script errors (exit 1) and re-run. Script warnings are findings to present, not errors to fix.

### Step 7: Compose, Validate, and Visualize

**7a — Compose report JSON (two-pass pattern):**

**Pass 1 (discovery):** Run compose WITHOUT `--strict` and WITHOUT `accepted_warnings` in `positioning.json`:

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --pretty -o "$ANALYSIS_DIR/report.json"
```

Inspect the warnings in the output. Fix any high-severity warnings (missing artifacts, stale run_id) and re-run Pass 1.

**Pass 2 (with acceptances):** If any medium-severity warnings should be accepted (agent judgment based on context — e.g., `MISSING_DO_NOTHING` in a regulated market, `MOAT_WITHOUT_EVIDENCE` for a do-nothing alternative), add `accepted_warnings` to `positioning.json` with the warning code, match pattern, and reason. Then re-run with `--strict`:

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --strict --pretty -o "$ANALYSIS_DIR/report.json"
```

This two-pass approach avoids the ordering problem where `accepted_warnings` must reference warnings that have not yet been generated. Medium-severity warnings are review findings to present, not data errors to fix.

**7b — Cross-skill lookups:** Use `find_artifact.py` to locate prior deck-review and market-sizing artifacts. If deck-review found, cross-reference competition slide claims against the analysis. If market-sizing found, validate market scope consistency. Note findings for inclusion in coaching commentary.

**7c — Write report and coaching commentary:** Read `report_markdown` from the compose output JSON. Insert your `## Coaching Commentary` section immediately before the final `---` separator line (the footer). The coaching commentary is agent-written (not script-generated) and should include:
- 2-3 competitive strengths to lead with in investor meetings
- The single highest-leverage improvement to the competitive narrative
- What investors will push on and how to prepare
- Defensibility roadmap: which moats to build and in what order
- Cross-skill findings from step 7b (if any prior artifacts were found)

Write the combined output (report_markdown + coaching commentary) to `$ANALYSIS_DIR/report.md` and display it to the user in full. **Present the file path** so the user can access it directly.

**7d — Visualize (optional):**

```bash
python3 "$SCRIPTS/visualize.py" --dir "$ANALYSIS_DIR" -o "$ANALYSIS_DIR/report.html"
```

**Present the HTML file path** to the user.

**7e — Explorer (optional):**

```bash
python3 "$SCRIPTS/explore.py" --dir "$ANALYSIS_DIR" -o "$ANALYSIS_DIR/explore.html"
```

**Present the HTML file path** to the user.

### Step 8: Deliver Artifacts

Copy final deliverables to workspace root with clean names:

```bash
cp "$ANALYSIS_DIR/report.md" "./${COMPANY_NAME}_Competitive_Positioning.md"
cp "$ANALYSIS_DIR/report.html" "./${COMPANY_NAME}_Competitive_Positioning.html" 2>/dev/null
cp "$ANALYSIS_DIR/explore.html" "./${COMPANY_NAME}_Competitive_Explorer.html" 2>/dev/null
```

Where `COMPANY_NAME` is the company name with spaces replaced by underscores (e.g., "Acme Corp" -> "Acme_Corp"). Present the file paths to the user.

## Scoring

### Moat Scoring
- 6 canonical dimensions per company, each: `strong` / `moderate` / `weak` / `absent` / `not_applicable`
- Moat count = dimensions rated `strong` or `moderate`
- Overall defensibility: `high` (2+ strong), `moderate` (1 strong or 2+ moderate), `low` (all else)

### Positioning Scoring
- Distance-weighted differentiation: rank contributes 50% (where the startup ranks among competitors) + gap contributes 50% (how far ahead of the next-best competitor). This distinguishes "barely ahead" from "dramatically ahead" at the same rank.
- Vanity axis detection: >80% of competitors within 20% range on either axis
- Differentiation strength: `strong` (top quartile both axes), `moderate` (top quartile one axis), `weak` (middle of pack), `undifferentiated` (bottom half both axes)

### Checklist Scoring
- 25 items, each: pass / fail / warn / not_applicable
- `score_pct` = (pass + 0.5 * warn) / (total - not_applicable) * 100
- Overall: "strong" (>=85%), "solid" (>=70%), "needs_work" (>=50%), "major_revision" (<50%)

## Cross-Agent Integration

This skill imports artifacts from prior deck-review (competition slide claims) and market-sizing (market scope validation) analyses. Imported artifacts are recorded with dates. Imports older than 7 days are flagged as `STALE_IMPORT`.
