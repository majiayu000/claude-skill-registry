---
name: aeo-visibility-monitor
description: >
  Run recurring AEO (Answer Engine Optimization) visibility checks across ChatGPT,
  Perplexity, Gemini, and Claude. Compares each run to the previous one to surface
  visibility changes, competitor movements, and missed query opportunities. Wraps
  aeo-visibility with delta analysis and trend tracking. Use when a marketing team
  wants to know whether their brand is winning (or losing) in AI search over time.
tags: [seo]
---

# AEO Visibility Monitor

Recurring visibility tracking across AI answer engines. Runs the `aeo-visibility` check on a schedule, compares results to the last run, and surfaces what changed — brand mentions gained or lost, competitor movements, new query opportunities.

**Built on top of:** `aeo-visibility` skill. This skill adds the recurring cadence, delta analysis, and trend reporting layer.

## When to Use

- "Track our AEO visibility over time"
- "Are we appearing more or less in AI search?"
- "Set up monthly AEO monitoring for [client]"
- "What changed in our AI search visibility since last month?"
- "Are competitors gaining ground on AI answer engines?"

## Phase 0: Intake

1. Company name and website URL
2. 2-3 main competitors to track visibility against
3. Run cadence: monthly (default), bi-weekly, or weekly?
4. First run or recurring run?
   - **First run:** Will profile the company and generate queries (takes 15-30 min)
   - **Recurring run:** Reuses existing profile and queries (faster)
5. Any new queries to add since last run? (Optional)

## Phase 1: Check for Existing Profile

Look in `clients/<client-name>/aeo-visibility-reports/`:

```
clients/<client-name>/aeo-visibility-reports/
├── profile.json        # Company + competitor profile
├── queries.json        # ~100 test queries
├── history.csv         # Summary of all runs
└── runs/
    ├── 2026-02-01T08-00-00/
    └── 2026-03-01T08-00-00/
```

**If profile exists:** Skip to Phase 3 (run check).
**If not:** Run Phase 2 (profile setup).

## Phase 2: First-Time Setup (Profile)

Run `aeo-visibility` profile command:

```bash
node skills/aeo-visibility/src/cli.js profile <client-name> --url=<website_url>
```

This will:
- Research the company and identify competitors
- Generate ~100 diverse test queries covering:
  - Brand queries (direct mention)
  - Category queries (what you do)
  - Problem queries (the pain you solve)
  - Comparison queries (you vs competitors)
  - Use-case queries (specific scenarios)

**Before running the full check:** Review and edit `queries.json` to:
- Remove irrelevant queries
- Add high-priority queries specific to this client's positioning
- Ensure competitors are correctly identified

## Phase 3: Run Visibility Check

```bash
node skills/aeo-visibility/src/cli.js run <client-name>
```

Runs all queries against all 4 engines. Creates a dated run folder with:
- `report.md` — full analysis
- `results.csv` — raw data per query per engine
- `raw-responses.json` — full API responses

**Cost per run:** ~$10-30 (100 queries × 4 engines × ~$0.025-0.075/query)

## Phase 4: Delta Analysis (Core Value of This Skill)

After the run completes, compare the new `results.csv` against the previous run's `results.csv`.

### Metrics to Compare

For each engine (ChatGPT, Perplexity, Gemini, Claude):

| Metric | Definition |
|--------|------------|
| **Mention rate** | % of queries where brand is mentioned |
| **Prominence rate** | % of mentions that are "high" prominence |
| **Avg sentiment** | Average sentiment score across all mentions |
| **Competitor share** | % of queries where competitor is mentioned |

### Change Flags

| Change | Threshold | Severity |
|--------|-----------|----------|
| Mention rate ↓ | >5% drop | 🔴 Alert |
| Competitor mention rate ↑ | >5% increase | 🟡 Watch |
| Prominence drop | High → Medium or Low | 🟡 Watch |
| New queries with 0 mentions | Any new "missed opportunities" | 🟡 Watch |
| Mention rate ↑ | >5% increase | 🟢 Win |

### New Opportunity Detection

Compare queries where:
- **You: not mentioned** AND **competitor: mentioned** → These are displacement queries to target
- **You: mentioned, low prominence** → Content optimization opportunity

## Phase 5: Output Format

```markdown
# AEO Visibility Report — [DATE]
Client: [Name] | Previous run: [DATE] | Change period: [N days]

---

## Summary

| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Overall mention rate | [X%] | [X%] | ▲/▼ [X%] |
| High-prominence rate | [X%] | [X%] | ▲/▼ [X%] |
| Avg sentiment | [X] | [X] | ▲/▼ |
| [Competitor] mention rate | [X%] | [X%] | ▲/▼ [X%] |

**Net verdict:** [Improving / Stable / Declining]

---

## Changes Since Last Run

### 🟢 Wins
- [Engine]: Mention rate ↑ from [X%] to [X%]
- Now mentioned for: "[query example]" — was not before
- ...

### 🔴 Alerts
- [Engine]: Mention rate ↓ from [X%] to [X%]
- Lost visibility on: "[query example]"
- [Competitor] gained mentions on [N] queries where you dropped

### 🟡 Watch
- [Competitor] mention rate up [X%] on [Engine]
- [N] new queries added where you have zero mentions

---

## Engine Breakdown

### ChatGPT
- Mention rate: [X%] ([▲/▼ X%])
- Prominence: High [X%] / Medium [X%] / Low [X%]
- Top performing queries: [list]
- Missed queries (competitor mentioned, you not): [list]

### Perplexity
...

### Gemini
...

### Claude
...

---

## Competitor Movements

| Competitor | Mention rate change | Engines gaining | Notes |
|-----------|--------------------|--------------|----|
| [Name] | ▲ [X%] | ChatGPT, Perplexity | [context] |
...

---

## Top Opportunity Queries

Queries where a competitor appears but you don't — highest traffic potential:

1. "[Query]" — [Competitor] appears, you don't | Est. query volume: [range]
   Suggested fix: [content or PR action to get mentioned here]

2. "[Query]" — ...

---

## Recommended Actions

### This Month
1. [Specific action to recover lost visibility on [engine]]
2. [Content to publish targeting [opportunity query]]

### Next Quarter
1. [Structural PR / content strategy to improve overall mention rate]
```

Save to `clients/<client-name>/aeo-visibility-reports/runs/[YYYY-MM-DD]/monitor-report.md`.

Also update `clients/<client-name>/aeo-visibility-reports/history.csv` with the run summary row.

## Scheduling

```bash
# Monthly on the 1st at 8am
0 8 1 * * node run_skill.js aeo-visibility-monitor --client <client-name>
```

## Cost

| Component | Cost per run |
|-----------|-------------|
| First-time profile | ~$0.50 |
| Full visibility check (100 queries × 4 engines) | $10-30 |
| Delta analysis (LLM reasoning) | ~$0.50-1 |
| **Total per monthly run** | **~$11-32** |

## Environment Variables Required

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
PERPLEXITY_API_KEY=...
```

## Tools Required

- **Upstream skill:** `aeo-visibility`
- API keys for all 4 engines (see above)

## Trigger Phrases

- "Run the monthly AEO visibility check"
- "How has our AI search visibility changed?"
- "Are we gaining or losing ground in AI answer engines?"
- "Set up AEO monitoring for [client]"
