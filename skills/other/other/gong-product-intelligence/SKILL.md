---
name: gong-product-intelligence
description: Analyzes Gong sales call transcripts from a product team perspective. Extracts what customers love, what they dislike, missing features they request, objection categories, sentiment, and conversion blockers. Use when the user wants to analyze sales calls, understand product feedback, identify feature gaps, or generate a product intelligence report from call data.
metadata:
  author: LTX Analytics
  version: 3.0.0
  category: product-intelligence
---

# Gong Product Intelligence Agent

Analyzes LTX sales call transcripts to extract structured product insights for the product team.
Fetches data directly from BigQuery — no CSV required.

## Trigger phrases

Use this skill when the user says:
- "analyze gong calls"
- "what do customers think about the product"
- "product feedback from sales calls"
- "what features are customers asking for"
- "why aren't deals converting"
- "generate product intelligence report"
- "regenerate the report"
- "refresh the HTML"

---

## Interactive agent flow

When triggered, **always ask these questions first** before running anything:

```
1. Which product? (studio / api / scaler)
2. What time period? (e.g. "last 3 months", "since Oct 2025", "all time")
3. Which calls to include?
   - non-converted (default) — companies that never became pilots or paying customers
   - converted — companies that DID become pilots or paying/enterprise customers
   - both — all calls regardless of conversion outcome
4. Is there a specific topic or question you want to focus on? (optional)
   e.g. "storyboard adoption", "pricing objections", "why enterprise deals don't close"
   Press Enter / say "no" to skip — Claude will do a full broad analysis.
```

Then translate the answers into the correct CLI command and run it.

### Example: user says "analyze studio calls since October, focus on storyboard"

```bash
python3 agents/gong-product-intelligence/scripts/analyze_calls.py \
  --product studio \
  --date-from 2025-10-01 \
  --output "/Users/yfainberg/my-project/gong calls analyze/output" \
  --focus "storyboard adoption and feedback"
```

### Example: user says "api calls, all time, converted customers only"

```bash
python3 agents/gong-product-intelligence/scripts/analyze_calls.py \
  --product api \
  --date-from 2020-01-01 \
  --conversion-status converted \
  --output "/Users/yfainberg/my-project/gong calls analyze/output"
```

### Example: user says "studio, last 6 months, both converted and non-converted"

```bash
python3 agents/gong-product-intelligence/scripts/analyze_calls.py \
  --product studio \
  --date-from 2024-09-01 \
  --conversion-status both \
  --output "/Users/yfainberg/my-project/gong calls analyze/output"
```

---

## All CLI flags

| Flag | Description |
|------|-------------|
| `--product studio\|api\|scaler` | Product to analyze — fetches from BigQuery |
| `--date-from YYYY-MM-DD` | Earliest call date to include (default: 2025-01-01) |
| `--output /path/` | Output directory (default: configured inside script) |
| `--limit N` | Analyze only N calls (for quick tests) |
| `--fresh` | Ignore cached results and reprocess all |
| `--report-only` | Regenerate HTML from existing `analysis_results.json` without any API calls |
| `--backfill-clusters` | Add cluster fields to pre-v2 results using keyword matching, then regenerate report |
| `--validate N` | Generate side-by-side HTML report for N random calls for manual accuracy review |
| `--qa` | After report generation, enter interactive Q&A mode |
| `--conversion-status non-converted\|converted\|both` | Which calls to include (default: non-converted) |
| `--focus "topic"` | Optional focus area — Claude pays extra attention to this topic in every call |

---

## Q&A mode

After the report is generated, `--qa` drops into an interactive loop:

```
Q&A Mode  (type 'done' or press Ctrl-C to finish)

Your question: What are the top 3 reasons enterprise deals don't close?
→ Asking Claude...

Answer: Based on the data, the top enterprise conversion blockers are:
1. Price/ROI uncertainty (17 mentions) — prospects want clearer cost justification
2. Missing Adobe/NLE integration (12 mentions) — teams can't adopt without workflow continuity
3. Credit system confusion (9 mentions) — hourly billing model feels unpredictable
```

Each answer is:
- Saved to `qa.json` in the output directory
- Immediately appended to the HTML report (visible as a "Q&A" section at the bottom)

The report can be shared with the team and will include all Q&A pairs.

---

## What the report contains

| Section | What it shows |
|---------|---------------|
| AI Executive Summary | Headline + key findings + product priorities + sales recs |
| Sentiment | Categorical distribution: positive / neutral / negative call counts |
| Industry filter | Click any industry pill to filter all charts |
| Monthly trend | Stacked bar chart showing sentiment over time |
| Objections | Donut chart: product / price / competitor / timing / process |
| Product Strengths | Clustered bar chart — click any bar to drill into examples |
| Product Weaknesses | Clustered bar chart — click to drill |
| Feature Requests | Clustered bar chart — click to drill |
| Discovery Gaps | Features customers asked for that already exist (education opportunity) |
| Competitors | Full horizontal bar chart of all normalized competitors |
| Feature Sentiment | Per-feature sentiment split table |
| Voice of Customer | 9 notable verbatim quotes |
| Q&A | Questions asked and Claude's answers (if Q&A mode was used) |

---

## How the analysis works

1. **BigQuery fetch** — SQL query runs for the chosen product and conversion status, pulling call transcripts joined with Salesforce opportunity data
2. **Claude analyzes each call** using `ANALYSIS_SYSTEM_PROMPT` (product knowledge + optional focus injected) + `ANALYSIS_USER_PROMPT` (call context + transcript). Returns structured JSON per call including reasoning and cluster assignments.
3. **Python aggregates** all results — normalizes competitors (`normalize_competitor()`), clusters strengths/weaknesses/feature requests by the Claude-assigned cluster names, counts categorical sentiment
4. **Claude generates the AI executive summary** from the aggregated data (cached in `summary.json`)
5. **Python generates the HTML report** from all the above
6. **Q&A mode** (optional) — user asks questions, Claude answers from `aggregated.json`, answers saved to `qa.json` and re-injected into the report

The intelligence comes from steps 2, 4, and 6 (LLM). Steps 1, 3, 5 are deterministic Python.

---

## Output files

| File | Description |
|------|-------------|
| `analysis_results.json` | Per-call structured JSON (one entry per call) |
| `aggregated.json` | Aggregated counts, clustered data, normalized competitors |
| `summary.json` | AI executive summary (cached) |
| `qa.json` | Q&A pairs (if Q&A mode was used) |
| `product_intelligence_report.html` | The visual HTML report |

The script is resumable — it skips already-processed calls based on company+date key, saving every 10 calls.

---

## Products

> For product descriptions see `shared/product-context.md`. The table below covers SQL-specific logic only.

| Product | SQL logic |
|---------|-----------|
| `studio` | Studio leads, no enterprise orgs, pilot filter per `--conversion-status` |
| `api` | API-only leads, call title contains "api" or "ltx-2", stage filter per `--conversion-status` |
| `scaler` | Scaler-only leads, call title contains "scaler" or "brands", stage filter per `--conversion-status` |

---

## Regenerate report only (no API calls, instant)

Use this when you update clustering constants, HTML layout, or competitor normalization:

```bash
python3 agents/gong-product-intelligence/scripts/analyze_calls.py \
  --output "/path/to/output/" \
  --report-only
```

Add `--qa` to also enter Q&A mode after regeneration.

---

## Product knowledge

The agent uses `shared/product-features.md` as its source of truth (injected into every call analysis):
- **Features that EXIST** — used to distinguish real feature gaps from things already built
- **Features that do NOT exist** — used to correctly classify feature requests
- **Pricing tiers** — used for price objection context
- **Canonical competitor names** — ensures consistent normalization across all calls

**Update `shared/product-features.md` when new features ship.** It's shared across all agents.

---

## Clustering constants (in analyze_calls.py)

The script contains predefined cluster name lists injected into both the analysis prompt AND the Python aggregator:
- `STRENGTH_CLUSTER_NAMES` — 14 topic buckets
- `WEAKNESS_CLUSTER_NAMES` — 15 topic buckets
- `FEATURE_REQUEST_CLUSTER_NAMES` — 14 topic buckets
- `COMPETITOR_MAP` — maps raw competitor strings to canonical names

To improve clustering accuracy without re-running the LLM analysis:
1. Edit the cluster names in `analyze_calls.py`
2. Run with `--backfill-clusters` to re-apply keyword matching to old results
3. Run with `--report-only` to instantly regenerate the report

---

## Report design principles (do not revert these)

- **Sentiment is CATEGORICAL** — shown as 3 cards (positive / neutral / negative) with counts and percentages. Never show it as a numerical average.
- **Strengths/weaknesses/feature requests are CLUSTERED** — individual items grouped into semantic topic buckets so the full picture is visible. Click any bar to drill into examples.
- **All competitors are shown** — not just top 10. Full horizontal bar chart with all normalized competitors sorted by mention count.
- **Q&A is persistent** — answers saved to `qa.json` and always included in the report on regeneration.
- **Chart.js** is used for visualizations (dark theme, loaded from CDN).
