---
name: ic-sim
description: "Simulates a realistic VC Investment Committee with three partner archetypes debating a startup's merits, concerns, and deal terms, scored across 28 dimensions."
when_to_use: >
  Use ONLY when the user has asked to simulate an IC discussion
  or to hear how partners would debate a specific startup, AND has
  provided enough context (a deck, a description of the company,
  or a specific fund). Do not auto-invoke on general fundraising
  questions.
user-invocable: true
---

# IC Simulation Skill

Help startup founders prepare for the conversation that happens behind closed doors — the one where VC partners debate whether to invest. Produce a realistic IC simulation with three distinct partner perspectives, scored across 28 dimensions, with specific coaching on what to prepare. The tone is founder-first: a coaching tool for preparation, not a judgment.

## Skill Metadata

- **Author:** lool-ventures
- **Version:** managed in `founder-skills/.claude-plugin/plugin.json`
- **Compatibility:** Python 3.10+ and `uv` for script execution.
- **Imports (recommended):**
  - `market-sizing:sizing.json` — fund alignment and market validation
  - `deck-review:checklist.json` — deck quality assessment
- **Exports:**
  - `report.json` → `fundraise-readiness`, `dd-readiness`

## Skill Execution Model (READ FIRST)

This skill runs **inline in the main thread** (not as a sub-agent). The main thread has full tool access including Bash, and is responsible for orchestrating the full pipeline: running producer scripts, persisting artifacts, and dispatching the ic-sim sub-agent at specific moments.

**Two dispatch contexts for the sub-agent:**

- **Context A — Per-step analytical dispatch (Mitigation 1):** Steps 4, 5, and 6 dispatch the ic-sim agent via the `Task` tool. The novel element here is **parallel dispatch**: Step 4 (PARTNER_ANALYSIS) dispatches the agent **three times simultaneously** — one per partner archetype — in a **single assistant turn**. Steps 5 and 6 (SCORE_DIMENSIONS and DETECT_CONFLICTS) are sequential dispatches. The sub-agent does deep analysis and returns structured JSON. The main thread captures the JSON and pipes it through the producer script. The sub-agent does NOT write artifacts directly.
- **Context B — Post-compose coaching dispatch:** The final step dispatches the sub-agent after `compose_report.py` writes `report.md`. The sub-agent reads `report.md`, appends `## Coaching Commentary`, verifies all canonical artifacts on disk, and returns a structured success payload.

**Why this model:** In Cowork, sub-agents have a restricted tool allowlist (no Bash). By keeping orchestration in the main thread and dispatching sub-agents only for analytical or post-compose tasks that use only Read/Edit/Glob/Grep, the pipeline works correctly in both Claude Code (CLI) and Cowork.

**Tolerant JSON extraction protocol (Context A):** After dispatching the sub-agent, capture its final assistant message. The sub-agent should return raw JSON, but may wrap it in ` ```json ... ``` ` fences or add a prose preamble. Extract JSON tolerantly:

1. If the message is wrapped in a ` ```json ... ``` ` (or plain ` ``` ... ``` `) fence, strip the fence first.
2. Try to parse the stripped text directly as JSON.
3. If that fails, walk through the text looking for the first `{` character and try `json.JSONDecoder().raw_decode(text[i:])` — this is brace-aware and handles nested objects correctly (unlike regex, which truncates on the first `}`).
4. If extraction fails entirely, re-prompt the sub-agent with: "Your previous reply could not be parsed as JSON. Return ONLY the JSON object — no markdown fences, no prose preamble."

> See `founder-skills/references/skill-execution-model.md` for the full inline-skill execution model (3 dispatch contexts, Mitigation 1+2, producer contract, Cowork quirks, per-symptom triage).

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
- **`evaluation-criteria.md`** — Read before Step 5. 28 dimensions across 7 categories with stage-calibrated thresholds
- **`ic-dynamics.md`** — Read before composing discussion.json. How real VC ICs work: formats, decisions, what kills deals
- **`artifact-schemas.md`** — Consult as needed when depositing agent-written artifacts

## Artifact Pipeline

Every simulation deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | founder context | `founder_context.py` read/init |
| 2 | `startup_profile.json` | Agent (heredoc) |
| 3 | `prior_artifacts.json` | Agent (heredoc) |
| 4 | `fund_profile.json` | Agent (heredoc) then `fund_profile.py` validates |
| 5a | `conflict_check.json` | Context A dispatch: DETECT_CONFLICTS → `detect_conflicts.py` |
| 5b-d | `partner_assessment_{visionary,operator,analyst}.json` | Context A dispatch: PARTNER_ANALYSIS × 3 **in parallel** |
| 6 | `discussion.json` | Main thread combines 3 partner returns |
| 7 | `score_dimensions.json` | Context A dispatch: SCORE_DIMENSIONS → `score_dimensions.py` |
| 8 | Report | `compose_report.py` (writes both `report.json` and `report.md`) |
| 9 | Coaching | Context B dispatch: POST_COMPOSE_COACHING |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts, consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$SIM_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (5–7), share a one-sentence finding before moving on.

## Workflow

### Step 0: Path Setup

**Every Bash tool call runs in a fresh shell — variables do not persist.** Prefix every Bash call that uses these paths with the variable block below, or substitute absolute paths directly:

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/scripts"
REFS="${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references"
SHARED_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/ic-sim/scripts/score_dimensions.py`, strip to get `SCRIPTS`, derive `REFS` and `SHARED_SCRIPTS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

After Step 1 (when the slug is known):

```bash
SIM_DIR="$ARTIFACTS_ROOT/ic-sim-${SLUG}"
mkdir -p "$SIM_DIR"
mkdir -p "$SIM_DIR/.staging"   # for ad-hoc sub-agent JSON staging (v0.4.2)
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

Read the provided materials and extract the startup profile directly. Import any prior market-sizing or deck-review artifacts from `$ARTIFACTS_ROOT`. Deposit both artifacts to `$SIM_DIR`.

**Read `$REFS/artifact-schemas.md` before writing artifacts** to ensure JSON schema compliance.

Write `startup_profile.json`:
```bash
cat <<'PROFILE_EOF' > "$SIM_DIR/startup_profile.json"
{
  "company_name": "...",
  "simulation_date": "YYYY-MM-DD",
  "stage": "seed",
  "one_liner": "...",
  "sector": "...",
  "geography": "...",
  "business_model": "...",
  "funding_history": "...",
  "current_raise": "...",
  "key_metrics": "...",
  "materials_provided": ["..."],
  "metadata": {"run_id": "<RUN_ID>"}
}
PROFILE_EOF
```

Write `prior_artifacts.json` (stub if no prior artifacts):
```bash
cat <<'PRIOR_EOF' > "$SIM_DIR/prior_artifacts.json"
{"imported": [], "skipped": [], "reason": "No prior artifacts available", "metadata": {"run_id": "<RUN_ID>"}}
PRIOR_EOF
```

### Step 4: Build Fund Profile -> `fund_profile.json`

**REQUIRED — read `$REFS/partner-archetypes.md` now.**

**Generic mode:** Build a standard early-stage fund profile with the three canonical archetypes (visionary, operator, analyst).

**Fund-specific mode:** Use WebSearch to research fund thesis, portfolio, partner backgrounds, check size range, and stage preference. Map real partners to archetype roles.

**Validation constraints:** `check_size_range` must be a dict (not a string), `stage_focus` must be a non-empty array, each source must have `url` or `title`.

```bash
cat <<'FUND_EOF' | python3 "$SCRIPTS/fund_profile.py" --pretty -o "$SIM_DIR/fund_profile.json"
{...fund profile JSON...}
FUND_EOF
```

**Accepted warnings:** Add `accepted_warnings` array with `code`, `match` (case-insensitive), and `reason`. Compose downgrades matching warnings to `"acknowledged"`.

### Sub-agent JSON staging (v0.4.2)

When a sub-agent returns JSON too large for bash heredoc, write it to
`$SIM_DIR/.staging/<step>_input.json` first, then pipe via:

```bash
cat "$SIM_DIR/.staging/<step>_input.json" | python3 "$SCRIPTS/<producer>.py" ...
```

The `.staging/` directory is created at setup and removed at cleanup.
This avoids `Operation not permitted` errors that occur when writing to
`$OUTPUTS_ROOT/` (Cowork sandbox marks that read-only post-write).

### Step 5a: Check Portfolio Conflicts -> `conflict_check.json` (Context A dispatch)

**Dispatch the ic-sim sub-agent in Context A (DETECT_CONFLICTS).** Dispatch via the `Task` tool.

**Dispatch prompt template:**

```
CONTEXT: DETECT_CONFLICTS
SIM_DIR: <absolute path to SIM_DIR>
RUN_ID: <RUN_ID>

You are the ic-sim agent dispatched in Context A (DETECT_CONFLICTS).
Read fund_profile.json at <SIM_DIR>/fund_profile.json and startup_profile.json
at <SIM_DIR>/startup_profile.json.

For each company in the fund's portfolio, assess whether it conflicts with the
startup. Assess each company for: direct conflict, adjacent conflict, or
customer overlap. Use consistent names between portfolio and conflicts.

Return JSON only — exactly the shape expected by detect_conflicts.py
(portfolio_size and conflicts array — no metadata block; producer script adds it):
{
  "portfolio_size": <integer>,
  "conflicts": [
    {
      "company": "<portfolio company name>",
      "type": "direct|adjacent|customer_overlap",
      "severity": "blocking|manageable",
      "rationale": "<specific reason for conflict>"
    }
  ]
}

Return empty conflicts array if no conflicts found. portfolio_size must equal
the number of companies in the fund's portfolio.
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol (see "Skill Execution Model" preamble) to obtain the structured JSON. Then pipe through the producer script:

```bash
cat <<'CONFLICT_EOF' | python3 "$SCRIPTS/detect_conflicts.py" --pretty -o "$SIM_DIR/conflict_check.json"
<JSON extracted from sub-agent reply>
CONFLICT_EOF
```

### Step 5b-d: Partner Assessments (PARTNER_ANALYSIS × 3 in parallel)

**REQUIRED — read `$REFS/partner-archetypes.md` and `$REFS/evaluation-criteria.md` now (if not already read).**

#### Parallel dispatch recipe

Dispatch the ic-sim agent **THREE TIMES in parallel** via the Task tool — one per archetype (visionary, operator, analyst). Use a **SINGLE assistant turn** with 3 Task tool calls (NOT three sequential turns). The Claude Code harness runs all three Task calls in parallel when they appear in the same assistant response.

Pseudocode for the dispatch (executed as 3 parallel Task tool_use blocks):

```
[
  Task(description="Partner analysis: visionary",
       prompt="CONTEXT: PARTNER_ANALYSIS\narchetype: visionary\nSIM_DIR: <path>\nRUN_ID: <id>\nfund_profile: <contents>\ndeal_context: <startup_profile contents>"),
  Task(description="Partner analysis: operator",
       prompt="CONTEXT: PARTNER_ANALYSIS\narchetype: operator\nSIM_DIR: <path>\nRUN_ID: <id>\nfund_profile: <contents>\ndeal_context: <startup_profile contents>"),
  Task(description="Partner analysis: analyst",
       prompt="CONTEXT: PARTNER_ANALYSIS\narchetype: analyst\nSIM_DIR: <path>\nRUN_ID: <id>\nfund_profile: <contents>\ndeal_context: <startup_profile contents>"),
]
```

**Full dispatch prompt template (used for each archetype separately, with `archetype:` changed):**

```
CONTEXT: PARTNER_ANALYSIS
archetype: visionary|operator|analyst
SIM_DIR: <absolute path to SIM_DIR>
RUN_ID: <RUN_ID>

You are the ic-sim agent dispatched in Context A (PARTNER_ANALYSIS) for the
<archetype> archetype. Read:
- ${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references/partner-archetypes.md
- ${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references/evaluation-criteria.md
- <SIM_DIR>/startup_profile.json
- <SIM_DIR>/fund_profile.json
- <SIM_DIR>/prior_artifacts.json (if present)

Embody the <archetype> partner perspective as defined in partner-archetypes.md.
Evaluate the startup from that specific lens. Every conviction point and concern
must be grounded in specific evidence from the startup materials.

Return JSON only — the partner assessment object (no metadata block):
{
  "partner": "<archetype>",
  "verdict": "invest|more_diligence|pass|hard_pass",
  "rationale": "<200+ word explanation of the verdict from this archetype's perspective>",
  "conviction_points": ["<specific strength, min 2>", ...],
  "key_concerns": ["<specific concern, min 2>", ...],
  "questions_for_founders": ["<question the archetype would ask>", ...],
  "diligence_requirements": ["<what this partner needs to see before committing>", ...]
}
```

**After all three sub-agents return:** apply the tolerant JSON extraction protocol to each of the three returned messages. Write each partner's assessment directly:

```bash
# Write partner_assessment_visionary.json (insert the extracted JSON, adding metadata)
cat <<'VISIONARY_EOF' | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['metadata'] = {'run_id': '$RUN_ID'}
with open('$SIM_DIR/partner_assessment_visionary.json', 'w') as f:
    json.dump(data, f, indent=2)
"
<JSON extracted from visionary sub-agent reply>
VISIONARY_EOF

# Repeat for operator and analyst
```

Or more concisely: write the three extracted JSONs to `partner_assessment_{role}.json` with `metadata.run_id` injected.

**Verify after writes:** check that `$SIM_DIR` contains all three `partner_assessment_*.json` files. If any are missing, re-run that dispatch before proceeding.

### Step 6: Compose Discussion -> `discussion.json`

**REQUIRED — read `$REFS/ic-dynamics.md` now.**

Read all 3 partner assessments from `$SIM_DIR`. Compose the IC discussion object: each partner presents, partners respond to each other, build toward consensus. In interactive mode, pause between positions.

**Verdict reconciliation:** Ensure each partner's verdict in `partner_verdicts` reflects their **final** position after debate, not their opening position. The compose report flags `UNANIMOUS_VERDICT_MISMATCH` when all partners contradict the consensus.

Write `discussion.json` directly:

```bash
cat <<'DISCUSSION_EOF' > "$SIM_DIR/discussion.json"
{
  "assessment_mode": "sub-agent",
  "assessment_mode_intentional": true,
  "partner_verdicts": [
    {"partner": "visionary", "verdict": "...", "rationale": "..."},
    {"partner": "operator", "verdict": "...", "rationale": "..."},
    {"partner": "analyst", "verdict": "...", "rationale": "..."}
  ],
  "debate_sections": [
    {
      "topic": "...",
      "exchanges": [
        {"partner": "visionary", "position": "..."},
        {"partner": "operator", "position": "..."}
      ]
    }
  ],
  "consensus_verdict": "...",
  "key_concerns": ["..."],
  "diligence_requirements": ["..."],
  "metadata": {"run_id": "<RUN_ID>"}
}
DISCUSSION_EOF
```

### Step 7: Score Dimensions -> `score_dimensions.json` (Context A dispatch)

**Dispatch the ic-sim sub-agent in Context A (SCORE_DIMENSIONS).** Dispatch via the `Task` tool.

**Dispatch prompt template:**

```
CONTEXT: SCORE_DIMENSIONS
SIM_DIR: <absolute path to SIM_DIR>
RUN_ID: <RUN_ID>

You are the ic-sim agent dispatched in Context A (SCORE_DIMENSIONS).
Read:
- ${CLAUDE_PLUGIN_ROOT}/skills/ic-sim/references/evaluation-criteria.md
- <SIM_DIR>/startup_profile.json
- <SIM_DIR>/discussion.json
- <SIM_DIR>/partner_assessment_visionary.json
- <SIM_DIR>/partner_assessment_operator.json
- <SIM_DIR>/partner_assessment_analyst.json

Score all 28 dimensions based on the evidence from the startup materials and
the partner assessments. Ensure scoring reflects the discussion conclusions —
if a dimension was debated as a dealbreaker, the score must reflect that.

Return JSON only — the items array without summary (producer script computes summary):
{
  "items": [
    {
      "id": "team_founder_market_fit",
      "category": "Team",
      "status": "strong_conviction|moderate_conviction|concern|dealbreaker|not_applicable",
      "evidence": "<specific evidence from startup materials>",
      "notes": "<optional explanation>"
    },
    ...all 28 dimensions...
  ]
}
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the structured JSON. Then pipe through the producer script:

```bash
cat <<'SCORE_EOF' | python3 "$SCRIPTS/score_dimensions.py" --pretty -o "$SIM_DIR/score_dimensions.json"
<JSON extracted from sub-agent reply>
SCORE_EOF
```

### Step 8: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$SIM_DIR" --pretty \
  -o "$SIM_DIR/report.json" \
  --write-md "$SIM_DIR/report.md"
```

`compose_report.py` writes both `report.json` and `report.md` deterministically. **Do NOT** read `report_markdown` out of `report.json` and re-write it via heredoc — agent heredoc handling can drift and produce unparseable output.

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Post-write verification:** `compose_report.py` exits non-zero (code 2) if the declared output files don't exist or are empty after writing. If compose exits non-zero, stop and report the exact stderr — do not proceed to Step 9.

### Step 9: Post-Compose Coaching Commentary (Context B dispatch — POST_COMPOSE_COACHING)

**Dispatch the ic-sim sub-agent in Context B.** Dispatch via the `Task` tool after `compose_report.py` has successfully written both `report.json` and `report.md`.

**Mitigation 2 protocol (v0.4.2):** the main thread reads the structured `coaching_payload` from `report.json` and inlines it into the dispatch prompt. The sub-agent does NOT Read full `report.md` — it consumes `coaching_payload` directly, performs Grep idempotency, Edits via the per-run uuid `insertion_marker`, and Grep-verifies all artifacts. See the ic-sim agent body's "Context B — Post-compose coaching dispatch (POST_COMPOSE_COACHING)" section for the full procedure.

<!-- skill-quality-ci: bash-after-subagent-ok -->
```bash
COACHING_PAYLOAD="$(python3 -c '
import json, sys
data = json.load(open(sys.argv[1]))
print(json.dumps(data["coaching_payload"], indent=2))
' "$SIM_DIR/report.json")"
```

**Dispatch prompt template:**

```
CONTEXT: POST_COMPOSE_COACHING

You are dispatched to add coaching commentary to an IC simulation report.

The compose_report.py script has finished. The structured `coaching_payload`
from report.json is:

<paste $COACHING_PAYLOAD JSON here verbatim>

Follow your agent body's Context B procedure
(POST_COMPOSE_COACHING):

1. grep_idempotency_check — Grep "## Coaching Commentary" (output_mode:count)
   and Grep the EXACT coaching_payload.insertion_marker (output_mode:count)
   on coaching_payload.report_path. Apply the 6-state decision matrix.
2. Compose commentary from the inlined coaching_payload (dealbreakers,
   concerns, summary, high_severity_warnings, company_name).
   Do NOT Read the full report.md.
3. edit_via_marker — single Edit on coaching_payload.report_path:
     old_string = coaching_payload.insertion_marker  (EXACT uuid string)
     new_string = "## Coaching Commentary\n\n<your commentary>"
4. self_verify_artifacts_via_grep_run_id — Grep run_id from each producer
   artifact (fund_profile.json, conflict_check.json, discussion.json,
   score_dimensions.json), confirm all 4 match; bounded Read (limit:1) on
   report.json and report.md; re-Grep the marker (must be 0) and the
   "## Coaching Commentary" header (must be 1).
5. Return the success payload:
   {"status": "complete", "review_dir": "<path>", "report_path": "<path>",
    "decision": "<summary.verdict>", "consensus_strength": "strong|mixed|weak",
    "key_concerns": ["<top 3 from concerns[].dimension>"],
    "high_severity_warnings": [<list>]}
   OR if verification fails:
   {"status": "blocked", "reason": "<specific gap>"}

Stop after returning JSON. Do not narrate.
```

**After the sub-agent returns:** apply the tolerant JSON extraction protocol to obtain the success/blocked payload. If `status == "blocked"`, stop and report the reason to the founder. If `status == "complete"`, present `report_path` to the founder.

### Step 10 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$SIM_DIR" -o "$SIM_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 11: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_IC_Simulation.md`, `.html` (if generated), `.json` (optional).

```bash
rm -rf "$SIM_DIR/.staging" 2>/dev/null || true
```

## Main-Thread Return

This skill runs inline in the main thread (not as a sub-agent). The final outcome the main thread delivers to the founder is:

- The path to `$SIM_DIR/report.md` — the primary deliverable.
- The structured success payload from the Context B sub-agent (Step 9): `{status, review_dir, report_path, decision, consensus_strength, key_concerns, high_severity_warnings}`.
- Optionally: the HTML report path from Step 10.

**Do NOT inline `report_markdown` in the assistant message.** The founder reads the file via the path.

## Scoring

- 28 dimensions, each: `strong_conviction` / `moderate_conviction` / `concern` / `dealbreaker` / `not_applicable`
- Conviction score: `(strong*1.0 + moderate*0.5) / applicable * 100`
- Verdicts: `invest` (>=75%), `more_diligence` (>=50%), `pass` (<50%), `hard_pass` (any dealbreaker)
- One dealbreaker forces `hard_pass` regardless of score

## Cross-Agent Integration

This skill imports artifacts from prior market-sizing and deck-review analyses. Imported artifacts are recorded with dates. Imports older than 7 days are flagged as `STALE_IMPORT`.
