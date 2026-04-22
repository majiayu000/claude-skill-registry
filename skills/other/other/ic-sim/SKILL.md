---
name: ic-sim
disable-model-invocation: true
description: "Simulates a realistic VC Investment Committee with three partner archetypes debating a startup's merits, concerns, and deal terms, scored across 28 dimensions."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.3.0"
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

Also available from `${CLAUDE_PLUGIN_ROOT}/scripts/` (shared):

- **`founder_context.py`** — Per-company context management (init/read/merge/validate)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/scripts/<script>.py --pretty [args]`

## Available References

Read each when first needed — do NOT load all upfront. At `${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references/`:

- **`partner-archetypes.md`** — Read before Step 4. Three canonical archetypes with focus areas, debate styles, red flags
- **`evaluation-criteria.md`** — Read before Step 6. 28 dimensions across 7 categories with stage-calibrated thresholds
- **`ic-dynamics.md`** — Read before Step 6d. How real VC ICs work: formats, decisions, what kills deals
- **`artifact-schemas.md`** — Consult as needed when depositing agent-written artifacts

## Artifact Pipeline

Every simulation deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | founder context | `founder_context.py` read/init |
| 2 | `startup_profile.json` | Sub-agent (Task) or agent (heredoc) |
| 3 | `prior_artifacts.json` | Sub-agent (Task) or agent (heredoc) |
| 4 | `fund_profile.json` | Agent (heredoc) then `fund_profile.py` validates |
| 5 | `conflict_check.json` | Agent (heredoc) then `detect_conflicts.py` validates |
| 6a-c | `partner_assessment_{role}.json` | Sub-agents (Task, parallel) |
| 6d | `discussion.json` | Main agent (composes from 6a-c + debate) |
| 7 | `score_dimensions.json` | `score_dimensions.py` |
| 8 | Report | `compose_report.py` reads all |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts, consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$SIM_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (5–7), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

```bash
SCRIPTS="$CLAUDE_PLUGIN_ROOT/skills/ic-sim/scripts"
REFS="$CLAUDE_PLUGIN_ROOT/skills/ic-sim/references"
SHARED_SCRIPTS="$CLAUDE_PLUGIN_ROOT/scripts"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/ic-sim/scripts/score_dimensions.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

After Step 1 (when the slug is known):

```bash
SIM_DIR="$ARTIFACTS_ROOT/ic-sim-${SLUG}"
mkdir -p "$SIM_DIR"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Pass `RUN_ID` to all sub-agents. Every artifact written to `$SIM_DIR` must include `"metadata": {"run_id": "$RUN_ID"}` at the top level. `compose_report.py` checks that all artifact run IDs match — a mismatch triggers a `STALE_ARTIFACT` high-severity warning, blocking under `--strict`.

If `SIM_DIR` already contains artifacts from a previous run, remove them before starting:

    rm -f "$SIM_DIR"/{startup_profile,prior_artifacts,fund_profile,conflict_check,discussion,score_dimensions,partner_assessment_visionary,partner_assessment_operator,partner_assessment_analyst,report}.json "$SIM_DIR"/report.{html,md}

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

### Mode Selection

Ask the user (or infer from context):

1. **Interactive** — Pause between partner positions for founder input
2. **Auto-pilot** — Run all sections without pausing
3. **Fund-specific** — Research a real fund first. Combines with either mode.

### Steps 2-3: Extract Startup Profile and Import Prior Artifacts

When files are provided, spawn a `general-purpose` Task sub-agent to read materials, extract startup profile, and import prior market-sizing/deck-review artifacts. The sub-agent deposits both `startup_profile.json` and `prior_artifacts.json` to `$SIM_DIR`.

If missing fields are flagged, ask the user and patch the artifact. When only text is provided, extract directly without a sub-agent.

**Graceful degradation:** If Task tool is unavailable, extract directly.

After the sub-agent returns, verify that `$SIM_DIR` contains `startup_profile.json` and `prior_artifacts.json`. If either is missing, the sub-agent failed — re-run it before proceeding to Mode Selection.

### Step 4: Build Fund Profile -> `fund_profile.json`

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

### Step 5: Check Portfolio Conflicts -> `conflict_check.json`

Review the fund's portfolio against the startup. Assess each company for: direct conflict, adjacent conflict, or customer overlap. Use consistent names between portfolio and conflicts. Duplicates are auto-deduplicated by (company, type) pair.

```bash
cat <<'CONFLICT_EOF' | python3 "$SCRIPTS/detect_conflicts.py" --pretty -o "$SIM_DIR/conflict_check.json"
{"portfolio_size": 15, "conflicts": [...]}
CONFLICT_EOF
```

### Step 6: Partner Assessments and Discussion

**Step 6a-6c: Parallel Sub-Agent Assessments**

**REQUIRED — read `$REFS/evaluation-criteria.md` now.**

Spawn 3 `general-purpose` Task sub-agents **in a single message** (parallel, no `isolation: "worktree"`). Each receives: archetype persona, startup_profile, fund_profile, conflict_check, prior_artifacts, and relevant evaluation criteria. Each independently produces `partner_assessment_{role}.json`. Instruct each sub-agent to return ONLY: (1) the file path written, (2) the verdict, and (3) a one-sentence rationale — do not echo the full assessment back.

**Graceful degradation:** If Task tool unavailable, generate sequentially with strict persona separation. Set `assessment_mode: "sequential"` and `"assessment_mode_intentional": true` in discussion.json.

After all three sub-agents return, verify that `$SIM_DIR` contains `partner_assessment_visionary.json`, `partner_assessment_operator.json`, and `partner_assessment_analyst.json`. If any are missing, re-run the failed sub-agent before proceeding to Step 6d.

**Step 6d: Orchestrate Discussion -> `discussion.json`**

**REQUIRED — read `$REFS/ic-dynamics.md` now.**

Read all 3 assessments. Generate debate: each partner presents, partners respond to each other, build toward consensus. In interactive mode, pause between positions.

**Verdict reconciliation:** Ensure each partner's verdict reflects their **final** position after debate, not their opening position. The compose report flags `UNANIMOUS_VERDICT_MISMATCH` when all partners contradict the consensus.

**Discussion-to-Score reconciliation:** Before scoring, re-read discussion conclusions. If a dimension was debated as a dealbreaker, ensure the score reflects that severity. Compose flags `CONSENSUS_SCORE_MISMATCH` when discussion verdict and score diverge.

### Step 7: Score Dimensions -> `score_dimensions.json`

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

### Step 8: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$SIM_DIR" --pretty -o "$SIM_DIR/report.json"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Primary deliverable:** Read `report_markdown` from the output JSON, write it to `$SIM_DIR/report.md`, and display it to the user in full. **Present the file path** so the user can access it directly. Then add coaching commentary.

### Step 9 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$SIM_DIR" -o "$SIM_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 10: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_IC_Simulation.md`, `.html` (if generated), `.json` (optional).

## Scoring

- 28 dimensions, each: `strong_conviction` / `moderate_conviction` / `concern` / `dealbreaker` / `not_applicable`
- Conviction score: `(strong*1.0 + moderate*0.5) / applicable * 100`
- Verdicts: `invest` (>=75%), `more_diligence` (>=50%), `pass` (<50%), `hard_pass` (any dealbreaker)
- One dealbreaker forces `hard_pass` regardless of score

## Cross-Agent Integration

This skill imports artifacts from prior market-sizing and deck-review analyses. Imported artifacts are recorded with dates. Imports older than 7 days are flagged as `STALE_IMPORT`.
