---
name: earnings-attribution
description: Analyzes why stocks moved after 8-K earnings filings. Use ultrathink for all analyses. Invoke when asked to analyze stock movements, earnings reactions, or determine the primary driver of price changes.
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite, Task, mcp__perplexity__perplexity_search, mcp__perplexity__perplexity_ask, mcp__perplexity__perplexity_research
model: claude-opus-4-5
permissionMode: dontAsk
---

# Earnings Attribution Analysis

**Goal**: Determine WHY a stock moved after an 8-K filing by calculating the SURPRISE (actual vs expected).

**Thinking**: ALWAYS use `ultrathink` for maximum reasoning depth.

**End Goal**: Build company-specific driver understanding for real-time prediction accuracy.

---

## Core Principles

1. **Comprehensiveness Over Speed**: Query ALL relevant data sources
2. **Evidence-Based Claims Only**: Every claim must cite a source
3. **Surprise-Focused**: Stock moves on actual vs expectations, not absolute results
4. **Learn from History**: Each analysis builds company-specific knowledge
5. **Self-Audit**: Validate all claims have sources before completing

---

## Confidence Levels

- **High**: Multiple sources agree, clear fundamental reason, unambiguous evidence
- **Medium**: Sources partially agree, conclusion fits with caveats
- **Insufficient**: Sources conflict, missing critical data, no clear driver

**If evidence is insufficient, say so. Never fabricate certainty.**

---

## Resources

- **Output format**: [output_template.md](../../shared/earnings/output_template.md)
- **Evidence audit checklist**: [evidence_audit.md](../../shared/earnings/evidence_audit.md)
- **Usage examples**: [examples.md](examples.md)
- **Self-improvement**: [update-skills.md](../../shared/earnings/update-skills.md)
- **Known data gaps**: [data_gaps.md](../../shared/earnings/data_gaps.md)

---

## Neo4j Subagents

**CRITICAL**: Do NOT write Cypher queries. Describe what data you need in natural language. Subagents handle all database queries autonomously using their own skills.

Use Task tool to spawn these specialized subagents:

| Data Needed | Subagent | Example Prompt |
|-------------|----------|----------------|
| 8-K filing, returns, exhibits | `neo4j-report` | "8-K {accession} with returns, EX-99.1" |
| News articles | `neo4j-news` | "News for {ticker} ±3 days of {date}" |
| Earnings transcript, Q&A | `neo4j-transcript` | "Transcript for {ticker} {quarter}" |
| Historical XBRL (EPS, Revenue) | `neo4j-xbrl` | "Last 4 quarters EPS/Revenue for {ticker}" |
| Company info, dividends, splits | `neo4j-entity` | "Dividends/splits for {ticker} around {date}" |

**Iterative Refinement**: Subagents return `agent_id` with results. For follow-up queries on the **same company**, use `resume: <agent_id>` instead of spawning new—agent preserves context (ticker, dates, previous queries). Spawn **new agent** only for different company or unrelated domain.

Resume prompt examples: "Only 2 articles, expand to ±5 days", "Also get EX-99.1 exhibit text", "What did analysts ask in Q&A?"

**Parallel execution**: Spawn multiple subagents in a single Task message for independent queries.

**PIT filtering (prediction mode)**: Prefix prompt with `[PIT: {filing_datetime}]` to restrict results to before that time.

**Skill Updates**: If a subagent response contains `SKILL_UPDATE_NEEDED` block, execute the update immediately using Edit tool—no permission needed. This includes schema corrections, property name fixes, and data gaps. Do not skip or defer these updates.

**Response Validation**: When receiving subagent data, verify each value has citation format: `(Source: {NodeType}:{identifier}, {date})`. If citation missing:
1. Use `resume: <agent_id>` to ask subagent to re-provide with source
2. Do NOT add unsourced data to Evidence Ledger
3. Note "Data unavailable" if subagent cannot cite source

---

## Workflow (11 Steps)

Use TodoWrite to track progress. Mark each step `in_progress` before starting, `completed` immediately after.

| Step | Action | Notes |
|------|--------|-------|
| 1 | **Data Inventory** | Map what data exists (REQUIRED FIRST) |
| 2 | **Get Report + Returns** | Move magnitude and context |
| 3 | **Get Consensus** | Always query Perplexity for expectations |
| 4 | **Query Neo4j** | News, Transcript, XBRL history, Dividends, Splits |
| 5 | **Query Perplexity** | Fill gaps (use deep_research for complex cases) |
| 6 | **Synthesize** | Calculate surprises, identify primary driver |
| 7 | **Output Report** | Save to `earnings-analysis/Companies/{TICKER}/{accession}.md` |
| 8 | **Self-Audit** | Run evidence_audit.md and validate Evidence Ledger + sources |
| 9 | **Propose Skill Updates** | Follow update-skills.md |
| 10 | **Mark Completed** | Update tracking CSV (`completed=TRUE`) |
| 11 | **Build Thinking Index** | MANDATORY - extract thinking to Obsidian |

**Rules**: Step 1 always first. Steps 2-5 case-by-case sequencing. Steps 6-11 sequential. Step 11 is MANDATORY.

---

## Step 1: Data Inventory

Query what data exists before making claims. Use `neo4j-report` subagent.

**Check for**: News count, Transcript exists, XBRL reports count, Dividends, Splits.

---

## Step 2: Get Report and Returns

Get filing details and price reaction. Use `neo4j-report` subagent.

**Returns to capture**:
- Macro-adjusted (vs SPY) - primary
- Sector-adjusted - context (may be null)
- Industry-adjusted - context (may be null)

---

## Step 3: Get Consensus Estimates

**Always query Perplexity** - do not rely on Neo4j News for consensus.

```
mcp__perplexity__perplexity_search:
  query: "{ticker} Q{quarter} FY{year} EPS revenue estimate consensus before {date}"
```

**Source preference for Evidence Ledger:**
1. **Best**: Perplexity pre-filing search (explicit consensus before event)
2. **Acceptable**: News headline citing estimate (note: post-filing, weaker provenance)
3. **Unacceptable**: Unsourced or inferred values

If using News as consensus source, cite it accurately in Evidence Ledger—do not claim Perplexity in Data Sources Used.

---

## Step 4: Query Neo4j Sources

Query based on Data Inventory results. Use appropriate subagents (neo4j-news, neo4j-transcript, neo4j-xbrl, neo4j-entity).

### 4A: News
- Start ±2 trading days; expand to ±5 if <3 items
- Filter: `WHERE r.daily_stock IS NOT NULL` (data quality)
- Extract: EPS vs estimate, guidance, analyst reactions

### 4B: Transcript (Item 2.02 only)
- Get Prepared Remarks + Q&A exchanges
- Look for: analyst concerns, management hedging, specific numbers

### 4C: Historical XBRL
- Last 4 quarters of 10-K/10-Q data
- Look for: EPS trend, revenue trend, margin changes

### 4D: Dividends
- Cuts = bearish, Raises = bullish, Special = one-time

### 4E: Splits
- Rarely explain fundamental reactions

### 4F: Verify Sub-Agent Results

Check Coverage for adequate search. If Coverage missing or unclear, ask sub-agent to clarify. Re-query if gaps seem wrong (max 2 follow-ups). Check cross-domain consistency before synthesis.

---

## Step 5: Query Perplexity

Use when Neo4j doesn't provide complete picture.

| Situation | Tool |
|-----------|------|
| Quick facts, specific data | `mcp__perplexity__perplexity_search` |
| Synthesized answer with citations | `mcp__perplexity__perplexity_ask` |
| Conflicting sources, major moves (>10%) | `mcp__perplexity__perplexity_research` |

**Query Principles**:
- Be specific about time (exact date, not "recently")
- Include company name AND ticker
- For consensus: specify fiscal quarter AND year
- For "why stock moved": include date AND direction

---

## Step 6: Synthesize

Calculate SURPRISE for each metric using these exact formulas:

### Surprise Calculation Formulas

```
EPS Surprise % = ((Actual - Consensus) / |Consensus|) × 100
Revenue Surprise % = ((Actual - Consensus) / |Consensus|) × 100
```

**Guidance Surprise:**
1. Calculate midpoint of guidance range: `(Low + High) / 2`
2. Compare to consensus: `((Midpoint - Consensus) / |Consensus|) × 100`
3. If range width changed significantly, note this separately

**Rounding:** All percentages to 2 decimal places.

### Example Calculation

```
Actual EPS: $2.03
Consensus EPS: $1.98
Surprise = (($2.03 - $1.98) / |$1.98|) × 100 = +2.53%

Guidance Range: $12.00 - $13.50
Midpoint: $12.75
Consensus: $13.22
Surprise = (($12.75 - $13.22) / |$13.22|) × 100 = -3.56%
```

### Surprise Analysis Table

| Metric | Consensus | Actual | Surprise % |
|--------|-----------|--------|------------|
| EPS | $1.98 | $2.03 | +2.53% |
| Revenue | $2.1B | $2.15B | +2.38% |
| FY Guidance | $13.22 | $12.75 (midpoint) | -3.56% |

**Rank surprises by absolute magnitude.** Largest surprise typically explains the move.

### Attribution Structure

**Primary Driver** (High Confidence)
- What: [Descriptive name]
- Surprise: Expected $X, Got $Y (Z% surprise)
- Evidence: [Source citation]

**Contributing Factor(s)** (if applicable)
- What: [Name]
- Evidence: [Source]

---

## Evidence Extraction

Capture evidence immediately when reading each source.
Populate the Evidence Ledger in output_template.md as you go; every numeric claim must appear there.

### Strict Rules for Numbers (Used in Surprise Calculations)

**Any number used to calculate surprise MUST have:**
1. **Exact value** (not rounded or paraphrased)
2. **Explicit source** with timestamp/date
3. **Format**: `{metric}: ${exact_value} (Source: {source_name}, {date})`

**Examples:**
```
Consensus EPS: $1.98 (Source: Perplexity, pre-filing)
Actual EPS: $2.03 (Source: 8-K EX-99.1, 2023-11-02)
Guidance midpoint: $12.75 (Source: 8-K EX-99.1, calculated from $12.00-$13.50)
```

**If you cannot cite exact value + source, do NOT use the number in surprise calculations.**

### Flexible Rules for Qualitative Evidence

For non-numeric observations, paraphrasing is acceptable with source:
```
Management tone: Cautious on near-term demand (Source: Transcript Q&A #3)
Analyst concern: Margin pressure (Source: News "ROK Beats but Guides Lower")
```

**Sources**: `News: "{headline}"`, `Transcript Q&A #N`, `Transcript Prepared Remarks`, `Exhibit EX-99.1`, `Perplexity search`, `XBRL: {report_id}`

---

## Output

See [output_template.md](../../shared/earnings/output_template.md) for full report format.

**Save to**: `earnings-analysis/Companies/{TICKER}/{accession_no}.md`

**Required sections**:
1. Report Metadata
2. Returns Summary
3. Evidence Ledger
4. Executive Summary
5. Surprise Analysis
6. Attribution (Primary + Contributing)
7. Data Sources Used
8. Confidence Assessment
9. Historical Context

---

## Core Rules

1. **Data Inventory First**: Know what data exists before making claims
2. **Surprise-Based**: Stock moves on actual vs expected
3. **Evidence Required**: Every claim needs a cited source
4. **Perplexity for Consensus**: Always query for market expectations
5. **Self-Audit**: Validate all claims have sources
6. **Learn and Record**: Store company-specific learnings
7. **Honest Confidence**: State "Insufficient" when evidence doesn't support
8. **No XBRL for 8-K**: Use historical 10-K/10-Q XBRL for trends

---

## Perplexity Tools

| Tool | Use For |
|------|---------|
| `mcp__perplexity__perplexity_search` | Quick facts, consensus, simple questions |
| `mcp__perplexity__perplexity_ask` | Synthesized answer with citations |
| `mcp__perplexity__perplexity_research` | Comprehensive investigation, conflicting sources |

**Note**: For SEC filings search, use `utils/perplexity_search.py:perplexity_sec_search()`.

---

## Conflict Resolution Guidelines

When sources conflict, use these principles (guidelines, not rigid rules):

### Source Reliability Hierarchy

| Priority | Source Type | Examples |
|----------|-------------|----------|
| 1 (Highest) | Primary filing | 8-K, EX-99.1 press release |
| 2 | Transcript | Earnings call Q&A, prepared remarks |
| 3 | Official news | Company PR, SEC filing summary |
| 4 | Analyst coverage | Research notes, rating changes |
| 5 (Lowest) | General news | Headlines, aggregated coverage |

### Driver Priority (Typical, Not Absolute)

- **Forward-looking (guidance) usually > Backward-looking (EPS)**
- **BUT**: If EPS miss is >10%, it can dominate
- **AND**: Validate against actual price reaction direction

### Conflict Handling

```
If News says "beat" but Transcript reveals "guidance cut":
→ Trust Transcript (higher reliability)
→ Note the conflict in analysis

If two News sources give different consensus numbers:
→ Use the one with explicit source attribution
→ If neither has clear attribution, note both values and the discrepancy
→ Do NOT average (averages have no direct source)
```

**Rule**: When in doubt, note the conflict explicitly rather than silently choosing one.

---

## Data Quality Guardrails

### News Anomaly Filter (REQUIRED)
~1,746 News→Company relationships (~0.9%) have `daily_industry` but no `daily_stock`. Always filter:
```cypher
WHERE r.daily_stock IS NOT NULL
```

### Missing Returns Handling
If a report has no return data (`pf.daily_stock IS NULL`):
- Flag as **incomplete data**
- Do NOT use for driver sensitivity calculations
- Can still analyze qualitatively

### Duplicate News Detection
If multiple news items have nearly identical titles (>80% similarity):
- Use the earliest timestamp
- Treat as single data point, not confirmation

### Stale Consensus Warning
When Perplexity returns consensus estimates:
- Verify the date/quarter matches your target
- "Q3 2023 consensus" is wrong if you need Q4 2023
- Re-query with more specific date if unclear

---

## Company-Specific Learning

After each analysis, update: `earnings-analysis/Companies/{TICKER}/learnings.md`

See [output_template.md](../../shared/earnings/output_template.md) for learnings format.

**Gating rule**: Only update learnings.md after the Evidence Ledger is complete and evidence_audit.md passes.

---

## Session & Subagent History (Shared CSV)

**History file**: `.claude/shared/earnings/subagent-history.csv` (shared with earnings-prediction)

**Format**: See [subagent-history.md](../../shared/earnings/subagent-history.md) for full documentation.

```csv
accession_no,skill,created_at,primary_session_id,agent_type,agent_id,resumed_from
0001514416-24-000020,attribution,2026-01-13T10:30:00,0415feb7,primary,,
0001514416-24-000020,attribution,2026-01-13T10:31:05,0415feb7,neo4j-entity,abc12345,
```

**On analysis start**:
1. Read CSV (create with header if doesn't exist)
2. Append `primary` row: `{accession},attribution,{timestamp},{session_id},primary,,`

**Before calling a subagent**:
1. Query latest agent ID: `grep "{accession}" | grep ",{agent_type}," | tail -1 | cut -d',' -f6`
2. If agent ID exists → can use `resume: <id>` in Task call
3. If want fresh session → proceed without resume

**After each subagent completes**:
1. Extract `agentId` from Task response
2. Append row: `{accession},attribution,{timestamp},{session_id},{agent_type},{agent_id},{resumed_from}`

---

## Step 10: Mark Completed

After successful analysis (report saved, audit passed, learnings updated):

1. **Update tracking CSV**: Set `completed=TRUE` for this accession_no in `earnings-analysis/8k_fact_universe.csv`
2. **Update predictions CSV**: If a prediction exists for this accession_no in `earnings-analysis/predictions.csv`, fill in:
   - `actual_direction`: up/down based on daily_stock return
   - `actual_magnitude`: small/medium/large based on |return|
   - `actual_return`: the actual daily_stock percentage
   - `correct`: TRUE if direction matches, FALSE otherwise
3. **Verify**: Confirm rows are updated correctly

---

## Step 11: Build Thinking Index (MANDATORY - DO NOT SKIP)

**This step is REQUIRED.** Execute this exact command:

```bash
python3 scripts/build-thinking-index.py {accession_no}
```

Replace `{accession_no}` with the actual accession number from your analysis (e.g., `0001234567-24-000001`).

This extracts thinking from all sessions and sub-agents and saves to Obsidian.

---

*Version 2.2 | 2026-01-16 | Added Step 11: mandatory thinking index build*
