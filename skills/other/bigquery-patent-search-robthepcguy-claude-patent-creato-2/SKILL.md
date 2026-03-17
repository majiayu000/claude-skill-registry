---
name: bigquery-patent-search
description: Fast, cloud-based patent searching across 76 million+ worldwide patents using Google BigQuery - keyword search, CPC classification, patent details retrieval
tools: Bash, Read, Write
model: sonnet
---

# BigQuery Patent Search Skill

Fast, cloud-based patent searching across 76 million+ worldwide patents using Google BigQuery.

## When to Use

Invoke this skill when users ask to:
- Search for prior art patents
- Find patents in a specific technology area
- Search by CPC classification code
- Look up patent details by publication number
- Conduct freedom-to-operate searches
- Research patent landscapes

## What This Skill Does

Provides access to Google's public patent dataset:

1. **Keyword Search** across 76M+ patents:
   - Full-text search of titles, abstracts, claims
   - Filter by country (US, EP, JP, CN, etc.)
   - Filter by filing/grant date ranges
   - Fast cloud-based queries (< 5 seconds)

2. **CPC Classification Search**:
   - Search by CPC code (e.g., "G06F16/", "H04L29/06")
   - Browse patent classifications
   - Find patents in specific technical domains

3. **Patent Details Retrieval**:
   - Get full patent text by publication number
   - Access title, abstract, claims, description
   - View CPC codes, inventors, assignees
   - See filing and grant dates

## Required Setup

This skill requires Google Cloud authentication:

**Prerequisites**:
1. Google Cloud Project (free to create)
2. BigQuery API enabled (free for reasonable usage)
3. Application Default Credentials configured

**Setup Commands**:
```bash
# Install Google Cloud SDK (if not installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Set project (get ID from console.cloud.google.com)
export GOOGLE_CLOUD_PROJECT=your-project-id
```

**Environment Variable**:
Set in `.env` file: `GOOGLE_CLOUD_PROJECT=your-project-id`

## How to Use

When this skill is invoked:

1. **Initialize BigQuery searcher**:
   ```python
   import sys
   sys.path.insert(0, os.path.join(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'), 'python'))
   from python.bigquery_search import BigQueryPatentSearch

   searcher = BigQueryPatentSearch()
   ```

2. **Search by keywords**:
   ```python
   results = searcher.search_patents(
       query="blockchain authentication",
       limit=20,
       country="US",  # Optional: filter by country
       start_year=2020,  # Optional: filter by year
       end_year=2024
   )
   ```

3. **Search by CPC code**:
   ```python
   results = searcher.search_by_cpc(
       cpc_code="G06F16/",  # CPC prefix
       limit=20,
       country="US"
   )
   ```

4. **Get patent details**:
   ```python
   patent = searcher.get_patent(
       patent_number="US10123456B2"  # Publication number
   )
   ```

## BigQuery Dataset

Uses `patents-public-data.patents` on Google BigQuery:
- **76M+ worldwide patents**
- **12M+ US patents** with full text
- Updated weekly
- Free to query (no billing for reasonable usage)

## Search Result Format

Each result includes:
```python
{
    "publication_number": "US10123456B2",
    "title": "Method and system for...",
    "abstract": "A system for...",
    "filing_date": "2019-01-15",
    "grant_date": "2020-06-30",
    "country": "US",
    "cpc_codes": ["G06F16/245", "H04L29/06"],
    "inventors": ["John Doe", "Jane Smith"],
    "assignee": "Example Corp"
}
```

Full patent details also include:
- `claims`: Full text of all claims
- `description`: Complete description section
- `priority_date`: Earliest priority date
- `family_id`: Patent family ID

## Presentation Format

Present search results as:

```
PATENT SEARCH RESULTS
====================

Query: "blockchain authentication"
Found: 247 patents (showing top 20)
Date Range: 2020-2024
Country: US

[1] US10123456B2 - System for blockchain-based authentication
    Assignee: Example Corp
    Filed: 2019-01-15 | Granted: 2020-06-30
    CPC: G06F16/245, H04L29/06

    Abstract: A system for authenticating users using blockchain
    technology with distributed ledger verification...

[2] US10234567B1 - Method of secure authentication using blockchain
    ...

---

Top 5 Most Relevant:
1. US10123456B2 (95% relevance)
2. US10234567B1 (92% relevance)
...
```

## Advanced Search Techniques

1. **Boolean Operators** in queries:
   - "blockchain AND authentication"
   - "encryption OR cryptography"
   - "(mobile OR wireless) AND security"

2. **Phrase Search**:
   - "distributed ledger technology"
   - "public key infrastructure"

3. **CPC Code Hierarchies**:
   - "G06F" = Computing
   - "G06F16/" = Information retrieval
   - "G06F16/245" = Structured query language

## Common CPC Codes

- **G06F**: Computing, calculating, counting
- **H04L**: Digital communication
- **G06Q**: Business methods
- **H04W**: Wireless communication
- **G06N**: Computer systems based on specific models
- **G06T**: Image processing

## Error Handling

If BigQuery is not configured:
1. Check if `google-cloud-bigquery` is installed
2. Verify authentication: `gcloud auth application-default login`
3. Confirm project ID in environment: `GOOGLE_CLOUD_PROJECT`
4. Test with: `python scripts/test_bigquery.py`

## Cost Considerations

BigQuery pricing:
- **First 1TB/month**: FREE
- **After 1TB**: $5 per TB queried
- **Typical query**: 10-50 MB per search
- **~20,000 searches** free per month

## Tools Available

- **Bash**: To run Python BigQuery searches
- **Read**: To load saved search results
- **Write**: To save patent search results
- **Grep**: To search through saved results
