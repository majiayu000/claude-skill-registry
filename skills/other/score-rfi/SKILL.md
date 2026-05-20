---
context: fork
description: Score vendor RFI responses using a 0-3 rubric with SQLite storage
model: sonnet
---

# /score-rfi

Score vendor RFI responses stored in SQLite databases using a standardised 0-3 rubric.

## Usage

```
/score-rfi <vendor-name>
/score-rfi pwc
/score-rfi accenture
/score-rfi ibm
```

## Prerequisites

Before scoring, ensure the vendor's CSV has been converted to SQLite:

```bash
# Convert CSV to SQLite (see /csv-to-sql skill)
node scripts/csv-to-sqlite.js "Inbox/<vendor>-rfi-responses.csv" --start-row <n> --fts --verbose
```

## Scoring Rubric (0-3 Scale)

| Score | Rating | Qualitative Assessment                                                                                           |
| ----- | ------ | ---------------------------------------------------------------------------------------------------------------- |
| **3** | High   | Strong proven experience; clear, detailed answer demonstrating deep understanding; high confidence in capability |
| **2** | Medium | Some capability demonstrated; potential but unproven or limited evidence; moderate risk                          |
| **1** | Low    | Insufficient evidence; generic or superficial response; does not address specifics; high risk                    |
| **0** | Zero   | Not demonstrated at all; no evidence or response; very high risk                                                 |

### Scoring Criteria

When evaluating responses, consider:

1. **Domain Specificity** - Does the response demonstrate understanding of your industry operations and relevant regulations?
2. **Organisation Context** - Does it show awareness of your organisation's scale, operations, existing systems?
3. **Technical Depth** - Are specific technologies, frameworks, methodologies named with concrete examples?
4. **Proven Experience** - Are past implementations cited? Client references? Metrics?
5. **Risk Indicators** - Are there red flags like "we will learn", "to be determined", "partner with"?

### Score Format

All scores MUST be written in this format:

```
[score] - [brief reason for score]
```

Examples:

- `3 - Strong domain-specific response with mature frameworks; explicit regulatory references; relevant experience cited`
- `2 - Solid methodology but no domain-specific examples; generic enterprise approach`
- `1 - Insufficient evidence of capability; significant capability gap`
- `0 - No response provided`

## Instructions

### Phase 1: Database Setup

1. **Verify database exists**:

   ```bash
   sqlite3 .data/<vendor>-rfi-scoring.db ".tables"
   ```

2. **Check schema and scorer columns**:

   ```bash
   sqlite3 .data/<vendor>-rfi-scoring.db ".schema"
   ```

3. **Identify the scorer column** (e.g., `john_smith`, `jane_doe`)

### Phase 2: Parallel Scoring

Launch sub-agents to score questions in parallel. Each agent scores ~10-12 questions.

**Agent Prompt Template:**

```
You are scoring vendor RFI responses for the Systems Integrator procurement.

**Vendor:** <vendor-name>
**Database:** .data/<vendor>-rfi-scoring.db
**Table:** <table-name>
**Scorer Column:** <scorer-column>
**Questions:** <start-id> to <end-id>

**Scoring Rubric (0-3):**
- 3 = High: Strong proven experience, detailed response, high confidence
- 2 = Medium: Some capability, potential but unproven, moderate risk
- 1 = Low: Insufficient evidence, generic response, high risk
- 0 = Zero: Not demonstrated, no evidence, very high risk

**Focus Areas:**
- Domain specificity (industry regulations and compliance)
- Organisation context awareness
- Technical depth with concrete examples
- Proven implementations and references

**Instructions:**
1. Query questions <start-id> to <end-id>
2. For each, read the question and response columns
3. Apply the rubric to score each response
4. Return results in this format:
   ID|SCORE|REASON

Example:
1|3|Strong domain-specific frameworks; compliance explicit
2|2|Solid approach but lacks specific examples

After scoring, update the database:
sqlite3 .data/<db>.db "UPDATE <table> SET <scorer_col> = '<score> - <reason>' WHERE id = '<id>';"
```

### Phase 3: Execute Scoring

1. **Launch 4 parallel agents** covering all questions (e.g., 1-11, 12-22, 23-33, 34-44)

2. **Verify updates**:
   ```bash
   sqlite3 .data/<vendor>-rfi-scoring.db -markdown -header \
     "SELECT id, <scorer_col> FROM <table> ORDER BY CAST(id AS INTEGER);"
   ```

### Phase 4: Generate Summary

1. **Query score distribution**:

   ```bash
   sqlite3 .data/<vendor>-rfi-scoring.db \
     "SELECT CAST(SUBSTR(<scorer_col>, 1, 1) AS INTEGER) as score, COUNT(*)
      FROM <table> GROUP BY score ORDER BY score DESC;"
   ```

2. **Query low scores (risks)**:

   ```bash
   sqlite3 .data/<vendor>-rfi-scoring.db -markdown -header \
     "SELECT id, SUBSTR(question, 1, 60) as question, <scorer_col>
      FROM <table>
      WHERE <scorer_col> LIKE '1 -%' OR <scorer_col> LIKE '0 -%'
      ORDER BY CAST(id AS INTEGER);"
   ```

3. **Create summary Page** using template below

### Phase 5: Create Summary Page

Create a Page note at: `Page - SI RFI Scoring - <Vendor> - <Scorer> Scores.md`

**Template:**

```markdown
---
type: Page
title: SI RFI Scoring - <Vendor> - <Scorer> Scores
created: <today>
modified: <today>
tags:
  - project/<project-name>
  - activity/evaluation
  - vendor/<vendor-lowercase>
  - workstream/rfi-scoring
confidence: high
freshness: current
source: primary
verified: true
reviewed: <today>
relatedTo:
  - "[[Project - <Project Name>]]"
  - "[[Page - SI RFI Scoring - <Vendor> Response]]"
---

# SI RFI Scoring - <Vendor> - <Scorer> Scores

Scoring assessment of <Vendor>'s response to the Systems Integrator RFI.

## Summary

| Metric           | Value            |
| ---------------- | ---------------- |
| Total Questions  | <count>          |
| Average Score    | <avg> / 3.00     |
| Score 3 (High)   | <count> (<pct>%) |
| Score 2 (Medium) | <count> (<pct>%) |
| Score 1 (Low)    | <count> (<pct>%) |
| Score 0 (Zero)   | <count> (<pct>%) |

## Key Findings

### Strengths (Score 3)

<bullet list of strength themes>

### Gaps (Score 1-2)

| ID  | Area | Score | Risk |
| --- | ---- | ----- | ---- |

<table of low-scoring questions>

### Risk Summary

<brief summary of primary risks and mitigation>

## Detailed Scores

| ID  | Question | Score | Reason |
| --- | -------- | ----- | ------ |

<full table of all scores>

## Data Source

Scores stored in SQLite database: `.data/<vendor>-rfi-scoring.db`
```

## Useful Queries

```bash
# All scores with full questions
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question, <scorer_col> FROM <table> ORDER BY CAST(id AS INTEGER);"

# Compare multiple scorers
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, scorer_1, scorer_2, scorer_3 FROM <table> ORDER BY CAST(id AS INTEGER);"

# Average score
sqlite3 .data/<db>.db \
  "SELECT ROUND(AVG(CAST(SUBSTR(<scorer_col>, 1, 1) AS REAL)), 2) FROM <table>;"

# Search responses for keyword
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question FROM <table>_fts WHERE <table>_fts MATCH 'integration';"
```

## Multi-Vendor Comparison

After scoring all vendors, create a comparison summary:

```bash
# Export each vendor's scores
sqlite3 .data/pwc-rfi.db "SELECT id, SUBSTR(scorer_col,1,1) as score FROM data;" > pwc-scores.txt
sqlite3 .data/accenture-rfi.db "SELECT id, SUBSTR(scorer_col,1,1) as score FROM data;" > accenture-scores.txt
```

Create a comparison Page: `Page - SI RFI Scoring - Vendor Comparison.md`

## Related Skills

- [[.claude/skills/csv-to-sql/SKILL.md]] - Convert CSV to SQLite database
- [[.claude/skills/csv-to-markdown/SKILL.md]] - Convert CSV to markdown table
