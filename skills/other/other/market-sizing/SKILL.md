---
name: market-sizing
disable-model-invocation: true
description: "Builds credible TAM/SAM/SOM analysis with external validation and sensitivity testing for startup fundraising. Use when user asks to 'size this market', 'what's the TAM', 'analyze this market', 'validate these market numbers', 'review the market sizing slide', 'is this market big enough', 'market sizing', 'TAM/SAM/SOM', 'stress-test market assumptions', or provides a pitch deck, financial model, or market data for analysis. Supports top-down, bottom-up, or dual-methodology approaches. Do NOT use for general market research without sizing, competitive landscape analysis, or financial model review (use financial-model-review)."
compatibility: Requires Python 3.10+ and uv for script execution.
metadata:
  author: lool-ventures
  version: "0.2.0"
exports:
  - "sizing.json -> financial-model-review, ic-sim, fundraise-readiness"
  - "sensitivity.json -> financial-model-review"
  - "checklist.json -> ic-sim"
---

# Market Sizing Skill

Help startup founders build credible, defensible TAM/SAM/SOM analysis — the kind that earns investor trust rather than raising eyebrows. Produce a structured, validated market sizing with external sources, sensitivity testing, and a self-check against common pitfalls. The tone is founder-first: a rigorous but supportive coaching session.

## Input Formats

Accept any format: pitch deck (PDF, PPTX, markdown), financial model, market data, text descriptions, or verbal description of the business.

## Available Scripts

All scripts are at `${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/scripts/`:

- **`market_sizing.py`** — TAM/SAM/SOM calculator (top-down, bottom-up, or both)
- **`sensitivity.py`** — Stress-test assumptions with low/base/high ranges and confidence-based auto-widening
- **`checklist.py`** — Validates 22-item self-check with pass/fail per item
- **`compose_report.py`** — Assembles report with cross-artifact validation; `--strict` exits 1 on high/medium warnings
- **`visualize.py`** — Generates self-contained HTML with SVG charts (not JSON)

Run with: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/scripts/<script>.py --pretty [args]`

## Available References

Read as needed from `${CLAUDE_PLUGIN_ROOT}/skills/market-sizing/references/`:

- **`tam-sam-som-methodology.md`** — Definitions, calculation methods, industry examples, best practices
- **`pitfalls-checklist.md`** — Self-review checklist for common mistakes
- **`artifact-schemas.md`** — JSON schemas for all analysis artifacts

## Artifact Pipeline

Every analysis deposits structured JSON artifacts into a working directory. The final step assembles all artifacts into a report and validates consistency. This is not optional.

| Step | Artifact | Producer |
|------|----------|----------|
| 1 | `inputs.json` | Sub-agent (Task) or agent (heredoc) |
| 2 | `methodology.json` | Sub-agent (Task) or agent (heredoc) |
| 3 | `validation.json` | Agent (consolidates sub-agent web research) |
| 4 | `sizing.json` | `market_sizing.py -o` |
| 5 | `sensitivity.json` | Sub-agent (Task) + `sensitivity.py` |
| 6 | `checklist.json` | Sub-agent (Task) + `checklist.py` |
| 7 | Report | `compose_report.py` reads all |

**Rules:**
- Deposit each artifact before proceeding to the next step
- For agent-written artifacts (Steps 1-3), consult `references/artifact-schemas.md` for the JSON schema
- If a step is not applicable, deposit a stub: `{"skipped": true, "reason": "..."}`
- **Do NOT use `isolation: "worktree"`** for sub-agents — files written in a worktree won't appear in the main `$ANALYSIS_DIR`

Keep the founder informed with brief, plain-language updates at each step. Never mention file names, scripts, or JSON. After each analytical step (4–6), share a one-sentence finding before moving on.

## Workflow

### Path Setup

```bash
SCRIPTS="$CLAUDE_PLUGIN_ROOT/skills/market-sizing/scripts"
REFS="$CLAUDE_PLUGIN_ROOT/skills/market-sizing/references"
SHARED_REFS="$CLAUDE_PLUGIN_ROOT/references"
if ls "$(pwd)"/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/mnt/*/ | head -1)artifacts"
elif ls "$(pwd)"/sessions/*/mnt/*/ >/dev/null 2>&1; then
  ARTIFACTS_ROOT="$(ls -d "$(pwd)"/sessions/*/mnt/*/ | head -1)artifacts"
else
  ARTIFACTS_ROOT="$(pwd)/artifacts"
fi
```

If `CLAUDE_PLUGIN_ROOT` is empty, fall back: `Glob` for `**/founder-skills/skills/market-sizing/scripts/market_sizing.py`, strip to get `SCRIPTS`, derive `REFS`.

**If `ARTIFACTS_ROOT` resolves to `$(pwd)/artifacts` but no `artifacts/` directory exists at `$(pwd)`:** The workspace may not be mounted yet. Use `Glob` with pattern `**/artifacts/founder_context.json` to locate existing artifacts, and derive `ARTIFACTS_ROOT` from the result. If nothing is found, `mkdir -p "$ARTIFACTS_ROOT"` and proceed.

```bash
ANALYSIS_DIR="$ARTIFACTS_ROOT/market-sizing-{company-slug}"
mkdir -p "$ANALYSIS_DIR"
```

### Steps 1-2: Extract Inputs & Choose Methodology

**When files are provided (deck, model, market data),** spawn a `general-purpose` Task sub-agent to read materials and determine methodology. The sub-agent receives: file path(s), `SCRIPTS`, `REFS`, `SHARED_REFS`, and `ANALYSIS_DIR` paths. **Do NOT use `isolation: "worktree"`.**

The sub-agent:
1. Reads the provided file(s)
2. Reads `$REFS/tam-sam-som-methodology.md`
3. Reads `$REFS/artifact-schemas.md` for `inputs.json` and `methodology.json` schemas
4. Extracts all market-relevant data
5. Writes `inputs.json` to `$ANALYSIS_DIR/inputs.json`
6. Writes `methodology.json` to `$ANALYSIS_DIR/methodology.json`

If the deck includes explicit TAM/SAM/SOM claims, record them in `inputs.json` under `existing_claims`. These are used by compose_report.py and visualize.py to compare deck claims against calculated figures.

Instruct the sub-agent to return ONLY:
1. File paths written
2. **Company brief:** name, product description, geography, target segments, pricing model, revenue model type
3. **Quantitative data found:** revenue, customer count, ARPU, growth rates, headcount (actual values, not the full inputs.json)
4. **Existing claims:** actual TAM/SAM/SOM numbers from the deck (if found), with slide/section reference
5. **Methodology:** chosen approach + rationale
6. **Data availability:** which key fields are populated vs missing
7. List of missing/unclear fields that the founder should clarify

Do not echo the full artifacts or raw document content. The company brief must be rich enough for the main agent to direct web research, construct sizing calculations, perform reality checks, and provide contextual coaching — without needing to re-read the source materials.

After the sub-agent returns, review the summary. If missing fields are flagged, ask the founder and patch `inputs.json`. Share a brief update.

**When conversational input (no files):** Handle directly in the main agent — the data is already in the conversation. Read `references/tam-sam-som-methodology.md`, choose the approach, and write both artifacts directly.

**Graceful degradation:** If Task tool is unavailable, extract directly in the main agent.

### Step 3: External Validation -> `validation.json`

**When methodology is "both",** spawn 2 `general-purpose` Task sub-agents **in a single message** (parallel, no `isolation: "worktree"`). Each receives: company description, product/service, geography, segments from `inputs.json`, and methodology context.

- **Sub-agent A (Top-down research):** WebSearch for industry reports, government statistics, analyst estimates for total market size, segment percentages, market growth rates.
- **Sub-agent B (Bottom-up research):** WebSearch for customer counts, pricing/ARPU benchmarks, competitor data, serviceable segment data. Also receives: pricing model, customer profile.

Each returns ONLY: (1) structured assumptions array `[{name, value, source_url, source_title, quality_tier, confidence, category}]`, (2) key market figures found, (3) source count and quality distribution. Do not echo raw search results.

Main agent consolidates both sets of findings into `validation.json`, cross-validates between approaches, and flags discrepancies.

**When methodology is single (top-down or bottom-up),** spawn 1 sub-agent for the chosen approach. Same return contract. Main agent writes `validation.json`.

**When pure calculation (user provides all numbers, no validation needed):** Handle directly — no sub-agent.

**Source quality hierarchy:** Government/regulatory > Established analysts > Industry associations > Academic > Business press > Company blogs (product facts only).

Triangulate key numbers with 2+ independent sources. Track every source with quality tier and segment match. Every assumption must appear in the `assumptions` array with a `name` matching script parameter names and a `category` of `sourced`, `derived`, or `agent_estimate`.

**Graceful degradation:** If Task tool is unavailable, research directly in the main agent.

### Step 4: Calculate TAM/SAM/SOM -> `sizing.json`

```bash
cat <<'SIZING_EOF' | python3 "$SCRIPTS/market_sizing.py" --stdin --pretty -o "$ANALYSIS_DIR/sizing.json"
{...sizing input JSON — see artifact-schemas.md for format...}
SIZING_EOF
```

For "both" mode, check the comparison section — a >30% TAM discrepancy means investigating which assumptions are flawed. TAM must match the product's actual target universe (not inflated industry totals).

**Multi-vertical / platform companies:** If `inputs.json` lists applications in 2+ distinct industries:

1. **Identify verticals** — classify as `commercial` (revenue/pilots), `r_and_d` (demonstrated feasibility, 2-3yr commercialization path), or `future` (conceptual/early).
2. **Include `commercial` and `r_and_d` in TAM.** If top-down only covers one vertical, use bottom-up as primary. When verticals have different ARPUs, compute weighted blended ARPU. `Future` verticals go in coaching commentary as upside, not in the calculated TAM.
3. **Narrow SAM and SOM** — SAM = traction + active R&D segments. SOM = beachhead only.
4. **Document scope** in `methodology.json` `rationale`.

Default to full-scope TAM. Only narrow to beachhead if the user explicitly requests it.

### Step 4.5: Reality Check

Before proceeding, answer:

1. **Laugh test:** Would an experienced VC nod or raise an eyebrow? Seed + <5 pilots + >$1B TAM = explain yourself.
2. **Scope match:** Does TAM cover all `commercial` and `r_and_d` verticals from `inputs.json`?
3. **Customer count sanity:** Can you name a representative sample of the customers in your count?
4. **Convergence integrity:** Were top-down and bottom-up parameters set independently? If you adjusted one after seeing the other, revert and accept the delta.

This step produces no artifact. If it reveals problems, fix them before proceeding.

### Steps 5 & 6: Parallel Analysis (Sensitivity + Checklist)

Spawn 2 `general-purpose` Task sub-agents **in a single message** (parallel, no `isolation: "worktree"`) after Step 4.5 reality check passes. Each receives the expanded `SCRIPTS`, `REFS`, and `ANALYSIS_DIR` paths.

**Sub-agent A — Sensitivity:**

Reads `$ANALYSIS_DIR/validation.json` for confidence tiers and `$ANALYSIS_DIR/sizing.json` for base values and approach. Constructs sensitivity input with confidence-based ranges and runs `sensitivity.py`.

Tag each parameter with confidence from validation: `sourced` (range stands), `derived` (min +/-30%), `agent_estimate` (min +/-50%). Include **every `agent_estimate` parameter** — compose_report.py flags missing ones as `UNSOURCED_ASSUMPTIONS`.

```bash
cat <<'SENS_EOF' | python3 "$SCRIPTS/sensitivity.py" --pretty -o "$ANALYSIS_DIR/sensitivity.json"
{...sensitivity input JSON — see artifact-schemas.md for format...}
SENS_EOF
```

Instruct Sub-agent A to return ONLY: (1) file path written, (2) `most_sensitive` parameter, (3) top 3 sensitivity ranking entries (parameter + SOM swing %).

**Sub-agent B — Checklist:**

Reads `$REFS/pitfalls-checklist.md` for the 22 criteria and all prior artifacts (`inputs.json`, `methodology.json`, `validation.json`, `sizing.json`). Assesses all 22 items with status and notes. **Read `$REFS/artifact-schemas.md` "Canonical 22 checklist IDs" section first.**

```bash
cat <<'CHECK_EOF' | python3 "$SCRIPTS/checklist.py" --pretty -o "$ANALYSIS_DIR/checklist.json"
{"items": [
  {"id": "structural_tam_gt_sam_gt_som", "status": "pass", "notes": null},
  ...all 22 items...
]}
CHECK_EOF
```

Instruct Sub-agent B to return ONLY: (1) file path written, (2) `score_pct`, (3) `overall_status`, (4) list of failed items.

**Graceful degradation:** If Task tool is unavailable, run Steps 5-6 sequentially in the main agent.

After both sub-agents return, share a coaching update with the founder before proceeding to Step 7.

### Step 7: Compose and Validate Report

```bash
python3 "$SCRIPTS/compose_report.py" --dir "$ANALYSIS_DIR" --pretty -o "$ANALYSIS_DIR/report.json"
```

Fix high-severity warnings and re-run. Use `--strict` to enforce a clean report.

**Primary deliverable:** Read `report_markdown` from the output JSON, write it to `$ANALYSIS_DIR/report.md`, and display it to the user in full. **Present the file path** so the user can access it directly. Then add coaching commentary: what to feel confident about, the highest-leverage fix, whether the market story holds together, and which 1-2 sensitivity parameters to prioritize sourcing.

### Step 8 (Optional): Generate Visual Report

```bash
python3 "$SCRIPTS/visualize.py" --dir "$ANALYSIS_DIR" -o "$ANALYSIS_DIR/report.html"
```

**Present the HTML file path** to the user so they can open the visual report.

### Step 9: Deliver Artifacts

Copy final deliverables to workspace root: `{Company}_Market_Sizing.md`, `.html` (if generated), `.json` (optional).

## Scoring

- Each of 22 items: pass / fail / not_applicable
- `score_pct` = pass / (total - not_applicable) x 100
- compose_report.py validates cross-artifact consistency (assumption coverage, sensitivity ranges)
