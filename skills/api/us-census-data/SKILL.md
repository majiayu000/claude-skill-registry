---
name: us-census-data
description: This skill should be used when the user asks to "get Census data", "query American Community Survey", "find ACS data", "get population by state", "query Decennial Census", "find Census variables", "get median income data", "download demographic data", "Census API query", "get housing data from Census", or mentions US Census Bureau data (demographics, income, poverty, education, housing, population estimates, etc.).
version: 1.1.0
---

# US Census Data Skill

Query demographic, economic, housing, and population data from the US Census Bureau API. Supports American Community Survey (ACS), Decennial Census, and Population Estimates.

## Prerequisites

Before querying, check if the user has an API key:

1. Look for `CENSUS_API_KEY` in the user's `.env` file
2. If found, append to requests: `&key=<api_key>`
3. If not found, instruct the user to:
   - Register at https://api.census.gov/data/key_signup.html
   - Add to `.env`: `CENSUS_API_KEY=your_key_here`

The API works without a key for testing but is rate-limited and may block requests.

## Quick Start

The Census API is at `api.census.gov`. Queries require:
1. **Dataset path**: `/data/{year}/{dataset}` (e.g., `/data/2022/acs/acs5`)
2. **Variables**: `?get=NAME,B01001_001E` (variable codes)
3. **Geography**: `&for=county:*&in=state:17` (FIPS codes)
4. **API Key**: `&key=YOUR_KEY` (required for production use)

## Workflow

### Step 1: Clarify the Data Need

Ask the user:
- **Topic**: What data? (population, income, housing, education, poverty, etc.)
- **Geography**: What level? (nation, state, county, tract, block group, ZCTA?)
- **Time period**: Which year(s)?
- **Dataset**: ACS 5-year (most common), ACS 1-year, or Decennial Census?

### Step 2: Choose the Dataset

| Need | Dataset | Endpoint | Notes |
|------|---------|----------|-------|
| Detailed demographics (small areas) | ACS 5-Year | `/data/{year}/acs/acs5` | Block group+, most reliable |
| Recent data (large areas only) | ACS 1-Year | `/data/{year}/acs/acs1` | 65k+ population areas only |
| Exact population counts | Decennial | `/data/2020/dec/dhc` | Every 10 years, block level |
| Annual population change | Pop Estimates | `/data/{year}/pep/population` | County+, intercensal |

See `references/datasets.md` for complete dataset documentation.

### Step 3: Find Variables

Census variables use codes like `B19013_001E` (median household income). The `E` suffix = estimate, `M` suffix = margin of error.

**Option A - Popular Variables Reference:**
See `references/popular-variables.md` for curated list of common variables.

**Option B - Variable Search API:**
```
GET https://api.census.gov/data/2022/acs/acs5/variables.json
```

**Option C - Groups (Tables) API:**
```
GET https://api.census.gov/data/2022/acs/acs5/groups.json
```

See `references/datasets.md` for common table prefixes and naming conventions.

### Step 4: Build the Query

**Basic structure:**
```
https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}&key={api_key}
```

**Example - Median income by county in Illinois:**
```
https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=YOUR_KEY
```

**Geography predicates:**
- `for=state:*` - All states
- `for=county:*&in=state:17` - All counties in Illinois
- `for=tract:*&in=state:17&in=county:031` - All tracts in Cook County, IL
- `for=block%20group:*&in=state:17&in=county:031&in=tract:010100` - Block groups in tract

See `references/geographies.md` for complete geography hierarchy and FIPS codes.

### Step 5: Handle Response

Census API returns JSON array where first row is column headers:
```json
[
  ["NAME", "B19013_001E", "state", "county"],
  ["Cook County, Illinois", "62088", "17", "031"],
  ["DuPage County, Illinois", "99007", "17", "043"]
]
```

For large queries, the API has no built-in pagination. Request specific geographies or use `&in=` filters.

## Query Syntax Reference

### Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `get` | Variables to return | `get=NAME,B01001_001E,B19013_001E` |
| `for` | Target geography | `for=county:*` or `for=county:031` |
| `in` | Parent geography filter | `in=state:17` |
| `key` | API key | `key=abc123` |

### Variable Syntax

- Request multiple: `get=NAME,B01001_001E,B19013_001E` (comma-separated)
- Request table: `get=group(B19013)` (all variables in table)
- Include MOE: `get=B19013_001E,B19013_001M`

### Geography Wildcards

Use `*` for "all" at that level:
- `for=state:*` - All 50 states + DC + territories
- `for=county:*&in=state:06` - All counties in California
- `for=tract:*&in=state:06&in=county:037` - All tracts in LA County

## Common Query Patterns

**State-level totals:**
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:*&key=$CENSUS_API_KEY"
```

**County-level within a state:**
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY"
```

**Tract-level (requires state + county):**
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=tract:*&in=state:17&in=county:031&key=$CENSUS_API_KEY"
```

**Multiple variables:**
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E,B25001_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY"
```

## Output Format

Provide the user with:
1. **Dataset**: Name + endpoint + year
2. **Variables**: Code + label for each
3. **Geography**: Level + filters
4. **Query**: Full URL or curl command
5. **Caveats**: MOE notes, update frequency, limitations

### Example Response Format
```
Dataset: ACS 5-Year 2022
Endpoint: https://api.census.gov/data/2022/acs/acs5

Variables:
- NAME: Geography name
- B19013_001E: Median Household Income (estimate)
- B19013_001M: Median Household Income (margin of error)

Geography: All counties in Illinois (state FIPS 17)

Query:
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E,B19013_001M&for=county:*&in=state:17&key=$CENSUS_API_KEY"

Note: ACS data are estimates with margins of error. 5-year estimates are most reliable for small geographies.
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 400 Bad Request | Invalid variable or geography | Check variable exists for that dataset/year |
| 204 No Content | Valid query, no matching data | Geography may not exist or have data |
| Empty array `[]` | No data for that geography | Try different year or geography level |
| "error: unknown variable" | Variable doesn't exist | Use variables.json endpoint to verify |
| Missing data for small areas | ACS 1-year limitation | Use ACS 5-year for areas <65k population |

## Margins of Error (ACS Data)

ACS estimates have sampling error. Always consider:
- `E` suffix = estimate, `M` suffix = margin of error (90% confidence)
- Small geographies have larger MOEs
- 5-year estimates are more reliable than 1-year
- Decennial Census has no MOE (100% count)

See `references/datasets.md` for MOE calculation guidance.

## Geometry (TIGERweb)

Census data API returns tabular data only. For geographic boundaries, use TIGERweb:

See `references/tigerweb.md` for geometry retrieval and data joining.

## Additional Resources

### Reference Files
- **`references/datasets.md`** - Complete dataset documentation (ACS, Decennial, PEP)
- **`references/popular-variables.md`** - Curated list of common variables by topic
- **`references/geographies.md`** - Geography hierarchy, FIPS codes, nesting rules
- **`references/tigerweb.md`** - Boundary/geometry retrieval via TIGERweb API

### Example Files
- **`examples/python-query.py`** - Python code with requests library
- **`examples/curl-examples.sh`** - curl command templates
