---
name: product-enrich
description: Auto-tag FF&E products with categories, colors, materials, and style tags using AI.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google__sheets_values_get
  - mcp__google__sheets_values_update
  - mcp__google__sheets_spreadsheet_get
user-invocable: true
---

# /product-enrich — Product Enrichment

Takes a product list with basic info (name + brand) and fills in missing metadata — category, subcategory, primary color, material, and style tags — using AI. Works on CSV files, Google Sheets, or pasted data.

## When to Use

- After a bulk import where products are missing categories or tags
- When a designer clips products quickly without filling in details
- To standardize metadata across products from different sources
- Before generating an FF&E schedule (enriched data makes better schedules)

## Step 1: Accept Input

Accept product data in any format:

**Google Sheet ID:**
```
/product-enrich 1FMScYW9guezOWc_m4ClTQxxFIpS6TNRr373R-MJGzgE
```

**CSV file:**
```
/product-enrich ~/Documents/project/products.csv
```

**Pasted data:**
```
/product-enrich
Eames Lounge Chair, Herman Miller
Saarinen Tulip Table, Knoll
PH 5 Pendant, Louis Poulsen
Togo Sofa, Ligne Roset
```

## Step 2: Analyze Each Product

For each product, infer the following fields:

### Category
Map to the canonical vocabulary (22 terms) defined in `../../schema/product-schema.md`.

### Subcategory
More specific classification within the category:
- Chair → Task Chair, Lounge Chair, Dining Chair, Side Chair, Stool, Bench
- Table → Dining Table, Coffee Table, Side Table, Console Table, Conference Table
- Light → Pendant, Floor Lamp, Table Lamp, Wall Sconce, Ceiling, Task Light, Chandelier
- Sofa → Sofa, Sectional, Loveseat, Daybed, Settee
- Storage → Credenza, Bookcase, Filing Cabinet, Wardrobe, Sideboard, Dresser
- Desk → Writing Desk, Executive Desk, Standing Desk, Workstation

### Primary Color
The dominant color of the product as typically sold:
- Use standard color names: Black, White, Gray, Brown, Beige, Navy, Blue, Green, Red, Orange, Yellow, Pink, Purple, Natural, Walnut, Oak, Teak, Chrome, Brass, Copper, Multi

### Material
Primary materials, comma-separated:
- Wood (specify type if known: Walnut, Oak, Maple, Teak, Birch, Ash, Beech)
- Metal (specify: Steel, Aluminum, Brass, Chrome, Iron, Copper)
- Upholstery (specify: Leather, Fabric, Velvet, Bouclé, Mohair, Linen, Wool)
- Other: Glass, Marble, Concrete, Ceramic, Plastic, Fiberglass, Rattan, Cane, Acrylic

### Style Tags
2-4 descriptive tags from:
- Period/movement: Mid-Century Modern, Art Deco, Bauhaus, Scandinavian, Japanese, Industrial, Contemporary, Traditional, Minimalist, Postmodern, Memphis
- Character: Organic, Geometric, Sculptural, Modular, Stackable, Compact, Statement, Classic, Iconic
- Context: Residential, Contract, Hospitality, Healthcare, Education, Outdoor

### Image Analysis
If the product data includes an image URL (column AC in the master schema), use Claude vision to verify and refine the enrichment. The image may reveal:
- Actual color (not just what the name suggests)
- Material details not in the product name
- Style characteristics

## Step 3: Present Preview

Show a preview of the enrichment before applying:

```
## Product Enrichment Preview

| Product | Brand | Category | Subcategory | Color | Material | Style Tags |
|---------|-------|----------|-------------|-------|----------|------------|
| Eames Lounge Chair | Herman Miller | Chair | Lounge Chair | Walnut/Black | Molded plywood, Leather | Mid-Century Modern, Iconic, Residential |
| Saarinen Tulip Table | Knoll | Table | Dining Table | White | Marble, Aluminum | Mid-Century Modern, Sculptural, Organic |
| PH 5 Pendant | Louis Poulsen | Light | Pendant | White | Aluminum | Scandinavian, Classic, Iconic |
| Togo Sofa | Ligne Roset | Sofa | Sofa | Brown | Fabric | Contemporary, Organic, Sculptural |

4 products enriched. Apply? (y/n)
```

Flag any products where enrichment is uncertain:
```
⚠ "Custom Reception Desk" — unknown product, category set to Desk but verify
```

## Step 4: Apply

### To Google Sheet
Write enriched fields to the master 33-column schema:
- Column J (Category) — enriched category
- Column Q (Materials) — enriched materials
- Column R (Colors/Finishes) — enriched color
- Column AD (Tags) — enriched style tags, appended to existing tags

Do NOT overwrite existing values unless the field is empty or the user explicitly asks to overwrite.

### To CSV
Add new columns if they don't exist: Category, Subcategory, Primary Color, Material, Style Tags. Save as `{original-name}-enriched.csv`.

### To conversation
Output the enriched table in markdown.

## Step 5: Summary

```
✓ Enriched 4 products
  Categories: 4 assigned (0 already had values)
  Colors: 4 assigned
  Materials: 4 assigned
  Style tags: 14 total tags across 4 products
  Uncertain: 1 (flagged for review)
```

## Pairs With

- `/product-spec-bulk-fetch` — fetch specs first, then enrich the results
- `/product-spec-bulk-cleanup` — cleanup normalizes formatting, enrich adds metadata
- `/ffe-schedule` — enriched products make better formatted schedules
- `/product-match` — enriched tags help find better matches
