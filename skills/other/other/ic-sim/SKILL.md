---
name: ic-sim
disable-model-invocation: true
description: "Simulates a realistic VC Investment Committee discussion with three partner archetypes debating a startup's merits, concerns, and deal terms, scored across 28 dimensions. Use when user asks to 'simulate an IC', 'how would VCs discuss this', 'IC meeting simulation', 'investment committee practice', 'prepare for IC', 'VC partner discussion', 'what will investors debate', 'how would a fund evaluate this', 'IC prep', or provides startup materials for investment committee simulation. Do NOT use for pitch deck feedback (use deck-review), market sizing, or financial model analysis."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.2.0"
imports:
  - "market-sizing:sizing.json (recommended — fund alignment and market validation)"
  - "deck-review:checklist.json (recommended — deck quality assessment)"
exports:
  - "report.json -> fundraise-readiness, dd-readiness"
---

# IC Simulation Skill

Help startup founders prepare for the conversation that happens behind closed doors — the one where VC partners debate whether to invest. Produce a realistic IC simulation with three distinct partner perspectives, scored across 28 dimensions, with specific coaching on what to prepare. The tone is founder-first: a coaching tool for preparation, not a judgment.

## Input Formats

Accept any combination: pitch deck, financial model, data room contents, text descriptions, prior market-sizing or deck-review artifacts, or just a verbal description of the business.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/scripts/`:

- **`fund_profile.py`** — Validates fund profile structure (archetypes, check size, thesis, portfolio)
- **`detect_conflicts.py`** — Validates conflict assessments and computes summary stats
- **`score_dimensions.py`** — Scores 28 dimensions across 7 categories with conviction-based scoring
- **`compose_report.py`** — Assembles report with cross-artifact validation; `--strict` exits 1 on high/medium warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/scripts/<script>.py --pretty [args]`

## Available References

Read each when first needed — do NOT load all upfront. At `${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references/`:

- **`partner-archetypes.md`** — Read before Step 3. Three canonical archetypes with focus areas, debate styles, red flags
- **`evaluation-criteria.md`** — Read before Step 5. 28 dimensions across 7 categories with stage-calibrated thresholds
- **`ic-dynamics.md`** — Read before Step 5d. How real VC ICs work: formats, decisions, what kills deals
- **`artifact-schemas.md`** — Consult as needed when depositing agent-written artifacts

## Artifact Pipeline

Every simulation deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | `startup_profile.json` | Sub-agent (Task) or agent (heredoc) |
| 2 | `prior_artifacts.json` | Sub-agent (Task) or agent (heredoc) |
| 3 | `fund_profile.json` | Agent (heredoc) then `fund_profile.py` validates |
| 4 | `conflict_check.json` | Agent (heredoc) then `detect_conflicts.py` validates |
| 5a-c | `partner_assessment_{role}.json` | Sub-agents (Task, parallel) |
| 5d | `discussion.json` | Main agent (composes from 5a-c + debate) |
| 6 | `score_dimensions.json` | `score_dimensions.py` |
| 7 | Report | `compose_report.py` reads all |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts, consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$SIM_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4–6), share a one-sentence finding before moving on.

## Workflow

### Path Setup

```bash
SCRIPTS="$CLAUDE_PLUGIN_ROOT/skills/ic-sim/scripts"
REFS="$CLAUDE_PLUGIN_ROOT/skills/ic-sim/references"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/ic-sim/scripts/score_dimensions.py`, strip to get `SCRIPTS`, derive `REFS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

```bash
SIM_DIR="$ARTIFACTS_ROOT/ic-sim-{company-slug}"
mkdir -p "$SIM_DIR"
```

### Mode Selection

Ask the user (or infer from context):

1. **Interactive** — Pause between partner positions for founder input
2. **Auto-pilot** — Run all sections without pausing
3. **Fund-specific** — Research a real fund first. Combines with either mode.

### Steps 1-2: Extract Startup Profile and Import Prior Artifacts

When files are provided, spawn a `general-purpose` Task sub-agent to read materials, extract startup profile, and import prior market-sizing/deck-review artifacts. The sub-agent deposits both `startup_profile.json` and `prior_artifacts.json` to `$SIM_DIR`.

If missing fields are flagged, ask the user and patch the artifact. When only text is provided, extract directly without a sub-agent.

**Graceful degradation:** If Task tool is unavailable, extract directly.

### Step 3: Build Fund Profile -> `fund_profile.json`

**REQUIRED — read `$REFS/partner-archetypes.md` now.**

**Generic mode:** Build a standard early-stage fund profile with the three canonical archetypes.

**Fund-specific mode:** Use WebSearch to research fund thesis, portfolio, partner backgrounds, check size range, and stage preference. Map real partners to archetype roles.

**Validation constraints:** `check_size_range` must be a dict (not a string), `stage_focus` must be a non-empty array, each source must have `url` or `title`.

```bash
cat <<'FUND_EOF' | python3 "$SCRIPTS/fund_profile.py" --pretty -o "$SIM_DIR/fund_profile.json"
{...fund profile JSON...}
FUND_EOF
```

**Accepted warnings:** Add `accepted_warnings` array with `code`, `match` (case-insensitive), and `reason`. Compose downgrades matching warnings to `"acknowledged"`.

### Step 4: Check Portfolio Conflicts -> `conflict_check.json`

Review the fund's portfolio against the startup. Assess each company for: direct conflict, adjacent conflict, or customer overlap. Use consistent names between portfolio and conflicts. Duplicates are auto-deduplicated by (company, type) pair.

```bash
cat <<'CONFLICT_EOF' | python3 "$SCRIPTS/detect_conflicts.py" --pretty -o "$SIM_DIR/conflict_check.json"
{"portfolio_size": 15, "conflicts": [...]}
CONFLICT_EOF
```

### Step 5: Partner Assessments and Discussion

**Step 5a-5c: Parallel Sub-Agent Assessments**

**REQUIRED — read `$REFS/evaluation-criteria.md` now.**

Spawn 3 `general-purpose` Task sub-agents **in a single message** (parallel, no `isolation: "worktree"`). Each receives: archetype persona, startup_profile, fund_profile, conflict_check, prior_artifacts, and relevant evaluation criteria. Each independently produces `partner_assessment_{role}.json`. Instruct each sub-agent to return ONLY: (1) the file path written, (2) the verdict, and (3) a one-sentence rationale — do not echo the full assessment back.

**Graceful degradation:** If Task tool unavailable, generate sequentially with strict persona separation. Set `assessment_mode: "sequential"` and `"assessment_mode_intentional": true` in discussion.json.

**Step 5d: Orchestrate Discussion -> `discussion.json`**

**REQUIRED — read `$REFS/ic-dynamics.md` now.**

Read all 3 assessments. Generate debate: each partner presents, partners respond to each other, build toward consensus. In interactive mode, pause between positions.

**Verdict reconciliation:** Ensure each partner's verdict reflects their **final** position after debate, not their opening position. The compose report flags `UNANIMOUS_VERDICT_MISMATCH` when all partners contradict the consensus.

**Discussion-to-Score reconciliation:** Before scoring, re-read discussion conclusions. If a dimension was debated as a dealbreaker, ensure the score reflects that severity. Compose flags `CONSENSUS_SCORE_MISMATCH` when discussion verdict and score diverge.

### Step 6: Score Dimensions -> `score_dimensions.json`

```bash
cat <<'SCORE_EOF' | python3 "$SCRIPTS/score_dimensions.py" --pretty -o "$SIM_DIR/score_dimensions.json"
{
  "items": [
    {"id": "team_founder_market_fit", "category": "Team", "status": "strong_conviction", "evidence": "...", "notes": "..."},
    ...all 28 items...
  ]
}
SCORE_EOF
```

### Step 7: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$SIM_DIR" --pretty -o "$SIM_DIR/report.json"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Primary deliverable:** Read `report_markdown` from the output JSON, write it to `$SIM_DIR/report.md`, and display it to the user in full. **Present the file path** so the user can access it directly. Then add coaching commentary.

### Step 8 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$SIM_DIR" -o "$SIM_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 9: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_IC_Simulation.md`, `.html` (if generated), `.json` (optional).

## Scoring

- 28 dimensions, each: `strong_conviction` / `moderate_conviction` / `concern` / `dealbreaker` / `not_applicable`
- Conviction score: `(strong*1.0 + moderate*0.5) / applicable * 100`
- Verdicts: `invest` (>=75%), `more_diligence` (>=50%), `pass` (<50%), `hard_pass` (any dealbreaker)
- One dealbreaker forces `hard_pass` regardless of score

## Cross-Agent Integration

This skill imports artifacts from prior market-sizing and deck-review analyses. Imported artifacts are recorded with dates. Imports older than 7 days are flagged as `STALE_IMPORT`.
