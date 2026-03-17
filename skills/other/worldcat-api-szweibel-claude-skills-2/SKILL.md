---
name: worldcat-api
description: Use OCLC WorldCat APIs to search for books and scholarly materials, retrieve bibliographic metadata, check library holdings worldwide, and get classification data. Use when working with ISBNs, DOIs, OCLC numbers, library catalogs, or institutional holdings.
license: MIT
category: api-integration
---

# WorldCat API

WorldCat is the world's largest library catalog with 500+ million bibliographic records and holdings from 10,000+ libraries worldwide.

## Two Main APIs

### Metadata API
For detailed bibliographic records and metadata.

**Python Library:** `bookops-worldcat` (recommended)
```python
from bookops_worldcat import MetadataSession, WorldcatAccessToken

# Authenticate
token = WorldcatAccessToken(
    key=OCLC_CLIENT_ID,
    secret=OCLC_CLIENT_SECRET,
    scopes="WorldCatMetadataAPI"
)
session = MetadataSession(authorization=token)

# Search for books
response = session.brief_bibs_search(q="title:Moby Dick")

# Get classification
response = session.bib_get_classification(oclcNumber="123456")

# Check specific institutions
response = session.summary_holdings_search(
    oclcNumber="123456",
    heldBySymbol=["ZGM", "NYP"]
)
```

**Key Methods:**
- `brief_bibs_search(q=query)` - search bibliographic records
- `summary_holdings_search()` - check holdings at specific institutions
- `bib_get_classification()` - get LC/Dewey classification
- `brief_bibs_get()` - get single record by OCLC number

Documentation: https://bookops-cat.github.io/bookops-worldcat/

### Search API V2
For comprehensive holdings data across ALL institutions.

**Important:** No Python library available - use direct REST calls.

**Key Endpoint - Get ALL Holdings:**
```python
import requests
from bookops_worldcat import WorldcatAccessToken

# Authenticate
token = WorldcatAccessToken(
    key=OCLC_CLIENT_ID,
    secret=OCLC_CLIENT_SECRET,
    scopes='wcapi:view_holdings wcapi:view_institution_holdings'
)

# Get ALL institutions holding this item (ONE API call)
url = 'https://americas.discovery.api.oclc.org/worldcat/search/v2/bibs-holdings'
headers = {
    'Authorization': f'Bearer {token.token_str}',
    'Accept': 'application/json'
}
params = {'oclcNumber': '123456'}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Extract institution symbols
institutions = []
for record in data.get('briefRecords', []):
    for holding in record.get('institutionHolding', {}).get('briefHoldings', []):
        institutions.append({
            'symbol': holding.get('oclcSymbol'),
            'name': holding.get('institutionName'),
            'country': holding.get('country')
        })

symbols = [inst['symbol'] for inst in institutions]
# Returns: ["DLC", "NYP", "ZGM", "ZCU", ...]
```

**Why This Matters:** This endpoint returns ALL holdings in one API call, avoiding the need for 100+ individual requests when checking multiple institutions.

## Authentication

All WorldCat APIs use OAuth 2.0 Client Credentials Grant:

```bash
# Set environment variables
export OCLC_CLIENT_ID="your_client_id"
export OCLC_CLIENT_SECRET="your_client_secret"
```

Get credentials from OCLC Developer Network: https://developer.api.oclc.org/

## Common Patterns

### Progressive Search Strategy

When searching with incomplete or messy citations:

1. Start broad - title keywords only
2. Add filters progressively if too many results
3. Pick best match based on metadata alignment

**Example:**
```
❌ Bad: "Ezra and Dorothy Pound: Letters in Captivity, 1945–1946"
✅ Good: "Pound Letters Captivity"
         → If 50+ results, add year: 1999
         → Pick match with correct publisher/author
```

**Why:** Bibliographic data has variations (punctuation, encoding, formatting). Better to get 20 results and filter than 0 results from being too specific.

### Efficient Holdings Checking

**Don't do this (slow - 150+ API calls):**
```python
for code in institution_codes:  # BAD!
    check_if_institution_holds(oclc_number, code)
```

**Do this instead (fast - 1 API call):**
```python
# Get ALL holdings at once
holdings = get_all_holdings_via_search_api_v2(oclc_number)
symbols = set(holdings['institution_symbols'])

# Filter locally
tier_codes = {'NYP', 'ZCU', 'ZYU'}
matches = symbols & tier_codes
```

### Handling Citations

Common citation formats encountered:
- `(Year) Title, Publisher`
- `Title / Vol. N, Subtitle`
- `"Title" : Subtitle`
- `Author. (Year). Title.`

**Best practice:** Extract clean search terms by removing volume info, subtitles, and complex punctuation initially. Add specificity only if needed.

### Common Challenges

**Encoding errors:**
- Look for: `?`, `�`, garbled characters
- Example: "Antigüedad" → "Antig?edad"
- Try: Remove accents initially, add back if no results

**Multiple OCLC records:**
- Same work may have multiple records (digital vs print editions)
- Check multiple if needed
- Document which record was used

**Missing metadata:**
- Not all records have DOIs or classification
- Handle missing data gracefully

## Institution Symbols

Libraries have OCLC institution symbols (codes):
- `DLC` - Library of Congress
- `NYP` - New York Public Library
- `ZGM` - CUNY Graduate Center
- `ZCU` - Columbia University
- `HUL` - Harvard University

The Search API V2 `/bibs-holdings` endpoint returns these symbols. Users typically maintain lists of symbols for their consortia.

## Workflows

### Find and Identify Items
1. Search by ISBN if available (most reliable)
2. Otherwise keyword search with progressive narrowing
3. Extract OCLC number from best match

### Get Complete Metadata
1. Use Metadata API or bookops-worldcat
2. Call `brief_bibs_get(oclcNumber=num)` or similar
3. Returns: title, author, publisher, ISBNs, subjects, classification

### Check Holdings Across Institutions
1. Use Search API V2 `/bibs-holdings` endpoint
2. Returns complete array of institution symbols
3. Filter/group symbols locally as needed

### Batch Processing
- Process items progressively
- Don't fail entire batch on one error
- Show progress for large datasets
- Document reasoning for each item

## Reference

Official OCLC documentation:
- Metadata API: https://www.oclc.org/developer/api/oclc-apis/worldcat-metadata-api.en.html
- Search API V2: https://developer.api.oclc.org/wcv2
