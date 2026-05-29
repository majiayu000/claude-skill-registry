---
name: guidance-inventory
description: Builds and maintains cumulative guidance inventory for a company. Use when collecting historical guidance, updating guidance after earnings, preparing context for prediction/attribution workflows, or when user asks about company outlook, earnings guidance, management expectations, forward forecasts, or FY/quarterly targets.
allowed-tools: Read, Write, Grep, Glob, Skill, mcp__neo4j-cypher__read_neo4j_cypher, mcp__perplexity__perplexity_search, mcp__alphavantage__EARNINGS_ESTIMATES
model: claude-opus-4-5-20251101
permissionMode: dontAsk
---

# Guidance Inventory

Builds cumulative guidance state per company. This is a **DATA skill** (pure collection) — analysis happens in attribution.

**Thinking**: ALWAYS use `ultrathink` for maximum reasoning depth when extracting and classifying guidance.

**Input**: `{ticker} {accession_no} {quarter}` (e.g., `AAPL 0001193125-24-000001 2`)

**Critical**: Every guidance entry has TWO dates — **must track BOTH**:
- **Given Date**: When management issued the guidance (citation timestamp)
- **Period Covered**: What fiscal period the guidance is FOR (Q2 FY25, FY25, etc.)

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Arguments](#arguments)
3. [Workflow](#workflow)
   - Step 1: Determine Scope
   - Step 2: Get Company Fiscal Profile
   - Step 3: Gather Guidance
   - Step 4: Extract Guidance Entries
   - Step 5: Classify Action
   - Step 6: Write Output
4. [Guidance Types to Capture](#guidance-types-to-capture)
5. [Period Types](#period-types)
6. [10 Critical Capture Items](#10-critical-capture-items-must-have)
7. [Citation Requirements](#citation-requirements-non-negotiable)
8. [Supersession Tracking](#supersession-tracking)
9. [File Lifecycle](#file-lifecycle)
10. [Integration with Other Skills](#integration-with-other-skills)
11. [What This Is NOT](#what-this-is-not)
12. [Invocation Examples](#invocation-examples)
13. [Error Handling](#error-handling)
14. [Reference Files](#reference-files)
15. [Requirements Checklist](#requirements-checklist)
16. [Data Model Reference](#data-model-reference)

---

## Quick Reference

| Field | Value |
|-------|-------|
| **Output** | `earnings-analysis/Companies/{TICKER}/guidance-inventory.md` |
| **Mode** | Cumulative (grows over time, never overwrites) |
| **Trigger** | Q1 = full historical build; Q>=2 = updated by attribution |

## Arguments

```
$ARGUMENTS = "{ticker} {accession_no} {quarter}"
```

- `ticker`: Company symbol (e.g., AAPL)
- `accession_no`: 8-K accession being processed
- `quarter`: Which quarter (1, 2, 3, 4) — determines historical depth

## Workflow

### Step 1: DETERMINE SCOPE

```
IF quarter = 1:
    depth = "all"        # All available historical guidance
    action = "BUILD"     # Create new inventory
ELSE:
    depth = "3 months"   # From previous r.created to current r.created
    action = "UPDATE"    # Append to existing inventory
```

### Step 2: GET COMPANY FISCAL PROFILE

Query Neo4j for fiscal year end:
```cypher
MATCH (c:Company {ticker: $ticker})<-[:PRIMARY_FILER]-(r:Report {formType: '10-K'})
RETURN r.periodOfReport
ORDER BY r.created DESC LIMIT 1
```

The `periodOfReport` reveals FYE (e.g., `2024-09-30` = September FYE).

Build fiscal calendar — see [FISCAL_CALENDAR.md](FISCAL_CALENDAR.md).

### Step 3: GATHER GUIDANCE

**Source Priority** (query in order):

| Priority | Source | Skill | Reliability | Best For |
|----------|--------|-------|-------------|----------|
| 1 | 8-K EX-99.1 press release | `/neo4j-report` | Highest | Official numbers |
| 2 | Earnings transcript | `/neo4j-transcript` | High | Context, nuance, Q&A |
| 3 | Alpha Vantage | `/alphavantage-earnings` | High | Consensus estimates |
| 4 | News | `/neo4j-news` | Medium | Reactions, analyst commentary |
| 5 | Perplexity | `/perplexity-search` | Medium | Gap filling, historical |
| 6 | WebSearch | `WebSearch` | Medium | SEC filings, IR pages |

See [QUERIES.md](QUERIES.md) for specific queries.

### Step 4: EXTRACT GUIDANCE ENTRIES

For each guidance found, capture ALL of these fields:

```yaml
- period_type: quarter | annual | half | long-range
  fiscal_year: 2025
  fiscal_quarter: 2              # null for annual
  calendar_start: "2025-01-01"   # Derived from FYE
  calendar_end: "2025-03-31"     # Derived from FYE
  status: future | current | past

  metric: "EPS"
  value_low: 1.50
  value_high: 1.70
  value_mid: 1.60
  unit: "USD"
  basis: "non-GAAP adjusted"     # CRITICAL: track definition

  given_date: "2025-02-05"       # When guidance was issued
  source_type: "8-K"
  source_id: "0001234567-25-000001"
  quote: "We expect Q2 EPS of $1.50 to $1.70"
  page_or_section: "Page 2, Outlook"

  action: INITIAL | RAISED | LOWERED | MAINTAINED | NARROWED | WIDENED | WITHDRAWN
  prior_value_mid: 1.55          # If action != INITIAL
  revision_pct: +3.2%            # (new_mid - prior_mid) / prior_mid
```

### Step 5: CLASSIFY ACTION

Compare to prior guidance for same metric/period:

| Condition | Action | Signal |
|-----------|--------|--------|
| No prior guidance exists | INITIAL | Sets anchor |
| Midpoint increased | RAISED | Bullish |
| Midpoint decreased | LOWERED | Bearish |
| Midpoint same, range narrower | NARROWED | More certainty |
| Midpoint same, range wider | WIDENED | More uncertainty |
| Explicitly reiterated unchanged | MAINTAINED | Neutral (can disappoint if beat expected) |
| Guidance removed | WITHDRAWN | Usually very bearish |

#### Anchor Tracking & Revision Math

**Q1 establishes the "anchor"** for annual guidance. Track cumulative revision:

```
Q1 FY25 call: "FY25 EPS $12.00-$13.50" (anchor midpoint: $12.75)
Q2 FY25 call: "FY25 EPS $12.50-$13.50" (revision: +$0.25 midpoint, +2.0% from anchor)
Q3 FY25 call: "FY25 EPS $13.00-$14.00" (cumulative: +$0.75 from anchor, +5.9%)
```

**Revision calculation**: `((new_mid - anchor_mid) / anchor_mid) × 100`

#### One Call → Multiple Periods

Each earnings call typically addresses MULTIPLE periods — track separately:

```
Q1 FY25 Earnings Call (Feb 2025):
├── Q1 FY25 (Oct-Dec 2024): ACTUALS REPORTED      ← past period
├── Q2 FY25 (Jan-Mar 2025): NEW GUIDANCE          ← future (quarterly)
├── FY25 Full Year:         GUIDANCE UPDATED      ← current (annual)
└── Sometimes: FY26:        PRELIMINARY OUTLOOK   ← future (next year preview)
```

### Step 6: WRITE OUTPUT

Use template in [OUTPUT_TEMPLATE.md](OUTPUT_TEMPLATE.md).

**Critical Rules**:
- Never overwrite existing content — always APPEND
- Each update gets a timestamped section header
- Include evidence ledger entry for every data point

---

## Guidance Types to Capture

### Financial - Hard Numbers
| Metric | Common Variants |
|--------|-----------------|
| EPS | GAAP, Non-GAAP, Adjusted, Diluted |
| Revenue | Total, By Segment, Organic vs Reported |
| Gross Margin | % |
| Operating Margin | GAAP, Non-GAAP |
| Net Income | GAAP, Adjusted |
| Free Cash Flow | Operating CF minus CapEx |
| CapEx | Total, By Category |

### Financial - Soft/Qualitative
- "Double-digit growth"
- "Margin expansion of 50-100 bps"
- "Flat year-over-year"
- "Modest improvement"

### Operational (Non-Financial)- few examples only, non exhasutive
- Units / Subscribers / DAUs / MAUs
- Store openings / closings
- Headcount changes
- Market share targets
- Product launch timing

---

## Period Types

| Period Type | Covers | Typical Pattern |
|-------------|--------|-----------------|
| **Quarterly** | Single quarter (3 months) | Given for next quarter only |
| **Annual** | Full fiscal year | Given in Q1, updated each quarter |
| **Half-Year** | H1 or H2 (6 months) | Some international companies |
| **Long-Range** | Multi-year targets | "2027 targets", analyst days |

---

## 10 Critical Capture Items (MUST-HAVE)

### A. Guidance vs Consensus Gap
```
Company Guidance: "FY25 EPS $12.00-$13.50" (mid: $12.75)
Street Consensus: "$13.22"
Gap: -3.6% (company below street) → bearish signal
```
Track BOTH separately.

### B. Metric Definition Drift
```
Q1: "Adjusted EPS excluding stock comp: $3.50"
Q2: "Adjusted EPS: $3.40"  ← Did definition change?
```
Note basis in every entry.

### C. Segment-Level Guidance
```
Total Revenue: $10B
  - Cloud: $4B (guidance given)
  - Hardware: $6B (no guidance)
```
Capture both consolidated AND segment if available.

### D. FX / Constant Currency
```
"Revenue growth 8-10% constant currency"
"Revenue growth 5-7% as reported"
```
Note which basis. FX assumption is a condition.

### E. Conditional Guidance
```
"Guidance assumes no further Fed rate increases"
"Contingent on closing the Acme acquisition in Q3"
```
Track assumptions — they can invalidate guidance.

### F. Pre-Announcements (Mid-Quarter Updates)
```
8-K filed mid-quarter: "Lowering Q2 guidance due to..."
```
These are often most market-moving. Query for 8-K Item 7.01 between earnings.

### G. Guidance Policy
```
"Company does not provide quarterly guidance"
```
Track if company guides at all — absence is informative.

### H. Historical Accuracy (Beat/Miss Pattern)
```
Last 8 quarters: Beat guidance 7/8 times
Average beat: +3.2%
Pattern: "Sandbagger" - guides low, beats high
```
This is predictive signal. Track in company profile section.

### I. Comparable Periods
```
FY25 Q2 guidance vs FY24 Q2 actual (YoY)
FY25 Q2 guidance vs FY25 Q1 actual (Sequential)
```
Link guidance to historical actuals for context.

### J. Range Asymmetry
```
Range: $12.00-$14.00, Midpoint: $13.00
Low end = -8% from mid, High end = +8% from mid → symmetric
Low end = -2%, High end = +14% → asymmetric bullish
```
Range shape signals management confidence.

---

## Citation Requirements (Non-Negotiable)

Every guidance entry MUST have:
- `source_type`: 8-K, Transcript, News, Perplexity
- `source_id`: Accession number or URL
- `given_date`: When guidance was issued (ISO format)
- `quote`: Exact quote or close paraphrase
- `page_or_section`: Where in source (if applicable)

**No citation = No entry**

---

## Supersession Tracking

When guidance is updated, the old entry is **superseded** (not deleted):

```yaml
# Entry 1 (superseded)
entry_id: "FY25-EPS-001"
value: "$6.60-$7.30"
given_date: "2024-11-01"
status: superseded
superseded_by: "FY25-EPS-002"

# Entry 2 (current)
entry_id: "FY25-EPS-002"
value: "$6.80-$7.40"
given_date: "2025-02-05"
status: active
superseded_by: null
```

This preserves the revision history chain.

---

## File Lifecycle

```
Q1 (First Report for Company):
    earnings-orchestrator
        ↓
    /guidance-inventory BUILD
        ↓
    Creates: {TICKER}/guidance-inventory.md (from all historical)

Q2-Q4 (Subsequent Reports):
    earnings-orchestrator
        ↓
    /guidance-inventory UPDATE
        ↓
    Appends: new guidance from current filing

Real-time (Future - Deferred):
    Background process monitors mid-quarter 8-Ks
        ↓
    Auto-triggers UPDATE
```

---

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| **earnings-orchestrator** | CALLS this skill for both BUILD (q=1) and UPDATE (q>=2) |
| **earnings-prediction** | READS guidance-inventory to know prior expectations |
| **earnings-attribution** | READS guidance-inventory for surprise calculation |

**Note**: This skill is called from orchestrator (Layer 1, forked). Task tool is BLOCKED.

---

## What This Is NOT

- **NOT consensus estimates storage** — consensus lives in prediction/attribution reports
- **NOT met/missed analysis** — that's attribution's job
- **NOT forward guidance interpretation** — just data collection
- **Pure inventory only** — no analysis, no recommendations

---

## Invocation Examples

### BUILD mode (Q1 - Initial)
```
/guidance-inventory AAPL 0001193125-24-000001 1
```
Creates full historical inventory from all available 8-Ks and transcripts.

### UPDATE mode (Q2-Q4)
```
/guidance-inventory AAPL 0001193125-24-000123 2
```
Appends only new guidance from the current quarter's filing.

### From orchestrator
```
Skill: guidance-inventory
Args: "GBX 0001193125-23-002899 1"
```
Called automatically by earnings-orchestrator for each 8-K.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **No 8-K found** | Log warning, return empty inventory section |
| **No EX-99.1 exhibit** | Try transcript, then Perplexity fallback |
| **No guidance in filing** | Note "No forward guidance provided" in inventory |
| **Neo4j query fails** | Retry once, then log error and continue with other sources |
| **Company doesn't provide guidance** | Record in Guidance Policy field, don't fabricate |
| **FYE not determinable** | Query Perplexity, assume December if no data |
| **Ambiguous period reference** | Note ambiguity in quote, use best interpretation |

**Principle**: Never fabricate guidance. If not found, document absence.

---

## Reference Files

- [QUERIES.md](QUERIES.md) — Neo4j and Perplexity queries
- [OUTPUT_TEMPLATE.md](OUTPUT_TEMPLATE.md) — File format template
- [FISCAL_CALENDAR.md](FISCAL_CALENDAR.md) — FYE handling and calendar mapping

---

## Input from guidance-extract (guidance.csv)

The `guidance-extract` agent outputs to `earnings-analysis/Companies/{TICKER}/guidance.csv`. This file uses an 18-field pipe-delimited format (+ quarter context = 19 fields).

### Field Mapping from guidance.csv

| guidance.csv Field | Type | Maps to GuidanceEntry |
|--------------------|------|------------------------|
| quarter | string | Context (which earnings call) |
| period_type | enum | `period.period_type` |
| fiscal_year | int | `period.fiscal_year` |
| fiscal_quarter | int/`.` | `period.fiscal_quarter` (`.` = null for annual) |
| segment | string | Additional context for segment-level guidance |
| metric | string | `metric` |
| low | float/`.` | `value_low` |
| mid | float/`.` | `value_mid` |
| high | float/`.` | `value_high` |
| unit | string | `unit` |
| basis | string | `basis` |
| derivation | enum | New field: `explicit`, `calculated`, `point`, `implied` |
| qualitative | string/`.` | Soft guidance text when numeric not available |
| source_type | string | `source_type` |
| source_id | string | `source_id` |
| source_key | string | Which content in source (e.g., `EX-99.1`, `full`) |
| given_date | date | `given_date` |
| section | string | `page_or_section` |
| quote | string | `quote` (pipes replaced with ¦) |

### Derived Fields (computed by guidance-inventory)

| Field | How Derived |
|-------|-------------|
| `calendar_start` | From `fiscal_year` + `fiscal_quarter` + company's `fiscal_year_end_month` |
| `calendar_end` | From `fiscal_year` + `fiscal_quarter` + company's `fiscal_year_end_month` |
| `status` | Compare `calendar_end` vs current date: `future`, `current`, `past` |
| `action` | Compare to prior guidance for same metric/period: `INITIAL`, `RAISED`, `LOWERED`, etc. |
| `entry_id` | Generate unique ID: `{metric}-{period_type}-{fiscal_year}-{sequence}` |

### Derivation Field Interpretation

| derivation | Meaning | Numeric Fields |
|------------|---------|----------------|
| `explicit` | All three values stated by management | low, mid, high populated |
| `calculated` | mid = (low+high)/2 computed by agent | low, high from source; mid calculated |
| `point` | Single value: "around $15B" | low = mid = high (same value) |
| `implied` | Qualitative only, no numbers | low, mid, high = `.`; qualitative populated |

### Handling Qualitative Guidance

When `derivation=implied`, the `qualitative` field contains non-numeric guidance:
- "double-digit" → Growth expectation without specific number
- "low to mid single digits" → Range expressed qualitatively

These entries should be captured in guidance-inventory with the qualitative text preserved in the `quote` field and noted in analysis context.

---

## Requirements Checklist

| Requirement | How Addressed |
|-------------|---------------|
| Period association | Every entry has period_type, fiscal_year, fiscal_quarter |
| Quarter vs Annual | `period_type` field distinguishes |
| Fiscal year tracking | `fiscal_year` + company `fiscal_year_end_month` |
| Calendar mapping | `calendar_start` / `calendar_end` derived from FYE |
| Future vs Past | `status` field: future / current / past |
| Supersession | `superseded_by` links to newer guidance entry |
| Anchor tracking | Q1 annual guidance marked, revisions calc'd vs anchor |
| Both dates tracked | `given_date` (citation) + period fields (target) |

---

## Data Model Reference

```python
@dataclass
class GuidancePeriod:
    """Represents a fiscal period that guidance covers."""
    period_type: Literal["quarter", "annual", "half", "long-range", "other"]
    fiscal_year: int                    # e.g., 2025
    fiscal_quarter: Optional[int]       # 1-4 for quarters, None for annual
    calendar_start: date                # Derived from company FYE
    calendar_end: date                  # Derived from company FYE

    def status(self, as_of: date) -> Literal["future", "current", "past"]:
        if self.calendar_end < as_of:
            return "past"
        elif self.calendar_start <= as_of <= self.calendar_end:
            return "current"
        else:
            return "future"

@dataclass
class GuidanceEntry:
    """A single guidance data point."""
    entry_id: str                       # e.g., "FY25-EPS-001"
    period: GuidancePeriod
    metric: str                         # "EPS", "Revenue", etc.
    value_low: Optional[float]
    value_mid: Optional[float]
    value_high: Optional[float]
    unit: str                           # "USD", "%", "B USD"
    basis: str                          # "GAAP", "non-GAAP adjusted"

    # Citation (required)
    source_type: str                    # "8-K", "Transcript", "News"
    source_id: str                      # accession or URL
    given_date: date                    # When guidance was issued
    quote: str                          # Exact quote
    page_or_section: Optional[str]      # Where in source

    # State
    action: Literal["INITIAL", "RAISED", "LOWERED", "MAINTAINED", "NARROWED", "WIDENED", "WITHDRAWN"]
    status: Literal["active", "superseded", "withdrawn"]
    superseded_by: Optional[str]        # Entry ID of newer guidance
```

---

*Version 1.6 | 2026-01-17 | Added Input line for quick reference*
