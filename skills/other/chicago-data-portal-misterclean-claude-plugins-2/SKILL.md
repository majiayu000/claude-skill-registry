---
name: chicago-data-portal
description: This skill should be used when the user asks to "query Chicago data", "find Chicago datasets", "get Chicago crime data", "download Chicago permits", "write a SODA query for Chicago", "search data.cityofchicago.org", or mentions Chicago city data (311, permits, licenses, inspections, crimes, etc.).
version: 1.1.0
---

# Chicago Data Portal Skill

Query and download datasets from the City of Chicago Data Portal using the Socrata Open Data API (SODA) and SoQL.

## Prerequisites

Before querying, check if the user has an app token:

1. Look for `CHICAGO_DATA_PORTAL_TOKEN` in the user's `.env` file
2. If found, use it in requests via header: `X-App-Token: <token>`
3. If not found, instruct the user to:
   - Sign up at https://data.cityofchicago.org/signup
   - Create an app token in Developer Settings
   - Add to `.env`: `CHICAGO_DATA_PORTAL_TOKEN=your_token_here`

Queries work without a token but are rate-limited.

## Quick Start

The Chicago Data Portal is at `data.cityofchicago.org`. Each dataset has a unique 4x4 ID (e.g., `ijzp-q8t2` for crimes). Use the catalog API to discover datasets, then query via SODA.

## Workflow

### Step 1: Clarify the Data Need

Ask the user:
- **Topic**: What data? (crimes, permits, 311 requests, businesses, etc.)
- **Geography**: Citywide, ward, community area, or specific location/radius?
- **Time window**: Date range or "most recent"?
- **Output**: JSON (code) or CSV (Excel)?
- **Granularity**: Raw rows or aggregated counts?

### Step 2: Find the Dataset

**Option A - Catalog Search API:**
```
GET https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=<keywords>
```

**Option B - Portal UI:**
Browse https://data.cityofchicago.org and use the search bar.

Deliverable: Dataset name, 4x4 ID, and API endpoint.

See `references/popular-datasets.md` for commonly requested datasets.

### Step 3: Get Dataset Metadata

Fetch schema and column info:
```
GET https://data.cityofchicago.org/api/views/<4x4-ID>
```

Key fields in response:
- `columns[].fieldName` - exact column names for queries
- `columns[].dataTypeName` - data type (text, number, calendar_date, location, etc.)
- `columns[].description` - what the column means
- `rowsUpdatedAt` - last data update timestamp

Always verify column names from metadata before building queries.

### Step 4: Build the Query

**Legacy GET (simple, recommended for most cases):**
```
https://data.cityofchicago.org/resource/<4x4-ID>.json?$where=<filter>&$limit=1000
```

**SODA3 POST (complex queries):**
```bash
curl -X POST \
  -H "X-App-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * WHERE date > '\''2024-01-01'\''", "page": {"pageNumber": 1, "pageSize": 1000}}' \
  https://data.cityofchicago.org/api/v3/views/<4x4-ID>/query.json
```

### Step 5: Handle Pagination

Default limit is 1000 rows. For larger extracts:
```
$limit=1000&$offset=0    # Page 1
$limit=1000&$offset=1000 # Page 2
```

Always include `$order` for stable paging:
```
$order=date DESC&$limit=1000&$offset=0
```

For full dataset export, use CSV:
```
https://data.cityofchicago.org/api/views/<4x4-ID>/rows.csv?accessType=DOWNLOAD
```

## SoQL Essentials

### Query Parameters
| Param | Purpose | Example |
|-------|---------|---------|
| `$select` | Columns to return | `$select=date,primary_type,ward` |
| `$where` | Filter rows | `$where=year=2024` |
| `$group` | Aggregate | `$group=primary_type` |
| `$having` | Filter aggregates | `$having=count(*)>100` |
| `$order` | Sort results | `$order=date DESC` |
| `$limit` | Max rows | `$limit=500` |
| `$offset` | Skip rows | `$offset=1000` |

### Syntax Rules
- Backticks around column names: `` `column_name` ``
- Single quotes for strings: `'value'`
- Dates as ISO strings: `'2024-01-01T00:00:00'`

### Common Filters
```sql
-- Date range
$where=date >= '2024-01-01' AND date < '2025-01-01'

-- Text matching (case-insensitive)
$where=upper(primary_type) = 'THEFT'

-- Null handling
$where=ward IS NOT NULL

-- Multiple values
$where=primary_type IN ('THEFT', 'BATTERY', 'ASSAULT')
```

### Aggregations
```sql
$select=primary_type, count(*) as total
$group=primary_type
$order=total DESC
```

See `references/soql-quick-ref.md` for full function reference.

## Geospatial Queries

If the dataset has a location field (Point type):

```sql
-- Within radius (meters)
$where=within_circle(location, 41.8781, -87.6298, 1000)

-- Within bounding box
$where=within_box(location, 42.0, -87.9, 41.6, -87.5)

-- Within polygon
$where=within_polygon(location, 'MULTIPOLYGON(((-87.6 41.8, -87.5 41.8, -87.5 41.9, -87.6 41.9, -87.6 41.8)))')
```

## App Tokens

Unauthenticated requests are rate-limited. Register for a free app token:

1. Create account at https://data.cityofchicago.org
2. Go to Developer Settings
3. Create New App Token
4. Use via header: `X-App-Token: YOUR_TOKEN`

## Output Format

Provide the user with:
1. **Dataset**: Name + 4x4 ID + portal link
2. **Columns used**: Exact field names
3. **Query**: Formatted SoQL
4. **How to run**: curl command or full URL
5. **Assumptions**: Time zone, update frequency, any caveats

### Example Response Format
```
Dataset: Crimes - 2001 to Present (ijzp-q8t2)
https://data.cityofchicago.org/d/ijzp-q8t2

Query:
SELECT date, primary_type, description, ward, latitude, longitude
WHERE date >= '2024-01-01' AND primary_type = 'THEFT'
ORDER BY date DESC
LIMIT 100

Run it:
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$select=date,primary_type,description,ward,latitude,longitude&\$where=date%20%3E=%20%272024-01-01%27%20AND%20primary_type%20=%20%27THEFT%27&\$order=date%20DESC&\$limit=100"

Note: Data updates daily. Dates are in Chicago local time (America/Chicago).
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 404 / "unknown column" | Wrong dataset ID or field name. Check metadata endpoint. |
| Empty results | Filters too strict, wrong date format, or nulls. |
| 429 throttled | Add X-App-Token header. |
| Slow query | Select fewer columns, add filters, reduce limit. |
| Encoding errors | URL-encode special chars: space=%20, >=%3E, '=%27 |

## Additional Resources

- **`references/popular-datasets.md`** - Common Chicago datasets with IDs
- **`references/soql-quick-ref.md`** - All SoQL functions
- **`examples/python-query.py`** - Python code snippet
- **`examples/curl-examples.sh`** - curl command templates
