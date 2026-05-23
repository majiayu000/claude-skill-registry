---
name: cook-county-data-portal
description: This skill should be used when the user asks to "query Cook County data", "find Cook County datasets", "get property assessments", "download parcel data", "search datacatalog.cookcountyil.gov", "get medical examiner data", "find court cases", "query State's Attorney data", or mentions Cook County government data (assessor, treasurer, courts, payroll, medical examiner, etc.).
version: 1.1.0
---

# Cook County Data Portal Skill

Query and download datasets from the Cook County Open Data Portal using the Socrata Open Data API (SODA) and SoQL.

## Prerequisites

Before querying, check if the user has an app token:

1. Look for `COOK_COUNTY_DATA_PORTAL_TOKEN` in the user's `.env` file
2. If not found, check for `CHICAGO_DATA_PORTAL_TOKEN` (both portals use Socrata, so tokens are interchangeable)
3. If found, use it in requests via header: `X-App-Token: <token>`
4. If neither token exists, instruct the user to:
   - Sign up at https://datacatalog.cookcountyil.gov/signup (or https://data.cityofchicago.org/signup)
   - Create an app token in Developer Settings
   - Add to `.env`: `COOK_COUNTY_DATA_PORTAL_TOKEN=your_token_here`

Queries work without a token but are rate-limited.

## Quick Start

The Cook County Data Portal is at `datacatalog.cookcountyil.gov`. Each dataset has a unique 4x4 ID (e.g., `uzyt-m557` for assessed values). Use the catalog API to discover datasets, then query via SODA.

## Workflow

### Step 1: Clarify the Data Need

Ask the user:
- **Topic**: What data? (property assessments, court cases, payroll, medical examiner, etc.)
- **Geography**: Countywide, township, municipality, or specific parcel/PIN?
- **Time window**: Date range, tax year, or fiscal quarter?
- **Output**: JSON (code) or CSV (Excel)?
- **Granularity**: Raw rows or aggregated counts?

### Step 2: Find the Dataset

**Option A - Catalog Search API:**
```
GET https://api.us.socrata.com/api/catalog/v1?domains=datacatalog.cookcountyil.gov&q=<keywords>
```

**Option B - Portal UI:**
Browse https://datacatalog.cookcountyil.gov and use the search bar.

Deliverable: Dataset name, 4x4 ID, and API endpoint.

See `references/datasets-*.md` for commonly requested datasets by category:
- `references/datasets-property.md` - Assessor, Treasurer, parcel data
- `references/datasets-courts.md` - State's Attorney, sentencing, dispositions
- `references/datasets-health.md` - Medical Examiner cases
- `references/datasets-finance.md` - Payroll, procurement, budgets

### Step 3: Get Dataset Metadata

Fetch schema and column info:
```
GET https://datacatalog.cookcountyil.gov/api/views/<4x4-ID>
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
https://datacatalog.cookcountyil.gov/resource/<4x4-ID>.json?$where=<filter>&$limit=1000
```

**SODA3 POST (complex queries):**
```bash
curl -X POST \
  -H "X-App-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * WHERE year = 2024", "page": {"pageNumber": 1, "pageSize": 1000}}' \
  https://datacatalog.cookcountyil.gov/api/v3/views/<4x4-ID>/query.json
```

### Step 5: Handle Pagination

Default limit is 1000 rows. For larger extracts:
```
$limit=1000&$offset=0    # Page 1
$limit=1000&$offset=1000 # Page 2
```

Always include `$order` for stable paging:
```
$order=year DESC&$limit=1000&$offset=0
```

For full dataset export, use CSV:
```
https://datacatalog.cookcountyil.gov/api/views/<4x4-ID>/rows.csv?accessType=DOWNLOAD
```

## SoQL Essentials

### Query Parameters
| Param | Purpose | Example |
|-------|---------|---------|
| `$select` | Columns to return | `$select=pin,year,mailed_tot` |
| `$where` | Filter rows | `$where=year=2024` |
| `$group` | Aggregate | `$group=township_code` |
| `$having` | Filter aggregates | `$having=count(*)>100` |
| `$order` | Sort results | `$order=year DESC` |
| `$limit` | Max rows | `$limit=500` |
| `$offset` | Skip rows | `$offset=1000` |

### Syntax Rules
- Backticks around column names: `` `column_name` ``
- Single quotes for strings: `'value'`
- Dates as ISO strings: `'2024-01-01T00:00:00'`

### Common Filters
```sql
-- Year range
$where=year >= 2020 AND year <= 2024

-- PIN lookup (zero-pad to 14 digits)
$where=pin = '12345678901234'

-- Text matching (case-insensitive)
$where=upper(manner_of_death) = 'HOMICIDE'

-- Null handling
$where=latitude IS NOT NULL

-- Multiple values
$where=township_code IN ('10', '20', '30')
```

### Aggregations
```sql
$select=township_code, count(*) as total, avg(mailed_tot) as avg_value
$group=township_code
$order=total DESC
```

See `references/soql-quick-ref.md` for full function reference.

## Geospatial Queries

If the dataset has a location field (Point type):

```sql
-- Within radius (meters from downtown Chicago)
$where=within_circle(location, 41.8781, -87.6298, 5000)

-- Within bounding box
$where=within_box(location, 42.0, -87.9, 41.6, -87.5)

-- Within polygon
$where=within_polygon(location, 'MULTIPOLYGON(((-87.6 41.8, -87.5 41.8, -87.5 41.9, -87.6 41.9, -87.6 41.8)))')
```

## App Tokens

Unauthenticated requests are rate-limited. Register for a free app token:

1. Create account at https://datacatalog.cookcountyil.gov
2. Go to Developer Settings
3. Create New App Token
4. Use via header: `X-App-Token: YOUR_TOKEN`

## Cook County Specifics

### Parcel Index Numbers (PINs)
- PINs are 14-digit identifiers for parcels
- Always zero-pad when querying: `'01234567890123'`
- Some exports may drop leading zeros; re-pad before joining datasets

### Tax Years vs Calendar Years
- Assessor data uses **tax year** (property taxes assessed)
- Tax year 2024 bills are paid in 2025
- Use `year` or `tax_year` columns accordingly

### Townships
- Cook County has 38 townships
- Township codes are 2-digit strings (e.g., `'10'` = Barrington)
- See Assessor datasets for township boundaries

### Fiscal Quarters (Payroll)
- Q1: December - February
- Q2: March - May
- Q3: June - August
- Q4: September - November

## Output Format

Provide the user with:
1. **Dataset**: Name + 4x4 ID + portal link
2. **Columns used**: Exact field names
3. **Query**: Formatted SoQL
4. **How to run**: curl command or full URL
5. **Assumptions**: Time zone, update frequency, any caveats

### Example Response Format
```
Dataset: Assessor - Assessed Values (uzyt-m557)
https://datacatalog.cookcountyil.gov/d/uzyt-m557

Query:
SELECT pin, year, class, mailed_tot, certified_tot
WHERE year = 2024 AND township_code = '70'
ORDER BY mailed_tot DESC
LIMIT 100

Run it:
curl "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$select=pin,year,class,mailed_tot,certified_tot&\$where=year%20=%202024%20AND%20township_code%20=%20%2770%27&\$order=mailed_tot%20DESC&\$limit=100"

Note: Values are assessed values, not market values. Adjust by level of assessment to get market value.
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 404 / "unknown column" | Wrong dataset ID or field name. Check metadata endpoint. |
| Empty results | Filters too strict, wrong date format, or nulls. |
| 429 throttled | Add X-App-Token header. |
| Slow query | Select fewer columns, add filters, reduce limit. |
| Encoding errors | URL-encode special chars: space=%20, >=%3E, '=%27 |
| PIN not found | Zero-pad to 14 digits. |

## Additional Resources

- **`references/datasets-property.md`** - Property & Taxation datasets
- **`references/datasets-courts.md`** - Courts & Legal datasets
- **`references/datasets-health.md`** - Health & Medical Examiner datasets
- **`references/datasets-finance.md`** - Finance & Administration datasets
- **`references/soql-quick-ref.md`** - All SoQL functions
- **`examples/python-query.py`** - Python code snippet
- **`examples/curl-examples.sh`** - curl command templates
