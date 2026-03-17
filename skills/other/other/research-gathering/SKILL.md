---
name: research-gathering
description: Use when assembling strategic context - collects and filters research by topic with expiry management to prevent using stale data in decisions
allowed-tools: Read, Grep, Glob
---

# Research Gathering

## Purpose

Assemble relevant research context for strategic sessions:
- Collect sources by topic (competitive-analysis, pricing-strategy, etc.)
- Filter by recency and expiry dates
- Extract key insights and quotes
- Prepare citation-ready references
- Flag stale data requiring refresh

## When to Use This Skill

Activate automatically when:
- `strategy-session` workflow needs context for decision-making
- `content-drafting` workflow requires research backing
- User explicitly requests research on a topic
- Building strategic memos requiring evidence
- Planning features based on market insights

## Research Topics

**Supported strategic categories:**
- `competitive-analysis` - Competitor capabilities, positioning, pricing
- `pricing-strategy` - Pricing models, packaging, value perception
- `market-positioning` - Market trends, customer segments, messaging
- `product-strategy` - Feature prioritization, roadmap direction
- `customer-segmentation` - Audience targeting, persona development
- `growth-strategy` - Acquisition, retention, expansion tactics

## Research Source Schema

**Expected structure** (from `datasets/research/{topic}/{filename}.md`):

```yaml
---
title: "Source Title"
kind: "file" | "url" | "note"
topic: "strategic-category"
url: "https://..." (if applicable)
checksum: "sha256:..."
added_utc: "YYYY-MM-DDTHH:MM:SSZ"
expiry_date: "YYYY-MM-DD"
author: "Author Name" (optional)
published_date: "YYYY-MM-DD" (optional)
tags: ["keyword1", "keyword2"]
---

# Source Title

## Key Insights
- Insight 1
- Insight 2

## Strategic Applications
- How this informs decisions
- Relevant use cases

## Citations / Quotes
> "Verbatim quote for future citation"
> — Author, Publication (Date)

## Related Internal Links
- [Meeting notes](datasets/meetings/...)
- [Epic](datasets/product/epics/...)
```

## Gathering Process

### 1. Determine Topic and Filters

**Inputs:**
- `topic`: Strategic category (required)
- `max_age_days`: Maximum age of sources (optional, default: varies by type)
- `include_expired`: Whether to include expired sources (default: false)
- `keywords`: Additional keyword filter (optional)

**Expiry guidelines:**
| Source Type | Default Max Age | Rationale |
|-------------|-----------------|-----------|
| Frameworks | 365-730 days (1-2 years) | Conceptual models change slowly |
| Market data | 90-180 days (3-6 months) | Markets evolve quickly |
| Competitor intel | 180-365 days (6-12 months) | Products change, pricing shifts |
| Customer insights | 180-365 days (6-12 months) | Needs evolve over time |

### 2. Collect Research Files

**Scan path:**
```
datasets/research/{topic}/**/*.md
```

**Use Glob to find sources:**
```
Glob pattern: datasets/research/{topic}/**/*.md
```

**Example:**
```
Topic: competitive-analysis
→ Glob: datasets/research/competitive-analysis/**/*.md
```

### 3. Filter by Recency and Expiry

**For each source file:**

**A. Read frontmatter:**
```yaml
added_utc: "YYYY-MM-DDTHH:MM:SSZ"
expiry_date: "YYYY-MM-DD"
```

**B. Calculate age:**
```
age_days = current_date - added_utc.date
```

**C. Check expiry:**
```
If expiry_date exists:
  is_expired = current_date > expiry_date
Else:
  Use default expiry based on source type
```

**D. Apply filters:**
```
Keep source if:
  (max_age_days not set OR age_days <= max_age_days) AND
  (include_expired=true OR not is_expired)
```

**E. Flag expired sources:**
If source is expired but included (because include_expired=true):
- Mark source as "[EXPIRED]" in output
- Recommend refresh in gathering report

### 4. Extract Key Information

**For each qualifying source:**

**A. Read content sections:**
- `## Key Insights` → Primary takeaways
- `## Strategic Applications` → How to use this research
- `## Citations / Quotes` → Verbatim quotes for citation
- `## Related Internal Links` → Connected context

**B. Extract insights:**
Parse bullet points from "Key Insights" section:
```
- Insight 1: Full text
- Insight 2: Full text
```

**C. Extract quotes:**
Parse blockquotes from "Citations / Quotes" section:
```
> "Verbatim quote text"
> — Author, Source (Date)
```

**D. Record metadata:**
```
{
  "title": "Source Title",
  "path": "/absolute/path/to/source.md",
  "url": "https://..." (if applicable),
  "topic": "strategic-category",
  "added_date": "YYYY-MM-DD",
  "expiry_date": "YYYY-MM-DD",
  "is_expired": true|false,
  "age_days": N,
  "insights": [array of insight strings],
  "quotes": [array of quote objects],
  "related_links": [array of internal link paths]
}
```

### 5. Apply Keyword Filters (Optional)

**If `keywords` provided:**

**Search across:**
- Source title
- Key insights text
- Strategic applications text
- Quote text
- Tags

**Method:**
```
Use Grep to search for keywords (case-insensitive):
grep -i "keyword" source.md
```

**Keep source if:**
Any keyword match found in source content.

### 6. Organize Output

**Group sources by sub-category (if applicable):**

Example for "competitive-analysis" topic:
- Competitor capabilities
- Pricing comparisons
- Market positioning
- Feature gaps

**Sort sources by:**
1. Recency (most recent first)
2. Relevance (if keyword search applied)
3. Expiry status (non-expired before expired)

### 7. Generate Gathering Report

**Output structure:**
```markdown
# Research Gathering Report

**Topic**: {topic}
**Sources Found**: {N total}
**Active Sources**: {N non-expired}
**Expired Sources**: {N expired}
**Date Range**: {earliest added} to {most recent added}

## Active Sources

### Source 1: {Title}
- **Added**: {YYYY-MM-DD} ({age_days} days ago)
- **Expires**: {YYYY-MM-DD} ({days_until_expiry} days remaining)
- **Path**: {file_path}
- **URL**: {url} (if applicable)

**Key Insights:**
- Insight 1
- Insight 2

**Strategic Applications:**
- Application 1
- Application 2

**Notable Quotes:**
> "Quote text"
> — Author, Source (Date)

---

### Source 2: {Title}
[... same structure ...]

## Expired Sources (Require Refresh)

### Source 3: {Title} [EXPIRED]
- **Added**: {YYYY-MM-DD}
- **Expired**: {YYYY-MM-DD} ({days_expired} days ago)
- **Recommendation**: Refresh or archive

---

## Summary

**Citation-Ready Quotes**: {N quotes extracted}
**Internal Links**: {N related meetings/epics found}
**Recommended Actions**:
1. Refresh {N} expired sources
2. Consider adding research on {identified gaps}
```

## Integration with Workflows

### Strategy Session Integration

**Invoked by:**
- `strategy-session` workflow (context assembly phase)

**Inputs:**
- Topic matching session focus
- Default expiry filtering (exclude expired sources)

**Outputs:**
- Gathered research context for decision-making
- Citation-ready quotes
- Source recommendations

**Usage:**
```
Strategy session on "competitive-analysis"
→ Gather active competitive intel
→ Present insights for discussion
→ Reference in strategy memo
```

### Content Creation Integration

**Invoked by:**
- `content-drafting` workflow (when research backing needed)

**Inputs:**
- Topic matching content subject
- Keyword filters for specificity

**Outputs:**
- Research-backed claims
- Citation sources
- Expert insights for quotes

### Manual Research Queries

**Direct usage:**
User can query research library:
```
"Gather research on pricing-strategy from last 6 months"
"Show competitive-analysis sources with keyword 'segmentation'"
```

## Refresh Recommendations

**When gathering detects expired sources:**

**Auto-generate refresh tasks:**
```
Expired sources requiring refresh:
1. [Source Title] - Expired 45 days ago
   - Original URL: {url}
   - Suggested action: Re-fetch and update

2. [Source Title] - Expired 120 days ago
   - No URL (manual notes)
   - Suggested action: Review and archive or manually update
```

**Offer to:**
- Re-fetch URL-based sources automatically
- Schedule manual review for note-based sources
- Archive sources that are no longer relevant

## Success Criteria

Research gathering complete when:
- All sources in topic directory scanned
- Recency and expiry filters applied
- Key insights and quotes extracted
- Sources organized and sorted
- Expired sources flagged for refresh
- Output structured for consuming workflows

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Including expired sources without flagging | Mark clearly as [EXPIRED] |
| Not extracting verbatim quotes | Preserve exact quote text for citations |
| Missing internal link extraction | Parse and include related links |
| Skipping expiry recommendations | Suggest refresh for expired sources |
| Not respecting topic boundaries | Only gather from specified topic directory |

## Related Skills

- **source-integrity**: Validates source checksums and metadata
- **strategy-session**: Primary consumer of gathered research
- **content-drafting**: Uses gathered research for citations
- **research-processing**: Adds new sources to research library

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Expired source is still relevant" | Flag as expired, recommend refresh. |
| "Close enough" on quote extraction | Preserve verbatim text exactly. |
| "Skip keyword filtering" | Apply filters as requested. |
| "One source is enough" | Gather all relevant sources. |
