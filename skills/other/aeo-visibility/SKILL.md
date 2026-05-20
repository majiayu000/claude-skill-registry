---
name: aeo-visibility
description: >
  Check how visible your company is across AI answer engines (ChatGPT, Claude, Gemini, Perplexity).
  Profiles a company, generates test queries, runs visibility checks, and tracks trends over time.
tags: [seo]
---

# AEO Visibility Checker

Check how visible your company is across AI answer engines (ChatGPT, Claude, Gemini, Perplexity).

## What It Does

1. **Profile a company**: Research the company, discover competitors, generate ~100 test queries
2. **Run visibility check**: Query all 4 engines with your queries, analyze mentions/prominence/sentiment
3. **Generate reports**: Markdown report + CSV export with full metrics
4. **Track history**: Maintain historical runs to track visibility trends over time

## Usage

### 1. Profile a Client

```bash
node src/cli.js profile <client-name> [--url=https://example.com]
```

This will:
- Research the company (via web_search in production)
- Discover competitors automatically
- Generate ~100 diverse search queries
- Save to `clients/<client-name>/profile.json` and `queries.json`

**Review and edit** `queries.json` before running.

### 2. Run Full Check

```bash
node src/cli.js run <client-name>
```

Runs all queries against all 4 engines. Creates:
- `clients/<client-name>/runs/YYYY-MM-DD-HHMM/report.md` (detailed markdown report)
- `clients/<client-name>/runs/YYYY-MM-DD-HHMM/results.csv` (full data export)
- `clients/<client-name>/runs/YYYY-MM-DD-HHMM/raw-responses.json` (raw API responses)
- Updates `clients/<client-name>/history.csv` (summary of all runs)

**Cost**: ~$10-30 per full run (100 queries × 4 engines × ~$0.025-0.075/query)

### 3. Run Specific Queries (Granular)

```bash
node src/cli.js run <client-name> --queries "best AI tools" "top LLMs for coding" "AI assistants"
```

Test specific queries only (cheaper, faster).

### 4. View History

```bash
node src/cli.js history <client-name>
```

Shows all historical runs with key metrics.

## Report Contents

### Markdown Report (`report.md`)
- **Executive summary**: Total mentions, avg visibility score, top engine
- **Performance by engine**: Mention rate, prominent mentions, avg sentiment
- **Competitor comparison**: How often competitors are mentioned vs you
- **Top performing queries**: Queries where you're mentioned most
- **Missed opportunities**: Queries where competitors are mentioned but you're not

### CSV Export (`results.csv`)
Raw data with columns:
- query
- mentioned (yes/no per engine)
- prominence (high/medium/low per engine)
- sentiment (-1 to 1 per engine)
- competitors_mentioned

## Analysis Metrics

**Mentioned**: Is the company mentioned in the response at all?

**Prominence**:
- High: Mentioned in first 2 sentences (top of mind)
- Medium: Mentioned in middle of response
- Low: Mentioned at end or as footnote

**Sentiment**: -1 to 1 scale
- 1 = Very positive
- 0 = Neutral
- -1 = Negative

## Multi-Client Support

Results are saved to the workspace-level client directory (not inside the skill):

```
clients/
├── acme-corp/
│   └── aeo-visibility-reports/
│       ├── profile.json
│       ├── queries.json
│       ├── runs/
│       │   ├── 2026-02-25T02-00-00/
│       │   └── 2026-03-01T10-30-00/
│       └── history.csv
└── other-client/
    └── aeo-visibility-reports/
        └── ...
```

## Environment Variables Required

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
export PERPLEXITY_API_KEY=...
```

## Integration with OpenClaw

This skill is designed to be triggered via OpenClaw chat:

```
"Can you check our AEO visibility?"
"Run visibility check for acme-corp"
"Check how we rank for AI coding tools on answer engines"
```

OpenClaw agent will:
1. Call `profile` command if client not yet set up
2. Present generated queries for review
3. Run visibility check after approval
4. Summarize results from report

## Cost Management

- **Full run**: $10-30 (100 queries × 4 engines)
- **Granular run**: ~$0.10-0.30 per query × 4 engines
- **Profiling**: ~$0.50 (competitor discovery + query generation)

The CLI shows cost estimate before running.

## Future Enhancements

- [ ] Add more engines (Gemini Deep Research, SearchGPT)
- [ ] Weekly scheduled runs with trend alerts
- [ ] Optimize query set based on performance
- [ ] A/B test different query phrasings
- [ ] Auto-generate optimization recommendations
