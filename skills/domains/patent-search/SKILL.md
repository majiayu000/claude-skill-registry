---
name: patent-search
description: Search 76M+ patents using BigQuery (fast, zero setup) or PatentsView API (US patents with rich metadata).
---

# Patent Search Skill

Two powerful patent search methods:

1. **BigQuery Search** (Recommended) - 76M+ worldwide patents, zero local storage
2. **PatentsView API** - Detailed US patent metadata (inventors, assignees, classifications, citations)

**FOR CLAUDE:** All files and dependencies installed.
- Go directly to Quick Test section
- Script at: `.claude/skills/patent-search/bigquery_search.py`
- Run from skill directory
- Windows: Use cmd syntax (dir, set, &&)

## Quick Test

```bash
# Windows
cd ".claude\skills\patent-search"
set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\\gcloud\\application_default_credentials.json
python bigquery_search.py search "voice biometric" 5

# Linux/macOS
cd .claude/skills/patent-search
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
python bigquery_search.py search "voice biometric" 5
```

**Expected:** 5 patent results in ~4 seconds

## Quick Start

### BigQuery Search

```bash
# Keyword search (2-3 keywords for best results)
python bigquery_search.py search "voice biometric authentication" 20

# Get specific patent (hyphenated format: US-XXXXXXX-XX)
python bigquery_search.py get US-12424224-B2

# CPC classification search
python bigquery_search.py cpc G10L 15
```


### PatentsView API


## Choosing the Right Method

### Use BigQuery When:
- Quick keyword search needed
- Worldwide patents (not just US)
- Fast results (3-4 seconds)
- Zero local storage
- CPC classification search
- Budget-conscious (free tier: 1TB/month)

### Use PatentsView When:
- Need detailed US patent metadata
- Searching by inventor/assignee
- Citation analysis required
- Complex boolean queries
- Exact field matching
- Patent family analysis

### Combined Workflow

1. Start with BigQuery (broad keyword search)
2. Identify relevant patents and CPC codes
3. Switch to PatentsView (detailed metadata/citations)
4. Export final results

**Example:**
```bash
# Step 1: BigQuery broad search
python bigquery_search.py search "voice biometric authentication" 20

# Step 2: Found CPC G10L17, search more
python bigquery_search.py cpc G10L17 50

# Step 3: Use PatentsView for inventor/assignee analysis
```


## Instructions for Claude

When user requests patent searches:

1. **Understand Goal**: Technology, time period, prior art vs competitive analysis, US vs worldwide
2. **Check Dependencies**: Verify BigQuery/PatentsView setup
3. **Choose Method**: Default BigQuery for broad, PatentsView for detailed
4. **Optimize Queries**:
   - BigQuery: 2-3 keywords, simplify if zero results, use CPC codes
   - PatentsView: Verify API key, construct JSON queries, handle pagination
5. **Present Results**: Parse JSON, highlight key info, provide Google Patents URLs
6. **Offer Next Steps**: Suggest refinements, related classifications, citation analysis


## Common Use Cases

### Prior Art Search
1. BigQuery keyword search
2. Identify CPC codes
3. BigQuery CPC search
4. PatentsView citation analysis
5. Document findings

### Competitive Intelligence
1. PatentsView search by assignee
2. Filter by date range
3. Group by CPC
4. Identify key inventors
5. Trend report

### Technology Landscape
1. BigQuery CPC search worldwide
2. Analyze by country/date
3. Identify patent families
4. PatentsView US details
5. Summary report

### Freedom to Operate
1. BigQuery keyword + CPC search
2. Filter by jurisdiction/active status
3. PatentsView claim analysis
4. Review forward citations
5. Risk assessment

## Performance & Coverage

| Method | Patents | Coverage | Speed | Cost | Storage |
|--------|---------|----------|-------|------|---------|
| BigQuery | 76M+ | Worldwide | 3-4s | Free* | 0GB |
| PatentsView | 9.2M | US only | 1-3s | Free | 0GB |

*Free tier: 1TB queries/month

## Quick Reference

### BigQuery Commands

```bash
python bigquery_search.py search "query" <limit>
python bigquery_search.py get <PATENT-NUMBER>
python bigquery_search.py cpc <CODE> <limit>
```

### Common CPC Codes

| Code | Technology |
|------|-----------|
| G10L | Speech analysis/synthesis |
| G10L15 | Speech recognition |
| G10L17 | Speaker recognition/verification |
| G06F21 | Security arrangements |
| G06N | Computing models |

### Troubleshooting

**FOR CLAUDE:** Only run diagnostics if Quick Test fails.

| Problem | Solution |
|---------|----------|
| BigQuery auth fails | `gcloud auth application-default login` |
| No module google.cloud | `pip install google-cloud-bigquery db-dtypes` |
| Zero results | Simplify query (2-3 keywords max) |
| Patent get fails | Use hyphenated format: `US-XXXXX-XX` |
| PatentsView 403 | Set API key environment variable |
| Rate limit (429) | Wait 60 seconds (PatentsView: 45 req/min) |
