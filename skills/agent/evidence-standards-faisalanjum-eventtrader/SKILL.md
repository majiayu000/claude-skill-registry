---
name: evidence-standards
description: Evidence citation and domain scope standards for Neo4j subagents. Prevents hallucination and ensures audit trail.
user-invocable: false
---

# Evidence Standards for Neo4j Subagents

## Domain Scope

Each agent queries ONLY its designated node types:

| Agent | Allowed Nodes | NOT Allowed |
|-------|---------------|-------------|
| neo4j-report | Report, ExtractedSectionContent, ExhibitContent | News, Transcript, Fact |
| neo4j-news | News | Report, Transcript, Fact |
| neo4j-transcript | Transcript, QAExchange, PreparedRemark | Report, News, Fact |
| neo4j-xbrl | Fact, Concept, Dimension, Member | Report, News, Transcript |
| neo4j-entity | Company, Sector, Industry, Dividend, Split | Report, News, Fact |

**If asked for data outside your domain**: Respond "This requires [correct-agent] agent" and do not query.

---

## Evidence Citation Format

All returned data MUST include source verification.

**Template**: `{metric}: {value} (Source: {NodeType}:{identifier}, {date})`

### Examples by Domain

**Report**:
```
Actual EPS: $2.03 (Source: Report:0001104659-24-098778/EX-99.1, 2024-09-11)
Filing type: 8-K (Source: Report:0001104659-24-098778, form_type)
Daily return: +84.14% (Source: Report:0001104659-24-098778, pf.daily_stock)
```

**News**:
```
Headline: "PLCE beats estimates by 127%" (Source: News:benzinga-456789, 2024-09-11)
Consensus EPS: $-0.19 (Source: News:streetinsider-123, 2024-09-10)
```

**Transcript**:
```
CEO guidance: "Expect continued margin expansion" (Source: Transcript:PLCE-Q2-FY2024/PreparedRemarks, 2024-09-12)
Analyst question: "What about inventory levels?" (Source: Transcript:PLCE-Q2-FY2024/QA#3, 2024-09-12)
```

**XBRL**:
```
Q2 Revenue: $345.6M (Source: Fact:us-gaap:Revenues/10-Q:0001234567-24-000123, 2024-06-30)
Basic EPS: $0.85 (Source: Fact:us-gaap:EarningsPerShareBasic/10-Q:0001234567-24-000123, 2024-06-30)
```

**Entity**:
```
Dividend: $0.50/share (Source: Dividend:PLCE/2024-09-15, declaration_date)
Stock split: 2:1 (Source: Split:PLCE/2024-01-15, execution_date)
Market cap: $128M (Source: Company:PLCE, mkt_cap)
```

---

## Core Rules

1. **No source = Don't return the data.** If you cannot cite the exact Neo4j node and field, do not include the value. State what data is unavailable instead.

2. **Exact values only.** Return database values as-is. No rounding, no paraphrasing, no approximations. `$2.03` not `~$2`, `84.14%` not `about 84%`.

Example:
- WRONG: "EPS was $2.03"
- RIGHT: "Actual EPS: $2.03 (Source: Report:0001104659-24-098778/EX-99.1, 2024-09-11)"
- RIGHT: "EPS data not found in Report nodes for this accession."

---

## Verification

The main agent can verify any citation by:
1. Re-querying the cited node type and identifier
2. Checking the field/date matches
3. Confirming the value

This ensures audit trail and prevents hallucination.

---

## Operating Protocol

**Thoroughness:** Exhaust your domain. If sparse (<3 items for news, or expected data missing for other domains), expand search. Surface conflicts with both sources—don't resolve.

**PIT:** If `[PIT: datetime]` specified, all results must predate it.

**Response:**
```
## Results
<citations per format above; conflicts show both values>

## Coverage (required)
Must include: what searched, count found, gaps, PIT status.
Example: Searched: ±5 days, fulltext "guidance" | Found: 7 | Gaps: no consensus | PIT: n/a
(Natural language variants acceptable if all elements present)
```
