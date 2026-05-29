---
name: product-data-import
description: Generate a formatted FF&E specification schedule from raw product data — notes, CSV, or pasted lists. Outputs a structured schedule compatible with the 33-column master schema.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__update_cells
  - mcp__google-sheets__list_sheets
---

# /product-data-import — Product Data Importer

Takes raw, unstructured product data and formats it into a proper FF&E specification schedule. Input can be notes, a CSV, a pasted spreadsheet, or a conversation. Output is a formatted schedule as markdown, CSV, or written to a Google Sheet — using the same 33-column schema as `/product-research`, `/product-spec-bulk-fetch`, and other product skills.

## When to Use

- Designer has a list of products in notes or conversation and needs it formatted for a deliverable
- A rough product list needs to become a spec-ready schedule with item numbers, quantities, and extended pricing
- Products from multiple sources need to be consolidated into one formatted schedule
- An existing schedule needs to be reformatted to match the standard schema

## Step 1: Accept Input

The designer provides product data in any format:

**Raw notes:**
```
3x Eames Lounge Chair, Herman Miller, walnut/black leather, $5,695 each
2x Nelson Platform Bench 48", Herman Miller, natural maple, $2,195
1x Noguchi Coffee Table, Herman Miller, walnut/glass, $2,095
Pendant light for above the table - something by Flos, budget $800-1200
```

**Pasted spreadsheet or CSV:**
```
Product, Brand, Qty, Price
Eames Lounge Chair, Herman Miller, 3, $5695
Nelson Bench 48, Herman Miller, 2, $2195
```

**A file path:**
```
/product-data-import ~/Documents/project/product-list.csv
```

**Conversational:**
```
"We need 8 task chairs — Steelcase Leap V2, black, about $1,200 each.
 Also 4 monitor arms, any brand, under $300."
```

Accept whatever the designer gives. Don't ask for more structure — work with what you have.

## Step 2: Parse and Enrich

For each product in the input:

1. **Extract known fields:** product name, brand, quantity, price, dimensions, materials, finish, category
2. **Fill in from knowledge:** If the product is well-known (Eames Lounge Chair, Steelcase Leap, etc.), fill in standard dimensions, materials, and weight from your training data. Mark these as "from reference" in notes.
3. **Assign categories:** Map to the canonical vocabulary defined in `../../schema/product-schema.md`
4. **Calculate extended prices:** Unit price × quantity
5. **Assign item numbers:** Sequential within each category group (S-01, S-02 for Seating; T-01 for Tables; L-01 for Lighting, etc.)
6. **Flag unknowns:** If a product is vague ("pendant light, Flos, $800-1200"), note it as "TBD — needs specification" and include budget range

### Category prefixes for item numbers

Item number prefixes are defined in `../../schema/product-schema.md` under **Item Number Prefixes**. Read that file for the full mapping of canonical categories to prefixes (e.g. Chair → S, Table → T, Light → L).

## Step 3: Present the Schedule

Show the formatted schedule as a markdown table:

```
## FF&E Schedule — [Project Name if known]

[n] items · [total qty] units · $[total extended] estimated

| Item # | Product | Brand | Qty | W | D | H | Unit | Materials | Finish | Unit $ | Ext $ | Lead | Notes |
|--------|---------|-------|-----|---|---|---|------|-----------|--------|--------|-------|------|-------|
| S-01 | Eames Lounge Chair | Herman Miller | 3 | 32.75 | 32.5 | 33.5 | in | Molded plywood, leather | Walnut/Black | $5,695 | $17,085 | 8-12w | |
| T-01 | Nelson Platform Bench 48" | Herman Miller | 2 | 48 | 18.5 | 14 | in | Solid maple | Natural | $2,195 | $4,390 | 6-8w | |
| T-02 | Noguchi Coffee Table | Herman Miller | 1 | 50 | 36 | 15.75 | in | Walnut, glass | — | $2,095 | $2,095 | 6-8w | |
| L-01 | TBD Pendant | Flos | 1 | — | — | — | — | — | — | $800-$1,200 | $800-$1,200 | — | Needs specification |

**Subtotals by category:**
- Seating: $17,085 (3 units)
- Tables: $6,485 (3 units)
- Lighting: $800-$1,200 (1 unit, TBD)
- **Total: $24,370-$24,770**
```

### Presentation rules

- **Group by category**, sorted by item number within each group
- **Show subtotals** per category and a grand total
- **Flag TBD items** clearly — include budget range if given
- **Show dimensions** from reference data when you know the product; leave blank and note "dims TBD" when you don't
- **Don't fabricate prices** — if you're unsure, note "price TBD" or "estimated" and use the designer's stated budget
- **Currency** — default USD unless the designer specifies otherwise

## Step 4: Ask for Output Format

Ask the designer how they want the schedule:

1. **Markdown** — stay in conversation (already shown)
2. **CSV file** — save as `.csv` to the current directory or a specified path
3. **Google Sheet** — write to the master product library using the 33-column schema

If the designer doesn't specify, default to saving a CSV file.

## Step 5: Save

### CSV output

Save as `product-data-import-[date].csv` with these columns:

```
Item #, Product Name, Brand, Category, Qty, W, D, H, Unit, Materials, Finish, Unit Price, Extended Price, Lead Time, Notes
```

### Google Sheet output

If the designer provides a Sheet ID or says "save to my sheet", write to the 33-column master schema. Read `../../schema/product-schema.md` (relative to this SKILL.md) for the full column reference, field formats, and category vocabulary. Read `../../schema/sheet-conventions.md` for CRUD patterns with MCP tools.

Skill-specific column values:
- **AG (Source):** `product-data-import`
- **AF (Status):** `specified`
- **AD (Tags):** Item number (e.g. "S-01") + any project tags
- **AE (Notes):** `Qty: 3 · Ext: $17,085` (quantity and extended price, since the schema has no dedicated Qty column)

### Quantity handling

The master sheet is one row per product, not per unit. Put the quantity in the Notes column (e.g., "Qty: 3") since the 33-column schema doesn't have a dedicated quantity column. Also include the extended price in Notes: "Qty: 3 · Ext: $17,085".

## Step 6: Summary

After saving:

```
✓ FF&E Schedule saved to [path or sheet]
  [n] line items · [total qty] units · $[total] estimated
  [n] items fully specified, [n] items need specification (TBD)
```

If there are TBD items, offer to research them:

```
Want me to research the TBD items? I can use /product-research to find specific products for:
- L-01: Flos pendant, $800-$1,200 budget
```

## Pairs With

- `/product-research` — research specific products to fill TBD slots
- `/product-spec-bulk-fetch` — pull full specs from product URLs
- `/product-data-cleanup` — normalize the schedule after assembly
- `/product-enrich` — auto-tag categories, colors, and materials
- `/csv-to-sif` — convert the schedule to SIF for dealer procurement
