---
name: harvest-structured
description: Structured data extraction - tables, pricing, products, API endpoints with schema
allowed-tools: [Bash, Read, Write, WebFetch]
keywords: [scrape, structured, data, extract, schema, table, pricing, product, json, csv]
---

# Harvest Structured

Extract structured data from web pages using user-defined schemas. Turns messy HTML into clean JSON/CSV - pricing tables, product listings, API endpoint docs, comparison matrices.

## Usage

```
/scrape <url> --schema "<field descriptions>"
```

## Examples

```bash
# Extract pricing data
/scrape https://example.com/pricing --schema "plan_name, price, features[], cta_text"

# Extract product listings
/scrape https://store.example.com/products --schema "name, price, rating, reviews_count, image_url"

# Extract API endpoints
/scrape https://docs.api.com/reference --schema "method, path, description, parameters[], response_code"
```

## Schema Definition

Define fields as comma-separated names. Use `[]` for arrays:

```
name            → Single text value
price           → Single value (auto-detects currency)
features[]      → Array of items
description     → Long text
url             → Auto-detects links
image_url       → Auto-detects image sources
```

## How It Works

1. Fetch page content
2. Parse schema definition
3. Use CSS selectors or LLM extraction to match fields
4. Validate extracted data against schema
5. Output as JSON (default) or CSV

## Output Format

### JSON (default)
```json
[
  {
    "plan_name": "Pro",
    "price": "$29/mo",
    "features": ["Unlimited projects", "Priority support", "API access"],
    "source_url": "https://example.com/pricing"
  }
]
```

### CSV
```csv
plan_name,price,features,source_url
Pro,"$29/mo","Unlimited projects; Priority support; API access",https://example.com/pricing
```

## Integration

- **growth**: Competitor pricing extraction
- **migrator**: Changelog/breaking changes extraction
- **tech-radar**: Feature comparison across tools
- **data-analyst**: Structured data for analysis

## Rules

- Only extract publicly visible data
- Respect rate limits (1 req/sec)
- Validate schema before extraction
- Report confidence per field (high/medium/low)
- Output includes source URL for every record
