---
name: product-spec-bulk-fetch
description: Fetch structured FF&E product specs from a list of URLs. Extracts name, brand, dimensions, materials, price, and images into a standardized schedule.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - AskUserQuestion
  - mcp__google__sheets_values_get
  - mcp__google__sheets_values_update
  - mcp__google__sheets_spreadsheet_get
---

# /product-spec-bulk-fetch — Bulk Product Spec Fetcher

Extract structured FF&E data from a list of product page URLs. Outputs a standardized schedule ready for design specs, procurement, or import into Canoa.

## Input

The user provides product URLs in one of these ways:

1. **Inline list** — URLs pasted directly in the message (one per line, or comma-separated)
2. **File path** — A `.txt`, `.csv`, or `.md` file containing URLs (one per line)
3. **Google Sheet column** — A spreadsheet ID + column containing URLs to re-fetch

If the input format is unclear, ask.

## Output Schema

Products are written to the **master Google Sheet** — the same 33-column schema used by Norma Jean, `/product-research`, and all other data-management skills. When writing to CSV, use the same column order.

Read `../../schema/product-schema.md` (relative to this SKILL.md) for the full column reference, field formats, and category vocabulary. Read `../../schema/sheet-conventions.md` for CRUD patterns with MCP tools.

Skill-specific column values:
- **AF (Status):** `saved`
- **AG (Source):** `bulk-fetch`
- **AD (Tags):** Blank (set by user later)
- **AE (Notes):** Blank
- **S (Selected Color/Finish):** Blank (unknown from URL)

## Extraction Process

For each URL:

1. **Fetch the page** using WebFetch with the prompt below
2. **Parse the response** into the schema fields
3. **Flag issues** — missing price, missing dimensions, non-product page
4. **Continue to next URL** — never stop the batch on a single failure

### WebFetch Extraction Prompt

Use this prompt (or close variant) for each URL:

```
Extract structured product/furniture specification data from this page. Return a JSON object with these exact fields:

- product_name: Full product name (Title Case)
- description: Short description or tagline (1-2 sentences), or null
- sku: Product ID, SKU, model number, or catalog number, or null
- brand: Manufacturer name (Title Case)
- designer: Designer or design studio name if attributed, or null
- vendor: The retailer/website selling the product (may differ from brand), or null
- collection: Product line or collection name, or null
- category: One of: Chair, Table, Sofa, Bed, Light, Storage, Desk, Shelving, Rug, Mirror, Accessory, Tabletop, Kitchen, Bath, Window, Door, Outdoor Furniture, Textile, Acoustic, Planter, Partition, Other
- width: Numeric width value only (no units), or null
- depth: Numeric depth value only (no units), or null
- height: Numeric height value only (no units), or null
- seat_height: Numeric seat height for seating products, or null
- unit: "in", "cm", or "mm" — whichever the page uses
- weight: Weight as stated with unit (e.g. "45 lbs"), or null
- materials: Comma-separated list of primary materials
- colors_finishes: Comma-separated list of ALL available colors or finish options
- list_price: Numeric price (no currency symbol, no commas), or null
- sale_price: Discounted/sale price if shown, or null
- currency: "USD", "EUR", "GBP", etc.
- lead_time: Delivery estimate as stated, or null
- warranty: Warranty info as stated, or null
- certifications: Comma-separated certifications (GREENGUARD, FSC, BIFMA, etc.), or null
- com_col: "COM", "COL", "COM/COL" if mentioned, or null
- indoor_outdoor: "Indoor", "Outdoor", or "Indoor/Outdoor" if specified, or null
- image_url: URL of the primary product image (largest/hero image)

If this is NOT a product page, return: {"error": "not_a_product_page"}
If dimensions use a combined format like "32 x 24 x 30 in", split them into W x D x H.
If price says "Contact for pricing" or similar, set price to null.
Return ONLY the JSON object, no other text.
```

## Workflow

### Step 1: Parse input
Extract all URLs from the user's input. Report count: "Found N product URLs."

### Step 2: Fetch in parallel
Process URLs using WebFetch. Use parallel tool calls — fetch up to 5 URLs simultaneously to maximize speed. Report progress after each batch.

### Step 3: Compile results
Build a results table. Group into:
- **Successful** — all key fields extracted
- **Partial** — some fields missing (still include in output)
- **Failed** — non-product page or fetch error

### Step 4: Present results
Show a summary table in markdown with all successful + partial results. Flag any issues:
- "Price not found" for trade/dealer sites
- "Dimensions not found" if missing
- "Failed to fetch" for errors

### Step 5: Ask about output format
Ask the user: **"Where should I save this?"**
Options:
- **Master Google Sheet** — append rows to the shared product library (same sheet used by Norma Jean). Ask for spreadsheet ID if not already known.
- **Local CSV** — save to a specified path (default: `~/Documents/Work-Docs/ffe-fetch-YYYY-MM-DD.csv`)
- **Just the table** — leave as markdown in the conversation

### Step 6: Save
Write the output in the chosen format using the 33-column master schema. For Google Sheets, use `mcp__google__sheets_values_update` to append rows. Set `Clipped At` to current timestamp and `Source` to `bulk-fetch`.

## CSV Format

When saving to CSV, use the CSV header from `../../schema/product-schema.md`.

## Edge Cases

- **Redirects or blocked pages**: Note the URL as failed, move on
- **Multiple products on one page**: Extract only the primary/featured product
- **Non-English pages**: Extract data as-is, note the language. The cleanup skill handles translation.
- **Vendor sites requiring login**: Will likely fail — note as "Login required" and move on
- **Duplicate URLs in input**: Skip duplicates, note them

## Error Reporting

After the batch completes, always report:
```
Fetched: X/Y successful, Z partial, W failed
```
List any failed URLs with the reason.
