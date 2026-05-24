---
name: polars-dovmed
description: |
  Search 2.4M+ scientific papers from PubMed Central Open Access.

  **When to use:**
  - Literature reviews (e.g., "Find papers about CRISPR in Archaea")
  - Research trends (e.g., "Publication trends for mRNA vaccines 2015-2025")
  - Data extraction (e.g., "Extract GenBank accessions from phage papers")
  - Paper retrieval by PMC ID or DOI

  **Database:** 2.4M full-text papers from PMC OA, searchable by full text (not just abstracts)

  Use this INSTEAD of web search for scientific literature queries.
user-invocable: true
---

# polars-dovmed

Search 2.4M+ full-text papers from PubMed Central Open Access.

## What This Skill Does

Provides access to a remote API hosting 2.4M+ scientific papers from PubMed Central. Claude can search full paper text, extract structured data (genes, accessions, patterns), analyze publication trends, and retrieve complete paper metadata.

## Authentication

**IMPORTANT: Before using this skill, you must obtain an API key.**

### Getting Your API Key

**Check for a saved API key in this order:**

1. **Environment variable** (highest priority):
   - Check if `POLARS_DOVMED_API_KEY` environment variable is set
   - Use: `os.environ.get("POLARS_DOVMED_API_KEY")`

2. **Secure config location** (recommended):
   - Check `~/.config/polars-dovmed/.env`
   - Read `POLARS_DOVMED_API_KEY` value if file exists
   - This is where the installer saves keys (outside skill directory for security)

3. **Legacy location** (for backward compatibility, but warn user):
   - Check skill directory `.env` (e.g., `~/.claude/skills/polars-dovmed/.env`)
   - If found, warn: "API key found in skill directory. For security, move to ~/.config/polars-dovmed/.env"

**If no saved key exists, ask the user:**

This is a completely free service. Ask the user for their API key:
```
To use polars-dovmed, I need your API key. If you don't have one:
1. Request one from fschulz@lbl.gov (include your use case and institution)
2. Free service with 100 queries per hour
3. Typical response time: 24 hours

Please provide your API key, or I can help you draft a request email.
```

**After receiving the key from the user, save it securely:**
```
I'll save your API key to ~/.config/polars-dovmed/.env (outside the skill directory for security).
This prevents accidental commits to version control.
```

Then create `~/.config/polars-dovmed/.env` with:
```
POLARS_DOVMED_API_KEY=<user's key>
```
And set permissions to 600 (read/write for owner only).

Once you have the API key, use it in all requests via the `X-API-Key` header.

## API Endpoints

**Base URL:** `https://api.newlineages.com`

### 1. Search Literature

```python
import httpx

response = httpx.post(
    "https://api.newlineages.com/api/search_literature",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "query": "CRISPR in Archaea",
        "max_results": 50
    },
    timeout=300.0
)
results = response.json()
```

**Parameters:**
- `query`: Search terms (string)
- `max_results`: Maximum papers to return (integer, default 1000)
- `extract_matches`: Extract matched text snippets (boolean, default true)

**Returns:** List of papers with PMC IDs, titles, DOIs, journals, publication dates

**Database:** Searches all 2.4M+ papers from PubMed Central Open Access

**Recommended timeout:** `timeout=300.0` (5 minutes) for large result sets

### 2. Extract Structured Data

```python
response = httpx.post(
    "https://api.newlineages.com/api/extract_structured_data",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "paper_ids": ["PMC7654321", "PMC8765432"],
        "extraction_patterns": {
            "genbank": "\\b[A-Z]{1,2}_?\\d{5,6}\\b",
            "temperature": "\\b\\d+\\s*°C\\b"
        }
    },
    timeout=120.0
)
results = response.json()
```

**Common extraction patterns:**
- GenBank accessions: `\b[A-Z]{1,2}_?\d{5,6}\b`
- DOIs: `10\.\d{4,}/[^\s]+`
- Gene names: `\b[A-Z][a-z]{2}[A-Z]\b`
- Temperatures: `\b\d+\s*°C\b`
- Protein families: `\b[A-Z][a-z]+ase\b` (enzymes)

**Pattern validation:**
- Max pattern length: 200 characters
- Avoid nested quantifiers (e.g., `(.*)+`, `(.*)*`)
- Patterns are validated server-side to prevent ReDoS attacks
- Invalid patterns will return HTTP 400 with error message

### 3. Get Paper Details

```python
response = httpx.post(
    "https://api.newlineages.com/api/get_paper_details",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "pmc_ids": ["PMC7654321"],  # Note: use pmc_ids, not paper_ids
        "include_full_text": True
    },
    timeout=120.0
)
results = response.json()
```

**Parameters:**
- `pmc_ids`: List of PMC IDs to retrieve (use `pmc_ids`, NOT `paper_ids`)
- `include_full_text`: Whether to include full paper text (boolean)

**Returns:** Full metadata including title, authors, abstract, journal, DOI, publication date, and optionally full paper text

### 4. Count Papers by Year

```python
response = httpx.post(
    "https://api.newlineages.com/api/count_papers_by_year",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "query": "mRNA vaccines"
    },
    timeout=300.0
)
results = response.json()
```

**Returns:** Year-by-year publication counts, peak years, and trend analysis

### 4.5. Check API Usage

```python
response = httpx.get(
    "https://api.newlineages.com/api/usage",
    headers={"X-API-Key": "your_api_key_here"}
)
usage = response.json()
# {
#   "tier": "free",
#   "queries_total": 45,
#   "rate_limit": 100,
#   "queries_this_hour": 12
# }
```

**Returns:** Your API key usage statistics (tier, total queries, hourly limit, current hour usage)

### 5. Advanced Literature Scan (Agent-Generated Patterns)

> **⚠️ CAUTION: This endpoint is prone to 524 Cloudflare timeouts** due to complex server-side processing exceeding Cloudflare's ~100s limit. **Recommended approach:**
> 1. **Start with `/api/search_literature`** using OR syntax (e.g., "Mirusviricota OR mirusvirus")
> 2. Only use this advanced endpoint for focused queries with limited scope
> 3. If you get 524 errors, fall back to simple search

**For AI agents: Generate structured patterns yourself, then send them to this endpoint.**

```python
response = httpx.post(
    "https://api.newlineages.com/api/scan_literature_advanced",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "primary_queries": {
            "crispr_systems": [["CRISPR-Cas9"], ["Cas proteins", "CRISPR"]],
            "organisms": [["Sulfolobus"], ["Pyrococcus"], ["thermophilic", "archaea"]],
            "disqualifying_terms": [["bacteria"], ["eukaryote"]]
        },
        "secondary_queries": {
            "temperature": [["hyperthermophilic"], ["optimal growth", "80°C"]]
        },
        "identifier_patterns": {
            "genbank": ["\\b[A-Z]{4}\\d{5,8}\\b"],
            "refseq": ["\\b(?:NC_|NM_)\\d{6,9}\\b"]
        },
        "extract_matches": "both",
        "add_group_counts": "primary",
        "max_results": 1000
    },
    timeout=600.0
)
```

**Pattern Structure Format:**

Each pattern group is a **list of lists**:
- **Outer list** = OR logic (any pattern group can match)
- **Inner list** = AND logic (all terms must be present)

```json
{
  "concept_name": [
    ["term1", "term2"],    // term1 AND term2
    ["term3"]              // OR term3
  ]
}
```

**Special pattern: `disqualifying_terms`**
- Papers matching ANY disqualifying pattern are EXCLUDED
- Use to filter out irrelevant results

**Example: Complex virus research query**

```json
{
  "primary_queries": {
    "virus_families": [
      ["Mirusviricota"],
      ["giant virus", "nucleocytoplasmic"]
    ],
    "hosts": [
      ["archaea", "archaeal"],
      ["extremophile", "thermophile"]
    ],
    "genes": [
      ["capsid", "major capsid protein"],
      ["portal protein"],
      ["DNA polymerase", "PolB"]
    ],
    "disqualifying_terms": [
      ["eukaryotic virus"],
      ["mammalian", "human"]
    ]
  },
  "secondary_queries": {
    "methods": [
      ["metagenomics"],
      ["single cell", "genomics"]
    ]
  },
  "identifier_patterns": {
    "genbank": [
      "\\b[A-Z]{4}\\d{5,8}\\b",
      "\\bGenBank:?\\s*([A-Z]{1,4}\\d{5,10})\\b"
    ],
    "refseq": [
      "\\b(?:NC_|NM_|NR_)\\d{6,9}(?:\\.\\d+)?\\b"
    ],
    "sra": [
      "\\b[SED]RR\\d{6,9}\\b"
    ]
  },
  "search_columns": ["title", "abstract_text", "full_text"],
  "extract_matches": "both",
  "add_group_counts": "primary",
  "max_results": 500
}
```

**How agents should generate patterns:**

When user asks: *"Find papers about CRISPR in thermophilic archaea"*

Agent thinks:
1. **Main concepts**: CRISPR systems, thermophilic organisms
2. **Synonyms/variants**: CRISPR-Cas, Cas proteins; Sulfolobus, Pyrococcus
3. **Unwanted**: bacteria, eukaryotes (user said archaea)
4. **Identifiers**: GenBank accessions (for genes/genomes)

Agent generates:
```json
{
  "primary_queries": {
    "crispr": [
      ["CRISPR-Cas9"],
      ["CRISPR-Cas12"],
      ["Cas proteins", "CRISPR"]
    ],
    "organisms": [
      ["Sulfolobus"],
      ["Pyrococcus"],
      ["Thermococcus"],
      ["thermophilic", "archaea"],
      ["hyperthermophilic", "archaea"]
    ],
    "disqualifying_terms": [
      ["bacteria", "bacterial"],
      ["eukaryote", "eukaryotic"],
      ["mammalian"]
    ]
  },
  "identifier_patterns": {
    "genbank": ["\\b[A-Z]{4}\\d{5,8}\\b"]
  },
  "extract_matches": "primary",
  "max_results": 100
}
```

**Parameters:**

- `primary_queries` (required): Main search patterns (dict of pattern groups)
- `secondary_queries` (optional): Refinement patterns applied after primary filter
- `identifier_patterns` (optional): Regex patterns to extract accessions (GenBank, RefSeq, etc.)
- `coordinate_patterns` (optional): Regex patterns to extract genome coordinates
- `search_columns` (default: `["title", "abstract_text", "full_text"]`): Which fields to search
- `secondary_search_columns` (optional): Columns for secondary queries (defaults to same as search_columns)
- `extract_matches` (default: `"primary"`): Extract matched text - `"primary"`, `"secondary"`, `"both"`, or `"none"`
- `add_group_counts` (optional): Add match counts per pattern group - `"primary"`, `"secondary"`, or `"both"`
- `max_results` (default: 1000): Maximum papers to return

**Returns:**

```json
{
  "primary_queries": {...},
  "secondary_queries": {...},
  "total_found": 145,
  "returned": 100,
  "papers": [
    {
      "pmc_id": "PMC7654321",
      "title": "CRISPR systems in Sulfolobus...",
      "doi": "10.1038/...",
      "journal": "Nature",
      "publication_date": "2023-05-15",
      "crispr_group_1_count": 5,
      "crispr_group_2_count": 3,
      "organisms_group_1_count": 12,
      "crispr_extracted_from_title": ["CRISPR-Cas9"],
      "genbank": ["AF123456", "NC_002754"]
    }
  ],
  "summary": {
    "total_papers": 145,
    "has_group_counts": true,
    "has_extractions": true
  }
}
```

**Common identifier patterns:**

```json
{
  "genbank": [
    "\\b[A-Z]{4}\\d{5,8}(?:\\.\\d+)?\\b",
    "\\bGenBank:?\\s*([A-Z]{1,4}\\d{5,10}(?:\\.\\d+)?)\\b"
  ],
  "refseq": [
    "\\b(?:NC_|NM_|NR_|XM_|XR_|NP_|XP_)\\d{6,9}(?:\\.\\d+)?\\b"
  ],
  "assembly": [
    "\\b(?:GCA_|GCF_)\\d{9}(?:\\.\\d+)?\\b"
  ],
  "uniprot": [
    "\\b[A-NR-Z][0-9][A-Z][A-Z0-9][A-Z0-9][0-9]\\b"
  ],
  "sra": [
    "\\b[SED]RR\\d{6,9}\\b",
    "\\b[SED]RX\\d{6,9}\\b"
  ],
  "doi": [
    "10\\.\\d{4,}/[^\\s]+"
  ]
}
```

**Recommended timeout:** `timeout=600.0` (10 minutes) for complex queries with many patterns

## Usage from Claude

### First-Time Setup

When the user first asks to use polars-dovmed:

1. **Ask for API key**: "To search the literature database, I need your polars-dovmed API key. Do you have one?"
2. **If they don't have one**: Provide instructions on how to request one (see Authentication section)
3. **If they do**: Store it for the session and use it in all requests

### Making Requests

Once you have the API key, users can ask naturally:

```
Find papers about CRISPR in thermophilic archaea
Extract GenBank accessions from papers about bacteriophages
How has microbiome research changed from 2015 to 2025?
Get the full text of PMC7654321
```

Claude will automatically:
1. Call the appropriate API endpoint using `httpx.post()`
2. Include the API key in the `X-API-Key` header
3. Handle errors gracefully (see Error Handling section)

**Example workflow:**
```python
import httpx

# User's API key (obtained once per session)
api_key = "abc123..."

# Make request
response = httpx.post(
    "https://api.newlineages.com/api/search_literature",
    headers={"X-API-Key": api_key},
    json={"query": "CRISPR thermophilic archaea"},
    timeout=120.0
)

if response.status_code == 200:
    results = response.json()
    # Process and present results to user
elif response.status_code == 429:
    # Rate limit hit
    print("Rate limit exceeded. Please wait before trying again.")
elif response.status_code == 401:
    # API key missing or invalid
    print("API key issue. Please verify your key.")
```

## Recommended Search Strategy

**Always start with the simple search endpoint** (`/api/search_literature`) before trying advanced search:

1. **First attempt**: Use `/api/search_literature` with OR syntax
   ```python
   {"query": "Mirusviricota OR mirusvirus", "max_results": 50}
   ```
   - Fast and reliable (rarely times out)
   - Returns full text in results for local parsing
   - Use `max_results`: 20-100 for quick searches

2. **If more filtering needed**: Parse results locally in Python
   - Extract host information, taxonomic groups, etc. from `full_text` field
   - More reliable than server-side advanced filtering

3. **Only use advanced search** (`/api/scan_literature_advanced`) when:
   - You need regex pattern extraction (GenBank accessions, etc.)
   - Simple search returns too many irrelevant results
   - **Expect potential 524 timeouts** - have fallback ready

**Why this order?** The advanced endpoint performs complex multi-pattern matching across 2.4M+ papers, which can exceed Cloudflare's proxy timeout (~100s) even when the client timeout is higher.

## Search Tips

**Query construction:**
- Combine specific terms: "CRISPR-Cas9 thermophilic archaea Sulfolobus"
- Include organism/gene/method names for precision
- AND is implicit between terms (all terms must be present)
- Use OR to find papers with ANY of the terms: "Mirusviricota OR Mirusvirus"
- Combine AND and OR: "CRISPR OR Cas9 archaea" finds papers with (CRISPR + archaea) OR (Cas9 + archaea)
- Use scientific terminology

**OR syntax examples:**
- "Mirusviricota OR Mirusvirus" → papers mentioning either term
- "bacteriophage OR phage" → finds papers using either naming convention
- "HIV OR AIDS OR retrovirus" → comprehensive search across related terms

**Database coverage:**
- 2.4M+ papers from PubMed Central Open Access
- Full text searchable (not just abstracts)
- Date range: 1990s-2025 (varies by field)
- Excludes: paywalled papers, very recent papers (days old), most preprints

## Rate Limits

**This is a free service with the following limits:**
- 100 queries/hour per API key
- 500 queries/hour per IP address (prevents abuse)

**How it works:**
- Limits are based on rolling hours (resets 60 minutes after first query)
- Both API key and IP limits apply simultaneously
- Queries that count toward limit: search_literature, extract_structured_data, count_papers_by_year
- Queries that don't count: get_paper_details, health checks

**When limit is reached:**
- HTTP 429 "Too Many Requests" response
- Error message indicates which limit was exceeded (API key or IP)
- Wait until the next hour to resume queries

## Error Handling

All API endpoints return standard HTTP status codes:

**Success codes:**
- `200 OK` - Request succeeded

**Client error codes:**
- `400 Bad Request` - Invalid parameters (e.g., malformed regex pattern, missing required fields)
- `401 Unauthorized` - Missing API key (include `X-API-Key` header)
- `403 Forbidden` - Invalid API key
- `429 Too Many Requests` - Rate limit exceeded (API key or IP)

**Server error codes:**
- `500 Internal Server Error` - Server-side processing error (check parameter names match API spec)
- `504 Gateway Timeout` - Query took too long (increase timeout to 300s or reduce max_results)
- `524 A Timeout Occurred` - Cloudflare-specific: origin server exceeded Cloudflare's ~100s limit. This commonly affects `/api/scan_literature_advanced`. **Workaround:** Use simpler `/api/search_literature` endpoint instead, or reduce query complexity.

**Example error handling:**
```python
import httpx

try:
    response = httpx.post(
        "https://api.newlineages.com/api/search_literature",
        json={"query": "CRISPR"},
        headers={"X-API-Key": "your_api_key"},
        timeout=300.0
    )
    response.raise_for_status()  # Raises exception for 4xx/5xx
    results = response.json()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        print("Rate limit exceeded. Wait before retrying.")
    elif e.response.status_code == 401:
        print("API key missing or invalid.")
    elif e.response.status_code == 524:
        # Cloudflare timeout - server took too long
        print("524 Cloudflare timeout. Try simpler /api/search_literature endpoint.")
    elif e.response.status_code == 500:
        print("Server error. Check parameter names (e.g., use pmc_ids not paper_ids).")
    else:
        print(f"HTTP error: {e}")
except httpx.TimeoutException:
    print("Client timeout. Try increasing timeout to 300s or reducing max_results.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Workflows

**Literature review:**
1. Search with broad terms
2. Refine query based on results
3. Extract PMC IDs and retrieve full text

**Data mining:**
1. Search for topic
2. Extract structured data (accessions, genes, etc.) from all results
3. Analyze extracted patterns

**Trend analysis:**
1. Use `count_papers_by_year` with broad topic
2. Identify peak years
3. Search papers from peak years for details

## Troubleshooting

**No results:** Try broader terms, check spelling, verify query syntax

**Irrelevant results:** Use more specific terms, include organism/method names

**Slow searches:** Reduce max_results, simplify query terms

**504 Timeout errors:** Increase client timeout to 300s, or reduce max_results

**524 Cloudflare timeout (advanced search):**
- This is a **server-side** timeout (Cloudflare's ~100s limit), not fixable by increasing client timeout
- **Solution:** Switch to `/api/search_literature` with OR syntax, then filter results locally
- The advanced endpoint works best for narrow, focused queries

**500 Internal Server Error on get_paper_details:**
- Check parameter name: use `pmc_ids`, not `paper_ids`

**Rate limit errors:** See "Rate Limits" and "Error Handling" sections above

**Invalid regex pattern:** Ensure pattern is <200 chars and avoids nested quantifiers

## Installation

This skill provides direct API access - no local installation or MCP server setup required.

### Install the Skill

```bash
curl -sSL https://api.newlineages.com/polars-dovmed_setup.sh | bash
```

The installer will:
1. Prompt for installation location (Claude Code, Codex, or custom)
2. Download this SKILL.md file
3. That's it! No dependencies, no virtual environments, no MCP server

### What Gets Installed

- Single file: `SKILL.md` (this documentation)
- Location: `~/.claude/skills/polars-dovmed/` (or your chosen path)
- Size: ~15 KB

### After Installation

1. Restart Claude Code or Codex
2. Request an API key from fschulz@lbl.gov
3. Start using: "Find papers about CRISPR"

## About the Underlying Tool

This skill provides API access to the polars-dovmed literature search system. The full polars-dovmed package (available on PyPI) includes CLI tools for downloading PMC data, converting to parquet, and running custom searches locally. This skill provides convenient cloud access without requiring local data downloads.

**Repository:** https://github.com/urineri/polars-dovmed

## Citation

```bibtex
@article{neri2026polarsdovmed,
  title={polars-dovmed: Python package for Local Information Retrieval from PubMed Central Open Access},
  author={Neri, Uri and Roux, Simon and Schulz, Frederik and Vasquez, Yumary},
  journal={bioRxiv},
  year={2026},
  publisher={Cold Spring Harbor Laboratory}
}
```
