---
name: competitive-positioning
description: "Maps a startup's competitive landscape, scores moat strength across 6+ dimensions, and generates an investor-ready competition narrative with positioning map."
when_to_use: >
  Use ONLY when the user has asked for competitive landscape mapping,
  moat analysis, or positioning evaluation AND has provided enough
  context (a deck, a list of competitors, or a clearly named startup).
  Do not auto-invoke on general questions about competition or strategy.
user-invocable: true
---

# Competitive Positioning Skill

Help startup founders see their competitive landscape clearly — who the real competitors are, where they're differentiated, how defensible that differentiation is, and how to present it to investors. Produce a competitive analysis with positioning maps, moat scorecards, and an investor-ready narrative. The tone is founder-first: a coaching tool for preparation, not a judgment.

## Skill Metadata

- **Author:** lool-ventures
- **Version:** managed in `founder-skills/.claude-plugin/plugin.json`
- **Compatibility:** Python 3.10+ and `uv` for script execution.
- **Imports (optional):**
  - `deck-review:checklist.json` — competition slide claims for cross-validation
  - `market-sizing:sizing.json` — validate market claims in positioning
- **Exports:**
  - `landscape.json` → `deck-review`, `fundraise-readiness`
  - `report.json` → `ic-sim`, `fundraise-readiness`, `cross-document-consistency`

## Skill Execution Model (READ FIRST)

This skill runs **inline in the main thread** (not as a sub-agent). The main thread has full tool access including Bash, and is responsible for orchestrating the full pipeline: running producer scripts, persisting artifacts, and dispatching the competitive-positioning sub-agent at specific moments.

**Two dispatch contexts for the sub-agent:**

- **Context A — Per-step analytical dispatch (Mitigation 1):** Steps 4 (LANDSCAPE_RESEARCH), 5 (MOAT_SCORING + POSITIONING_SCORING), and 6 (CHECKLIST) dispatch the competitive-positioning agent via the `Task` tool. The agent does deep analysis and returns structured JSON. The main thread captures the JSON and pipes it through the producer script (`validate_landscape.py`, `score_moats.py`, `score_positioning.py`, or `checklist.py`). The sub-agent does NOT write artifacts directly.
- **Context B — Post-compose coaching dispatch:** Step 7 dispatches the sub-agent after `compose_report.py` writes `report.md`. The sub-agent reads `report.md`, appends `## Coaching Commentary`, verifies all canonical artifacts on disk, and returns a structured success payload.

**Why this model:** In Cowork, sub-agents have a restricted tool allowlist (no Bash). By keeping orchestration in the main thread and dispatching sub-agents only for analytical or post-compose tasks that use only Read/Edit/Glob/Grep, the pipeline works correctly in both Claude Code (CLI) and Cowork.

**Tolerant JSON extraction protocol (Context A):** After dispatching the sub-agent, capture its final assistant message. The sub-agent should return raw JSON, but may wrap it in ` ```json ... ``` ` fences or add a prose preamble. Extract JSON tolerantly:

1. If the message is wrapped in a ` ```json ... ``` ` (or plain ` ``` ... ``` `) fence, strip the fence first.
2. Try to parse the stripped text directly as JSON.
3. If that fails, walk through the text looking for the first `{` character and try `json.JSONDecoder().raw_decode(text[i:])` — this is brace-aware and handles nested objects correctly (unlike regex, which truncates on the first `}`).
4. If extraction fails entirely, re-prompt the sub-agent with: "Your previous reply could not be parsed as JSON. Return ONLY the JSON object — no markdown fences, no prose preamble."

> See `founder-skills/references/skill-execution-model.md` for the full inline-skill execution model (3 dispatch contexts, Mitigation 1+2, producer contract, Cowork quirks, per-symptom triage).

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
| 4 | `landscape_enriched.json` | Context A dispatch: LANDSCAPE_RESEARCH |
| 4b | `landscape.json` | `validate_landscape.py` (from enriched) |
| 5a | `moat_scores.json` | Context A dispatch: MOAT_SCORING → `score_moats.py` |
| 5b | `positioning_scores.json` | Context A dispatch: POSITIONING_SCORING → `score_positioning.py` |
| 5c | `positioning.json` | Agent (main — views, moats, stress-tests) |
| 6 | `checklist.json` | Context A dispatch: CHECKLIST → `checklist.py` |
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
mkdir -p "$ANALYSIS_DIR/.staging"   # for ad-hoc sub-agent JSON staging (v0.4.2)
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

**Step A: Output a chat message** with the competitor list and candidate axes. Use a markdown table or formatted list. This is a normal assistant message — NOT an AskUserQuestion call.

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question. The question field is plain text — NO markdown, NO tables, NO bullet points, NO competitor names.

Question: `Does this competitor set look right?`
Options: `Looks good` / `Missing competitors` / `Remove some` / `Change axes`

**CRITICAL: The AskUserQuestion question must be ONE SHORT SENTENCE. Put ALL details in the chat message (Step A), not in the question.**

If founder requests changes, apply corrections and repeat Steps A+B.

Apply all corrections to `landscape_draft.json` before proceeding.

### Sub-agent JSON staging (v0.4.2)

When a sub-agent returns JSON too large for bash heredoc, write it to
`$ANALYSIS_DIR/.staging/<step>_input.json` first, then pipe via:

```bash
cat "$ANALYSIS_DIR/.staging/<step>_input.json" | python3 "$SCRIPTS/<producer>.py" ...
```

The `.staging/` directory is created at setup and removed at cleanup.
This avoids `Operation not permitted` errors that occur when writing to
`$OUTPUTS_ROOT/` (Cowork sandbox marks that read-only post-write).

### Step 4: Research & Enrich Competitors -> `landscape_enriched.json` -> `landscape.json` (Context A: LANDSCAPE_RESEARCH dispatch)

**Dispatch the competitive-positioning sub-agent in Context A (LANDSCAPE_RESEARCH).** The sub-agent declares `WebSearch` in its tool allowlist (v0.4.7+) and performs the research itself — dispatch it via the `Task` tool so the research runs in an isolated context.

**Dispatch prompt template:**

```
CONTEXT: LANDSCAPE_RESEARCH
ANALYSIS_DIR: <absolute path to ANALYSIS_DIR>
RUN_ID: <RUN_ID>

You are the competitive-positioning agent dispatched in Context A (LANDSCAPE_RESEARCH).
Read landscape_draft.json at <ANALYSIS_DIR>/landscape_draft.json and
product_profile.json at <ANALYSIS_DIR>/product_profile.json.

Phase A — Enrich existing competitors: For each competitor in landscape_draft.json,
use WebSearch to find pricing model, funding history, team size, target customers,
strengths, weaknesses. Issue separate searches per competitor as needed. Record
evidence_source per field: "researched" only when the value came from a WebSearch
result; "agent_estimate" when you fell back to training-cutoff knowledge.
Set research_depth per competitor — MUST be one of: full, partial, or
founder_provided.

Phase B — Gap detection: After enriching, check for missing competitor categories.
Use WebSearch ("<product category> competitors", "<adjacent category> tools", etc.)
to discover competitors absent from the draft. Add them to suggested_additions[]
with merged: false. Do NOT add to competitors[] — only to suggested_additions[].

Return JSON only — exactly the shape expected by validate_landscape.py:
{
  "competitors": [...original competitors enriched, NOT new ones...],
  "suggested_additions": [...newly discovered...],
  "suggested_axes": [],
  "assessment_mode": "sub-agent",
  "research_depth": "full",
  "input_mode": "<from product_profile>",
  "metadata": {"run_id": "<RUN_ID>"}
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol (see "Skill Execution Model" preamble) to obtain the structured JSON. If `suggested_additions` exist, present them to the founder and ask which to include. Merge approved ones into `competitors[]`. Then pipe through the producer script:

```bash
cat <<'LANDSCAPE_EOF' | python3 "$SCRIPTS/validate_landscape.py" --pretty -o "$ANALYSIS_DIR/landscape.json"
<JSON extracted from sub-agent reply, with approved additions merged in>
LANDSCAPE_EOF
```

Fix any errors (exit 1) and re-run. Warnings are acceptable — address medium-severity ones in the report.

### Gate 2: Founder Validation of Positioning

**MANDATORY STOP — TWO SEPARATE STEPS, same pattern as Gate 1.**

**Step A: Output a chat message** with the positioning preview.

**Step B: AFTER the chat message, call `AskUserQuestion`** with ONLY a short question.

Question: `Does this positioning look right?`
Options: `Proceed to scoring` / `Adjust positions` / `Change axes` / `Other changes`

If founder changes an axis (not just coordinates), re-assign ALL competitor coordinates on the new axis with fresh evidence. Apply all corrections before proceeding to Step 5.

### Step 5: Positioning & Moat Assessment -> `positioning.json` + Dispatch Moat/Positioning Scoring (Context A)

**REQUIRED — read `$REFS/moat-definitions.md` now.**

Write `positioning.json` to `$ANALYSIS_DIR` (consult `references/artifact-schemas.md` for the schema). Then dispatch the sub-agent **twice in parallel** (two Task calls in one message) — once for MOAT_SCORING and once for POSITIONING_SCORING.

**MOAT_SCORING dispatch prompt:**

```
CONTEXT: MOAT_SCORING
ANALYSIS_DIR: <absolute path>
RUN_ID: <RUN_ID>

You are the competitive-positioning agent dispatched in Context A (MOAT_SCORING).
Read positioning.json at <ANALYSIS_DIR>/positioning.json and landscape.json at
<ANALYSIS_DIR>/landscape.json.

Score every slug (including _startup) across the 6 canonical moat dimensions from
${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/references/moat-definitions.md:
network_effects, data_advantages, switching_costs, regulatory_barriers,
cost_structure, brand_reputation.

Each moat: status (strong/moderate/weak/absent/not_applicable), evidence (required),
evidence_source (researched/agent_estimate/founder_override), trajectory
(building/stable/eroding).

For trajectory and any moat where landscape.json evidence is thin, use WebSearch
to find recent (last 12 months) signals — funding rounds, M&A, hiring, executive
changes, patent filings, product launches. Stamp evidence_source: "researched"
only when the signal came from a WebSearch result.

Return JSON only — exactly the shape expected by score_moats.py:
{
  "moat_assessments": {
    "_startup": {"moats": [...]},
    "<slug>": {"moats": [...]},
    ...
  },
  "metadata": {"run_id": "<RUN_ID>"}
}
```

**POSITIONING_SCORING dispatch prompt:**

```
CONTEXT: POSITIONING_SCORING
ANALYSIS_DIR: <absolute path>
RUN_ID: <RUN_ID>

You are the competitive-positioning agent dispatched in Context A (POSITIONING_SCORING).
Read positioning.json at <ANALYSIS_DIR>/positioning.json.

For each view in positioning.json, assign coordinates (0-100) for every competitor
and _startup on both axes. Every point needs x_evidence, y_evidence, and provenance.
Assess differentiation claims: verifiable (boolean), evidence, challenge, verdict
(holds/partially_holds/does_not_hold).

The axes themselves drive the search queries — when an axis is "customer support
depth" or "pricing transparency," issue WebSearch queries targeting that specific
dimension per competitor. Stamp x_evidence_source / y_evidence_source as
"researched" only when the coordinate came from a WebSearch result. For each
differentiation_claim, use WebSearch to find supporting or contradicting evidence
before assigning a verdict.

Return JSON only — exactly the shape expected by score_positioning.py:
{
  "views": [
    {
      "id": "...", "x_axis": {"name": "..."}, "y_axis": {"name": "..."},
      "x_axis_rationale": "...", "y_axis_rationale": "...",
      "points": [
        {"competitor": "...", "x": 0-100, "y": 0-100,
         "x_evidence": "...", "y_evidence": "...",
         "x_evidence_source": "researched|agent_estimate",
         "y_evidence_source": "researched|agent_estimate"}
      ]
    }
  ],
  "differentiation_claims": [...],
  "metadata": {"run_id": "<RUN_ID>"}
}
```

**After both sub-agents return:** apply the tolerant JSON extraction protocol to each. Pipe MOAT_SCORING output through `score_moats.py` and POSITIONING_SCORING output through `score_positioning.py`:

```bash
cat <<'MOAT_EOF' | python3 "$SCRIPTS/score_moats.py" --pretty -o "$ANALYSIS_DIR/moat_scores.json"
<JSON extracted from MOAT_SCORING sub-agent reply>
MOAT_EOF
```

```bash
cat <<'POS_EOF' | python3 "$SCRIPTS/score_positioning.py" --pretty -o "$ANALYSIS_DIR/positioning_scores.json"
<JSON extracted from POSITIONING_SCORING sub-agent reply>
POS_EOF
```

### Step 6: Score Checklist -> `checklist.json` (Context A: CHECKLIST dispatch)

**REQUIRED — read `$REFS/checklist-criteria.md` now.**

**Dispatch the competitive-positioning sub-agent in Context A (CHECKLIST).** Dispatch via the `Task` tool.

**Dispatch prompt template:**

```
CONTEXT: CHECKLIST
ANALYSIS_DIR: <absolute path>
RUN_ID: <RUN_ID>

You are the competitive-positioning agent dispatched in Context A (CHECKLIST).
Read landscape.json, positioning.json, moat_scores.json, and positioning_scores.json
from <ANALYSIS_DIR>. Also read
${CLAUDE_PLUGIN_ROOT}/skills/competitive-positioning/references/checklist-criteria.md.

Assess all 25 checklist items (COVER_01..05, POS_01..05, MOAT_01..04,
EVID_01..04, NARR_01..04, MISS_01..03). Mode-based gating applies: when
input_mode is conversation, research-dependent items auto-gate to not_applicable.

Evidence is MANDATORY for every item: every fail and warn MUST have a non-empty
evidence string citing specific findings. Every pass MUST have evidence noting
what was checked.

Return JSON only — the items array without a summary (the producer script
computes the summary):
{"items": [{"id": "COVER_01", "status": "pass", "evidence": "...", "notes": "..."}, ...all 25 items...]}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the structured JSON. Then pipe through the producer script:

```bash
cat <<'CHECKLIST_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$ANALYSIS_DIR/checklist.json"
<JSON extracted from sub-agent reply>
CHECKLIST_EOF
```

### Step 7: Compose, Validate, and Post-Compose Coaching

**7a — Compose report JSON (two-pass pattern):**

**Pass 1 (discovery):** Run compose WITHOUT `--strict` and WITHOUT `accepted_warnings` in `positioning.json`:

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --pretty \
  -o "$ANALYSIS_DIR/report.json" \
  --write-md "$ANALYSIS_DIR/report.md"
```

`compose_report.py` writes both `report.json` and `report.md` deterministically. **Do NOT** read `report_markdown` out of `report.json` and re-write it via heredoc.

Inspect the warnings in the output. Fix any high-severity warnings (missing artifacts, stale run_id) and re-run Pass 1.

**Pass 2 (with acceptances):** If any medium-severity warnings should be accepted, add `accepted_warnings` to `positioning.json` with the warning code, match pattern, and reason. Then re-run with `--strict`:

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --strict --pretty \
  -o "$ANALYSIS_DIR/report.json" \
  --write-md "$ANALYSIS_DIR/report.md"
```

**Post-write verification:** `compose_report.py` exits non-zero (code 2) if the declared output files don't exist or are empty after writing. If compose exits non-zero, stop and report the exact stderr — do not proceed.

**7b — Cross-skill lookups:** Use `find_artifact.py` to locate prior deck-review and market-sizing artifacts. If found, note findings for inclusion in coaching commentary.

**7c — Post-Compose Coaching Commentary (Context B dispatch — POST_COMPOSE_COACHING):**

**Dispatch the competitive-positioning sub-agent in Context B.** Dispatch via the `Task` tool after `compose_report.py` has successfully written both `report.json` and `report.md`.

**Mitigation 2 protocol (v0.4.2):** the main thread reads the structured `coaching_payload` from `report.json` and inlines it into the dispatch prompt. The sub-agent does NOT Read full `report.md` — it consumes `coaching_payload` directly, performs Grep idempotency, Edits via the per-run uuid `insertion_marker`, and Grep-verifies all artifacts. See the competitive-positioning agent body's "Context B — Post-compose coaching dispatch (POST_COMPOSE_COACHING)" section for the full procedure.

<!-- skill-quality-ci: bash-after-subagent-ok -->
```bash
COACHING_PAYLOAD="$(python3 -c '
import json, sys
data = json.load(open(sys.argv[1]))
print(json.dumps(data["coaching_payload"], indent=2))
' "$ANALYSIS_DIR/report.json")"
```

**Dispatch prompt template:**

```
CONTEXT: POST_COMPOSE_COACHING

You are dispatched to add coaching commentary to a competitive positioning review.

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
   Do NOT Read the full report.md.
3. edit_via_marker — single Edit on coaching_payload.report_path:
     old_string = coaching_payload.insertion_marker  (EXACT uuid string)
     new_string = "## Coaching Commentary\n\n<your commentary>"
4. self_verify_artifacts_via_grep_run_id — Grep run_id from each producer
   artifact (landscape.json, positioning.json, moat_scores.json,
   positioning_scores.json, checklist.json), confirm all 5 match;
   bounded Read (limit:1) on report.json and report.md; re-Grep the marker
   (must be 0) and the "## Coaching Commentary" header (must be 1).
5. Return the success payload:
   {"status": "complete", "review_dir": "<path>", "report_path": "<path>",
    "landscape_summary": "<one-liner>", "top_moats": [<list>],
    "high_severity_warnings": [<list>]}
   OR if verification fails:
   {"status": "blocked", "reason": "<specific gap>"}

Stop after returning JSON. Do not narrate.
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the success/blocked payload. If `status == "blocked"`, stop and report the reason. If `status == "complete"`, present `report_path` to the founder.

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
rm -rf "$ANALYSIS_DIR/.staging" 2>/dev/null || true
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

## Main-Thread Return

This skill runs inline in the main thread (not as a sub-agent). The final outcome the main thread delivers to the founder is:

- The path to `$ANALYSIS_DIR/report.md` — the primary deliverable.
- The structured success payload from the Context B sub-agent (Step 7c): `{status, review_dir, report_path, landscape_summary, top_moats, high_severity_warnings}`.
- Optionally: the HTML report paths from Steps 7d and 7e.

**Do NOT inline `report_markdown` in the assistant message.** The founder reads the file via the path.
